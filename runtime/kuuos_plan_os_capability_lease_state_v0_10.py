from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_rotation_kernel_v0_9 import (
    validate_capability_epoch_state,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BOUND as CAPABILITIES_BOUND,
    CAPABILITY_KINDS,
)
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import (
    ACTIVE,
    BOUNDARY,
    EXHAUSTED,
    EXPIRED,
    NON_AUTHORITY,
    PARTIALLY_EXHAUSTED,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    state_digest,
)


def effective_lease_status(lease: Mapping[str, Any], now_ms: int) -> str:
    now = require_int(now_ms, "now_ms")
    if now >= int(lease["expires_at_ms"]):
        return EXPIRED
    if int(lease["used_uses"]) >= int(lease["max_uses"]):
        return EXHAUSTED
    if int(lease["used_cost_units"]) >= int(lease["max_cost_units"]):
        return EXHAUSTED
    return ACTIVE


def refresh_lease_statuses(state: Mapping[str, Any], now_ms: int) -> dict[str, Any]:
    next_state = deepcopy(dict(state))
    leases = deepcopy(dict(next_state["leases"]))
    for lease in leases.values():
        lease["status"] = effective_lease_status(lease, now_ms)
    active_count = sum(1 for lease in leases.values() if lease["status"] == ACTIVE)
    if active_count == len(leases):
        overall = ACTIVE
    elif active_count == 0:
        overall = EXHAUSTED
    else:
        overall = PARTIALLY_EXHAUSTED
    next_state["leases"] = leases
    next_state["status"] = overall
    next_state["updated_at_ms"] = require_int(now_ms, "now_ms")
    next_state["capability_lease_state_digest"] = ""
    next_state["capability_lease_state_digest"] = state_digest(next_state)
    return next_state


def build_capability_lease_state(
    *,
    capability_epoch_state: Mapping[str, Any],
    lease_specs: Sequence[Mapping[str, Any]],
    now_ms: int,
) -> dict[str, Any]:
    source_errors = validate_capability_epoch_state(capability_epoch_state)
    if source_errors:
        raise ValueError("lease_source_state_invalid:" + ";".join(source_errors))
    if capability_epoch_state.get("status") != CAPABILITIES_BOUND:
        raise ValueError("lease_source_capabilities_not_bound")
    if len(lease_specs) != len(CAPABILITY_KINDS):
        raise ValueError("lease_spec_inventory_incomplete")
    bindings = dict(capability_epoch_state["capability_bindings"])
    kinds: set[str] = set()
    leases: dict[str, dict[str, Any]] = {}
    for raw in lease_specs:
        kind = require_string(raw.get("kind"), "kind")
        if kind not in CAPABILITY_KINDS or kind in kinds:
            raise ValueError("lease_spec_kind_invalid")
        binding = dict(bindings.get(kind, {}))
        if not binding:
            raise ValueError("lease_source_binding_missing")
        stage = require_string(raw.get("stage"), "stage")
        operations = list(raw.get("operations", []))
        if not operations or any(
            not isinstance(operation, str) or not operation.strip()
            for operation in operations
        ):
            raise ValueError("lease_operations_required")
        if len(operations) != len(set(operations)):
            raise ValueError("lease_operations_duplicate")
        issued = require_int(raw.get("issued_at_ms"), "issued_at_ms")
        expires = require_int(
            raw.get("expires_at_ms"), "expires_at_ms", minimum=issued + 1
        )
        if issued < int(binding["issued_at_ms"]):
            raise ValueError("lease_issued_before_capability_binding")
        if expires > int(binding["expires_at_ms"]):
            raise ValueError("lease_exceeds_capability_binding_expiry")
        max_uses = require_int(raw.get("max_uses"), "max_uses", minimum=1)
        max_cost = require_int(
            raw.get("max_cost_units"), "max_cost_units", minimum=1
        )
        scope = require_string(raw.get("scope_digest"), "scope_digest")
        lease_id = sha(
            {
                "source_state": capability_epoch_state[
                    "capability_epoch_state_digest"
                ],
                "kind": kind,
                "binding": binding["capability_reissue_binding_digest"],
                "stage": stage,
                "operations": operations,
                "scope": scope,
                "max_uses": max_uses,
                "max_cost_units": max_cost,
                "issued_at_ms": issued,
                "expires_at_ms": expires,
            }
        )
        leases[kind] = {
            "lease_id": lease_id,
            "kind": kind,
            "owner_id": capability_epoch_state["current_owner_id"],
            "epoch_index": capability_epoch_state["current_epoch_index"],
            "epoch_digest": capability_epoch_state["current_epoch_digest"],
            "capability_binding_digest": binding[
                "capability_reissue_binding_digest"
            ],
            "issued_capability_digest": binding[
                "issued_capability_digest"
            ],
            "source_authority_receipt_digest": binding[
                "source_authority_receipt_digest"
            ],
            "stage": stage,
            "operations": operations,
            "scope_digest": scope,
            "max_uses": max_uses,
            "used_uses": 0,
            "max_cost_units": max_cost,
            "used_cost_units": 0,
            "generation": 0,
            "issued_at_ms": issued,
            "expires_at_ms": expires,
            "status": ACTIVE,
            "renewed_from_lease_id": "",
            "renewal_receipt_digest": "",
        }
        kinds.add(kind)
    state = {
        "version": STATE_VERSION,
        "supervisor_id": "lease:" + str(capability_epoch_state["rotation_id"]),
        "continuity_id": capability_epoch_state["continuity_id"],
        "lineage_id": capability_epoch_state["lineage_id"],
        "mission_contract_digest": capability_epoch_state[
            "mission_contract_digest"
        ],
        "policy_digest": capability_epoch_state["policy_digest"],
        "capability_epoch_state_digest": capability_epoch_state[
            "capability_epoch_state_digest"
        ],
        "capability_rotation_receipt_digest": capability_epoch_state[
            "capability_rotation_receipt_digest"
        ],
        "owner_id": capability_epoch_state["current_owner_id"],
        "epoch_index": capability_epoch_state["current_epoch_index"],
        "epoch_digest": capability_epoch_state["current_epoch_digest"],
        "leases": leases,
        "processed_consumption_digests": [],
        "processed_renewal_digests": [],
        "consumption_count": 0,
        "renewal_count": 0,
        "status": ACTIVE,
        "created_at_ms": require_int(now_ms, "now_ms"),
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "capability_lease_state_digest": "",
    }
    state["capability_lease_state_digest"] = state_digest(state)
    errors = validate_capability_lease_state(state)
    if errors:
        raise ValueError("lease_initial_state_invalid:" + ";".join(errors))
    return state


