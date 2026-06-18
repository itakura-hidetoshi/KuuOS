#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v07_plan_os_external_resume_handover_reentry import run_kernel


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "PLAN_OS_EXTERNAL_RESUME_HANDOVER_REENTRY_V0_7_OK",
        "hold_reentered": True,
        "hold_owner_id": "owner-alpha",
        "handover_reentered": True,
        "handover_owner_id": "owner-beta",
        "target_status": "ACTIVE",
        "next_generation_authorized": True,
        "execution_granted": False,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    if len(result.get("rejection_checks", [])) != 5:
        print("ERROR: rejection matrix incomplete", result)
        return 1
    print("PASS: PlanOS v0.7 external resume and handover re-entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
