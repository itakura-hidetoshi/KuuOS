#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    DISPOSITION_COMPLETED as SOURCE_DISPOSITION_COMPLETED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    METRICS_DIGEST_FIELD as SOURCE_METRICS_DIGEST_FIELD,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    SCHEMA_VERSION,
    STAGE_NAMES,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1"
PROFILE_VERSION = "CodeAI Generated Patch Error Reduction Comparative Replay Evaluation v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DISPOSITION_CONFIRMED = "generated_patch_error_reduction_confirmed"
DISPOSITION_NOT_CONFIRMED = "generated_patch_error_reduction_not_confirmed"

REQUEST_DIGEST_FIELD = "codeai_generated_patch_error_reduction_comparison_request_digest"
POLICY_DIGEST_FIELD = "codeai_generated_patch_error_reduction_comparison_policy_digest"
COMPARISON_METRICS_DIGEST_FIELD = "codeai_generated_patch_error_reduction_comparison_metrics_digest"
EVIDENCE_DIGEST_FIELD = "codeai_generated_patch_error_reduction_comparison_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_generated_patch_error_reduction_comparison_receipt_digest"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")

SOURCE_EVIDENCE_FIELDS = {
    "schema_version",
    "profile_version",
    "evaluation_id",
    "dataset_id",
    "repository_full_name",
    "request_digest",
    "policy_digest",
    "dataset_digest",
    "case_digests",
    "evaluated_case_count",
    "metrics",
    "metrics_digest",
    "exact_source_correspondence_verified",
    "read_only_replay_evaluation_completed",
    "historical_code_reexecuted",
    "provider_invoked",
    "verification_runner_invoked",
    "repository_mutation_performed",
    "git_effect_performed",
    "network_accessed",
    "secret_material_read",
    "selection_authority_granted",
    "successor_stage_authority_granted",
    SOURCE_EVIDENCE_DIGEST_FIELD,
}

