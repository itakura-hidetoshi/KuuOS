#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_atomic_checkpoint_creation_v1_02 import (
    execute_atomic_repository_checkpoint_creation as _execute,
    repository_atomic_checkpoint_creation_result_issues as _issues,
)


def execute_atomic_repository_checkpoint_creation(*args, **kwargs):
    result, final_state, final_registry = _execute(*args, **kwargs)
    if args:
        issues = _issues(
            result,
            final_state,
            final_registry,
            *args[1:],
            **kwargs,
        )
    else:
        issue_kwargs = dict(kwargs)
        issue_kwargs.pop("transaction_id", None)
        issues = _issues(
            result,
            final_state,
            final_registry,
            **issue_kwargs,
        )
    if issues:
        raise ValueError(f"atomic_checkpoint_result_invalid:{issues[0]}")
    return result, final_state, final_registry


def repository_atomic_checkpoint_creation_result_issues(*args, **kwargs):
    return _issues(*args, **kwargs)
