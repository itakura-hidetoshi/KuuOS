#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v011_plan_os_bounded_renewal_governance import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_BOUNDED_RENEWAL_GOVERNANCE_V0_11_OK"
    assert result["renewal_count"] == 2
    assert result["cumulative_added_uses"] == 2
    assert result["cumulative_added_cost_units"] == 4
    assert result["policy_status"] == "ESCALATION_REQUIRED"
    assert result["lease_expires_at_ms"] == 60_000
    assert result["automatic_renewal"] is False
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.11")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
