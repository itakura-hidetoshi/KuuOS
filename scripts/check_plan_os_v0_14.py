#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v014_plan_os_materialized_chain_activation import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_MATERIALIZED_CHAIN_ACTIVATION_V0_14_OK"
    assert result["activation_status"] == "ACTIVATION_READY"
    assert result["active_from_cycle"] == result["current_cycle_index"] + 1
    assert result["mission_cycle_phase"] == "plan"
    assert result["scope_count"] == 4
    assert result["next_plan_cycle_handoff_ready"] is True
    assert result["chain_activation_authorized"] is True
    assert result["activation_single_use"] is True
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.14")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
