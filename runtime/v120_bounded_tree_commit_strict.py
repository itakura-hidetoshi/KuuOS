#!/usr/bin/env python3
from runtime.v120_bounded_tree_commit_execution import (
    execute_repository_bounded_tree_commit as _execute_repository_bounded_tree_commit,
)


def execute_repository_bounded_tree_commit(*args, **kwargs):
    if kwargs.get("git_executable", "git") != "git":
        raise ValueError("v120_git_executable_not_allowed")
    return _execute_repository_bounded_tree_commit(*args, **kwargs)
