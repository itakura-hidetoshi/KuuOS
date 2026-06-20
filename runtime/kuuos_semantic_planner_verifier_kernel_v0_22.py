from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_goal_portfolio_v0_20 import (
    validate_goal_portfolio,
    validate_goal_proposal,
)
from runtime.kuuos_mission_contract_types_v0_20 import (
    sha,
    validate_mission_contract,
)
from runtime.kuuos_mission_state_v0_20 import (
    build_mission_evidence,
    validate_mission_state,
)
from runtime.kuuos_observation_belief_state_kernel_v0_21 import (
    validate_belief_state,
    validate_observation,
)

VERSION = "kuuos_semantic_planner_verifier_kernel_v0_22"
PLAN_VERSION = "kuuos_semantic_plan_v0_22"
STEP_VERSION = "kuuos_semantic_plan_step_v0_22"
VERIFICATION_VERSION = "kuuos_outcome_verification_receipt_v0_22"
INVALIDATION_VERSION = "kuuos_plan_invalidation_receipt_v0_22"

PLAN_STATUSES = frozenset(
    {
        "ready",
        "blocked_unknown",
        "blocked_contradiction",
        "blocked_stale",
        "capability_gap",
        "resource_blocked",
        "invalidated",
    }
)
VERIFICATION_STATUSES = frozenset(
    {
        "verified_success",
        "partial_success",
        "inconclusive",
        "contradicted",
        "regression_detected",
        "verification_requires_human",
    }
)
CRITERION_STATUSES = frozenset(
    {"satisfied", "unsatisfied", "unknown", "contradicted", "regressed"}
)

PLAN_NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_final_commitment_authority": False,
    "grants_self_modification_authority": False,
    "planner_can_self_verify": False,
}

VERIFICATION_NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_final_commitment_authority": False,
    "grants_self_modification_authority": False,
    "grants_mission_transition_authority": False,
}

REQUIRED_BOUNDARY = {
    "plan_is_proposal_only": True,
    "lower_effect_license_is_required": True,
    "planner_verifier_separation_is_required": True,
    "execution_success_is_not_mission_success": True,
    "independent_observation_is_required_for_verified_success": True,
    "belief_change_invalidates_exact_plan_basis": True,
    "contradiction_is_not_silently_resolved": True,
    "resource_envelope_remains_finite": True,
    "mission_and_chart_binding_are_exact": True,
    "root_overwrite_is_forbidden": True,
    "graph_semantics_forbidden": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "semantic_plan_digest"))


def step_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "plan_step_digest"))


def verification_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "verification_receipt_digest"))


def invalidation_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "plan_invalidation_receipt_digest"))


def _text(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name}_missing")
    return result


def _nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if result < 0:
        raise ValueError(f"{name}_negative")
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


def _confidence(value: Any) -> float:
    result = _finite(value, "confidence", minimum=0.0)
    if result > 1.0:
        raise ValueError("confidence_above_one")
    return result


