#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_cross_cycle_reentry_scenarios_v1_4 import (
    run_cross_cycle_reentry_scenarios,
)


def main() -> int:
    result = run_cross_cycle_reentry_scenarios()
    assert result["status"] == "KUUOS_QI_WORLD_CROSS_CYCLE_REENTRY_V1_4_OK"
    assert result["next_artifact_count"] == 6
    assert result["next_act_not_started"] is True
    assert result["next_plan_basis_digest"] == result[
        "previous_learning_delta_digest"
    ]
    assert all(
        value is False for value in result["cross_cycle_non_authority"].values()
    )
    print("PASS: Qi-WORLD cross-cycle reentry v1.4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
