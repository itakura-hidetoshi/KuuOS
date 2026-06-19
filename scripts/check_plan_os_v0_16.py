#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v016_plan_os_lease_monitor_suspension import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_LEASE_MONITOR_SUSPENSION_V0_16_OK"
    assert result["session_status_after"] == "SESSION_SUSPENDED"
    assert result["tick_index"] == 2
    assert result["recovery_route"] == "RENEW_OR_ESCALATE"
    assert result["reason_count"] >= 1
    assert result["plan_progress_allowed"] is False
    assert result["session_suspended"] is True
    assert result["suspension_terminal"] is True
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.16")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
