from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE,
)
from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    MODE_PORTFOLIO_ONLY,
    PORTFOLIO_DIGEST_FIELD,
    PORTFOLIO_DISPOSITION,
    RECEIPT_DIGEST_FIELD as PORTFOLIO_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    DISPOSITION_COMPLETED as BASELINE_DISPOSITION_COMPLETED,
    EVIDENCE_DIGEST_FIELD as BASELINE_EVIDENCE_DIGEST_FIELD,
    METRICS_DIGEST_FIELD as BASELINE_METRICS_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as BASELINE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import *


def validate_portfolio_pair(portfolio: Mapping[str, Any], receipt: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not digest_ok(portfolio, PORTFOLIO_DIGEST_FIELD):
        issues.append("source_portfolio_digest_mismatch")
    if not digest_ok(receipt, PORTFOLIO_RECEIPT_DIGEST_FIELD):
        issues.append("source_portfolio_receipt_digest_mismatch")
    if portfolio.get("codeai_disposition") != PORTFOLIO_DISPOSITION:
        issues.append("source_portfolio_disposition_invalid")
    if portfolio.get("operating_mode") != MODE_PORTFOLIO_ONLY:
        issues.append("source_portfolio_mode_invalid")
    if receipt.get("evidence_bearing_candidate_portfolio_digest") != portfolio.get(PORTFOLIO_DIGEST_FIELD):
        issues.append("source_portfolio_receipt_correspondence_mismatch")
    for field in (
        "exact_lineage_verified",
        "classification_evidence_preserved",
        "finding_evidence_preserved",
        "preflight_route_receipts_preserved",
    ):
        if portfolio.get(field) is not True or receipt.get(field) is not True:
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
        if portfolio.get(field) is not False or receipt.get(field) is not False:
            issues.append("source_portfolio_required_false:" + field)
    candidates = portfolio.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        issues.append("source_portfolio_candidates_invalid")
        return sorted(set(issues))
    ids = [candidate.get("candidate_id") for candidate in candidates if isinstance(candidate, Mapping)]
    if len(ids) != len(candidates) or len(ids) != len(set(ids)) or ids != portfolio.get("candidate_ids"):
        issues.append("source_portfolio_candidate_ids_invalid")
    if portfolio.get("candidate_count") != len(candidates):
        issues.append("source_portfolio_candidate_count_mismatch")
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            issues.append(f"source_portfolio_candidate[{index}]_not_mapping")
            continue
        findings = candidate.get("findings")
        if not isinstance(findings, list):
            issues.append(f"source_portfolio_candidate[{index}]_findings_invalid")
            continue
        if candidate.get("classification") == DISPOSITION_ADMISSIBLE and findings:
            issues.append(f"source_portfolio_candidate[{index}]_admissible_with_findings")
        for finding_index, finding in enumerate(findings):
            if not isinstance(finding, Mapping):
                issues.append(f"source_portfolio_candidate[{index}]_finding[{finding_index}]_not_mapping")
                continue
            code = finding.get("code")
            severity = finding.get("severity")
            if not isinstance(code, str) or not code:
                issues.append(f"source_portfolio_candidate[{index}]_finding[{finding_index}]_code_invalid")
            if severity not in SEVERITIES:
                issues.append(f"source_portfolio_candidate[{index}]_finding[{finding_index}]_severity_invalid")
    return sorted(set(issues))


def validate_baseline_pair(evidence: Mapping[str, Any], receipt: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not digest_ok(evidence, BASELINE_EVIDENCE_DIGEST_FIELD):
        issues.append("baseline_evidence_digest_mismatch")
    if not digest_ok(receipt, BASELINE_RECEIPT_DIGEST_FIELD):
        issues.append("baseline_receipt_digest_mismatch")
    if receipt.get("codeai_disposition") != BASELINE_DISPOSITION_COMPLETED:
        issues.append("baseline_receipt_disposition_invalid")
    if receipt.get("evidence_digest") != evidence.get(BASELINE_EVIDENCE_DIGEST_FIELD):
        issues.append("baseline_receipt_evidence_correspondence_mismatch")
    metrics = evidence.get("metrics")
    if not isinstance(metrics, Mapping):
        issues.append("baseline_metrics_not_mapping")
    else:
        if not digest_ok(metrics, BASELINE_METRICS_DIGEST_FIELD):
            issues.append("baseline_metrics_digest_mismatch")
        counts = metrics.get("error_fingerprint_counts")
        if not isinstance(counts, Mapping):
            issues.append("baseline_fingerprint_counts_invalid")
        else:
            for fingerprint, count in counts.items():
                if not isinstance(fingerprint, str) or FINGERPRINT.fullmatch(fingerprint) is None:
                    issues.append("baseline_fingerprint_invalid:" + str(fingerprint))
                if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
                    issues.append("baseline_fingerprint_count_invalid:" + str(fingerprint))
    for field in (
        "exact_source_correspondence_verified",
        "read_only_replay_evaluation_completed",
    ):
        if evidence.get(field) is not True or receipt.get(field) is not True:
            issues.append("baseline_required_true:" + field)
    for field in (
        "historical_code_reexecuted",
        "provider_invoked",
        "verification_runner_invoked",
        "repository_mutation_performed",
        "git_effect_performed",
        "selection_authority_granted",
        "successor_stage_authority_granted",
    ):
        if evidence.get(field) is not False or receipt.get(field) is not False:
            issues.append("baseline_required_false:" + field)
    return sorted(set(issues))


def classify_finding(
    *,
    candidate_id: str,
    candidate_sequence: int,
    error_sequence: int,
    finding: Mapping[str, Any],
    baseline_counts: Mapping[str, Any],
) -> dict[str, Any]:
    code = str(finding["code"])
    family, stage = FINDING_TAXONOMY[code]
    severity = str(finding["severity"])
    fingerprint = fingerprint_for(code)
    historical_count = int(baseline_counts.get(fingerprint, 0))
    value = {
        "candidate_id": candidate_id,
        "candidate_sequence": candidate_sequence,
        "error_sequence": error_sequence,
        "source_finding": dict(finding),
        "source_finding_code": code,
        "error_family": family,
        "error_stage": stage,
        "severity": severity,
        "repair_route": repair_route_for(severity),
        "error_fingerprint": fingerprint,
        "baseline_occurrence_count": historical_count,
        "baseline_novelty": NOVELTY_KNOWN if historical_count > 0 else NOVELTY_NOVEL,
        "cause_proven": False,
        "correctness_implication_claimed": False,
        "repair_authority_granted": False,
        "selection_authority_granted": False,
    }
    return seal(value, "typed_error_digest")


def summarize_typed_errors(errors: list[Mapping[str, Any]]) -> dict[str, Any]:
    families = Counter(error["error_family"] for error in errors)
    stages = Counter(error["error_stage"] for error in errors)
    routes = Counter(error["repair_route"] for error in errors)
    novelty = Counter(error["baseline_novelty"] for error in errors)
    severity = Counter(error["severity"] for error in errors)
    return {
        "typed_error_count": len(errors),
        "family_counts": {family: families[family] for family in ERROR_FAMILIES},
        "stage_counts": {stage: stages[stage] for stage in ERROR_STAGES},
        "repair_route_counts": {route: routes[route] for route in REPAIR_ROUTES},
        "novelty_counts": {status: novelty[status] for status in NOVELTY_STATUSES},
        "severity_counts": {item: severity[item] for item in SEVERITIES},
    }


__all__ = [
    "classify_finding",
    "summarize_typed_errors",
    "validate_baseline_pair",
    "validate_portfolio_pair",
]
