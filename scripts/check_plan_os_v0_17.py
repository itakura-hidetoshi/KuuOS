#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v017_plan_os_suspension_recovery_router import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_SUSPENSION_RECOVERY_ROUTER_V0_17_OK"
    assert result["revalidation_target"] == "REVALIDATION_REQUIRED"
    assert result["renewal_target"] == "V11_RENEWAL_REVIEW"
    assert result["renewal_candidate_count"] == 1
    assert result["escalation_target"] == "V12_ESCALATION_REQUIRED"
    assert result["escalation_kind_count"] == 4
    assert result["rerotation_target"] == "V12_REROTATION_REQUIRED"
    assert result["old_session_closed"] is True
    assert result["old_session_resume_allowed"] is False
    assert result["new_lineage_required"] is True
    assert result["new_activation_required"] is True
    assert result["new_session_required"] is True
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.17")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
