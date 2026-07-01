#!/usr/bin/env python3
import os
from threading import Lock
from unittest.mock import patch

import runtime.v119_live_object_materialization_execution as execution
from runtime.v119_probe_adapter import run_bounded_object_git_command

_LOCK = Lock()


def _sanitized_environment() -> dict[str, str]:
    return {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }


def execute_repository_live_object_materialization(*args, **kwargs):
    if kwargs.get("git_executable", "git") != "git":
        raise ValueError("v119_git_executable_not_allowed")
    with _LOCK:
        with patch.dict(os.environ, _sanitized_environment(), clear=True):
            with patch.object(
                execution,
                "run_bounded_object_git_command",
                run_bounded_object_git_command,
            ):
                return execution.execute_repository_live_object_materialization(
                    *args, **kwargs
                )
