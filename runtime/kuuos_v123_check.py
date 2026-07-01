#!/usr/bin/env python3
from runtime.v123_sandbox_worktree_runtime import run_v123


if __name__ == "__main__":
    status = run_v123()
    if status != 0:
        raise RuntimeError("KuuOS repository runtime v1.23 failed")
