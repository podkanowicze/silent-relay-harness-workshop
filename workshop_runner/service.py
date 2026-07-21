from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import tempfile
import threading
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from .agent_runtime import (
    AgentResult,
    AgentRuntime,
    ScopeViolation,
    project_hash,
    validate_workspace,
)
from .catalog import Exercise
from .config import Settings
from .store import EDITABLE_FILES, ConflictError, Store


class WorkshopService:
    def __init__(
        self,
        settings: Settings,
        store: Store,
        exercises: list[Exercise],
        runtime: AgentRuntime,
    ):
        self.settings = settings
        self.store = store
        self.exercises = {exercise.slug: exercise for exercise in exercises}
        self.runtime = runtime
        self._project_locks: defaultdict[int, threading.Lock] = defaultdict(threading.Lock)

    def admin_state(self) -> dict[str, Any]:
        return self.store.admin_state()

    def start_workshop(self) -> dict[str, Any]:
        return self.store.start_workshop()

    @asynccontextmanager
    async def _project_lock(self, work_item_id: int):
        lock = self._project_locks[work_item_id]
        await asyncio.to_thread(lock.acquire)
        try:
            yield
        finally:
            lock.release()

    def public_state(self, user_id: int) -> dict[str, Any]:
        raw = self.store.state_for_user(user_id)
        assignment = raw.pop("assignment", None)
        if assignment is None:
            return raw

        exercise = self.exercises[assignment["exercise_slug"]]
        stage = assignment["stage_number"]
        common = {
            "id": assignment["id"],
            "station": f"Station {exercise.number:02d}",
            "stage": stage,
            "kind": assignment["kind"],
            "revision": assignment["revision"],
            "project_revision": assignment["project_version"],
            "deadline_at": assignment["deadline_at"],
            "latest_agent_reply": assignment["current_response"]
            or assignment["incoming_response"],
            "has_successful_run": assignment["selected_run_id"] is not None,
            "preview_url": f"/preview/{assignment['id']}",
        }
        if assignment["kind"] == "delta":
            common["delta"] = {
                "number": stage,
                "text": exercise.deltas[stage],
            }
            if stage == 1 and assignment["author_user_id"] == user_id:
                common["spec0_image_url"] = f"/api/spec0/{assignment['id']}.svg"
        else:
            common.update(
                {
                    "exercise_title": exercise.title,
                    "spec0": exercise.spec0,
                    "deltas": exercise.deltas,
                    "interpretation": assignment.get("interpretation"),
                }
            )
        raw["assignment"] = common
        return raw

    async def run_prompt(
        self,
        *,
        user_id: int,
        assignment_id: int,
        client_request_id: str,
        prompt: str,
    ) -> dict[str, Any]:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        if (
            self.settings.max_prompt_chars > 0
            and len(prompt) > self.settings.max_prompt_chars
        ):
            raise ValueError(
                f"Prompt exceeds {self.settings.max_prompt_chars} characters"
            )

        assignment = self.store.assignment_for_user(user_id, assignment_id)
        async with self._project_lock(assignment["work_item_id"]):
            reserved = self.store.reserve_prompt(
                user_id=user_id,
                assignment_id=assignment_id,
                client_request_id=client_request_id,
                prompt=prompt,
                runtime=self.runtime.name,
                model=self.settings.model,
            )
            if reserved["status"] == "succeeded":
                return self._stored_run_response(reserved)
            if reserved["status"] == "failed":
                raise ConflictError(reserved["error_text"] or "Previous run failed")
            if reserved.get("reused"):
                raise ConflictError("Agent run is already in progress")

            project_dir = Path(reserved["workspace_dir"])
            try:
                result = await self.runtime.run(project_dir, prompt)
                self._publish_and_record(
                    run_id=reserved["id"],
                    result=result,
                    project_dir=project_dir,
                    expected_project_version=reserved["project_version"],
                )
            except Exception as error:
                self.store.fail_prompt(reserved["id"], str(error))
                raise

        return {
            "status": "succeeded",
            "run_id": reserved["id"],
            "response": result.response,
            "activities": result.activities
            + [
                {
                    "type": "validation.completed",
                    "message": "Only the three allowed files remain",
                }
            ],
            "changed_files": result.changed_files,
            "after_hash": result.after_hash,
        }

    @staticmethod
    def _stored_run_response(run: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": run["status"],
            "run_id": run["id"],
            "response": run["response"],
            "activities": json.loads(run["activities_json"]),
            "changed_files": json.loads(run["changed_files_json"]),
            "after_hash": run["after_hash"],
        }

    def _publish_and_record(
        self,
        *,
        run_id: int,
        result: AgentResult,
        project_dir: Path,
        expected_project_version: int,
    ) -> None:
        live = validate_workspace(project_dir, self.settings.max_file_bytes)
        if project_hash(live) != result.before_hash:
            raise ConflictError("Project files changed while the agent was running")

        self.store.prepare_prompt_publication(
            run_id=run_id,
            workspace_dir=project_dir,
            before_files=result.before_files,
            after_files=result.after_files,
            expected_project_version=expected_project_version,
        )
        try:
            self._atomic_publish(project_dir, result.after_files)
            published = validate_workspace(
                project_dir, self.settings.max_file_bytes
            )
            if project_hash(published) != result.after_hash:
                raise ScopeViolation("Published files do not match the validated result")
            self.store.complete_prompt(
                run_id=run_id,
                response=result.response,
                activities=result.activities,
                changed_files=result.changed_files,
                before_hash=result.before_hash,
                after_hash=result.after_hash,
                expected_project_version=expected_project_version,
            )
        except Exception:
            try:
                self._atomic_publish(project_dir, result.before_files)
                restored = validate_workspace(
                    project_dir, self.settings.max_file_bytes
                )
                if project_hash(restored) != result.before_hash:
                    raise ScopeViolation("Could not restore the previous project revision")
            except Exception:
                # Leave the journal as prepared so startup recovery will retry.
                raise
            self.store.abort_prompt_publication(run_id)
            raise

    @staticmethod
    def _atomic_publish(project_dir: Path, files: dict[str, str]) -> None:
        before = {
            filename: (project_dir / filename).read_bytes()
            for filename in EDITABLE_FILES
        }
        committed: list[str] = []
        with tempfile.TemporaryDirectory(
            prefix=".workshop-publish-", dir=project_dir.parent
        ) as temporary:
            stage = Path(temporary)
            for filename in EDITABLE_FILES:
                (stage / filename).write_bytes(files[filename].encode("utf-8"))
            try:
                for filename in EDITABLE_FILES:
                    os.replace(stage / filename, project_dir / filename)
                    committed.append(filename)
            except Exception:
                for filename in committed:
                    (project_dir / filename).write_bytes(before[filename])
                raise

    async def pass_assignment(
        self,
        *,
        user_id: int,
        assignment_id: int,
        request_key: str,
        interpretation: dict[str, str] | None,
    ) -> dict[str, Any]:
        assignment = self.store.assignment_for_actor(user_id, assignment_id)
        async with self._project_lock(assignment["work_item_id"]):
            return self.store.pass_assignment(
                user_id=user_id,
                assignment_id=assignment_id,
                request_key=request_key,
                interpretation=interpretation,
            )

    async def complete_review(
        self, *, user_id: int, assignment_id: int, notes: str
    ) -> None:
        assignment = self.store.assignment_for_user(user_id, assignment_id)
        async with self._project_lock(assignment["work_item_id"]):
            self.store.complete_review(
                user_id=user_id, assignment_id=assignment_id, notes=notes
            )

    def assignment_project(
        self, *, user_id: int, assignment_id: int
    ) -> tuple[dict[str, Any], Path]:
        assignment = self.store.assignment_for_user(user_id, assignment_id)
        return assignment, Path(assignment["workspace_dir"])

    def preview_ticket(self, user_id: int, assignment_id: int) -> str:
        expires = int(time.time()) + 600
        payload = f"{user_id}:{assignment_id}:{expires}"
        signature = hmac.new(
            self.settings.preview_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"{payload}:{signature}"

    def validate_preview_ticket(self, ticket: str, assignment_id: int) -> int:
        try:
            user_text, assignment_text, expires_text, signature = ticket.split(":", 3)
            user_id = int(user_text)
            ticket_assignment = int(assignment_text)
            expires = int(expires_text)
        except (ValueError, TypeError) as error:
            raise ValueError("Invalid preview ticket") from error
        if ticket_assignment != assignment_id or expires < int(time.time()):
            raise ValueError("Preview ticket expired or mismatched")
        payload = f"{user_id}:{assignment_id}:{expires}"
        expected = hmac.new(
            self.settings.preview_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("Invalid preview ticket")
        self.store.assignment_for_user(user_id, assignment_id)
        return user_id
