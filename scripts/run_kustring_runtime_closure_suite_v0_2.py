#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS = [
    [sys.executable, "scripts/run_kustring_runtime_suite_v0_2.py"],
    [sys.executable, "scripts/check_kustring_runtime_closure_v0_2.py"],
]


def main() -> int:
    for cmd in COMMANDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
            return code
    print("\nPASS: KuString runtime closure suite v0.2 completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
