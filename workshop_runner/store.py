from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import tempfile
import unicodedata
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterator

from .catalog import Exercise
from .config import Settings
from .routing import next_slot


EDITABLE_FILES = ("index.html", "styles.css", "app.js")


class StoreError(RuntimeError):
    pass


class AuthenticationError(StoreError):
    pass


class ConflictError(StoreError):
    pass


class NotFoundError(StoreError):
    pass


class ValidationError(StoreError):
    pass


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _deadline(stage: int) -> str:
    seconds = 480 if stage == 1 else 240
    return (datetime.now(UTC) + timedelta(seconds=seconds)).isoformat()


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def normalize_nickname(nickname: str) -> tuple[str, str]:
    display = unicodedata.normalize("NFKC", nickname).strip()
    if not 2 <= len(display) <= 32:
        raise ValidationError("Nickname must contain 2–32 characters")
    if any(character in "\r\n\t/\\" or ord(character) < 32 for character in display):
        raise ValidationError("Nickname contains unsupported characters")
    return display, display.casefold()


@dataclass(frozen=True)
class Session:
    token: str
    user_id: int
    nickname: str
    slot: int


class Store:
    def __init__(self, settings: Settings, exercises: list[Exercise]):
        self.settings = settings
        self.exercises = {exercise.slug: exercise for exercise in exercises}
        self.settings.ensure_directories()
        self._initialize_schema()
        self._recover_unfinished_publications()
        self._recover_interrupted_runs()
        self._initialize_catalog_and_work_items(exercises)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(
            self.settings.database_path,
            timeout=30,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        try:
            yield connection
        finally:
            connection.close()

    def _initialize_schema(self) -> None:
        with self.connect() as db:
            db.execute("PRAGMA journal_mode = WAL")
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS workshop (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    state TEXT NOT NULL,
                    participant_count INTEGER NOT NULL,
                    routing_mode TEXT NOT NULL,
                    active_slugs_json TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nickname TEXT NOT NULL,
                    nickname_key TEXT NOT NULL UNIQUE,
                    slot INTEGER NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS login_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    token_hash TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL,
                    revoked_at TEXT
                );

                CREATE TABLE IF NOT EXISTS exercise_definitions (
                    slug TEXT PRIMARY KEY,
                    number INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    spec0 TEXT NOT NULL,
                    source_path TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS exercise_deltas (
                    exercise_slug TEXT NOT NULL REFERENCES exercise_definitions(slug),
                    delta_number INTEGER NOT NULL CHECK (delta_number BETWEEN 1 AND 12),
                    task_text TEXT NOT NULL,
                    PRIMARY KEY (exercise_slug, delta_number)
                );

                CREATE TABLE IF NOT EXISTS work_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_slug TEXT NOT NULL UNIQUE REFERENCES exercise_definitions(slug),
                    workspace_dir TEXT NOT NULL UNIQUE,
                    author_user_id INTEGER REFERENCES users(id),
                    author_slot INTEGER,
                    state TEXT NOT NULL DEFAULT 'pending',
                    current_stage INTEGER NOT NULL DEFAULT 0,
                    version INTEGER NOT NULL DEFAULT 0,
                    last_agent_response TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    work_item_id INTEGER NOT NULL REFERENCES work_items(id),
                    stage_number INTEGER NOT NULL CHECK (stage_number BETWEEN 1 AND 13),
                    kind TEXT NOT NULL CHECK (kind IN ('delta', 'author_review')),
                    assignee_user_id INTEGER NOT NULL REFERENCES users(id),
                    status TEXT NOT NULL CHECK (status IN ('queued', 'active', 'completed')),
                    incoming_response TEXT NOT NULL DEFAULT '',
                    current_response TEXT NOT NULL DEFAULT '',
                    selected_run_id INTEGER,
                    revision INTEGER NOT NULL DEFAULT 0,
                    queued_at TEXT NOT NULL,
                    opened_at TEXT,
                    deadline_at TEXT,
                    completed_at TEXT,
                    UNIQUE (work_item_id, stage_number)
                );

                CREATE UNIQUE INDEX IF NOT EXISTS one_active_assignment_per_user
                ON assignments(assignee_user_id) WHERE status = 'active';

                CREATE TABLE IF NOT EXISTS prompt_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id INTEGER NOT NULL REFERENCES assignments(id),
                    actor_user_id INTEGER NOT NULL REFERENCES users(id),
                    ordinal INTEGER NOT NULL,
                    client_request_id TEXT NOT NULL UNIQUE,
                    agent_session_id TEXT NOT NULL UNIQUE,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL DEFAULT '',
                    runtime TEXT NOT NULL,
                    model TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('running', 'succeeded', 'failed')),
                    activities_json TEXT NOT NULL DEFAULT '[]',
                    changed_files_json TEXT NOT NULL DEFAULT '[]',
                    before_hash TEXT,
                    after_hash TEXT,
                    error_text TEXT,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    UNIQUE (assignment_id, ordinal)
                );

                CREATE UNIQUE INDEX IF NOT EXISTS one_running_prompt_per_assignment
                ON prompt_runs(assignment_id) WHERE status = 'running';

                CREATE TABLE IF NOT EXISTS run_file_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_run_id INTEGER NOT NULL REFERENCES prompt_runs(id),
                    phase TEXT NOT NULL CHECK (phase IN ('before', 'after')),
                    relative_path TEXT NOT NULL,
                    content TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    UNIQUE (prompt_run_id, phase, relative_path)
                );

                CREATE TABLE IF NOT EXISTS publication_journal (
                    run_id INTEGER PRIMARY KEY REFERENCES prompt_runs(id),
                    work_item_id INTEGER NOT NULL REFERENCES work_items(id),
                    workspace_dir TEXT NOT NULL,
                    before_files_json TEXT NOT NULL,
                    after_files_json TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('prepared', 'finalized', 'recovered')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS handoffs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    work_item_id INTEGER NOT NULL REFERENCES work_items(id),
                    from_assignment_id INTEGER NOT NULL UNIQUE REFERENCES assignments(id),
                    to_assignment_id INTEGER NOT NULL UNIQUE REFERENCES assignments(id),
                    selected_prompt_run_id INTEGER NOT NULL REFERENCES prompt_runs(id),
                    from_user_id INTEGER NOT NULL REFERENCES users(id),
                    to_user_id INTEGER NOT NULL REFERENCES users(id),
                    response_text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS final_interpretations (
                    work_item_id INTEGER PRIMARY KEY REFERENCES work_items(id),
                    assignment_id INTEGER NOT NULL REFERENCES assignments(id),
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    application_for TEXT NOT NULL,
                    primary_user TEXT NOT NULL,
                    final_action_causes TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS author_reviews (
                    work_item_id INTEGER PRIMARY KEY REFERENCES work_items(id),
                    assignment_id INTEGER NOT NULL REFERENCES assignments(id),
                    author_user_id INTEGER NOT NULL REFERENCES users(id),
                    notes TEXT NOT NULL DEFAULT '',
                    completed_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS idempotency_requests (
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    endpoint TEXT NOT NULL,
                    request_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, endpoint, request_key)
                );
                """
            )

    def _replace_workspace_files(
        self, workspace_dir: str | Path, files: dict[str, str]
    ) -> None:
        workspace = Path(workspace_dir).resolve()
        projects_root = self.settings.projects_dir.resolve()
        try:
            workspace.relative_to(projects_root)
        except ValueError as error:
            raise StoreError("Publication journal points outside the projects root") from error
        if set(files) != set(EDITABLE_FILES) or not workspace.is_dir():
            raise StoreError("Publication journal contains an invalid workspace snapshot")

        with tempfile.TemporaryDirectory(
            prefix=".workshop-recovery-", dir=workspace.parent
        ) as temporary:
            stage = Path(temporary)
            for filename in EDITABLE_FILES:
                (stage / filename).write_bytes(files[filename].encode("utf-8"))
            for filename in EDITABLE_FILES:
                os.replace(stage / filename, workspace / filename)

    def _recover_unfinished_publications(self) -> None:
        with self.connect() as db:
            rows = db.execute(
                "SELECT * FROM publication_journal WHERE status = 'prepared'"
            ).fetchall()
        for row in rows:
            try:
                before_files = json.loads(row["before_files_json"])
                self._replace_workspace_files(row["workspace_dir"], before_files)
            except Exception as error:
                raise StoreError(
                    f"Could not recover interrupted publication for run {row['run_id']}"
                ) from error
            now = utc_now()
            with self.connect() as db:
                db.execute("BEGIN IMMEDIATE")
                db.execute(
                    """
                    UPDATE prompt_runs
                    SET status = 'failed', error_text = ?, completed_at = ?
                    WHERE id = ? AND status = 'running'
                    """,
                    (
                        "Interrupted during file publication; restored previous files",
                        now,
                        row["run_id"],
                    ),
                )
                db.execute(
                    """
                    UPDATE publication_journal
                    SET status = 'recovered', updated_at = ?
                    WHERE run_id = ? AND status = 'prepared'
                    """,
                    (now, row["run_id"]),
                )
                db.execute("COMMIT")

    def _recover_interrupted_runs(self) -> None:
        """A fresh server cannot still own an in-progress model invocation."""
        with self.connect() as db:
            db.execute(
                """
                UPDATE prompt_runs
                SET status = 'failed', error_text = ?, completed_at = ?
                WHERE status = 'running'
                """,
                ("Interrupted by server restart; submit a new prompt", utc_now()),
            )

    def _initialize_catalog_and_work_items(self, exercises: list[Exercise]) -> None:
        configured_slugs = [exercise.slug for exercise in exercises]
        configured_json = json.dumps(configured_slugs)
        now = utc_now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute("SELECT * FROM workshop WHERE id = 1").fetchone()
            if existing:
                current_config = (
                    existing["participant_count"],
                    existing["routing_mode"],
                    existing["active_slugs_json"],
                )
                requested_config = (
                    self.settings.participant_count,
                    self.settings.routing_mode,
                    configured_json,
                )
                if current_config != requested_config:
                    user_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
                    if user_count:
                        db.execute("ROLLBACK")
                        raise StoreError(
                            "Workshop configuration differs from the existing database. "
                            "Use a new WORKSHOP_DATA_DIR for a new run."
                        )
                    db.execute("DELETE FROM work_items")
                    db.execute("DELETE FROM workshop WHERE id = 1")

            db.execute(
                """
                INSERT OR IGNORE INTO workshop
                    (id, state, participant_count, routing_mode, active_slugs_json, created_at)
                VALUES (1, 'lobby', ?, ?, ?, ?)
                """,
                (
                    self.settings.participant_count,
                    self.settings.routing_mode,
                    configured_json,
                    now,
                ),
            )

            for exercise in exercises:
                db.execute(
                    """
                    INSERT INTO exercise_definitions(slug, number, title, spec0, source_path)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(slug) DO UPDATE SET
                        number = excluded.number,
                        title = excluded.title,
                        spec0 = excluded.spec0,
                        source_path = excluded.source_path
                    """,
                    (
                        exercise.slug,
                        exercise.number,
                        exercise.title,
                        exercise.spec0,
                        str(exercise.source_path),
                    ),
                )
                for number, task in exercise.deltas.items():
                    db.execute(
                        """
                        INSERT INTO exercise_deltas(exercise_slug, delta_number, task_text)
                        VALUES (?, ?, ?)
                        ON CONFLICT(exercise_slug, delta_number)
                        DO UPDATE SET task_text = excluded.task_text
                        """,
                        (exercise.slug, number, task),
                    )

                existing_work_item = db.execute(
                    "SELECT id FROM work_items WHERE exercise_slug = ?",
                    (exercise.slug,),
                ).fetchone()
                workspace = (self.settings.projects_dir / exercise.slug).resolve()
                workspace.mkdir(parents=True, exist_ok=True)
                for filename in EDITABLE_FILES:
                    path = workspace / filename
                    if not path.exists():
                        path.touch()
                unexpected = sorted(
                    path.name for path in workspace.iterdir() if path.name not in EDITABLE_FILES
                )
                if unexpected:
                    db.execute("ROLLBACK")
                    raise StoreError(
                        f"Workspace {workspace} contains forbidden entries: {unexpected}"
                    )
                invalid_entries = [
                    path.name
                    for path in workspace.iterdir()
                    if path.is_symlink() or not path.is_file()
                ]
                if invalid_entries:
                    db.execute("ROLLBACK")
                    raise StoreError(
                        f"Workspace {workspace} contains invalid entries: {invalid_entries}"
                    )
                if existing_work_item is None and any(
                    (workspace / filename).read_text(encoding="utf-8").strip()
                    for filename in EDITABLE_FILES
                ):
                    db.execute("ROLLBACK")
                    raise StoreError(
                        f"New workshop workspace {workspace} is not empty. "
                        "Use a fresh WORKSHOP_DATA_DIR or WORKSHOP_PROJECTS_DIR."
                    )

                db.execute(
                    """
                    INSERT OR IGNORE INTO work_items
                        (exercise_slug, workspace_dir, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (exercise.slug, str(workspace), now, now),
                )
            db.execute("COMMIT")

    def login(self, nickname: str) -> Session:
        display, nickname_key = normalize_nickname(nickname)
        now = utc_now()
        token = secrets.token_urlsafe(32)
        expires = (datetime.now(UTC) + timedelta(days=7)).isoformat()

        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            user = db.execute(
                "SELECT * FROM users WHERE nickname_key = ?", (nickname_key,)
            ).fetchone()
            if user is None:
                workshop = db.execute(
                    "SELECT state FROM workshop WHERE id = 1"
                ).fetchone()
                if workshop["state"] != "lobby":
                    db.execute("ROLLBACK")
                    raise ConflictError(
                        "The workshop has already started; re-enter with your original nickname"
                    )
                used_slots = {
                    row[0] for row in db.execute("SELECT slot FROM users").fetchall()
                }
                slot = next(
                    (
                        candidate
                        for candidate in range(1, self.settings.participant_count + 1)
                        if candidate not in used_slots
                    ),
                    None,
                )
                if slot is None:
                    db.execute("ROLLBACK")
                    raise ConflictError("The workshop is full")
                cursor = db.execute(
                    """
                    INSERT INTO users(nickname, nickname_key, slot, created_at, last_seen_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (display, nickname_key, slot, now, now),
                )
                user_id = cursor.lastrowid
                user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            else:
                db.execute(
                    "UPDATE users SET nickname = ?, last_seen_at = ? WHERE id = ?",
                    (display, now, user["id"]),
                )

            db.execute(
                """
                INSERT INTO login_sessions
                    (user_id, token_hash, created_at, expires_at, last_seen_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user["id"], _token_hash(token), now, expires, now),
            )
            db.execute("COMMIT")
        return Session(token, user["id"], display, user["slot"])

    def admin_state(self) -> dict[str, Any]:
        with self.connect() as db:
            workshop = db.execute("SELECT * FROM workshop WHERE id = 1").fetchone()
            participants = [
                {"nickname": row["nickname"], "slot": row["slot"]}
                for row in db.execute(
                    "SELECT nickname, slot FROM users ORDER BY slot"
                ).fetchall()
            ]
            exercise_count = db.execute(
                "SELECT COUNT(*) FROM work_items"
            ).fetchone()[0]
            active_count = db.execute(
                "SELECT COUNT(*) FROM work_items WHERE state != 'pending'"
            ).fetchone()[0]
        return {
            "state": workshop["state"],
            "capacity": workshop["participant_count"],
            "minimum_participants": self.settings.minimum_participants,
            "registered_count": len(participants),
            "active_participant_count": active_count,
            "exercise_count": exercise_count,
            "participants": participants,
            "started_at": workshop["started_at"],
        }

    def start_workshop(self) -> dict[str, Any]:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            workshop = db.execute("SELECT * FROM workshop WHERE id = 1").fetchone()
            if workshop["state"] != "lobby":
                db.execute("ROLLBACK")
                raise ConflictError("The workshop has already started")

            users = db.execute("SELECT * FROM users ORDER BY slot").fetchall()
            user_count = len(users)
            if user_count < self.settings.minimum_participants:
                db.execute("ROLLBACK")
                raise ValidationError(
                    f"At least {self.settings.minimum_participants} participants must join before start"
                )

            work_items = db.execute(
                """
                SELECT wi.* FROM work_items wi
                JOIN exercise_definitions ed ON ed.slug = wi.exercise_slug
                ORDER BY ed.number
                LIMIT ?
                """,
                (user_count,),
            ).fetchall()
            if len(work_items) != user_count:
                db.execute("ROLLBACK")
                raise ValidationError(
                    f"{user_count} participants joined but only {len(work_items)} exercises are configured"
                )

            now = utc_now()
            for item, author in zip(work_items, users, strict=True):
                db.execute(
                    """
                    UPDATE work_items
                    SET author_user_id = ?, author_slot = ?, state = 'running',
                        current_stage = 1, updated_at = ?
                    WHERE id = ?
                    """,
                    (author["id"], author["slot"], now, item["id"]),
                )
                db.execute(
                    """
                    INSERT INTO assignments
                        (work_item_id, stage_number, kind, assignee_user_id, status,
                         queued_at, opened_at, deadline_at)
                    VALUES (?, 1, 'delta', ?, 'active', ?, ?, ?)
                    """,
                    (item["id"], author["id"], now, now, _deadline(1)),
                )
            db.execute(
                "UPDATE workshop SET state = 'running', started_at = ? WHERE id = 1",
                (now,),
            )
            db.execute("COMMIT")
        return self.admin_state()

    def authenticate(self, token: str) -> sqlite3.Row:
        if not token:
            raise AuthenticationError("Login required")
        now = utc_now()
        with self.connect() as db:
            row = db.execute(
                """
                SELECT u.*, s.id AS session_id, s.expires_at
                FROM login_sessions s
                JOIN users u ON u.id = s.user_id
                WHERE s.token_hash = ? AND s.revoked_at IS NULL AND s.expires_at > ?
                """,
                (_token_hash(token), now),
            ).fetchone()
            if row is None:
                raise AuthenticationError("Session is invalid or expired")
            db.execute(
                "UPDATE login_sessions SET last_seen_at = ? WHERE id = ?",
                (now, row["session_id"]),
            )
            return row

    def logout(self, token: str) -> None:
        with self.connect() as db:
            db.execute(
                "UPDATE login_sessions SET revoked_at = ? WHERE token_hash = ?",
                (utc_now(), _token_hash(token)),
            )

    def _activate_next(self, db: sqlite3.Connection, user_id: int) -> None:
        active = db.execute(
            "SELECT id FROM assignments WHERE assignee_user_id = ? AND status = 'active'",
            (user_id,),
        ).fetchone()
        if active:
            return
        queued = db.execute(
            """
            SELECT * FROM assignments
            WHERE assignee_user_id = ? AND status = 'queued'
            ORDER BY queued_at, id LIMIT 1
            """,
            (user_id,),
        ).fetchone()
        if queued:
            now = utc_now()
            db.execute(
                """
                UPDATE assignments
                SET status = 'active', opened_at = ?, deadline_at = ?
                WHERE id = ? AND status = 'queued'
                """,
                (now, _deadline(queued["stage_number"]), queued["id"]),
            )

    def state_for_user(self, user_id: int) -> dict[str, Any]:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self._activate_next(db, user_id)
            user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            workshop = db.execute("SELECT * FROM workshop WHERE id = 1").fetchone()
            assignment = db.execute(
                """
                SELECT a.*, wi.exercise_slug, wi.workspace_dir, wi.author_user_id,
                       wi.author_slot, wi.state AS work_item_state, wi.version AS project_version,
                       ed.number AS exercise_number, ed.title AS exercise_title
                FROM assignments a
                JOIN work_items wi ON wi.id = a.work_item_id
                JOIN exercise_definitions ed ON ed.slug = wi.exercise_slug
                WHERE a.assignee_user_id = ? AND a.status = 'active'
                ORDER BY a.opened_at, a.id LIMIT 1
                """,
                (user_id,),
            ).fetchone()
            queued_count = db.execute(
                "SELECT COUNT(*) FROM assignments WHERE assignee_user_id = ? AND status = 'queued'",
                (user_id,),
            ).fetchone()[0]
            registered = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            db.execute("COMMIT")

        base: dict[str, Any] = {
            "participant": {
                "nickname": user["nickname"],
                "slot": user["slot"],
            },
            "workshop": {
                "state": workshop["state"],
                "participant_count": workshop["participant_count"],
                "registered_count": registered,
                "active_participant_count": (
                    registered if workshop["state"] != "lobby" else 0
                ),
                "routing_mode": workshop["routing_mode"],
            },
            "queued_count": queued_count,
        }
        if assignment is None:
            base["screen"] = (
                "lobby" if workshop["state"] == "lobby" else "waiting"
            )
            if workshop["state"] == "complete":
                base["screen"] = "complete"
            return base

        assignment_data = dict(assignment)
        if assignment["kind"] == "author_review":
            base["screen"] = "review"
            interpretation = self.get_final_interpretation(assignment["work_item_id"])
            assignment_data["interpretation"] = interpretation
        else:
            base["screen"] = "ready"
        base["assignment"] = assignment_data
        return base

    def get_final_interpretation(self, work_item_id: int) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute(
                "SELECT * FROM final_interpretations WHERE work_item_id = ?",
                (work_item_id,),
            ).fetchone()
            return dict(row) if row else None

    def reserve_prompt(
        self,
        *,
        user_id: int,
        assignment_id: int,
        client_request_id: str,
        prompt: str,
        runtime: str,
        model: str,
    ) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute(
                "SELECT * FROM prompt_runs WHERE client_request_id = ?",
                (client_request_id,),
            ).fetchone()
            if existing:
                if (
                    existing["actor_user_id"] != user_id
                    or existing["assignment_id"] != assignment_id
                    or existing["prompt"] != prompt
                ):
                    db.execute("ROLLBACK")
                    raise ConflictError(
                        "Request identifier was reused with different prompt data"
                    )
                db.execute("COMMIT")
                result = dict(existing)
                result["reused"] = True
                return result

            assignment = db.execute(
                """
                SELECT a.*, wi.workspace_dir, wi.exercise_slug, wi.version AS project_version
                FROM assignments a JOIN work_items wi ON wi.id = a.work_item_id
                WHERE a.id = ?
                """,
                (assignment_id,),
            ).fetchone()
            if assignment is None:
                db.execute("ROLLBACK")
                raise NotFoundError("Assignment not found")
            if (
                assignment["assignee_user_id"] != user_id
                or assignment["status"] != "active"
                or assignment["kind"] != "delta"
            ):
                db.execute("ROLLBACK")
                raise ConflictError("This assignment is not active for this participant")
            unfinished_publication = db.execute(
                """
                SELECT run_id FROM publication_journal
                WHERE work_item_id = ? AND status = 'prepared'
                """,
                (assignment["work_item_id"],),
            ).fetchone()
            if unfinished_publication:
                db.execute("ROLLBACK")
                raise ConflictError(
                    "This project needs publication recovery; restart the server"
                )
            running = db.execute(
                "SELECT id FROM prompt_runs WHERE assignment_id = ? AND status = 'running'",
                (assignment_id,),
            ).fetchone()
            if running:
                db.execute("ROLLBACK")
                raise ConflictError("An agent run is already active for this assignment")
            ordinal = db.execute(
                "SELECT COALESCE(MAX(ordinal), 0) + 1 FROM prompt_runs WHERE assignment_id = ?",
                (assignment_id,),
            ).fetchone()[0]
            cursor = db.execute(
                """
                INSERT INTO prompt_runs
                    (assignment_id, actor_user_id, ordinal, client_request_id,
                     agent_session_id, prompt, runtime, model, status, started_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'running', ?)
                """,
                (
                    assignment_id,
                    user_id,
                    ordinal,
                    client_request_id,
                    str(uuid.uuid4()),
                    prompt,
                    runtime,
                    model,
                    now,
                ),
            )
            run = db.execute(
                "SELECT * FROM prompt_runs WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            db.execute("COMMIT")
            result = dict(run)
            result["reused"] = False
            result.update(
                {
                    "workspace_dir": assignment["workspace_dir"],
                    "exercise_slug": assignment["exercise_slug"],
                    "work_item_id": assignment["work_item_id"],
                    "project_version": assignment["project_version"],
                }
            )
            return result

    def prepare_prompt_publication(
        self,
        *,
        run_id: int,
        workspace_dir: Path,
        before_files: dict[str, str],
        after_files: dict[str, str],
        expected_project_version: int,
    ) -> None:
        if set(before_files) != set(EDITABLE_FILES) or set(after_files) != set(
            EDITABLE_FILES
        ):
            raise ValidationError("Publication snapshot must contain exactly three files")
        now = utc_now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            run = db.execute(
                """
                SELECT pr.*, a.work_item_id, a.status AS assignment_status
                FROM prompt_runs pr JOIN assignments a ON a.id = pr.assignment_id
                WHERE pr.id = ?
                """,
                (run_id,),
            ).fetchone()
            if run is None or run["status"] != "running":
                db.execute("ROLLBACK")
                raise ConflictError("Agent run is no longer active")
            project = db.execute(
                "SELECT * FROM work_items WHERE id = ?", (run["work_item_id"],)
            ).fetchone()
            if project["version"] != expected_project_version:
                db.execute("ROLLBACK")
                raise ConflictError("Project changed while the agent was running")
            if run["assignment_status"] != "active":
                db.execute("ROLLBACK")
                raise ConflictError("Assignment was passed while the agent was running")

            for phase, files in (("before", before_files), ("after", after_files)):
                for filename, content in files.items():
                    db.execute(
                        """
                        INSERT INTO run_file_snapshots
                            (prompt_run_id, phase, relative_path, content, sha256)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            run_id,
                            phase,
                            filename,
                            content,
                            hashlib.sha256(content.encode("utf-8")).hexdigest(),
                        ),
                    )
            db.execute(
                """
                INSERT INTO publication_journal
                    (run_id, work_item_id, workspace_dir, before_files_json,
                     after_files_json, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'prepared', ?, ?)
                """,
                (
                    run_id,
                    run["work_item_id"],
                    str(workspace_dir.resolve()),
                    json.dumps(before_files, ensure_ascii=False),
                    json.dumps(after_files, ensure_ascii=False),
                    now,
                    now,
                ),
            )
            db.execute("COMMIT")

    def complete_prompt(
        self,
        *,
        run_id: int,
        response: str,
        activities: list[dict[str, Any]],
        changed_files: list[str],
        before_hash: str,
        after_hash: str,
        expected_project_version: int,
    ) -> None:
        now = utc_now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            run = db.execute(
                """
                SELECT pr.*, a.work_item_id, a.status AS assignment_status
                FROM prompt_runs pr JOIN assignments a ON a.id = pr.assignment_id
                WHERE pr.id = ?
                """,
                (run_id,),
            ).fetchone()
            if run is None or run["status"] != "running":
                db.execute("ROLLBACK")
                raise ConflictError("Agent run is no longer active")
            project = db.execute(
                "SELECT * FROM work_items WHERE id = ?", (run["work_item_id"],)
            ).fetchone()
            if project["version"] != expected_project_version:
                db.execute("ROLLBACK")
                raise ConflictError("Project changed while the agent was running")
            if run["assignment_status"] != "active":
                db.execute("ROLLBACK")
                raise ConflictError("Assignment was passed while the agent was running")
            journal = db.execute(
                "SELECT status FROM publication_journal WHERE run_id = ?", (run_id,)
            ).fetchone()
            if journal is None or journal["status"] != "prepared":
                db.execute("ROLLBACK")
                raise ConflictError("File publication was not prepared")
            db.execute(
                """
                UPDATE prompt_runs
                SET status = 'succeeded', response = ?, activities_json = ?,
                    changed_files_json = ?, before_hash = ?, after_hash = ?, completed_at = ?
                WHERE id = ?
                """,
                (
                    response,
                    json.dumps(activities),
                    json.dumps(changed_files),
                    before_hash,
                    after_hash,
                    now,
                    run_id,
                ),
            )
            db.execute(
                """
                UPDATE assignments
                SET selected_run_id = ?, current_response = ?, revision = revision + 1
                WHERE id = ?
                """,
                (run_id, response, run["assignment_id"]),
            )
            db.execute(
                """
                UPDATE work_items
                SET last_agent_response = ?, version = version + 1, updated_at = ?
                WHERE id = ?
                """,
                (response, now, run["work_item_id"]),
            )
            db.execute(
                """
                UPDATE publication_journal
                SET status = 'finalized', updated_at = ?
                WHERE run_id = ? AND status = 'prepared'
                """,
                (now, run_id),
            )
            db.execute("COMMIT")

    def abort_prompt_publication(self, run_id: int) -> None:
        with self.connect() as db:
            db.execute(
                """
                UPDATE publication_journal
                SET status = 'recovered', updated_at = ?
                WHERE run_id = ? AND status = 'prepared'
                """,
                (utc_now(), run_id),
            )

    def fail_prompt(self, run_id: int, error: str) -> None:
        with self.connect() as db:
            db.execute(
                """
                UPDATE prompt_runs SET status = 'failed', error_text = ?, completed_at = ?
                WHERE id = ? AND status = 'running'
                """,
                (error[:4000], utc_now(), run_id),
            )

    def pass_assignment(
        self,
        *,
        user_id: int,
        assignment_id: int,
        request_key: str,
        interpretation: dict[str, str] | None,
    ) -> dict[str, Any]:
        request_payload = json.dumps(
            {"assignment_id": assignment_id, "interpretation": interpretation},
            sort_keys=True,
        )
        request_hash = hashlib.sha256(request_payload.encode("utf-8")).hexdigest()
        now = utc_now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            idem = db.execute(
                """
                SELECT * FROM idempotency_requests
                WHERE user_id = ? AND endpoint = 'pass' AND request_key = ?
                """,
                (user_id, request_key),
            ).fetchone()
            if idem:
                if idem["request_hash"] != request_hash:
                    db.execute("ROLLBACK")
                    raise ConflictError("Idempotency key was reused with different data")
                db.execute("COMMIT")
                return json.loads(idem["response_json"])

            assignment = db.execute(
                """
                SELECT a.*, wi.author_user_id, wi.author_slot, wi.exercise_slug
                FROM assignments a JOIN work_items wi ON wi.id = a.work_item_id
                WHERE a.id = ?
                """,
                (assignment_id,),
            ).fetchone()
            if assignment is None:
                db.execute("ROLLBACK")
                raise NotFoundError("Assignment not found")
            if assignment["assignee_user_id"] != user_id or assignment["status"] != "active":
                db.execute("ROLLBACK")
                raise ConflictError("This assignment is no longer active")
            if assignment["kind"] != "delta":
                db.execute("ROLLBACK")
                raise ConflictError("Use the review endpoint for an author review")
            if assignment["selected_run_id"] is None:
                db.execute("ROLLBACK")
                raise ValidationError("Run at least one successful prompt before passing")
            changed_run = db.execute(
                """
                SELECT id FROM prompt_runs
                WHERE assignment_id = ? AND status = 'succeeded'
                  AND changed_files_json != '[]'
                LIMIT 1
                """,
                (assignment_id,),
            ).fetchone()
            if changed_run is None:
                db.execute("ROLLBACK")
                raise ValidationError(
                    "Implement the task before passing; no project file changed"
                )
            running = db.execute(
                "SELECT id FROM prompt_runs WHERE assignment_id = ? AND status = 'running'",
                (assignment_id,),
            ).fetchone()
            if running:
                db.execute("ROLLBACK")
                raise ConflictError("Wait for the active agent run to finish")

            current_user = db.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            db.execute(
                "UPDATE assignments SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, assignment_id),
            )

            if assignment["stage_number"] == 12:
                values = interpretation or {}
                required = ("application_for", "primary_user", "final_action_causes")
                if any(not values.get(key, "").strip() for key in required):
                    db.execute("ROLLBACK")
                    raise ValidationError(
                        "Final interpretation requires all three answers"
                    )
                db.execute(
                    """
                    INSERT INTO final_interpretations
                        (work_item_id, assignment_id, user_id, application_for,
                         primary_user, final_action_causes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        assignment["work_item_id"],
                        assignment_id,
                        user_id,
                        values["application_for"].strip(),
                        values["primary_user"].strip(),
                        values["final_action_causes"].strip(),
                        now,
                    ),
                )
                cursor = db.execute(
                    """
                    INSERT INTO assignments
                        (work_item_id, stage_number, kind, assignee_user_id, status,
                         incoming_response, queued_at)
                    VALUES (?, 13, 'author_review', ?, 'queued', ?, ?)
                    """,
                    (
                        assignment["work_item_id"],
                        assignment["author_user_id"],
                        assignment["current_response"],
                        now,
                    ),
                )
                next_assignment_id = cursor.lastrowid
                db.execute(
                    """
                    UPDATE work_items SET state = 'awaiting_author_review',
                        current_stage = 13, updated_at = ? WHERE id = ?
                    """,
                    (now, assignment["work_item_id"]),
                )
                target_user_id = assignment["author_user_id"]
            else:
                active_participant_count = db.execute(
                    "SELECT COUNT(*) FROM users"
                ).fetchone()[0]
                target_slot = next_slot(
                    current_slot=current_user["slot"],
                    author_slot=assignment["author_slot"],
                    participant_count=active_participant_count,
                    routing_mode=self.settings.routing_mode,
                )
                target = db.execute(
                    "SELECT * FROM users WHERE slot = ?", (target_slot,)
                ).fetchone()
                if target is None:
                    db.execute("ROLLBACK")
                    raise ConflictError("The next participant has not joined")
                next_stage = assignment["stage_number"] + 1
                cursor = db.execute(
                    """
                    INSERT INTO assignments
                        (work_item_id, stage_number, kind, assignee_user_id, status,
                         incoming_response, queued_at)
                    VALUES (?, ?, 'delta', ?, 'queued', ?, ?)
                    """,
                    (
                        assignment["work_item_id"],
                        next_stage,
                        target["id"],
                        assignment["current_response"],
                        now,
                    ),
                )
                next_assignment_id = cursor.lastrowid
                target_user_id = target["id"]
                db.execute(
                    """
                    UPDATE work_items SET current_stage = ?, updated_at = ? WHERE id = ?
                    """,
                    (next_stage, now, assignment["work_item_id"]),
                )

            db.execute(
                """
                INSERT INTO handoffs
                    (work_item_id, from_assignment_id, to_assignment_id,
                     selected_prompt_run_id, from_user_id, to_user_id,
                     response_text, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    assignment["work_item_id"],
                    assignment_id,
                    next_assignment_id,
                    assignment["selected_run_id"],
                    user_id,
                    target_user_id,
                    assignment["current_response"],
                    now,
                ),
            )
            self._activate_next(db, target_user_id)
            self._activate_next(db, user_id)
            response = {"ok": True, "next_assignment_id": next_assignment_id}
            db.execute(
                """
                INSERT INTO idempotency_requests
                    (user_id, endpoint, request_key, request_hash, response_json, created_at)
                VALUES (?, 'pass', ?, ?, ?, ?)
                """,
                (user_id, request_key, request_hash, json.dumps(response), now),
            )
            db.execute("COMMIT")
            return response

    def complete_review(
        self, *, user_id: int, assignment_id: int, notes: str
    ) -> None:
        now = utc_now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            assignment = db.execute(
                """
                SELECT a.*, wi.author_user_id FROM assignments a
                JOIN work_items wi ON wi.id = a.work_item_id WHERE a.id = ?
                """,
                (assignment_id,),
            ).fetchone()
            if assignment is None:
                db.execute("ROLLBACK")
                raise NotFoundError("Review assignment not found")
            if (
                assignment["kind"] != "author_review"
                or assignment["status"] != "active"
                or assignment["author_user_id"] != user_id
            ):
                db.execute("ROLLBACK")
                raise ConflictError("This review is not active for this author")
            db.execute(
                """
                INSERT INTO author_reviews
                    (work_item_id, assignment_id, author_user_id, notes, completed_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    assignment["work_item_id"],
                    assignment_id,
                    user_id,
                    notes.strip(),
                    now,
                ),
            )
            db.execute(
                "UPDATE assignments SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, assignment_id),
            )
            db.execute(
                "UPDATE work_items SET state = 'complete', updated_at = ? WHERE id = ?",
                (now, assignment["work_item_id"]),
            )
            self._activate_next(db, user_id)
            remaining = db.execute(
                "SELECT COUNT(*) FROM work_items WHERE state NOT IN ('pending', 'complete')"
            ).fetchone()[0]
            if remaining == 0:
                db.execute(
                    "UPDATE workshop SET state = 'complete', completed_at = ? WHERE id = 1",
                    (now,),
                )
            db.execute("COMMIT")

    def assignment_for_user(self, user_id: int, assignment_id: int) -> dict[str, Any]:
        with self.connect() as db:
            row = db.execute(
                """
                SELECT a.*, wi.workspace_dir, wi.exercise_slug, wi.version AS project_version,
                       wi.author_user_id
                FROM assignments a JOIN work_items wi ON wi.id = a.work_item_id
                WHERE a.id = ? AND a.assignee_user_id = ? AND a.status = 'active'
                """,
                (assignment_id, user_id),
            ).fetchone()
            if row is None:
                raise NotFoundError("Active assignment not found")
            return dict(row)

    def assignment_for_actor(self, user_id: int, assignment_id: int) -> dict[str, Any]:
        """Return an assignment owned by the actor regardless of completion state."""
        with self.connect() as db:
            row = db.execute(
                """
                SELECT a.*, wi.workspace_dir, wi.exercise_slug, wi.version AS project_version,
                       wi.author_user_id
                FROM assignments a JOIN work_items wi ON wi.id = a.work_item_id
                WHERE a.id = ? AND a.assignee_user_id = ?
                """,
                (assignment_id, user_id),
            ).fetchone()
            if row is None:
                raise NotFoundError("Assignment not found for this participant")
            return dict(row)

    def prompt_result_by_client_id(self, client_request_id: str) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute(
                "SELECT * FROM prompt_runs WHERE client_request_id = ?",
                (client_request_id,),
            ).fetchone()
            return dict(row) if row else None
