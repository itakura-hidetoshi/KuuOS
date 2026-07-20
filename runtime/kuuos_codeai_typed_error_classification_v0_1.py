from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    PORTFOLIO_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as PORTFOLIO_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD as BASELINE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as BASELINE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import *
from runtime.kuuos_codeai_typed_error_classification_checks_v0_1 import (
    classify_finding,
    summarize_typed_errors,
    validate_baseline_pair,
    validate_portfolio_pair,
)


def _blocked(*issues: str) -> CodeAITypedErrorClassificationResult:
    return CodeAITypedErrorClassificationResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(classification: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "typed_error_classification_digest": classification[CLASSIFICATION_DIGEST_FIELD],
        "classification_request_digest": classification["classification_request_digest"],
        "classification_policy_digest": classification["classification_policy_digest"],
        "repository_full_name": classification["repository_full_name"],
        "source_commit_sha": classification["source_commit_sha"],
        "source_portfolio_digest": classification["source_portfolio_digest"],
        "source_portfolio_receipt_digest": classification["source_portfolio_receipt_digest"],
        "baseline_evidence_digest": classification["baseline_evidence_digest"],
        "baseline_receipt_digest": classification["baseline_receipt_digest"],
        "candidate_count": classification["candidate_count"],
        "typed_error_count": classification["typed_error_count"],
        "family_counts": classification["family_counts"],
        "repair_route_counts": classification["repair_route_counts"],
        "baseline_known_error_count": classification["novelty_counts"][NOVELTY_KNOWN],
        "baseline_novel_error_count": classification["novelty_counts"][NOVELTY_NOVEL],
        "operating_mode": MODE_CLASSIFICATION_ONLY,
        "route_receipt_recorded": True,
        "typed_error_classification_emitted": True,
        "exact_lineage_verified": True,
        "source_finding_evidence_preserved": True,
        "taxonomy_complete_for_observed_findings": True,
        "historical_baseline_used_as_reference_only": True,
        "provider_invoked": False,
        "ranking_performed": False,
        "candidate_selected": False,
        "verification_runner_invoked": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "typed_error_treated_as_cause_proof": False,
        "historical_frequency_treated_as_probability": False,
        "zero_static_error_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_typed_error_classification(
    *,
    source_portfolio: Any,
    source_portfolio_receipt: Any,
    baseline_evidence: Any,
    baseline_receipt: Any,
    classification_request: Any,
    classification_policy: Any,
) -> CodeAITypedErrorClassificationResult:
    portfolio = mapping(source_portfolio)
    portfolio_receipt = mapping(source_portfolio_receipt)
    baseline = mapping(baseline_evidence)
    baseline_route = mapping(baseline_receipt)
    request = mapping(classification_request)
    policy = mapping(classification_policy)
    if None in (portfolio, portfolio_receipt, baseline, baseline_route, request, policy):
        return _blocked("classification_input_not_mapping")

    assert portfolio is not None
    assert portfolio_receipt is not None
    assert baseline is not None
    assert baseline_route is not None
    assert request is not None
    assert policy is not None

    issues = (
        validate_request(request)
        + validate_policy(policy)
        + validate_portfolio_pair(portfolio, portfolio_receipt)
        + validate_baseline_pair(baseline, baseline_route)
    )
    if issues:
        return _blocked(*issues)

    authority_fields = (
        "allow_ranking",
        "allow_candidate_selection",
        "allow_verification_runner_invocation",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    if any(policy[field] for field in authority_fields):
        return _blocked("classification_policy_effect_or_authority_enabled")
    if not policy["require_exact_lineage"]:
        return _blocked("classification_policy_exact_lineage_not_required")
    if not policy["require_complete_taxonomy"]:
        return _blocked("classification_policy_complete_taxonomy_not_required")
    if not policy["require_finding_evidence_preservation"]:
        return _blocked("classification_policy_finding_preservation_not_required")
    if request["claims_authority"]:
        return _blocked("classification_request_claims_authority")
    if request["unresolved_classification_questions"]:
        return _blocked("classification_unresolved_questions_present")

    portfolio_digest = str(portfolio[PORTFOLIO_DIGEST_FIELD])
    portfolio_receipt_digest = str(portfolio_receipt[PORTFOLIO_RECEIPT_DIGEST_FIELD])
    baseline_digest = str(baseline[BASELINE_EVIDENCE_DIGEST_FIELD])
    baseline_receipt_digest = str(baseline_route[BASELINE_RECEIPT_DIGEST_FIELD])
    exact_pairs = (
        (request["repository_full_name"], portfolio["repository_full_name"], "request_repository_mismatch"),
        (request["source_commit_sha"], portfolio["source_commit_sha"], "request_source_commit_mismatch"),
        (request["source_portfolio_digest"], portfolio_digest, "request_portfolio_digest_mismatch"),
        (
            request["source_portfolio_receipt_digest"],
            portfolio_receipt_digest,
            "request_portfolio_receipt_digest_mismatch",
        ),
        (request["baseline_evidence_digest"], baseline_digest, "request_baseline_evidence_digest_mismatch"),
        (request["baseline_receipt_digest"], baseline_receipt_digest, "request_baseline_receipt_digest_mismatch"),
        (policy["expected_repository_full_name"], portfolio["repository_full_name"], "policy_repository_mismatch"),
        (policy["expected_source_commit_sha"], portfolio["source_commit_sha"], "policy_source_commit_mismatch"),
        (policy["expected_source_portfolio_digest"], portfolio_digest, "policy_portfolio_digest_mismatch"),
        (
            policy["expected_source_portfolio_receipt_digest"],
            portfolio_receipt_digest,
            "policy_portfolio_receipt_digest_mismatch",
        ),
        (policy["expected_baseline_evidence_digest"], baseline_digest, "policy_baseline_evidence_digest_mismatch"),
        (policy["expected_baseline_receipt_digest"], baseline_receipt_digest, "policy_baseline_receipt_digest_mismatch"),
        (baseline["repository_full_name"], portfolio["repository_full_name"], "baseline_repository_mismatch"),
    )
    correspondence_issues = [code for left, right, code in exact_pairs if left != right]
    if correspondence_issues:
        return _blocked(*correspondence_issues)

    evaluation_epoch = int(policy["evaluation_epoch"])
    request_epoch = int(request["request_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= request_epoch <= evaluation_epoch:
        return _blocked("classification_request_window_invalid")

    candidates = portfolio["candidates"]
    if len(candidates) > policy["maximum_candidates"]:
        return _blocked("classification_candidate_budget_exceeded")
    unknown_codes = sorted(
        {
            finding["code"]
            for candidate in candidates
            for finding in candidate["findings"]
            if finding["code"] not in FINDING_TAXONOMY
        }
    )
    if unknown_codes:
        return _blocked("classification_taxonomy_missing_codes:" + ",".join(unknown_codes))

    baseline_counts = baseline["metrics"]["error_fingerprint_counts"]
    typed_candidates: list[dict[str, Any]] = []
    all_errors: list[dict[str, Any]] = []
    for candidate in candidates:
        typed_errors = [
            classify_finding(
                candidate_id=candidate["candidate_id"],
                candidate_sequence=candidate["candidate_sequence"],
                error_sequence=index,
                finding=finding,
                baseline_counts=baseline_counts,
            )
            for index, finding in enumerate(candidate["findings"], start=1)
        ]
        all_errors.extend(typed_errors)
        typed_candidates.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate_sequence": candidate["candidate_sequence"],
                "source_candidate_digest": canonical_digest(candidate),
                "source_classification": candidate["classification"],
                "source_finding_count": len(candidate["findings"]),
                "typed_error_count": len(typed_errors),
                "typed_errors": typed_errors,
                "no_static_error_observed": len(typed_errors) == 0,
                "source_finding_evidence_preserved": [error["source_finding"] for error in typed_errors]
                == candidate["findings"],
                "candidate_selected": False,
                "repair_executed": False,
                "verification_runner_invoked": False,
            }
        )

    if len(all_errors) > policy["maximum_typed_errors"]:
        return _blocked("classification_typed_error_budget_exceeded")
    if len(all_errors) != portfolio["total_finding_count"]:
        return _blocked("classification_finding_accounting_mismatch")
    if not all(candidate["source_finding_evidence_preserved"] for candidate in typed_candidates):
        return _blocked("classification_source_finding_evidence_not_preserved")

    summary = summarize_typed_errors(all_errors)
    classification = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "classification_id": request["classification_id"],
        "classification_revision": request["classification_revision"],
        "classification_request_digest": request[REQUEST_DIGEST_FIELD],
        "classification_policy_digest": policy[POLICY_DIGEST_FIELD],
        "repository_full_name": portfolio["repository_full_name"],
        "source_commit_sha": portfolio["source_commit_sha"],
        "source_repository_snapshot_digest": portfolio["source_repository_snapshot_digest"],
        "source_portfolio_digest": portfolio_digest,
        "source_portfolio_receipt_digest": portfolio_receipt_digest,
        "baseline_evidence_digest": baseline_digest,
        "baseline_receipt_digest": baseline_receipt_digest,
        "baseline_metrics_digest": baseline["metrics_digest"],
        "candidate_count": len(typed_candidates),
        "candidate_ids": [candidate["candidate_id"] for candidate in typed_candidates],
        "typed_candidates": typed_candidates,
        "typed_error_count": summary["typed_error_count"],
        "family_counts": summary["family_counts"],
        "stage_counts": summary["stage_counts"],
        "repair_route_counts": summary["repair_route_counts"],
        "novelty_counts": summary["novelty_counts"],
        "severity_counts": summary["severity_counts"],
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_CLASSIFICATION_ONLY,
        "exact_lineage_verified": True,
        "source_finding_evidence_preserved": True,
        "taxonomy_complete_for_observed_findings": True,
        "historical_baseline_used_as_reference_only": True,
        "provider_invoked": False,
        "ranking_performed": False,
        "candidate_selected": False,
        "verification_runner_invoked": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "typed_error_treated_as_cause_proof": False,
        "historical_frequency_treated_as_probability": False,
        "zero_static_error_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    classification = seal(classification, CLASSIFICATION_DIGEST_FIELD)
    return CodeAITypedErrorClassificationResult(
        STATUS_READY,
        (),
        classification,
        _receipt(classification),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAITypedErrorClassificationResult",
    "build_codeai_typed_error_classification",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
