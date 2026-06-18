from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_reentry_scenarios_v0_7 import (
    run_handover_acceptance,
    run_hold_resume,
    verify_rejections,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v07-") as temporary:
        hold = run_hold_resume(Path(temporary))
        handover = run_handover_acceptance()
        rejections = verify_rejections()
        return {
            "status": "PLAN_OS_EXTERNAL_RESUME_HANDOVER_REENTRY_V0_7_OK",
            "hold_reentered": hold["status"] == "REENTERED",
            "hold_owner_id": hold["current_owner_id"],
            "handover_reentered": handover["status"] == "REENTERED",
            "handover_owner_id": handover["current_owner_id"],
            "target_status": handover["target_active_state"]["status"],
            "next_generation_authorized": handover[
                "target_active_state"
            ]["next_generation_authorized"],
            "execution_granted": handover["execution_granted"],
            "rejection_checks": rejections,
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
