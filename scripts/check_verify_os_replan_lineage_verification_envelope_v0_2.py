#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v02_verify_os_replan_lineage_verification_envelope import (
    run_kernel,
)


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "VERIFY_OS_REPLAN_LINEAGE_VERIFICATION_ENVELOPE_V0_2_OK",
        "route": "VERIFICATION_PASSED",
        "verdict": "passed",
        "verification_debt_discharged": True,
        "learning_required": True,
        "learning_must_be_future_only": True,
        "ledger_commits": 2,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    print("PASS: VerifyOS v0.2 replan-lineage verification envelope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
