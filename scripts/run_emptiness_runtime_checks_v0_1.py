#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS = [
    [sys.executable, "examples/emptiness_runtime_v0_1.py"],
    [sys.executable, "scripts/eval_emptiness_runtime_claims_v0_1.py"],
    [sys.executable, "scripts/eval_emptiness_runtime_claims_v0_1.py", "--json"],
    [sys.executable, "scripts/check_emptiness_runtime_audit_chain_v0_1.py"],
    [sys.executable, "scripts/check_emptiness_runtime_worm_receipt_v0_1.py"],
    [sys.executable, "scripts/check_emptiness_runtime_bundle_v0_1.py"],
    [sys.executable, "-m", "unittest", "tests/test_emptiness_runtime_v0_1.py"],
]


def main() -> int:
    for cmd in COMMANDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
            return code
    print("\nPASS: Emptiness runtime v0.1 checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
