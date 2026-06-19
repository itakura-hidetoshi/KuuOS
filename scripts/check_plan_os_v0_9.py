#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v09_plan_os_capability_rotation_revocation import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_CAPABILITY_ROTATION_REVOCATION_V0_9_OK"
    assert result["handover_current_owner_id"] == "owner-beta"
    assert result["current_epoch_index"] == result["previous_epoch_index"] + 1
    assert result["revoked_capability_count"] == 4
    assert result["bound_capability_count"] == 4
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
