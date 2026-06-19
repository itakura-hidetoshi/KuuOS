from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_materialized_chain_activation_scenarios_v0_14 import (
    run_activation,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v014-") as temporary:
        receipt = run_activation(Path(temporary))
        result = {
            "status": "PLAN_OS_MATERIALIZED_CHAIN_ACTIVATION_V0_14_OK",
            "activation_status": receipt["status"],
            "owner_id": receipt["owner_id"],
            "epoch_index": receipt["epoch_index"],
            "current_cycle_index": receipt["current_cycle_index"],
            "active_from_cycle": receipt["active_from_cycle"],
            "mission_cycle_phase": receipt["mission_cycle_phase"],
            "scope_count": len(receipt["scope_inventory"]),
            "next_plan_cycle_handoff_ready": receipt[
                "next_plan_cycle_handoff_ready"
            ],
            "chain_activation_authorized": receipt[
                "chain_activation_authorized"
            ],
            "activation_single_use": receipt["activation_single_use"],
            "execution_granted": receipt["execution_granted"],
            "host_license_granted": receipt["host_license_granted"],
            "memory_overwrite": receipt["memory_overwrite"],
        }
    from runtime.v015_plan_os_next_cycle_session_bootstrap import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_NEXT_CYCLE_SESSION_BOOTSTRAP_V0_15_OK":
        raise AssertionError(next_result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
