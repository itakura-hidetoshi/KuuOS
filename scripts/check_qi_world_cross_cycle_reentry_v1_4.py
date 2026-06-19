#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_cross_cycle_reentry_scenarios_v1_4 import (
    run_cross_cycle_reentry_scenarios,
)
from runtime.kuuos_qi_world_cross_cycle_blocker_scenarios_v1_5 import (
    run_cross_cycle_blocker_scenarios,
)


def main() -> int:
    cross_cycle = run_cross_cycle_reentry_scenarios()
    blocker = run_cross_cycle_blocker_scenarios()
    expected = {
        "cross_cycle": "KUUOS_QI_WORLD_CROSS_CYCLE_REENTRY_V1_4_OK",
        "blocker": "KUUOS_QI_WORLD_CROSS_CYCLE_BLOCKER_V1_5_OK",
    }
    observed = {
        "cross_cycle": cross_cycle.get("status"),
        "blocker": blocker.get("status"),
    }
    if observed != expected:
        print(
            json.dumps(
                {
                    "status": "KUUOS_QI_WORLD_CROSS_CYCLE_CHAIN_INVALID",
                    "expected": expected,
                    "observed": observed,
                    "cross_cycle": cross_cycle,
                    "blocker": blocker,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1
    print(
        json.dumps(
            {
                "status": "KUUOS_QI_WORLD_CROSS_CYCLE_REENTRY_V1_4_OK",
                "cross_cycle": cross_cycle,
                "blocker_v1_5": blocker,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
