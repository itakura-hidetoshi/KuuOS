#!/usr/bin/env python3
from runtime.v124_checkpoint_reflog_runtime import run_v124


if __name__ == "__main__":
    status = run_v124()
    if status != 0:
        raise RuntimeError("KuuOS repository runtime v1.24 failed")
