#!/usr/bin/env python3
import os
from threading import Lock
from unittest.mock import patch

import runtime.v119_live_object_materialization_execution as execution
from runtime.v119_probe_adapter import run_bounded_object_git_command

_LOCK = Lock()
_UNSAFE_GIT_ENVIRONMENT = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
)


def _sanitized_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for name in _UNSAFE_GIT_ENVIRONMENT:
        environment.pop(name, None)
    return environment


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
