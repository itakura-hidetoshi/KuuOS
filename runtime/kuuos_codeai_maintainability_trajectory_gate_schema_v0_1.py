from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_DIGEST_FIELD as SOURCE_SELECTION_DECISION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_SELECTION_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_maintainability_trajectory_gate_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Maintainability Trajectory Gate v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_GATE_ONLY = "maintainability_trajectory_gate_only"
DISPOSITION_COMPLETED = "maintainability_trajectory_gate_completed"

GATE_ADMITTED = "admitted"
GATE_HELD = "held"
GATE_DECISIONS = (GATE_ADMITTED, GATE_HELD)

REASON_ADMITTED = "bounded_maintainability_trajectory_admitted"
REASON_AXIS_LIMIT = "axis_regression_limit_exceeded"
REASON_TOTAL_REGRESSION = "total_regression_limit_exceeded"
REASON_INSUFFICIENT_IMPROVEMENT = "insufficient_improved_axes"
GATE_REASONS = (
    REASON_ADMITTED,
    REASON_AXIS_LIMIT,
    REASON_TOTAL_REGRESSION,
    REASON_INSUFFICIENT_IMPROVEMENT,
)

AXIS_STRUCTURAL_COMPLEXITY = "structural_complexity"
AXIS_DEPENDENCY_SURFACE = "dependency_surface"
AXIS_DUPLICATION = "duplication"
AXIS_TEST_BURDEN = "test_burden"
AXIS_PROOF_BURDEN = "proof_burden"
AXIS_REPAIR_RECURRENCE = "repair_recurrence"
MAINTAINABILITY_AXES = (
    AXIS_STRUCTURAL_COMPLEXITY,
    AXIS_DEPENDENCY_SURFACE,
    AXIS_DUPLICATION,
    AXIS_TEST_BURDEN,
    AXIS_PROOF_BURDEN,
    AXIS_REPAIR_RECURRENCE,
)

REQUEST_DIGEST_FIELD = "codeai_maintainability_trajectory_gate_request_digest"
POLICY_DIGEST_FIELD = "codeai_maintainability_trajectory_gate_policy_digest"
EVIDENCE_PACKET_DIGEST_FIELD = "codeai_maintainability_trajectory_evidence_packet_digest"
EVIDENCE_RECORD_DIGEST_FIELD = "codeai_maintainability_trajectory_evidence_record_digest"
DECISION_DIGEST_FIELD = "codeai_maintainability_trajectory_gate_decision_digest"
RECEIPT_DIGEST_FIELD = "codeai_maintainability_trajectory_gate_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,127}$")


@dataclass(frozen=True)
class CodeAIMaintainabilityTrajectoryGateResult:
    status: str
    issues: tuple[str, ...]
    decision: dict[str, Any] | None
    receipt: dict[str, Any] | None


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


