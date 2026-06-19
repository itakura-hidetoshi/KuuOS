from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_suspension_recovery_scenarios_v0_17 import (
    run_suspension_recovery,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v017-") as temporary:
        result = run_suspension_recovery(Path(temporary))
        revalidate = result["revalidate"]
        renewal = result["renewal"]
        escalation = result["escalation"]
        rerotation = result["rerotation"]
        return {
            "status": "PLAN_OS_SUSPENSION_RECOVERY_ROUTER_V0_17_OK",
            "revalidation_target": revalidate["target_stage"],
            "renewal_target": renewal["target_stage"],
            "renewal_candidate_count": len(
                renewal["renewal_candidate_kinds"]
            ),
            "escalation_target": escalation["target_stage"],
            "escalation_kind_count": len(
                escalation["escalation_required_kinds"]
            ),
            "rerotation_target": rerotation["target_stage"],
            "old_session_closed": rerotation["old_session_closed"],
            "old_session_resume_allowed": rerotation[
                "old_session_resume_allowed"
            ],
            "new_lineage_required": rerotation["new_lineage_required"],
            "new_activation_required": rerotation[
                "new_activation_required"
            ],
            "new_session_required": rerotation["new_session_required"],
            "execution_granted": rerotation["execution_granted"],
            "host_license_granted": rerotation[
                "host_license_granted"
            ],
            "memory_overwrite": rerotation["memory_overwrite"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
