import re

from fastapi.testclient import TestClient

from workshop_runner.main import create_app

from .helpers import make_settings


def test_browser_api_spec_preview_prompt_and_pass(tmp_path):
    settings = make_settings(
        tmp_path,
        participants=1,
        slugs=("01-small-town-wings",),
        routing_mode="circular",
    )
    client = TestClient(create_app(settings))

    login = client.post("/api/login", json={"nickname": "Solo", "client": "browser"})
    assert login.status_code == 200
    assert "token" not in login.json()
    assert login.json()["state"]["screen"] == "lobby"
    unauthorized = client.post("/api/admin/start")
    assert unauthorized.status_code == 401
    started = client.post(
        "/api/admin/start",
        headers={"X-Workshop-Admin": settings.admin_code},
    )
    assert started.status_code == 200
    state = client.get("/api/state").json()
    assignment = state["assignment"]
    assert assignment["stage"] == 1

    spec = client.get(assignment["spec0_image_url"])
    assert spec.status_code == 200
    assert spec.headers["content-type"].startswith("image/svg+xml")

    preview = client.get(assignment["preview_url"])
    assert preview.status_code == 200
    source = re.search(r'src="([^"]+/index\.html[^\"]*)"', preview.text).group(1)
    content = client.get(source)
    assert content.status_code == 200
    assert "connect-src 'none'" in content.headers["content-security-policy"]

    run = client.post(
        "/api/run",
        json={
            "assignment_id": assignment["id"],
            "prompt": "Create a visible first screen",
            "client_request_id": "api-run-0001",
        },
    )
    assert run.status_code == 200
    assert run.json()["status"] == "succeeded"

    progress = client.get("/api/run-progress/api-run-0001?cursor=0")
    assert progress.status_code == 200
    assert progress.json()["status"] == "succeeded"
    assert any(
        event["stream"] == "stdout" for event in progress.json()["events"]
    )

    passed = client.post(
        "/api/pass",
        json={
            "assignment_id": assignment["id"],
            "request_key": "api-pass-0001",
            "interpretation": None,
        },
    )
    assert passed.status_code == 200
    assert passed.json()["assignment"]["stage"] == 2
    assert client.get(assignment["spec0_image_url"]).status_code == 404


def test_browser_source_stores_only_nickname_in_local_storage():
    source = (make_settings.__globals__["ROOT"] / "workshop_runner" / "web" / "app.js").read_text(encoding="utf-8")
    local_storage_lines = [line for line in source.splitlines() if "localStorage" in line]
    assert local_storage_lines
    assert all("workshopNickname" in line for line in local_storage_lines)
    assert not any("token" in line.casefold() for line in local_storage_lines)
