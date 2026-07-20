#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping, Sequence

VERSION = "kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Generated Patch Error Baseline Replay Evaluation v0.1"
DATASET_PROFILE_VERSION = "CodeAI Generated Patch Error Replay Dataset v0.1"
CASE_PROFILE_VERSION = "CodeAI Generated Patch Error Replay Case v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DISPOSITION_COMPLETED = "generated_patch_error_baseline_replay_evaluation_completed"

STAGE_NOT_RUN = "not_run"
STAGE_PASSED = "passed"
STAGE_FAILED = "failed"
STAGE_ABORTED = "aborted"
STAGE_STATUSES = {STAGE_NOT_RUN, STAGE_PASSED, STAGE_FAILED, STAGE_ABORTED}

VERIFICATION_NOT_RUN = "not_run"
VERIFICATION_PASSED = "passed"
VERIFICATION_FAILED = "failed"
VERIFICATION_INCONCLUSIVE = "inconclusive"
VERIFICATION_STATUSES = {
    VERIFICATION_NOT_RUN,
    VERIFICATION_PASSED,
    VERIFICATION_FAILED,
    VERIFICATION_INCONCLUSIVE,
}

STAGE_FIELDS = (
    "structured_output_status",
    "patch_application_status",
    "parse_status",
    "typecheck_status",
    "targeted_test_status",
    "full_regression_status",
)
STAGE_NAMES = (
    "structured_output",
    "patch_application",
    "parse",
    "typecheck",
    "targeted_test",
    "full_regression",
)

CASE_DIGEST_FIELD = "codeai_generated_patch_error_replay_case_digest"
DATASET_DIGEST_FIELD = "codeai_generated_patch_error_replay_dataset_digest"
REQUEST_DIGEST_FIELD = "codeai_generated_patch_error_baseline_request_digest"
POLICY_DIGEST_FIELD = "codeai_generated_patch_error_baseline_policy_digest"
METRICS_DIGEST_FIELD = "codeai_generated_patch_error_baseline_metrics_digest"
EVIDENCE_DIGEST_FIELD = "codeai_generated_patch_error_baseline_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_generated_patch_error_baseline_receipt_digest"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")
_ERROR_FINGERPRINT = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")

CASE_FIELDS = {
    "schema_version",
    "profile_version",
    "case_id",
    "repository_full_name",
    "source_commit_sha",
    "candidate_digest",
    "patch_artifact_digest",
    "generation_receipt_digest",
    "application_receipt_digest",
    "verification_execution_receipt_digest",
    "independent_verification_receipt_digest",
    "provider_id",
    "model_id",
    *STAGE_FIELDS,
    "independent_verification_status",
    "repair_cycle_count",
    "repair_reached_green",
    "provider_call_count",
    "generated_output_bytes",
    "error_fingerprints",
    "observed_epoch",
    CASE_DIGEST_FIELD,
}

