#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/eval_kustring_runtime_packets_v0_2.py"],
    [sys.executable, "scripts/eval_kustring_runtime_packets_v0_2.py", "--json"],
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    return subprocess.run(list(cmd), cwd=ROOT).returncode


def main() -> int:
    for cmd in COMMANDS:
        code = run_command(cmd)
        if code != 0:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
            return code
    print("\nPASS: KuString runtime packet checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
