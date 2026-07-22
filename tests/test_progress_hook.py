from workshop_runner.progress_hook import compact_event


def test_progress_hook_keeps_only_safe_activity_metadata():
    compact = compact_event(
        {
            "event": "tool.use",
            "tool_name": "write_file",
            "tool_args": {
                "file_path": "/tmp/stage/index.html",
                "content": "secret product specification",
            },
        }
    )
    assert compact == {
        "event": "tool.use",
        "tool": "write_file",
        "file": "index.html",
    }


def test_progress_hook_does_not_expose_paths_outside_allowlist():
    compact = compact_event(
        {
            "event": "tool.result",
            "tool_name": "read_file",
            "tool_status": "error",
            "tool_args": {"file_path": "/tmp/private.txt"},
        }
    )
    assert compact == {
        "event": "tool.result",
        "tool": "read_file",
        "status": "error",
    }
