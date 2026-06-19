from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_bounded_renewal_state_v0_11 import (
    validate_bounded_renewal_state,
)
from runtime.kuuos_plan_os_bounded_renewal_types_v0_11 import ACTIVE
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS
from runtime.kuuos_plan_os_lease_monitor_kernel_v0_16 import (
    validate_lease_monitor_tick,
)
from runtime.kuuos_plan_os_lease_monitor_types_v0_16 import (
    CONTINUE,
    REVALIDATE,
    RENEW_OR_ESCALATE,
    REROTATE_REQUIRED,
    SESSION_SUSPENDED,
)
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import (
    validate_next_cycle_plan_session,
)
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    validate_rerotation_materialization_receipt,
)
from runtime.kuuos_plan_os_suspension_recovery_types_v0_17 import (
    BOUNDARY,
    HANDOFF_VERSION,
    NON_AUTHORITY,
    RECOVERY_ROUTED,
    REVALIDATION_REQUIRED,
    TARGET_STAGES,
    V11_RENEWAL_REVIEW,
    V12_ESCALATION_REQUIRED,
    V12_REROTATION_REQUIRED,
    copy_boundary,
    copy_non_authority,
    handoff_digest,
    require_int,
    require_string,
)


def _renewal_eligible(policy: Mapping[str, Any], now_ms: int) -> bool:
    last = int(policy.get("last_renewed_at_ms", 0))
    cooldown = int(policy.get("cooldown_ms", 0))
    cooldown_ready = last == 0 or now_ms >= last + cooldown
    return (
        policy.get("status") == ACTIVE
        and int(policy.get("renewal_count", 0))
        < int(policy.get("max_renewals", 0))
        and int(policy.get("cumulative_added_uses", 0))
        < int(policy.get("max_cumulative_added_uses", 0))
        and int(policy.get("cumulative_added_cost_units", 0))
        < int(policy.get("max_cumulative_added_cost_units", 0))
        and now_ms < int(policy.get("absolute_expires_at_ms", 0))
        and cooldown_ready
    )


