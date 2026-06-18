from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_mission_contract_kernel_v0_20 import (
    NON_AUTHORITY_FLAGS,
    sha,
    validate_mission_contract,
)

GOAL_VERSION = "kuuos_goal_proposal_v0_20"
PORTFOLIO_VERSION = "kuuos_goal_portfolio_v0_20"
GOAL_HORIZONS = frozenset({"short", "medium", "long"})


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def goal_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "goal_digest")


def portfolio_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "goal_portfolio_digest")


def _text(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name}_missing")
    return result


def _strings(value: Sequence[Any], name: str, *, allow_empty: bool = False) -> list[str]:
    result = [_text(item, name) for item in value]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _finite(value: Any, name: str, *, minimum: float = 0.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name}_not_finite")
    if result < minimum:
        raise ValueError(f"{name}_below_minimum")
    return result


def build_goal_proposal(
    *,
    contract: Mapping[str, Any],
    goal_id: str,
    objective: str,
    priority_weight: float,
    horizon: str,
    expected_outcomes: Sequence[str],
    required_capabilities: Sequence[str],
    dependencies: Sequence[str],
    requested_cost: float,
    requested_cycles: int,
    created_at_ms: int,
    exclusive_group: str = "",
) -> dict[str, Any]:
    contract_errors = validate_mission_contract(contract)
    if contract_errors:
        raise ValueError(";".join(contract_errors))
    horizon_name = _text(horizon, "horizon")
    if horizon_name not in GOAL_HORIZONS:
        raise ValueError("goal_horizon_invalid")
    weight = _finite(priority_weight, "priority_weight", minimum=0.0)
    if weight <= 0.0 or weight > 1.0:
        raise ValueError("priority_weight_out_of_range")
    cycles = int(requested_cycles)
    if cycles <= 0:
        raise ValueError("requested_cycles_not_positive")
    goal_name = _text(goal_id, "goal_id")
    dependency_ids = _strings(dependencies, "dependencies", allow_empty=True)
    if goal_name in dependency_ids:
        raise ValueError("goal_self_dependency")
    packet = {
        "version": GOAL_VERSION,
        "goal_id": goal_name,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "objective": _text(objective, "objective"),
        "priority_weight": weight,
        "horizon": horizon_name,
        "expected_outcomes": _strings(expected_outcomes, "expected_outcomes"),
        "required_capabilities": _strings(
            required_capabilities, "required_capabilities", allow_empty=True
        ),
        "dependencies": dependency_ids,
        "requested_cost": _finite(requested_cost, "requested_cost", minimum=0.0),
        "requested_cycles": cycles,
        "created_at_ms": int(created_at_ms),
        "exclusive_group": str(exclusive_group).strip(),
        "effect_authority_granted": False,
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "goal_digest": "",
    }
    packet["goal_digest"] = goal_digest(packet)
    errors = validate_goal_proposal(packet, contract)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_goal_proposal(
    goal: Mapping[str, Any], contract: Mapping[str, Any]
) -> list[str]:
    errors = validate_mission_contract(contract)
    if errors:
        return ["contract:" + item for item in errors]
    if goal.get("version") != GOAL_VERSION:
        errors.append("goal_version_invalid")
    if goal.get("mission_id") != contract.get("mission_id"):
        errors.append("goal_mission_mismatch")
    if goal.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("goal_contract_digest_mismatch")
    if not str(goal.get("goal_id", "")).strip() or not str(
        goal.get("objective", "")
    ).strip():
        errors.append("goal_identity_or_objective_missing")
    if goal.get("horizon") not in GOAL_HORIZONS:
        errors.append("goal_horizon_invalid")
    try:
        weight = _finite(goal.get("priority_weight"), "priority_weight", minimum=0.0)
        if weight <= 0.0 or weight > 1.0:
            errors.append("priority_weight_out_of_range")
        requested_cost = _finite(
            goal.get("requested_cost"), "requested_cost", minimum=0.0
        )
        if requested_cost < 0:
            errors.append("requested_cost_negative")
        if int(goal.get("requested_cycles", 0)) <= 0:
            errors.append("requested_cycles_not_positive")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    dependencies = goal.get("dependencies")
    if not isinstance(dependencies, list):
        errors.append("goal_dependencies_invalid")
    elif goal.get("goal_id") in dependencies:
        errors.append("goal_self_dependency")
    if not isinstance(goal.get("expected_outcomes"), list) or not goal.get(
        "expected_outcomes"
    ):
        errors.append("expected_outcomes_missing")
    if goal.get("effect_authority_granted") is not False:
        errors.append("goal_effect_authority_forbidden")
    if dict(goal.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("goal_non_authority_invalid")
    if goal.get("goal_digest") != goal_digest(goal):
        errors.append("goal_digest_invalid")
    return errors


def _normalized_weights(
    goals: list[Mapping[str, Any]], plurality_floor: float
) -> dict[str, float]:
    if not goals:
        return {}
    if len(goals) == 1:
        return {str(goals[0]["goal_id"]): 1.0}
    floor = min(float(plurality_floor), 1.0 / len(goals) - 1e-12)
    total = sum(float(goal["priority_weight"]) for goal in goals)
    residual = 1.0 - floor * len(goals)
    weights = {
        str(goal["goal_id"]): floor
        + residual * float(goal["priority_weight"]) / total
        for goal in goals
    }
    correction = 1.0 - sum(weights.values())
    last = sorted(weights)[-1]
    weights[last] += correction
    return weights


def build_goal_portfolio(
    *,
    contract: Mapping[str, Any],
    goals: Sequence[Mapping[str, Any]],
    now_ms: int,
    previous_portfolio: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    contract_errors = validate_mission_contract(contract)
    if contract_errors:
        raise ValueError(";".join(contract_errors))
    goal_list = [deepcopy(dict(goal)) for goal in goals]
    if len(goal_list) > int(contract["resource_envelope"]["max_goal_count"]):
        raise ValueError("goal_count_exceeds_contract")
    goal_ids = [str(goal.get("goal_id", "")) for goal in goal_list]
    if len(goal_ids) != len(set(goal_ids)):
        raise ValueError("goal_id_duplicate")
    for goal in goal_list:
        errors = validate_goal_proposal(goal, contract)
        if errors:
            raise ValueError(";".join(errors))

    goal_by_id = {str(goal["goal_id"]): goal for goal in goal_list}
    rejected: list[dict[str, Any]] = []
    held: list[dict[str, Any]] = []
    eligible: list[dict[str, Any]] = []
    residues: list[dict[str, Any]] = []
    prohibited = set(str(item) for item in contract["prohibited_outcomes"])
    scoped_capabilities = set(
        str(item)
        for item in contract["authority_scope"]["requested_capabilities"]
    )
    max_cycle_cost = float(contract["resource_envelope"]["max_cycle_cost"])
    max_cycles = int(
        contract["resource_envelope"]["max_cycles_before_renewal"]
    )

    for goal in goal_list:
        goal_id = str(goal["goal_id"])
        collision = sorted(
            set(str(item) for item in goal["expected_outcomes"]) & prohibited
        )
        if collision:
            rejected.append(
                {"goal_id": goal_id, "reason": "prohibited_outcome_collision"}
            )
            residues.append(
                {
                    "type": "prohibited_outcome_collision",
                    "goal_ids": [goal_id],
                    "details": collision,
                }
            )
            continue
        capability_gap = sorted(
            set(str(item) for item in goal["required_capabilities"])
            - scoped_capabilities
        )
        if capability_gap:
            rejected.append(
                {"goal_id": goal_id, "reason": "capability_scope_exceeded"}
            )
            residues.append(
                {
                    "type": "capability_scope_exceeded",
                    "goal_ids": [goal_id],
                    "details": capability_gap,
                }
            )
            continue
        missing_dependencies = sorted(
            dep for dep in goal["dependencies"] if dep not in goal_by_id
        )
        if missing_dependencies:
            held.append({"goal_id": goal_id, "reason": "dependency_missing"})
            residues.append(
                {
                    "type": "dependency_missing",
                    "goal_ids": [goal_id],
                    "details": missing_dependencies,
                }
            )
            continue
        if (
            float(goal["requested_cost"]) > max_cycle_cost
            or int(goal["requested_cycles"]) > max_cycles
        ):
            held.append(
                {
                    "goal_id": goal_id,
                    "reason": "resource_request_exceeds_envelope",
                }
            )
            residues.append(
                {
                    "type": "resource_request_exceeds_envelope",
                    "goal_ids": [goal_id],
                    "details": [],
                }
            )
            continue
        eligible.append(goal)

    groups: dict[str, list[dict[str, Any]]] = {}
    for goal in list(eligible):
        group = str(goal.get("exclusive_group", ""))
        if group:
            groups.setdefault(group, []).append(goal)
    for group, members in sorted(groups.items()):
        if len(members) <= 1:
            continue
        ordered_members = sorted(
            members,
            key=lambda item: (
                -float(item["priority_weight"]),
                int(item["created_at_ms"]),
                str(item["goal_id"]),
            ),
        )
        top_weight = float(ordered_members[0]["priority_weight"])
        top = [
            item
            for item in ordered_members
            if float(item["priority_weight"]) == top_weight
        ]
        if len(top) > 1 and contract["goal_policy"].get(
            "equal_exclusive_priority_requires_human"
        ):
            for item in members:
                eligible.remove(item)
                held.append(
                    {
                        "goal_id": item["goal_id"],
                        "reason": "human_arbitration_required",
                    }
                )
            residues.append(
                {
                    "type": "exclusive_goal_tie",
                    "goal_ids": sorted(str(item["goal_id"]) for item in members),
                    "details": [group],
                }
            )
        else:
            winner = ordered_members[0]
            for item in ordered_members[1:]:
                eligible.remove(item)
                held.append(
                    {
                        "goal_id": item["goal_id"],
                        "reason": "exclusive_goal_conflict",
                    }
                )
            residues.append(
                {
                    "type": "exclusive_goal_conflict",
                    "goal_ids": sorted(str(item["goal_id"]) for item in members),
                    "details": [group, str(winner["goal_id"])],
                }
            )

    ordered = sorted(
        eligible,
        key=lambda item: (
            -float(item["priority_weight"]),
            int(item["created_at_ms"]),
            str(item["goal_id"]),
        ),
    )
    max_active = int(contract["resource_envelope"]["max_active_goals"])
    active = ordered[:max_active]
    deferred = [
        {"goal_id": str(goal["goal_id"]), "reason": "active_goal_capacity"}
        for goal in ordered[max_active:]
    ]
    weights = _normalized_weights(
        ordered, float(contract["goal_policy"]["plurality_floor"])
    )
    revision = (
        int(previous_portfolio.get("revision", -1)) + 1
        if previous_portfolio
        else 0
    )
    parent_digest = (
        str(previous_portfolio.get("goal_portfolio_digest", ""))
        if previous_portfolio
        else ""
    )
    status = "ready"
    if not active and held:
        status = "human_or_dependency_blocked"
    elif not active and rejected:
        status = "rejected"
    elif deferred or held or rejected:
        status = "partial"
    portfolio = {
        "version": PORTFOLIO_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "revision": revision,
        "parent_portfolio_digest": parent_digest,
        "created_at_ms": int(now_ms),
        "status": status,
        "ordered_goal_ids": [str(goal["goal_id"]) for goal in ordered],
        "active_goal_ids": [str(goal["goal_id"]) for goal in active],
        "recommended_goal_id": str(active[0]["goal_id"]) if active else "",
        "normalized_weights": weights,
        "held_goals": sorted(held, key=lambda item: item["goal_id"]),
        "deferred_goals": sorted(deferred, key=lambda item: item["goal_id"]),
        "rejected_goals": sorted(rejected, key=lambda item: item["goal_id"]),
        "conflict_residues": residues,
        "goal_digests": {
            str(goal["goal_id"]): str(goal["goal_digest"])
            for goal in goal_list
        },
        "recommendation_grants_effect_authority": False,
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "goal_portfolio_digest": "",
    }
    portfolio["goal_portfolio_digest"] = portfolio_digest(portfolio)
    errors = validate_goal_portfolio(portfolio, contract)
    if errors:
        raise ValueError(";".join(errors))
    return portfolio


def validate_goal_portfolio(
    portfolio: Mapping[str, Any], contract: Mapping[str, Any]
) -> list[str]:
    errors = validate_mission_contract(contract)
    if errors:
        return ["contract:" + item for item in errors]
    if portfolio.get("version") != PORTFOLIO_VERSION:
        errors.append("portfolio_version_invalid")
    if portfolio.get("mission_id") != contract.get("mission_id"):
        errors.append("portfolio_mission_mismatch")
    if portfolio.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("portfolio_contract_digest_mismatch")
    ordered = portfolio.get("ordered_goal_ids")
    active = portfolio.get("active_goal_ids")
    if not isinstance(ordered, list) or len(ordered) != len(
        set(str(item) for item in ordered)
    ):
        errors.append("portfolio_order_invalid")
    if not isinstance(active, list) or len(active) != len(
        set(str(item) for item in active)
    ):
        errors.append("portfolio_active_invalid")
    elif isinstance(ordered, list) and not set(active).issubset(set(ordered)):
        errors.append("active_goals_not_ordered")
    if len(active or []) > int(contract["resource_envelope"]["max_active_goals"]):
        errors.append("active_goal_capacity_exceeded")
    weights = portfolio.get("normalized_weights")
    if not isinstance(weights, Mapping):
        errors.append("normalized_weights_invalid")
    else:
        if set(weights) != set(ordered or []):
            errors.append("normalized_weight_goal_mismatch")
        if weights and abs(
            sum(float(value) for value in weights.values()) - 1.0
        ) > 1e-9:
            errors.append("normalized_weights_not_one")
        if len(weights) > 1:
            floor = float(contract["goal_policy"]["plurality_floor"])
            if any(
                float(value) + 1e-12 < min(floor, 1.0 / len(weights))
                for value in weights.values()
            ):
                errors.append("plurality_floor_violated")
    if portfolio.get("recommendation_grants_effect_authority") is not False:
        errors.append("portfolio_effect_authority_forbidden")
    if dict(portfolio.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("portfolio_non_authority_invalid")
    if portfolio.get("goal_portfolio_digest") != portfolio_digest(portfolio):
        errors.append("goal_portfolio_digest_invalid")
    return errors
