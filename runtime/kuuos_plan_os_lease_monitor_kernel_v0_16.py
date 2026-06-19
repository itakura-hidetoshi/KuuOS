from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import (
    validate_next_cycle_plan_session,
)
from runtime.kuuos_plan_os_next_cycle_session_types_v0_15 import SESSION_ACTIVE
from runtime.kuuos_plan_os_lease_monitor_types_v0_16 import (
    BOUNDARY,
    CONTINUE,
    COST_BUDGET_EMPTY,
    COST_BUDGET_INCREASE,
    EPOCH_MISMATCH,
    EXPIRED,
    LEASE_WINDOW_MISMATCH,
    NON_AUTHORITY,
    OBSERVATION_TIME_MISMATCH,
    OWNER_MISMATCH,
    REVALIDATE,
    RENEW_OR_ESCALATE,
    REROTATE_REQUIRED,
    SCOPE_MISMATCH,
    SESSION_HEALTHY,
    SESSION_SUSPENDED,
    SUSPENSION_REASONS,
    TICK_VERSION,
    USE_BUDGET_EMPTY,
    USE_BUDGET_INCREASE,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    tick_digest,
)


def _route_for(reasons: list[str]) -> str:
    reason_set = set(reasons)
    if reason_set.intersection({OWNER_MISMATCH, EPOCH_MISMATCH, SCOPE_MISMATCH}):
        return REROTATE_REQUIRED
    if reason_set.intersection(
        {
            LEASE_WINDOW_MISMATCH,
            USE_BUDGET_INCREASE,
            COST_BUDGET_INCREASE,
            OBSERVATION_TIME_MISMATCH,
        }
    ):
        return REVALIDATE
    if reason_set:
        return RENEW_OR_ESCALATE
    return CONTINUE


def build_lease_monitor_tick(
    *,
    session: Mapping[str, Any],
    observed_leases: Mapping[str, Mapping[str, Any]],
    tick_index: int,
    now_ms: int,
) -> dict[str, Any]:
    session_errors = validate_next_cycle_plan_session(session)
    if session_errors:
        raise ValueError("monitor_session_invalid:" + ";".join(session_errors))
    if session.get("status") != SESSION_ACTIVE:
        raise ValueError("monitor_session_not_active")
    if set(observed_leases) != set(CAPABILITY_KINDS):
        raise ValueError("monitor_observation_inventory_incomplete")
    now = require_int(now_ms, "now_ms")
    index = require_int(tick_index, "tick_index", minimum=1)
    clocks = dict(session["lease_clocks"])
    scopes = dict(session["scope_inventory"])
    owner = require_string(session["owner_id"], "owner_id")
    epoch = require_string(session["epoch_digest"], "epoch_digest")
    per_kind: dict[str, dict[str, Any]] = {}
    all_reasons: list[str] = []
    normalized_observations: dict[str, dict[str, Any]] = {}
    for kind in CAPABILITY_KINDS:
        observation = dict(observed_leases[kind])
        clock = dict(clocks[kind])
        observed_at = require_int(
            observation.get("observed_at_ms"), "observed_at_ms"
        )
        expires = require_int(
            observation.get("expires_at_ms"), "expires_at_ms", minimum=1
        )
        uses = require_int(
            observation.get("remaining_uses"), "remaining_uses"
        )
        cost = require_int(
            observation.get("remaining_cost_units"),
            "remaining_cost_units",
        )
        observed_owner = require_string(
            observation.get("owner_id"), "observed_owner_id"
        )
        observed_epoch = require_string(
            observation.get("epoch_digest"), "observed_epoch_digest"
        )
        observed_scope = require_string(
            observation.get("scope_digest"), "observed_scope_digest"
        )
        reasons: list[str] = []
        if observed_at != now:
            reasons.append(OBSERVATION_TIME_MISMATCH)
        if observed_owner != owner:
            reasons.append(OWNER_MISMATCH)
        if observed_epoch != epoch:
            reasons.append(EPOCH_MISMATCH)
        if observed_scope != scopes[kind]:
            reasons.append(SCOPE_MISMATCH)
        if expires != int(clock["expires_at_ms"]):
            reasons.append(LEASE_WINDOW_MISMATCH)
        if now >= expires:
            reasons.append(EXPIRED)
        if uses == 0:
            reasons.append(USE_BUDGET_EMPTY)
        if cost == 0:
            reasons.append(COST_BUDGET_EMPTY)
        if uses > int(clock["remaining_uses"]):
            reasons.append(USE_BUDGET_INCREASE)
        if cost > int(clock["remaining_cost_units"]):
            reasons.append(COST_BUDGET_INCREASE)
        normalized_observations[kind] = {
            "owner_id": observed_owner,
            "epoch_digest": observed_epoch,
            "scope_digest": observed_scope,
            "expires_at_ms": expires,
            "remaining_uses": uses,
            "remaining_cost_units": cost,
            "observed_at_ms": observed_at,
        }
        per_kind[kind] = {
            "healthy": not reasons,
            "reasons": reasons,
            "route": _route_for(reasons),
        }
        all_reasons.extend(f"{kind}:{reason}" for reason in reasons)
    suspended = bool(all_reasons)
    status = SESSION_SUSPENDED if suspended else SESSION_HEALTHY
    routes = [item["route"] for item in per_kind.values()]
    if REROTATE_REQUIRED in routes:
        route = REROTATE_REQUIRED
    elif REVALIDATE in routes:
        route = REVALIDATE
    elif RENEW_OR_ESCALATE in routes:
        route = RENEW_OR_ESCALATE
    else:
        route = CONTINUE
    observation_digest = sha(normalized_observations)
    tick = {
        "version": TICK_VERSION,
        "source_session_digest": session["plan_control_session_digest"],
        "plan_control_session_id": session["plan_control_session_id"],
        "owner_id": owner,
        "epoch_index": session["epoch_index"],
        "epoch_digest": epoch,
        "mission_cycle_index": session["mission_cycle_index"],
        "mission_cycle_phase": session["mission_cycle_phase"],
        "tick_index": index,
        "tick_at_ms": now,
        "observed_leases": normalized_observations,
        "observation_digest": observation_digest,
        "per_kind": per_kind,
        "session_status_after": status,
        "suspension_reasons": all_reasons,
        "recovery_route": route,
        "plan_progress_allowed": not suspended,
        "session_suspended": suspended,
        "suspension_terminal": suspended,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "lease_monitor_tick_digest": "",
    }
    tick["lease_monitor_tick_digest"] = tick_digest(tick)
    errors = validate_lease_monitor_tick(tick)
    if errors:
        raise ValueError("monitor_tick_invalid:" + ";".join(errors))
    return tick


