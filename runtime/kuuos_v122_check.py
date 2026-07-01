#!/usr/bin/env python3
from runtime.v122_dedicated_index_runtime import run_v122


if __name__ == "__main__":
    status = run_v122()
    if status != 0:
        raise RuntimeError("KuuOS repository runtime v1.22 failed")
