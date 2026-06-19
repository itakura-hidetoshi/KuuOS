from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import validate_capability_lease_state
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS
from runtime.kuuos_plan_os_bounded_renewal_types_v0_11 import (
    ACTIVE,
    BOUNDARY,
    ESCALATION_REQUIRED,
    NON_AUTHORITY,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    state_digest,
)


def build_bounded_renewal_state(
    *,
    lease_state: Mapping[str, Any],
    policies: Mapping[str, Mapping[str, Any]],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_capability_lease_state(lease_state)
    if errors:
        raise ValueError("renewal_source_lease_state_invalid:" + ";".join(errors))
    if set(policies) != set(CAPABILITY_KINDS):
        raise ValueError("renewal_policy_inventory_incomplete")
    normalized: dict[str, dict[str, Any]] = {}
    for kind in CAPABILITY_KINDS:
        policy = dict(policies[kind])
        normalized[kind] = {
            "kind": kind,
            "renewal_authority_id": require_string(policy.get("renewal_authority_id"), "renewal_authority_id"),
            "max_renewals": require_int(policy.get("max_renewals"), "max_renewals", minimum=1),
            "max_cumulative_added_uses": require_int(policy.get("max_cumulative_added_uses"), "max_cumulative_added_uses", minimum=1),
            "max_cumulative_added_cost_units": require_int(policy.get("max_cumulative_added_cost_units"), "max_cumulative_added_cost_units", minimum=1),
            "absolute_expires_at_ms": require_int(
                policy.get("absolute_expires_at_ms"),
                "absolute_expires_at_ms",
                minimum=int(lease_state["leases"][kind]["expires_at_ms"]),
            ),
            "cooldown_ms": require_int(policy.get("cooldown_ms"), "cooldown_ms"),
            "renewal_count": 0,
            "cumulative_added_uses": 0,
            "cumulative_added_cost_units": 0,
            "last_renewed_at_ms": 0,
            "last_governed_receipt_digest": "",
            "status": ACTIVE,
        }
    created = require_int(now_ms, "now_ms")
    state = {
        "version": STATE_VERSION,
        "renewal_governor_id": "renewal:" + str(lease_state["lease_supervisor_id"]),
        "lease_supervisor_id": lease_state["lease_supervisor_id"],
        "rotation_id": lease_state["rotation_id"],
        "continuity_id": lease_state["continuity_id"],
        "source_lease_state": deepcopy(dict(lease_state)),
        "current_lease_state": deepcopy(dict(lease_state)),
        "current_owner_id": lease_state["current_owner_id"],
        "current_epoch_digest": lease_state["current_epoch_digest"],
        "policies": normalized,
        "processed_governed_receipt_digests": [],
        "created_at_ms": created,
        "updated_at_ms": created,
        "automatic_renewal": False,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "bounded_renewal_state_digest": "",
    }
    state["bounded_renewal_state_digest"] = state_digest(state)
    return state


def validate_bounded_renewal_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("bounded_renewal_state_version_invalid")
        if state.get("bounded_renewal_state_digest") != state_digest(state):
            errors.append("bounded_renewal_state_digest_invalid")
        for field in (
            "renewal_governor_id", "lease_supervisor_id", "rotation_id",
            "continuity_id", "current_owner_id", "current_epoch_digest",
        ):
            require_string(state.get(field), field)
        source_errors = validate_capability_lease_state(dict(state.get("source_lease_state", {})))
        current_errors = validate_capability_lease_state(dict(state.get("current_lease_state", {})))
        if source_errors:
            errors.append("bounded_renewal_source_lease_invalid")
        if current_errors:
            errors.append("bounded_renewal_current_lease_invalid")
        current = dict(state.get("current_lease_state", {}))
        if current.get("lease_supervisor_id") != state.get("lease_supervisor_id"):
            errors.append("bounded_renewal_lease_supervisor_mismatch")
        if current.get("current_owner_id") != state.get("current_owner_id"):
            errors.append("bounded_renewal_owner_mismatch")
        if current.get("current_epoch_digest") != state.get("current_epoch_digest"):
            errors.append("bounded_renewal_epoch_mismatch")
        policies = dict(state.get("policies", {}))
        if set(policies) != set(CAPABILITY_KINDS):
            errors.append("bounded_renewal_policy_inventory_invalid")
        for kind, policy in policies.items():
            if policy.get("kind") != kind:
                errors.append("bounded_renewal_policy_kind_mismatch")
            max_count = require_int(policy.get("max_renewals"), "max_renewals", minimum=1)
            count = require_int(policy.get("renewal_count"), "renewal_count")
            max_uses = require_int(policy.get("max_cumulative_added_uses"), "max_cumulative_added_uses", minimum=1)
            used_uses = require_int(policy.get("cumulative_added_uses"), "cumulative_added_uses")
            max_cost = require_int(policy.get("max_cumulative_added_cost_units"), "max_cumulative_added_cost_units", minimum=1)
            used_cost = require_int(policy.get("cumulative_added_cost_units"), "cumulative_added_cost_units")
            if count > max_count or used_uses > max_uses or used_cost > max_cost:
                errors.append("bounded_renewal_ceiling_exceeded")
            require_int(policy.get("absolute_expires_at_ms"), "absolute_expires_at_ms")
            require_int(policy.get("cooldown_ms"), "cooldown_ms")
            require_int(policy.get("last_renewed_at_ms"), "last_renewed_at_ms")
            require_string(policy.get("renewal_authority_id"), "renewal_authority_id")
            expected = ESCALATION_REQUIRED if (
                count >= max_count or used_uses >= max_uses or used_cost >= max_cost
            ) else ACTIVE
            if policy.get("status") != expected:
                errors.append("bounded_renewal_policy_status_invalid")
        processed = list(state.get("processed_governed_receipt_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("bounded_renewal_history_duplicate")
        for field in ("automatic_renewal", "execution_granted", "host_license_granted", "memory_overwrite"):
            if state.get(field) is not False:
                errors.append(f"bounded_renewal_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("bounded_renewal_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("bounded_renewal_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
