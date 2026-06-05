#!/usr/bin/env python3
"""Run Regge Zero Governance v0.1 checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "validators" / "validate_regge_zero_governance_v0_1.py"


def main() -> int:
    result = subprocess.run([sys.executable, str(VALIDATOR)], cwd=str(ROOT), check=False)
    if result.returncode != 0:
        print("REGGE_ZERO_GOVERNANCE_CHECKS: FAIL")
        return result.returncode
    print("REGGE_ZERO_GOVERNANCE_CHECKS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
