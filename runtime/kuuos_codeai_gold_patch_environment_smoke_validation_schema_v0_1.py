from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_gold_patch_environment_smoke_validation_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Gold-Patch Environment Smoke Validation v0.1"
PREDECESSOR_PROFILE_VERSION = "CodeAI External Corpus Acquisition and Freeze Receipt v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DECISION_ADMIT = "gold_patch_environment_smoke_admitted"
DECISION_HOLD = "gold_patch_environment_smoke_held"
MODE = "evaluator_only_gold_patch_environment_smoke"

REQUEST_DIGEST_FIELD = "gold_patch_smoke_request_digest"
POLICY_DIGEST_FIELD = "gold_patch_smoke_policy_digest"
PLAN_DIGEST_FIELD = "gold_patch_smoke_plan_digest"
OBSERVATION_DIGEST_FIELD = "gold_patch_smoke_observation_digest"
PACK_DIGEST_FIELD = "gold_patch_smoke_pack_digest"
RECEIPT_DIGEST_FIELD = "gold_patch_smoke_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,191}$")

BINDING_FIELDS = (
    "controller_repository",
    "controller_source_commit_sha",
    "predecessor_manifest_digest",
    "predecessor_freeze_pack_digest",
    "predecessor_freeze_receipt_digest",
    "dataset_name",
    "dataset_revision",
    "dataset_split",
    "dataset_artifact_sha256",
    "harness_repository",
    "harness_commit_sha",
    "instance_id",
    "smoke_contract_digest",
    "environment_contract_digest",
)

@dataclass(frozen=True)
class GoldPatchEnvironmentSmokeResult:
    status: str
    issues: tuple[str, ...]
    smoke_pack: dict[str, Any] | None
    receipt: dict[str, Any] | None

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})

def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result[field] = digest_without(result, field)
    return result

def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None

def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    item = value.get(field)
    return isinstance(item, str) and SHA256.fullmatch(item) is not None and item == digest_without(value, field)

def nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0

def positive_int(value: Any) -> bool:
    return nonnegative_int(value) and value > 0

