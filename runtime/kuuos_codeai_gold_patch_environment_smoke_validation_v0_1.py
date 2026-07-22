from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_schema_v0_1 import (
    BINDING_FIELDS, DECISION_ADMIT, DECISION_HOLD, MODE, OBSERVATION_DIGEST_FIELD,
    PACK_DIGEST_FIELD, PLAN_DIGEST_FIELD, POLICY_DIGEST_FIELD, PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD, REQUEST_DIGEST_FIELD, STATUS_BLOCKED, STATUS_READY,
    GoldPatchEnvironmentSmokeResult, canonical_digest, mapping, seal,
    validate_observation, validate_plan, validate_policy, validate_request,
)

def _binding(value: Mapping[str, Any]) -> dict[str, Any]:
    return {field: value[field] for field in BINDING_FIELDS}

def evaluate_gold_patch_environment_smoke(
    request_value: Any,
    policy_value: Any,
    predecessor_manifest_value: Any,
    plan_value: Any,
    observation_value: Any,
) -> GoldPatchEnvironmentSmokeResult:
    request = mapping(request_value)
    policy = mapping(policy_value)
    predecessor = mapping(predecessor_manifest_value)
    plan = mapping(plan_value)
    observation = mapping(observation_value)
    shape_issues: list[str] = []
    if request is None: shape_issues.append("request_not_mapping")
    if policy is None: shape_issues.append("policy_not_mapping")
    if predecessor is None: shape_issues.append("predecessor_not_mapping")
    if plan is None: shape_issues.append("plan_not_mapping")
    if observation is None: shape_issues.append("observation_not_mapping")
    if shape_issues:
        return GoldPatchEnvironmentSmokeResult(STATUS_BLOCKED, tuple(shape_issues), None, None)
    issues = (
        validate_request(request) + validate_policy(policy) +
        validate_plan(plan) + validate_observation(observation)
    )
    if issues:
        return GoldPatchEnvironmentSmokeResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)

    expected_binding = {field: policy["expected_" + field] for field in BINDING_FIELDS}
    for label, value in (("request", request), ("plan", plan), ("observation", observation)):
        if _binding(value) != expected_binding:
            issues.append(label + "_binding_mismatch")
    if _binding(request) != _binding(plan) or _binding(request) != _binding(observation):
        issues.append("cross_input_binding_mismatch")

    if predecessor.get("profile_version") != "CodeAI External Corpus Acquisition and Freeze Receipt v0.1":
        issues.append("predecessor_profile_mismatch")
    if canonical_digest(predecessor) != request["predecessor_manifest_digest"]:
        issues.append("predecessor_manifest_digest_mismatch")
    if predecessor.get("freeze_decision") != "external_corpus_freeze_admitted":
        issues.append("predecessor_not_admitted")
    if predecessor.get("freeze_pack_digest") != request["predecessor_freeze_pack_digest"]:
        issues.append("predecessor_pack_mismatch")
    if predecessor.get("receipt_digest") != request["predecessor_freeze_receipt_digest"]:
        issues.append("predecessor_receipt_mismatch")
    if predecessor.get("corpus_frozen") is not True:
        issues.append("predecessor_corpus_not_frozen")

    if policy["evaluation_epoch"] - request["request_created_epoch"] > policy["maximum_request_age"]:
        issues.append("request_stale")
    if policy["evaluation_epoch"] - observation["observation_created_epoch"] > policy["maximum_observation_age"]:
        issues.append("observation_stale")
    if plan["run_id"] != observation["run_id"]:
        issues.append("run_id_mismatch")
    if plan["maximum_workers"] != policy["maximum_workers"]:
        issues.append("worker_count_mismatch")
    if plan["timeout_seconds"] != policy["timeout_seconds"]:
        issues.append("timeout_mismatch")

    forbidden_request = (
        request["claims_solver_gold_access"] or
        request["claims_candidate_generation_access"] or
        request["claims_repair_memory_access"] or
        request["claims_repository_mutation_authority"] or
        request["claims_git_authority"] or
        request["claims_correctness"]
    )
    forbidden_policy = (
        policy["allow_kernel_harness_execution"] or
        policy["allow_solver_gold_access"] or
        policy["allow_candidate_generation_access"] or
        policy["allow_repair_memory_access"] or
        policy["allow_repository_mutation"] or
        policy["allow_git_authority"] or
        policy["allow_correctness_claim"]
    )
    if forbidden_request: issues.append("request_forbidden_authority")
    if forbidden_policy: issues.append("policy_forbidden_authority")
    if issues:
        return GoldPatchEnvironmentSmokeResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)

    hold: list[str] = []
    required_true = (
        ("plan_preregistered", plan["plan_preregistered"]),
        ("gold_prediction_mode", plan["gold_prediction_mode"]),
        ("gold_evaluator_only", plan["gold_available_to_evaluator_only"]),
        ("external_harness_observed", observation["external_harness_execution_observed"]),
        ("network_by_external_harness", observation["network_access_performed_by_external_harness"]),
        ("docker_used", observation["docker_used"]),
        ("image_available", observation["image_available"]),
        ("container_started", observation["container_started"]),
        ("gold_patch_applied", observation["gold_patch_applied"]),
        ("evaluation_completed", observation["evaluation_completed"]),
        ("report_observed", observation["report_observed"]),
        ("logs_observed", observation["logs_observed"]),
        ("resolved", observation["resolved"]),
    )
    for name, value in required_true:
        if value is not True: hold.append(name + "_required")
    forbidden_observed = (
        ("plan_gold_available_to_solver", plan["gold_available_to_solver"]),
        ("kernel_harness_execution", observation["harness_execution_performed_by_kernel"]),
        ("solver_gold_exposure", observation["gold_patch_exposed_to_solver"]),
        ("candidate_generation_gold_use", observation["gold_patch_used_for_candidate_generation"]),
        ("repair_memory_gold_use", observation["gold_patch_used_for_repair_memory"]),
        ("repository_mutation", observation["repository_mutation_performed"]),
        ("git_authority", observation["git_authority_granted"]),
        ("correctness_claim", observation["correctness_claimed"]),
    )
    for name, value in forbidden_observed:
        if value is True: hold.append(name + "_forbidden")
    if len(plan["instance_ids"]) != policy["required_smoke_runs"]:
        hold.append("smoke_run_count_mismatch")

    decision = DECISION_ADMIT if not hold else DECISION_HOLD
    pack = seal({
        "schema_version": "v0.1",
        "profile_version": PROFILE_VERSION,
        "mode": MODE,
        "binding": expected_binding,
        "request_digest": request[REQUEST_DIGEST_FIELD],
        "policy_digest": policy[POLICY_DIGEST_FIELD],
        "plan_digest": plan[PLAN_DIGEST_FIELD],
        "observation_digest": observation[OBSERVATION_DIGEST_FIELD],
        "decision": decision,
        "hold_reasons": sorted(set(hold)),
        "smoke_run_count": len(plan["instance_ids"]),
        "resolved_count": 1 if observation["resolved"] else 0,
        "gold_prediction_mode": plan["gold_prediction_mode"],
        "gold_evaluator_only": plan["gold_available_to_evaluator_only"],
        "external_harness_execution_observed": observation["external_harness_execution_observed"],
        "harness_execution_performed_by_kernel": observation["harness_execution_performed_by_kernel"],
        "repository_mutation_performed": observation["repository_mutation_performed"],
        "git_authority_granted": observation["git_authority_granted"],
        "correctness_claimed": observation["correctness_claimed"],
    }, PACK_DIGEST_FIELD)
    receipt = seal({
        "schema_version": "v0.1",
        "profile_version": PROFILE_VERSION,
        "status": STATUS_READY,
        "mode": MODE,
        "decision": decision,
        "instance_id": request["instance_id"],
        "resolved": observation["resolved"],
        "smoke_pack_digest": pack[PACK_DIGEST_FIELD],
        "gold_patch_available_to_solver": False,
        "gold_patch_used_for_candidate_generation": False,
        "gold_patch_used_for_repair_memory": False,
        "future_harness_execution_authority_granted": False,
        "repository_mutation_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }, RECEIPT_DIGEST_FIELD)
    return GoldPatchEnvironmentSmokeResult(STATUS_READY, tuple(sorted(set(hold))), pack, receipt)
