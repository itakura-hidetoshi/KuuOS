#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v013_plan_os_rerotation_materialization import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_REROTATION_MATERIALIZATION_V0_13_OK"
    assert result["materialization_status"] == "MATERIALIZED"
    assert result["current_epoch_index"] == result["previous_epoch_index"] + 1
    assert result["revoked_capability_count"] == 4
    assert result["new_binding_count"] == 4
    assert result["capability_status"] == "BOUND"
    assert result["lease_count"] == 4
    assert result["lease_history_fresh"] is True
    assert result["renewal_history_fresh"] is True
    assert result["old_lease_lineage_closed"] is True
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.13")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