def validate_capability_lease_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("lease_state_version_invalid")
        if state.get("capability_lease_state_digest") != state_digest(state):
            errors.append("lease_state_digest_invalid")
        for field in (
            "supervisor_id",
            "continuity_id",
            "lineage_id",
            "mission_contract_digest",
            "policy_digest",
            "capability_epoch_state_digest",
            "capability_rotation_receipt_digest",
            "owner_id",
            "epoch_digest",
        ):
            require_string(state.get(field), field)
        require_int(state.get("epoch_index"), "epoch_index", minimum=1)
        leases = dict(state.get("leases", {}))
        if set(leases) != set(CAPABILITY_KINDS):
            errors.append("lease_state_inventory_invalid")
        lease_ids: list[str] = []
        for key, lease in leases.items():
            if lease.get("kind") != key:
                errors.append("lease_state_kind_key_mismatch")
            for field in (
                "lease_id",
                "owner_id",
                "epoch_digest",
                "capability_binding_digest",
                "issued_capability_digest",
                "source_authority_receipt_digest",
                "stage",
                "scope_digest",
            ):
                require_string(lease.get(field), f"lease_{field}")
            if lease.get("owner_id") != state.get("owner_id"):
                errors.append("lease_state_owner_mismatch")
            if lease.get("epoch_index") != state.get("epoch_index"):
                errors.append("lease_state_epoch_index_mismatch")
            if lease.get("epoch_digest") != state.get("epoch_digest"):
                errors.append("lease_state_epoch_digest_mismatch")
            operations = list(lease.get("operations", []))
            if not operations or len(operations) != len(set(operations)):
                errors.append("lease_state_operations_invalid")
            max_uses = require_int(lease.get("max_uses"), "max_uses", minimum=1)
            used_uses = require_int(lease.get("used_uses"), "used_uses")
            max_cost = require_int(
                lease.get("max_cost_units"), "max_cost_units", minimum=1
            )
            used_cost = require_int(
                lease.get("used_cost_units"), "used_cost_units"
            )
            if used_uses > max_uses or used_cost > max_cost:
                errors.append("lease_state_budget_overdrawn")
            require_int(lease.get("generation"), "generation")
            issued = require_int(lease.get("issued_at_ms"), "issued_at_ms")
            require_int(
                lease.get("expires_at_ms"),
                "expires_at_ms",
                minimum=issued + 1,
            )
            if lease.get("status") not in (ACTIVE, EXHAUSTED, EXPIRED):
                errors.append("lease_state_status_invalid")
            if not isinstance(lease.get("renewed_from_lease_id"), str):
                errors.append("lease_renewed_from_string_required")
            if not isinstance(lease.get("renewal_receipt_digest"), str):
                errors.append("lease_renewal_digest_string_required")
            lease_ids.append(str(lease.get("lease_id", "")))
        if len(lease_ids) != len(set(lease_ids)):
            errors.append("lease_state_lease_id_duplicate")
        consumptions = list(state.get("processed_consumption_digests", []))
        renewals = list(state.get("processed_renewal_digests", []))
        if len(consumptions) != len(set(consumptions)):
            errors.append("lease_consumption_history_duplicate")
        if len(renewals) != len(set(renewals)):
            errors.append("lease_renewal_history_duplicate")
        if state.get("consumption_count") != len(consumptions):
            errors.append("lease_consumption_count_invalid")
        if state.get("renewal_count") != len(renewals):
            errors.append("lease_renewal_count_invalid")
        if state.get("status") not in (ACTIVE, PARTIALLY_EXHAUSTED, EXHAUSTED):
            errors.append("lease_supervisor_status_invalid")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite"):
            if state.get(field) is not False:
                errors.append(f"lease_state_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("lease_state_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("lease_state_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
