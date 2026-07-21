from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from workshop_runner.config import Settings


ROOT = Path(__file__).resolve().parents[1]


def make_settings(
    tmp_path: Path,
    *,
    participants: int = 2,
    slugs: tuple[str, ...] = ("01-small-town-wings", "02-early-shift-lift"),
    routing_mode: str = "circular",
) -> Settings:
    base = Settings.from_env(ROOT)
    data = tmp_path / "data"
    return replace(
        base,
        data_dir=data,
        database_path=data / "workshop.db",
        projects_dir=tmp_path / "projects",
        staging_dir=data / "staging",
        participant_count=participants,
        minimum_participants=min(2, participants),
        exercise_slugs=slugs,
        routing_mode=routing_mode,
        agent_mode="mock",
        open_browser=False,
        preview_secret="test-preview-secret",
    )
