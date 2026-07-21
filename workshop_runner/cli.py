from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
import uuid
from typing import Any


class Client:
    def __init__(self, server: str, token: str | None = None):
        self.server = server.rstrip("/")
        self.token = token

    def request(self, path: str, method: str = "GET", data: Any = None) -> Any:
        body = json.dumps(data).encode("utf-8") if data is not None else None
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(
            f"{self.server}{path}", data=body, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=240) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            payload = json.loads(error.read().decode("utf-8") or "{}")
            raise RuntimeError(payload.get("detail", f"HTTP {error.code}")) from error


def print_state(state: dict[str, Any]) -> None:
    participant = state["participant"]
    print(f"\n{participant['nickname']} · participant {participant['slot']}")
    screen = state["screen"]
    if screen == "lobby":
        workshop = state["workshop"]
        print(
            f"Lobby: {workshop['registered_count']}/{workshop['participant_count']} joined."
        )
        return
    if screen == "waiting":
        print(f"Waiting. Queued applications: {state['queued_count']}")
        return
    if screen == "complete":
        print("Workshop complete.")
        return
    assignment = state["assignment"]
    if screen == "review":
        print(f"Author review: {assignment['exercise_title']}")
        print(json.dumps(assignment.get("interpretation"), indent=2, ensure_ascii=False))
        return
    print(f"{assignment['station']} · DELTA-{assignment['stage']}")
    print(f"TASK: {assignment['delta']['text']}")
    print("LATEST AGENT REPLY:")
    print(assignment["latest_agent_reply"] or "(none)")
    if assignment.get("spec0_image_url"):
        print("SPEC-0 is available as an image in the browser UI.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Terminal client for Context Telephone")
    parser.add_argument("--server", default="http://127.0.0.1:8000")
    parser.add_argument("--nick", required=True)
    args = parser.parse_args()

    client = Client(args.server)
    login = client.request(
        "/api/login", "POST", {"nickname": args.nick, "client": "cli"}
    )
    client.token = login["token"]
    state = login["state"]

    while True:
        print_state(state)
        if state["screen"] in {"lobby", "waiting"}:
            command = input("[Enter] refresh, /quit: ").strip()
            if command == "/quit":
                return
            state = client.request("/api/state")
            continue
        if state["screen"] == "complete":
            return
        if state["screen"] == "review":
            notes = input("Review notes (or /quit): ").strip()
            if notes == "/quit":
                return
            state = client.request(
                "/api/review",
                "POST",
                {"assignment_id": state["assignment"]["id"], "notes": notes},
            )
            continue

        assignment = state["assignment"]
        prompt = input("Prompt, /pass, /refresh, or /quit: ").strip()
        if prompt == "/quit":
            return
        if prompt == "/refresh":
            state = client.request("/api/state")
            continue
        if prompt == "/pass":
            interpretation = None
            if assignment["stage"] == 12:
                interpretation = {
                    "application_for": input("This application is for: ").strip(),
                    "primary_user": input("Its primary user is: ").strip(),
                    "final_action_causes": input("Its final action causes: ").strip(),
                }
            state = client.request(
                "/api/pass",
                "POST",
                {
                    "assignment_id": assignment["id"],
                    "request_key": f"cli-pass-{assignment['id']}",
                    "interpretation": interpretation,
                },
            )
            continue
        if not prompt:
            continue
        result = client.request(
            "/api/run",
            "POST",
            {
                "assignment_id": assignment["id"],
                "prompt": prompt,
                "client_request_id": f"cli-run-{uuid.uuid4()}",
            },
        )
        print("\nAGENT:")
        print(result["response"])
        state = client.request("/api/state")


if __name__ == "__main__":
    main()
