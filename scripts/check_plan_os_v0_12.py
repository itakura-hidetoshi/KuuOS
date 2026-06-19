#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v012_plan_os_renewal_escalation_rerotation import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "PLAN_OS_RENEWAL_ESCALATION_REROTATION_V0_12_OK"
    assert result["deny_status"] == "RESOLVED_DENIED"
    assert result["handover_status"] == "HANDOVER_PENDING"
    assert result["handover_target_owner_id"] == "human-owner-gamma"
    assert result["rerotation_status"] == "REROTATION_AUTHORIZED"
    assert result["rerotation_next_epoch_index"] == result["rerotation_current_epoch_index"] + 1
    assert result["new_v09_chain_required"] is True
    assert result["old_lease_lineage_closed"] is True
    assert result["continuation_granted"] is True
    assert result["execution_granted"] is False
    assert result["host_license_granted"] is False
    assert result["memory_overwrite"] is False
    print("PASS: PlanOS v0.12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
