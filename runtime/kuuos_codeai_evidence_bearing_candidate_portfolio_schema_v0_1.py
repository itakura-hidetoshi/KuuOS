from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    DISPOSITION_REPAIRABLE,
    REPORT_DIGEST_FIELD as PREFLIGHT_REPORT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as PREFLIGHT_RECEIPT_DIGEST_FIELD,
    SEVERITY_HOLD,
    SEVERITY_REJECT,
    SEVERITY_REPAIRABLE,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Evidence-Bearing Candidate Portfolio v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_PORTFOLIO_ONLY = "evidence_portfolio_only"
PORTFOLIO_DISPOSITION = "evidence_bearing_candidate_portfolio_normalized"

REQUEST_DIGEST_FIELD = "codeai_evidence_bearing_candidate_portfolio_request_digest"
POLICY_DIGEST_FIELD = "codeai_evidence_bearing_candidate_portfolio_policy_digest"
PORTFOLIO_DIGEST_FIELD = "codeai_evidence_bearing_candidate_portfolio_digest"
RECEIPT_DIGEST_FIELD = "codeai_evidence_bearing_candidate_portfolio_receipt_digest"

CLASSIFICATIONS = (
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_REPAIRABLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
)
SEVERITIES = (SEVERITY_REPAIRABLE, SEVERITY_HOLD, SEVERITY_REJECT)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CodeAIEvidenceBearingCandidatePortfolioResult:
    status: str
    issues: tuple[str, ...]
    portfolio: dict[str, Any] | None
    receipt: dict[str, Any] | None


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    digest = value.get(field)
    return isinstance(digest, str) and SHA256.fullmatch(digest) is not None and digest == digest_without(value, field)


def classification_flags(classification: str) -> dict[str, bool]:
    return {
        "admissible": classification == DISPOSITION_ADMISSIBLE,
        "repair_required": classification == DISPOSITION_REPAIRABLE,
        "held": classification == DISPOSITION_HOLD,
        "rejected": classification == DISPOSITION_REJECTED,
    }


def route_for(classification: str) -> str:
    return {
        DISPOSITION_ADMISSIBLE: "admissible_evidence_route",
        DISPOSITION_REPAIRABLE: "repairable_evidence_route",
        DISPOSITION_HOLD: "hold_evidence_route",
        DISPOSITION_REJECTED: "rejected_evidence_route",
    }[classification]


