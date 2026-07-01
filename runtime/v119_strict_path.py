#!/usr/bin/env python3
from threading import Lock
from unittest.mock import patch

import runtime.v119_live_object_materialization_execution as execution
from runtime.v119_probe_adapter import run_bounded_object_git_command

_LOCK = Lock()


def execute_repository_live_object_materialization(*args, **kwargs):
    with _LOCK:
        with patch.object(
            execution,
            "run_bounded_object_git_command",
            run_bounded_object_git_command,
        ):
            return execution.execute_repository_live_object_materialization(
                *args, **kwargs
            )
