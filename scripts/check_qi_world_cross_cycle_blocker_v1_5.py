#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_cross_cycle_blocker_scenarios_v1_5 import (
    run_cross_cycle_blocker_scenarios,
)
from runtime.kuuos_qi_world_licensed_blocker_discharge_scenarios_v1_6 import (
    run_licensed_blocker_discharge_scenarios,
)


def main() -> int:
    blocker = run_cross_cycle_blocker_scenarios()
    licensed = run_licensed_blocker_discharge_scenarios()
    expected = {
        "blocker": "KUUOS_QI_WORLD_CROSS_CYCLE_BLOCKER_V1_5_OK",
        "licensed": "KUUOS_QI_WORLD_LICENSED_BLOCKER_DISCHARGE_V1_6_OK",
    }
    observed = {
        "blocker": blocker.get("status"),
        "licensed": licensed.get("status"),
    }
    if observed != expected:
        print(
            json.dumps(
                {
                    "status": "KUUOS_QI_WORLD_BLOCKER_CHAIN_INVALID",
                    "expected": expected,
                    "observed": observed,
                    "blocker_v1_5": blocker,
                    "licensed_v1_6": licensed,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1
    print(
        json.dumps(
            {
                "status": "KUUOS_QI_WORLD_CROSS_CYCLE_BLOCKER_V1_5_OK",
                "blocker_v1_5": blocker,
                "licensed_v1_6": licensed,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
