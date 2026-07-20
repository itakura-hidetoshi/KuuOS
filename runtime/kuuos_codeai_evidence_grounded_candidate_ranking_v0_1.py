#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_grounded_candidate_ranking_schema_v0_1 import *
from runtime.kuuos_codeai_evidence_grounded_candidate_ranking_checks_v0_1 import (
    classification_counts,
    rank_candidates,
    total_changed_path_count,
    total_finding_count,
)


def _blocked(*issues: str) -> CodeAIEvidenceGroundedCandidateRankingResult:
    return CodeAIEvidenceGroundedCandidateRankingResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(ranking: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_portfolio_digest": ranking["source_portfolio_digest"],
        "source_portfolio_receipt_digest": ranking["source_portfolio_receipt_digest"],
        "ranking_request_digest": ranking["ranking_request_digest"],
        "ranking_policy_digest": ranking["ranking_policy_digest"],
        "repository_full_name": ranking["repository_full_name"],
        "source_commit_sha": ranking["source_commit_sha"],
        "source_repository_snapshot_digest": ranking["source_repository_snapshot_digest"],
        "candidate_count": ranking["candidate_count"],
        "ordered_candidate_ids": ranking["ordered_candidate_ids"],
        "ordered_classifications": ranking["ordered_classifications"],
        "classification_counts": ranking["classification_counts"],
        "total_finding_count": ranking["total_finding_count"],
        "total_changed_path_count": ranking["total_changed_path_count"],
        "ranking_strategy": ranking["ranking_strategy"],
        "ranking_purpose": ranking["ranking_purpose"],
        "codeai_disposition": ranking["codeai_disposition"],
        "evidence_grounded_candidate_ranking_digest": ranking[RANKING_DIGEST_FIELD],
        "operating_mode": MODE_RANKING_ONLY,
        "route_receipt_recorded": True,
        "ranking_emitted": True,
        "exact_lineage_verified": True,
        "classification_evidence_preserved": True,
        "finding_evidence_preserved": True,
        "stable_tie_break_verified": True,
        "ranking_performed": True,
        "candidate_selected": False,
        "selection_authority_granted": False,
        "verification_runner_invoked": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "ranking_treated_as_correctness_proof": False,
        "ranking_treated_as_selection": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_evidence_grounded_candidate_ranking(
    *,
    source_portfolio: Any,
    source_portfolio_receipt: Any,
    ranking_request: Any,
    ranking_policy: Any,
) -> CodeAIEvidenceGroundedCandidateRankingResult:
    portfolio = mapping(source_portfolio)
    source_receipt = mapping(source_portfolio_receipt)
    request = mapping(ranking_request)
    policy = mapping(ranking_policy)
    if portfolio is None or source_receipt is None or request is None or policy is None:
        return _blocked("ranking_input_not_mapping")

    issues = (
        validate_source_portfolio(portfolio)
        + validate_source_receipt(source_receipt)
        + validate_request(request)
        + validate_policy(policy)
    )
    if issues:
        return _blocked(*issues)

    authority_fields = (
        "allow_candidate_selection",
        "allow_verification_runner_invocation",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    if any(policy[field] for field in authority_fields):
        return _blocked("ranking_policy_effect_or_authority_enabled")
    if request["claims_selection_authority"]:
        return _blocked("ranking_request_claims_selection_authority")
    if request["unresolved_ranking_questions"]:
        return _blocked("ranking_unresolved_questions_present")
    if not all(
        policy[field]
        for field in (
            "require_exact_lineage",
            "require_classification_preservation",
            "require_finding_evidence_preservation",
            "require_stable_tie_break",
        )
    ):
        return _blocked("ranking_policy_required_preservation_disabled")
    if not (
        policy["evaluation_epoch"] - policy["maximum_request_age"]
        <= request["request_created_epoch"]
        <= policy["evaluation_epoch"]
    ):
        return _blocked("ranking_request_window_invalid")

    source_portfolio_digest = portfolio[SOURCE_PORTFOLIO_DIGEST_FIELD]
    source_receipt_digest = source_receipt[SOURCE_RECEIPT_DIGEST_FIELD]
    correspondence = (
        (
            source_receipt["evidence_bearing_candidate_portfolio_digest"],
            source_portfolio_digest,
            "source_receipt_portfolio_digest_mismatch",
        ),
        (request["source_portfolio_digest"], source_portfolio_digest, "ranking_request_portfolio_digest_mismatch"),
        (
            request["source_portfolio_receipt_digest"],
            source_receipt_digest,
            "ranking_request_portfolio_receipt_digest_mismatch",
        ),
        (
            policy["expected_source_portfolio_digest"],
            source_portfolio_digest,
            "ranking_policy_portfolio_digest_mismatch",
        ),
        (
            policy["expected_source_portfolio_receipt_digest"],
            source_receipt_digest,
            "ranking_policy_portfolio_receipt_digest_mismatch",
        ),
        (request["repository_full_name"], portfolio["repository_full_name"], "ranking_request_repository_mismatch"),
        (request["source_commit_sha"], portfolio["source_commit_sha"], "ranking_request_source_commit_mismatch"),
        (
            request["source_repository_snapshot_digest"],
            portfolio["source_repository_snapshot_digest"],
            "ranking_request_snapshot_mismatch",
        ),
        (
            policy["expected_repository_full_name"],
            portfolio["repository_full_name"],
            "ranking_policy_repository_mismatch",
        ),
        (
            policy["expected_source_commit_sha"],
            portfolio["source_commit_sha"],
            "ranking_policy_source_commit_mismatch",
        ),
        (
            policy["expected_source_repository_snapshot_digest"],
            portfolio["source_repository_snapshot_digest"],
            "ranking_policy_snapshot_mismatch",
        ),
        (source_receipt["repository_full_name"], portfolio["repository_full_name"], "source_receipt_repository_mismatch"),
        (source_receipt["source_commit_sha"], portfolio["source_commit_sha"], "source_receipt_source_commit_mismatch"),
        (
            source_receipt["source_repository_snapshot_digest"],
            portfolio["source_repository_snapshot_digest"],
            "source_receipt_snapshot_mismatch",
        ),
        (source_receipt["candidate_count"], portfolio["candidate_count"], "source_receipt_candidate_count_mismatch"),
        (source_receipt["candidate_ids"], portfolio["candidate_ids"], "source_receipt_candidate_ids_mismatch"),
        (
            source_receipt["classification_counts"],
            portfolio["classification_counts"],
            "source_receipt_classification_counts_mismatch",
        ),
        (
            source_receipt["total_finding_count"],
            portfolio["total_finding_count"],
            "source_receipt_finding_count_mismatch",
        ),
        (
            source_receipt["total_changed_path_count"],
            portfolio["total_changed_path_count"],
            "source_receipt_changed_path_count_mismatch",
        ),
    )
    mismatches = [code for actual, expected, code in correspondence if actual != expected]
    if mismatches:
        return _blocked(*mismatches)

    candidates = portfolio["candidates"]
    if len(candidates) > policy["maximum_candidates"]:
        return _blocked("ranking_candidate_budget_exceeded")
    if portfolio["total_finding_count"] > policy["maximum_total_findings"]:
        return _blocked("ranking_finding_budget_exceeded")
    if portfolio["total_changed_path_count"] > policy["maximum_total_changed_paths"]:
        return _blocked("ranking_changed_path_budget_exceeded")

    computed_counts = classification_counts(candidates)
    computed_findings = total_finding_count(candidates)
    computed_changed_paths = total_changed_path_count(candidates)
    if computed_counts != portfolio["classification_counts"]:
        return _blocked("ranking_source_classification_accounting_mismatch")
    if computed_findings != portfolio["total_finding_count"]:
        return _blocked("ranking_source_finding_accounting_mismatch")
    if computed_changed_paths != portfolio["total_changed_path_count"]:
        return _blocked("ranking_source_changed_path_accounting_mismatch")

    ranked = rank_candidates(candidates)
    ranking = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "ranking_request_digest": request[REQUEST_DIGEST_FIELD],
        "ranking_policy_digest": policy[POLICY_DIGEST_FIELD],
        "ranking_request_id": request["ranking_request_id"],
        "ranking_request_revision": request["ranking_request_revision"],
        "source_portfolio_digest": source_portfolio_digest,
        "source_portfolio_receipt_digest": source_receipt_digest,
        "repository_full_name": portfolio["repository_full_name"],
        "source_commit_sha": portfolio["source_commit_sha"],
        "source_repository_snapshot_digest": portfolio["source_repository_snapshot_digest"],
        "candidate_count": len(ranked),
        "ordered_candidate_ids": [item["candidate_id"] for item in ranked],
        "ordered_classifications": [item["classification"] for item in ranked],
        "ranked_candidates": ranked,
        "classification_counts": computed_counts,
        "total_finding_count": computed_findings,
        "total_changed_path_count": computed_changed_paths,
        "ranking_strategy": RANKING_STRATEGY,
        "ranking_purpose": RANKING_PURPOSE,
        "codeai_disposition": RANKING_DISPOSITION,
        "operating_mode": MODE_RANKING_ONLY,
        "exact_lineage_verified": True,
        "classification_evidence_preserved": True,
        "finding_evidence_preserved": True,
        "stable_tie_break_verified": True,
        "ranking_performed": True,
        "candidate_selected": False,
        "selection_authority_granted": False,
        "verification_runner_invoked": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "ranking_treated_as_correctness_proof": False,
        "ranking_treated_as_selection": False,
        "admissible_treated_as_selected": False,
        "repairable_treated_as_repaired": False,
        "hold_treated_as_rejected": False,
        "rejected_treated_as_repository_deletion": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    ranking = seal(ranking, RANKING_DIGEST_FIELD)
    return CodeAIEvidenceGroundedCandidateRankingResult(
        STATUS_READY,
        (),
        ranking,
        _receipt(ranking),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEvidenceGroundedCandidateRankingResult",
    "build_codeai_evidence_grounded_candidate_ranking",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
