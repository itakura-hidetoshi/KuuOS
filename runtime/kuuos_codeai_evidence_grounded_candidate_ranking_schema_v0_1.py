from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    CLASSIFICATIONS,
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    DISPOSITION_REPAIRABLE,
    PORTFOLIO_DIGEST_FIELD as SOURCE_PORTFOLIO_DIGEST_FIELD,
    PORTFOLIO_DISPOSITION as SOURCE_PORTFOLIO_DISPOSITION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    SEVERITIES,
    SHA40,
    SHA256,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_evidence_grounded_candidate_ranking_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Evidence-Grounded Candidate Ranking v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_RANKING_ONLY = "evidence_ranking_only"
RANKING_DISPOSITION = "evidence_grounded_candidate_ranking_completed"
RANKING_PURPOSE = "independent_verification_prioritization"
RANKING_STRATEGY = "classification_then_evidence_burden"

REQUEST_DIGEST_FIELD = "codeai_evidence_grounded_candidate_ranking_request_digest"
POLICY_DIGEST_FIELD = "codeai_evidence_grounded_candidate_ranking_policy_digest"
RANKING_DIGEST_FIELD = "codeai_evidence_grounded_candidate_ranking_digest"
RECEIPT_DIGEST_FIELD = "codeai_evidence_grounded_candidate_ranking_receipt_digest"

CLASSIFICATION_PRIORITY = {
    DISPOSITION_ADMISSIBLE: 0,
    DISPOSITION_REPAIRABLE: 1,
    DISPOSITION_HOLD: 2,
    DISPOSITION_REJECTED: 3,
}

_REQUEST_FIELDS = {
    "schema_version",
    "profile_version",
    "ranking_request_id",
    "ranking_request_revision",
    "source_portfolio_digest",
    "source_portfolio_receipt_digest",
    "repository_full_name",
    "source_commit_sha",
    "source_repository_snapshot_digest",
    "ranking_purpose",
    "request_created_epoch",
    "unresolved_ranking_questions",
    "claims_selection_authority",
    REQUEST_DIGEST_FIELD,
}

