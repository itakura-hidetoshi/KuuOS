from __future__ import annotations

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_integrated_long_duration_operation_kernel_v0_27 import (
    build_initial_state,
    build_integrated_operation_contract,
)
from runtime.kuuos_integrated_long_duration_operation_types_v0_27 import LOWER_COMPONENTS


def make_source_state() -> dict:
    contract = build_integrated_operation_contract(
        contract_id="lineage-v029-contract",
        mission_id="lineage-v029-mission",
        lineage_id="lineage-v029-root",
        lower_contract_digests={name: sha(name) for name in LOWER_COMPONENTS},
        initial_host_license_digest=sha("host-license"),
        max_cycle_cost=100,
        max_cycle_steps=20,
        max_cycle_duration_ms=10_000,
        max_lease_cycles=4,
        max_lease_cost=400,
        initial_lease_id="lineage-v029-lease",
        initial_lease_cycles=4,
        initial_lease_cost=400,
        initial_lease_expires_at_ms=200_000,
        user_control_policy_digest=sha("user-control"),
        recovery_policy_digest=sha("recovery-policy"),
        audit_policy_digest=sha("audit-policy"),
        created_at_ms=1_000,
    )
    return build_initial_state(contract=contract, initialized_at_ms=2_000)


__all__ = ["make_source_state"]
