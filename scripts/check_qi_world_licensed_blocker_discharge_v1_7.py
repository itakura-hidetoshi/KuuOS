#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_licensed_blocker_discharge_scenarios_v1_7 import (
    run_licensed_blocker_discharge_scenarios,
)
from runtime.kuuos_qi_world_licensed_effect_evidence_closure_scenarios_v1_8 import (
    run_licensed_effect_evidence_closure_scenarios,
)


def main() -> int:
    discharge = run_licensed_blocker_discharge_scenarios()
    closure = run_licensed_effect_evidence_closure_scenarios()
    expected = {
        "discharge": "KUUOS_QI_WORLD_LICENSED_BLOCKER_DISCHARGE_V1_7_OK",
        "closure": "KUUOS_QI_WORLD_LICENSED_EFFECT_EVIDENCE_CLOSURE_V1_8_OK",
    }
    observed = {
        "discharge": discharge.get("status"),
        "closure": closure.get("status"),
    }
    if observed != expected:
        print(
            json.dumps(
                {
                    "status": "KUUOS_QI_WORLD_LICENSED_EFFECT_CHAIN_INVALID",
                    "expected": expected,
                    "observed": observed,
                    "discharge_v1_7": discharge,
                    "closure_v1_8": closure,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1
    print(
        json.dumps(
            {
                "status": "KUUOS_QI_WORLD_LICENSED_BLOCKER_DISCHARGE_V1_7_OK",
                "discharge_v1_7": discharge,
                "closure_v1_8": closure,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
