#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CMDS = [
    [sys.executable, "scripts/run_two_truths_runtime_closure_checks_v0_1.py"],
    [sys.executable, "scripts/check_two_truths_runtime_finality_v0_1.py"],
]


def main() -> int:
    for cmd in CMDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            return code
    print("\nPASS: Two Truths finality v0.1 checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
