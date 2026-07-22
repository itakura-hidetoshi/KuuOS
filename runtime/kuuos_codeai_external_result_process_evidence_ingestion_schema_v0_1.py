from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI External Result and Process-Evidence Ingestion v0.1"

STATUS_ADMITTED = "admitted"
STATUS_HELD = "held"
STATUS_BLOCKED = "blocked"
DECISION_ADMITTED = "external_result_process_evidence_ingestion_admitted"
DECISION_HELD = "external_result_process_evidence_ingestion_held"

REQUEST_DIGEST_FIELD = "external_result_ingestion_request_digest"
POLICY_DIGEST_FIELD = "external_result_ingestion_policy_digest"
PLAN_DIGEST_FIELD = "external_result_ingestion_plan_digest"
RESULT_DIGEST_FIELD = "external_result_evidence_digest"
PROCESS_DIGEST_FIELD = "process_evidence_digest"
PACK_DIGEST_FIELD = "external_result_ingestion_pack_digest"
RECEIPT_DIGEST_FIELD = "external_result_ingestion_receipt_digest"

PREDECESSOR_MANIFEST_FIELDS = {
    "correctness_claimed", "decision", "evaluation_completed",
    "future_harness_execution_authority_granted", "git_authority_granted",
    "gold_access_granted", "instance_id", "instance_log_digest",
    "model_name_or_path", "patch_applied", "prediction_digest",
    "profile_version", "receipt_digest", "report_digest",
    "repository_mutation_authority_granted", "resolved", "test_output_digest",
}

BINDING_FIELDS = (
    "controller_repository", "controller_source_commit_sha",
    "predecessor_manifest_digest", "predecessor_execution_pack_digest",
    "predecessor_receipt_digest", "predecessor_workflow_run_id",
    "predecessor_artifact_id", "predecessor_artifact_digest",
    "instance_id", "prediction_digest", "external_observation_digest",
    "ingestion_contract_digest",
)

REQUEST_FIELDS = {
    "schema_version", "profile_version", "request_id", "request_revision",
    *BINDING_FIELDS, "request_created_epoch", "claims_raw_gold_access",
    "claims_raw_test_name_access", "claims_candidate_generation_feedback",
    "claims_repair_memory_feedback", "claims_repository_mutation_authority",
    "claims_git_authority", "claims_correctness", REQUEST_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "schema_version", "profile_version",
    *("expected_" + field for field in BINDING_FIELDS),
    "evaluation_epoch", "maximum_request_age", "maximum_result_age",
    "maximum_process_evidence_age", "required_result_count",
    "required_process_evidence_count", "require_exact_binding",
    "require_predecessor_admitted", "require_completed_workflow",
    "require_unexpired_artifact", "require_aggregate_only_ingestion",
    "require_patch_applied", "require_evaluation_completed",
    "require_report_and_logs", "allow_resolved_or_unresolved",
    "allow_raw_gold_access", "allow_raw_test_names", "allow_raw_logs_committed",
    "allow_candidate_generation_feedback", "allow_repair_memory_feedback",
    "allow_kernel_harness_execution", "allow_repository_mutation",
    "allow_git_authority", "allow_correctness_claim", POLICY_DIGEST_FIELD,
}
PLAN_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS, "ingestion_id",
    "ingestion_mode", "result_count", "process_evidence_count",
    "source_artifact_retained_externally", "raw_artifact_committed",
    "raw_test_names_ingested", "raw_logs_ingested",
    "candidate_generation_feedback_enabled", "repair_memory_feedback_enabled",
    "comparison_authority_granted", "plan_created_epoch", PLAN_DIGEST_FIELD,
}
RESULT_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS,
    "report_digest", "result_created_epoch", "patch_exists", "patch_applied",
    "evaluation_completed", "resolved", "fail_to_pass_success_count",
    "fail_to_pass_failure_count", "pass_to_pass_success_count",
    "pass_to_pass_failure_count", "error_count", "raw_test_names_included",
    "gold_material_included", RESULT_DIGEST_FIELD,
}
PROCESS_FIELDS = {
    "schema_version", "profile_version", *BINDING_FIELDS,
    "test_output_digest", "instance_log_digest", "process_created_epoch",
    "workflow_completed", "artifact_expired", "docker_used", "image_available",
    "container_started", "patch_applied_cleanly", "evaluation_completed",
    "git_diff_stable", "container_removed", "image_removed", "report_observed",
    "logs_observed", "network_used_by_external_harness",
    "harness_executed_by_kernel", "raw_logs_committed", "repository_mutated",
    "git_authority", "correctness_claimed", PROCESS_DIGEST_FIELD,
}

class BlockedInput(ValueError):
    pass

@dataclass(frozen=True)
class IngestionResult:
    status: str
    reasons: tuple[str, ...]
    ingestion_pack: dict[str, Any] | None
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
