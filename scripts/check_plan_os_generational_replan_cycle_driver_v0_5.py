#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v05_plan_os_generational_replan_cycle_driver import run_kernel


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "PLAN_OS_GENERATIONAL_REPLAN_CYCLE_DRIVER_V0_5_OK",
        "next_cycle_index": result["source_cycle_index"] + 1,
        "replan_phase_sequence": [
            "history", "qi_condition", "generate", "constrain",
            "deliberate", "synthesize", "commit_next",
        ],
        "second_generation_plan_id": "v05-second-generation-plan",
        "execution_granted": False,
        "ledger_commits": 1,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    print("PASS: PlanOS v0.5 generational replan cycle driver")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
