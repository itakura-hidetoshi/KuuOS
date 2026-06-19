from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_rerotation_materialization_scenarios_v0_13 import (
    run_materialization,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v013-") as temporary:
        receipt = run_materialization(Path(temporary))
        capability_state = receipt["capability_state"]
        lease_state = receipt["lease_state"]
        renewal_state = receipt["renewal_state"]
        result = {
            "status": "PLAN_OS_REROTATION_MATERIALIZATION_V0_13_OK",
            "materialization_status": receipt["status"],
            "previous_epoch_index": receipt["previous_epoch_index"],
            "current_epoch_index": receipt["current_epoch_index"],
            "revoked_capability_count": len(
                receipt["revoked_capability_digests"]
            ),
            "new_binding_count": len(capability_state["capability_bindings"]),
            "capability_status": capability_state["status"],
            "lease_count": len(lease_state["leases"]),
            "lease_history_fresh": (
                lease_state["processed_consumption_digests"] == []
                and lease_state["processed_renewal_digests"] == []
            ),
            "renewal_history_fresh": all(
                policy["renewal_count"] == 0
                and policy["cumulative_added_uses"] == 0
                and policy["cumulative_added_cost_units"] == 0
                for policy in renewal_state["policies"].values()
            ),
            "old_lease_lineage_closed": receipt[
                "old_lease_lineage_closed"
            ],
            "execution_granted": receipt["execution_granted"],
            "host_license_granted": receipt["host_license_granted"],
            "memory_overwrite": receipt["memory_overwrite"],
        }
    from runtime.v014_plan_os_materialized_chain_activation import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_MATERIALIZED_CHAIN_ACTIVATION_V0_14_OK":
        raise AssertionError(next_result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
