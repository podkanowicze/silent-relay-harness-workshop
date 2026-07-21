from __future__ import annotations

import os
import secrets
import tempfile
from dataclasses import dataclass
from pathlib import Path


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    project_root: Path
    data_dir: Path
    database_path: Path
    projects_dir: Path
    staging_dir: Path
    participant_count: int
    minimum_participants: int
    exercise_slugs: tuple[str, ...]
    routing_mode: str
    agent_mode: str
    model: str
    reasoning_effort: str
    agent_timeout_seconds: int
    agent_max_turns: int
    max_prompt_chars: int
    max_file_bytes: int
    host: str
    port: int
    open_browser: bool
    cookie_secure: bool
    preview_secret: str
    admin_code: str

    @classmethod
    def from_env(cls, project_root: Path | None = None) -> "Settings":
        root = (project_root or Path(__file__).resolve().parents[1]).resolve()
        data_dir = Path(os.getenv("WORKSHOP_DATA_DIR", root / "workshop_data")).resolve()
        database_path = Path(
            os.getenv("WORKSHOP_DB_PATH", data_dir / "workshop.db")
        ).resolve()
        projects_dir = Path(
            os.getenv("WORKSHOP_PROJECTS_DIR", database_path.parent / "projects")
        ).resolve()
        participants = int(os.getenv("WORKSHOP_PARTICIPANTS", "12"))
        if not 1 <= participants <= 12:
            raise ValueError("WORKSHOP_PARTICIPANTS must be between 1 and 12")
        minimum_participants = int(os.getenv("WORKSHOP_MIN_PARTICIPANTS", "2"))
        if not 1 <= minimum_participants <= participants:
            raise ValueError(
                "WORKSHOP_MIN_PARTICIPANTS must be between 1 and WORKSHOP_PARTICIPANTS"
            )

        raw_slugs = os.getenv("WORKSHOP_EXERCISES", "").strip()
        slugs = tuple(item.strip() for item in raw_slugs.split(",") if item.strip())
        if len(slugs) > participants:
            raise ValueError("There cannot be more active exercises than participants")

        routing_mode = os.getenv("WORKSHOP_ROUTING_MODE", "circular").strip()
        if routing_mode not in {"circular", "skip_author"}:
            raise ValueError("WORKSHOP_ROUTING_MODE must be circular or skip_author")
        if routing_mode == "skip_author" and participants < 2:
            raise ValueError("skip_author routing requires at least two participants")

        agent_mode = os.getenv("WORKSHOP_AGENT_MODE", "dcode").strip()
        if agent_mode not in {"mock", "dcode"}:
            raise ValueError("WORKSHOP_AGENT_MODE must be mock or dcode")

        return cls(
            project_root=root,
            data_dir=data_dir,
            database_path=database_path,
            projects_dir=projects_dir,
            staging_dir=Path(
                os.getenv(
                    "WORKSHOP_STAGING_DIR",
                    Path(tempfile.gettempdir()) / "context-telephone-staging",
                )
            ).resolve(),
            participant_count=participants,
            minimum_participants=minimum_participants,
            exercise_slugs=slugs,
            routing_mode=routing_mode,
            agent_mode=agent_mode,
            model=os.getenv("WORKSHOP_MODEL", "gpt-5.6-luna").strip(),
            reasoning_effort=os.getenv(
                "WORKSHOP_REASONING_EFFORT", "high"
            ).strip(),
            agent_timeout_seconds=int(os.getenv("WORKSHOP_AGENT_TIMEOUT", "210")),
            agent_max_turns=int(os.getenv("WORKSHOP_AGENT_MAX_TURNS", "50")),
            max_prompt_chars=int(os.getenv("WORKSHOP_MAX_PROMPT_CHARS", "0")),
            max_file_bytes=int(os.getenv("WORKSHOP_MAX_FILE_BYTES", "1000000")),
            host=os.getenv("WORKSHOP_HOST", "0.0.0.0"),
            port=int(os.getenv("WORKSHOP_PORT", "8000")),
            open_browser=_as_bool(os.getenv("WORKSHOP_OPEN_BROWSER"), True),
            cookie_secure=_as_bool(os.getenv("WORKSHOP_COOKIE_SECURE"), False),
            preview_secret=os.getenv("WORKSHOP_PREVIEW_SECRET") or secrets.token_hex(32),
            admin_code=os.getenv("WORKSHOP_ADMIN_CODE") or secrets.token_urlsafe(12),
        )

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