def _strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = False
) -> list[str]:
    result = [_text(item, name) for item in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _source_errors(
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
) -> list[str]:
    errors = ["contract:" + item for item in validate_mission_contract(contract)]
    errors.extend(
        "mission_state:" + item
        for item in validate_mission_state(mission_state, contract)
    )
    errors.extend(
        "belief_state:" + item
        for item in validate_belief_state(belief_state, contract, mission_state)
    )
    if mission_state.get("lifecycle_state") != "active":
        errors.append("mission_not_active")
    return errors


def _acyclic(nodes: Sequence[str], dependencies: Mapping[str, Sequence[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visited:
            return True
        if node in visiting:
            return False
        visiting.add(node)
        for dependency in dependencies.get(node, []):
            if not visit(str(dependency)):
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    return all(visit(str(node)) for node in nodes)


def _normalize_subgoals(subgoals: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in subgoals:
        packet = {
            "subgoal_id": _text(item.get("subgoal_id"), "subgoal_id"),
            "objective": _text(item.get("objective"), "subgoal_objective"),
            "dependencies": _strings(
                item.get("dependencies", []), "subgoal_dependencies", allow_empty=True
            ),
            "required_claim_ids": _strings(
                item.get("required_claim_ids", []),
                "subgoal_required_claim_ids",
                allow_empty=True,
            ),
        }
        result.append(packet)
    identifiers = [item["subgoal_id"] for item in result]
    if not identifiers:
        raise ValueError("subgoals_missing")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("subgoal_id_duplicate")
    identifier_set = set(identifiers)
    for item in result:
        if item["subgoal_id"] in item["dependencies"]:
            raise ValueError("subgoal_self_dependency")
        if not set(item["dependencies"]).issubset(identifier_set):
            raise ValueError("subgoal_dependency_missing")
    if not _acyclic(
        identifiers, {item["subgoal_id"]: item["dependencies"] for item in result}
    ):
        raise ValueError("subgoal_dependency_cycle")
    return result


def _normalize_step(item: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": STEP_VERSION,
        "step_id": _text(item.get("step_id"), "step_id"),
        "objective": _text(item.get("objective"), "step_objective"),
        "dependencies": _strings(
            item.get("dependencies", []), "step_dependencies", allow_empty=True
        ),
        "required_capabilities": _strings(
            item.get("required_capabilities", []),
            "step_required_capabilities",
            allow_empty=True,
        ),
        "cost_bound": _finite(item.get("cost_bound", 0.0), "step_cost_bound"),
        "expected_observations": _strings(
            item.get("expected_observations", []), "expected_observations"
        ),
        "success_claim_ids": _strings(
            item.get("success_claim_ids", []), "success_claim_ids"
        ),
        "compensation_refs": _strings(
            item.get("compensation_refs", []),
            "compensation_refs",
            allow_empty=True,
        ),
        "effect_authority_granted": False,
        "plan_step_digest": "",
    }
    packet["plan_step_digest"] = step_digest(packet)
    return packet


def _normalize_steps(steps: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = [_normalize_step(item) for item in steps]
    identifiers = [item["step_id"] for item in result]
    if not identifiers:
        raise ValueError("plan_steps_missing")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("step_id_duplicate")
    identifier_set = set(identifiers)
    for item in result:
        if item["step_id"] in item["dependencies"]:
            raise ValueError("step_self_dependency")
        if not set(item["dependencies"]).issubset(identifier_set):
            raise ValueError("step_dependency_missing")
    if not _acyclic(
        identifiers, {item["step_id"]: item["dependencies"] for item in result}
    ):
        raise ValueError("step_dependency_cycle")
    return result


def _normalize_alternatives(
    alternatives: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    result = [
        {
            "alternative_id": _text(item.get("alternative_id"), "alternative_id"),
            "trigger": _text(item.get("trigger"), "alternative_trigger"),
            "summary": _text(item.get("summary"), "alternative_summary"),
        }
        for item in alternatives
    ]
    identifiers = [item["alternative_id"] for item in result]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("alternative_id_duplicate")
    return result


def _claim_evidence_digests(claim: Mapping[str, Any]) -> list[str]:
    return sorted(
        {
            str(digest)
            for field in (
                "support_evidence_digests",
                "oppose_evidence_digests",
                "unknown_evidence_digests",
            )
            for digest in claim.get(field, [])
        }
    )


def _plan_status(blockers: Sequence[Mapping[str, Any]]) -> str:
    blocker_types = {str(item.get("type")) for item in blockers}
    for blocker_type, status in (
        ("claim_contradicted", "blocked_contradiction"),
        ("claim_stale", "blocked_stale"),
        ("claim_unknown", "blocked_unknown"),
        ("capability_gap", "capability_gap"),
        ("resource_envelope_exceeded", "resource_blocked"),
    ):
        if blocker_type in blocker_types:
            return status
    return "ready"


def build_semantic_plan(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    planner_id: str,
    plan_id: str,
    required_claim_ids: Sequence[str],
    available_capabilities: Sequence[str],
    subgoals: Sequence[Mapping[str, Any]],
    steps: Sequence[Mapping[str, Any]],
    alternatives: Sequence[Mapping[str, Any]],
    created_at_ms: int,
    valid_until_ms: int,
    previous_plan: Mapping[str, Any] | None = None,
    failure_verification: Mapping[str, Any] | None = None,
    replan_reason: str = "",
) -> dict[str, Any]:
    errors = _source_errors(contract, mission_state, belief_state)
    errors.extend("goal:" + item for item in validate_goal_proposal(goal, contract))
    errors.extend(
        "portfolio:" + item
        for item in validate_goal_portfolio(goal_portfolio, contract)
    )
    if errors:
        raise ValueError(";".join(errors))
    goal_id = str(goal["goal_id"])
    if goal_id not in set(str(item) for item in goal_portfolio["active_goal_ids"]):
        raise ValueError("selected_goal_not_active")
    if goal_portfolio.get("goal_digests", {}).get(goal_id) != goal.get("goal_digest"):
        raise ValueError("selected_goal_digest_mismatch")

    created = _nonnegative_int(created_at_ms, "created_at_ms")
    valid_until = _nonnegative_int(valid_until_ms, "valid_until_ms")
    if valid_until < created:
        raise ValueError("plan_validity_interval_invalid")
    required_claims = _strings(
        required_claim_ids, "required_claim_ids", allow_empty=True
    )
    claims = belief_state.get("claims", {})
    missing_claims = sorted(set(required_claims) - set(str(item) for item in claims))
    if missing_claims:
        raise ValueError("required_claim_missing:" + ",".join(missing_claims))

    normalized_subgoals = _normalize_subgoals(subgoals)
    normalized_steps = _normalize_steps(steps)
    normalized_alternatives = _normalize_alternatives(alternatives)
    for subgoal in normalized_subgoals:
        if not set(subgoal["required_claim_ids"]).issubset(set(claims)):
            raise ValueError("subgoal_required_claim_missing")

    available = _strings(
        available_capabilities, "available_capabilities", allow_empty=True
    )
    contract_capabilities = set(
        str(item) for item in contract["authority_scope"]["requested_capabilities"]
    )
    if not set(available).issubset(contract_capabilities):
        raise ValueError("available_capability_outside_contract")

    blockers: list[dict[str, Any]] = []
    basis_claim_digests: dict[str, str] = {}
    planning_observations: set[str] = set()
    for claim_id in required_claims:
        claim = claims[claim_id]
        basis_claim_digests[claim_id] = str(claim["claim_digest"])
        planning_observations.update(_claim_evidence_digests(claim))
        status = str(claim["status"])
        if status in {"unknown", "contradicted", "stale"}:
            blockers.append(
                {
                    "type": f"claim_{status}",
                    "claim_id": claim_id,
                    "details": [str(claim.get("proposition", ""))],
                }
            )

    required_capabilities = set(
        str(item) for item in goal.get("required_capabilities", [])
    )
    required_capabilities.update(
        capability
        for step in normalized_steps
        for capability in step["required_capabilities"]
    )
    capability_gap = sorted(required_capabilities - set(available))
    if capability_gap:
        blockers.append(
            {"type": "capability_gap", "claim_id": "", "details": capability_gap}
        )

    total_cost = sum(float(step["cost_bound"]) for step in normalized_steps)
    resource = contract["resource_envelope"]
    remaining_total = max(
        0.0,
        float(resource["max_total_cost"])
        - float(mission_state["used_cost"])
        - float(resource["reserve_floor"]),
    )
    cycle_budget = min(float(resource["max_cycle_cost"]), remaining_total)
    if total_cost > cycle_budget + 1e-12:
        blockers.append(
            {
                "type": "resource_envelope_exceeded",
                "claim_id": "",
                "details": [str(total_cost), str(cycle_budget)],
            }
        )

    revision = 0
    parent_digest = ""
    failure_digest = ""
    normalized_replan_reason = str(replan_reason).strip()
    if previous_plan is not None:
        if previous_plan.get("mission_id") != contract.get("mission_id"):
            raise ValueError("previous_plan_mission_mismatch")
        if previous_plan.get("goal_id") != goal_id:
            raise ValueError("previous_plan_goal_mismatch")
        if previous_plan.get("semantic_plan_digest") != plan_digest(previous_plan):
            raise ValueError("previous_plan_digest_invalid")
        if not normalized_replan_reason:
            raise ValueError("replan_reason_missing")
        revision = int(previous_plan.get("revision", -1)) + 1
        parent_digest = str(previous_plan["semantic_plan_digest"])
        if failure_verification is None:
            raise ValueError("replan_failure_verification_missing")
        if failure_verification.get("source_plan_digest") != parent_digest:
            raise ValueError("replan_verification_plan_mismatch")
        if failure_verification.get("status") == "verified_success":
            raise ValueError("verified_success_cannot_trigger_replan")
        if failure_verification.get("verification_receipt_digest") != verification_digest(
            failure_verification
        ):
            raise ValueError("replan_verification_digest_invalid")
        failure_digest = str(failure_verification["verification_receipt_digest"])
    elif failure_verification is not None:
        raise ValueError("failure_verification_without_previous_plan")

    packet = {
        "version": PLAN_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "source_belief_state_digest": belief_state["observation_belief_state_digest"],
        "chart_id": belief_state["chart_id"],
        "goal_id": goal_id,
        "goal_digest": goal["goal_digest"],
        "goal_portfolio_digest": goal_portfolio["goal_portfolio_digest"],
        "planner_id": _text(planner_id, "planner_id"),
        "plan_id": _text(plan_id, "plan_id"),
        "revision": revision,
        "parent_plan_digest": parent_digest,
        "failure_verification_digest": failure_digest,
        "replan_reason": normalized_replan_reason,
        "status": _plan_status(blockers),
        "required_claim_ids": required_claims,
        "plan_basis_claim_digests": basis_claim_digests,
        "planning_observation_digests": sorted(planning_observations),
        "available_capabilities": available,
        "required_capabilities": sorted(required_capabilities),
        "subgoals": normalized_subgoals,
        "steps": normalized_steps,
        "alternatives": normalized_alternatives,
        "blockers": blockers,
        "total_cost_bound": total_cost,
        "cycle_budget_bound": cycle_budget,
        "created_at_ms": created,
        "valid_until_ms": valid_until,
        "effect_authority_granted": False,
        "non_authority": deepcopy(PLAN_NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "semantic_plan_digest": "",
    }
    packet["semantic_plan_digest"] = plan_digest(packet)
    plan_errors = validate_semantic_plan(
        packet,
        contract,
        mission_state,
        belief_state,
        goal,
        goal_portfolio,
    )
    if plan_errors:
        raise ValueError(";".join(plan_errors))
    return packet


def validate_semantic_plan_static(plan: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("version") != PLAN_VERSION:
        errors.append("plan_version_invalid")
    for field in (
        "mission_id",
        "lineage_id",
        "contract_digest",
        "source_mission_state_digest",
        "source_belief_state_digest",
        "chart_id",
        "goal_id",
        "goal_digest",
        "goal_portfolio_digest",
        "planner_id",
        "plan_id",
    ):
        if not str(plan.get(field, "")).strip():
            errors.append(f"plan_{field}_missing")
    if plan.get("status") not in PLAN_STATUSES:
        errors.append("plan_status_invalid")
    try:
        _nonnegative_int(plan.get("revision"), "revision")
        created = _nonnegative_int(plan.get("created_at_ms"), "created_at_ms")
        valid_until = _nonnegative_int(plan.get("valid_until_ms"), "valid_until_ms")
        if valid_until < created:
            errors.append("plan_validity_interval_invalid")
        _finite(plan.get("total_cost_bound"), "total_cost_bound")
        _finite(plan.get("cycle_budget_bound"), "cycle_budget_bound")
    except ValueError as exc:
        errors.append(str(exc))
    if not isinstance(plan.get("required_claim_ids"), list):
        errors.append("plan_required_claims_invalid")
    elif len(plan["required_claim_ids"]) != len(set(plan["required_claim_ids"])):
        errors.append("plan_required_claims_duplicate")
    if not isinstance(plan.get("plan_basis_claim_digests"), Mapping):
        errors.append("plan_basis_claim_digests_invalid")
    elif set(plan["plan_basis_claim_digests"]) != set(
        plan.get("required_claim_ids", [])
    ):
        errors.append("plan_basis_claim_set_mismatch")
    if not isinstance(plan.get("planning_observation_digests"), list):
        errors.append("plan_observation_digests_invalid")
    elif len(plan["planning_observation_digests"]) != len(
        set(plan["planning_observation_digests"])
    ):
        errors.append("plan_observation_digests_duplicate")
    try:
        normalized_subgoals = _normalize_subgoals(plan.get("subgoals", []))
        if normalized_subgoals != plan.get("subgoals"):
            errors.append("plan_subgoals_not_normalized")
        normalized_steps = _normalize_steps(plan.get("steps", []))
        if normalized_steps != plan.get("steps"):
            errors.append("plan_steps_not_normalized")
        normalized_alternatives = _normalize_alternatives(plan.get("alternatives", []))
        if normalized_alternatives != plan.get("alternatives"):
            errors.append("plan_alternatives_not_normalized")
    except ValueError as exc:
        errors.append(str(exc))
    if not isinstance(plan.get("blockers"), list):
        errors.append("plan_blockers_invalid")
    elif plan.get("status") != _plan_status(plan["blockers"]):
        errors.append("plan_status_blocker_mismatch")
    if plan.get("effect_authority_granted") is not False:
        errors.append("plan_effect_authority_forbidden")
    if dict(plan.get("non_authority", {})) != PLAN_NON_AUTHORITY:
        errors.append("plan_non_authority_invalid")
    if dict(plan.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("plan_boundary_invalid")
    if plan.get("semantic_plan_digest") != plan_digest(plan):
        errors.append("semantic_plan_digest_invalid")
    return errors


def validate_semantic_plan(
    plan: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
) -> list[str]:
    errors = validate_semantic_plan_static(plan)
    errors.extend(_source_errors(contract, mission_state, belief_state))
    errors.extend("goal:" + item for item in validate_goal_proposal(goal, contract))
    errors.extend(
        "portfolio:" + item
        for item in validate_goal_portfolio(goal_portfolio, contract)
    )
    expected = {
        "mission_id": contract.get("mission_id"),
        "lineage_id": contract.get("lineage_id"),
        "contract_digest": contract.get("mission_contract_digest"),
        "source_mission_state_digest": mission_state.get("mission_state_digest"),
        "source_belief_state_digest": belief_state.get(
            "observation_belief_state_digest"
        ),
        "chart_id": belief_state.get("chart_id"),
        "goal_id": goal.get("goal_id"),
        "goal_digest": goal.get("goal_digest"),
        "goal_portfolio_digest": goal_portfolio.get("goal_portfolio_digest"),
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            errors.append(f"plan_{field}_mismatch")
    if goal.get("goal_id") not in goal_portfolio.get("active_goal_ids", []):
        errors.append("plan_goal_not_active")
    for claim_id, digest_value in plan.get("plan_basis_claim_digests", {}).items():
        claim = belief_state.get("claims", {}).get(claim_id)
        if claim is None or claim.get("claim_digest") != digest_value:
            errors.append("plan_claim_basis_mismatch")
    return errors


def build_plan_invalidation_receipt(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    source_belief_state: Mapping[str, Any],
    current_belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    plan: Mapping[str, Any],
    checked_at_ms: int,
) -> dict[str, Any]:
    errors = validate_semantic_plan(
        plan,
        contract,
        mission_state,
        source_belief_state,
        goal,
        goal_portfolio,
    )
    errors.extend(
        "current_belief_state:" + item
        for item in validate_belief_state(current_belief_state, contract, mission_state)
    )
    if errors:
        raise ValueError(";".join(errors))
    changed_claim_ids = sorted(
        claim_id
        for claim_id, digest_value in plan["plan_basis_claim_digests"].items()
        if current_belief_state.get("claims", {}).get(claim_id, {}).get(
            "claim_digest"
        )
        != digest_value
    )
    exact_basis_changed = (
        current_belief_state["observation_belief_state_digest"]
        != plan["source_belief_state_digest"]
    )
    receipt = {
        "version": INVALIDATION_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_plan_digest": plan["semantic_plan_digest"],
        "source_belief_state_digest": plan["source_belief_state_digest"],
        "current_belief_state_digest": current_belief_state[
            "observation_belief_state_digest"
        ],
        "chart_id": plan["chart_id"],
        "status": "invalidated" if exact_basis_changed else "still_current",
        "changed_claim_ids": changed_claim_ids,
        "exact_basis_changed": exact_basis_changed,
        "checked_at_ms": _nonnegative_int(checked_at_ms, "checked_at_ms"),
        "invalidation_grants_execution_authority": False,
        "plan_invalidation_receipt_digest": "",
    }
    receipt["plan_invalidation_receipt_digest"] = invalidation_digest(receipt)
    return receipt


def validate_invalidation_receipt_static(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != INVALIDATION_VERSION:
        errors.append("invalidation_version_invalid")
    if receipt.get("status") not in {"invalidated", "still_current"}:
        errors.append("invalidation_status_invalid")
    if bool(receipt.get("exact_basis_changed")) != (
        receipt.get("status") == "invalidated"
    ):
        errors.append("invalidation_status_basis_mismatch")
    if not isinstance(receipt.get("changed_claim_ids"), list):
        errors.append("invalidation_changed_claims_invalid")
    if receipt.get("invalidation_grants_execution_authority") is not False:
        errors.append("invalidation_authority_forbidden")
    if receipt.get("plan_invalidation_receipt_digest") != invalidation_digest(receipt):
        errors.append("invalidation_digest_invalid")
    return errors


def _normalize_assessments(
    assessments: Sequence[Mapping[str, Any]],
    independent_digests: set[str],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in assessments:
        status = _text(item.get("status"), "criterion_status")
        if status not in CRITERION_STATUSES:
            raise ValueError("criterion_status_invalid")
        evidence = _strings(
            item.get("evidence_observation_digests", []),
            "criterion_evidence",
            allow_empty=True,
        )
        if not set(evidence).issubset(independent_digests):
            raise ValueError("criterion_evidence_not_independent")
        if status == "satisfied" and not evidence:
            raise ValueError("satisfied_criterion_evidence_missing")
        result.append(
            {
                "criterion": _text(item.get("criterion"), "criterion"),
                "status": status,
                "confidence": _confidence(item.get("confidence", 0.0)),
                "evidence_observation_digests": evidence,
                "notes": str(item.get("notes", "")),
            }
        )
    criteria = [item["criterion"] for item in result]
    if len(criteria) != len(set(criteria)):
        raise ValueError("criterion_duplicate")
    return result


def _verification_status(
    *,
    plan_status: str,
    assessments: Sequence[Mapping[str, Any]],
    independent_count: int,
    minimum_confidence: float,
    human_required: bool,
) -> str:
    if human_required:
        return "verification_requires_human"
    statuses = [str(item["status"]) for item in assessments]
    if "regressed" in statuses:
        return "regression_detected"
    if "contradicted" in statuses or "unsatisfied" in statuses:
        return "contradicted"
    all_satisfied = bool(statuses) and all(status == "satisfied" for status in statuses)
    confidence_ok = all(
        float(item["confidence"]) >= minimum_confidence for item in assessments
    )
    if plan_status == "ready" and all_satisfied and confidence_ok and independent_count > 0:
        return "verified_success"
    if "satisfied" in statuses and any(status == "unknown" for status in statuses):
        return "partial_success"
    return "inconclusive"


def build_verification_receipt(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    source_belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    plan: Mapping[str, Any],
    verifier_id: str,
    independent_observations: Sequence[Mapping[str, Any]],
    criterion_assessments: Sequence[Mapping[str, Any]],
    execution_receipt_digests: Sequence[str],
    observed_at_ms: int,
    human_required: bool = False,
) -> dict[str, Any]:
    errors = validate_semantic_plan(
        plan,
        contract,
        mission_state,
        source_belief_state,
        goal,
        goal_portfolio,
    )
    if errors:
        raise ValueError(";".join(errors))
    verifier = _text(verifier_id, "verifier_id")
    if verifier == plan["planner_id"]:
        raise ValueError("planner_self_verification_forbidden")

    observations = [deepcopy(dict(item)) for item in independent_observations]
    observation_digests: list[str] = []
    for observation in observations:
        observation_errors = validate_observation(observation, contract, mission_state)
        if observation_errors:
            raise ValueError("observation:" + ";".join(observation_errors))
        if observation.get("chart_id") != plan.get("chart_id"):
            raise ValueError("verification_observation_chart_mismatch")
        if observation.get("source_id") == plan.get("planner_id"):
            raise ValueError("planner_observation_not_independent")
        digest_value = str(observation["observation_digest"])
        if digest_value in set(plan["planning_observation_digests"]):
            raise ValueError("planning_evidence_reused_as_independent_verification")
        observation_digests.append(digest_value)
    if len(observation_digests) != len(set(observation_digests)):
        raise ValueError("independent_observation_duplicate")

    normalized_assessments = _normalize_assessments(
        criterion_assessments, set(observation_digests)
    )
    expected_criteria = set(str(item) for item in contract["success_criteria"])
    if set(item["criterion"] for item in normalized_assessments) != expected_criteria:
        raise ValueError("verification_criteria_mismatch")
    minimum_confidence = float(contract["evidence_policy"]["minimum_confidence"])
    status = _verification_status(
        plan_status=str(plan["status"]),
        assessments=normalized_assessments,
        independent_count=len(observation_digests),
        minimum_confidence=minimum_confidence,
        human_required=bool(human_required),
    )
    aggregate_confidence = (
        min(float(item["confidence"]) for item in normalized_assessments)
        if normalized_assessments
        else 0.0
    )
    receipt = {
        "version": VERIFICATION_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "source_belief_state_digest": source_belief_state[
            "observation_belief_state_digest"
        ],
        "chart_id": plan["chart_id"],
        "goal_id": plan["goal_id"],
        "source_plan_digest": plan["semantic_plan_digest"],
        "planner_id": plan["planner_id"],
        "verifier_id": verifier,
        "status": status,
        "criterion_assessments": normalized_assessments,
        "independent_observation_digests": observation_digests,
        "execution_receipt_digests": _strings(
            execution_receipt_digests,
            "execution_receipt_digests",
            allow_empty=True,
        ),
        "independent_evidence_count": len(observation_digests),
        "aggregate_confidence": aggregate_confidence,
        "execution_success_implies_mission_success": False,
        "human_required": bool(human_required),
        "observed_at_ms": _nonnegative_int(observed_at_ms, "observed_at_ms"),
        "non_authority": deepcopy(VERIFICATION_NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "verification_receipt_digest": "",
    }
    receipt["verification_receipt_digest"] = verification_digest(receipt)
    receipt_errors = validate_verification_receipt_static(receipt)
    if receipt_errors:
        raise ValueError(";".join(receipt_errors))
    return receipt


def validate_verification_receipt_static(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != VERIFICATION_VERSION:
        errors.append("verification_version_invalid")
    if receipt.get("status") not in VERIFICATION_STATUSES:
        errors.append("verification_status_invalid")
    for field in (
        "mission_id",
        "lineage_id",
        "contract_digest",
        "source_mission_state_digest",
        "source_belief_state_digest",
        "chart_id",
        "goal_id",
        "source_plan_digest",
        "planner_id",
        "verifier_id",
    ):
        if not str(receipt.get(field, "")).strip():
            errors.append(f"verification_{field}_missing")
    if receipt.get("planner_id") == receipt.get("verifier_id"):
        errors.append("planner_self_verification_forbidden")
    assessments = receipt.get("criterion_assessments")
    if not isinstance(assessments, list) or not assessments:
        errors.append("verification_assessments_missing")
    else:
        criteria = [str(item.get("criterion", "")) for item in assessments]
        if len(criteria) != len(set(criteria)):
            errors.append("verification_criterion_duplicate")
        if any(item.get("status") not in CRITERION_STATUSES for item in assessments):
            errors.append("verification_criterion_status_invalid")
    independent = receipt.get("independent_observation_digests")
    if not isinstance(independent, list):
        errors.append("verification_independent_evidence_invalid")
    elif len(independent) != len(set(str(item) for item in independent)):
        errors.append("verification_independent_evidence_duplicate")
    if int(receipt.get("independent_evidence_count", -1)) != len(independent or []):
        errors.append("verification_independent_evidence_count_mismatch")
    if receipt.get("status") == "verified_success" and not independent:
        errors.append("verified_success_without_independent_evidence")
    if receipt.get("execution_success_implies_mission_success") is not False:
        errors.append("execution_success_mission_success_collapse")
    try:
        _confidence(receipt.get("aggregate_confidence"))
        _nonnegative_int(receipt.get("observed_at_ms"), "observed_at_ms")
    except ValueError as exc:
        errors.append(str(exc))
    if dict(receipt.get("non_authority", {})) != VERIFICATION_NON_AUTHORITY:
        errors.append("verification_non_authority_invalid")
    if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("verification_boundary_invalid")
    if receipt.get("verification_receipt_digest") != verification_digest(receipt):
        errors.append("verification_receipt_digest_invalid")
    return errors


def verification_to_mission_evidence(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_verification_receipt_static(receipt)
    if errors:
        raise ValueError(";".join(errors))
    if receipt.get("mission_id") != contract.get("mission_id"):
        raise ValueError("verification_mission_mismatch")
    if receipt.get("source_mission_state_digest") != mission_state.get(
        "mission_state_digest"
    ):
        raise ValueError("verification_mission_state_stale")
    status = str(receipt["status"])
    return build_mission_evidence(
        contract=contract,
        state=mission_state,
        source_id=str(receipt["verifier_id"]),
        source_role="verifier",
        evidence_level="authorized_verification",
        observed_at_ms=int(receipt["observed_at_ms"]),
        confidence=float(receipt["aggregate_confidence"]),
        success_verified=status == "verified_success",
        failure_verified=status in {"contradicted", "regression_detected"},
        invariant_breach=False,
        prohibited_outcome_observed=False,
        nonrecoverable=False,
        external_handover_required=status == "verification_requires_human",
        evidence_refs=list(receipt["independent_observation_digests"])
        + [str(receipt["verification_receipt_digest"])],
    )


__all__ = [
    "CRITERION_STATUSES",
    "INVALIDATION_VERSION",
    "PLAN_NON_AUTHORITY",
    "PLAN_STATUSES",
    "PLAN_VERSION",
    "REQUIRED_BOUNDARY",
    "VERIFICATION_NON_AUTHORITY",
    "VERIFICATION_STATUSES",
    "VERIFICATION_VERSION",
    "VERSION",
    "build_plan_invalidation_receipt",
    "build_semantic_plan",
    "build_verification_receipt",
    "invalidation_digest",
    "plan_digest",
    "step_digest",
    "validate_invalidation_receipt_static",
    "validate_semantic_plan",
    "validate_semantic_plan_static",
    "validate_verification_receipt_static",
    "verification_digest",
    "verification_to_mission_evidence",
]
