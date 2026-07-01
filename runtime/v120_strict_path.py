#!/usr/bin/env python3
import os
from threading import Lock
from types import SimpleNamespace
from unittest.mock import patch

import runtime.v120_tree_commit_git_adapter as git_adapter
import runtime.v120_tree_commit_materialization_execution as execution

_LOCK = Lock()


def _sanitized_environment() -> dict[str, str]:
    return {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }


def _safe_message_arguments(args, kwargs):
    positional = list(args)
    keyword = dict(kwargs)
    if len(positional) >= 3:
        message = positional[2]
        if not isinstance(message, str) or "\x00" in message or "\r" in message:
            positional[2] = ""
    elif "message" in keyword:
        message = keyword["message"]
        if not isinstance(message, str) or "\x00" in message or "\r" in message:
            keyword["message"] = ""
    return tuple(positional), keyword


def execute_repository_tree_commit_materialization(*args, **kwargs):
    if kwargs.get("git_executable", "git") != "git":
        raise ValueError("v120_git_executable_not_allowed")
    args, kwargs = _safe_message_arguments(args, kwargs)
    adapter_os = SimpleNamespace(environ=_sanitized_environment())
    with _LOCK:
        with patch.object(git_adapter, "os", adapter_os):
            return execution.execute_repository_tree_commit_materialization(
                *args, **kwargs
            )
