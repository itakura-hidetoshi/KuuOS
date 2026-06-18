from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

VERSION = "kuuos_mission_contract_kernel_v0_20"
CONTRACT_VERSION = "kuuos_mission_contract_v0_20"
STATE_VERSION = "kuuos_mission_state_v0_20"
COMMAND_VERSION = "kuuos_mission_command_v0_20"
EVIDENCE_VERSION = "kuuos_mission_evidence_v0_20"
DECISION_VERSION = "kuuos_mission_lifecycle_decision_v0_20"
APPLY_RESULT_VERSION = "kuuos_mission_decision_apply_result_v0_20"

MISSION_STATES = frozenset(
    {
        "proposed",
        "active",
        "paused",
        "renewal_required",
        "completed",
        "terminated",
        "handed_over",
    }
)
TERMINAL_STATES = frozenset({"completed", "terminated", "handed_over"})
MISSION_COMMANDS = frozenset(
    {
        "pause",
        "resume",
        "terminate",
        "handover",
        "request_renewal",
        "renew",
    }
)
DECISION_CLASSES = frozenset(
    {
        "continue",
        "pause",
        "resume",
        "renewal_required",
        "complete",
        "terminate",
        "handover",
        "no_change",
    }
)
EVIDENCE_LEVELS = frozenset({"observation", "authorized_verification", "human_attestation"})

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "mission_persistence_is_not_execution_license": True,
    "goal_priority_is_not_effect_authority": True,
    "success_evidence_requires_authorized_source": True,
    "renewal_requires_explicit_authorization": True,
    "resource_envelope_is_finite": True,
    "mission_revision_is_append_only": True,
    "state_transition_is_replay_safe": True,
    "lower_execution_authority_preserved": True,
    "foreground_user_control_preserved": True,
    "graph_semantics_forbidden": True,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def contract_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_contract_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_state_digest")


def command_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_command_digest")


def evidence_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_evidence_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_decision_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "apply_result_digest")


def _require_nonempty_string(value: Any, name: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{name}_missing")
    return text


def _require_unique_strings(value: Sequence[Any], name: str, *, allow_empty: bool = False) -> list[str]:
    result = [_require_nonempty_string(item, name) for item in value]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _require_finite_number(value: Any, name: str, *, minimum: float | None = None) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name}_not_finite")
    if minimum is not None and number < minimum:
        raise ValueError(f"{name}_below_minimum")
    return number


def _require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if number < 0:
        raise ValueError(f"{name}_negative")
    return number


def _require_positive_int(value: Any, name: str) -> int:
    number = _require_nonnegative_int(value, name)
    if number <= 0:
        raise ValueError(f"{name}_not_positive")
    return number


def build_resource_envelope(
    *,
    max_total_cost: float,
    max_cycle_cost: float,
    max_cycles_before_renewal: int,
    max_active_goals: int,
    max_goal_count: int,
    reserve_floor: float = 0.0,
    cost_unit: str = "cost_units",
) -> dict[str, Any]:
    envelope = {
        "max_total_cost": _require_finite_number(max_total_cost, "max_total_cost", minimum=0.0),
        "max_cycle_cost": _require_finite_number(max_cycle_cost, "max_cycle_cost", minimum=0.0),
        "max_cycles_before_renewal": _require_positive_int(
            max_cycles_before_renewal, "max_cycles_before_renewal"
        ),
        "max_active_goals": _require_positive_int(max_active_goals, "max_active_goals"),
        "max_goal_count": _require_positive_int(max_goal_count, "max_goal_count"),
        "reserve_floor": _require_finite_number(reserve_floor, "reserve_floor", minimum=0.0),
        "cost_unit": _require_nonempty_string(cost_unit, "cost_unit"),
    }
    errors = validate_resource_envelope(envelope)
    if errors:
        raise ValueError(";".join(errors))
    return envelope


