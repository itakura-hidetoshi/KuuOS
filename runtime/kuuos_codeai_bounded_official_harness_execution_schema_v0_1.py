from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Bounded Official Harness Execution v0.1"

STATUS_ADMITTED = "admitted"
STATUS_HELD = "held"
STATUS_BLOCKED = "blocked"
DECISION_ADMITTED = "bounded_official_harness_execution_admitted"
DECISION_HELD = "bounded_official_harness_execution_held"

REQUEST_DIGEST_FIELD = "bounded_execution_request_digest"
POLICY_DIGEST_FIELD = "bounded_execution_policy_digest"
PLAN_DIGEST_FIELD = "bounded_execution_plan_digest"
PREDICTION_DIGEST_FIELD = "bounded_prediction_digest"
OBSERVATION_DIGEST_FIELD = "bounded_execution_observation_digest"
PACK_DIGEST_FIELD = "bounded_execution_pack_digest"
RECEIPT_DIGEST_FIELD = "bounded_execution_receipt_digest"

OFFICIAL_PREDICTION_FIELDS = ("instance_id", "model_name_or_path", "model_patch")

REQUEST_FIELDS = {
    "schema_version", "profile_version", "request_id", "request_revision",
    "controller_repository", "controller_source_commit_sha",
    "predecessor_manifest_digest", "predecessor_smoke_pack_digest",
    "predecessor_smoke_receipt_digest", "predecessor_external_artifact_digest",
    "dataset_name", "dataset_revision", "dataset_split", "dataset_artifact_sha256",
    "harness_repository", "harness_commit_sha", "instance_id", "base_commit_sha",
    "prediction_digest", "execution_contract_digest", "request_created_epoch",
    "claims_gold_access", "claims_kernel_harness_execution",
    "claims_repository_mutation_authority", "claims_git_authority",
    "claims_correctness", REQUEST_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "schema_version", "profile_version",
    "expected_controller_repository", "expected_controller_source_commit_sha",
    "expected_predecessor_manifest_digest", "expected_predecessor_smoke_pack_digest",
    "expected_predecessor_smoke_receipt_digest",
    "expected_predecessor_external_artifact_digest", "expected_dataset_name",
    "expected_dataset_revision", "expected_dataset_split",
    "expected_dataset_artifact_sha256", "expected_harness_repository",
    "expected_harness_commit_sha", "expected_instance_id", "expected_base_commit_sha",
    "expected_prediction_digest", "expected_execution_contract_digest",
    "evaluation_epoch", "maximum_request_age", "maximum_observation_age",
    "required_sample_count", "maximum_workers", "timeout_seconds",
    "require_exact_binding", "require_predecessor_smoke_admitted",
    "require_frozen_sample", "require_frozen_prediction",
    "require_official_prediction_shape", "require_non_gold_prediction",
    "require_patch_applied", "require_evaluation_completed",
    "require_report_observed", "require_logs_observed",
    "allow_resolved_or_unresolved", "allow_kernel_harness_execution",
    "allow_gold_access", "allow_repository_mutation", "allow_git_authority",
    "allow_correctness_claim", POLICY_DIGEST_FIELD,
}
PLAN_FIELDS = {
    "schema_version", "profile_version", "controller_repository",
    "controller_source_commit_sha", "predecessor_manifest_digest",
    "predecessor_smoke_pack_digest", "predecessor_smoke_receipt_digest",
    "predecessor_external_artifact_digest", "dataset_name", "dataset_revision",
    "dataset_split", "dataset_artifact_sha256", "harness_repository",
    "harness_commit_sha", "instance_id", "base_commit_sha", "prediction_digest",
    "execution_contract_digest", "run_id", "prediction_file_name",
    "prediction_file_digest", "sample_count", "maximum_workers",
    "timeout_seconds", "cache_level", "clean_images", "sample_frozen",
    "prediction_frozen", "official_prediction_shape", "non_gold_prediction",
    "gold_available_to_solver", "plan_created_epoch", PLAN_DIGEST_FIELD,
}
PREDICTION_FIELDS = {
    "schema_version", "profile_version", "instance_id", "base_commit_sha",
    "model_name_or_path", "model_patch", "changed_paths", "source_kind",
    "source_locator", "source_digest", "gold_derived", "gold_accessed",
    "candidate_receipt_digest", "prediction_created_epoch",
    "claims_resolved", "claims_correctness", PREDICTION_DIGEST_FIELD,
}
OBSERVATION_FIELDS = {
    "schema_version", "profile_version", "controller_repository",
    "controller_source_commit_sha", "predecessor_manifest_digest",
    "predecessor_smoke_pack_digest", "predecessor_smoke_receipt_digest",
    "predecessor_external_artifact_digest", "dataset_name", "dataset_revision",
    "dataset_split", "dataset_artifact_sha256", "harness_repository",
    "harness_commit_sha", "instance_id", "base_commit_sha", "prediction_digest",
    "execution_contract_digest", "observer_id", "run_id",
    "observation_created_epoch", "external_harness_execution_observed",
    "harness_execution_performed_by_kernel", "network_used_by_external_harness",
    "docker_used", "image_available", "container_started", "patch_applied",
    "evaluation_completed", "resolved", "report_observed", "logs_observed",
    "report_digest", "test_output_digest", "instance_log_digest",
    "gold_exposed_to_solver", "gold_used_for_candidate_generation",
    "gold_used_for_repair_memory", "repository_mutated", "git_authority",
    "correctness_claimed", OBSERVATION_DIGEST_FIELD,
}

