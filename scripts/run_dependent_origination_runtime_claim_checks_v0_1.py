#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS = [
    [sys.executable, "scripts/run_dependent_origination_runtime_checks_v0_1.py"],
    [sys.executable, "scripts/eval_dependent_origination_runtime_claims_v0_1.py"],
    [sys.executable, "scripts/eval_dependent_origination_runtime_claims_v0_1.py", "--json"],
    [sys.executable, "scripts/check_dependent_origination_runtime_audit_chain_v0_1.py"],
]


def main() -> int:
    for cmd in COMMANDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
            return code
    print("\nPASS: Dependent Origination runtime claim checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
