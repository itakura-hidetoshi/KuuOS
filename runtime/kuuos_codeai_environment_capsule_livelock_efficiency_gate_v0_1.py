from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_environment_capsule_livelock_efficiency_gate_checks_v0_1 import (
    binding_mismatches,
    derive_progress_metrics,
    validate_environment_capsule,
    validate_progress_trace,
    validate_router_admission,
)
from runtime.kuuos_codeai_environment_capsule_livelock_efficiency_gate_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult:
    return CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def _receipt(pack: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "gate_pack_digest": pack[PACK_DIGEST_FIELD],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "router_admission_manifest_digest": pack["router_admission_manifest_digest"],
        "router_admission_pack_digest": pack["router_admission_pack_digest"],
        "router_admission_receipt_digest": pack["router_admission_receipt_digest"],
        "environment_capsule_digest": pack["environment_capsule_digest"],
        "progress_trace_digest": pack["progress_trace_digest"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "selected_specialist_id": pack["selected_specialist_id"],
        "gate_decision": pack["gate_decision"],
        "hold_reasons": pack["hold_reasons"],
        "environment_exact": pack["environment_exact"],
        "capsule_reproducible": pack["capsule_reproducible"],
        "livelock_free": pack["livelock_free"],
        "efficiency_within_budget": pack["efficiency_within_budget"],
        "continuation_hint_only": True,
        "continuation_authority_granted": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_environment_capsule_livelock_efficiency_gate(
    *, request: Any, policy: Any, router_admission: Any, environment_capsule: Any, progress_trace: Any
) -> CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult:
    request_map = mapping(request)
    policy_map = mapping(policy)
    router_map = mapping(router_admission)
    capsule_map = mapping(environment_capsule)
    trace_map = mapping(progress_trace)
    if any(item is None for item in (request_map, policy_map, router_map, capsule_map, trace_map)):
        return _blocked("input_not_mapping")
    assert request_map is not None and policy_map is not None and router_map is not None
    assert capsule_map is not None and trace_map is not None

    issues = (
        validate_request(request_map)
        + validate_policy(policy_map)
        + validate_router_admission(router_map)
        + validate_environment_capsule(capsule_map)
        + validate_progress_trace(trace_map)
    )
    if issues:
        return _blocked(*issues)

    required_true = (
        "require_exact_binding",
        "require_immutable_capsule",
        "require_complete_capsule",
        "require_observed_capsule",
        "require_dependency_lock",
        "require_network_disabled",
        "require_observable_trace",
        "require_cycle_free",
        "allow_continuation_hint",
    )
    if any(policy_map[field] is not True for field in required_true):
        return _blocked("policy_required_guarantee_disabled")
    forbidden_policy = (
        "allow_continuation_authority",
        "allow_execution_authority",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
    )
    if any(policy_map[field] is not False for field in forbidden_policy):
        return _blocked("policy_effect_or_authority_enabled")
    if any(request_map[field] for field in (
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
    )):
        return _blocked("request_claims_authority_or_correctness")
    if request_map["unresolved_questions"]:
        return _blocked("request_unresolved_questions_present")

    binding_issues = [
        "request_policy_binding_mismatch:" + field
        for field in BINDING_FIELDS
        if request_map[field] != policy_map["expected_" + field]
    ]
    binding_issues.extend(
        "capsule_binding_mismatch:" + field
        for field in binding_mismatches(capsule_map, request_map)
    )
    binding_issues.extend(
        "trace_binding_mismatch:" + field
        for field in binding_mismatches(trace_map, request_map)
    )
    if binding_issues:
        return _blocked(*binding_issues)

    actual_router_manifest_digest = canonical_digest(router_map)
    predecessor_checks = (
        (actual_router_manifest_digest == request_map["router_admission_manifest_digest"], "router_manifest_digest_mismatch"),
        (router_map["admission_pack_digest"] == request_map["router_admission_pack_digest"], "router_pack_digest_mismatch"),
        (router_map["receipt_digest"] == request_map["router_admission_receipt_digest"], "router_receipt_digest_mismatch"),
        (router_map["selected_specialist_id"] == request_map["selected_specialist_id"], "router_selected_specialist_id_mismatch"),
        (router_map["selected_specialist_kind"] == request_map["selected_specialist_kind"], "router_selected_specialist_kind_mismatch"),
        (router_map["queried_subtask_kind"] == request_map["selected_subtask_kind"], "router_subtask_mismatch"),
        (router_map["route_decision"] == "specialist_route_admitted", "router_route_not_admitted"),
        (router_map["route_hint_only"] is True, "router_route_hint_boundary_missing"),
        (router_map["measurement_grounded"] is True, "router_measurement_not_grounded"),
    )
    predecessor_issues = [code for condition, code in predecessor_checks if not condition]
    for field in (
        "specialist_dispatched",
        "candidate_selected",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if router_map[field]:
            predecessor_issues.append("router_forbidden_effect:" + field)
    if predecessor_issues:
        return _blocked(*predecessor_issues)

    if trace_map["environment_capsule_digest"] != capsule_map[CAPSULE_DIGEST_FIELD]:
        return _blocked("trace_capsule_digest_mismatch")

    evaluation_epoch = int(policy_map["evaluation_epoch"])
    time_checks = (
        (
            evaluation_epoch - int(policy_map["maximum_request_age"])
            <= int(request_map["request_created_epoch"])
            <= evaluation_epoch,
            "request_window_invalid",
        ),
        (
            evaluation_epoch - int(policy_map["maximum_capsule_age"])
            <= int(capsule_map["capsule_created_epoch"])
            <= evaluation_epoch,
            "capsule_window_invalid",
        ),
        (
            evaluation_epoch - int(policy_map["maximum_trace_age"])
            <= int(trace_map["trace_created_epoch"])
            <= evaluation_epoch,
            "trace_window_invalid",
        ),
    )
    time_issues = [code for condition, code in time_checks if not condition]
    if time_issues:
        return _blocked(*time_issues)

    metrics = derive_progress_metrics(list(trace_map["checkpoints"]))
    hold_reasons: list[str] = []

    environment_checks = (
        (capsule_map["root_filesystem_immutable"] is True, "environment_capsule_not_immutable"),
        (capsule_map["dependency_lock_verified"] is True, "environment_dependency_lock_unverified"),
        (capsule_map["capsule_complete"] is True, "environment_capsule_incomplete"),
        (capsule_map["capsule_observed"] is True, "environment_capsule_unobserved"),
        (capsule_map["self_report_only"] is False, "environment_capsule_self_report_only"),
        (capsule_map["network_access_allowed"] is False, "environment_capsule_network_enabled"),
    )
    hold_reasons.extend(code for condition, code in environment_checks if not condition)

    trace_checks = (
        (trace_map["trace_observable"] is True, "progress_trace_not_observable"),
        (trace_map["trace_complete"] is True, "progress_trace_incomplete"),
        (trace_map["self_report_only"] is False, "progress_trace_self_report_only"),
    )
    hold_reasons.extend(code for condition, code in trace_checks if not condition)

    for source_name, source in (("capsule", capsule_map), ("trace", trace_map)):
        for field in (
            "continuation_authority_granted",
            "execution_authority_granted",
            "repository_mutation_performed",
            "git_authority_granted",
            "correctness_claimed",
        ):
            if source[field]:
                hold_reasons.append(source_name + "_forbidden_effect:" + field)

    if metrics["cycle_count"] > int(policy_map["maximum_cycle_count"]):
        hold_reasons.append("livelock_cycle_detected")
    if metrics["repeated_zero_progress_transitions"] > int(policy_map["maximum_repeated_zero_progress_transitions"]):
        hold_reasons.append("livelock_repeated_zero_progress_transition")
    if metrics["maximum_no_progress_streak"] > int(policy_map["maximum_no_progress_streak"]):
        hold_reasons.append("livelock_no_progress_streak_exceeded")

    budget_checks = (
        (metrics["step_count"] <= policy_map["maximum_steps"], "efficiency_step_budget_exceeded"),
        (metrics["tool_call_count"] <= policy_map["maximum_tool_calls"], "efficiency_tool_call_budget_exceeded"),
        (metrics["model_call_count"] <= policy_map["maximum_model_calls"], "efficiency_model_call_budget_exceeded"),
        (metrics["token_units"] <= policy_map["maximum_token_units"], "efficiency_token_budget_exceeded"),
        (metrics["wall_clock_ms"] <= policy_map["maximum_wall_clock_ms"], "efficiency_wall_clock_budget_exceeded"),
        (metrics["failed_action_count"] <= policy_map["maximum_failed_actions"], "efficiency_failed_action_budget_exceeded"),
        (metrics["total_progress_units"] >= policy_map["minimum_total_progress_units"], "efficiency_total_progress_insufficient"),
        (metrics["distinct_state_count"] >= policy_map["minimum_distinct_state_count"], "efficiency_distinct_state_progress_insufficient"),
    )
    hold_reasons.extend(code for condition, code in budget_checks if not condition)
    hold_reasons = sorted(set(hold_reasons))

    environment_reason_prefixes = ("environment_", "capsule_forbidden_effect:")
    livelock_reason_prefix = "livelock_"
    efficiency_reason_prefix = "efficiency_"
    capsule_reproducible = not any(reason.startswith(environment_reason_prefixes) for reason in hold_reasons)
    livelock_free = not any(reason.startswith(livelock_reason_prefix) for reason in hold_reasons)
    efficiency_within_budget = not any(reason.startswith(efficiency_reason_prefix) for reason in hold_reasons)
    trace_grounded = not any(reason.startswith("progress_trace_") or reason.startswith("trace_forbidden_effect:") for reason in hold_reasons)
    gate_decision = DECISION_CONTINUE if not hold_reasons else DECISION_HOLD

    pack = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": request_map["request_id"],
        "request_revision": request_map["request_revision"],
        "request_digest": request_map[REQUEST_DIGEST_FIELD],
        "policy_digest": policy_map[POLICY_DIGEST_FIELD],
        "router_admission_manifest_digest": request_map["router_admission_manifest_digest"],
        "router_admission_pack_digest": request_map["router_admission_pack_digest"],
        "router_admission_receipt_digest": request_map["router_admission_receipt_digest"],
        "environment_capsule_digest": capsule_map[CAPSULE_DIGEST_FIELD],
        "progress_trace_digest": trace_map[TRACE_DIGEST_FIELD],
        "repository_full_name": request_map["repository_full_name"],
        "source_commit_sha": request_map["source_commit_sha"],
        "source_tree_digest": request_map["source_tree_digest"],
        "selected_specialist_id": request_map["selected_specialist_id"],
        "selected_specialist_kind": request_map["selected_specialist_kind"],
        "selected_subtask_kind": request_map["selected_subtask_kind"],
        **metrics,
        "environment_exact": True,
        "predecessor_router_verified": True,
        "trace_grounded": trace_grounded,
        "capsule_reproducible": capsule_reproducible,
        "livelock_free": livelock_free,
        "efficiency_within_budget": efficiency_within_budget,
        "gate_decision": gate_decision,
        "hold_reasons": hold_reasons,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_GATE_ONLY,
        "continuation_hint_only": True,
        "continuation_authority_granted": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    pack = seal(pack, PACK_DIGEST_FIELD)
    return CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult(
        STATUS_READY, (), pack, _receipt(pack)
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult",
    "build_codeai_environment_capsule_livelock_efficiency_gate",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
