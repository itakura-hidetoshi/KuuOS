#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v06_plan_os_bounded_multi_generation_supervisor import run_kernel


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "PLAN_OS_BOUNDED_MULTI_GENERATION_SUPERVISOR_V0_6_OK",
        "completed_generations": 2,
        "current_cycle_index": 12,
        "terminal_status": "STOPPED",
        "terminal_reason": "STOP_CONVERGED",
        "next_generation_authorized": False,
        "ledger_commits": 2,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    if len(result.get("tested_decisions", [])) != 10:
        print("ERROR: decision matrix incomplete", result)
        return 1
    print("PASS: PlanOS v0.6 bounded multi-generation supervisor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
