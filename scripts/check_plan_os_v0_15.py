#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v015_plan_os_next_cycle_session_bootstrap import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_NEXT_CYCLE_SESSION_BOOTSTRAP_V0_15_OK"
    assert result["session_status"] == "SESSION_ACTIVE"
    assert result["mission_cycle_index"] == 13
    assert result["mission_cycle_phase"] == "plan"
    assert result["plan_phase"] == "bind"
    assert result["event_index"] == 0
    assert result["step_count"] == 0
    assert result["lease_clock_count"] == 4
    assert result["lease_monitor_deadline_ms"] > result["lease_monitor_started_at_ms"]
    assert result["activation_consumed"] is True
    assert result["session_single_use"] is True
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.15")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