SOURCE_RECEIPT_FIELDS = {
    "schema_version",
    "profile_version",
    "codeai_disposition",
    "evaluation_id",
    "dataset_id",
    "repository_full_name",
    "request_digest",
    "policy_digest",
    "dataset_digest",
    "evidence_digest",
    "metrics_digest",
    "evaluated_case_count",
    "route_receipt_recorded",
    "exact_source_correspondence_verified",
    "read_only_replay_evaluation_completed",
    "historical_code_reexecuted",
    "provider_invoked",
    "verification_runner_invoked",
    "repository_mutation_performed",
    "git_effect_performed",
    "network_accessed",
    "secret_material_read",
    "selection_authority_granted",
    "successor_stage_authority_granted",
    "correctness_proof_claimed",
    SOURCE_RECEIPT_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "schema_version",
    "profile_version",
    "comparison_id",
    "repository_full_name",
    "baseline_evidence_digest",
    "baseline_receipt_digest",
    "successor_evidence_digest",
    "successor_receipt_digest",
    "evaluator_id",
    "request_created_epoch",
    "compare_stage_pass_rates",
    "compare_verification_outcomes",
    "compare_error_recurrence",
    "compare_repair_and_generation_cost",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "schema_version",
    "profile_version",
    "expected_repository_full_name",
    "expected_baseline_evidence_digest",
    "expected_baseline_receipt_digest",
    "expected_successor_evidence_digest",
    "expected_successor_receipt_digest",
    "authorized_evaluator_ids",
    "evaluation_epoch",
    "maximum_request_age",
    "require_distinct_dataset_digests",
    "require_equal_case_count",
    "require_defined_ratio_deltas",
    "minimum_independent_verification_pass_rate_delta_basis_points",
    "minimum_verified_patch_count_delta",
    "maximum_typecheck_first_failure_count_delta",
    "maximum_repeated_error_fingerprint_count_delta",
    "maximum_cases_with_repeated_error_fingerprint_delta",
    "maximum_repair_cycles_per_verified_patch_delta_basis_points",
    "maximum_provider_calls_per_verified_patch_delta_basis_points",
    "maximum_generated_output_bytes_per_verified_patch_delta_basis_points",
    "allow_read_only_comparison",
    "allow_historical_code_reexecution",
    "allow_provider_invocation",
    "allow_verification_runner_invocation",
    "allow_repository_mutation",
    "allow_git_effect",
    "allow_network_access",
    "allow_secret_read",
    "allow_selection_authority",
    "allow_successor_authority",
    POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIGeneratedPatchErrorReductionComparativeReplayEvaluationResult:
    status: str
    issues: tuple[str, ...]
    evidence: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _exact_fields(value: Mapping[str, Any], expected: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = expected - set(value)
    extra = set(value) - expected
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _digest(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and bool(_IDENTIFIER.fullmatch(value))


def _nat(value: Any, *, positive: bool = False) -> int | None:
    minimum = 1 if positive else 0
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        return None
    return value


def _integer(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _unique_strings(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not value:
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    result = tuple(value)
    return result if len(result) == len(set(result)) else None


def _validate_ratio(value: Any, prefix: str, issues: list[str]) -> None:
    ratio = _mapping(value)
    if ratio is None:
        issues.append(prefix + "_not_mapping")
        return
    if set(ratio) != {"numerator", "denominator", "defined", "basis_points"}:
        issues.append(prefix + "_fields_invalid")
        return
    numerator = _nat(ratio.get("numerator"))
    denominator = _nat(ratio.get("denominator"))
    if numerator is None:
        issues.append(prefix + "_numerator_invalid")
    if denominator is None:
        issues.append(prefix + "_denominator_invalid")
    defined = ratio.get("defined")
    basis_points = ratio.get("basis_points")
    if not isinstance(defined, bool):
        issues.append(prefix + "_defined_invalid")
        return
    if defined != (denominator is not None and denominator > 0):
        issues.append(prefix + "_defined_mismatch")
    if defined:
        if _nat(basis_points) is None:
            issues.append(prefix + "_basis_points_invalid")
        elif numerator is not None and denominator is not None:
            expected = numerator * 10000 // denominator
            if basis_points != expected:
                issues.append(prefix + "_basis_points_mismatch")
    elif basis_points is not None:
        issues.append(prefix + "_undefined_basis_points_present")


def _validate_metrics(metrics: Any, prefix: str) -> list[str]:
    issues: list[str] = []
    value = _mapping(metrics)
    if value is None:
        return [prefix + "_not_mapping"]
    required = {
        "total_case_count",
        "stage_metrics",
        "independent_verification_metrics",
        "first_failure_counts",
        "incomplete_case_count",
        "verified_patch_count",
        "repair_attempted_case_count",
        "repair_green_case_count",
        "repair_green_rate",
        "total_repair_cycles",
        "repair_cycles_per_verified_patch",
        "total_provider_calls",
        "provider_calls_per_verified_patch",
        "total_generated_output_bytes",
        "generated_output_bytes_per_verified_patch",
        "distinct_error_fingerprint_count",
        "repeated_error_fingerprint_count",
        "cases_with_repeated_error_fingerprint",
        "error_fingerprint_counts",
        SOURCE_METRICS_DIGEST_FIELD,
    }
    issues.extend(_exact_fields(value, required, prefix))
    if issues:
        return issues
    if value[SOURCE_METRICS_DIGEST_FIELD] != digest_without(value, SOURCE_METRICS_DIGEST_FIELD):
        issues.append(prefix + "_digest_mismatch")
    for field in required - {
        "stage_metrics",
        "independent_verification_metrics",
        "first_failure_counts",
        "repair_green_rate",
        "repair_cycles_per_verified_patch",
        "provider_calls_per_verified_patch",
        "generated_output_bytes_per_verified_patch",
        "error_fingerprint_counts",
        SOURCE_METRICS_DIGEST_FIELD,
    }:
        if _nat(value.get(field)) is None:
            issues.append(prefix + "_nat_invalid:" + field)

    stage_metrics = _mapping(value.get("stage_metrics"))
    if stage_metrics is None or set(stage_metrics) != set(STAGE_NAMES):
        issues.append(prefix + "_stage_metrics_invalid")
    else:
        for stage in STAGE_NAMES:
            stage_value = _mapping(stage_metrics[stage])
            if stage_value is None:
                issues.append(prefix + "_stage_not_mapping:" + stage)
                continue
            stage_fields = {
                "reached_count",
                "passed_count",
                "failed_count",
                "aborted_count",
                "not_run_count",
                "conditional_pass_rate",
            }
            if set(stage_value) != stage_fields:
                issues.append(prefix + "_stage_fields_invalid:" + stage)
                continue
            for field in stage_fields - {"conditional_pass_rate"}:
                if _nat(stage_value.get(field)) is None:
                    issues.append(prefix + "_stage_nat_invalid:" + stage + ":" + field)
            _validate_ratio(
                stage_value.get("conditional_pass_rate"),
                prefix + "_stage_ratio:" + stage,
                issues,
            )

    verification = _mapping(value.get("independent_verification_metrics"))
    verification_fields = {
        "reached_count",
        "passed_count",
        "failed_count",
        "inconclusive_count",
        "not_run_count",
        "conditional_pass_rate",
    }
    if verification is None or set(verification) != verification_fields:
        issues.append(prefix + "_verification_metrics_invalid")
    else:
        for field in verification_fields - {"conditional_pass_rate"}:
            if _nat(verification.get(field)) is None:
                issues.append(prefix + "_verification_nat_invalid:" + field)
        _validate_ratio(
            verification.get("conditional_pass_rate"),
            prefix + "_verification_ratio",
            issues,
        )

    first_failures = _mapping(value.get("first_failure_counts"))
    required_first_failures = {*STAGE_NAMES, "independent_verification"}
    if first_failures is None or set(first_failures) != required_first_failures:
        issues.append(prefix + "_first_failure_counts_invalid")
    else:
        for stage, count in first_failures.items():
            if _nat(count) is None:
                issues.append(prefix + "_first_failure_nat_invalid:" + stage)

    for field in (
        "repair_green_rate",
        "repair_cycles_per_verified_patch",
        "provider_calls_per_verified_patch",
        "generated_output_bytes_per_verified_patch",
    ):
        _validate_ratio(value.get(field), prefix + "_" + field, issues)

    fingerprints = _mapping(value.get("error_fingerprint_counts"))
    if fingerprints is None:
        issues.append(prefix + "_error_fingerprint_counts_invalid")
    else:
        for fingerprint, count in fingerprints.items():
            if not isinstance(fingerprint, str) or not fingerprint:
                issues.append(prefix + "_error_fingerprint_invalid")
            if _nat(count, positive=True) is None:
                issues.append(prefix + "_error_fingerprint_count_invalid:" + str(fingerprint))
    return issues


def _validate_source(
    evidence: Mapping[str, Any],
    receipt: Mapping[str, Any],
    prefix: str,
) -> list[str]:
    issues = _exact_fields(evidence, SOURCE_EVIDENCE_FIELDS, prefix + "_evidence")
    issues.extend(_exact_fields(receipt, SOURCE_RECEIPT_FIELDS, prefix + "_receipt"))
    if issues:
        return issues
    if evidence.get("schema_version") != SCHEMA_VERSION:
        issues.append(prefix + "_evidence_schema_unsupported")
    if receipt.get("schema_version") != SCHEMA_VERSION:
        issues.append(prefix + "_receipt_schema_unsupported")
    if evidence.get("profile_version") != SOURCE_PROFILE_VERSION:
        issues.append(prefix + "_evidence_profile_unsupported")
    if receipt.get("profile_version") != SOURCE_PROFILE_VERSION:
        issues.append(prefix + "_receipt_profile_unsupported")
    if receipt.get("codeai_disposition") != SOURCE_DISPOSITION_COMPLETED:
        issues.append(prefix + "_receipt_disposition_unsupported")
    if evidence.get(SOURCE_EVIDENCE_DIGEST_FIELD) != digest_without(
        evidence, SOURCE_EVIDENCE_DIGEST_FIELD
    ):
        issues.append(prefix + "_evidence_digest_mismatch")
    if receipt.get(SOURCE_RECEIPT_DIGEST_FIELD) != digest_without(
        receipt, SOURCE_RECEIPT_DIGEST_FIELD
    ):
        issues.append(prefix + "_receipt_digest_mismatch")
    metrics_issues = _validate_metrics(evidence.get("metrics"), prefix + "_metrics")
    issues.extend(metrics_issues)
    metrics_map = _mapping(evidence.get("metrics")) or {}
    if evidence.get("metrics_digest") != metrics_map.get(SOURCE_METRICS_DIGEST_FIELD):
        issues.append(prefix + "_evidence_metrics_digest_mismatch")
    if receipt.get("metrics_digest") != evidence.get("metrics_digest"):
        issues.append(prefix + "_receipt_metrics_digest_mismatch")
    if receipt.get("evidence_digest") != evidence.get(SOURCE_EVIDENCE_DIGEST_FIELD):
        issues.append(prefix + "_receipt_evidence_digest_mismatch")
    for field in (
        "evaluation_id",
        "dataset_id",
        "repository_full_name",
        "request_digest",
        "policy_digest",
        "dataset_digest",
        "evaluated_case_count",
    ):
        if receipt.get(field) != evidence.get(field):
            issues.append(prefix + "_source_correspondence_mismatch:" + field)
    if not isinstance(evidence.get("repository_full_name"), str) or not _REPOSITORY.fullmatch(
        evidence["repository_full_name"]
    ):
        issues.append(prefix + "_repository_invalid")
    if not _identifier(evidence.get("evaluation_id")):
        issues.append(prefix + "_evaluation_id_invalid")
    if not _identifier(evidence.get("dataset_id")):
        issues.append(prefix + "_dataset_id_invalid")
    if not _digest(evidence.get("dataset_digest")):
        issues.append(prefix + "_dataset_digest_invalid")
    if _nat(evidence.get("evaluated_case_count"), positive=True) is None:
        issues.append(prefix + "_evaluated_case_count_invalid")
    if evidence.get("evaluated_case_count") != metrics_map.get("total_case_count"):
        issues.append(prefix + "_case_count_metrics_mismatch")
    case_digests = evidence.get("case_digests")
    if (
        not isinstance(case_digests, list)
        or len(case_digests) != evidence.get("evaluated_case_count")
        or not all(_digest(item) for item in case_digests)
        or len(case_digests) != len(set(case_digests))
    ):
        issues.append(prefix + "_case_digests_invalid")
    required_true = (
        "exact_source_correspondence_verified",
        "read_only_replay_evaluation_completed",
    )
    required_false = (
        "historical_code_reexecuted",
        "provider_invoked",
        "verification_runner_invoked",
        "repository_mutation_performed",
        "git_effect_performed",
        "network_accessed",
        "secret_material_read",
        "selection_authority_granted",
        "successor_stage_authority_granted",
    )
    for field in required_true:
        if evidence.get(field) is not True or receipt.get(field) is not True:
            issues.append(prefix + "_required_true:" + field)
    for field in required_false:
        if evidence.get(field) is not False or receipt.get(field) is not False:
            issues.append(prefix + "_required_false:" + field)
    if receipt.get("route_receipt_recorded") is not True:
        issues.append(prefix + "_route_receipt_not_recorded")
    if receipt.get("correctness_proof_claimed") is not False:
        issues.append(prefix + "_correctness_claim_present")
    return issues


def _validate_request(request: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(request, REQUEST_FIELDS, "request")
    if issues:
        return issues
    if request.get("schema_version") != SCHEMA_VERSION:
        issues.append("request_schema_unsupported")
    if request.get("profile_version") != PROFILE_VERSION:
        issues.append("request_profile_unsupported")
    for field in ("comparison_id", "evaluator_id"):
        if not _identifier(request.get(field)):
            issues.append("request_identifier_invalid:" + field)
    repository = request.get("repository_full_name")
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        issues.append("request_repository_invalid")
    for field in (
        "baseline_evidence_digest",
        "baseline_receipt_digest",
        "successor_evidence_digest",
        "successor_receipt_digest",
    ):
        if not _digest(request.get(field)):
            issues.append("request_digest_invalid:" + field)
    if _nat(request.get("request_created_epoch")) is None:
        issues.append("request_created_epoch_invalid")
    for field in (
        "compare_stage_pass_rates",
        "compare_verification_outcomes",
        "compare_error_recurrence",
        "compare_repair_and_generation_cost",
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
    repository = policy.get("expected_repository_full_name")
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        issues.append("policy_repository_invalid")
    for field in (
        "expected_baseline_evidence_digest",
        "expected_baseline_receipt_digest",
        "expected_successor_evidence_digest",
        "expected_successor_receipt_digest",
    ):
        if not _digest(policy.get(field)):
            issues.append("policy_digest_invalid:" + field)
    evaluators = _unique_strings(policy.get("authorized_evaluator_ids"))
    if evaluators is None or any(not _identifier(item) for item in (evaluators or ())):
        issues.append("policy_authorized_evaluators_invalid")
    for field in ("evaluation_epoch", "maximum_request_age"):
        if _nat(policy.get(field), positive=field == "maximum_request_age") is None:
            issues.append("policy_nat_invalid:" + field)
    for field in (
        "minimum_independent_verification_pass_rate_delta_basis_points",
        "minimum_verified_patch_count_delta",
        "maximum_typecheck_first_failure_count_delta",
        "maximum_repeated_error_fingerprint_count_delta",
        "maximum_cases_with_repeated_error_fingerprint_delta",
        "maximum_repair_cycles_per_verified_patch_delta_basis_points",
        "maximum_provider_calls_per_verified_patch_delta_basis_points",
        "maximum_generated_output_bytes_per_verified_patch_delta_basis_points",
    ):
        if _integer(policy.get(field)) is None:
            issues.append("policy_integer_invalid:" + field)
    for field in (
        "require_distinct_dataset_digests",
        "require_equal_case_count",
        "require_defined_ratio_deltas",
        "allow_read_only_comparison",
    ):
        if policy.get(field) is not True:
            issues.append("policy_required_true:" + field)
    for field in (
        "allow_historical_code_reexecution",
        "allow_provider_invocation",
        "allow_verification_runner_invocation",
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


def _ratio_basis_points(metrics: Mapping[str, Any], path: tuple[str, ...]) -> int | None:
    value: Any = metrics
    for key in path:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    if not isinstance(value, Mapping) or value.get("defined") is not True:
        return None
    basis_points = value.get("basis_points")
    return basis_points if isinstance(basis_points, int) and not isinstance(basis_points, bool) else None


def _delta(successor: int, baseline: int) -> int:
    return successor - baseline


def _build_comparison_metrics(
    baseline: Mapping[str, Any],
    successor: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    stage_deltas: dict[str, int] = {}
    for stage in STAGE_NAMES:
        baseline_bp = _ratio_basis_points(
            baseline, ("stage_metrics", stage, "conditional_pass_rate")
        )
        successor_bp = _ratio_basis_points(
            successor, ("stage_metrics", stage, "conditional_pass_rate")
        )
        if baseline_bp is None or successor_bp is None:
            issues.append("stage_ratio_undefined:" + stage)
        else:
            stage_deltas[stage] = _delta(successor_bp, baseline_bp)

    ratio_paths = {
        "independent_verification_pass_rate_delta_basis_points": (
            "independent_verification_metrics",
            "conditional_pass_rate",
        ),
        "repair_green_rate_delta_basis_points": ("repair_green_rate",),
        "repair_cycles_per_verified_patch_delta_basis_points": (
            "repair_cycles_per_verified_patch",
        ),
        "provider_calls_per_verified_patch_delta_basis_points": (
            "provider_calls_per_verified_patch",
        ),
        "generated_output_bytes_per_verified_patch_delta_basis_points": (
            "generated_output_bytes_per_verified_patch",
        ),
    }
    ratio_deltas: dict[str, int] = {}
    for field, path in ratio_paths.items():
        baseline_bp = _ratio_basis_points(baseline, path)
        successor_bp = _ratio_basis_points(successor, path)
        if baseline_bp is None or successor_bp is None:
            issues.append("ratio_undefined:" + field)
        else:
            ratio_deltas[field] = _delta(successor_bp, baseline_bp)

    if issues and policy["require_defined_ratio_deltas"]:
        return None, issues

    first_failure_deltas = {
        stage: _delta(
            successor["first_failure_counts"][stage],
            baseline["first_failure_counts"][stage],
        )
        for stage in (*STAGE_NAMES, "independent_verification")
    }
    metrics = {
        "baseline_metrics_digest": baseline[SOURCE_METRICS_DIGEST_FIELD],
        "successor_metrics_digest": successor[SOURCE_METRICS_DIGEST_FIELD],
        "baseline_case_count": baseline["total_case_count"],
        "successor_case_count": successor["total_case_count"],
        "case_count_delta": _delta(
            successor["total_case_count"], baseline["total_case_count"]
        ),
        "stage_conditional_pass_rate_deltas_basis_points": stage_deltas,
        **ratio_deltas,
        "first_failure_count_deltas": first_failure_deltas,
        "verified_patch_count_delta": _delta(
            successor["verified_patch_count"], baseline["verified_patch_count"]
        ),
        "incomplete_case_count_delta": _delta(
            successor["incomplete_case_count"], baseline["incomplete_case_count"]
        ),
        "distinct_error_fingerprint_count_delta": _delta(
            successor["distinct_error_fingerprint_count"],
            baseline["distinct_error_fingerprint_count"],
        ),
        "repeated_error_fingerprint_count_delta": _delta(
            successor["repeated_error_fingerprint_count"],
            baseline["repeated_error_fingerprint_count"],
        ),
        "cases_with_repeated_error_fingerprint_delta": _delta(
            successor["cases_with_repeated_error_fingerprint"],
            baseline["cases_with_repeated_error_fingerprint"],
        ),
    }
    targets = {
        "independent_verification_pass_rate_target_met":
            metrics["independent_verification_pass_rate_delta_basis_points"]
            >= policy["minimum_independent_verification_pass_rate_delta_basis_points"],
        "verified_patch_count_target_met":
            metrics["verified_patch_count_delta"]
            >= policy["minimum_verified_patch_count_delta"],
        "typecheck_first_failure_target_met":
            metrics["first_failure_count_deltas"]["typecheck"]
            <= policy["maximum_typecheck_first_failure_count_delta"],
        "repeated_error_fingerprint_target_met":
            metrics["repeated_error_fingerprint_count_delta"]
            <= policy["maximum_repeated_error_fingerprint_count_delta"],
        "repeated_error_case_target_met":
            metrics["cases_with_repeated_error_fingerprint_delta"]
            <= policy["maximum_cases_with_repeated_error_fingerprint_delta"],
        "repair_cycle_efficiency_target_met":
            metrics["repair_cycles_per_verified_patch_delta_basis_points"]
            <= policy["maximum_repair_cycles_per_verified_patch_delta_basis_points"],
        "provider_call_efficiency_target_met":
            metrics["provider_calls_per_verified_patch_delta_basis_points"]
            <= policy["maximum_provider_calls_per_verified_patch_delta_basis_points"],
        "generated_output_efficiency_target_met":
            metrics["generated_output_bytes_per_verified_patch_delta_basis_points"]
            <= policy["maximum_generated_output_bytes_per_verified_patch_delta_basis_points"],
    }
    metrics["target_results"] = targets
    metrics["target_count"] = len(targets)
    metrics["targets_met_count"] = sum(targets.values())
    metrics["all_targets_met"] = all(targets.values())
    return seal(metrics, COMPARISON_METRICS_DIGEST_FIELD), []


def build_codeai_generated_patch_error_reduction_comparative_replay_evaluation(
    *,
    baseline_evidence: Mapping[str, Any],
    baseline_receipt: Mapping[str, Any],
    successor_evidence: Mapping[str, Any],
    successor_receipt: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> CodeAIGeneratedPatchErrorReductionComparativeReplayEvaluationResult:
    raw_inputs = {
        "baseline_evidence": baseline_evidence,
        "baseline_receipt": baseline_receipt,
        "successor_evidence": successor_evidence,
        "successor_receipt": successor_receipt,
        "request": request,
        "policy": policy,
    }
    mapped: dict[str, Mapping[str, Any]] = {}
    issues: list[str] = []
    for name, value in raw_inputs.items():
        mapped_value = _mapping(value)
        if mapped_value is None:
            issues.append(name + "_not_mapping")
        else:
            mapped[name] = mapped_value
    if issues:
        return CodeAIGeneratedPatchErrorReductionComparativeReplayEvaluationResult(
            STATUS_BLOCKED, tuple(issues), None, None
        )

    baseline_evidence_map = mapped["baseline_evidence"]
    baseline_receipt_map = mapped["baseline_receipt"]
    successor_evidence_map = mapped["successor_evidence"]
    successor_receipt_map = mapped["successor_receipt"]
    request_map = mapped["request"]
    policy_map = mapped["policy"]

    issues.extend(_validate_request(request_map))
    issues.extend(_validate_policy(policy_map))
    issues.extend(
        _validate_source(baseline_evidence_map, baseline_receipt_map, "baseline")
    )
    issues.extend(
        _validate_source(successor_evidence_map, successor_receipt_map, "successor")
    )

    if not issues:
        source_pairs = (
            (
                "baseline_evidence_digest",
                baseline_evidence_map[SOURCE_EVIDENCE_DIGEST_FIELD],
                "expected_baseline_evidence_digest",
            ),
            (
                "baseline_receipt_digest",
                baseline_receipt_map[SOURCE_RECEIPT_DIGEST_FIELD],
                "expected_baseline_receipt_digest",
            ),
            (
                "successor_evidence_digest",
                successor_evidence_map[SOURCE_EVIDENCE_DIGEST_FIELD],
                "expected_successor_evidence_digest",
            ),
            (
                "successor_receipt_digest",
                successor_receipt_map[SOURCE_RECEIPT_DIGEST_FIELD],
                "expected_successor_receipt_digest",
            ),
        )
        for request_field, actual, policy_field in source_pairs:
            if request_map[request_field] != actual:
                issues.append("request_source_correspondence_mismatch:" + request_field)
            if policy_map[policy_field] != actual:
                issues.append("policy_source_correspondence_mismatch:" + policy_field)
        repository = baseline_evidence_map["repository_full_name"]
        if successor_evidence_map["repository_full_name"] != repository:
            issues.append("source_repository_mismatch")
        if request_map["repository_full_name"] != repository:
            issues.append("request_repository_correspondence_mismatch")
        if policy_map["expected_repository_full_name"] != repository:
            issues.append("policy_repository_correspondence_mismatch")
        if request_map["evaluator_id"] not in policy_map["authorized_evaluator_ids"]:
            issues.append("evaluator_not_authorized")
        evaluation_epoch = policy_map["evaluation_epoch"]
        request_epoch = request_map["request_created_epoch"]
        if evaluation_epoch < request_epoch:
            issues.append("request_from_future")
        elif evaluation_epoch - request_epoch > policy_map["maximum_request_age"]:
            issues.append("request_stale")
        if (
            policy_map["require_distinct_dataset_digests"]
            and baseline_evidence_map["dataset_digest"]
            == successor_evidence_map["dataset_digest"]
        ):
            issues.append("source_dataset_digests_not_distinct")
        if (
            policy_map["require_equal_case_count"]
            and baseline_evidence_map["evaluated_case_count"]
            != successor_evidence_map["evaluated_case_count"]
        ):
            issues.append("source_case_count_mismatch")

    if issues:
        return CodeAIGeneratedPatchErrorReductionComparativeReplayEvaluationResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
        )

    comparison_metrics, metric_issues = _build_comparison_metrics(
        baseline_evidence_map["metrics"],
        successor_evidence_map["metrics"],
        policy_map,
    )
    if comparison_metrics is None:
        return CodeAIGeneratedPatchErrorReductionComparativeReplayEvaluationResult(
            STATUS_BLOCKED, tuple(sorted(set(metric_issues))), None, None
        )

    confirmed = comparison_metrics["all_targets_met"]
    disposition = DISPOSITION_CONFIRMED if confirmed else DISPOSITION_NOT_CONFIRMED
    evidence = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "comparison_id": request_map["comparison_id"],
            "repository_full_name": baseline_evidence_map["repository_full_name"],
            "baseline_evaluation_id": baseline_evidence_map["evaluation_id"],
            "successor_evaluation_id": successor_evidence_map["evaluation_id"],
            "baseline_dataset_digest": baseline_evidence_map["dataset_digest"],
            "successor_dataset_digest": successor_evidence_map["dataset_digest"],
            "baseline_evidence_digest": baseline_evidence_map[
                SOURCE_EVIDENCE_DIGEST_FIELD
            ],
            "baseline_receipt_digest": baseline_receipt_map[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            "successor_evidence_digest": successor_evidence_map[
                SOURCE_EVIDENCE_DIGEST_FIELD
            ],
            "successor_receipt_digest": successor_receipt_map[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "comparison_metrics": comparison_metrics,
            "comparison_metrics_digest": comparison_metrics[
                COMPARISON_METRICS_DIGEST_FIELD
            ],
            "error_reduction_confirmed": confirmed,
            "exact_source_correspondence_verified": True,
            "read_only_comparison_completed": True,
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
            "probability_claimed": False,
            "dataset_unbiasedness_claimed": False,
        },
        EVIDENCE_DIGEST_FIELD,
    )
    receipt = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "codeai_disposition": disposition,
            "comparison_id": request_map["comparison_id"],
            "repository_full_name": baseline_evidence_map["repository_full_name"],
            "baseline_evidence_digest": baseline_evidence_map[
                SOURCE_EVIDENCE_DIGEST_FIELD
            ],
            "baseline_receipt_digest": baseline_receipt_map[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            "successor_evidence_digest": successor_evidence_map[
                SOURCE_EVIDENCE_DIGEST_FIELD
            ],
            "successor_receipt_digest": successor_receipt_map[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
            "comparison_metrics_digest": comparison_metrics[
                COMPARISON_METRICS_DIGEST_FIELD
            ],
            "error_reduction_confirmed": confirmed,
            "route_receipt_recorded": True,
            "exact_source_correspondence_verified": True,
            "read_only_comparison_completed": True,
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
            "probability_claimed": False,
            "dataset_unbiasedness_claimed": False,
        },
        RECEIPT_DIGEST_FIELD,
    )
    return CodeAIGeneratedPatchErrorReductionComparativeReplayEvaluationResult(
        STATUS_READY, (), evidence, receipt
    )