_POLICY_FIELDS = {
    "schema_version",
    "profile_version",
    "expected_source_portfolio_digest",
    "expected_source_portfolio_receipt_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "expected_source_repository_snapshot_digest",
    "evaluation_epoch",
    "maximum_request_age",
    "maximum_candidates",
    "maximum_total_findings",
    "maximum_total_changed_paths",
    "classification_priority",
    "ranking_strategy",
    "require_exact_lineage",
    "require_classification_preservation",
    "require_finding_evidence_preservation",
    "require_stable_tie_break",
    "allow_candidate_selection",
    "allow_verification_runner_invocation",
    "allow_repair_execution",
    "allow_repository_mutation",
    "allow_execution_authority",
    "allow_git_authority",
    POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIEvidenceGroundedCandidateRankingResult:
    status: str
    issues: tuple[str, ...]
    ranking: dict[str, Any] | None
    receipt: dict[str, Any] | None


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def positive_nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    digest = value.get(field)
    return isinstance(digest, str) and SHA256.fullmatch(digest) is not None and digest == digest_without(value, field)


def exact_fields(value: Mapping[str, Any], expected: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = expected.difference(value)
    extra = set(value).difference(expected)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(request, _REQUEST_FIELDS, "ranking_request")
    if issues:
        return issues
    try:
        if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
            issues.append("ranking_request_profile_invalid")
        for field in ("ranking_request_id", "ranking_request_revision", "repository_full_name"):
            if not isinstance(request[field], str) or not request[field]:
                issues.append("ranking_request_string_invalid:" + field)
        for field in ("source_portfolio_digest", "source_portfolio_receipt_digest", "source_repository_snapshot_digest"):
            if not isinstance(request[field], str) or SHA256.fullmatch(request[field]) is None:
                issues.append("ranking_request_digest_invalid:" + field)
        if not isinstance(request["source_commit_sha"], str) or SHA40.fullmatch(request["source_commit_sha"]) is None:
            issues.append("ranking_request_source_commit_invalid")
        if request["ranking_purpose"] != RANKING_PURPOSE:
            issues.append("ranking_request_purpose_invalid")
        if not isinstance(request["request_created_epoch"], int) or isinstance(request["request_created_epoch"], bool):
            issues.append("ranking_request_epoch_invalid")
        if not unique_strings(request["unresolved_ranking_questions"]):
            issues.append("ranking_request_questions_invalid")
        if not isinstance(request["claims_selection_authority"], bool):
            issues.append("ranking_request_authority_claim_invalid")
        if not digest_ok(request, REQUEST_DIGEST_FIELD):
            issues.append("ranking_request_digest_mismatch")
    except (KeyError, TypeError, AttributeError):
        issues.append("ranking_request_required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(policy, _POLICY_FIELDS, "ranking_policy")
    if issues:
        return issues
    try:
        if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
            issues.append("ranking_policy_profile_invalid")
        for field in (
            "expected_source_portfolio_digest",
            "expected_source_portfolio_receipt_digest",
            "expected_source_repository_snapshot_digest",
        ):
            if not isinstance(policy[field], str) or SHA256.fullmatch(policy[field]) is None:
                issues.append("ranking_policy_digest_invalid:" + field)
        if not isinstance(policy["expected_repository_full_name"], str) or not policy["expected_repository_full_name"]:
            issues.append("ranking_policy_repository_invalid")
        if not isinstance(policy["expected_source_commit_sha"], str) or SHA40.fullmatch(policy["expected_source_commit_sha"]) is None:
            issues.append("ranking_policy_source_commit_invalid")
        for field in (
            "evaluation_epoch",
            "maximum_request_age",
            "maximum_candidates",
            "maximum_total_findings",
            "maximum_total_changed_paths",
        ):
            if not positive_nat(policy[field]):
                issues.append("ranking_policy_positive_nat_invalid:" + field)
        if policy["classification_priority"] != list(CLASSIFICATIONS):
            issues.append("ranking_policy_classification_priority_invalid")
        if policy["ranking_strategy"] != RANKING_STRATEGY:
            issues.append("ranking_policy_strategy_invalid")
        for field in (
            "require_exact_lineage",
            "require_classification_preservation",
            "require_finding_evidence_preservation",
            "require_stable_tie_break",
            "allow_candidate_selection",
            "allow_verification_runner_invocation",
            "allow_repair_execution",
            "allow_repository_mutation",
            "allow_execution_authority",
            "allow_git_authority",
        ):
            if not isinstance(policy[field], bool):
                issues.append("ranking_policy_boolean_invalid:" + field)
        if not digest_ok(policy, POLICY_DIGEST_FIELD):
            issues.append("ranking_policy_digest_mismatch")
    except (KeyError, TypeError, AttributeError):
        issues.append("ranking_policy_required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_source_candidate(candidate: Mapping[str, Any], index: int) -> list[str]:
    prefix = f"source_candidate[{index}]"
    issues: list[str] = []
    try:
        if not isinstance(candidate["candidate_id"], str) or not candidate["candidate_id"]:
            issues.append(prefix + ":candidate_id_invalid")
        if not positive_nat(candidate["candidate_sequence"]):
            issues.append(prefix + ":candidate_sequence_invalid")
        classification = candidate["classification"]
        if classification not in CLASSIFICATIONS:
            issues.append(prefix + ":classification_invalid")
        elif candidate["evidence_route"] != {
            DISPOSITION_ADMISSIBLE: "admissible_evidence_route",
            DISPOSITION_REPAIRABLE: "repairable_evidence_route",
            DISPOSITION_HOLD: "hold_evidence_route",
            DISPOSITION_REJECTED: "rejected_evidence_route",
        }[classification]:
            issues.append(prefix + ":evidence_route_invalid")
        for field in (
            "typed_edit_ir_digest",
            "typed_edit_ir_receipt_digest",
            "static_admissibility_report_digest",
            "preflight_receipt_digest",
            "source_repository_snapshot_digest",
            "result_repository_snapshot_digest",
        ):
            if not isinstance(candidate[field], str) or SHA256.fullmatch(candidate[field]) is None:
                issues.append(prefix + ":digest_invalid:" + field)
        if not isinstance(candidate["source_commit_sha"], str) or SHA40.fullmatch(candidate["source_commit_sha"]) is None:
            issues.append(prefix + ":source_commit_invalid")
        if not isinstance(candidate["repository_full_name"], str) or not candidate["repository_full_name"]:
            issues.append(prefix + ":repository_invalid")
        if not isinstance(candidate["operation_count"], int) or isinstance(candidate["operation_count"], bool) or candidate["operation_count"] < 0:
            issues.append(prefix + ":operation_count_invalid")
        if not unique_strings(candidate["changed_paths"]):
            issues.append(prefix + ":changed_paths_invalid")
        findings = candidate["findings"]
        counts = candidate["finding_counts"]
        if not isinstance(findings, list) or not isinstance(counts, Mapping):
            issues.append(prefix + ":finding_evidence_invalid")
        else:
            actual = {severity: 0 for severity in SEVERITIES}
            for finding_index, finding in enumerate(findings):
                if not isinstance(finding, Mapping) or finding.get("severity") not in SEVERITIES:
                    issues.append(prefix + f":finding[{finding_index}]_invalid")
                else:
                    actual[finding["severity"]] += 1
            if dict(counts) != actual:
                issues.append(prefix + ":finding_counts_mismatch")
        for field in (
            "exact_lineage_verified",
            "classification_preserved",
            "finding_evidence_preserved",
            "preflight_route_receipt_preserved",
        ):
            if candidate[field] is not True:
                issues.append(prefix + ":required_true:" + field)
        for field in (
            "rank_assigned",
            "candidate_selected",
            "verification_runner_invoked",
            "repair_executed",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            if candidate[field] is not False:
                issues.append(prefix + ":required_false:" + field)
    except (KeyError, TypeError, AttributeError):
        issues.append(prefix + ":required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_source_portfolio(portfolio: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        if not digest_ok(portfolio, SOURCE_PORTFOLIO_DIGEST_FIELD):
            issues.append("source_portfolio_digest_mismatch")
        if portfolio["codeai_disposition"] != SOURCE_PORTFOLIO_DISPOSITION:
            issues.append("source_portfolio_disposition_invalid")
        if portfolio["operating_mode"] != "evidence_portfolio_only":
            issues.append("source_portfolio_mode_invalid")
        for field in (
            "evidence_portfolio_normalized",
            "exact_lineage_verified",
            "classification_evidence_preserved",
            "finding_evidence_preserved",
            "preflight_route_receipts_preserved",
        ):
            if portfolio[field] is not True:
                issues.append("source_portfolio_required_true:" + field)
        for field in (
            "ranking_performed",
            "candidate_selected",
            "verification_runner_invoked",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            if portfolio[field] is not False:
                issues.append("source_portfolio_required_false:" + field)
        candidates = portfolio["candidates"]
        if not isinstance(candidates, list) or not candidates:
            issues.append("source_portfolio_candidates_invalid")
        else:
            ids: list[str] = []
            sequences: list[int] = []
            for index, candidate in enumerate(candidates):
                if not isinstance(candidate, Mapping):
                    issues.append(f"source_candidate[{index}]_not_mapping")
                    continue
                issues.extend(validate_source_candidate(candidate, index))
                ids.append(str(candidate.get("candidate_id")))
                sequences.append(candidate.get("candidate_sequence"))
            if len(ids) != len(set(ids)):
                issues.append("source_portfolio_candidate_ids_duplicate")
            if sorted(sequences) != list(range(1, len(candidates) + 1)):
                issues.append("source_portfolio_candidate_sequence_invalid")
            if portfolio["candidate_count"] != len(candidates):
                issues.append("source_portfolio_candidate_count_mismatch")
            if portfolio["candidate_ids"] != ids:
                issues.append("source_portfolio_candidate_ids_mismatch")
    except (KeyError, TypeError, AttributeError):
        issues.append("source_portfolio_required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_source_receipt(receipt: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        if not digest_ok(receipt, SOURCE_RECEIPT_DIGEST_FIELD):
            issues.append("source_receipt_digest_mismatch")
        if receipt["codeai_disposition"] != SOURCE_PORTFOLIO_DISPOSITION:
            issues.append("source_receipt_disposition_invalid")
        if receipt["operating_mode"] != "evidence_portfolio_only":
            issues.append("source_receipt_mode_invalid")
        for field in (
            "route_receipt_recorded",
            "portfolio_emitted",
            "exact_lineage_verified",
            "classification_evidence_preserved",
            "finding_evidence_preserved",
            "preflight_route_receipts_preserved",
        ):
            if receipt[field] is not True:
                issues.append("source_receipt_required_true:" + field)
        for field in (
            "ranking_performed",
            "candidate_selected",
            "verification_runner_invoked",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            if receipt[field] is not False:
                issues.append("source_receipt_required_false:" + field)
        if not isinstance(receipt["evidence_bearing_candidate_portfolio_digest"], str) or SHA256.fullmatch(
            receipt["evidence_bearing_candidate_portfolio_digest"]
        ) is None:
            issues.append("source_receipt_portfolio_digest_invalid")
    except (KeyError, TypeError, AttributeError):
        issues.append("source_receipt_required_field_missing_or_invalid")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEvidenceGroundedCandidateRankingResult",
    "canonical_digest",
    "canonical_json",
    "digest_ok",
    "digest_without",
    "exact_fields",
    "mapping",
    "positive_nat",
    "seal",
    "unique_strings",
    "validate_policy",
    "validate_request",
    "validate_source_candidate",
    "validate_source_portfolio",
    "validate_source_receipt",
]
