from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_baseline_versus_codeai_ablation_comparison_schema_v0_1 import *

DIGEST_BINDINGS = {
    "predecessor_manifest_digest", "predecessor_ingestion_pack_digest",
    "predecessor_receipt_digest", "sample_binding_digest",
    "holdout_partition_digest", "comparison_contract_digest",
}

def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise BlockedInput(f"{label} must be a nonempty list")
    if not all(isinstance(item, str) and item for item in value):
        raise BlockedInput(f"{label} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise BlockedInput(f"{label} must contain unique values")
    return value

def _require_pair_list(value: Any, label: str) -> list[list[str]]:
    if not isinstance(value, list) or not value:
        raise BlockedInput(f"{label} must be a nonempty list")
    normalized: list[list[str]] = []
    for index, pair in enumerate(value):
        if not isinstance(pair, list) or len(pair) != 2:
            raise BlockedInput(f"{label}[{index}] must be a two-element list")
        if not all(isinstance(item, str) and item for item in pair):
            raise BlockedInput(f"{label}[{index}] must contain nonempty strings")
        if pair[0] == pair[1]:
            raise BlockedInput(f"{label}[{index}] must compare distinct cohorts")
        normalized.append(pair)
    if len({tuple(pair) for pair in normalized}) != len(normalized):
        raise BlockedInput(f"{label} must contain unique pairs")
    return normalized

def validate_structure(
    *,
    request: dict[str, Any],
    policy: dict[str, Any],
    predecessor_manifest: dict[str, Any],
    plan: dict[str, Any],
    cohort_registry: dict[str, Any],
    metric_registry: dict[str, Any],
    observation_registry: dict[str, Any],
) -> None:
    require_exact_fields(request, REQUEST_FIELDS, "request")
    require_exact_fields(policy, POLICY_FIELDS, "policy")
    require_exact_fields(predecessor_manifest, PREDECESSOR_MANIFEST_FIELDS, "predecessor_manifest")
    require_exact_fields(plan, PLAN_FIELDS, "plan")
    require_exact_fields(cohort_registry, COHORT_REGISTRY_FIELDS, "cohort_registry")
    require_exact_fields(metric_registry, METRIC_REGISTRY_FIELDS, "metric_registry")
    require_exact_fields(observation_registry, OBSERVATION_REGISTRY_FIELDS, "observation_registry")

    for label, value, digest_field in (
        ("request", request, REQUEST_DIGEST_FIELD),
        ("policy", policy, POLICY_DIGEST_FIELD),
        ("plan", plan, PLAN_DIGEST_FIELD),
        ("cohort_registry", cohort_registry, COHORT_DIGEST_FIELD),
        ("metric_registry", metric_registry, METRIC_DIGEST_FIELD),
        ("observation_registry", observation_registry, OBSERVATION_DIGEST_FIELD),
    ):
        require_profile(value, label)
        validate_seal(value, digest_field)

    for field in BINDING_FIELDS:
        if field == "controller_source_commit_sha":
            require_git_sha(request[field], field)
        elif field in DIGEST_BINDINGS:
            require_sha256(request[field], field)
        else:
            require_nonempty_string(request[field], field)

    for value, fields in (
        (request, [
            "claims_raw_gold_access", "claims_raw_test_name_access",
            "claims_raw_log_access", "claims_candidate_generation_feedback",
            "claims_repair_memory_feedback", "claims_repository_mutation_authority",
            "claims_git_authority", "claims_correctness",
        ]),
        (policy, [
            "require_exact_binding", "require_predecessor_admitted",
            "require_predecessor_execution_valid", "require_aggregate_only",
            "require_frozen_holdout", "require_equal_target_sample_count",
            "require_balanced_measured_cohorts",
            "require_execution_failure_as_unresolved",
            "require_missing_evidence_hold",
            "allow_preregistration_with_pending_observations",
            "allow_limited_comparison_authority", "allow_raw_gold_access",
            "allow_raw_test_names", "allow_raw_logs", "allow_candidate_feedback",
            "allow_repair_memory_feedback", "allow_repository_mutation",
            "allow_git_authority", "allow_correctness_claim",
        ]),
        (plan, [
            "aggregate_only", "holdout_frozen",
            "comparison_direction_predeclared",
            "limited_comparison_authority_granted",
            "repository_mutation_authority_granted",
            "git_authority_granted", "correctness_claimed",
        ]),
    ):
        for field in fields:
            require_bool(value[field], field)

    for field in (
        "evaluation_epoch", "maximum_request_age", "maximum_registry_age",
        "required_ablation_count", "required_primary_metric_count",
    ):
        require_nonnegative_int(policy[field], field)
    require_nonnegative_int(request["request_created_epoch"], "request_created_epoch")
    require_nonnegative_int(plan["plan_created_epoch"], "plan_created_epoch")

    _require_string_list(policy["required_cohort_ids"], "required_cohort_ids")
    _require_string_list(policy["required_metric_ids"], "required_metric_ids")
    _require_string_list(plan["ablation_cohort_ids"], "ablation_cohort_ids")
    _require_pair_list(plan["comparison_pairs"], "comparison_pairs")

    cohorts = cohort_registry["cohorts"]
    if not isinstance(cohorts, list) or not cohorts:
        raise BlockedInput("cohorts must be a nonempty list")
    cohort_ids: list[str] = []
    for index, cohort in enumerate(cohorts):
        if not isinstance(cohort, dict):
            raise BlockedInput(f"cohort[{index}] must be mapping")
        require_exact_fields(cohort, COHORT_FIELDS, f"cohort[{index}]")
        for field in (
            "frozen_before_observation", "aggregate_only",
            "gold_access_granted", "raw_test_name_access_granted",
            "raw_log_access_granted", "candidate_feedback_enabled",
            "repair_memory_feedback_enabled",
        ):
            require_bool(cohort[field], f"cohort[{index}].{field}")
        require_nonnegative_int(cohort["target_sample_count"], f"cohort[{index}].target_sample_count")
        require_sha256(cohort["sample_binding_digest"], f"cohort[{index}].sample_binding_digest")
        require_sha256(cohort["holdout_partition_digest"], f"cohort[{index}].holdout_partition_digest")
        for field in ("cohort_id", "role", "system_variant"):
            require_nonempty_string(cohort[field], f"cohort[{index}].{field}")
        cohort_ids.append(cohort["cohort_id"])
    if len(cohort_ids) != len(set(cohort_ids)):
        raise BlockedInput("duplicate cohort_id")

    metrics = metric_registry["metrics"]
    if not isinstance(metrics, list) or not metrics:
        raise BlockedInput("metrics must be a nonempty list")
    metric_ids: list[str] = []
    for index, metric in enumerate(metrics):
        if not isinstance(metric, dict):
            raise BlockedInput(f"metric[{index}] must be mapping")
        require_exact_fields(metric, METRIC_FIELDS, f"metric[{index}]")
        for field in ("primary", "predeclared"):
            require_bool(metric[field], f"metric[{index}].{field}")
        for field in (
            "metric_id", "metric_kind", "numerator_field", "denominator_field",
            "direction", "missing_evidence_disposition",
            "execution_failure_disposition",
        ):
            require_nonempty_string(metric[field], f"metric[{index}].{field}")
        metric_ids.append(metric["metric_id"])
    if len(metric_ids) != len(set(metric_ids)):
        raise BlockedInput("duplicate metric_id")

    observations = observation_registry["observations"]
    if not isinstance(observations, list) or not observations:
        raise BlockedInput("observations must be a nonempty list")
    observation_ids: list[str] = []
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            raise BlockedInput(f"observation[{index}] must be mapping")
        require_exact_fields(observation, OBSERVATION_FIELDS, f"observation[{index}]")
        for field in (
            "metric_values_complete", "raw_gold_included",
            "raw_test_names_included", "raw_logs_included",
        ):
            require_bool(observation[field], f"observation[{index}].{field}")
        for field in (
            "sample_count", "execution_valid_count", "resolved_count",
            "fail_to_pass_success_count", "fail_to_pass_failure_count",
            "pass_to_pass_success_count", "pass_to_pass_failure_count",
            "error_count", "observation_created_epoch",
        ):
            require_nonnegative_int(observation[field], f"observation[{index}].{field}")
        require_sha256(observation["source_receipt_digest"], f"observation[{index}].source_receipt_digest")
        require_sha256(observation["sample_binding_digest"], f"observation[{index}].sample_binding_digest")
        require_sha256(observation["holdout_partition_digest"], f"observation[{index}].holdout_partition_digest")
        for field in ("cohort_id", "evidence_state", "source_kind"):
            require_nonempty_string(observation[field], f"observation[{index}].{field}")
        observation_ids.append(observation["cohort_id"])
    if len(observation_ids) != len(set(observation_ids)):
        raise BlockedInput("duplicate observation cohort_id")


def exact_binding(request: dict[str, Any], policy: dict[str, Any], *bound: dict[str, Any]) -> bool:
    for field in BINDING_FIELDS:
        expected = policy["expected_" + field]
        if request[field] != expected:
            return False
        for item in bound:
            if item[field] != expected:
                return False
    return True

def nested_binding_ok(
    request: dict[str, Any],
    cohort_registry: dict[str, Any],
    observation_registry: dict[str, Any],
) -> bool:
    for cohort in cohort_registry["cohorts"]:
        if cohort["sample_binding_digest"] != request["sample_binding_digest"]:
            return False
        if cohort["holdout_partition_digest"] != request["holdout_partition_digest"]:
            return False
    for observation in observation_registry["observations"]:
        if observation["sample_binding_digest"] != request["sample_binding_digest"]:
            return False
        if observation["holdout_partition_digest"] != request["holdout_partition_digest"]:
            return False
    return True

def freshness_ok(
    request: dict[str, Any],
    policy: dict[str, Any],
    plan: dict[str, Any],
    cohort_registry: dict[str, Any],
    metric_registry: dict[str, Any],
    observation_registry: dict[str, Any],
) -> bool:
    epoch = policy["evaluation_epoch"]
    if not 0 <= epoch - request["request_created_epoch"] <= policy["maximum_request_age"]:
        return False
    for value, field in (
        (plan, "plan_created_epoch"),
        (cohort_registry, "registry_created_epoch"),
        (metric_registry, "registry_created_epoch"),
        (observation_registry, "registry_created_epoch"),
    ):
        if not 0 <= epoch - value[field] <= policy["maximum_registry_age"]:
            return False
    for observation in observation_registry["observations"]:
        if not 0 <= epoch - observation["observation_created_epoch"] <= policy["maximum_registry_age"]:
            return False
    return True
