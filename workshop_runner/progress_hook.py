"""Emit compact, non-sensitive Deep Agents Code hook events for the host UI."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


EDITABLE_FILES = {"index.html", "styles.css", "app.js"}


def compact_event(payload: dict[str, Any]) -> dict[str, str]:
    event = str(payload.get("event", "activity"))
    result = {"event": event}
    tool = payload.get("tool_name")
    if isinstance(tool, str) and tool:
        result["tool"] = tool[:80]
    status = payload.get("tool_status")
    if status in {"success", "error"}:
        result["status"] = status
    arguments = payload.get("tool_args")
    if isinstance(arguments, dict):
        for key in ("file_path", "path", "filename"):
            value = arguments.get(key)
            if isinstance(value, str) and Path(value).name in EDITABLE_FILES:
                result["file"] = Path(value).name
                break
    return result


def main() -> None:
    destination = os.getenv("WORKSHOP_DCODE_EVENT_LOG")
    if not destination:
        return
    try:
        payload = json.loads(sys.stdin.buffer.read())
        if not isinstance(payload, dict):
            return
        line = (json.dumps(compact_event(payload), separators=(",", ":")) + "\n").encode()
        descriptor = os.open(destination, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            os.write(descriptor, line)
        finally:
            os.close(descriptor)
    except (OSError, ValueError, TypeError):
        return


if __name__ == "__main__":
    main()
