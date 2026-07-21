from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_trajectory_grounded_specialist_router_admission_checks_v0_1 import (
    binding_mismatches, validate_specialists, validate_trajectory,
)
from runtime.kuuos_codeai_trajectory_grounded_specialist_router_admission_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAITrajectoryGroundedSpecialistRouterAdmissionResult:
    return CodeAITrajectoryGroundedSpecialistRouterAdmissionResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def _receipt(pack: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "admission_pack_digest": pack[PACK_DIGEST_FIELD],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "trajectory_digest": pack["trajectory_digest"],
        "memory_pack_digest": pack["memory_pack_digest"],
        "memory_receipt_digest": pack["memory_receipt_digest"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "queried_subtask_kind": pack["queried_subtask_kind"],
        "route_decision": pack["route_decision"],
        "selected_specialist_id": pack["selected_specialist_id"],
        "measurement_grounded": pack["measurement_grounded"],
        "exact_binding_verified": True,
        "memory_pack_binding_verified": True,
        "specialist_alignment_verified": True,
        "independent_measurement_verified": True,
        "route_hint_only": True,
        "specialist_dispatched": False,
        "candidate_selected": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_trajectory_grounded_specialist_router_admission(
    *, request: Any, policy: Any, trajectory: Any, specialists: Any
) -> CodeAITrajectoryGroundedSpecialistRouterAdmissionResult:
    request_map = mapping(request)
    policy_map = mapping(policy)
    trajectory_map = mapping(trajectory)
    if any(item is None for item in (request_map, policy_map, trajectory_map)):
        return _blocked("input_not_mapping")
    assert request_map is not None and policy_map is not None and trajectory_map is not None

    issues = (
        validate_request(request_map)
        + validate_policy(policy_map)
        + validate_trajectory(trajectory_map)
        + validate_specialists(specialists)
    )
    if issues:
        return _blocked(*issues)

    required_true = (
        "require_exact_binding", "require_partial_trajectory", "require_observable_artifacts",
        "require_independent_measurement", "require_specialist_alignment",
        "require_memory_pack_binding", "allow_route_hint",
    )
    if any(policy_map[field] is not True for field in required_true):
        return _blocked("policy_required_guarantee_disabled")
    forbidden = (
        "allow_specialist_dispatch", "allow_candidate_selection", "allow_execution_authority",
        "allow_repository_mutation", "allow_git_authority",
    )
    if any(policy_map[field] is not False for field in forbidden):
        return _blocked("policy_effect_or_authority_enabled")
    if any(request_map[field] for field in (
        "claims_selection_authority", "claims_dispatch_authority", "claims_execution_authority",
        "claims_repository_mutation_authority", "claims_git_authority",
    )):
        return _blocked("request_claims_authority")
    if request_map["unresolved_questions"]:
        return _blocked("request_unresolved_questions_present")

    binding_issues = [
        "request_policy_binding_mismatch:" + field
        for field in BINDING_FIELDS
        if request_map[field] != policy_map["expected_" + field]
    ]
    binding_issues.extend(
        "trajectory_binding_mismatch:" + field
        for field in binding_mismatches(trajectory_map, request_map)
    )
    if binding_issues:
        return _blocked(*binding_issues)

    evaluation_epoch = int(policy_map["evaluation_epoch"])
    request_epoch = int(request_map["request_created_epoch"])
    trajectory_epoch = int(trajectory_map["trajectory_created_epoch"])
    if not evaluation_epoch - int(policy_map["maximum_request_age"]) <= request_epoch <= evaluation_epoch:
        return _blocked("request_window_invalid")
    if not evaluation_epoch - int(policy_map["maximum_trajectory_age"]) <= trajectory_epoch <= evaluation_epoch:
        return _blocked("trajectory_window_invalid")

    trajectory_requirements = (
        (trajectory_map["exploration_turns"] >= policy_map["minimum_exploration_turns"], "trajectory_turns_insufficient"),
        (trajectory_map["observation_count"] >= policy_map["minimum_observation_count"], "trajectory_observations_insufficient"),
        (trajectory_map["execution_signal_count"] >= policy_map["minimum_execution_signal_count"], "trajectory_execution_signals_insufficient"),
        (len(trajectory_map["grounding_sources"]) >= policy_map["minimum_grounding_sources"], "trajectory_grounding_sources_insufficient"),
        (len(trajectory_map["observable_artifact_digests"]) >= policy_map["minimum_observable_artifacts"], "trajectory_artifacts_insufficient"),
        (trajectory_map["self_report_only"] is False, "trajectory_self_report_only"),
        (trajectory_map["measurement_complete"] is True, "trajectory_measurement_incomplete"),
        (trajectory_map["repository_state_observed"] is True, "trajectory_repository_state_unobserved"),
        (trajectory_map["tests_observed"] is True, "trajectory_tests_unobserved"),
    )
    trajectory_issues = [code for condition, code in trajectory_requirements if not condition]
    for field in (
        "repository_mutation_performed", "specialist_dispatched", "candidate_selected",
        "execution_authority_granted", "git_authority_granted",
    ):
        if trajectory_map[field]:
            trajectory_issues.append("trajectory_forbidden_effect:" + field)
    if trajectory_issues:
        return _blocked(*trajectory_issues)

    candidates = list(specialists)
    if len(candidates) > int(policy_map["maximum_candidates"]):
        return _blocked("specialist_candidate_budget_exceeded")

    requested_kinds = set(request_map["requested_specialist_kinds"])
    eligible: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for evidence in candidates:
        reasons: list[str] = []
        reasons.extend("binding_mismatch:" + field for field in binding_mismatches(evidence, request_map))
        if evidence["specialist_kind"] not in requested_kinds:
            reasons.append("specialist_not_requested")
        if evidence["supported_subtask_kind"] != request_map["subtask_kind"]:
            reasons.append("subtask_mismatch")
        if evidence["measurement_packet_digest"] != trajectory_map[TRAJECTORY_DIGEST_FIELD]:
            reasons.append("measurement_packet_mismatch")
        if evidence["independent_measurement"] is not True:
            reasons.append("measurement_not_independent")
        if evidence["route_hint_only"] is not True:
            reasons.append("route_hint_boundary_missing")
        if evidence["fit_score"] < policy_map["minimum_fit_score"]:
            reasons.append("fit_score_below_threshold")
        if evidence["reliability_score"] < policy_map["minimum_reliability_score"]:
            reasons.append("reliability_score_below_threshold")
        if evidence["estimated_cost_units"] > policy_map["maximum_cost_units"]:
            reasons.append("cost_above_limit")
        if not evaluation_epoch - int(policy_map["maximum_evidence_age"]) <= int(evidence["evidence_created_epoch"]) <= evaluation_epoch:
            reasons.append("evidence_window_invalid")
        for field in (
            "repository_mutation_performed", "specialist_dispatched", "candidate_selected",
            "execution_authority_granted", "git_authority_granted", "correctness_claimed",
        ):
            if evidence[field]:
                reasons.append("forbidden_specialist_claim:" + field)
        if reasons:
            excluded.append({
                "specialist_id": evidence["specialist_id"],
                "specialist_digest": evidence[SPECIALIST_DIGEST_FIELD],
                "reasons": sorted(set(reasons)),
            })
        else:
            eligible.append(evidence)

    eligible.sort(key=lambda item: (-int(item["utility_score"]), item["specialist_id"]))
    selected: dict[str, Any] | None = None
    hold_reason = "no_admissible_specialist"
    if eligible:
        if len(eligible) == 1:
            selected = eligible[0]
        else:
            top, runner_up = eligible[0], eligible[1]
            if int(top["utility_score"]) >= int(runner_up["utility_score"]) + int(policy_map["minimum_route_margin"]):
                selected = top
            else:
                hold_reason = "route_margin_not_met"

    route_decision = DECISION_ADMIT if selected is not None else DECISION_HOLD
    pack = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": request_map["request_id"],
        "request_revision": request_map["request_revision"],
        "request_digest": request_map[REQUEST_DIGEST_FIELD],
        "policy_digest": policy_map[POLICY_DIGEST_FIELD],
        "trajectory_digest": trajectory_map[TRAJECTORY_DIGEST_FIELD],
        "repository_full_name": request_map["repository_full_name"],
        "source_commit_sha": request_map["source_commit_sha"],
        "source_tree_digest": request_map["source_tree_digest"],
        "memory_pack_digest": request_map["memory_pack_digest"],
        "memory_receipt_digest": request_map["memory_receipt_digest"],
        "queried_subtask_kind": request_map["subtask_kind"],
        "exploration_turns": trajectory_map["exploration_turns"],
        "observation_count": trajectory_map["observation_count"],
        "execution_signal_count": trajectory_map["execution_signal_count"],
        "grounding_source_count": len(trajectory_map["grounding_sources"]),
        "observable_artifact_count": len(trajectory_map["observable_artifact_digests"]),
        "measurement_grounded": True,
        "eligible_specialist_count": len(eligible),
        "excluded_specialist_count": len(excluded),
        "eligible_specialists": [
            {
                "specialist_id": item["specialist_id"],
                "specialist_kind": item["specialist_kind"],
                "specialist_digest": item[SPECIALIST_DIGEST_FIELD],
                "fit_score": item["fit_score"],
                "reliability_score": item["reliability_score"],
                "estimated_cost_units": item["estimated_cost_units"],
                "utility_score": item["utility_score"],
            }
            for item in eligible
        ],
        "excluded_specialists": excluded,
        "route_decision": route_decision,
        "hold_reason": None if selected is not None else hold_reason,
        "selected_specialist_id": None if selected is None else selected["specialist_id"],
        "selected_specialist_kind": None if selected is None else selected["specialist_kind"],
        "selected_specialist_digest": None if selected is None else selected[SPECIALIST_DIGEST_FIELD],
        "selected_utility_score": None if selected is None else selected["utility_score"],
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_ADMISSION_ONLY,
        "exact_binding_verified": True,
        "memory_pack_binding_verified": True,
        "specialist_alignment_verified": True,
        "independent_measurement_verified": True,
        "route_hint_only": True,
        "specialist_dispatched": False,
        "candidate_selected": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    pack = seal(pack, PACK_DIGEST_FIELD)
    return CodeAITrajectoryGroundedSpecialistRouterAdmissionResult(
        STATUS_READY, (), pack, _receipt(pack)
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAITrajectoryGroundedSpecialistRouterAdmissionResult",
    "build_codeai_trajectory_grounded_specialist_router_admission",
    "canonical_digest", "canonical_json", "digest_without", "seal",
]
