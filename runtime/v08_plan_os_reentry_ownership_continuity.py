from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_ownership_continuity_scenarios_v0_8 import (
    run_handover_continuity,
    run_hold_continuity,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v08-") as temporary:
        handover = run_handover_continuity(Path(temporary))
        hold = run_hold_continuity()
        result = {
            "status": "PLAN_OS_REENTRY_OWNERSHIP_CONTINUITY_V0_8_OK",
            "handover_status": handover["status"],
            "handover_previous_owner_id": handover["previous_owner_id"],
            "handover_current_owner_id": handover["current_owner_id"],
            "handover_stage_index": handover["stage_index"],
            "handover_stage_count": len(handover["stage_receipt_digests"]),
            "hold_current_owner_id": hold["current_owner_id"],
            "hold_stage_index": hold["stage_index"],
            "execution_granted": handover["execution_granted"],
            "host_license_granted": handover["host_license_granted"],
            "memory_overwrite": handover["memory_overwrite"],
        }
    from runtime.v09_plan_os_capability_rotation_revocation import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_CAPABILITY_ROTATION_REVOCATION_V0_9_OK":
        raise AssertionError(next_result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
