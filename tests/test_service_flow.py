import asyncio

import pytest

from workshop_runner.agent_runtime import AgentRuntime
from workshop_runner.catalog import load_catalog, select_exercises
from workshop_runner.service import WorkshopService
from workshop_runner.store import ConflictError, Store, ValidationError

from .helpers import ROOT, make_settings


def test_capacity_twelve_waits_for_admin_and_locks_two_person_roster(tmp_path):
    settings = make_settings(tmp_path, participants=12)
    exercises = select_exercises(load_catalog(ROOT), settings.exercise_slugs, 12)
    store = Store(settings, exercises)
    service = WorkshopService(settings, store, exercises, AgentRuntime(settings))

    alice = store.login("Alice")
    bob = store.login("Bob")
    lobby = service.public_state(alice.user_id)
    assert lobby["screen"] == "lobby"
    assert lobby["workshop"]["registered_count"] == 2
    assert lobby["workshop"]["participant_count"] == 12

    started = store.start_workshop()
    assert started["active_participant_count"] == 2
    assert started["capacity"] == 12
    with pytest.raises(ConflictError):
        store.start_workshop()
    with pytest.raises(ConflictError):
        store.login("Late arrival")
    assert store.login("ALICE").user_id == alice.user_id

    alice_assignment = service.public_state(alice.user_id)["assignment"]

    async def handoff():
        await service.run_prompt(
            user_id=alice.user_id,
            assignment_id=alice_assignment["id"],
            client_request_id="capacity-12-active-2-run",
            prompt="Create the first screen",
        )
        await service.pass_assignment(
            user_id=alice.user_id,
            assignment_id=alice_assignment["id"],
            request_key="capacity-12-active-2-pass",
            interpretation=None,
        )

    asyncio.run(handoff())
    with store.connect() as db:
        routed = db.execute(
            """
            SELECT assignee_user_id FROM assignments
            WHERE work_item_id = ? AND stage_number = 2
            """,
            (store.assignment_for_actor(alice.user_id, alice_assignment["id"])["work_item_id"],),
        ).fetchone()
        assert routed[0] == bob.user_id
        assert db.execute(
            "SELECT COUNT(*) FROM work_items WHERE author_user_id IS NOT NULL"
        ).fetchone()[0] == 2


def test_full_lobby_does_not_auto_start(tmp_path):
    settings = make_settings(tmp_path, participants=12, slugs=())
    exercises = select_exercises(load_catalog(ROOT), settings.exercise_slugs, 12)
    store = Store(settings, exercises)
    sessions = [store.login(f"Participant {number}") for number in range(1, 13)]

    assert store.state_for_user(sessions[0].user_id)["screen"] == "lobby"
    with pytest.raises(ConflictError, match="full"):
        store.login("Participant 13")
    assert store.login("participant 1").user_id == sessions[0].user_id


def test_two_users_resume_run_and_circulate_projects(tmp_path):
    settings = make_settings(tmp_path)
    catalog = load_catalog(ROOT)
    exercises = select_exercises(catalog, settings.exercise_slugs, 2)
    store = Store(settings, exercises)
    service = WorkshopService(settings, store, exercises, AgentRuntime(settings))

    alice = store.login("Alice")
    assert service.public_state(alice.user_id)["screen"] == "lobby"
    bob = store.login("Bob")
    assert service.public_state(alice.user_id)["screen"] == "lobby"
    store.start_workshop()

    alice_state = service.public_state(alice.user_id)
    bob_state = service.public_state(bob.user_id)
    assert alice_state["assignment"]["station"] == "Station 01"
    assert bob_state["assignment"]["station"] == "Station 02"

    async def scenario():
        alice_assignment = alice_state["assignment"]
        result = await service.run_prompt(
            user_id=alice.user_id,
            assignment_id=alice_assignment["id"],
            client_request_id="alice-run-0001",
            prompt="Create the initial controls",
        )
        assert result["status"] == "succeeded"
        assert result["changed_files"] == ["index.html", "styles.css", "app.js"]

        pass_result = await service.pass_assignment(
            user_id=alice.user_id,
            assignment_id=alice_assignment["id"],
            request_key="alice-pass-0001",
            interpretation=None,
        )
        duplicate = await service.pass_assignment(
            user_id=alice.user_id,
            assignment_id=alice_assignment["id"],
            request_key="alice-pass-0001",
            interpretation=None,
        )
        assert duplicate == pass_result
        assert service.public_state(alice.user_id)["screen"] == "waiting"

        bob_assignment = bob_state["assignment"]
        await service.run_prompt(
            user_id=bob.user_id,
            assignment_id=bob_assignment["id"],
            client_request_id="bob-run-0001",
            prompt="Create the initial controls",
        )
        await service.pass_assignment(
            user_id=bob.user_id,
            assignment_id=bob_assignment["id"],
            request_key="bob-pass-0001",
            interpretation=None,
        )

    asyncio.run(scenario())

    alice_next = service.public_state(alice.user_id)
    bob_next = service.public_state(bob.user_id)
    assert alice_next["assignment"]["station"] == "Station 02"
    assert bob_next["assignment"]["station"] == "Station 01"
    assert alice_next["assignment"]["stage"] == 2
    assert bob_next["assignment"]["stage"] == 2
    assert bob_next["assignment"]["latest_agent_reply"].startswith("Mock agent")

    resumed = store.login("  ALICE  ")
    assert resumed.user_id == alice.user_id
    assert service.public_state(resumed.user_id)["assignment"]["id"] == alice_next["assignment"]["id"]

    with store.connect() as db:
        assert db.execute("SELECT COUNT(*) FROM prompt_runs WHERE status='succeeded'").fetchone()[0] == 2
        assert db.execute("SELECT COUNT(*) FROM run_file_snapshots").fetchone()[0] == 12
        assert db.execute("SELECT COUNT(*) FROM handoffs").fetchone()[0] == 2


