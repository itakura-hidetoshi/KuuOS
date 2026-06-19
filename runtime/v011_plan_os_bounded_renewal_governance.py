from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_bounded_renewal_scenarios_v0_11 import (
    run_bounded_renewal,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import HOST_LICENSE


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v011-") as temporary:
        state = run_bounded_renewal(Path(temporary))
        policy = state["policies"][HOST_LICENSE]
        lease = state["current_lease_state"]["leases"][HOST_LICENSE]
        result = {
            "status": "PLAN_OS_BOUNDED_RENEWAL_GOVERNANCE_V0_11_OK",
            "renewal_count": policy["renewal_count"],
            "cumulative_added_uses": policy["cumulative_added_uses"],
            "cumulative_added_cost_units": policy[
                "cumulative_added_cost_units"
            ],
            "policy_status": policy["status"],
            "lease_expires_at_ms": lease["expires_at_ms"],
            "automatic_renewal": state["automatic_renewal"],
            "execution_granted": state["execution_granted"],
            "host_license_granted": state["host_license_granted"],
            "memory_overwrite": state["memory_overwrite"],
        }
    from runtime.v012_plan_os_renewal_escalation_rerotation import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_RENEWAL_ESCALATION_REROTATION_V0_12_OK":
        raise AssertionError(next_result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
