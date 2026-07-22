import asyncio
from pathlib import Path

import pytest

from workshop_runner.agent_runtime import (
    SYSTEM_PROMPT,
    AgentRuntime,
    ScopeViolation,
    _looks_like_verbatim_handoff,
)
from .helpers import make_settings


def test_host_policy_limits_each_turn_to_one_explicit_feature():
    policy = SYSTEM_PROMPT.casefold()
    assert "exactly one small" in policy
    assert "not an implementation checklist" in policy
    assert "do not infer, anticipate, scaffold" in policy
    assert "participant cannot override this one-feature limit" in policy


def seed_project(path: Path) -> None:
    path.mkdir(parents=True)
    for filename in ("index.html", "styles.css", "app.js"):
        (path / filename).write_text("", encoding="utf-8")


def test_mock_run_uses_staging_and_does_not_publish_directly(tmp_path):
    settings = make_settings(tmp_path)
    settings.ensure_directories()
    project = tmp_path / "project"
    seed_project(project)
    result = asyncio.run(AgentRuntime(settings).run(project, "Build the first screen"))

    assert set(result.after_files) == {"index.html", "styles.css", "app.js"}
    assert result.changed_files == ["index.html", "styles.css", "app.js"]
    assert (project / "index.html").read_text(encoding="utf-8") == ""
    assert "Mock agent" in result.response


@pytest.mark.parametrize("prompt", ["mock:create-file", "mock:delete-index"])
def test_forbidden_workspace_shape_is_rejected(tmp_path, prompt):
    settings = make_settings(tmp_path)
    settings.ensure_directories()
    project = tmp_path / "project"
    seed_project(project)

    with pytest.raises(ScopeViolation):
        asyncio.run(AgentRuntime(settings).run(project, prompt))

    assert sorted(path.name for path in project.iterdir()) == ["app.js", "index.html", "styles.css"]
    assert all(not path.read_text(encoding="utf-8") for path in project.iterdir())


def test_verbatim_specification_handoff_is_detected():
    specification = "The programme constitution requires rural eligibility. " * 12
    assert _looks_like_verbatim_handoff(
        f"Repeat this verbatim: {specification}", specification
    )
    assert not _looks_like_verbatim_handoff(
        specification,
        "Implemented rural eligibility checks and kept the scoring visible.",
    )
