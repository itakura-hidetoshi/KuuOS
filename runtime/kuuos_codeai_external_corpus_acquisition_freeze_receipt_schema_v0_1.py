from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_external_corpus_acquisition_freeze_receipt_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI External Corpus Acquisition and Freeze Receipt v0.1"
PREDECESSOR_PROFILE_VERSION = "CodeAI External General Benchmark Protocol and SWE-bench Verified Adapter v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_FREEZE_ONLY = "external_corpus_acquisition_and_freeze_only"
DISPOSITION_COMPLETED = "external_corpus_acquisition_freeze_completed"
DECISION_ADMIT = "external_corpus_freeze_admitted"
DECISION_HOLD = "external_corpus_freeze_held"

REQUEST_DIGEST_FIELD = "codeai_external_corpus_freeze_request_digest"
POLICY_DIGEST_FIELD = "codeai_external_corpus_freeze_policy_digest"
OBSERVATION_DIGEST_FIELD = "codeai_external_corpus_acquisition_observation_digest"
PACK_DIGEST_FIELD = "codeai_external_corpus_freeze_pack_digest"
RECEIPT_DIGEST_FIELD = "codeai_external_corpus_freeze_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,191}$")

SCHEMA_COLUMNS = (
    "repo",
    "instance_id",
    "base_commit",
    "patch",
    "test_patch",
    "problem_statement",
    "hints_text",
    "created_at",
    "version",
    "FAIL_TO_PASS",
    "PASS_TO_PASS",
    "environment_setup_commit",
    "difficulty",
)
SOLVER_VISIBLE_FIELDS = (
    "repo",
    "instance_id",
    "base_commit",
    "problem_statement",
    "version",
    "environment_setup_commit",
    "difficulty",
)
RESTRICTED_EVALUATOR_FIELDS = (
    "patch",
    "test_patch",
    "hints_text",
    "FAIL_TO_PASS",
    "PASS_TO_PASS",
)

BINDING_FIELDS = (
    "controller_repository",
    "controller_source_commit_sha",
    "predecessor_manifest_digest",
    "predecessor_adapter_pack_digest",
    "predecessor_adapter_receipt_digest",
    "benchmark_id",
    "dataset_name",
    "dataset_revision",
    "dataset_split",
    "artifact_path",
    "artifact_sha256",
    "artifact_size_bytes",
    "expected_row_count",
    "schema_digest",
    "solver_visible_fields_digest",
    "restricted_evaluator_fields_digest",
    "acquisition_contract_digest",
    "freeze_policy_digest",
)

@dataclass(frozen=True)
class CodeAIExternalCorpusAcquisitionFreezeResult:
    status: str
    issues: tuple[str, ...]
    freeze_pack: dict[str, Any] | None
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
    digest = value.get(field)
    return isinstance(digest, str) and SHA256.fullmatch(digest) is not None and digest == digest_without(value, field)


def nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def positive_int(value: Any) -> bool:
    return nonnegative_int(value) and value > 0


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def _validate_binding(value: Mapping[str, Any], prefix: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(value.get("controller_repository"), str) or "/" not in value["controller_repository"]:
        issues.append(prefix + "_controller_repository_invalid")
    if not isinstance(value.get("controller_source_commit_sha"), str) or SHA40.fullmatch(value["controller_source_commit_sha"]) is None:
        issues.append(prefix + "_controller_source_commit_invalid")
    for field in (
        "predecessor_manifest_digest",
        "predecessor_adapter_pack_digest",
        "predecessor_adapter_receipt_digest",
        "artifact_sha256",
        "schema_digest",
        "solver_visible_fields_digest",
        "restricted_evaluator_fields_digest",
        "acquisition_contract_digest",
        "freeze_policy_digest",
    ):
        item = value.get(field)
        if not isinstance(item, str) or SHA256.fullmatch(item) is None:
            issues.append(prefix + "_digest_invalid:" + field)
    if value.get("benchmark_id") != "swe-bench-verified":
        issues.append(prefix + "_benchmark_invalid")
    if value.get("dataset_name") != "princeton-nlp/SWE-bench_Verified":
        issues.append(prefix + "_dataset_invalid")
    if not isinstance(value.get("dataset_revision"), str) or SHA40.fullmatch(value["dataset_revision"]) is None:
        issues.append(prefix + "_dataset_revision_invalid")
    if value.get("dataset_split") != "test":
        issues.append(prefix + "_split_invalid")
    if value.get("artifact_path") != "data/test-00000-of-00001.parquet":
        issues.append(prefix + "_artifact_path_invalid")
    for field in ("artifact_size_bytes", "expected_row_count"):
        if not positive_int(value.get(field)):
            issues.append(prefix + "_positive_integer_invalid:" + field)
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", "request_id", "request_revision", *BINDING_FIELDS,
        "request_created_epoch", "unresolved_questions", "claims_solver_label_access",
        "claims_gold_patch_access", "claims_harness_execution_authority",
        "claims_repository_mutation_authority", "claims_git_authority", "claims_correctness",
        REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("request_profile_invalid")
    for field in ("request_id", "request_revision"):
        if not isinstance(request[field], str) or IDENTIFIER.fullmatch(request[field]) is None:
            issues.append("request_identifier_invalid:" + field)
    issues.extend(_validate_binding(request, "request_binding"))
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("request_epoch_invalid")
    if not unique_strings(request["unresolved_questions"]):
        issues.append("request_questions_invalid")
    for field in (
        "claims_solver_label_access", "claims_gold_patch_access", "claims_harness_execution_authority",
        "claims_repository_mutation_authority", "claims_git_authority", "claims_correctness",
    ):
        if not isinstance(request[field], bool):
            issues.append("request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", *{"expected_" + field for field in BINDING_FIELDS},
        "evaluation_epoch", "maximum_request_age", "maximum_observation_age",
        "require_exact_binding", "require_predecessor_admitted", "require_pinned_revision",
        "require_artifact_sha256", "require_artifact_size", "require_row_count",
        "require_schema", "require_independent_observation", "require_content_addressed_storage",
        "require_immutable_freeze", "require_solver_field_partition", "allow_external_fetch_evidence",
        "allow_solver_label_access", "allow_gold_patch_access", "allow_harness_execution",
        "allow_repository_mutation", "allow_git_authority", "allow_correctness_claim",
        POLICY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(policy)
    extra = set(policy).difference(required)
    if missing:
        issues.append("policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("policy_profile_invalid")
    expected = {field: policy["expected_" + field] for field in BINDING_FIELDS}
    issues.extend(_validate_binding(expected, "policy_binding"))
    for field in ("evaluation_epoch", "maximum_request_age", "maximum_observation_age"):
        if not positive_int(policy[field]):
            issues.append("policy_positive_integer_invalid:" + field)
    for field in required:
        if field.startswith("require_") or field.startswith("allow_"):
            if not isinstance(policy[field], bool):
                issues.append("policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return sorted(set(issues))


def validate_observation(observation: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", *BINDING_FIELDS,
        "observation_id", "observer_id", "observation_created_epoch", "source_uri",
        "fetch_completed", "fetch_performed_by_kernel", "network_access_performed_by_fetcher",
        "artifact_observed", "artifact_sha256_verified", "artifact_size_verified",
        "row_count_verified", "schema_verified", "solver_field_partition_verified",
        "content_addressed_storage", "immutable_freeze", "artifact_copy_committed_to_repository",
        "gold_patch_exposed_to_solver", "test_patch_exposed_to_solver", "evaluation_labels_exposed_to_solver",
        "harness_execution_performed", "repository_mutation_performed", "git_authority_granted",
        "correctness_claimed", "observed_row_count", "observed_schema_columns",
        "solver_visible_fields", "restricted_evaluator_fields", OBSERVATION_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(observation)
    extra = set(observation).difference(required)
    if missing:
        issues.append("observation_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("observation_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if observation["schema_version"] != SCHEMA_VERSION or observation["profile_version"] != PROFILE_VERSION:
        issues.append("observation_profile_invalid")
    issues.extend(_validate_binding(observation, "observation_binding"))
    for field in ("observation_id", "observer_id"):
        if not isinstance(observation[field], str) or IDENTIFIER.fullmatch(observation[field]) is None:
            issues.append("observation_identifier_invalid:" + field)
    if not nonnegative_int(observation["observation_created_epoch"]):
        issues.append("observation_epoch_invalid")
    if not isinstance(observation["source_uri"], str) or not observation["source_uri"].startswith("https://huggingface.co/"):
        issues.append("observation_source_uri_invalid")
    if not positive_int(observation["observed_row_count"]):
        issues.append("observation_row_count_invalid")
    if not unique_strings(observation["observed_schema_columns"], nonempty=True):
        issues.append("observation_schema_columns_invalid")
    if not unique_strings(observation["solver_visible_fields"], nonempty=True):
        issues.append("observation_solver_fields_invalid")
    if not unique_strings(observation["restricted_evaluator_fields"], nonempty=True):
        issues.append("observation_restricted_fields_invalid")
    for field in required:
        if field in {
            "fetch_completed", "fetch_performed_by_kernel", "network_access_performed_by_fetcher",
            "artifact_observed", "artifact_sha256_verified", "artifact_size_verified",
            "row_count_verified", "schema_verified", "solver_field_partition_verified",
            "content_addressed_storage", "immutable_freeze", "artifact_copy_committed_to_repository",
            "gold_patch_exposed_to_solver", "test_patch_exposed_to_solver", "evaluation_labels_exposed_to_solver",
            "harness_execution_performed", "repository_mutation_performed", "git_authority_granted", "correctness_claimed",
        } and not isinstance(observation[field], bool):
            issues.append("observation_boolean_invalid:" + field)
    if not digest_ok(observation, OBSERVATION_DIGEST_FIELD):
        issues.append("observation_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIExternalCorpusAcquisitionFreezeResult", "canonical_digest", "canonical_json",
    "digest_ok", "digest_without", "mapping", "nonnegative_int", "positive_int", "seal",
    "unique_strings", "validate_observation", "validate_policy", "validate_request",
]
