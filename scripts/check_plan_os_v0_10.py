#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v010_plan_os_scoped_capability_lease import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_SCOPED_CAPABILITY_LEASE_V0_10_OK"
    assert result["owner_id"] == "owner-beta"
    assert result["epoch_index"] == 4
    assert result["remaining_uses"] == 1
    assert result["remaining_cost"] == 3
    assert result["renewals"] == 1
    assert result["expired"] == 4
    assert result["execution_granted"] is False
    assert result["automatic_renewal"] is False
    print("PASS: PlanOS v0.10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
