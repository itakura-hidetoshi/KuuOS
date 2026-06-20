#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_indra_transport_request_scenarios_v1_6 import (
    run_indra_transport_request_scenarios,
)
from runtime.kuuos_qi_world_licensed_blocker_discharge_scenarios_v1_7 import (
    run_licensed_blocker_discharge_scenarios,
)


def main() -> int:
    indra = run_indra_transport_request_scenarios()
    licensed = run_licensed_blocker_discharge_scenarios()
    expected = {
        "indra": "KUUOS_QI_WORLD_INDRA_TRANSPORT_REQUEST_V1_6_OK",
        "licensed": "KUUOS_QI_WORLD_LICENSED_BLOCKER_DISCHARGE_V1_7_OK",
    }
    observed = {
        "indra": indra.get("status"),
        "licensed": licensed.get("status"),
    }
    if observed != expected:
        print(
            json.dumps(
                {
                    "status": "KUUOS_QI_WORLD_INDRA_DISCHARGE_CHAIN_INVALID",
                    "expected": expected,
                    "observed": observed,
                    "indra_v1_6": indra,
                    "licensed_v1_7": licensed,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1
    assert indra["source_patch_id"] != indra["target_patch_id"]
    assert indra["disposition"] == "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED"
    assert indra["runtime_transport_realized"] is False
    assert all(value is False for value in indra["request_non_authority"].values())
    assert licensed["indra_transport_still_unrealized"] is True
    assert licensed["effect_recorded"] is True
    assert licensed["observation_required"] is True
    assert licensed["verification_required"] is True
    print(
        json.dumps(
            {
                "status": "KUUOS_QI_WORLD_INDRA_TRANSPORT_REQUEST_V1_6_OK",
                "indra_v1_6": indra,
                "licensed_v1_7": licensed,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
