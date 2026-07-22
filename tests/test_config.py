from workshop_runner.config import Settings

from .helpers import ROOT


def test_default_reasoning_effort_is_medium(monkeypatch):
    monkeypatch.delenv("WORKSHOP_REASONING_EFFORT", raising=False)
    assert Settings.from_env(ROOT).reasoning_effort == "medium"
