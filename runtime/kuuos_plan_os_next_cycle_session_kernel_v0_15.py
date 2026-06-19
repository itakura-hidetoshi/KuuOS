from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS
from runtime.kuuos_plan_os_materialized_chain_activation_kernel_v0_14 import (
    validate_materialized_chain_activation_receipt,
)
from runtime.kuuos_plan_os_materialized_chain_activation_types_v0_14 import (
    ACTIVATION_READY,
)
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    validate_rerotation_materialization_receipt,
)
from runtime.kuuos_plan_os_rerotation_materialization_types_v0_13 import (
    MATERIALIZED,
)
from runtime.kuuos_plan_os_next_cycle_session_types_v0_15 import (
    BOUNDARY,
    NON_AUTHORITY,
    PLAN_BIND,
    SESSION_ACTIVE,
    SESSION_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    session_digest,
)


def build_next_cycle_plan_session(
    *,
    activation_receipt: Mapping[str, Any],
    materialization_receipt: Mapping[str, Any],
    mission_cycle_index: int,
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    requested_owner_id: str,
    requested_epoch_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    activation_errors = validate_materialized_chain_activation_receipt(
        activation_receipt
    )
    if activation_errors:
        raise ValueError(
            "session_activation_receipt_invalid:" + ";".join(activation_errors)
        )
    materialization_errors = validate_rerotation_materialization_receipt(
        materialization_receipt
    )
    if materialization_errors:
        raise ValueError(
            "session_materialization_receipt_invalid:"
            + ";".join(materialization_errors)
        )
    if activation_receipt.get("status") != ACTIVATION_READY:
        raise ValueError("session_activation_not_ready")
    if materialization_receipt.get("status") != MATERIALIZED:
        raise ValueError("session_materialization_not_ready")
    if activation_receipt.get("materialization_receipt_digest") != materialization_receipt.get(
        "rerotation_materialization_receipt_digest"
    ):
        raise ValueError("session_materialization_digest_mismatch")
    for field, expected in {
        "source_escalation_state_digest": materialization_receipt.get(
            "source_escalation_state_digest"
        ),
        "source_resolution_decision_digest": materialization_receipt.get(
            "source_resolution_decision_digest"
        ),
        "continuity_id": materialization_receipt.get("continuity_id"),
        "owner_id": materialization_receipt.get("current_owner_id"),
        "epoch_index": materialization_receipt.get("current_epoch_index"),
        "epoch_digest": materialization_receipt.get("current_epoch_digest"),
        "capability_state_digest": materialization_receipt.get(
            "capability_state", {}
        ).get("capability_epoch_state_digest"),
        "lease_state_digest": materialization_receipt.get("lease_state", {}).get(
            "capability_lease_state_digest"
        ),
        "renewal_state_digest": materialization_receipt.get(
            "renewal_state", {}
        ).get("bounded_renewal_state_digest"),
    }.items():
        if activation_receipt.get(field) != expected:
            raise ValueError(f"session_activation_{field}_mismatch")
    cycle = require_int(mission_cycle_index, "mission_cycle_index", minimum=1)
    if cycle != activation_receipt.get("active_from_cycle"):
        raise ValueError("session_cycle_mismatch")
    phase = require_string(mission_cycle_phase, "mission_cycle_phase")
    if phase != "plan" or activation_receipt.get("mission_cycle_phase") != "plan":
        raise ValueError("session_phase_mismatch")
    owner = require_string(requested_owner_id, "requested_owner_id")
    epoch = require_string(requested_epoch_digest, "requested_epoch_digest")
    if owner != activation_receipt.get("owner_id"):
        raise ValueError("session_owner_mismatch")
    if epoch != activation_receipt.get("epoch_digest"):
        raise ValueError("session_epoch_mismatch")
    now = require_int(now_ms, "now_ms")
    leases = dict(materialization_receipt.get("lease_state", {}).get("leases", {}))
    if set(leases) != set(CAPABILITY_KINDS):
        raise ValueError("session_lease_inventory_incomplete")
    scopes = dict(activation_receipt.get("scope_inventory", {}))
    if set(scopes) != set(CAPABILITY_KINDS):
        raise ValueError("session_scope_inventory_incomplete")
    lease_clocks: dict[str, dict[str, Any]] = {}
    deadlines: list[int] = []
    for kind in CAPABILITY_KINDS:
        lease = dict(leases[kind])
        not_before = require_int(lease.get("not_before_ms"), "not_before_ms")
        expires = require_int(lease.get("expires_at_ms"), "expires_at_ms", minimum=1)
        if now < not_before:
            raise ValueError(f"session_lease_not_started:{kind}")
        if now >= expires:
            raise ValueError(f"session_lease_expired:{kind}")
        if lease.get("owner_id") != owner:
            raise ValueError(f"session_lease_owner_mismatch:{kind}")
        if lease.get("epoch_digest") != epoch:
            raise ValueError(f"session_lease_epoch_mismatch:{kind}")
        if lease.get("scope_digest") != scopes[kind]:
            raise ValueError(f"session_lease_scope_mismatch:{kind}")
        if int(lease.get("remaining_uses", 0)) <= 0:
            raise ValueError(f"session_lease_use_budget_empty:{kind}")
        if int(lease.get("remaining_cost_units", 0)) <= 0:
            raise ValueError(f"session_lease_cost_budget_empty:{kind}")
        deadlines.append(expires)
        lease_clocks[kind] = {
            "scope_digest": lease["scope_digest"],
            "not_before_ms": not_before,
            "expires_at_ms": expires,
            "remaining_uses": int(lease["remaining_uses"]),
            "remaining_cost_units": int(lease["remaining_cost_units"]),
            "monitor_status": "MONITORING",
        }
    session_id = "plan-session:" + sha(
        {
            "activation_receipt_digest": activation_receipt[
                "materialized_chain_activation_receipt_digest"
            ],
            "mission_cycle_index": cycle,
            "owner_id": owner,
            "epoch_digest": epoch,
        }
    )
    plan_bootstrap = {
        "plan_session_id": session_id,
        "current_phase": PLAN_BIND,
        "event_index": 0,
        "plan_version": 0,
        "completed_plans": 0,
        "steps": [],
        "topological_order": [],
        "next_plan_basis_digest": activation_receipt["next_plan_basis_digest"],
        "plan_basis_bound": True,
        "source_identity_preserved": True,
        "execution_permission": False,
    }
    state = {
        "version": SESSION_VERSION,
        "status": SESSION_ACTIVE,
        "plan_control_session_id": session_id,
        "activation_receipt_digest": activation_receipt[
            "materialized_chain_activation_receipt_digest"
        ],
        "materialization_receipt_digest": materialization_receipt[
            "rerotation_materialization_receipt_digest"
        ],
        "continuity_id": activation_receipt["continuity_id"],
        "owner_id": owner,
        "epoch_index": activation_receipt["epoch_index"],
        "epoch_digest": epoch,
        "scope_inventory": scopes,
        "scope_inventory_digest": activation_receipt[
            "scope_inventory_digest"
        ],
        "capability_state_digest": activation_receipt[
            "capability_state_digest"
        ],
        "lease_state_digest": activation_receipt["lease_state_digest"],
        "renewal_state_digest": activation_receipt["renewal_state_digest"],
        "mission_cycle_index": cycle,
        "mission_cycle_phase": "plan",
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "predecessor_mission_cycle_state_digest": activation_receipt[
            "mission_cycle_state_digest"
        ],
        "next_plan_basis_digest": activation_receipt[
            "next_plan_basis_digest"
        ],
        "plan_bootstrap_state": plan_bootstrap,
        "lease_monitor_started_at_ms": now,
        "lease_monitor_deadline_ms": min(deadlines),
        "lease_clocks": lease_clocks,
        "activation_consumed": True,
        "session_single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "created_at_ms": now,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "plan_control_session_digest": "",
    }
    state["plan_control_session_digest"] = session_digest(state)
    errors = validate_next_cycle_plan_session(state)
    if errors:
        raise ValueError("session_state_invalid:" + ";".join(errors))
    return state


def validate_next_cycle_plan_session(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != SESSION_VERSION:
            errors.append("session_version_invalid")
        if state.get("status") != SESSION_ACTIVE:
            errors.append("session_status_invalid")
        if state.get("plan_control_session_digest") != session_digest(state):
            errors.append("session_digest_invalid")
        for field in (
            "plan_control_session_id",
            "activation_receipt_digest",
            "materialization_receipt_digest",
            "continuity_id",
            "owner_id",
            "epoch_digest",
            "scope_inventory_digest",
            "capability_state_digest",
            "lease_state_digest",
            "renewal_state_digest",
            "mission_cycle_state_digest",
            "predecessor_mission_cycle_state_digest",
            "next_plan_basis_digest",
        ):
            require_string(state.get(field), field)
        require_int(state.get("epoch_index"), "epoch_index", minimum=1)
        require_int(
            state.get("mission_cycle_index"), "mission_cycle_index", minimum=1
        )
        started = require_int(
            state.get("lease_monitor_started_at_ms"),
            "lease_monitor_started_at_ms",
        )
        deadline = require_int(
            state.get("lease_monitor_deadline_ms"),
            "lease_monitor_deadline_ms",
            minimum=1,
        )
        if deadline <= started:
            errors.append("session_lease_monitor_deadline_invalid")
        if state.get("mission_cycle_phase") != "plan":
            errors.append("session_phase_invalid")
        scopes = dict(state.get("scope_inventory", {}))
        clocks = dict(state.get("lease_clocks", {}))
        if set(scopes) != set(CAPABILITY_KINDS):
            errors.append("session_scope_inventory_invalid")
        if set(clocks) != set(CAPABILITY_KINDS):
            errors.append("session_lease_clock_inventory_invalid")
        for kind, clock in clocks.items():
            if clock.get("scope_digest") != scopes.get(kind):
                errors.append("session_scope_clock_mismatch")
            if clock.get("monitor_status") != "MONITORING":
                errors.append("session_monitor_status_invalid")
            if int(clock.get("remaining_uses", 0)) <= 0:
                errors.append("session_monitor_use_budget_invalid")
            if int(clock.get("remaining_cost_units", 0)) <= 0:
                errors.append("session_monitor_cost_budget_invalid")
            if int(clock.get("not_before_ms", 0)) > started:
                errors.append("session_monitor_started_too_early")
            if int(clock.get("expires_at_ms", 0)) <= started:
                errors.append("session_monitor_expired")
        bootstrap = dict(state.get("plan_bootstrap_state", {}))
        if bootstrap.get("plan_session_id") != state.get(
            "plan_control_session_id"
        ):
            errors.append("session_plan_id_mismatch")
        if bootstrap.get("current_phase") != PLAN_BIND:
            errors.append("session_plan_phase_invalid")
        for field in ("event_index", "plan_version", "completed_plans"):
            if bootstrap.get(field) != 0:
                errors.append(f"session_plan_{field}_not_zero")
        if bootstrap.get("steps") != [] or bootstrap.get("topological_order") != []:
            errors.append("session_plan_not_empty")
        if bootstrap.get("next_plan_basis_digest") != state.get(
            "next_plan_basis_digest"
        ):
            errors.append("session_plan_basis_mismatch")
        if bootstrap.get("plan_basis_bound") is not True:
            errors.append("session_plan_basis_not_bound")
        if bootstrap.get("source_identity_preserved") is not True:
            errors.append("session_source_identity_not_preserved")
        if bootstrap.get("execution_permission") is not False:
            errors.append("session_plan_execution_permission_invalid")
        for field, expected in {
            "activation_consumed": True,
            "session_single_use": True,
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if state.get(field) != expected:
                errors.append(f"session_{field}_invalid")
        require_int(state.get("created_at_ms"), "created_at_ms")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("session_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("session_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
