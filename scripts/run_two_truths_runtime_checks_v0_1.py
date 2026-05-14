#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

CMDS = [
    [sys.executable, "examples/two_truths_mass_gap_runtime_adapter_minimal.py"],
    [sys.executable, "examples/two_truths_runtime_v0_1.py"],
    [sys.executable, "scripts/eval_two_truths_runtime_claims_v0_1.py"],
    [sys.executable, "scripts/eval_two_truths_runtime_claims_v0_1.py", "--json"],
    [sys.executable, "-m", "unittest", "tests/test_two_truths_runtime_v0_1.py"],
]


def main() -> int:
    for cmd in CMDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            return code
    print("\nPASS: Two Truths runtime v0.1 checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
