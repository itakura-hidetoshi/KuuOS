from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "Baseline-versus-CodeAI and Ablation Comparison v0.1"

STATUS_ADMITTED = "admitted"
STATUS_HELD = "held"
STATUS_BLOCKED = "blocked"
DECISION_ADMITTED = "baseline_versus_codeai_ablation_comparison_admitted"
DECISION_HELD = "baseline_versus_codeai_ablation_comparison_held"

REQUEST_DIGEST_FIELD = "comparison_request_digest"
POLICY_DIGEST_FIELD = "comparison_policy_digest"
PLAN_DIGEST_FIELD = "comparison_plan_digest"
COHORT_DIGEST_FIELD = "cohort_registry_digest"
METRIC_DIGEST_FIELD = "metric_registry_digest"
OBSERVATION_DIGEST_FIELD = "observation_registry_digest"
PACK_DIGEST_FIELD = "comparison_pack_digest"
RECEIPT_DIGEST_FIELD = "comparison_receipt_digest"

PREDECESSOR_MANIFEST_FIELDS = {
    "candidate_generation_feedback_enabled", "comparison_authority_granted",
    "correctness_claimed", "decision", "execution_valid",
    "external_observation_digest", "fail_to_pass_failure_count",
    "fail_to_pass_success_count", "git_authority_granted",
    "ingestion_pack_digest", "instance_id", "outcome_disposition",
    "pass_to_pass_failure_count", "pass_to_pass_success_count",
    "predecessor_artifact_digest", "predecessor_artifact_id",
    "predecessor_workflow_run_id", "prediction_digest", "profile_version",
    "raw_gold_ingested", "raw_logs_committed", "raw_test_names_ingested",
    "receipt_digest", "repair_memory_feedback_enabled",
    "repository_mutation_authority_granted", "resolved",
}

BINDING_FIELDS = (
    "controller_repository", "controller_source_commit_sha",
    "predecessor_manifest_digest", "predecessor_ingestion_pack_digest",
    "predecessor_receipt_digest", "sample_binding_digest",
    "holdout_partition_digest", "comparison_contract_digest",
)

REQUEST_FIELDS = {
    "schema_version", "profile_version", "request_id", "request_revision",
    *BINDING_FIELDS, "request_created_epoch", "comparison_phase",
    "claims_raw_gold_access", "claims_raw_test_name_access",
    "claims_raw_log_access", "claims_candidate_generation_feedback",
    "claims_repair_memory_feedback", "claims_repository_mutation_authority",
    "claims_git_authority", "claims_correctness",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "schema_version", "profile_version",
    *("expected_" + field for field in BINDING_FIELDS),
    "evaluation_epoch", "maximum_request_age", "maximum_registry_age",
    "required_cohort_ids", "required_metric_ids", "required_ablation_count",
    "required_primary_metric_count", "require_exact_binding",
    "require_predecessor_admitted", "require_predecessor_execution_valid",
    "require_aggregate_only", "require_frozen_holdout",
    "require_equal_target_sample_count", "require_balanced_measured_cohorts",
    "require_execution_failure_as_unresolved", "require_missing_evidence_hold",
    "allow_preregistration_with_pending_observations",
    "allow_limited_comparison_authority", "allow_raw_gold_access",
    "allow_raw_test_names", "allow_raw_logs", "allow_candidate_feedback",
    "allow_repair_memory_feedback", "allow_repository_mutation",
    "allow_git_authority", "allow_correctness_claim",
    POLICY_DIGEST_FIELD,
}

PLAN_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS,
    "comparison_id", "comparison_phase", "comparison_mode",
    "cohort_registry_id", "metric_registry_id", "observation_registry_id",
    "baseline_cohort_id", "codeai_cohort_id", "ablation_cohort_ids",
    "comparison_pairs", "aggregate_only", "holdout_frozen",
    "missing_evidence_disposition", "execution_failure_disposition",
    "comparison_direction_predeclared", "limited_comparison_authority_granted",
    "repository_mutation_authority_granted", "git_authority_granted",
    "correctness_claimed", "plan_created_epoch", PLAN_DIGEST_FIELD,
}