def validate_resource_envelope(envelope: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        max_total_cost = _require_finite_number(
            envelope.get("max_total_cost"), "max_total_cost", minimum=0.0
        )
        max_cycle_cost = _require_finite_number(
            envelope.get("max_cycle_cost"), "max_cycle_cost", minimum=0.0
        )
        reserve_floor = _require_finite_number(
            envelope.get("reserve_floor"), "reserve_floor", minimum=0.0
        )
        max_cycles = _require_positive_int(
            envelope.get("max_cycles_before_renewal"), "max_cycles_before_renewal"
        )
        max_active = _require_positive_int(
            envelope.get("max_active_goals"), "max_active_goals"
        )
        max_goals = _require_positive_int(envelope.get("max_goal_count"), "max_goal_count")
        _require_nonempty_string(envelope.get("cost_unit"), "cost_unit")
        if max_total_cost <= 0.0:
            errors.append("max_total_cost_not_positive")
        if max_cycle_cost <= 0.0:
            errors.append("max_cycle_cost_not_positive")
        if max_cycle_cost > max_total_cost:
            errors.append("max_cycle_cost_exceeds_total")
        if reserve_floor >= max_total_cost:
            errors.append("reserve_floor_not_below_total")
        if max_active > max_goals:
            errors.append("max_active_goals_exceeds_goal_count")
        if max_cycles <= 0:
            errors.append("max_cycles_before_renewal_not_positive")
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def build_goal_policy(*, plurality_floor: float = 0.05) -> dict[str, Any]:
    policy = {
        "plurality_floor": _require_finite_number(
            plurality_floor, "plurality_floor", minimum=0.0
        ),
        "winner_take_all_forbidden": True,
        "equal_exclusive_priority_requires_human": True,
        "recommendation_grants_effect_authority": False,
    }
    if policy["plurality_floor"] >= 1.0:
        raise ValueError("plurality_floor_not_below_one")
    return policy


def build_renewal_policy(
    *,
    max_renewals: int,
    renewal_window_ms: int,
    authorized_roles: Sequence[str],
    allow_resource_increase: bool = False,
) -> dict[str, Any]:
    return {
        "max_renewals": _require_nonnegative_int(max_renewals, "max_renewals"),
        "renewal_window_ms": _require_positive_int(renewal_window_ms, "renewal_window_ms"),
        "authorized_roles": _require_unique_strings(authorized_roles, "authorized_roles"),
        "requires_explicit_authorization": True,
        "allow_resource_increase": bool(allow_resource_increase),
    }


def build_evidence_policy(
    *,
    completion_roles: Sequence[str],
    failure_roles: Sequence[str],
    invariant_roles: Sequence[str],
    minimum_confidence: float = 0.8,
) -> dict[str, Any]:
    confidence = _require_finite_number(
        minimum_confidence, "minimum_confidence", minimum=0.0
    )
    if confidence > 1.0:
        raise ValueError("minimum_confidence_above_one")
    return {
        "completion_roles": _require_unique_strings(completion_roles, "completion_roles"),
        "failure_roles": _require_unique_strings(failure_roles, "failure_roles"),
        "invariant_roles": _require_unique_strings(invariant_roles, "invariant_roles"),
        "minimum_confidence": confidence,
        "authorized_evidence_levels": ["authorized_verification", "human_attestation"],
    }


def build_override_policy(role_commands: Mapping[str, Sequence[str]]) -> dict[str, Any]:
    normalized: dict[str, list[str]] = {}
    if not role_commands:
        raise ValueError("override_policy_missing")
    for role, commands in sorted(role_commands.items()):
        normalized_role = _require_nonempty_string(role, "override_role")
        normalized_commands = _require_unique_strings(commands, "override_commands")
        unknown = sorted(set(normalized_commands) - set(MISSION_COMMANDS))
        if unknown:
            raise ValueError("override_command_unknown:" + ",".join(unknown))
        normalized[normalized_role] = sorted(normalized_commands)
    return {
        "role_commands": normalized,
        "command_requires_reason": True,
        "command_requires_source_state_digest": True,
    }


def build_authority_scope(
    *,
    domain_scope: Sequence[str],
    requested_capabilities: Sequence[str],
) -> dict[str, Any]:
    return {
        "domain_scope": _require_unique_strings(domain_scope, "domain_scope"),
        "requested_capabilities": _require_unique_strings(
            requested_capabilities, "requested_capabilities", allow_empty=True
        ),
        "execution_authority_granted": False,
        "tool_authority_granted": False,
        "network_authority_granted": False,
        "shell_authority_granted": False,
        "clinical_authority_granted": False,
        "theorem_authority_granted": False,
        "self_modification_authority_granted": False,
    }


def build_mission_contract(
    *,
    mission_id: str,
    lineage_id: str,
    revision: int,
    parent_contract_digest: str,
    issuer_id: str,
    issuer_role: str,
    governance_root_digest: str,
    purpose: str,
    success_criteria: Sequence[str],
    failure_criteria: Sequence[str],
    invariants: Sequence[str],
    prohibited_outcomes: Sequence[str],
    resource_envelope: Mapping[str, Any],
    authority_scope: Mapping[str, Any],
    renewal_policy: Mapping[str, Any],
    override_policy: Mapping[str, Any],
    evidence_policy: Mapping[str, Any],
    goal_policy: Mapping[str, Any],
    created_at_ms: int,
    valid_from_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    contract = {
        "version": CONTRACT_VERSION,
        "mission_id": _require_nonempty_string(mission_id, "mission_id"),
        "lineage_id": _require_nonempty_string(lineage_id, "lineage_id"),
        "revision": _require_nonnegative_int(revision, "revision"),
        "parent_contract_digest": str(parent_contract_digest),
        "issuer_id": _require_nonempty_string(issuer_id, "issuer_id"),
        "issuer_role": _require_nonempty_string(issuer_role, "issuer_role"),
        "governance_root_digest": _require_nonempty_string(
            governance_root_digest, "governance_root_digest"
        ),
        "purpose": _require_nonempty_string(purpose, "purpose"),
        "success_criteria": _require_unique_strings(success_criteria, "success_criteria"),
        "failure_criteria": _require_unique_strings(failure_criteria, "failure_criteria"),
        "invariants": _require_unique_strings(invariants, "invariants"),
        "prohibited_outcomes": _require_unique_strings(
            prohibited_outcomes, "prohibited_outcomes"
        ),
        "resource_envelope": deepcopy(dict(resource_envelope)),
        "authority_scope": deepcopy(dict(authority_scope)),
        "renewal_policy": deepcopy(dict(renewal_policy)),
        "override_policy": deepcopy(dict(override_policy)),
        "evidence_policy": deepcopy(dict(evidence_policy)),
        "goal_policy": deepcopy(dict(goal_policy)),
        "created_at_ms": _require_nonnegative_int(created_at_ms, "created_at_ms"),
        "valid_from_ms": _require_nonnegative_int(valid_from_ms, "valid_from_ms"),
        "expires_at_ms": _require_nonnegative_int(expires_at_ms, "expires_at_ms"),
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "mission_contract_digest": "",
    }
    contract["mission_contract_digest"] = contract_digest(contract)
    errors = validate_mission_contract(contract)
    if errors:
        raise ValueError(";".join(errors))
    return contract


def validate_mission_contract(contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if contract.get("version") != CONTRACT_VERSION:
        errors.append("contract_version_invalid")
    for field in (
        "mission_id",
        "lineage_id",
        "issuer_id",
        "issuer_role",
        "governance_root_digest",
        "purpose",
    ):
        if not str(contract.get(field, "")).strip():
            errors.append(f"{field}_missing")
    try:
        revision = _require_nonnegative_int(contract.get("revision"), "revision")
        parent = str(contract.get("parent_contract_digest", ""))
        if revision == 0 and parent:
            errors.append("initial_contract_has_parent")
        if revision > 0 and not parent:
            errors.append("successor_contract_parent_missing")
        created = _require_nonnegative_int(contract.get("created_at_ms"), "created_at_ms")
        valid_from = _require_nonnegative_int(contract.get("valid_from_ms"), "valid_from_ms")
        expires = _require_nonnegative_int(contract.get("expires_at_ms"), "expires_at_ms")
        if created > valid_from:
            errors.append("contract_created_after_valid_from")
        if valid_from >= expires:
            errors.append("contract_validity_window_invalid")
    except ValueError as exc:
        errors.append(str(exc))
    for field in (
        "success_criteria",
        "failure_criteria",
        "invariants",
        "prohibited_outcomes",
    ):
        values = contract.get(field)
        if not isinstance(values, list) or not values:
            errors.append(f"{field}_missing")
        elif len(values) != len(set(str(item) for item in values)):
            errors.append(f"{field}_duplicate")
    resource_errors = validate_resource_envelope(
        contract.get("resource_envelope", {})
        if isinstance(contract.get("resource_envelope"), Mapping)
        else {}
    )
    errors.extend("resource_envelope:" + item for item in resource_errors)
    authority = contract.get("authority_scope")
    if not isinstance(authority, Mapping):
        errors.append("authority_scope_missing")
    else:
        if not authority.get("domain_scope"):
            errors.append("authority_domain_scope_missing")
        for flag in (
            "execution_authority_granted",
            "tool_authority_granted",
            "network_authority_granted",
            "shell_authority_granted",
            "clinical_authority_granted",
            "theorem_authority_granted",
            "self_modification_authority_granted",
        ):
            if authority.get(flag) is not False:
                errors.append(f"authority_scope_forbidden:{flag}")
    renewal = contract.get("renewal_policy")
    if not isinstance(renewal, Mapping):
        errors.append("renewal_policy_missing")
    else:
        try:
            _require_nonnegative_int(renewal.get("max_renewals"), "max_renewals")
            _require_positive_int(
                renewal.get("renewal_window_ms"), "renewal_window_ms"
            )
        except ValueError as exc:
            errors.append(str(exc))
        if renewal.get("requires_explicit_authorization") is not True:
            errors.append("renewal_not_explicit")
        if not renewal.get("authorized_roles"):
            errors.append("renewal_authorized_roles_missing")
    override = contract.get("override_policy")
    if not isinstance(override, Mapping) or not isinstance(
        override.get("role_commands"), Mapping
    ):
        errors.append("override_policy_missing")
    else:
        for role, commands in override.get("role_commands", {}).items():
            if not str(role).strip() or not isinstance(commands, list) or not commands:
                errors.append("override_policy_invalid")
                continue
            unknown = set(str(item) for item in commands) - set(MISSION_COMMANDS)
            if unknown:
                errors.append("override_policy_unknown_command")
    evidence_policy = contract.get("evidence_policy")
    if not isinstance(evidence_policy, Mapping):
        errors.append("evidence_policy_missing")
    else:
        for field in ("completion_roles", "failure_roles", "invariant_roles"):
            if not evidence_policy.get(field):
                errors.append(f"evidence_policy_{field}_missing")
        try:
            confidence = _require_finite_number(
                evidence_policy.get("minimum_confidence"),
                "minimum_confidence",
                minimum=0.0,
            )
            if confidence > 1.0:
                errors.append("minimum_confidence_above_one")
        except ValueError as exc:
            errors.append(str(exc))
        levels = set(
            str(item) for item in evidence_policy.get("authorized_evidence_levels", [])
        )
        if not levels or not levels.issubset(EVIDENCE_LEVELS):
            errors.append("authorized_evidence_levels_invalid")
    goal_policy = contract.get("goal_policy")
    if not isinstance(goal_policy, Mapping):
        errors.append("goal_policy_missing")
    else:
        try:
            floor = _require_finite_number(
                goal_policy.get("plurality_floor"), "plurality_floor", minimum=0.0
            )
            if floor >= 1.0:
                errors.append("plurality_floor_not_below_one")
        except ValueError as exc:
            errors.append(str(exc))
        if goal_policy.get("winner_take_all_forbidden") is not True:
            errors.append("winner_take_all_not_forbidden")
        if goal_policy.get("recommendation_grants_effect_authority") is not False:
            errors.append("goal_recommendation_authority_forbidden")
    if dict(contract.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("contract_non_authority_invalid")
    if dict(contract.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("contract_boundary_invalid")
    if contract.get("mission_contract_digest") != contract_digest(contract):
        errors.append("mission_contract_digest_invalid")
    return errors