def _digest_field_ok(value: Mapping[str, Any], field: str) -> bool:
    item = value.get(field)
    return isinstance(item, str) and SHA256.fullmatch(item) is not None


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "gate_request_id",
        "gate_request_revision",
        "selection_decision_digest",
        "selection_receipt_digest",
        "memory_snapshot_digest",
        "memory_receipt_digest",
        "trajectory_evidence_packet_digest",
        "repository_full_name",
        "source_commit_sha",
        "source_repository_snapshot_digest",
        "selected_candidate_id",
        "selected_candidate_digest",
        "request_created_epoch",
        "unresolved_maintainability_questions",
        "claims_selection_authority",
        "claims_verification_authority",
        "claims_repair_authority",
        "claims_execution_authority",
        "claims_git_authority",
        REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("maintainability_request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("maintainability_request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("maintainability_request_profile_invalid")
    for field in ("gate_request_id", "gate_request_revision", "selected_candidate_id"):
        if not isinstance(request[field], str) or IDENTIFIER.fullmatch(request[field]) is None:
            issues.append("maintainability_request_identifier_invalid:" + field)
    if not isinstance(request["repository_full_name"], str) or not request["repository_full_name"]:
        issues.append("maintainability_request_repository_invalid")
    if not isinstance(request["source_commit_sha"], str) or SHA40.fullmatch(request["source_commit_sha"]) is None:
        issues.append("maintainability_request_source_commit_invalid")
    for field in (
        "selection_decision_digest",
        "selection_receipt_digest",
        "memory_snapshot_digest",
        "memory_receipt_digest",
        "trajectory_evidence_packet_digest",
        "source_repository_snapshot_digest",
        "selected_candidate_digest",
    ):
        if not _digest_field_ok(request, field):
            issues.append("maintainability_request_digest_invalid:" + field)
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("maintainability_request_epoch_invalid")
    if not unique_strings(request["unresolved_maintainability_questions"]):
        issues.append("maintainability_request_questions_invalid")
    for field in (
        "claims_selection_authority",
        "claims_verification_authority",
        "claims_repair_authority",
        "claims_execution_authority",
        "claims_git_authority",
    ):
        if not isinstance(request[field], bool):
            issues.append("maintainability_request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("maintainability_request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "expected_selection_decision_digest",
        "expected_selection_receipt_digest",
        "expected_memory_snapshot_digest",
        "expected_memory_receipt_digest",
        "expected_trajectory_evidence_packet_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_source_repository_snapshot_digest",
        "expected_selected_candidate_id",
        "expected_selected_candidate_digest",
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_evidence_age",
        "maximum_trajectory_records",
        "required_axes",
        "maximum_allowed_increase",
        "maximum_total_regression",
        "minimum_improved_axes",
        "require_source_selection_selected",
        "require_exact_lineage",
        "require_complete_axis_coverage",
        "require_independent_assessor",
        "require_independent_reviewer",
        "require_isolated_candidate_evaluation",
        "require_source_correspondence",
        "require_exact_memory_binding",
        "require_live_repository_unchanged",
        "allow_maintainability_gate_decision",
        "allow_memory_threshold_waiver",
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_selection_authority",
        "allow_verification_authority",
        "allow_repair_authority",
        "allow_execution_authority",
        "allow_git_authority",
        POLICY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(policy)
    extra = set(policy).difference(required)
    if missing:
        issues.append("maintainability_policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("maintainability_policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("maintainability_policy_profile_invalid")
    if not isinstance(policy["expected_repository_full_name"], str) or not policy["expected_repository_full_name"]:
        issues.append("maintainability_policy_repository_invalid")
    if not isinstance(policy["expected_source_commit_sha"], str) or SHA40.fullmatch(policy["expected_source_commit_sha"]) is None:
        issues.append("maintainability_policy_source_commit_invalid")
    if not isinstance(policy["expected_selected_candidate_id"], str) or IDENTIFIER.fullmatch(policy["expected_selected_candidate_id"]) is None:
        issues.append("maintainability_policy_candidate_id_invalid")
    for field in (
        "expected_selection_decision_digest",
        "expected_selection_receipt_digest",
        "expected_memory_snapshot_digest",
        "expected_memory_receipt_digest",
        "expected_trajectory_evidence_packet_digest",
        "expected_source_repository_snapshot_digest",
        "expected_selected_candidate_digest",
    ):
        if not _digest_field_ok(policy, field):
            issues.append("maintainability_policy_digest_invalid:" + field)
    for field in (
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_evidence_age",
        "maximum_trajectory_records",
    ):
        if not positive_int(policy[field]):
            issues.append("maintainability_policy_positive_integer_invalid:" + field)
    if not nonnegative_int(policy["maximum_total_regression"]):
        issues.append("maintainability_policy_total_regression_invalid")
    if not positive_int(policy["minimum_improved_axes"]):
        issues.append("maintainability_policy_minimum_improved_axes_invalid")
    if policy["minimum_improved_axes"] > len(MAINTAINABILITY_AXES):
        issues.append("maintainability_policy_minimum_improved_axes_excessive")
    if policy["required_axes"] != list(MAINTAINABILITY_AXES):
        issues.append("maintainability_policy_required_axes_invalid")
    limits = policy["maximum_allowed_increase"]
    if not isinstance(limits, Mapping) or set(limits) != set(MAINTAINABILITY_AXES):
        issues.append("maintainability_policy_axis_limits_invalid")
    elif any(not nonnegative_int(limits[axis]) for axis in MAINTAINABILITY_AXES):
        issues.append("maintainability_policy_axis_limit_value_invalid")
    for field in (
        "require_source_selection_selected",
        "require_exact_lineage",
        "require_complete_axis_coverage",
        "require_independent_assessor",
        "require_independent_reviewer",
        "require_isolated_candidate_evaluation",
        "require_source_correspondence",
        "require_exact_memory_binding",
        "require_live_repository_unchanged",
        "allow_maintainability_gate_decision",
        "allow_memory_threshold_waiver",
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_selection_authority",
        "allow_verification_authority",
        "allow_repair_authority",
        "allow_execution_authority",
        "allow_git_authority",
    ):
        if not isinstance(policy[field], bool):
            issues.append("maintainability_policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("maintainability_policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIMaintainabilityTrajectoryGateResult",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "digest_ok",
    "mapping",
    "nonnegative_int",
    "positive_int",
    "seal",
    "unique_strings",
    "validate_policy",
    "validate_request",
]
