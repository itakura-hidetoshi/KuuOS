from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_plan_os_renewal_escalation_decision_v0_12 import (
    validate_escalation_decision,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import RE_ROTATE
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    materialize_rerotation_chain,
)


def materialize_authorized_rerotation_chain(
    *,
    escalation_state: Mapping[str, Any],
    escalation_decision: Mapping[str, Any],
    source_bounded_renewal_state: Mapping[str, Any],
    binding_specs: Mapping[str, Mapping[str, Any]],
    lease_specs: Mapping[str, Mapping[str, Any]],
    renewal_policies: Mapping[str, Mapping[str, Any]],
    now_ms: int,
) -> dict[str, Any]:
    decision_errors = validate_escalation_decision(escalation_decision)
    if decision_errors:
        raise ValueError(
            "materialization_source_decision_invalid:"
            + ";".join(decision_errors)
        )
    if escalation_decision.get("route") != RE_ROTATE:
        raise ValueError("materialization_source_decision_not_rerotation")
    expected = {
        "escalation_id": escalation_state.get("escalation_id"),
        "renewal_escalation_decision_digest": escalation_state.get(
            "resolution_decision_digest"
        ),
        "current_owner_id": escalation_state.get("current_owner_id"),
        "current_epoch_index": escalation_state.get("current_epoch_index"),
        "current_epoch_digest": escalation_state.get("current_epoch_digest"),
        "next_epoch_index": escalation_state.get("next_epoch_index"),
        "next_epoch_seed_digest": escalation_state.get(
            "next_epoch_seed_digest"
        ),
        "target_owner_id": escalation_state.get("current_owner_id"),
        "new_v09_chain_required": True,
        "continuation_granted": True,
        "old_lease_lineage_closed": True,
    }
    for field, value in expected.items():
        if escalation_decision.get(field) != value:
            raise ValueError(f"materialization_decision_{field}_mismatch")
    return materialize_rerotation_chain(
        escalation_state=escalation_state,
        source_bounded_renewal_state=source_bounded_renewal_state,
        binding_specs=binding_specs,
        lease_specs=lease_specs,
        renewal_policies=renewal_policies,
        now_ms=now_ms,
    )
