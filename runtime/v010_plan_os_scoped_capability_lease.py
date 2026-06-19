from __future__ import annotations

import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_capability_lease_scenarios_v0_10 import (
    run_consumption_and_renewal,
    run_expiry,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import HOST_LICENSE


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-v010-") as temporary:
        root = Path(temporary)
        state = run_consumption_and_renewal(root)
        expired = run_expiry(root)
        host = state["leases"][HOST_LICENSE]
        result = {
            "status": "PLAN_OS_SCOPED_CAPABILITY_LEASE_V0_10_OK",
            "owner_id": state["current_owner_id"],
            "epoch_index": state["current_epoch_index"],
            "remaining_uses": host["remaining_uses"],
            "remaining_cost": host["remaining_cost_units"],
            "renewals": host["renewal_count"],
            "expired": sum(
                1
                for item in expired["leases"].values()
                if item["status"] == "EXPIRED"
            ),
            "execution_granted": state["execution_granted"],
            "automatic_renewal": state["automatic_renewal"],
        }
    from runtime.v011_plan_os_bounded_renewal_governance import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_BOUNDED_RENEWAL_GOVERNANCE_V0_11_OK":
        raise AssertionError(next_result)
    return result
