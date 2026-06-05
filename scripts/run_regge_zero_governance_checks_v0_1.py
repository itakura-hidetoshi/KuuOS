#!/usr/bin/env python3
"""Run Regge Zero Governance v0.1 checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "validators/validate_regge_zero_governance_v0_1.py"],
    [sys.executable, "tests/test_regge_zero_governance_validator_v0_1.py"],
    [sys.executable, "validators/validate_regge_zero_governance_regression_addendum_v0_1.py"],
    [sys.executable, "validators/check_regge_zero_governance_finality_packet_v0_1.py"],
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    completed = subprocess.run(list(cmd), cwd=str(ROOT), check=False)
    return completed.returncode


def main() -> int:
    for cmd in COMMANDS:
        code = run_command(cmd)
        if code != 0:
            print("REGGE_ZERO_GOVERNANCE_CHECKS: FAIL")
            return code
    print("REGGE_ZERO_GOVERNANCE_CHECKS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