COHORT_REGISTRY_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS,
    "cohort_registry_id", "registry_created_epoch", "cohorts",
    COHORT_DIGEST_FIELD,
}

COHORT_FIELDS = {
    "cohort_id", "role", "system_variant", "target_sample_count",
    "sample_binding_digest", "holdout_partition_digest",
    "frozen_before_observation", "aggregate_only",
    "gold_access_granted", "raw_test_name_access_granted",
    "raw_log_access_granted", "candidate_feedback_enabled",
    "repair_memory_feedback_enabled",
}

METRIC_REGISTRY_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS,
    "metric_registry_id", "registry_created_epoch", "metrics",
    METRIC_DIGEST_FIELD,
}

METRIC_FIELDS = {
    "metric_id", "metric_kind", "numerator_field", "denominator_field",
    "direction", "primary", "missing_evidence_disposition",
    "execution_failure_disposition", "predeclared",
}

OBSERVATION_REGISTRY_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS,
    "observation_registry_id", "registry_created_epoch",
    "observation_mode", "observations", OBSERVATION_DIGEST_FIELD,
}

OBSERVATION_FIELDS = {
    "cohort_id", "evidence_state", "source_kind", "source_receipt_digest",
    "sample_binding_digest", "holdout_partition_digest",
    "sample_count", "execution_valid_count", "resolved_count",
    "fail_to_pass_success_count", "fail_to_pass_failure_count",
    "pass_to_pass_success_count", "pass_to_pass_failure_count",
    "error_count", "metric_values_complete", "raw_gold_included",
    "raw_test_names_included", "raw_logs_included",
    "observation_created_epoch",
}

class BlockedInput(ValueError):
    pass

@dataclass(frozen=True)
class ComparisonResult:
    status: str
    reasons: tuple[str, ...]
    comparison_pack: dict[str, Any] | None
    receipt: dict[str, Any] | None

def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()

def seal(value: dict[str, Any], digest_field: str) -> dict[str, Any]:
    if digest_field in value:
        raise ValueError(f"{digest_field} already present")
    sealed = dict(value)
    sealed[digest_field] = canonical_digest(value)
    return sealed

def validate_seal(value: dict[str, Any], digest_field: str) -> None:
    observed = value.get(digest_field)
    require_sha256(observed, digest_field)
    material = {k: v for k, v in value.items() if k != digest_field}
    if canonical_digest(material) != observed:
        raise BlockedInput(f"digest mismatch: {digest_field}")

def require_exact_fields(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise BlockedInput(
            f"{label} fields mismatch; missing={sorted(expected-actual)}; extra={sorted(actual-expected)}"
        )

def require_profile(value: dict[str, Any], label: str) -> None:
    if value.get("schema_version") != SCHEMA_VERSION:
        raise BlockedInput(f"{label} schema mismatch")
    if value.get("profile_version") != PROFILE_VERSION:
        raise BlockedInput(f"{label} profile mismatch")

def require_sha256(value: Any, label: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise BlockedInput(f"{label} must be sha256")
    try:
        int(value, 16)
    except ValueError as exc:
        raise BlockedInput(f"{label} must be hexadecimal") from exc

def require_git_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or len(value) != 40:
        raise BlockedInput(f"{label} must be 40-char git sha")
    try:
        int(value, 16)
    except ValueError as exc:
        raise BlockedInput(f"{label} must be hexadecimal") from exc

def require_bool(value: Any, label: str) -> None:
    if not isinstance(value, bool):
        raise BlockedInput(f"{label} must be bool")

def require_nonnegative_int(value: Any, label: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise BlockedInput(f"{label} must be nonnegative int")

def require_nonempty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise BlockedInput(f"{label} must be nonempty string")
