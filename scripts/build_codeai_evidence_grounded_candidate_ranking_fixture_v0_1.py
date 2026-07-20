from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1 import (
    STATUS_READY as PORTFOLIO_STATUS_READY,
    build_codeai_evidence_bearing_candidate_portfolio,
)
from runtime.kuuos_codeai_evidence_grounded_candidate_ranking_schema_v0_1 import (
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    RANKING_PURPOSE,
    RANKING_STRATEGY,
    REQUEST_DIGEST_FIELD,
    SCHEMA_VERSION,
    seal,
)
from scripts.build_codeai_evidence_bearing_candidate_portfolio_fixture_v0_1 import (
    build_fixture as build_portfolio_fixture,
)


def build_fixture(spec: dict[str, Any]) -> dict[str, Any]:
    portfolio_fixture = build_portfolio_fixture(spec)
    portfolio_result = build_codeai_evidence_bearing_candidate_portfolio(
        portfolio_request=portfolio_fixture["portfolio_request"],
        portfolio_policy=portfolio_fixture["portfolio_policy"],
        candidate_preflight_bundles=portfolio_fixture["candidate_preflight_bundles"],
    )
    if (
        portfolio_result.status != PORTFOLIO_STATUS_READY
        or portfolio_result.portfolio is None
        or portfolio_result.receipt is None
    ):
        raise ValueError("source portfolio fixture blocked: " + ",".join(portfolio_result.issues))

    portfolio = portfolio_result.portfolio
    receipt = portfolio_result.receipt
    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "ranking_request_id": spec["ranking_request_id"],
            "ranking_request_revision": spec["ranking_request_revision"],
            "source_portfolio_digest": portfolio["codeai_evidence_bearing_candidate_portfolio_digest"],
            "source_portfolio_receipt_digest": receipt[
                "codeai_evidence_bearing_candidate_portfolio_receipt_digest"
            ],
            "repository_full_name": portfolio["repository_full_name"],
            "source_commit_sha": portfolio["source_commit_sha"],
            "source_repository_snapshot_digest": portfolio["source_repository_snapshot_digest"],
            "ranking_purpose": RANKING_PURPOSE,
            "request_created_epoch": spec["request_created_epoch"],
            "unresolved_ranking_questions": [],
            "claims_selection_authority": False,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "expected_source_portfolio_digest": portfolio[
                "codeai_evidence_bearing_candidate_portfolio_digest"
            ],
            "expected_source_portfolio_receipt_digest": receipt[
                "codeai_evidence_bearing_candidate_portfolio_receipt_digest"
            ],
            "expected_repository_full_name": portfolio["repository_full_name"],
            "expected_source_commit_sha": portfolio["source_commit_sha"],
            "expected_source_repository_snapshot_digest": portfolio[
                "source_repository_snapshot_digest"
            ],
            "evaluation_epoch": spec["evaluation_epoch"],
            "maximum_request_age": spec["maximum_request_age"],
            "maximum_candidates": spec["maximum_candidates"],
            "maximum_total_findings": spec["maximum_total_findings"],
            "maximum_total_changed_paths": spec["maximum_total_changed_paths"],
            "classification_priority": list(spec["classification_priority"]),
            "ranking_strategy": RANKING_STRATEGY,
            "require_exact_lineage": True,
            "require_classification_preservation": True,
            "require_finding_evidence_preservation": True,
            "require_stable_tie_break": True,
            "allow_candidate_selection": False,
            "allow_verification_runner_invocation": False,
            "allow_repair_execution": False,
            "allow_repository_mutation": False,
            "allow_execution_authority": False,
            "allow_git_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    return {
        "source_portfolio": portfolio,
        "source_portfolio_receipt": receipt,
        "ranking_request": request,
        "ranking_policy": policy,
    }


__all__ = ["build_fixture"]
