"""Launch Deep Agents Code with a narrow Windows compatibility fix."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path


def _patch_windows_server_command() -> None:
    """Avoid DCode 0.1.44's Windows readiness false-positive on os.getcwd."""
    if os.name != "nt":
        return

    from deepagents_code.client.launch import server

    original: Callable[..., list[str]] = server._build_server_cmd

    def build_server_command(
        config_path: Path, *, host: str, port: int
    ) -> list[str]:
        command = original(config_path, host=host, port=port)
        command.insert(command.index("dev") + 1, "--allow-blocking")
        return command

    server._build_server_cmd = build_server_command


def main() -> None:
    _patch_windows_server_command()
    from deepagents_code.main import cli_main

    cli_main()


if __name__ == "__main__":
    main()