DATASET_FIELDS = {
    "schema_version",
    "profile_version",
    "dataset_id",
    "repository_full_name",
    "window_start_epoch",
    "window_end_epoch",
    "case_digests",
    "cases",
    DATASET_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "schema_version",
    "profile_version",
    "evaluation_id",
    "dataset_digest",
    "repository_full_name",
    "evaluator_id",
    "request_created_epoch",
    "compute_stage_baseline",
    "compute_error_fingerprint_baseline",
    "compute_repair_efficiency",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "schema_version",
    "profile_version",
    "expected_repository_full_name",
    "expected_dataset_digest",
    "authorized_evaluator_ids",
    "maximum_request_age",
    "maximum_cases",
    "maximum_error_fingerprints_per_case",
    "maximum_repair_cycles_per_case",
    "maximum_provider_calls_per_case",
    "maximum_generated_output_bytes_per_case",
    "evaluation_epoch",
    "require_exact_case_digests",
    "require_sequential_stage_evidence",
    "allow_read_only_replay_evaluation",
    "allow_execution",
    "allow_repository_mutation",
    "allow_git_effect",
    "allow_network_access",
    "allow_secret_read",
    "allow_selection_authority",
    "allow_successor_authority",
    POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIGeneratedPatchErrorBaselineReplayEvaluationResult:
    status: str
    issues: tuple[str, ...]
    evidence: dict[str, Any] | None
    receipt: dict[str, Any] | None


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    sealed = dict(value)
    sealed[field] = digest_without(sealed, field)
    return sealed


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    minimum = 1 if positive else 0
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        return None
    return value


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields - set(value)
    extra = set(value) - fields
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _digest_value(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and bool(_IDENTIFIER.fullmatch(value))


def _string_list(value: Any, *, allow_empty: bool = True) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    result = tuple(value)
    if len(result) != len(set(result)):
        return None
    if not allow_empty and not result:
        return None
    return result


def _validate_nullable_digest(
    case: Mapping[str, Any],
    field: str,
    *,
    required: bool,
    issues: list[str],
) -> None:
    value = case.get(field)
    if required:
        if not _digest_value(value):
            issues.append("case_required_digest_invalid:" + field)
    elif value is not None:
        issues.append("case_unexpected_digest:" + field)


def _validate_case(case: Mapping[str, Any], policy: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(case, CASE_FIELDS, "case")
    if issues:
        return issues

    if case.get("schema_version") != SCHEMA_VERSION:
        issues.append("case_schema_unsupported")
    if case.get("profile_version") != CASE_PROFILE_VERSION:
        issues.append("case_profile_unsupported")
    if not _identifier(case.get("case_id")):
        issues.append("case_id_invalid")
    if not isinstance(case.get("repository_full_name"), str) or not _REPOSITORY.fullmatch(
        case["repository_full_name"]
    ):
        issues.append("case_repository_invalid")

    if not isinstance(case.get("source_commit_sha"), str) or not _GIT_SHA.fullmatch(case["source_commit_sha"]):
        issues.append("case_git_sha_invalid:source_commit_sha")
    for field in (
        "candidate_digest",
        "patch_artifact_digest",
        "generation_receipt_digest",
    ):
        if not _digest_value(case.get(field)):
            issues.append("case_digest_invalid:" + field)

    for field in ("provider_id", "model_id"):
        if not _identifier(case.get(field)):
            issues.append("case_identifier_invalid:" + field)

    for field in STAGE_FIELDS:
        if case.get(field) not in STAGE_STATUSES:
            issues.append("case_stage_status_invalid:" + field)
    verification_status = case.get("independent_verification_status")
    if verification_status not in VERIFICATION_STATUSES:
        issues.append("case_verification_status_invalid")

    for field in (
        "repair_cycle_count",
        "provider_call_count",
        "generated_output_bytes",
        "observed_epoch",
    ):
        if _nat(
            case.get(field),
            positive=field in {"provider_call_count", "generated_output_bytes"},
        ) is None:
            issues.append("case_nat_invalid:" + field)

    if not isinstance(case.get("repair_reached_green"), bool):
        issues.append("case_repair_reached_green_invalid")

    fingerprints = _string_list(case.get("error_fingerprints"))
    if fingerprints is None:
        issues.append("case_error_fingerprints_invalid")
        fingerprints = ()
    else:
        for fingerprint in fingerprints:
            if not _ERROR_FINGERPRINT.fullmatch(fingerprint):
                issues.append("case_error_fingerprint_invalid:" + fingerprint)

    if len(fingerprints) > policy["maximum_error_fingerprints_per_case"]:
        issues.append("case_error_fingerprint_budget_exceeded")
    if case["repair_cycle_count"] > policy["maximum_repair_cycles_per_case"]:
        issues.append("case_repair_cycle_budget_exceeded")
    if case["provider_call_count"] > policy["maximum_provider_calls_per_case"]:
        issues.append("case_provider_call_budget_exceeded")
    if case["generated_output_bytes"] > policy["maximum_generated_output_bytes_per_case"]:
        issues.append("case_generated_output_budget_exceeded")

    if case["repair_cycle_count"] == 0 and case["repair_reached_green"]:
        issues.append("case_repair_green_without_cycle")
    if case["repair_reached_green"] and verification_status != VERIFICATION_PASSED:
        issues.append("case_repair_green_without_verified_patch")

    if policy["require_sequential_stage_evidence"]:
        predecessor_passed = True
        for field in STAGE_FIELDS:
            status = case[field]
            if not predecessor_passed and status != STAGE_NOT_RUN:
                issues.append("case_nonsequential_stage_evidence:" + field)
            predecessor_passed = predecessor_passed and status == STAGE_PASSED
        if not predecessor_passed and verification_status != VERIFICATION_NOT_RUN:
            issues.append("case_nonsequential_independent_verification")

    application_required = case["patch_application_status"] != STAGE_NOT_RUN
    verification_execution_required = any(
        case[field] != STAGE_NOT_RUN
        for field in ("targeted_test_status", "full_regression_status")
    )
    independent_required = verification_status != VERIFICATION_NOT_RUN
    _validate_nullable_digest(
        case,
        "application_receipt_digest",
        required=application_required,
        issues=issues,
    )
    _validate_nullable_digest(
        case,
        "verification_execution_receipt_digest",
        required=verification_execution_required,
        issues=issues,
    )
    _validate_nullable_digest(
        case,
        "independent_verification_receipt_digest",
        required=independent_required,
        issues=issues,
    )

    if case.get(CASE_DIGEST_FIELD) != digest_without(case, CASE_DIGEST_FIELD):
        issues.append("case_digest_mismatch")
    return issues


def _validate_dataset(dataset: Mapping[str, Any], policy: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(dataset, DATASET_FIELDS, "dataset")
    if issues:
        return issues

    if dataset.get("schema_version") != SCHEMA_VERSION:
        issues.append("dataset_schema_unsupported")
    if dataset.get("profile_version") != DATASET_PROFILE_VERSION:
        issues.append("dataset_profile_unsupported")
    if not _identifier(dataset.get("dataset_id")):
        issues.append("dataset_id_invalid")
    if not isinstance(dataset.get("repository_full_name"), str) or not _REPOSITORY.fullmatch(
        dataset["repository_full_name"]
    ):
        issues.append("dataset_repository_invalid")

    start = _nat(dataset.get("window_start_epoch"))
    end = _nat(dataset.get("window_end_epoch"))
    if start is None or end is None or start > end:
        issues.append("dataset_window_invalid")

    cases_raw = dataset.get("cases")
    if not isinstance(cases_raw, list) or not cases_raw:
        issues.append("dataset_cases_invalid")
        cases: list[Mapping[str, Any]] = []
    else:
        cases = []
        for index, raw_case in enumerate(cases_raw):
            case = _mapping(raw_case)
            if case is None:
                issues.append(f"dataset_case_not_mapping:{index}")
                continue
            cases.append(case)
            for issue in _validate_case(case, policy):
                issues.append(f"dataset_case_{index}:{issue}")

    if len(cases) > policy["maximum_cases"]:
        issues.append("dataset_case_budget_exceeded")

    case_ids = [case.get("case_id") for case in cases]
    case_digests = [case.get(CASE_DIGEST_FIELD) for case in cases]
    if len(case_ids) != len(set(case_ids)):
        issues.append("dataset_duplicate_case_id")
    if len(case_digests) != len(set(case_digests)):
        issues.append("dataset_duplicate_case_digest")

    supplied_case_digests = _string_list(dataset.get("case_digests"), allow_empty=False)
    if supplied_case_digests is None:
        issues.append("dataset_case_digests_invalid")
    elif policy["require_exact_case_digests"] and list(supplied_case_digests) != case_digests:
        issues.append("dataset_case_digest_order_mismatch")

    if start is not None and end is not None:
        for index, case in enumerate(cases):
            observed = case.get("observed_epoch")
            if isinstance(observed, int) and not isinstance(observed, bool):
                if observed < start or observed > end:
                    issues.append(f"dataset_case_{index}:observed_epoch_outside_window")

    for index, case in enumerate(cases):
        if case.get("repository_full_name") != dataset.get("repository_full_name"):
            issues.append(f"dataset_case_{index}:repository_mismatch")

    if dataset.get(DATASET_DIGEST_FIELD) != digest_without(dataset, DATASET_DIGEST_FIELD):
        issues.append("dataset_digest_mismatch")
    return issues


def _validate_request(request: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(request, REQUEST_FIELDS, "request")
    if issues:
        return issues
    if request.get("schema_version") != SCHEMA_VERSION:
        issues.append("request_schema_unsupported")
    if request.get("profile_version") != PROFILE_VERSION:
        issues.append("request_profile_unsupported")
    for field in ("evaluation_id", "evaluator_id"):
        if not _identifier(request.get(field)):
            issues.append("request_identifier_invalid:" + field)
    if not _digest_value(request.get("dataset_digest")):
        issues.append("request_dataset_digest_invalid")
    if not isinstance(request.get("repository_full_name"), str) or not _REPOSITORY.fullmatch(
        request["repository_full_name"]
    ):
        issues.append("request_repository_invalid")
    if _nat(request.get("request_created_epoch")) is None:
        issues.append("request_created_epoch_invalid")
    for field in (
        "compute_stage_baseline",
        "compute_error_fingerprint_baseline",
        "compute_repair_efficiency",
    ):
        if request.get(field) is not True:
            issues.append("request_required_true:" + field)
    if request.get(REQUEST_DIGEST_FIELD) != digest_without(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return issues


def _validate_policy(policy: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(policy, POLICY_FIELDS, "policy")
    if issues:
        return issues
    if policy.get("schema_version") != SCHEMA_VERSION:
        issues.append("policy_schema_unsupported")
    if policy.get("profile_version") != PROFILE_VERSION:
        issues.append("policy_profile_unsupported")
    if not isinstance(policy.get("expected_repository_full_name"), str) or not _REPOSITORY.fullmatch(
        policy["expected_repository_full_name"]
    ):
        issues.append("policy_repository_invalid")
    if not _digest_value(policy.get("expected_dataset_digest")):
        issues.append("policy_dataset_digest_invalid")
    evaluators = _string_list(policy.get("authorized_evaluator_ids"), allow_empty=False)
    if evaluators is None or any(not _identifier(item) for item in (evaluators or ())):
        issues.append("policy_authorized_evaluators_invalid")
    for field in (
        "maximum_request_age",
        "maximum_cases",
        "maximum_error_fingerprints_per_case",
        "maximum_repair_cycles_per_case",
        "maximum_provider_calls_per_case",
        "maximum_generated_output_bytes_per_case",
        "evaluation_epoch",
    ):
        if _nat(
            policy.get(field),
            positive=field
            not in {"evaluation_epoch", "maximum_error_fingerprints_per_case", "maximum_repair_cycles_per_case"},
        ) is None:
            issues.append("policy_nat_invalid:" + field)
    for field in (
        "require_exact_case_digests",
        "require_sequential_stage_evidence",
        "allow_read_only_replay_evaluation",
    ):
        if policy.get(field) is not True:
            issues.append("policy_required_true:" + field)
    for field in (
        "allow_execution",
        "allow_repository_mutation",
        "allow_git_effect",
        "allow_network_access",
        "allow_secret_read",
        "allow_selection_authority",
        "allow_successor_authority",
    ):
        if policy.get(field) is not False:
            issues.append("policy_required_false:" + field)
    if policy.get(POLICY_DIGEST_FIELD) != digest_without(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return issues


def _ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "defined": denominator > 0,
        "basis_points": (numerator * 10000 // denominator) if denominator > 0 else None,
    }


def _stage_metrics(cases: Sequence[Mapping[str, Any]], field: str) -> dict[str, Any]:
    statuses = Counter(case[field] for case in cases)
    reached = len(cases) - statuses[STAGE_NOT_RUN]
    return {
        "reached_count": reached,
        "passed_count": statuses[STAGE_PASSED],
        "failed_count": statuses[STAGE_FAILED],
        "aborted_count": statuses[STAGE_ABORTED],
        "not_run_count": statuses[STAGE_NOT_RUN],
        "conditional_pass_rate": _ratio(statuses[STAGE_PASSED], reached),
    }


def _first_failure(case: Mapping[str, Any]) -> str | None:
    for field, name in zip(STAGE_FIELDS, STAGE_NAMES):
        if case[field] in {STAGE_FAILED, STAGE_ABORTED}:
            return name
        if case[field] == STAGE_NOT_RUN:
            return None
    verification = case["independent_verification_status"]
    if verification in {VERIFICATION_FAILED, VERIFICATION_INCONCLUSIVE}:
        return "independent_verification"
    return None


def _is_incomplete(case: Mapping[str, Any]) -> bool:
    if _first_failure(case) is not None:
        return False
    return case["independent_verification_status"] == VERIFICATION_NOT_RUN


def _build_metrics(cases: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    stage_metrics = {
        name: _stage_metrics(cases, field)
        for field, name in zip(STAGE_FIELDS, STAGE_NAMES)
    }

    verification_counts = Counter(
        case["independent_verification_status"] for case in cases
    )
    verification_reached = len(cases) - verification_counts[VERIFICATION_NOT_RUN]

    first_failure_counts = Counter(
        failure for case in cases if (failure := _first_failure(case)) is not None
    )

    fingerprint_counts: Counter[str] = Counter()
    case_fingerprint_sets: list[set[str]] = []
    for case in cases:
        fingerprint_set = set(case["error_fingerprints"])
        case_fingerprint_sets.append(fingerprint_set)
        fingerprint_counts.update(fingerprint_set)
    repeated_fingerprints = {
        fingerprint for fingerprint, count in fingerprint_counts.items() if count > 1
    }

    verified_patch_count = verification_counts[VERIFICATION_PASSED]
    repair_attempted = sum(case["repair_cycle_count"] > 0 for case in cases)
    repair_green = sum(case["repair_reached_green"] for case in cases)
    total_repair_cycles = sum(case["repair_cycle_count"] for case in cases)
    total_provider_calls = sum(case["provider_call_count"] for case in cases)
    total_generated_output_bytes = sum(case["generated_output_bytes"] for case in cases)

    metrics = {
        "total_case_count": len(cases),
        "stage_metrics": stage_metrics,
        "independent_verification_metrics": {
            "reached_count": verification_reached,
            "passed_count": verification_counts[VERIFICATION_PASSED],
            "failed_count": verification_counts[VERIFICATION_FAILED],
            "inconclusive_count": verification_counts[VERIFICATION_INCONCLUSIVE],
            "not_run_count": verification_counts[VERIFICATION_NOT_RUN],
            "conditional_pass_rate": _ratio(
                verification_counts[VERIFICATION_PASSED],
                verification_reached,
            ),
        },
        "first_failure_counts": {
            name: first_failure_counts[name]
            for name in (*STAGE_NAMES, "independent_verification")
        },
        "incomplete_case_count": sum(_is_incomplete(case) for case in cases),
        "verified_patch_count": verified_patch_count,
        "repair_attempted_case_count": repair_attempted,
        "repair_green_case_count": repair_green,
        "repair_green_rate": _ratio(repair_green, repair_attempted),
        "total_repair_cycles": total_repair_cycles,
        "repair_cycles_per_verified_patch": _ratio(
            total_repair_cycles,
            verified_patch_count,
        ),
        "total_provider_calls": total_provider_calls,
        "provider_calls_per_verified_patch": _ratio(
            total_provider_calls,
            verified_patch_count,
        ),
        "total_generated_output_bytes": total_generated_output_bytes,
        "generated_output_bytes_per_verified_patch": _ratio(
            total_generated_output_bytes,
            verified_patch_count,
        ),
        "distinct_error_fingerprint_count": len(fingerprint_counts),
        "repeated_error_fingerprint_count": len(repeated_fingerprints),
        "cases_with_repeated_error_fingerprint": sum(
            bool(fingerprints & repeated_fingerprints)
            for fingerprints in case_fingerprint_sets
        ),
        "error_fingerprint_counts": {
            fingerprint: fingerprint_counts[fingerprint]
            for fingerprint in sorted(fingerprint_counts)
        },
    }
    return seal(metrics, METRICS_DIGEST_FIELD)


def build_codeai_generated_patch_error_baseline_replay_evaluation(
    *,
    dataset: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> CodeAIGeneratedPatchErrorBaselineReplayEvaluationResult:
    dataset_map = _mapping(dataset)
    request_map = _mapping(request)
    policy_map = _mapping(policy)
    issues: list[str] = []

    if dataset_map is None:
        issues.append("dataset_not_mapping")
    if request_map is None:
        issues.append("request_not_mapping")
    if policy_map is None:
        issues.append("policy_not_mapping")
    if issues:
        return CodeAIGeneratedPatchErrorBaselineReplayEvaluationResult(
            STATUS_BLOCKED,
            tuple(issues),
            None,
            None,
        )

    assert dataset_map is not None
    assert request_map is not None
    assert policy_map is not None

    issues.extend(_validate_request(request_map))
    issues.extend(_validate_policy(policy_map))
    if not issues:
        issues.extend(_validate_dataset(dataset_map, policy_map))

    if not issues:
        if request_map["dataset_digest"] != dataset_map[DATASET_DIGEST_FIELD]:
            issues.append("request_dataset_correspondence_mismatch")
        if policy_map["expected_dataset_digest"] != dataset_map[DATASET_DIGEST_FIELD]:
            issues.append("policy_dataset_correspondence_mismatch")
        if request_map["repository_full_name"] != dataset_map["repository_full_name"]:
            issues.append("request_repository_correspondence_mismatch")
        if policy_map["expected_repository_full_name"] != dataset_map["repository_full_name"]:
            issues.append("policy_repository_correspondence_mismatch")
        if request_map["evaluator_id"] not in policy_map["authorized_evaluator_ids"]:
            issues.append("evaluator_not_authorized")
        evaluation_epoch = policy_map["evaluation_epoch"]
        request_epoch = request_map["request_created_epoch"]
        if evaluation_epoch < request_epoch:
            issues.append("request_from_future")
        elif evaluation_epoch - request_epoch > policy_map["maximum_request_age"]:
            issues.append("request_stale")

    if issues:
        return CodeAIGeneratedPatchErrorBaselineReplayEvaluationResult(
            STATUS_BLOCKED,
            tuple(sorted(set(issues))),
            None,
            None,
        )

    cases = dataset_map["cases"]
    metrics = _build_metrics(cases)

    evidence = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "evaluation_id": request_map["evaluation_id"],
            "dataset_id": dataset_map["dataset_id"],
            "repository_full_name": dataset_map["repository_full_name"],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "dataset_digest": dataset_map[DATASET_DIGEST_FIELD],
            "case_digests": list(dataset_map["case_digests"]),
            "evaluated_case_count": len(cases),
            "metrics": metrics,
            "metrics_digest": metrics[METRICS_DIGEST_FIELD],
            "exact_source_correspondence_verified": True,
            "read_only_replay_evaluation_completed": True,
            "historical_code_reexecuted": False,
            "provider_invoked": False,
            "verification_runner_invoked": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
            "selection_authority_granted": False,
            "successor_stage_authority_granted": False,
        },
        EVIDENCE_DIGEST_FIELD,
    )

    receipt = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "codeai_disposition": DISPOSITION_COMPLETED,
            "evaluation_id": request_map["evaluation_id"],
            "dataset_id": dataset_map["dataset_id"],
            "repository_full_name": dataset_map["repository_full_name"],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "dataset_digest": dataset_map[DATASET_DIGEST_FIELD],
            "evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
            "metrics_digest": metrics[METRICS_DIGEST_FIELD],
            "evaluated_case_count": len(cases),
            "route_receipt_recorded": True,
            "exact_source_correspondence_verified": True,
            "read_only_replay_evaluation_completed": True,
            "historical_code_reexecuted": False,
            "provider_invoked": False,
            "verification_runner_invoked": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
            "selection_authority_granted": False,
            "successor_stage_authority_granted": False,
            "correctness_proof_claimed": False,
        },
        RECEIPT_DIGEST_FIELD,
    )

    return CodeAIGeneratedPatchErrorBaselineReplayEvaluationResult(
        STATUS_READY,
        (),
        evidence,
        receipt,
    )
