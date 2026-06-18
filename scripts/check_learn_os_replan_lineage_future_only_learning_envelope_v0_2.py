#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v02_learn_os_replan_lineage_future_only_learning_envelope import (
    run_kernel,
)


def main() -> int:
    result = run_kernel()
    expected = {
        "status": "LEARN_OS_REPLAN_LINEAGE_FUTURE_ONLY_LEARNING_ENVELOPE_V0_2_OK",
        "learning_route": "LEARNING_REINFORCEMENT_CANDIDATE",
        "learning_kind": "reinforcement",
        "replan_handoff_ready": True,
        "future_only": True,
        "ledger_commits": 2,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            print("ERROR:", field, result)
            return 1
    print("PASS: LearnOS v0.2 replan-lineage future-only learning envelope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