class BlockedInput(ValueError):
    pass

@dataclass(frozen=True)
class ExecutionResult:
    status: str
    reasons: tuple[str, ...]
    execution_pack: dict[str, Any] | None
    receipt: dict[str, Any] | None

def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

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
    if not isinstance(observed, str) or len(observed) != 64:
        raise BlockedInput(f"invalid {digest_field}")
    material = {k: v for k, v in value.items() if k != digest_field}
    if canonical_digest(material) != observed:
        raise BlockedInput(f"digest mismatch: {digest_field}")

def require_exact_fields(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise BlockedInput(f"{label} fields mismatch; missing={missing}; extra={extra}")

def require_profile(value: dict[str, Any], label: str) -> None:
    if value.get("schema_version") != SCHEMA_VERSION:
        raise BlockedInput(f"{label} schema mismatch")
    if value.get("profile_version") != PROFILE_VERSION:
        raise BlockedInput(f"{label} profile mismatch")

def require_sha256(value: str, label: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise BlockedInput(f"{label} must be sha256")
    try:
        int(value, 16)
    except ValueError as exc:
        raise BlockedInput(f"{label} must be hexadecimal") from exc

def require_git_sha(value: str, label: str) -> None:
    if not isinstance(value, str) or len(value) != 40:
        raise BlockedInput(f"{label} must be 40-char git sha")
    try:
        int(value, 16)
    except ValueError as exc:
        raise BlockedInput(f"{label} must be hexadecimal") from exc

def derive_changed_paths(model_patch: str) -> list[str]:
    paths: list[str] = []
    for line in model_patch.splitlines():
        if line.startswith("diff --git a/"):
            parts = line.split()
            if len(parts) != 4 or not parts[2].startswith("a/"):
                raise BlockedInput("malformed diff header")
            path = parts[2][2:]
            if not path or path.startswith("/") or ".." in path.split("/"):
                raise BlockedInput("unsafe changed path")
            paths.append(path)
    if not paths:
        raise BlockedInput("model_patch has no diff header")
    if len(paths) != len(set(paths)):
        raise BlockedInput("duplicate changed path")
    return paths

def official_prediction(prediction: dict[str, Any]) -> dict[str, str]:
    return {field: prediction[field] for field in OFFICIAL_PREDICTION_FIELDS}
