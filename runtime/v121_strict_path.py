#!/usr/bin/env python3
import os
from threading import Lock
from types import SimpleNamespace
from unittest.mock import patch

import runtime.v117_checkpoint_live_git_preflight_core as preflight_core
import runtime.v118_checkpoint_live_ref_cas_core as live_ref_core
import runtime.v121_constructed_commit_publication_execution as execution

_LOCK = Lock()


def _sanitized_environment() -> dict[str, str]:
    return {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }


def execute_repository_constructed_commit_publication(*args, **kwargs):
    if kwargs.get("git_executable", "git") != "git":
        raise ValueError("v121_git_executable_not_allowed")
    adapter_os = SimpleNamespace(environ=_sanitized_environment())
    with _LOCK:
        with patch.object(preflight_core, "os", adapter_os):
            with patch.object(live_ref_core, "os", adapter_os):
                return execution.execute_repository_constructed_commit_publication(
                    *args, **kwargs
                )
