#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1 import (
    build_codeai_evidence_bearing_candidate_portfolio,
)
from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    build_codeai_generated_patch_error_baseline_replay_evaluation,
)
from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    seal,
)
from scripts.build_codeai_evidence_bearing_candidate_portfolio_fixture_v0_1 import (
    build_fixture as build_portfolio_fixture,
)


def build_fixture(
    classification_spec: dict[str, Any],
    portfolio_spec: dict[str, Any],
    baseline_spec: dict[str, Any],
) -> dict[str, Any]:
    portfolio_inputs = build_portfolio_fixture(portfolio_spec)
    portfolio_result = build_codeai_evidence_bearing_candidate_portfolio(
        portfolio_request=portfolio_inputs["portfolio_request"],
        portfolio_policy=portfolio_inputs["portfolio_policy"],
        candidate_preflight_bundles=portfolio_inputs["candidate_preflight_bundles"],
    )
    if portfolio_result.portfolio is None or portfolio_result.receipt is None:
        raise ValueError("portfolio fixture blocked: " + ",".join(portfolio_result.issues))

    baseline_result = build_codeai_generated_patch_error_baseline_replay_evaluation(
        dataset=baseline_spec["dataset"],
        request=baseline_spec["request"],
        policy=baseline_spec["policy"],
    )
    if baseline_result.evidence is None or baseline_result.receipt is None:
        raise ValueError("baseline fixture blocked: " + ",".join(baseline_result.issues))

    portfolio = portfolio_result.portfolio
    portfolio_receipt = portfolio_result.receipt
    baseline_evidence = baseline_result.evidence
    baseline_receipt = baseline_result.receipt
    request = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Typed Error Classification v0.1",
            "classification_id": classification_spec["classification_id"],
            "classification_revision": classification_spec["classification_revision"],
            "repository_full_name": portfolio["repository_full_name"],
            "source_commit_sha": portfolio["source_commit_sha"],
            "source_portfolio_digest": portfolio["codeai_evidence_bearing_candidate_portfolio_digest"],
            "source_portfolio_receipt_digest": portfolio_receipt[
                "codeai_evidence_bearing_candidate_portfolio_receipt_digest"
            ],
            "baseline_evidence_digest": baseline_evidence[
                "codeai_generated_patch_error_baseline_evidence_digest"
            ],
            "baseline_receipt_digest": baseline_receipt[
                "codeai_generated_patch_error_baseline_receipt_digest"
            ],
            "request_created_epoch": classification_spec["request_created_epoch"],
            "unresolved_classification_questions": [],
            "claims_authority": False,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Typed Error Classification v0.1",
            "expected_repository_full_name": portfolio["repository_full_name"],
            "expected_source_commit_sha": portfolio["source_commit_sha"],
            "expected_source_portfolio_digest": portfolio[
                "codeai_evidence_bearing_candidate_portfolio_digest"
            ],
            "expected_source_portfolio_receipt_digest": portfolio_receipt[
                "codeai_evidence_bearing_candidate_portfolio_receipt_digest"
            ],
            "expected_baseline_evidence_digest": baseline_evidence[
                "codeai_generated_patch_error_baseline_evidence_digest"
            ],
            "expected_baseline_receipt_digest": baseline_receipt[
                "codeai_generated_patch_error_baseline_receipt_digest"
            ],
            "evaluation_epoch": classification_spec["evaluation_epoch"],
            "maximum_request_age": classification_spec["maximum_request_age"],
            "maximum_candidates": classification_spec["maximum_candidates"],
            "maximum_typed_errors": classification_spec["maximum_typed_errors"],
            "require_exact_lineage": True,
            "require_complete_taxonomy": True,
            "require_finding_evidence_preservation": True,
            "allow_ranking": False,
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
        "source_portfolio_receipt": portfolio_receipt,
        "baseline_evidence": baseline_evidence,
        "baseline_receipt": baseline_receipt,
        "classification_request": request,
        "classification_policy": policy,
    }


__all__ = ["build_fixture"]