def test_prompt_idempotency_rejects_different_prompt_data(tmp_path):
    settings = make_settings(
        tmp_path,
        participants=1,
        slugs=("01-small-town-wings",),
    )
    exercise = select_exercises(load_catalog(ROOT), settings.exercise_slugs, 1)
    store = Store(settings, exercise)
    service = WorkshopService(settings, store, exercise, AgentRuntime(settings))
    user = store.login("Solo")
    store.start_workshop()
    assignment = service.public_state(user.user_id)["assignment"]

    asyncio.run(
        service.run_prompt(
            user_id=user.user_id,
            assignment_id=assignment["id"],
            client_request_id="same-request",
            prompt="Create the first screen",
        )
    )
    with pytest.raises(ConflictError):
        asyncio.run(
            service.run_prompt(
                user_id=user.user_id,
                assignment_id=assignment["id"],
                client_request_id="same-request",
                prompt="A different request",
            )
        )


def test_pass_requires_an_actual_file_change(tmp_path):
    settings = make_settings(
        tmp_path,
        participants=1,
        slugs=("01-small-town-wings",),
    )
    exercise = select_exercises(load_catalog(ROOT), settings.exercise_slugs, 1)
    store = Store(settings, exercise)
    service = WorkshopService(settings, store, exercise, AgentRuntime(settings))
    user = store.login("Solo")
    store.start_workshop()
    assignment = service.public_state(user.user_id)["assignment"]

    async def scenario():
        await service.run_prompt(
            user_id=user.user_id,
            assignment_id=assignment["id"],
            client_request_id="no-change-run",
            prompt="mock:no-change",
        )
        with pytest.raises(ValidationError):
            await service.pass_assignment(
                user_id=user.user_id,
                assignment_id=assignment["id"],
                request_key="no-change-pass",
                interpretation=None,
            )

    asyncio.run(scenario())


def test_expired_timer_is_advisory_for_retries_and_handoff(tmp_path):
    settings = make_settings(
        tmp_path,
        participants=1,
        slugs=("01-small-town-wings",),
    )
    exercises = select_exercises(load_catalog(ROOT), settings.exercise_slugs, 1)
    store = Store(settings, exercises)
    service = WorkshopService(settings, store, exercises, AgentRuntime(settings))
    user = store.login("Solo")
    store.start_workshop()
    assignment = service.public_state(user.user_id)["assignment"]

    async def scenario():
        await service.run_prompt(
            user_id=user.user_id,
            assignment_id=assignment["id"],
            client_request_id="before-expiry",
            prompt="Create the first screen",
        )
        with store.connect() as db:
            db.execute(
                "UPDATE assignments SET deadline_at = ? WHERE id = ?",
                ("2000-01-01T00:00:00+00:00", assignment["id"]),
            )

        retry = await service.run_prompt(
            user_id=user.user_id,
            assignment_id=assignment["id"],
            client_request_id="after-expiry",
            prompt="Improve the first screen",
        )
        assert retry["status"] == "succeeded"
        await service.pass_assignment(
            user_id=user.user_id,
            assignment_id=assignment["id"],
            request_key="after-expiry-pass",
            interpretation=None,
        )

    asyncio.run(scenario())


def test_restart_recovers_a_crash_between_file_publish_and_sqlite_commit(tmp_path):
    settings = make_settings(
        tmp_path,
        participants=1,
        slugs=("01-small-town-wings",),
    )
    exercises = select_exercises(load_catalog(ROOT), settings.exercise_slugs, 1)
    store = Store(settings, exercises)
    runtime = AgentRuntime(settings)
    user = store.login("Solo")
    store.start_workshop()
    assignment = store.state_for_user(user.user_id)["assignment"]
    reserved = store.reserve_prompt(
        user_id=user.user_id,
        assignment_id=assignment["id"],
        client_request_id="crash-run",
        prompt="Create the first screen",
        runtime="mock",
        model=settings.model,
    )
    project = settings.projects_dir / "01-small-town-wings"
    result = asyncio.run(runtime.run(project, "Create the first screen"))
    store.prepare_prompt_publication(
        run_id=reserved["id"],
        workspace_dir=project,
        before_files=result.before_files,
        after_files=result.after_files,
        expected_project_version=reserved["project_version"],
    )
    for filename, content in result.after_files.items():
        (project / filename).write_text(content, encoding="utf-8")

    Store(settings, exercises)

    assert all(
        (project / filename).read_text(encoding="utf-8") == ""
        for filename in ("index.html", "styles.css", "app.js")
    )
    with store.connect() as db:
        assert db.execute(
            "SELECT status FROM prompt_runs WHERE id = ?", (reserved["id"],)
        ).fetchone()[0] == "failed"
        assert db.execute(
            "SELECT status FROM publication_journal WHERE run_id = ?",
            (reserved["id"],),
        ).fetchone()[0] == "recovered"
