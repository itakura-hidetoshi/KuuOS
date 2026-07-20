#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import *
from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_checks_v0_1 import (
    normalize_candidate,
    report_receipt_correspondence_issues,
    route_counts_named,
    summarize,
)


def _blocked(*issues: str) -> CodeAIEvidenceBearingCandidatePortfolioResult:
    return CodeAIEvidenceBearingCandidatePortfolioResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(portfolio: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "portfolio_request_digest",
        "portfolio_policy_digest",
        "repository_full_name",
        "source_commit_sha",
        "source_repository_snapshot_digest",
        "candidate_count",
        "candidate_ids",
        "classification_counts",
        "total_finding_count",
        "total_changed_path_count",
        "codeai_disposition",
    )
    receipt = {key: portfolio[key] for key in keys}
    receipt.update(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "evidence_bearing_candidate_portfolio_digest": portfolio[PORTFOLIO_DIGEST_FIELD],
            "operating_mode": MODE_PORTFOLIO_ONLY,
            "route_receipt_recorded": True,
            "portfolio_emitted": True,
            "exact_lineage_verified": True,
            "classification_evidence_preserved": True,
            "finding_evidence_preserved": True,
            "preflight_route_receipts_preserved": True,
            "provider_invoked": False,
            "ranking_performed": False,
            "candidate_selected": False,
            "verification_runner_invoked": False,
            "repair_executed": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
            "execution_authority_granted": False,
            "git_authority_granted": False,
            "merge_authority_granted": False,
            "deployment_authority_granted": False,
            "portfolio_treated_as_correctness_proof": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        }
    )
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_evidence_bearing_candidate_portfolio(
    *,
    portfolio_request: Any,
    portfolio_policy: Any,
    candidate_preflight_bundles: Any,
) -> CodeAIEvidenceBearingCandidatePortfolioResult:
    request = mapping(portfolio_request)
    policy = mapping(portfolio_policy)
    if request is None or policy is None or not isinstance(candidate_preflight_bundles, list):
        return _blocked("input_not_mapping_or_bundle_list")

    issues = validate_request(request) + validate_policy(policy)
    if issues:
        return _blocked(*issues)

    authority_fields = (
        "allow_ranking",
        "allow_candidate_selection",
        "allow_verification_runner_invocation",
        "allow_repair_execution",
        "allow_execution_authority",
        "allow_git_authority",
    )
    if any(policy[field] for field in authority_fields):
        return _blocked("portfolio_policy_effect_or_authority_enabled")
    if request["claims_authority"]:
        return _blocked("portfolio_request_claims_authority")
    if request["unresolved_portfolio_questions"]:
        return _blocked("portfolio_unresolved_questions_present")
    if not (
        policy["evaluation_epoch"] - policy["maximum_request_age"]
        <= request["request_created_epoch"]
        <= policy["evaluation_epoch"]
    ):
        return _blocked("portfolio_request_window_invalid")
    if len(request["candidate_requests"]) > policy["maximum_candidates"]:
        return _blocked("portfolio_candidate_budget_exceeded")
    if len(candidate_preflight_bundles) != len(request["candidate_requests"]):
        return _blocked("portfolio_bundle_count_mismatch")

    identity_pairs = (
        (request["repository_full_name"], policy["expected_repository_full_name"], "portfolio_repository_policy_mismatch"),
        (request["source_commit_sha"], policy["expected_source_commit_sha"], "portfolio_source_commit_policy_mismatch"),
        (
            request["source_repository_snapshot_digest"],
            policy["expected_source_repository_snapshot_digest"],
            "portfolio_snapshot_policy_mismatch",
        ),
    )
    identity_issues = [code for left, right, code in identity_pairs if left != right]
    if identity_issues:
        return _blocked(*identity_issues)

    bundles_by_id: dict[str, Any] = {}
    for index, bundle in enumerate(candidate_preflight_bundles):
        if not isinstance(bundle, dict):
            return _blocked(f"candidate_bundle[{index}]_not_mapping")
        candidate_id = bundle.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            return _blocked(f"candidate_bundle[{index}]_id_invalid")
        if candidate_id in bundles_by_id:
            return _blocked("candidate_bundle_duplicate_candidate_id")
        bundles_by_id[candidate_id] = bundle

    request_ids = {item["candidate_id"] for item in request["candidate_requests"]}
    if set(bundles_by_id) != request_ids:
        return _blocked("candidate_bundle_id_set_mismatch")

    candidates: list[dict[str, Any]] = []
    for candidate_request in sorted(request["candidate_requests"], key=lambda item: item["candidate_sequence"]):
        candidate_id = candidate_request["candidate_id"]
        bundle = bundles_by_id[candidate_id]
        report = mapping(bundle.get("preflight_report"))
        receipt = mapping(bundle.get("preflight_receipt"))
        if report is None or receipt is None:
            return _blocked("candidate_preflight_evidence_not_mapping:" + candidate_id)

        candidate_issues = [
            f"{candidate_id}:{issue}"
            for issue in (
                validate_preflight_report(report)
                + validate_preflight_receipt(receipt)
                + report_receipt_correspondence_issues(report, receipt)
            )
        ]
        if candidate_issues:
            return _blocked(*candidate_issues)

        correspondence = (
            (
                candidate_request["expected_typed_edit_ir_digest"],
                report["typed_edit_ir_digest"],
                "typed_ir_digest_mismatch",
            ),
            (
                candidate_request["expected_static_admissibility_report_digest"],
                report[PREFLIGHT_REPORT_DIGEST_FIELD],
                "preflight_report_digest_mismatch",
            ),
            (
                candidate_request["expected_preflight_receipt_digest"],
                receipt[PREFLIGHT_RECEIPT_DIGEST_FIELD],
                "preflight_receipt_digest_mismatch",
            ),
            (
                request["repository_full_name"],
                report["repository_full_name"],
                "repository_full_name_mismatch",
            ),
            (
                request["source_commit_sha"],
                report["source_commit_sha"],
                "source_commit_sha_mismatch",
            ),
            (
                request["source_repository_snapshot_digest"],
                report["source_repository_snapshot_digest"],
                "source_repository_snapshot_digest_mismatch",
            ),
        )
        mismatches = [f"{candidate_id}:{code}" for expected, actual, code in correspondence if expected != actual]
        if mismatches and policy["require_exact_lineage"]:
            return _blocked(*mismatches)

        candidate = normalize_candidate(
            candidate_id=candidate_id,
            candidate_sequence=candidate_request["candidate_sequence"],
            report=report,
            receipt=receipt,
        )
        if policy["require_classification_preservation"] and candidate["classification"] != report["codeai_disposition"]:
            return _blocked(candidate_id + ":classification_not_preserved")
        if policy["require_finding_evidence_preservation"] and candidate["findings"] != report["findings"]:
            return _blocked(candidate_id + ":finding_evidence_not_preserved")
        candidates.append(candidate)

    counts, total_findings, total_changed_paths = summarize(candidates)
    if total_findings > policy["maximum_total_findings"]:
        return _blocked("portfolio_finding_budget_exceeded")
    if total_changed_paths > policy["maximum_total_changed_paths"]:
        return _blocked("portfolio_changed_path_budget_exceeded")

    portfolio = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "portfolio_request_digest": request[REQUEST_DIGEST_FIELD],
        "portfolio_policy_digest": policy[POLICY_DIGEST_FIELD],
        "portfolio_id": request["portfolio_id"],
        "portfolio_revision": request["portfolio_revision"],
        "repository_full_name": request["repository_full_name"],
        "source_commit_sha": request["source_commit_sha"],
        "source_repository_snapshot_digest": request["source_repository_snapshot_digest"],
        "candidate_count": len(candidates),
        "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
        "candidates": candidates,
        "classification_counts": route_counts_named(counts),
        "total_finding_count": total_findings,
        "total_changed_path_count": total_changed_paths,
        "codeai_disposition": PORTFOLIO_DISPOSITION,
        "operating_mode": MODE_PORTFOLIO_ONLY,
        "evidence_portfolio_normalized": True,
        "exact_lineage_verified": True,
        "classification_evidence_preserved": True,
        "finding_evidence_preserved": True,
        "preflight_route_receipts_preserved": True,
        "provider_invoked": False,
        "ranking_performed": False,
        "candidate_selected": False,
        "verification_runner_invoked": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "portfolio_treated_as_correctness_proof": False,
        "classification_treated_as_ranking": False,
        "admissible_treated_as_selected": False,
        "repairable_treated_as_repaired": False,
        "hold_treated_as_rejected": False,
        "rejected_treated_as_repository_deletion": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    portfolio = seal(portfolio, PORTFOLIO_DIGEST_FIELD)
    return CodeAIEvidenceBearingCandidatePortfolioResult(
        STATUS_READY,
        (),
        portfolio,
        _receipt(portfolio),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEvidenceBearingCandidatePortfolioResult",
    "build_codeai_evidence_bearing_candidate_portfolio",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
