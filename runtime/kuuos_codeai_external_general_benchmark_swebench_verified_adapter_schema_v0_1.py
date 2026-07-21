from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI External General Benchmark Protocol and SWE-bench Verified Adapter v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_PROTOCOL_ONLY = "external_general_benchmark_protocol_only"
DISPOSITION_COMPLETED = "external_general_benchmark_protocol_completed"

BENCHMARK_ID = "swe-bench-verified"
DATASET_NAME = "princeton-nlp/SWE-bench_Verified"
DATASET_SPLIT = "test"
EXPECTED_INSTANCE_COUNT = 500
HARNESS_REPOSITORY = "swe-bench/SWE-bench"
HARNESS_ENTRYPOINT = "python -m swebench.harness.run_evaluation"
OFFICIAL_PREDICTION_FIELDS = ("instance_id", "model_name_or_path", "model_patch")
EVALUATION_MODES = ("smoke", "pilot", "full")
CACHE_LEVELS = ("none", "base", "env", "instance")

DECISION_ADMIT = "external_benchmark_protocol_admitted"
DECISION_HOLD = "external_benchmark_protocol_held"

REQUEST_DIGEST_FIELD = "codeai_external_benchmark_request_digest"
POLICY_DIGEST_FIELD = "codeai_external_benchmark_policy_digest"
CONTRACT_DIGEST_FIELD = "codeai_swebench_verified_contract_digest"
RUN_PLAN_DIGEST_FIELD = "codeai_swebench_verified_run_plan_digest"
INSTANCE_CONTRACT_DIGEST_FIELD = "codeai_swebench_verified_instance_contract_digest"
PREDICTION_DIGEST_FIELD = "codeai_swebench_verified_prediction_digest"
PACK_DIGEST_FIELD = "codeai_external_benchmark_adapter_pack_digest"
RECEIPT_DIGEST_FIELD = "codeai_external_benchmark_adapter_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,191}$")
INSTANCE_ID = re.compile(r"^[A-Za-z0-9_.-]+__[A-Za-z0-9_.-]+-[0-9]+$")
PATH = re.compile(r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9._@+/-]+$")

BINDING_FIELDS = (
    "controller_repository_full_name",
    "controller_source_commit_sha",
    "controller_source_tree_digest",
    "benchmark_contract_digest",
    "run_plan_digest",
    "model_configuration_digest",
    "codeai_pipeline_digest",
    "harness_contract_digest",
    "evaluation_protocol_digest",
)


@dataclass(frozen=True)
class CodeAIExternalGeneralBenchmarkAdapterResult:
    status: str
    issues: tuple[str, ...]
    adapter_pack: dict[str, Any] | None
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
    return (
        isinstance(digest, str)
        and SHA256.fullmatch(digest) is not None
        and digest == digest_without(value, field)
    )


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


def exact_fields(value: Mapping[str, Any], required: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = required.difference(value)
    extra = set(value).difference(required)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _validate_binding(value: Mapping[str, Any], prefix: str) -> list[str]:
    issues: list[str] = []
    repository = value.get("controller_repository_full_name")
    if not isinstance(repository, str) or not repository:
        issues.append(prefix + "_repository_invalid")
    commit = value.get("controller_source_commit_sha")
    if not isinstance(commit, str) or SHA40.fullmatch(commit) is None:
        issues.append(prefix + "_commit_invalid")
    for field in (
        "controller_source_tree_digest",
        "benchmark_contract_digest",
        "run_plan_digest",
        "model_configuration_digest",
        "codeai_pipeline_digest",
        "harness_contract_digest",
        "evaluation_protocol_digest",
    ):
        item = value.get(field)
        if not isinstance(item, str) or SHA256.fullmatch(item) is None:
            issues.append(prefix + "_digest_invalid:" + field)
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "request_id",
        "request_revision",
        *BINDING_FIELDS,
        "request_created_epoch",
        "unresolved_questions",
        "claims_harness_execution_authority",
        "claims_network_authority",
        "claims_secret_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
        REQUEST_DIGEST_FIELD,
    }
    issues = exact_fields(request, required, "request")
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
        "claims_harness_execution_authority",
        "claims_network_authority",
        "claims_secret_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
    ):
        if not isinstance(request[field], bool):
            issues.append("request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        *{"expected_" + field for field in BINDING_FIELDS},
        "evaluation_epoch",
        "maximum_request_age",
        "minimum_sample_count",
        "maximum_sample_count",
        "maximum_patch_bytes",
        "maximum_total_patch_bytes",
        "maximum_changed_paths_per_prediction",
        "allowed_evaluation_modes",
        "allowed_cache_levels",
        "require_exact_binding",
        "require_official_verified_dataset",
        "require_expected_instance_count",
        "require_frozen_sample",
        "require_holdout_labels_hidden",
        "require_gold_patch_hidden",
        "require_pinned_harness",
        "require_containerized_harness",
        "require_official_prediction_shape",
        "require_unique_instances",
        "require_patch_digest",
        "require_derived_changed_paths",
        "require_protected_test_path_nonoverlap",
        "allow_protocol_projection",
        "allow_harness_execution",
        "allow_network_access",
        "allow_secret_access",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
        POLICY_DIGEST_FIELD,
    }
    issues = exact_fields(policy, required, "policy")
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("policy_profile_invalid")
    expected_binding = {field: policy["expected_" + field] for field in BINDING_FIELDS}
    issues.extend(_validate_binding(expected_binding, "policy_binding"))
    for field in (
        "evaluation_epoch",
        "maximum_request_age",
        "minimum_sample_count",
        "maximum_sample_count",
        "maximum_patch_bytes",
        "maximum_total_patch_bytes",
        "maximum_changed_paths_per_prediction",
    ):
        if not positive_int(policy[field]):
            issues.append("policy_positive_integer_invalid:" + field)
    if (
        positive_int(policy["minimum_sample_count"])
        and positive_int(policy["maximum_sample_count"])
        and policy["minimum_sample_count"] > policy["maximum_sample_count"]
    ):
        issues.append("policy_sample_bounds_invalid")
    if not unique_strings(policy["allowed_evaluation_modes"], nonempty=True):
        issues.append("policy_evaluation_modes_invalid")
    elif any(item not in EVALUATION_MODES for item in policy["allowed_evaluation_modes"]):
        issues.append("policy_evaluation_mode_unknown")
    if not unique_strings(policy["allowed_cache_levels"], nonempty=True):
        issues.append("policy_cache_levels_invalid")
    elif any(item not in CACHE_LEVELS for item in policy["allowed_cache_levels"]):
        issues.append("policy_cache_level_unknown")
    for field in (
        "require_exact_binding",
        "require_official_verified_dataset",
        "require_expected_instance_count",
        "require_frozen_sample",
        "require_holdout_labels_hidden",
        "require_gold_patch_hidden",
        "require_pinned_harness",
        "require_containerized_harness",
        "require_official_prediction_shape",
        "require_unique_instances",
        "require_patch_digest",
        "require_derived_changed_paths",
        "require_protected_test_path_nonoverlap",
        "allow_protocol_projection",
        "allow_harness_execution",
        "allow_network_access",
        "allow_secret_access",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
    ):
        if not isinstance(policy[field], bool):
            issues.append("policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIExternalGeneralBenchmarkAdapterResult",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "digest_ok",
    "exact_fields",
    "mapping",
    "nonnegative_int",
    "positive_int",
    "seal",
    "unique_strings",
    "validate_policy",
    "validate_request",
]