def _validate_findings(report: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    findings = report.get("findings")
    counts = report.get("finding_counts")
    if not isinstance(findings, list) or not isinstance(counts, Mapping):
        return ["preflight_finding_evidence_invalid"]
    actual = {severity: 0 for severity in SEVERITIES}
    for index, finding in enumerate(findings):
        if not isinstance(finding, Mapping):
            issues.append(f"preflight_finding[{index}]_not_mapping")
            continue
        if finding.get("severity") not in SEVERITIES:
            issues.append(f"preflight_finding[{index}]_severity_invalid")
        else:
            actual[finding["severity"]] += 1
        for field in ("code", "path", "operation_id", "detail"):
            if not isinstance(finding.get(field), str):
                issues.append(f"preflight_finding[{index}]_{field}_invalid")
    if dict(counts) != actual:
        issues.append("preflight_finding_counts_mismatch")
    return issues


def validate_preflight_report(report: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        if not digest_ok(report, PREFLIGHT_REPORT_DIGEST_FIELD):
            issues.append("preflight_report_digest_mismatch")
        classification = report["codeai_disposition"]
        if classification not in CLASSIFICATIONS:
            issues.append("preflight_report_classification_invalid")
        elif any(report.get(field) is not expected for field, expected in classification_flags(classification).items()):
            issues.append("preflight_report_classification_flags_mismatch")
        if report["operating_mode"] != "static_preflight_only":
            issues.append("preflight_report_mode_invalid")
        for field in (
            "static_admissibility_preflight_completed",
            "typed_ir_lineage_verified",
            "repository_snapshot_read_only",
            "result_snapshot_ephemeral",
        ):
            if report[field] is not True:
                issues.append("preflight_report_required_true:" + field)
        for field in (
            "provider_invoked",
            "verification_runner_invoked",
            "repository_mutation_performed",
            "git_effect_performed",
            "candidate_selected",
            "candidate_selection_authority_granted",
            "execution_authority_granted",
            "merge_authority_granted",
            "deployment_authority_granted",
            "static_preflight_treated_as_correctness_proof",
        ):
            if report[field] is not False:
                issues.append("preflight_report_required_false:" + field)
        if not SHA40.fullmatch(report["source_commit_sha"]):
            issues.append("preflight_report_source_commit_invalid")
        for field in (
            "typed_edit_ir_digest",
            "typed_edit_ir_receipt_digest",
            "source_repository_snapshot_digest",
            "result_repository_snapshot_digest",
        ):
            if not SHA256.fullmatch(report[field]):
                issues.append("preflight_report_digest_field_invalid:" + field)
        if not strings(report["changed_paths"]):
            issues.append("preflight_report_changed_paths_invalid")
        if not isinstance(report["operation_count"], int) or isinstance(report["operation_count"], bool) or report["operation_count"] < 0:
            issues.append("preflight_report_operation_count_invalid")
        issues.extend(_validate_findings(report))
    except (KeyError, TypeError, AttributeError):
        issues.append("preflight_report_required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_preflight_receipt(receipt: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        if not digest_ok(receipt, PREFLIGHT_RECEIPT_DIGEST_FIELD):
            issues.append("preflight_receipt_digest_mismatch")
        classification = receipt["codeai_disposition"]
        if classification not in CLASSIFICATIONS:
            issues.append("preflight_receipt_classification_invalid")
        elif any(receipt.get(field) is not expected for field, expected in classification_flags(classification).items()):
            issues.append("preflight_receipt_classification_flags_mismatch")
        for field in (
            "route_receipt_recorded",
            "static_admissibility_report_emitted",
            "repository_snapshot_read_only",
            "result_snapshot_ephemeral",
        ):
            if receipt[field] is not True:
                issues.append("preflight_receipt_required_true:" + field)
        for field in (
            "provider_invoked",
            "verification_runner_invoked",
            "repository_mutation_performed",
            "git_effect_performed",
            "candidate_selected",
            "candidate_selection_authority_granted",
            "execution_authority_granted",
            "merge_authority_granted",
            "deployment_authority_granted",
        ):
            if receipt[field] is not False:
                issues.append("preflight_receipt_required_false:" + field)
        if not SHA256.fullmatch(receipt["static_admissibility_report_digest"]):
            issues.append("preflight_receipt_report_digest_invalid")
    except (KeyError, TypeError, AttributeError):
        issues.append("preflight_receipt_required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_request(request: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        if not digest_ok(request, REQUEST_DIGEST_FIELD):
            issues.append("portfolio_request_digest_mismatch")
        if not SHA40.fullmatch(request["source_commit_sha"]):
            issues.append("portfolio_request_source_commit_invalid")
        if not SHA256.fullmatch(request["source_repository_snapshot_digest"]):
            issues.append("portfolio_request_snapshot_digest_invalid")
        if not isinstance(request["request_created_epoch"], int) or isinstance(request["request_created_epoch"], bool):
            issues.append("portfolio_request_epoch_invalid")
        if not isinstance(request["claims_authority"], bool):
            issues.append("portfolio_request_claims_authority_invalid")
        if not strings(request["unresolved_portfolio_questions"]):
            issues.append("portfolio_request_questions_invalid")
        candidate_requests = request["candidate_requests"]
        if not isinstance(candidate_requests, list) or not candidate_requests:
            issues.append("portfolio_request_candidates_invalid")
        else:
            ids: list[str] = []
            sequences: list[int] = []
            for index, candidate in enumerate(candidate_requests):
                if not isinstance(candidate, Mapping):
                    issues.append(f"portfolio_request_candidate[{index}]_not_mapping")
                    continue
                ids.append(candidate.get("candidate_id"))
                sequences.append(candidate.get("candidate_sequence"))
                if not isinstance(candidate.get("candidate_id"), str) or not candidate["candidate_id"]:
                    issues.append(f"portfolio_request_candidate[{index}]_id_invalid")
                if not isinstance(candidate.get("candidate_sequence"), int) or isinstance(candidate["candidate_sequence"], bool):
                    issues.append(f"portfolio_request_candidate[{index}]_sequence_invalid")
                for field in (
                    "expected_typed_edit_ir_digest",
                    "expected_static_admissibility_report_digest",
                    "expected_preflight_receipt_digest",
                ):
                    if not isinstance(candidate.get(field), str) or SHA256.fullmatch(candidate[field]) is None:
                        issues.append(f"portfolio_request_candidate[{index}]_{field}_invalid")
            if len(ids) != len(set(ids)):
                issues.append("portfolio_request_duplicate_candidate_id")
            if sorted(sequences) != list(range(1, len(candidate_requests) + 1)):
                issues.append("portfolio_request_sequence_not_contiguous")
    except (KeyError, TypeError, AttributeError):
        issues.append("portfolio_request_required_field_missing_or_invalid")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        if not digest_ok(policy, POLICY_DIGEST_FIELD):
            issues.append("portfolio_policy_digest_mismatch")
        if not SHA40.fullmatch(policy["expected_source_commit_sha"]):
            issues.append("portfolio_policy_source_commit_invalid")
        if not SHA256.fullmatch(policy["expected_source_repository_snapshot_digest"]):
            issues.append("portfolio_policy_snapshot_digest_invalid")
        for field in (
            "evaluation_epoch",
            "maximum_request_age",
            "maximum_candidates",
            "maximum_total_findings",
            "maximum_total_changed_paths",
        ):
            if not isinstance(policy[field], int) or isinstance(policy[field], bool) or policy[field] <= 0:
                issues.append("portfolio_policy_integer_invalid:" + field)
        for field in (
            "require_exact_lineage",
            "require_classification_preservation",
            "require_finding_evidence_preservation",
            "allow_ranking",
            "allow_candidate_selection",
            "allow_verification_runner_invocation",
            "allow_repair_execution",
            "allow_execution_authority",
            "allow_git_authority",
        ):
            if not isinstance(policy[field], bool):
                issues.append("portfolio_policy_boolean_invalid:" + field)
    except (KeyError, TypeError, AttributeError):
        issues.append("portfolio_policy_required_field_missing_or_invalid")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEvidenceBearingCandidatePortfolioResult",
    "canonical_digest",
    "canonical_json",
    "classification_flags",
    "digest_without",
    "mapping",
    "route_for",
    "seal",
    "validate_policy",
    "validate_preflight_receipt",
    "validate_preflight_report",
    "validate_request",
]
