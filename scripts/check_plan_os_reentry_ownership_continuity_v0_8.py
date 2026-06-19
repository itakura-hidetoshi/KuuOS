#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v08_plan_os_reentry_ownership_continuity import run_kernel


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "PLAN_OS_REENTRY_OWNERSHIP_CONTINUITY_V0_8_OK",
        "handover_status": "COMPLETED",
        "handover_previous_owner_id": "owner-alpha",
        "handover_current_owner_id": "owner-beta",
        "handover_stage_index": 5,
        "handover_stage_count": 5,
        "hold_current_owner_id": "owner-alpha",
        "hold_stage_index": 1,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    print("PASS: PlanOS v0.8 re-entry ownership continuity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