def _validate_binding(value: Mapping[str, Any], prefix: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(value.get("controller_repository"), str) or not value["controller_repository"]:
        issues.append(prefix + "_repository_invalid")
    for field in ("controller_source_commit_sha", "harness_commit_sha"):
        item = value.get(field)
        if not isinstance(item, str) or SHA40.fullmatch(item) is None:
            issues.append(prefix + "_sha40_invalid:" + field)
    for field in (
        "predecessor_manifest_digest",
        "predecessor_freeze_pack_digest",
        "predecessor_freeze_receipt_digest",
        "dataset_artifact_sha256",
        "smoke_contract_digest",
        "environment_contract_digest",
    ):
        item = value.get(field)
        if not isinstance(item, str) or SHA256.fullmatch(item) is None:
            issues.append(prefix + "_sha256_invalid:" + field)
    for field in ("dataset_name", "dataset_split", "harness_repository", "instance_id"):
        item = value.get(field)
        if not isinstance(item, str) or IDENTIFIER.fullmatch(item) is None:
            issues.append(prefix + "_identifier_invalid:" + field)
    revision = value.get("dataset_revision")
    if not isinstance(revision, str) or SHA40.fullmatch(revision) is None:
        issues.append(prefix + "_dataset_revision_invalid")
    return issues

def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", "request_id", "request_revision",
        *BINDING_FIELDS, "request_created_epoch", "requested_smoke_runs",
        "claims_solver_gold_access", "claims_candidate_generation_access",
        "claims_repair_memory_access", "claims_repository_mutation_authority",
        "claims_git_authority", "claims_correctness", REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing, extra = required.difference(request), set(request).difference(required)
    if missing: issues.append("request_missing_fields:" + ",".join(sorted(missing)))
    if extra: issues.append("request_extra_fields:" + ",".join(sorted(extra)))
    if issues: return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("request_profile_invalid")
    for field in ("request_id", "request_revision"):
        if not isinstance(request[field], str) or IDENTIFIER.fullmatch(request[field]) is None:
            issues.append("request_identifier_invalid:" + field)
    issues.extend(_validate_binding(request, "request_binding"))
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("request_epoch_invalid")
    if request["requested_smoke_runs"] != 1:
        issues.append("request_smoke_run_count_invalid")
    for field in (
        "claims_solver_gold_access", "claims_candidate_generation_access",
        "claims_repair_memory_access", "claims_repository_mutation_authority",
        "claims_git_authority", "claims_correctness",
    ):
        if not isinstance(request[field], bool):
            issues.append("request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return sorted(set(issues))

def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version",
        *{"expected_" + field for field in BINDING_FIELDS},
        "evaluation_epoch", "maximum_request_age", "maximum_observation_age",
        "required_smoke_runs", "maximum_workers", "timeout_seconds",
        "require_exact_binding", "require_predecessor_frozen",
        "require_plan_preregistered", "require_gold_prediction_mode",
        "require_evaluator_only_gold_access", "require_docker",
        "require_image_available", "require_container_started",
        "require_patch_applied", "require_evaluation_completed",
        "require_report_observed", "require_logs_observed",
        "require_resolved", "allow_kernel_harness_execution",
        "allow_solver_gold_access", "allow_candidate_generation_access",
        "allow_repair_memory_access", "allow_repository_mutation",
        "allow_git_authority", "allow_correctness_claim", POLICY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing, extra = required.difference(policy), set(policy).difference(required)
    if missing: issues.append("policy_missing_fields:" + ",".join(sorted(missing)))
    if extra: issues.append("policy_extra_fields:" + ",".join(sorted(extra)))
    if issues: return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("policy_profile_invalid")
    expected = {field: policy["expected_" + field] for field in BINDING_FIELDS}
    issues.extend(_validate_binding(expected, "policy_binding"))
    for field in ("evaluation_epoch", "maximum_request_age", "maximum_observation_age",
                  "required_smoke_runs", "maximum_workers", "timeout_seconds"):
        if not positive_int(policy[field]):
            issues.append("policy_positive_integer_invalid:" + field)
    for field in required:
        if field.startswith(("require_", "allow_")) and not isinstance(policy[field], bool):
            issues.append("policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return sorted(set(issues))

def validate_plan(plan: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", *BINDING_FIELDS,
        "run_id", "predictions_path", "instance_ids", "maximum_workers",
        "timeout_seconds", "cache_level", "clean_images",
        "plan_preregistered", "gold_prediction_mode",
        "gold_available_to_evaluator_only", "gold_available_to_solver",
        "plan_created_epoch", PLAN_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing, extra = required.difference(plan), set(plan).difference(required)
    if missing: issues.append("plan_missing_fields:" + ",".join(sorted(missing)))
    if extra: issues.append("plan_extra_fields:" + ",".join(sorted(extra)))
    if issues: return issues
    if plan["schema_version"] != SCHEMA_VERSION or plan["profile_version"] != PROFILE_VERSION:
        issues.append("plan_profile_invalid")
    issues.extend(_validate_binding(plan, "plan_binding"))
    if not isinstance(plan["run_id"], str) or IDENTIFIER.fullmatch(plan["run_id"]) is None:
        issues.append("plan_run_id_invalid")
    if plan["predictions_path"] != "gold":
        issues.append("plan_prediction_mode_invalid")
    if not isinstance(plan["instance_ids"], list) or len(plan["instance_ids"]) != 1 or plan["instance_ids"][0] != plan["instance_id"]:
        issues.append("plan_instances_invalid")
    for field in ("maximum_workers", "timeout_seconds", "plan_created_epoch"):
        if not positive_int(plan[field]):
            issues.append("plan_integer_invalid:" + field)
    for field in ("clean_images", "plan_preregistered", "gold_prediction_mode",
                  "gold_available_to_evaluator_only", "gold_available_to_solver"):
        if not isinstance(plan[field], bool):
            issues.append("plan_boolean_invalid:" + field)
    if not isinstance(plan["cache_level"], str) or plan["cache_level"] not in {"none", "base", "env", "instance"}:
        issues.append("plan_cache_level_invalid")
    if not digest_ok(plan, PLAN_DIGEST_FIELD):
        issues.append("plan_digest_mismatch")
    return sorted(set(issues))

def validate_observation(observation: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", *BINDING_FIELDS,
        "observer_id", "run_id", "observation_created_epoch",
        "external_harness_execution_observed", "harness_execution_performed_by_kernel",
        "network_access_performed_by_external_harness", "docker_used",
        "image_available", "container_started", "gold_patch_applied",
        "evaluation_completed", "resolved", "report_observed", "logs_observed",
        "report_digest", "test_output_digest", "instance_log_digest",
        "gold_patch_exposed_to_solver", "gold_patch_used_for_candidate_generation",
        "gold_patch_used_for_repair_memory", "repository_mutation_performed",
        "git_authority_granted", "correctness_claimed", OBSERVATION_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing, extra = required.difference(observation), set(observation).difference(required)
    if missing: issues.append("observation_missing_fields:" + ",".join(sorted(missing)))
    if extra: issues.append("observation_extra_fields:" + ",".join(sorted(extra)))
    if issues: return issues
    if observation["schema_version"] != SCHEMA_VERSION or observation["profile_version"] != PROFILE_VERSION:
        issues.append("observation_profile_invalid")
    issues.extend(_validate_binding(observation, "observation_binding"))
    for field in ("observer_id", "run_id"):
        if not isinstance(observation[field], str) or IDENTIFIER.fullmatch(observation[field]) is None:
            issues.append("observation_identifier_invalid:" + field)
    if not nonnegative_int(observation["observation_created_epoch"]):
        issues.append("observation_epoch_invalid")
    for field in (
        "external_harness_execution_observed", "harness_execution_performed_by_kernel",
        "network_access_performed_by_external_harness", "docker_used",
        "image_available", "container_started", "gold_patch_applied",
        "evaluation_completed", "resolved", "report_observed", "logs_observed",
        "gold_patch_exposed_to_solver", "gold_patch_used_for_candidate_generation",
        "gold_patch_used_for_repair_memory", "repository_mutation_performed",
        "git_authority_granted", "correctness_claimed",
    ):
        if not isinstance(observation[field], bool):
            issues.append("observation_boolean_invalid:" + field)
    for field in ("report_digest", "test_output_digest", "instance_log_digest"):
        item = observation[field]
        if not isinstance(item, str) or SHA256.fullmatch(item) is None:
            issues.append("observation_digest_invalid:" + field)
    if not digest_ok(observation, OBSERVATION_DIGEST_FIELD):
        issues.append("observation_digest_mismatch")
    return sorted(set(issues))

__all__ = [name for name in globals() if name.isupper()] + [
    "GoldPatchEnvironmentSmokeResult", "canonical_digest", "canonical_json",
    "digest_without", "digest_ok", "mapping", "nonnegative_int", "positive_int",
    "seal", "validate_request", "validate_policy", "validate_plan",
    "validate_observation",
]
