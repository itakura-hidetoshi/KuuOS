from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_bounded_renewal_state_v0_11 import (
    build_bounded_renewal_state,
    validate_bounded_renewal_state,
)
from runtime.kuuos_plan_os_capability_binding_kernel_v0_9 import (
    apply_capability_reissue_binding,
    build_capability_reissue_binding,
)
from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import (
    build_capability_lease_state,
    validate_capability_lease_state,
)
from runtime.kuuos_plan_os_capability_rotation_kernel_v0_9 import (
    validate_capability_epoch_state,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BOUND,
    BOUNDARY as V09_BOUNDARY,
    CAPABILITY_KINDS,
    NON_AUTHORITY as V09_NON_AUTHORITY,
    ROTATED,
    STATE_VERSION as V09_STATE_VERSION,
    state_digest as capability_state_digest,
)
from runtime.kuuos_plan_os_renewal_escalation_state_v0_12 import (
    validate_renewal_escalation_state,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import (
    REROTATION_AUTHORIZED,
)
from runtime.kuuos_plan_os_rerotation_materialization_types_v0_13 import (
    BOUNDARY,
    MATERIALIZED,
    NON_AUTHORITY,
    RECEIPT_VERSION,
    copy_boundary,
    copy_non_authority,
    receipt_digest,
    require_int,
    require_string,
)


def _old_capability_inventory(
    source_bounded_renewal_state: Mapping[str, Any],
) -> list[str]:
    lease_state = dict(source_bounded_renewal_state["current_lease_state"])
    leases = dict(lease_state["leases"])
    if set(leases) != set(CAPABILITY_KINDS):
        raise ValueError("materialization_old_lease_inventory_incomplete")
    digests = [
        require_string(leases[kind].get("capability_digest"), "old_capability_digest")
        for kind in CAPABILITY_KINDS
    ]
    if len(digests) != len(set(digests)):
        raise ValueError("materialization_old_capability_digest_duplicate")
    return digests


def _build_fresh_capability_state(
    *,
    escalation_state: Mapping[str, Any],
    source_bounded_renewal_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    old_lease_state = dict(source_bounded_renewal_state["current_lease_state"])
    old_capabilities = _old_capability_inventory(source_bounded_renewal_state)
    seed = require_string(
        escalation_state.get("next_epoch_seed_digest"),
        "next_epoch_seed_digest",
    )
    continuity_id = require_string(
        escalation_state.get("continuity_id"), "continuity_id"
    )
    current_owner = require_string(
        escalation_state.get("current_owner_id"), "current_owner_id"
    )
    materialization_root = {
        "escalation_state_digest": escalation_state[
            "renewal_escalation_state_digest"
        ],
        "resolution_decision_digest": escalation_state[
            "resolution_decision_digest"
        ],
        "next_epoch_seed_digest": seed,
        "next_epoch_index": escalation_state["next_epoch_index"],
        "current_owner_id": current_owner,
        "revoked_capability_digests": old_capabilities,
    }
    state = {
        "version": V09_STATE_VERSION,
        "rotation_id": "capability-rerotation:" + sha(materialization_root),
        "continuity_id": continuity_id,
        "lineage_id": sha({"continuity": continuity_id, "seed": seed}),
        "mission_contract_digest": sha(
            {
                "source": source_bounded_renewal_state[
                    "bounded_renewal_state_digest"
                ],
                "kind": "rerotation-mission",
            }
        ),
        "policy_digest": sha(
            {
                "source": source_bounded_renewal_state[
                    "bounded_renewal_state_digest"
                ],
                "kind": "rerotation-policy",
            }
        ),
        "ownership_state_digest": old_lease_state[
            "ownership_state_digest"
        ],
        "capability_rotation_receipt_digest": sha(materialization_root),
        "previous_owner_id": current_owner,
        "current_owner_id": current_owner,
        "handover": False,
        "previous_epoch_index": escalation_state["current_epoch_index"],
        "previous_epoch_digest": escalation_state["current_epoch_digest"],
        "current_epoch_index": escalation_state["next_epoch_index"],
        "current_epoch_digest": seed,
        "revoked_capability_digests": old_capabilities,
        "required_reissue_kinds": list(CAPABILITY_KINDS),
        "capability_bindings": {},
        "processed_binding_digests": [],
        "status": ROTATED,
        "created_at_ms": require_int(now_ms, "now_ms"),
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": deepcopy(V09_NON_AUTHORITY),
        "boundary": deepcopy(V09_BOUNDARY),
        "capability_epoch_state_digest": "",
    }
    state["capability_epoch_state_digest"] = capability_state_digest(state)
    errors = validate_capability_epoch_state(state)
    if errors:
        raise ValueError("materialization_fresh_capability_state_invalid:" + ";".join(errors))
    return state


def materialize_rerotation_chain(
    *,
    escalation_state: Mapping[str, Any],
    source_bounded_renewal_state: Mapping[str, Any],
    binding_specs: Mapping[str, Mapping[str, Any]],
    lease_specs: Mapping[str, Mapping[str, Any]],
    renewal_policies: Mapping[str, Mapping[str, Any]],
    now_ms: int,
) -> dict[str, Any]:
    escalation_errors = validate_renewal_escalation_state(escalation_state)
    if escalation_errors:
        raise ValueError("materialization_escalation_state_invalid:" + ";".join(escalation_errors))
    source_errors = validate_bounded_renewal_state(source_bounded_renewal_state)
    if source_errors:
        raise ValueError("materialization_source_state_invalid:" + ";".join(source_errors))
    if escalation_state.get("status") != REROTATION_AUTHORIZED:
        raise ValueError("materialization_rerotation_not_authorized")
    if escalation_state.get("new_v09_chain_required") is not True:
        raise ValueError("materialization_v09_chain_not_required")
    if escalation_state.get("old_lease_lineage_closed") is not True:
        raise ValueError("materialization_old_lease_lineage_open")
    if escalation_state.get("bounded_renewal_state_digest") != source_bounded_renewal_state.get(
        "bounded_renewal_state_digest"
    ):
        raise ValueError("materialization_source_state_digest_mismatch")
    source_lease = dict(source_bounded_renewal_state["current_lease_state"])
    if escalation_state.get("source_lease_state_digest") != source_lease.get(
        "capability_lease_state_digest"
    ):
        raise ValueError("materialization_source_lease_digest_mismatch")
    if escalation_state.get("current_owner_id") != source_bounded_renewal_state.get(
        "current_owner_id"
    ):
        raise ValueError("materialization_owner_mismatch")
    if escalation_state.get("current_epoch_digest") != source_bounded_renewal_state.get(
        "current_epoch_digest"
    ):
        raise ValueError("materialization_epoch_mismatch")
    if escalation_state.get("next_epoch_index") != int(
        escalation_state["current_epoch_index"]
    ) + 1:
        raise ValueError("materialization_next_epoch_invalid")
    if set(binding_specs) != set(CAPABILITY_KINDS):
        raise ValueError("materialization_binding_specs_incomplete")
    authority_receipts = [
        require_string(
            binding_specs[kind].get("source_authority_receipt_digest"),
            "source_authority_receipt_digest",
        )
        for kind in CAPABILITY_KINDS
    ]
    issued_capabilities = [
        require_string(
            binding_specs[kind].get("issued_capability_digest"),
            "issued_capability_digest",
        )
        for kind in CAPABILITY_KINDS
    ]
    if len(authority_receipts) != len(set(authority_receipts)):
        raise ValueError("materialization_authority_receipt_reuse_forbidden")
    if len(issued_capabilities) != len(set(issued_capabilities)):
        raise ValueError("materialization_new_capability_duplicate")
    old_capabilities = set(_old_capability_inventory(source_bounded_renewal_state))
    if old_capabilities.intersection(issued_capabilities):
        raise ValueError("materialization_old_capability_reuse_forbidden")

    created = require_int(now_ms, "now_ms")
    capability_state = _build_fresh_capability_state(
        escalation_state=escalation_state,
        source_bounded_renewal_state=source_bounded_renewal_state,
        now_ms=created,
    )
    binding_digests: dict[str, str] = {}
    for offset, kind in enumerate(CAPABILITY_KINDS, start=1):
        spec = dict(binding_specs[kind])
        binding = build_capability_reissue_binding(
            state=capability_state,
            kind=kind,
            owner_id=str(escalation_state["current_owner_id"]),
            source_authority_receipt_digest=authority_receipts[offset - 1],
            issued_capability_digest=issued_capabilities[offset - 1],
            scope_digest=require_string(spec.get("scope_digest"), "scope_digest"),
            issued_at_ms=require_int(spec.get("issued_at_ms"), "issued_at_ms"),
            expires_at_ms=require_int(spec.get("expires_at_ms"), "expires_at_ms"),
        )
        applied = apply_capability_reissue_binding(capability_state, binding)
        if applied.get("status") != "APPLIED":
            raise ValueError("materialization_binding_rejected:" + kind)
        capability_state = applied["state"]
        binding_digests[kind] = binding[
            "capability_reissue_binding_digest"
        ]
    if capability_state.get("status") != BOUND:
        raise ValueError("materialization_capability_state_not_bound")

    lease_state = build_capability_lease_state(
        capability_state=capability_state,
        lease_specs=lease_specs,
        now_ms=created + 100,
    )
    renewal_state = build_bounded_renewal_state(
        lease_state=lease_state,
        policies=renewal_policies,
        now_ms=created + 200,
    )
    if lease_state.get("processed_consumption_digests") != []:
        raise ValueError("materialization_old_consumption_history_carried")
    if lease_state.get("processed_renewal_digests") != []:
        raise ValueError("materialization_old_lease_renewal_history_carried")
    for policy in renewal_state["policies"].values():
        if any(
            int(policy[field]) != 0
            for field in (
                "renewal_count",
                "cumulative_added_uses",
                "cumulative_added_cost_units",
            )
        ):
            raise ValueError("materialization_old_governance_history_carried")

    receipt = {
        "version": RECEIPT_VERSION,
        "status": MATERIALIZED,
        "escalation_id": escalation_state["escalation_id"],
        "source_escalation_state_digest": escalation_state[
            "renewal_escalation_state_digest"
        ],
        "source_resolution_decision_digest": escalation_state[
            "resolution_decision_digest"
        ],
        "source_bounded_renewal_state_digest": source_bounded_renewal_state[
            "bounded_renewal_state_digest"
        ],
        "continuity_id": escalation_state["continuity_id"],
        "current_owner_id": escalation_state["current_owner_id"],
        "previous_epoch_index": escalation_state["current_epoch_index"],
        "previous_epoch_digest": escalation_state["current_epoch_digest"],
        "current_epoch_index": escalation_state["next_epoch_index"],
        "current_epoch_digest": escalation_state[
            "next_epoch_seed_digest"
        ],
        "revoked_capability_digests": sorted(old_capabilities),
        "binding_digests": binding_digests,
        "capability_state": capability_state,
        "lease_state": lease_state,
        "renewal_state": renewal_state,
        "old_lease_lineage_closed": True,
        "old_histories_carried_forward": False,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "materialized_at_ms": created + 200,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "rerotation_materialization_receipt_digest": "",
    }
    receipt["rerotation_materialization_receipt_digest"] = receipt_digest(
        receipt
    )
    errors = validate_rerotation_materialization_receipt(receipt)
    if errors:
        raise ValueError("materialization_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_rerotation_materialization_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("materialization_receipt_version_invalid")
        if receipt.get("status") != MATERIALIZED:
            errors.append("materialization_receipt_status_invalid")
        if receipt.get("rerotation_materialization_receipt_digest") != receipt_digest(
            receipt
        ):
            errors.append("materialization_receipt_digest_invalid")
        for field in (
            "escalation_id",
            "source_escalation_state_digest",
            "source_resolution_decision_digest",
            "source_bounded_renewal_state_digest",
            "continuity_id",
            "current_owner_id",
            "previous_epoch_digest",
            "current_epoch_digest",
        ):
            require_string(receipt.get(field), field)
        previous_index = require_int(
            receipt.get("previous_epoch_index"), "previous_epoch_index", minimum=1
        )
        current_index = require_int(
            receipt.get("current_epoch_index"), "current_epoch_index", minimum=2
        )
        if current_index != previous_index + 1:
            errors.append("materialization_receipt_epoch_invalid")
        capability_state = dict(receipt.get("capability_state", {}))
        lease_state = dict(receipt.get("lease_state", {}))
        renewal_state = dict(receipt.get("renewal_state", {}))
        if validate_capability_epoch_state(capability_state):
            errors.append("materialization_capability_state_invalid")
        if validate_capability_lease_state(lease_state):
            errors.append("materialization_lease_state_invalid")
        if validate_bounded_renewal_state(renewal_state):
            errors.append("materialization_renewal_state_invalid")
        if capability_state.get("status") != BOUND:
            errors.append("materialization_capability_state_not_bound")
        for state in (capability_state, lease_state, renewal_state):
            if state.get("current_owner_id") != receipt.get("current_owner_id"):
                errors.append("materialization_output_owner_mismatch")
            if state.get("current_epoch_digest") != receipt.get(
                "current_epoch_digest"
            ):
                errors.append("materialization_output_epoch_mismatch")
        revoked = list(receipt.get("revoked_capability_digests", []))
        if set(revoked) != set(
            capability_state.get("revoked_capability_digests", [])
        ):
            errors.append("materialization_revocation_set_mismatch")
        new_capabilities = {
            binding.get("issued_capability_digest")
            for binding in capability_state.get("capability_bindings", {}).values()
        }
        if set(revoked).intersection(new_capabilities):
            errors.append("materialization_old_capability_reused")
        if lease_state.get("processed_consumption_digests") != []:
            errors.append("materialization_consumption_history_not_fresh")
        if lease_state.get("processed_renewal_digests") != []:
            errors.append("materialization_lease_renewal_history_not_fresh")
        for policy in renewal_state.get("policies", {}).values():
            if any(
                int(policy.get(field, -1)) != 0
                for field in (
                    "renewal_count",
                    "cumulative_added_uses",
                    "cumulative_added_cost_units",
                )
            ):
                errors.append("materialization_governance_history_not_fresh")
        if receipt.get("old_lease_lineage_closed") is not True:
            errors.append("materialization_old_lineage_not_closed")
        if receipt.get("old_histories_carried_forward") is not False:
            errors.append("materialization_history_carry_flag_invalid")
        for field in (
            "execution_granted",
            "host_license_granted",
            "memory_overwrite",
        ):
            if receipt.get(field) is not False:
                errors.append(f"materialization_receipt_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("materialization_non_authority_invalid")
        if dict(receipt.get("boundary", {})) != BOUNDARY:
            errors.append("materialization_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
