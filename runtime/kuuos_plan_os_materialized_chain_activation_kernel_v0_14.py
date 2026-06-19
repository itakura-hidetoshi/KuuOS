from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_bounded_renewal_state_v0_11 import (
    validate_bounded_renewal_state,
)
from runtime.kuuos_plan_os_bounded_renewal_types_v0_11 import ACTIVE as RENEWAL_ACTIVE
from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import (
    validate_capability_lease_state,
)
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import ACTIVE as LEASE_ACTIVE
from runtime.kuuos_plan_os_capability_rotation_kernel_v0_9 import (
    validate_capability_epoch_state,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BOUND,
    CAPABILITY_KINDS,
)
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    validate_rerotation_materialization_receipt,
)
from runtime.kuuos_plan_os_rerotation_materialization_types_v0_13 import (
    MATERIALIZED,
)
from runtime.kuuos_plan_os_materialized_chain_activation_types_v0_14 import (
    ACTIVATION_READY,
    BOUNDARY,
    NON_AUTHORITY,
    RECEIPT_VERSION,
    copy_boundary,
    copy_non_authority,
    receipt_digest,
    require_int,
    require_string,
)


def _validate_fresh_chain(
    materialization_receipt: Mapping[str, Any], *, now_ms: int
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, str]]:
    receipt_errors = validate_rerotation_materialization_receipt(
        materialization_receipt
    )
    if receipt_errors:
        raise ValueError(
            "activation_materialization_invalid:" + ";".join(receipt_errors)
        )
    if materialization_receipt.get("status") != MATERIALIZED:
        raise ValueError("activation_materialization_not_ready")
    capability_state = dict(materialization_receipt["capability_state"])
    lease_state = dict(materialization_receipt["lease_state"])
    renewal_state = dict(materialization_receipt["renewal_state"])
    if validate_capability_epoch_state(capability_state):
        raise ValueError("activation_capability_state_invalid")
    if validate_capability_lease_state(lease_state):
        raise ValueError("activation_lease_state_invalid")
    if validate_bounded_renewal_state(renewal_state):
        raise ValueError("activation_renewal_state_invalid")
    if capability_state.get("status") != BOUND:
        raise ValueError("activation_capability_state_not_bound")
    owner = require_string(
        materialization_receipt.get("current_owner_id"), "current_owner_id"
    )
    epoch = require_string(
        materialization_receipt.get("current_epoch_digest"),
        "current_epoch_digest",
    )
    epoch_index = require_int(
        materialization_receipt.get("current_epoch_index"),
        "current_epoch_index",
        minimum=1,
    )
    for state_name, state in (
        ("capability", capability_state),
        ("lease", lease_state),
        ("renewal", renewal_state),
    ):
        if state.get("current_owner_id") != owner:
            raise ValueError(f"activation_{state_name}_owner_mismatch")
        if state.get("current_epoch_digest") != epoch:
            raise ValueError(f"activation_{state_name}_epoch_mismatch")
    if capability_state.get("current_epoch_index") != epoch_index:
        raise ValueError("activation_capability_epoch_index_mismatch")
    if lease_state.get("current_epoch_index") != epoch_index:
        raise ValueError("activation_lease_epoch_index_mismatch")
    if renewal_state.get("current_lease_state", {}).get(
        "capability_lease_state_digest"
    ) != lease_state.get("capability_lease_state_digest"):
        raise ValueError("activation_renewal_lease_state_mismatch")
    if renewal_state.get("current_lease_state", {}).get(
        "capability_epoch_state_digest"
    ) != capability_state.get("capability_epoch_state_digest"):
        raise ValueError("activation_renewal_capability_state_mismatch")

    now = require_int(now_ms, "now_ms")
    bindings = dict(capability_state.get("capability_bindings", {}))
    leases = dict(lease_state.get("leases", {}))
    policies = dict(renewal_state.get("policies", {}))
    if set(bindings) != set(CAPABILITY_KINDS):
        raise ValueError("activation_binding_inventory_incomplete")
    if set(leases) != set(CAPABILITY_KINDS):
        raise ValueError("activation_lease_inventory_incomplete")
    if set(policies) != set(CAPABILITY_KINDS):
        raise ValueError("activation_policy_inventory_incomplete")
    scope_inventory: dict[str, str] = {}
    for kind in CAPABILITY_KINDS:
        binding = dict(bindings[kind])
        lease = dict(leases[kind])
        policy = dict(policies[kind])
        if lease.get("status") != LEASE_ACTIVE:
            raise ValueError(f"activation_lease_not_active:{kind}")
        if now < int(lease["not_before_ms"]):
            raise ValueError(f"activation_lease_not_started:{kind}")
        if now >= int(lease["expires_at_ms"]):
            raise ValueError(f"activation_lease_expired:{kind}")
        if lease.get("owner_id") != owner:
            raise ValueError(f"activation_lease_owner_mismatch:{kind}")
        if lease.get("epoch_digest") != epoch:
            raise ValueError(f"activation_lease_epoch_mismatch:{kind}")
        if lease.get("capability_digest") != binding.get(
            "issued_capability_digest"
        ):
            raise ValueError(f"activation_lease_capability_mismatch:{kind}")
        if lease.get("capability_binding_digest") != binding.get(
            "capability_reissue_binding_digest"
        ):
            raise ValueError(f"activation_lease_binding_mismatch:{kind}")
        if int(lease.get("remaining_uses", 0)) <= 0:
            raise ValueError(f"activation_lease_use_budget_empty:{kind}")
        if int(lease.get("remaining_cost_units", 0)) <= 0:
            raise ValueError(f"activation_lease_cost_budget_empty:{kind}")
        scope_inventory[kind] = require_string(
            lease.get("scope_digest"), f"scope_digest_{kind}"
        )
        if policy.get("status") != RENEWAL_ACTIVE:
            raise ValueError(f"activation_renewal_policy_not_fresh:{kind}")
        for field in (
            "renewal_count",
            "cumulative_added_uses",
            "cumulative_added_cost_units",
            "last_renewed_at_ms",
        ):
            if int(policy.get(field, -1)) != 0:
                raise ValueError(f"activation_renewal_history_not_fresh:{kind}:{field}")
        if policy.get("last_governed_receipt_digest") != "":
            raise ValueError(
                f"activation_renewal_receipt_history_not_fresh:{kind}"
            )
    if lease_state.get("processed_consumption_digests") != []:
        raise ValueError("activation_consumption_history_not_fresh")
    if lease_state.get("processed_renewal_digests") != []:
        raise ValueError("activation_lease_renewal_history_not_fresh")
    if renewal_state.get("processed_governed_receipt_digests") != []:
        raise ValueError("activation_governed_renewal_history_not_fresh")
    return capability_state, lease_state, renewal_state, scope_inventory


