#!/usr/bin/env python3
from runtime.v122_dedicated_index_execution import (
    execute_repository_dedicated_index as _execute,
)


def execute_repository_dedicated_index(*args, **kwargs):
    if kwargs.get("git_executable", "git") != "git":
        raise ValueError("v122_git_executable_not_allowed")
    return _execute(*args, **kwargs)
