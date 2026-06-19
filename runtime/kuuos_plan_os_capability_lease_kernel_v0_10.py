from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_capability_rotation_kernel_v0_9 import validate_capability_epoch_state
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import BOUND as CAPABILITY_BOUND, CAPABILITY_KINDS
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import (
    ACTIVE,
    BOUNDARY,
    EXHAUSTED,
    EXPIRED,
    NON_AUTHORITY,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    state_digest,
)


def build_capability_lease_state(
    *,
    capability_state: Mapping[str, Any],
    lease_specs: Mapping[str, Mapping[str, Any]],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_capability_epoch_state(capability_state)
    if errors:
        raise ValueError("lease_capability_state_invalid:" + ";".join(errors))
    if capability_state.get("status") != CAPABILITY_BOUND:
        raise ValueError("lease_requires_bound_capability_state")
    if set(lease_specs) != set(CAPABILITY_KINDS):
        raise ValueError("lease_specs_incomplete")
    leases: dict[str, dict[str, Any]] = {}
    bindings = dict(capability_state["capability_bindings"])
    created = require_int(now_ms, "now_ms")
    for kind in CAPABILITY_KINDS:
        spec = dict(lease_specs[kind])
        binding = dict(bindings[kind])
        stages = list(spec.get("allowed_stages", []))
        operations = list(spec.get("operation_allowlist", []))
        if not stages or not all(isinstance(item, str) and item for item in stages):
            raise ValueError(f"lease_allowed_stages_invalid:{kind}")
        if not operations or not all(isinstance(item, str) and item for item in operations):
            raise ValueError(f"lease_operation_allowlist_invalid:{kind}")
        if len(stages) != len(set(stages)) or len(operations) != len(set(operations)):
            raise ValueError(f"lease_scope_duplicate:{kind}")
        max_uses = require_int(spec.get("max_uses"), "max_uses", minimum=1)
        max_cost = require_int(spec.get("max_cost_units"), "max_cost_units", minimum=1)
        not_before = require_int(spec.get("not_before_ms"), "not_before_ms")
        expires = require_int(spec.get("expires_at_ms"), "expires_at_ms", minimum=not_before + 1)
        lease = {
            "kind": kind,
            "owner_id": capability_state["current_owner_id"],
            "epoch_digest": capability_state["current_epoch_digest"],
            "capability_digest": binding["issued_capability_digest"],
            "capability_binding_digest": binding["capability_reissue_binding_digest"],
            "scope_digest": require_string(spec.get("scope_digest"), "scope_digest"),
            "allowed_stages": stages,
            "operation_allowlist": operations,
            "max_uses": max_uses,
            "remaining_uses": max_uses,
            "max_cost_units": max_cost,
            "remaining_cost_units": max_cost,
            "not_before_ms": not_before,
            "expires_at_ms": expires,
            "status": ACTIVE,
            "renewal_count": 0,
            "last_renewal_receipt_digest": "",
        }
        leases[kind] = lease
    state = {
        "version": STATE_VERSION,
        "lease_supervisor_id": "lease:" + str(capability_state["rotation_id"]),
        "rotation_id": capability_state["rotation_id"],
        "continuity_id": capability_state["continuity_id"],
        "ownership_state_digest": capability_state["ownership_state_digest"],
        "capability_epoch_state_digest": capability_state["capability_epoch_state_digest"],
        "current_owner_id": capability_state["current_owner_id"],
        "current_epoch_index": capability_state["current_epoch_index"],
        "current_epoch_digest": capability_state["current_epoch_digest"],
        "leases": leases,
        "processed_consumption_digests": [],
        "processed_renewal_digests": [],
        "created_at_ms": created,
        "updated_at_ms": created,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "automatic_renewal": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "capability_lease_state_digest": "",
    }
    state["capability_lease_state_digest"] = state_digest(state)
    return state


def validate_capability_lease_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("lease_state_version_invalid")
        if state.get("capability_lease_state_digest") != state_digest(state):
            errors.append("lease_state_digest_invalid")
        for field in (
            "lease_supervisor_id", "rotation_id", "continuity_id",
            "ownership_state_digest", "capability_epoch_state_digest",
            "current_owner_id", "current_epoch_digest",
        ):
            require_string(state.get(field), field)
        require_int(state.get("current_epoch_index"), "current_epoch_index", minimum=1)
        leases = dict(state.get("leases", {}))
        if set(leases) != set(CAPABILITY_KINDS):
            errors.append("lease_state_inventory_invalid")
        for kind, lease in leases.items():
            if lease.get("kind") != kind:
                errors.append("lease_kind_key_mismatch")
            if lease.get("owner_id") != state.get("current_owner_id"):
                errors.append("lease_owner_mismatch")
            if lease.get("epoch_digest") != state.get("current_epoch_digest"):
                errors.append("lease_epoch_mismatch")
            max_uses = require_int(lease.get("max_uses"), "max_uses", minimum=1)
            remaining_uses = require_int(lease.get("remaining_uses"), "remaining_uses")
            max_cost = require_int(lease.get("max_cost_units"), "max_cost_units", minimum=1)
            remaining_cost = require_int(lease.get("remaining_cost_units"), "remaining_cost_units")
            if remaining_uses > max_uses or remaining_cost > max_cost:
                errors.append("lease_budget_increased")
            not_before = require_int(lease.get("not_before_ms"), "not_before_ms")
            expires = require_int(lease.get("expires_at_ms"), "expires_at_ms", minimum=not_before + 1)
            expected_status = EXHAUSTED if remaining_uses == 0 or remaining_cost == 0 else lease.get("status")
            if lease.get("status") not in (ACTIVE, EXHAUSTED, EXPIRED):
                errors.append("lease_status_invalid")
            if expected_status == EXHAUSTED and lease.get("status") == ACTIVE:
                errors.append("lease_exhaustion_status_invalid")
            require_string(lease.get("capability_digest"), "capability_digest")
            require_string(lease.get("capability_binding_digest"), "capability_binding_digest")
            require_string(lease.get("scope_digest"), "scope_digest")
            if not list(lease.get("allowed_stages", [])):
                errors.append("lease_allowed_stages_empty")
            if not list(lease.get("operation_allowlist", [])):
                errors.append("lease_operation_allowlist_empty")
            require_int(lease.get("renewal_count"), "renewal_count")
            if not isinstance(lease.get("last_renewal_receipt_digest"), str):
                errors.append("lease_last_renewal_digest_invalid")
        consumptions = list(state.get("processed_consumption_digests", []))
        renewals = list(state.get("processed_renewal_digests", []))
        if len(consumptions) != len(set(consumptions)):
            errors.append("lease_consumption_history_duplicate")
        if len(renewals) != len(set(renewals)):
            errors.append("lease_renewal_history_duplicate")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite", "automatic_renewal"):
            if state.get(field) is not False:
                errors.append(f"lease_state_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("lease_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("lease_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def refresh_expired_leases(state: Mapping[str, Any], *, now_ms: int) -> dict[str, Any]:
    errors = validate_capability_lease_state(state)
    if errors:
        raise ValueError("lease_state_invalid:" + ";".join(errors))
    now = require_int(now_ms, "now_ms")
    next_state = deepcopy(dict(state))
    changed = False
    for lease in next_state["leases"].values():
        if lease["status"] == ACTIVE and now >= int(lease["expires_at_ms"]):
            lease["status"] = EXPIRED
            changed = True
    if changed:
        next_state["updated_at_ms"] = now
        next_state["capability_lease_state_digest"] = ""
        next_state["capability_lease_state_digest"] = state_digest(next_state)
    return next_state