def build_materialized_chain_activation_receipt(
    *,
    materialization_receipt: Mapping[str, Any],
    requested_owner_id: str,
    requested_epoch_digest: str,
    current_cycle_index: int,
    mission_cycle_state_digest: str,
    activation_authority_id: str,
    activation_authority_receipt_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    capability_state, lease_state, renewal_state, scopes = _validate_fresh_chain(
        materialization_receipt, now_ms=now_ms
    )
    owner = require_string(requested_owner_id, "requested_owner_id")
    epoch = require_string(requested_epoch_digest, "requested_epoch_digest")
    if owner != materialization_receipt.get("current_owner_id"):
        raise ValueError("activation_requested_owner_mismatch")
    if epoch != materialization_receipt.get("current_epoch_digest"):
        raise ValueError("activation_requested_epoch_mismatch")
    cycle = require_int(current_cycle_index, "current_cycle_index")
    next_cycle = cycle + 1
    authority = require_string(
        activation_authority_id, "activation_authority_id"
    )
    authority_receipt = require_string(
        activation_authority_receipt_digest,
        "activation_authority_receipt_digest",
    )
    scope_inventory_digest = sha(
        {
            "owner_id": owner,
            "epoch_digest": epoch,
            "scopes": scopes,
        }
    )
    next_plan_basis_digest = sha(
        {
            "materialization_receipt_digest": materialization_receipt[
                "rerotation_materialization_receipt_digest"
            ],
            "capability_state_digest": capability_state[
                "capability_epoch_state_digest"
            ],
            "lease_state_digest": lease_state[
                "capability_lease_state_digest"
            ],
            "renewal_state_digest": renewal_state[
                "bounded_renewal_state_digest"
            ],
            "owner_id": owner,
            "epoch_digest": epoch,
            "scope_inventory_digest": scope_inventory_digest,
            "active_from_cycle": next_cycle,
        }
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "status": ACTIVATION_READY,
        "materialization_receipt_digest": materialization_receipt[
            "rerotation_materialization_receipt_digest"
        ],
        "source_escalation_state_digest": materialization_receipt[
            "source_escalation_state_digest"
        ],
        "source_resolution_decision_digest": materialization_receipt[
            "source_resolution_decision_digest"
        ],
        "continuity_id": materialization_receipt["continuity_id"],
        "owner_id": owner,
        "epoch_index": materialization_receipt["current_epoch_index"],
        "epoch_digest": epoch,
        "capability_state_digest": capability_state[
            "capability_epoch_state_digest"
        ],
        "lease_state_digest": lease_state[
            "capability_lease_state_digest"
        ],
        "renewal_state_digest": renewal_state[
            "bounded_renewal_state_digest"
        ],
        "scope_inventory": scopes,
        "scope_inventory_digest": scope_inventory_digest,
        "current_cycle_index": cycle,
        "active_from_cycle": next_cycle,
        "mission_cycle_phase": "plan",
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "activation_authority_id": authority,
        "activation_authority_receipt_digest": authority_receipt,
        "next_plan_basis_digest": next_plan_basis_digest,
        "next_plan_cycle_handoff_ready": True,
        "chain_activation_authorized": True,
        "activation_single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "activated_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "materialized_chain_activation_receipt_digest": "",
    }
    receipt["materialized_chain_activation_receipt_digest"] = receipt_digest(
        receipt
    )
    errors = validate_materialized_chain_activation_receipt(receipt)
    if errors:
        raise ValueError("activation_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_materialized_chain_activation_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("activation_receipt_version_invalid")
        if receipt.get("status") != ACTIVATION_READY:
            errors.append("activation_receipt_status_invalid")
        if receipt.get(
            "materialized_chain_activation_receipt_digest"
        ) != receipt_digest(receipt):
            errors.append("activation_receipt_digest_invalid")
        for field in (
            "materialization_receipt_digest",
            "source_escalation_state_digest",
            "source_resolution_decision_digest",
            "continuity_id",
            "owner_id",
            "epoch_digest",
            "capability_state_digest",
            "lease_state_digest",
            "renewal_state_digest",
            "scope_inventory_digest",
            "mission_cycle_state_digest",
            "activation_authority_id",
            "activation_authority_receipt_digest",
            "next_plan_basis_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("epoch_index"), "epoch_index", minimum=1)
        current_cycle = require_int(
            receipt.get("current_cycle_index"), "current_cycle_index"
        )
        active_from = require_int(
            receipt.get("active_from_cycle"), "active_from_cycle", minimum=1
        )
        if active_from != current_cycle + 1:
            errors.append("activation_next_cycle_invalid")
        scopes = dict(receipt.get("scope_inventory", {}))
        if set(scopes) != set(CAPABILITY_KINDS):
            errors.append("activation_scope_inventory_invalid")
        if receipt.get("scope_inventory_digest") != sha(
            {
                "owner_id": receipt.get("owner_id"),
                "epoch_digest": receipt.get("epoch_digest"),
                "scopes": scopes,
            }
        ):
            errors.append("activation_scope_inventory_digest_invalid")
        if receipt.get("mission_cycle_phase") != "plan":
            errors.append("activation_phase_invalid")
        for field, expected in {
            "next_plan_cycle_handoff_ready": True,
            "chain_activation_authorized": True,
            "activation_single_use": True,
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"activation_{field}_invalid")
        require_int(receipt.get("activated_at_ms"), "activated_at_ms")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("activation_non_authority_invalid")
        if dict(receipt.get("boundary", {})) != BOUNDARY:
            errors.append("activation_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