def build_suspension_recovery_handoff(
    *,
    session: Mapping[str, Any],
    suspension_tick: Mapping[str, Any],
    materialization_receipt: Mapping[str, Any],
    recovery_authority_id: str,
    recovery_authority_receipt_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    session_errors = validate_next_cycle_plan_session(session)
    if session_errors:
        raise ValueError("recovery_session_invalid:" + ";".join(session_errors))
    tick_errors = validate_lease_monitor_tick(suspension_tick)
    if tick_errors:
        raise ValueError("recovery_tick_invalid:" + ";".join(tick_errors))
    materialization_errors = validate_rerotation_materialization_receipt(
        materialization_receipt
    )
    if materialization_errors:
        raise ValueError(
            "recovery_materialization_invalid:"
            + ";".join(materialization_errors)
        )
    if suspension_tick.get("session_status_after") != SESSION_SUSPENDED:
        raise ValueError("recovery_terminal_suspension_required")
    if suspension_tick.get("session_suspended") is not True:
        raise ValueError("recovery_suspension_flag_required")
    if suspension_tick.get("suspension_terminal") is not True:
        raise ValueError("recovery_terminal_flag_required")
    route = require_string(suspension_tick.get("recovery_route"), "recovery_route")
    if route == CONTINUE:
        raise ValueError("recovery_continue_route_forbidden")
    if suspension_tick.get("source_session_digest") != session.get(
        "plan_control_session_digest"
    ):
        raise ValueError("recovery_source_session_mismatch")
    for field in (
        "plan_control_session_id",
        "owner_id",
        "epoch_index",
        "epoch_digest",
        "mission_cycle_index",
        "mission_cycle_phase",
    ):
        if suspension_tick.get(field) != session.get(field):
            raise ValueError(f"recovery_tick_{field}_mismatch")
    if session.get("materialization_receipt_digest") != materialization_receipt.get(
        "rerotation_materialization_receipt_digest"
    ):
        raise ValueError("recovery_materialization_digest_mismatch")
    if session.get("owner_id") != materialization_receipt.get("current_owner_id"):
        raise ValueError("recovery_materialization_owner_mismatch")
    if session.get("epoch_digest") != materialization_receipt.get(
        "current_epoch_digest"
    ):
        raise ValueError("recovery_materialization_epoch_mismatch")
    renewal_state = dict(materialization_receipt.get("renewal_state", {}))
    renewal_errors = validate_bounded_renewal_state(renewal_state)
    if renewal_errors:
        raise ValueError("recovery_renewal_state_invalid:" + ";".join(renewal_errors))
    if session.get("renewal_state_digest") != renewal_state.get(
        "bounded_renewal_state_digest"
    ):
        raise ValueError("recovery_renewal_state_digest_mismatch")
    if session.get("lease_state_digest") != renewal_state.get(
        "current_lease_state", {}
    ).get("capability_lease_state_digest"):
        raise ValueError("recovery_lease_state_digest_mismatch")

    reasons_by_kind: dict[str, list[str]] = {}
    for kind in CAPABILITY_KINDS:
        reasons = list(suspension_tick.get("per_kind", {}).get(kind, {}).get("reasons", []))
        if reasons:
            reasons_by_kind[kind] = reasons
    affected = sorted(reasons_by_kind)
    if not affected:
        raise ValueError("recovery_suspension_reason_required")
    reason_inventory_digest = sha(reasons_by_kind)
    candidates: list[str] = []
    escalations: list[str] = []
    revalidation_digest = ""
    rerotation_required = False

    if route == REVALIDATE:
        target = REVALIDATION_REQUIRED
        revalidation_digest = require_string(
            suspension_tick.get("observation_digest"), "observation_digest"
        )
    elif route == RENEW_OR_ESCALATE:
        policies = dict(renewal_state.get("policies", {}))
        for kind in affected:
            if _renewal_eligible(dict(policies[kind]), int(suspension_tick["tick_at_ms"])):
                candidates.append(kind)
            else:
                escalations.append(kind)
        target = (
            V12_ESCALATION_REQUIRED
            if escalations
            else V11_RENEWAL_REVIEW
        )
    elif route == REROTATE_REQUIRED:
        target = V12_REROTATION_REQUIRED
        rerotation_required = True
    else:
        raise ValueError("recovery_route_unknown")

    routed_at = require_int(now_ms, "now_ms")
    if routed_at < int(suspension_tick["tick_at_ms"]):
        raise ValueError("recovery_time_precedes_suspension")
    root = {
        "session_digest": session["plan_control_session_digest"],
        "tick_digest": suspension_tick["lease_monitor_tick_digest"],
        "materialization_digest": materialization_receipt[
            "rerotation_materialization_receipt_digest"
        ],
        "route": route,
        "target": target,
        "reason_inventory_digest": reason_inventory_digest,
        "authority_receipt": recovery_authority_receipt_digest,
    }
    handoff = {
        "version": HANDOFF_VERSION,
        "status": RECOVERY_ROUTED,
        "recovery_id": "suspension-recovery:" + sha(root),
        "source_session_digest": session["plan_control_session_digest"],
        "source_session_id": session["plan_control_session_id"],
        "source_tick_digest": suspension_tick["lease_monitor_tick_digest"],
        "source_materialization_receipt_digest": materialization_receipt[
            "rerotation_materialization_receipt_digest"
        ],
        "current_bounded_renewal_state_digest": renewal_state[
            "bounded_renewal_state_digest"
        ],
        "current_lease_state_digest": renewal_state["current_lease_state"][
            "capability_lease_state_digest"
        ],
        "continuity_id": session["continuity_id"],
        "owner_id": session["owner_id"],
        "epoch_index": session["epoch_index"],
        "epoch_digest": session["epoch_digest"],
        "mission_cycle_index": session["mission_cycle_index"],
        "suspension_tick_index": suspension_tick["tick_index"],
        "suspended_at_ms": suspension_tick["tick_at_ms"],
        "recovery_route": route,
        "target_stage": target,
        "affected_kinds": affected,
        "reason_inventory": reasons_by_kind,
        "reason_inventory_digest": reason_inventory_digest,
        "renewal_candidate_kinds": candidates,
        "escalation_required_kinds": escalations,
        "revalidation_observation_digest": revalidation_digest,
        "rerotation_required": rerotation_required,
        "old_session_status": SESSION_SUSPENDED,
        "old_session_closed": True,
        "old_session_resume_allowed": False,
        "new_lineage_required": True,
        "new_activation_required": True,
        "new_session_required": True,
        "recovery_authority_id": require_string(
            recovery_authority_id, "recovery_authority_id"
        ),
        "recovery_authority_receipt_digest": require_string(
            recovery_authority_receipt_digest,
            "recovery_authority_receipt_digest",
        ),
        "routed_at_ms": routed_at,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "suspension_recovery_handoff_digest": "",
    }
    handoff["suspension_recovery_handoff_digest"] = handoff_digest(handoff)
    errors = validate_suspension_recovery_handoff(handoff)
    if errors:
        raise ValueError("recovery_handoff_invalid:" + ";".join(errors))
    return handoff


def validate_suspension_recovery_handoff(
    handoff: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if handoff.get("version") != HANDOFF_VERSION:
            errors.append("recovery_handoff_version_invalid")
        if handoff.get("status") != RECOVERY_ROUTED:
            errors.append("recovery_handoff_status_invalid")
        if handoff.get("suspension_recovery_handoff_digest") != handoff_digest(
            handoff
        ):
            errors.append("recovery_handoff_digest_invalid")
        for field in (
            "recovery_id",
            "source_session_digest",
            "source_session_id",
            "source_tick_digest",
            "source_materialization_receipt_digest",
            "current_bounded_renewal_state_digest",
            "current_lease_state_digest",
            "continuity_id",
            "owner_id",
            "epoch_digest",
            "recovery_route",
            "target_stage",
            "reason_inventory_digest",
            "old_session_status",
            "recovery_authority_id",
            "recovery_authority_receipt_digest",
        ):
            require_string(handoff.get(field), field)
        require_int(handoff.get("epoch_index"), "epoch_index", minimum=1)
        require_int(
            handoff.get("mission_cycle_index"), "mission_cycle_index", minimum=1
        )
        require_int(
            handoff.get("suspension_tick_index"),
            "suspension_tick_index",
            minimum=1,
        )
        require_int(handoff.get("suspended_at_ms"), "suspended_at_ms")
        require_int(handoff.get("routed_at_ms"), "routed_at_ms")
        target = handoff.get("target_stage")
        if target not in TARGET_STAGES:
            errors.append("recovery_target_stage_invalid")
        affected = list(handoff.get("affected_kinds", []))
        if not affected or len(affected) != len(set(affected)):
            errors.append("recovery_affected_kinds_invalid")
        if not set(affected).issubset(set(CAPABILITY_KINDS)):
            errors.append("recovery_affected_kind_unknown")
        reasons = dict(handoff.get("reason_inventory", {}))
        if set(reasons) != set(affected):
            errors.append("recovery_reason_inventory_invalid")
        if handoff.get("reason_inventory_digest") != sha(reasons):
            errors.append("recovery_reason_inventory_digest_invalid")
        candidates = list(handoff.get("renewal_candidate_kinds", []))
        escalations = list(handoff.get("escalation_required_kinds", []))
        if set(candidates).intersection(escalations):
            errors.append("recovery_kind_classification_overlap")
        route = handoff.get("recovery_route")
        if route == REVALIDATE:
            if target != REVALIDATION_REQUIRED:
                errors.append("recovery_revalidation_target_invalid")
            require_string(
                handoff.get("revalidation_observation_digest"),
                "revalidation_observation_digest",
            )
            if candidates or escalations or handoff.get("rerotation_required") is not False:
                errors.append("recovery_revalidation_payload_invalid")
        elif route == RENEW_OR_ESCALATE:
            if set(candidates).union(escalations) != set(affected):
                errors.append("recovery_renewal_classification_incomplete")
            expected_target = (
                V12_ESCALATION_REQUIRED if escalations else V11_RENEWAL_REVIEW
            )
            if target != expected_target:
                errors.append("recovery_renewal_target_invalid")
            if handoff.get("revalidation_observation_digest") != "":
                errors.append("recovery_renewal_revalidation_digest_forbidden")
            if handoff.get("rerotation_required") is not False:
                errors.append("recovery_renewal_rerotation_flag_invalid")
        elif route == REROTATE_REQUIRED:
            if target != V12_REROTATION_REQUIRED:
                errors.append("recovery_rerotation_target_invalid")
            if handoff.get("rerotation_required") is not True:
                errors.append("recovery_rerotation_flag_invalid")
            if candidates or escalations:
                errors.append("recovery_rerotation_renewal_payload_forbidden")
            if handoff.get("revalidation_observation_digest") != "":
                errors.append("recovery_rerotation_revalidation_digest_forbidden")
        else:
            errors.append("recovery_route_invalid")
        for field, expected in {
            "old_session_status": SESSION_SUSPENDED,
            "old_session_closed": True,
            "old_session_resume_allowed": False,
            "new_lineage_required": True,
            "new_activation_required": True,
            "new_session_required": True,
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if handoff.get(field) != expected:
                errors.append(f"recovery_{field}_invalid")
        if dict(handoff.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("recovery_non_authority_invalid")
        if dict(handoff.get("boundary", {})) != BOUNDARY:
            errors.append("recovery_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
