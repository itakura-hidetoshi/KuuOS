from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    CATEGORY_BASELINE,
    CATEGORY_ERROR_FREE,
    CATEGORY_ERROR_SPECIFIC,
    CATEGORY_NOVELTY,
    CATEGORY_ROUTE,
    OBLIGATION_CATEGORIES,
    OBLIGATION_DIGEST_FIELD,
    PLAN_DIGEST_FIELD as STRENGTHENING_PLAN_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as STRENGTHENING_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_evidence_weighted_selection_abstention_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Evidence-Weighted Selection and Abstention v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_SELECTION_ONLY = "evidence_weighted_selection_and_abstention_only"

DECISION_SELECTED = "selected"
DECISION_ABSTAINED = "abstained"
DECISIONS = (DECISION_SELECTED, DECISION_ABSTAINED)

REASON_SELECTED = "eligible_candidate_selected"
REASON_NO_ELIGIBLE = "no_eligible_candidate"
REASON_BELOW_THRESHOLD = "top_score_below_threshold"
REASON_INSUFFICIENT_MARGIN = "insufficient_score_margin"
REASON_TIED_TOP = "tied_top_score"
DECISION_REASONS = (
    REASON_SELECTED,
    REASON_NO_ELIGIBLE,
    REASON_BELOW_THRESHOLD,
    REASON_INSUFFICIENT_MARGIN,
    REASON_TIED_TOP,
)

OUTCOME_PASSED = "passed"
OUTCOME_FAILED = "failed"
OUTCOME_INCONCLUSIVE = "inconclusive"
OUTCOME_SKIPPED = "skipped"
EVIDENCE_OUTCOMES = (
    OUTCOME_PASSED,
    OUTCOME_FAILED,
    OUTCOME_INCONCLUSIVE,
    OUTCOME_SKIPPED,
)

REQUEST_DIGEST_FIELD = "codeai_evidence_weighted_selection_request_digest"
POLICY_DIGEST_FIELD = "codeai_evidence_weighted_selection_policy_digest"
EVIDENCE_PACKET_DIGEST_FIELD = "codeai_evidence_weighted_selection_evidence_packet_digest"
EVIDENCE_RECORD_DIGEST_FIELD = "codeai_evidence_weighted_selection_evidence_record_digest"
DECISION_DIGEST_FIELD = "codeai_evidence_weighted_selection_decision_digest"
RECEIPT_DIGEST_FIELD = "codeai_evidence_weighted_selection_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CodeAIEvidenceWeightedSelectionAbstentionResult:
    status: str
    issues: tuple[str, ...]
    decision: dict[str, Any] | None
    receipt: dict[str, Any] | None


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    digest = value.get(field)
    return isinstance(digest, str) and SHA256.fullmatch(digest) is not None and digest == digest_without(value, field)


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def positive_int(value: Any) -> bool:
    return nonnegative_int(value) and value > 0


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "selection_id",
        "selection_revision",
        "repository_full_name",
        "source_commit_sha",
        "strengthening_plan_digest",
        "strengthening_receipt_digest",
        "evidence_packet_digest",
        "request_created_epoch",
        "unresolved_selection_questions",
        "claims_execution_authority",
        "claims_git_authority",
        REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("selection_request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("selection_request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("selection_request_profile_invalid")
    for field in ("selection_id", "selection_revision", "repository_full_name"):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("selection_request_string_invalid:" + field)
    if not isinstance(request["source_commit_sha"], str) or SHA40.fullmatch(request["source_commit_sha"]) is None:
        issues.append("selection_request_source_commit_invalid")
    for field in ("strengthening_plan_digest", "strengthening_receipt_digest", "evidence_packet_digest"):
        if not isinstance(request[field], str) or SHA256.fullmatch(request[field]) is None:
            issues.append("selection_request_digest_invalid:" + field)
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("selection_request_epoch_invalid")
    if not unique_strings(request["unresolved_selection_questions"]):
        issues.append("selection_request_questions_invalid")
    for field in ("claims_execution_authority", "claims_git_authority"):
        if not isinstance(request[field], bool):
            issues.append("selection_request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("selection_request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_strengthening_plan_digest",
        "expected_strengthening_receipt_digest",
        "expected_evidence_packet_digest",
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_evidence_age",
        "maximum_candidates",
        "maximum_evidence_records",
        "minimum_evidence_score",
        "minimum_score_margin",
        "category_weights",
        "require_exact_lineage",
        "require_complete_obligation_coverage",
        "require_independent_runner",
        "require_independent_reviewer",
        "require_isolated_execution",
        "require_source_correspondence",
        "require_admissible_source_classification",
        "require_all_obligations_passed",
        "allow_selection_decision",
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
        POLICY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(policy)
    extra = set(policy).difference(required)
    if missing:
        issues.append("selection_policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("selection_policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("selection_policy_profile_invalid")
    if not isinstance(policy["expected_repository_full_name"], str) or not policy["expected_repository_full_name"]:
        issues.append("selection_policy_repository_invalid")
    if not isinstance(policy["expected_source_commit_sha"], str) or SHA40.fullmatch(policy["expected_source_commit_sha"]) is None:
        issues.append("selection_policy_source_commit_invalid")
    for field in (
        "expected_strengthening_plan_digest",
        "expected_strengthening_receipt_digest",
        "expected_evidence_packet_digest",
    ):
        if not isinstance(policy[field], str) or SHA256.fullmatch(policy[field]) is None:
            issues.append("selection_policy_digest_invalid:" + field)
    for field in (
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_evidence_age",
        "maximum_candidates",
        "maximum_evidence_records",
        "minimum_evidence_score",
        "minimum_score_margin",
    ):
        if not positive_int(policy[field]):
            issues.append("selection_policy_positive_integer_invalid:" + field)
    weights = policy["category_weights"]
    if not isinstance(weights, Mapping) or set(weights) != set(OBLIGATION_CATEGORIES):
        issues.append("selection_policy_category_weights_invalid")
    elif any(not positive_int(weights[category]) for category in OBLIGATION_CATEGORIES):
        issues.append("selection_policy_category_weight_invalid")
    for field in (
        "require_exact_lineage",
        "require_complete_obligation_coverage",
        "require_independent_runner",
        "require_independent_reviewer",
        "require_isolated_execution",
        "require_source_correspondence",
        "require_admissible_source_classification",
        "require_all_obligations_passed",
        "allow_selection_decision",
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    ):
        if not isinstance(policy[field], bool):
            issues.append("selection_policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("selection_policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEvidenceWeightedSelectionAbstentionResult",
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
