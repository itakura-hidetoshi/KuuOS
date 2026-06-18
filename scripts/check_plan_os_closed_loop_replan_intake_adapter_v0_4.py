#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_plan_os_closed_loop_monotone_patch_v0_4 import (
    install_monotone_stage_fixtures,
)

install_monotone_stage_fixtures()

from runtime.v04_plan_os_closed_loop_replan_intake_adapter import run_kernel


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "PLAN_OS_CLOSED_LOOP_REPLAN_INTAKE_ADAPTER_V0_4_OK",
        "bound_replan_phase": "bind",
        "next_phase": "history",
        "history_phase_required": True,
        "future_only": True,
        "ledger_commits": 2,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    print("PASS: PlanOS v0.4 closed-loop replan intake adapter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