def validate_lease_monitor_tick(tick: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if tick.get("version") != TICK_VERSION:
            errors.append("monitor_tick_version_invalid")
        if tick.get("lease_monitor_tick_digest") != tick_digest(tick):
            errors.append("monitor_tick_digest_invalid")
        for field in (
            "source_session_digest",
            "plan_control_session_id",
            "owner_id",
            "epoch_digest",
            "mission_cycle_phase",
            "observation_digest",
            "session_status_after",
            "recovery_route",
        ):
            require_string(tick.get(field), field)
        require_int(tick.get("epoch_index"), "epoch_index", minimum=1)
        require_int(
            tick.get("mission_cycle_index"), "mission_cycle_index", minimum=1
        )
        require_int(tick.get("tick_index"), "tick_index", minimum=1)
        require_int(tick.get("tick_at_ms"), "tick_at_ms")
        observations = dict(tick.get("observed_leases", {}))
        per_kind = dict(tick.get("per_kind", {}))
        if set(observations) != set(CAPABILITY_KINDS):
            errors.append("monitor_tick_observation_inventory_invalid")
        if set(per_kind) != set(CAPABILITY_KINDS):
            errors.append("monitor_tick_result_inventory_invalid")
        if tick.get("observation_digest") != sha(observations):
            errors.append("monitor_tick_observation_digest_invalid")
        reasons = list(tick.get("suspension_reasons", []))
        for item in reasons:
            if not isinstance(item, str) or ":" not in item:
                errors.append("monitor_tick_reason_invalid")
                continue
            reason = item.split(":", 1)[1]
            if reason not in SUSPENSION_REASONS:
                errors.append("monitor_tick_reason_unknown")
        suspended = bool(reasons)
        expected_status = SESSION_SUSPENDED if suspended else SESSION_HEALTHY
        if tick.get("session_status_after") != expected_status:
            errors.append("monitor_tick_status_invalid")
        if tick.get("session_suspended") is not suspended:
            errors.append("monitor_tick_suspended_flag_invalid")
        if tick.get("plan_progress_allowed") is not (not suspended):
            errors.append("monitor_tick_plan_progress_invalid")
        if tick.get("suspension_terminal") is not suspended:
            errors.append("monitor_tick_terminal_flag_invalid")
        if tick.get("recovery_route") not in {
            CONTINUE,
            REVALIDATE,
            RENEW_OR_ESCALATE,
            REROTATE_REQUIRED,
        }:
            errors.append("monitor_tick_route_invalid")
        for field in (
            "execution_granted",
            "host_license_granted",
            "memory_overwrite",
        ):
            if tick.get(field) is not False:
                errors.append(f"monitor_tick_{field}_invalid")
        if dict(tick.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("monitor_tick_non_authority_invalid")
        if dict(tick.get("boundary", {})) != BOUNDARY:
            errors.append("monitor_tick_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
