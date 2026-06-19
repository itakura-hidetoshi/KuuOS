from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_capability_rotation_scenarios_v0_9 import (
    run_handover_rotation,
    run_hold_rotation,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v09-") as temporary:
        handover = run_handover_rotation(Path(temporary))
        hold = run_hold_rotation()
        return {
            "status": "PLAN_OS_CAPABILITY_ROTATION_REVOCATION_V0_9_OK",
            "handover_previous_owner_id": handover["previous_owner_id"],
            "handover_current_owner_id": handover["current_owner_id"],
            "previous_epoch_index": handover["previous_epoch_index"],
            "current_epoch_index": handover["current_epoch_index"],
            "revoked_capability_count": len(
                handover["revoked_capability_digests"]
            ),
            "bound_capability_count": len(handover["capability_bindings"]),
            "handover_status": handover["status"],
            "hold_owner_id": hold["current_owner_id"],
            "hold_epoch_rotated": hold["previous_epoch_digest"]
            != hold["current_epoch_digest"],
            "execution_granted": handover["execution_granted"],
            "host_license_granted": handover["host_license_granted"],
            "memory_overwrite": handover["memory_overwrite"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
