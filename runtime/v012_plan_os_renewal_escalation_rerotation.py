from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_renewal_escalation_scenarios_v0_12 import (
    run_deny,
    run_handover,
    run_rerotation,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v012-") as temporary:
        root = Path(temporary)
        denied = run_deny(root / "deny")
        handover = run_handover(root / "handover")
        rerotation = run_rerotation(root / "rerotation")
        result = {
            "status": "PLAN_OS_RENEWAL_ESCALATION_REROTATION_V0_12_OK",
            "deny_status": denied["status"],
            "handover_status": handover["status"],
            "handover_target_owner_id": handover["target_owner_id"],
            "rerotation_status": rerotation["status"],
            "rerotation_current_epoch_index": rerotation[
                "current_epoch_index"
            ],
            "rerotation_next_epoch_index": rerotation["next_epoch_index"],
            "new_v09_chain_required": rerotation[
                "new_v09_chain_required"
            ],
            "old_lease_lineage_closed": rerotation[
                "old_lease_lineage_closed"
            ],
            "continuation_granted": rerotation[
                "continuation_granted"
            ],
            "execution_granted": rerotation["execution_granted"],
            "host_license_granted": rerotation[
                "host_license_granted"
            ],
            "memory_overwrite": rerotation["memory_overwrite"],
        }
    from runtime.v013_plan_os_rerotation_materialization import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_REROTATION_MATERIALIZATION_V0_13_OK":
        raise AssertionError(next_result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
