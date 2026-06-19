from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_bounded_renewal_state_v0_11 import (
    validate_bounded_renewal_state,
)
from runtime.kuuos_plan_os_bounded_renewal_types_v0_11 import (
    ESCALATION_REQUIRED,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import (
    BOUNDARY,
    NON_AUTHORITY,
    OPEN,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    state_digest,
)


def build_renewal_escalation_state(
    *,
    bounded_renewal_state: Mapping[str, Any],
    capability_kind: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_bounded_renewal_state(bounded_renewal_state)
    if errors:
        raise ValueError("escalation_source_invalid:" + ";".join(errors))
    kind = require_string(capability_kind, "capability_kind")
    policy = dict(bounded_renewal_state.get("policies", {}).get(kind, {}))
    if not policy:
        raise ValueError("escalation_policy_missing")
    if policy.get("status") != ESCALATION_REQUIRED:
        raise ValueError("escalation_not_required")
    lease_state = dict(bounded_renewal_state["current_lease_state"])
    lease = dict(lease_state["leases"][kind])
    created = require_int(now_ms, "now_ms")
    state = {
        "version": STATE_VERSION,
        "escalation_id": "escalation:" + str(bounded_renewal_state["renewal_governor_id"]) + ":" + kind,
        "renewal_governor_id": bounded_renewal_state["renewal_governor_id"],
        "bounded_renewal_state_digest": bounded_renewal_state[
            "bounded_renewal_state_digest"
        ],
        "lease_supervisor_id": bounded_renewal_state["lease_supervisor_id"],
        "rotation_id": bounded_renewal_state["rotation_id"],
        "continuity_id": bounded_renewal_state["continuity_id"],
        "capability_kind": kind,
        "current_owner_id": bounded_renewal_state["current_owner_id"],
        "current_epoch_index": lease_state["current_epoch_index"],
        "current_epoch_digest": bounded_renewal_state["current_epoch_digest"],
        "source_lease_state_digest": lease_state[
            "capability_lease_state_digest"
        ],
        "source_lease_digest": require_string(
            lease.get("capability_digest"), "source_lease_digest"
        ),
        "source_scope_digest": require_string(
            lease.get("scope_digest"), "source_scope_digest"
        ),
        "source_renewal_count": int(policy["renewal_count"]),
        "source_added_uses": int(policy["cumulative_added_uses"]),
        "source_added_cost_units": int(
            policy["cumulative_added_cost_units"]
        ),
        "status": OPEN,
        "resolution_route": "",
        "resolution_decision_digest": "",
        "target_owner_id": "",
        "next_epoch_index": 0,
        "next_epoch_seed_digest": "",
        "old_lease_lineage_closed": False,
        "new_v09_chain_required": False,
        "continuation_granted": False,
        "created_at_ms": created,
        "updated_at_ms": created,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "renewal_escalation_state_digest": "",
    }
    state["renewal_escalation_state_digest"] = state_digest(state)
    return state


def validate_renewal_escalation_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("escalation_state_version_invalid")
        if state.get("renewal_escalation_state_digest") != state_digest(state):
            errors.append("escalation_state_digest_invalid")
        for field in (
            "escalation_id",
            "renewal_governor_id",
            "bounded_renewal_state_digest",
            "lease_supervisor_id",
            "rotation_id",
            "continuity_id",
            "capability_kind",
            "current_owner_id",
            "current_epoch_digest",
            "source_lease_state_digest",
            "source_lease_digest",
            "source_scope_digest",
        ):
            require_string(state.get(field), field)
        require_int(
            state.get("current_epoch_index"),
            "current_epoch_index",
            minimum=1,
        )
        require_int(state.get("source_renewal_count"), "source_renewal_count")
        require_int(state.get("source_added_uses"), "source_added_uses")
        require_int(
            state.get("source_added_cost_units"),
            "source_added_cost_units",
        )
        require_int(state.get("created_at_ms"), "created_at_ms")
        require_int(state.get("updated_at_ms"), "updated_at_ms")
        status = state.get("status")
        if status == OPEN:
            if any(
                (
                    state.get("resolution_route"),
                    state.get("resolution_decision_digest"),
                    state.get("target_owner_id"),
                    state.get("next_epoch_seed_digest"),
                )
            ):
                errors.append("escalation_open_resolution_fields_nonempty")
            if state.get("next_epoch_index") != 0:
                errors.append("escalation_open_next_epoch_nonzero")
            if state.get("old_lease_lineage_closed") is not False:
                errors.append("escalation_open_lineage_closed")
            if state.get("new_v09_chain_required") is not False:
                errors.append("escalation_open_v09_required")
            if state.get("continuation_granted") is not False:
                errors.append("escalation_open_continuation_granted")
        else:
            require_string(state.get("resolution_route"), "resolution_route")
            require_string(
                state.get("resolution_decision_digest"),
                "resolution_decision_digest",
            )
            if state.get("old_lease_lineage_closed") is not True:
                errors.append("escalation_resolved_lineage_not_closed")
        for field in (
            "execution_granted",
            "host_license_granted",
            "memory_overwrite",
        ):
            if state.get(field) is not False:
                errors.append(f"escalation_state_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("escalation_state_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("escalation_state_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
