from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_baseline_versus_codeai_ablation_comparison_checks_v0_1 import *


def _cohort_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["cohort_id"]: item for item in registry["cohorts"]}


def _metric_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["metric_id"]: item for item in registry["metrics"]}


def _observation_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["cohort_id"]: item for item in registry["observations"]}


def build_codeai_baseline_versus_codeai_ablation_comparison(
    *,
    request: dict[str, Any],
    policy: dict[str, Any],
    predecessor_manifest: dict[str, Any],
    plan: dict[str, Any],
    cohort_registry: dict[str, Any],
    metric_registry: dict[str, Any],
    observation_registry: dict[str, Any],
) -> ComparisonResult:
    try:
        validate_structure(
            request=request,
            policy=policy,
            predecessor_manifest=predecessor_manifest,
            plan=plan,
            cohort_registry=cohort_registry,
            metric_registry=metric_registry,
            observation_registry=observation_registry,
        )
        if not exact_binding(
            request, policy, plan, cohort_registry, metric_registry, observation_registry
        ):
            raise BlockedInput("exact binding mismatch")
        if not nested_binding_ok(request, cohort_registry, observation_registry):
            raise BlockedInput("nested sample or holdout binding mismatch")
        if request["predecessor_manifest_digest"] != canonical_digest(predecessor_manifest):
            raise BlockedInput("predecessor manifest digest mismatch")
        if not freshness_ok(
            request, policy, plan, cohort_registry, metric_registry, observation_registry
        ):
            raise BlockedInput("stale or future-dated comparison material")
    except BlockedInput as exc:
        return ComparisonResult(STATUS_BLOCKED, (str(exc),), None, None)

    reasons: list[str] = []
    required_cohorts = tuple(policy["required_cohort_ids"])
    required_metrics = tuple(policy["required_metric_ids"])
    cohort_map = _cohort_map(cohort_registry)
    metric_map = _metric_map(metric_registry)
    observation_map = _observation_map(observation_registry)

    if predecessor_manifest["decision"] != "external_result_process_evidence_ingestion_admitted":
        reasons.append("predecessor not admitted")
    if not predecessor_manifest["execution_valid"]:
        reasons.append("predecessor execution invalid")
    if predecessor_manifest["ingestion_pack_digest"] != request["predecessor_ingestion_pack_digest"]:
        reasons.append("predecessor ingestion pack mismatch")
    if predecessor_manifest["receipt_digest"] != request["predecessor_receipt_digest"]:
        reasons.append("predecessor receipt mismatch")
    if predecessor_manifest["raw_gold_ingested"]:
        reasons.append("predecessor raw gold leakage")
    if predecessor_manifest["raw_test_names_ingested"]:
        reasons.append("predecessor raw test-name leakage")
    if predecessor_manifest["raw_logs_committed"]:
        reasons.append("predecessor raw-log leakage")
    if predecessor_manifest["candidate_generation_feedback_enabled"]:
        reasons.append("predecessor candidate feedback enabled")
    if predecessor_manifest["repair_memory_feedback_enabled"]:
        reasons.append("predecessor repair-memory feedback enabled")
    if predecessor_manifest["repository_mutation_authority_granted"]:
        reasons.append("predecessor repository mutation authority")
    if predecessor_manifest["git_authority_granted"]:
        reasons.append("predecessor Git authority")
    if predecessor_manifest["correctness_claimed"]:
        reasons.append("predecessor correctness claim")

    for field in (
        "require_exact_binding", "require_predecessor_admitted",
        "require_predecessor_execution_valid", "require_aggregate_only",
        "require_frozen_holdout", "require_equal_target_sample_count",
        "require_balanced_measured_cohorts",
        "require_execution_failure_as_unresolved", "require_missing_evidence_hold",
        "allow_preregistration_with_pending_observations",
        "allow_limited_comparison_authority",
    ):
        if not policy[field]:
            reasons.append(f"required policy disabled: {field}")
    for field in (
        "allow_raw_gold_access", "allow_raw_test_names", "allow_raw_logs",
        "allow_candidate_feedback", "allow_repair_memory_feedback",
        "allow_repository_mutation", "allow_git_authority",
        "allow_correctness_claim",
    ):
        if policy[field]:
            reasons.append(f"policy authority overreach: {field}")

    for field in (
        "claims_raw_gold_access", "claims_raw_test_name_access",
        "claims_raw_log_access", "claims_candidate_generation_feedback",
        "claims_repair_memory_feedback",
        "claims_repository_mutation_authority", "claims_git_authority",
        "claims_correctness",
    ):
        if request[field]:
            reasons.append(f"request authority overreach: {field}")

    if request["comparison_phase"] != plan["comparison_phase"]:
        reasons.append("request/plan phase mismatch")
    if plan["comparison_mode"] != "aggregate-only-preregistered":
        reasons.append("comparison mode not aggregate-only-preregistered")
    if plan["cohort_registry_id"] != cohort_registry["cohort_registry_id"]:
        reasons.append("cohort registry id mismatch")
    if plan["metric_registry_id"] != metric_registry["metric_registry_id"]:
        reasons.append("metric registry id mismatch")
    if plan["observation_registry_id"] != observation_registry["observation_registry_id"]:
        reasons.append("observation registry id mismatch")
    if not plan["aggregate_only"]:
        reasons.append("aggregate-only disabled")
    if not plan["holdout_frozen"]:
        reasons.append("holdout not frozen")
    if plan["missing_evidence_disposition"] != "hold":
        reasons.append("missing evidence does not HOLD")
    if plan["execution_failure_disposition"] != "count-as-unresolved":
        reasons.append("execution failure handling mismatch")
    if not plan["comparison_direction_predeclared"]:
        reasons.append("comparison direction not predeclared")
    if not plan["limited_comparison_authority_granted"]:
        reasons.append("limited comparison authority missing")
    if plan["repository_mutation_authority_granted"]:
        reasons.append("repository mutation authority granted")
    if plan["git_authority_granted"]:
        reasons.append("Git authority granted")
    if plan["correctness_claimed"]:
        reasons.append("correctness claimed")

    if set(cohort_map) != set(required_cohorts):
        reasons.append("cohort evidence incomplete")
    if len(plan["ablation_cohort_ids"]) != policy["required_ablation_count"]:
        reasons.append("ablation cohort count mismatch")
    expected_pairs = {
        (plan["baseline_cohort_id"], plan["codeai_cohort_id"]),
        *((plan["codeai_cohort_id"], cohort_id) for cohort_id in plan["ablation_cohort_ids"]),
    }
    if {tuple(pair) for pair in plan["comparison_pairs"]} != expected_pairs:
        reasons.append("comparison pairs mismatch")

    target_counts: list[int] = []
    role_counts = {"baseline": 0, "codeai": 0, "ablation": 0}
    for cohort_id in required_cohorts:
        cohort = cohort_map.get(cohort_id)
        if cohort is None:
            continue
        role = cohort["role"]
        if role not in role_counts:
            reasons.append(f"unknown cohort role: {cohort_id}")
        else:
            role_counts[role] += 1
        target_counts.append(cohort["target_sample_count"])
        if cohort["target_sample_count"] == 0:
            reasons.append(f"zero target sample count: {cohort_id}")
        if not cohort["frozen_before_observation"]:
            reasons.append(f"cohort not frozen: {cohort_id}")
        if not cohort["aggregate_only"]:
            reasons.append(f"cohort not aggregate-only: {cohort_id}")
        for field in (
            "gold_access_granted", "raw_test_name_access_granted",
            "raw_log_access_granted", "candidate_feedback_enabled",
            "repair_memory_feedback_enabled",
        ):
            if cohort[field]:
                reasons.append(f"cohort leakage or feedback: {cohort_id}:{field}")
    if role_counts != {
        "baseline": 1,
        "codeai": 1,
        "ablation": policy["required_ablation_count"],
    }:
        reasons.append("cohort roles incomplete")
    if target_counts and len(set(target_counts)) != 1:
        reasons.append("cohort target imbalance")

    if set(metric_map) != set(required_metrics):
        reasons.append("required metric missing")
    primary_count = 0
    for metric_id in required_metrics:
        metric = metric_map.get(metric_id)
        if metric is None:
            continue
        primary_count += int(metric["primary"])
        if not metric["predeclared"]:
            reasons.append(f"metric not predeclared: {metric_id}")
        if metric["direction"] not in {"higher-is-better", "lower-is-better"}:
            reasons.append(f"metric direction invalid: {metric_id}")
        if metric["missing_evidence_disposition"] != "hold":
            reasons.append(f"metric missing-evidence handling invalid: {metric_id}")
        if metric["execution_failure_disposition"] != "count-as-unresolved":
            reasons.append(f"metric execution-failure handling invalid: {metric_id}")
    if primary_count != policy["required_primary_metric_count"]:
        reasons.append("primary metric count mismatch")

    if set(observation_map) != set(required_cohorts):
        reasons.append("observation registry incomplete")
    measured_counts: list[int] = []
    pending_ids: list[str] = []
    for cohort_id in required_cohorts:
        observation = observation_map.get(cohort_id)
        if observation is None:
            continue
        for field in ("raw_gold_included", "raw_test_names_included", "raw_logs_included"):
            if observation[field]:
                reasons.append(f"observation leakage: {cohort_id}:{field}")
        if observation["evidence_state"] == "measured":
            measured_counts.append(observation["sample_count"])
            if observation["sample_count"] == 0:
                reasons.append(f"measured cohort has zero samples: {cohort_id}")
            if not observation["metric_values_complete"]:
                reasons.append(f"measured cohort metrics incomplete: {cohort_id}")
            if observation["execution_valid_count"] > observation["sample_count"]:
                reasons.append(f"execution-valid count exceeds sample count: {cohort_id}")
            if observation["resolved_count"] > observation["sample_count"]:
                reasons.append(f"resolved count exceeds sample count: {cohort_id}")
        elif observation["evidence_state"] == "pending":
            pending_ids.append(cohort_id)
            aggregate_fields = (
                "sample_count", "execution_valid_count", "resolved_count",
                "fail_to_pass_success_count", "fail_to_pass_failure_count",
                "pass_to_pass_success_count", "pass_to_pass_failure_count",
                "error_count",
            )
            if any(observation[field] != 0 for field in aggregate_fields):
                reasons.append(f"pending observation carries aggregate values: {cohort_id}")
            if observation["metric_values_complete"]:
                reasons.append(f"pending observation claims complete metrics: {cohort_id}")
        else:
            reasons.append(f"unknown observation state: {cohort_id}")

    codeai_observation = observation_map.get(plan["codeai_cohort_id"])
    if codeai_observation is None:
        reasons.append("CodeAI predecessor observation missing")
    else:
        if codeai_observation["evidence_state"] != "measured":
            reasons.append("CodeAI predecessor observation not measured")
        if codeai_observation["source_kind"] != "admitted-ingestion-receipt":
            reasons.append("CodeAI predecessor source kind mismatch")
        if codeai_observation["source_receipt_digest"] != request["predecessor_receipt_digest"]:
            reasons.append("CodeAI predecessor observation receipt mismatch")
        expected_counts = {
            "sample_count": 1,
            "execution_valid_count": 1,
            "resolved_count": int(predecessor_manifest["resolved"]),
            "fail_to_pass_success_count": predecessor_manifest["fail_to_pass_success_count"],
            "fail_to_pass_failure_count": predecessor_manifest["fail_to_pass_failure_count"],
            "pass_to_pass_success_count": predecessor_manifest["pass_to_pass_success_count"],
            "pass_to_pass_failure_count": predecessor_manifest["pass_to_pass_failure_count"],
            "error_count": 0,
        }
        for field, expected in expected_counts.items():
            if codeai_observation[field] != expected:
                reasons.append(f"CodeAI predecessor aggregate mismatch: {field}")

    if request["comparison_phase"] == "preregistration":
        expected_pending = set(required_cohorts) - {plan["codeai_cohort_id"]}
        if set(pending_ids) != expected_pending:
            reasons.append("preregistration pending cohort set mismatch")
    elif request["comparison_phase"] == "comparison-execution":
        if pending_ids:
            reasons.append("comparison evidence insufficient")
        if measured_counts and len(set(measured_counts)) != 1:
            reasons.append("measured cohort imbalance")
    else:
        reasons.append("unsupported comparison phase")

    if reasons:
        return ComparisonResult(STATUS_HELD, tuple(sorted(set(reasons))), None, None)

    comparison_completed = request["comparison_phase"] == "comparison-execution"
    pack = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "decision": DECISION_ADMITTED,
        **{field: request[field] for field in BINDING_FIELDS},
        "comparison_id": plan["comparison_id"],
        "comparison_phase": request["comparison_phase"],
        "cohort_registry_digest": cohort_registry[COHORT_DIGEST_FIELD],
        "metric_registry_digest": metric_registry[METRIC_DIGEST_FIELD],
        "observation_registry_digest": observation_registry[OBSERVATION_DIGEST_FIELD],
        "cohort_ids": list(required_cohorts),
        "metric_ids": list(required_metrics),
        "pending_cohort_ids": sorted(pending_ids),
        "preregistration_completed": True,
        "performance_comparison_completed": comparison_completed,
        "limited_aggregate_comparison_authority_granted": True,
        "raw_gold_visible": False,
        "raw_test_names_visible": False,
        "raw_logs_visible": False,
        "candidate_generation_feedback_enabled": False,
        "repair_memory_feedback_enabled": False,
        "repository_mutation_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "performance_claimed": False,
    }, PACK_DIGEST_FIELD)
    receipt = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "decision": DECISION_ADMITTED,
        "comparison_pack_digest": pack[PACK_DIGEST_FIELD],
        "predecessor_manifest_digest": request["predecessor_manifest_digest"],
        "predecessor_ingestion_pack_digest": request["predecessor_ingestion_pack_digest"],
        "predecessor_receipt_digest": request["predecessor_receipt_digest"],
        "comparison_phase": request["comparison_phase"],
        "preregistration_completed": True,
        "performance_comparison_completed": comparison_completed,
        "pending_cohort_count": len(pending_ids),
        "limited_aggregate_comparison_authority_granted": True,
        "repository_mutation_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "performance_claimed": False,
    }, RECEIPT_DIGEST_FIELD)
    return ComparisonResult(STATUS_ADMITTED, (), pack, receipt)
