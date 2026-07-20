from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CLASSIFICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import *
from runtime.kuuos_codeai_independent_test_strengthening_checks_v0_1 import (
    build_obligations,
    capability_map,
    required_capability_issues,
    required_check_kinds,
    summarize_obligations,
    validate_source_pair,
)


def _blocked(*issues: str) -> CodeAIIndependentTestStrengtheningResult:
    return CodeAIIndependentTestStrengtheningResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(plan: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "independent_test_strengthening_plan_digest": plan[PLAN_DIGEST_FIELD],
        "strengthening_request_digest": plan["strengthening_request_digest"],
        "strengthening_policy_digest": plan["strengthening_policy_digest"],
        "capability_catalog_digest": plan["capability_catalog_digest"],
        "source_classification_digest": plan["source_classification_digest"],
        "source_classification_receipt_digest": plan["source_classification_receipt_digest"],
        "repository_full_name": plan["repository_full_name"],
        "source_commit_sha": plan["source_commit_sha"],
        "candidate_count": plan["candidate_count"],
        "typed_error_count": plan["typed_error_count"],
        "obligation_count": plan["obligation_count"],
        "check_kind_counts": plan["check_kind_counts"],
        "category_counts": plan["category_counts"],
        "operating_mode": MODE_PLAN_ONLY,
        "route_receipt_recorded": True,
        "strengthened_test_plan_emitted": True,
        "exact_lineage_verified": True,
        "all_candidates_preserved": True,
        "baseline_obligations_present": True,
        "typed_error_obligations_present": True,
        "novel_error_falsification_obligations_present": True,
        "error_free_mutation_probes_present": True,
        "route_specific_obligations_present": True,
        "provider_invoked": False,
        "test_generation_performed": False,
        "test_execution_performed": False,
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
        "strengthened_plan_treated_as_test_success": False,
        "obligation_count_treated_as_candidate_quality": False,
        "test_coverage_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_independent_test_strengthening(
    *,
    source_classification: Any,
    source_classification_receipt: Any,
    capability_catalog: Any,
    strengthening_request: Any,
    strengthening_policy: Any,
) -> CodeAIIndependentTestStrengtheningResult:
    classification = mapping(source_classification)
    classification_receipt = mapping(source_classification_receipt)
    catalog = mapping(capability_catalog)
    request = mapping(strengthening_request)
    policy = mapping(strengthening_policy)
    if any(value is None for value in (classification, classification_receipt, catalog, request, policy)):
        return _blocked("strengthening_input_not_mapping")

    assert classification is not None
    assert classification_receipt is not None
    assert catalog is not None
    assert request is not None
    assert policy is not None

    issues = (
        validate_request(request)
        + validate_policy(policy)
        + validate_capability_catalog(catalog)
        + validate_source_pair(classification, classification_receipt)
    )
    if issues:
        return _blocked(*issues)

    effect_or_authority_fields = (
        "allow_test_generation",
        "allow_test_execution",
        "allow_candidate_selection",
        "allow_verification_authority",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    if any(policy[field] for field in effect_or_authority_fields):
        return _blocked("strengthening_policy_effect_or_authority_enabled")
    required_policy_fields = (
        "require_exact_lineage",
        "require_baseline_obligations",
        "require_independent_runner",
        "require_isolated_execution",
        "require_falsification_for_novel_errors",
        "require_error_free_mutation_probe",
        "require_route_specific_obligations",
    )
    missing_requirements = [field for field in required_policy_fields if policy[field] is not True]
    if missing_requirements:
        return _blocked("strengthening_policy_required_guarantee_disabled:" + ",".join(missing_requirements))
    if request["claims_authority"]:
        return _blocked("strengthening_request_claims_authority")
    if request["unresolved_strengthening_questions"]:
        return _blocked("strengthening_unresolved_questions_present")

    classification_digest = str(classification[CLASSIFICATION_DIGEST_FIELD])
    classification_receipt_digest = str(classification_receipt[CLASSIFICATION_RECEIPT_DIGEST_FIELD])
    catalog_digest = str(catalog[CAPABILITY_CATALOG_DIGEST_FIELD])
    exact_pairs = (
        (request["repository_full_name"], classification["repository_full_name"], "request_repository_mismatch"),
        (request["source_commit_sha"], classification["source_commit_sha"], "request_source_commit_mismatch"),
        (
            request["source_classification_digest"],
            classification_digest,
            "request_classification_digest_mismatch",
        ),
        (
            request["source_classification_receipt_digest"],
            classification_receipt_digest,
            "request_classification_receipt_digest_mismatch",
        ),
        (request["capability_catalog_digest"], catalog_digest, "request_capability_catalog_digest_mismatch"),
        (
            policy["expected_repository_full_name"],
            classification["repository_full_name"],
            "policy_repository_mismatch",
        ),
        (
            policy["expected_source_commit_sha"],
            classification["source_commit_sha"],
            "policy_source_commit_mismatch",
        ),
        (
            policy["expected_source_classification_digest"],
            classification_digest,
            "policy_classification_digest_mismatch",
        ),
        (
            policy["expected_source_classification_receipt_digest"],
            classification_receipt_digest,
            "policy_classification_receipt_digest_mismatch",
        ),
        (
            policy["expected_capability_catalog_digest"],
            catalog_digest,
            "policy_capability_catalog_digest_mismatch",
        ),
    )
    correspondence_issues = [code for left, right, code in exact_pairs if left != right]
    if correspondence_issues:
        return _blocked(*correspondence_issues)

    evaluation_epoch = int(policy["evaluation_epoch"])
    request_epoch = int(request["request_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= request_epoch <= evaluation_epoch:
        return _blocked("strengthening_request_window_invalid")

    source_candidates = classification["typed_candidates"]
    if len(source_candidates) > policy["maximum_candidates"]:
        return _blocked("strengthening_candidate_budget_exceeded")

    capabilities = capability_map(catalog)
    required_kinds = sorted(
        {
            kind
            for candidate in source_candidates
            for kind in required_check_kinds(candidate)
        }
    )
    unsupported = [kind for kind in required_kinds if kind not in capabilities]
    if unsupported:
        return _blocked(
            "strengthening_required_check_kinds_unsupported:" + ",".join(unsupported)
        )
    candidate_plans: list[dict[str, Any]] = []
    for candidate in source_candidates:
        obligations = build_obligations(candidate, capabilities)
        candidate_plans.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate_sequence": candidate["candidate_sequence"],
                "source_candidate_digest": candidate["source_candidate_digest"],
                "source_classification": candidate["source_classification"],
                "source_typed_error_count": candidate["typed_error_count"],
                "source_error_fingerprints": [
                    error["error_fingerprint"] for error in candidate["typed_errors"]
                ],
                "obligation_count": len(obligations),
                "obligations": obligations,
                "baseline_obligations_present": all(
                    kind in {obligation["check_kind"] for obligation in obligations}
                    for kind in BASELINE_CHECKS
                ),
                "error_free_mutation_probe_required": candidate["typed_error_count"] == 0,
                "novel_error_falsification_required": any(
                    error["baseline_novelty"] == NOVELTY_NOVEL
                    for error in candidate["typed_errors"]
                ),
                "test_generated": False,
                "test_executed": False,
                "candidate_selected": False,
                "verification_runner_invoked": False,
            }
        )

    summary = summarize_obligations(candidate_plans)
    if summary["obligation_count"] > policy["maximum_obligations"]:
        return _blocked("strengthening_obligation_budget_exceeded")
    capability_issues = required_capability_issues(candidate_plans, capabilities, policy)
    if capability_issues:
        return _blocked(*capability_issues)
    if not all(candidate["baseline_obligations_present"] for candidate in candidate_plans):
        return _blocked("strengthening_baseline_obligations_missing")
    if [candidate["candidate_id"] for candidate in candidate_plans] != classification["candidate_ids"]:
        return _blocked("strengthening_candidate_order_not_preserved")
    obligation_ids = [
        obligation["obligation_id"]
        for candidate in candidate_plans
        for obligation in candidate["obligations"]
    ]
    if len(obligation_ids) != len(set(obligation_ids)):
        return _blocked("strengthening_obligation_ids_duplicate")

    plan = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "strengthening_id": request["strengthening_id"],
        "strengthening_revision": request["strengthening_revision"],
        "strengthening_request_digest": request[REQUEST_DIGEST_FIELD],
        "strengthening_policy_digest": policy[POLICY_DIGEST_FIELD],
        "capability_catalog_digest": catalog_digest,
        "source_classification_digest": classification_digest,
        "source_classification_receipt_digest": classification_receipt_digest,
        "repository_full_name": classification["repository_full_name"],
        "source_commit_sha": classification["source_commit_sha"],
        "source_repository_snapshot_digest": classification["source_repository_snapshot_digest"],
        "candidate_count": len(candidate_plans),
        "candidate_ids": [candidate["candidate_id"] for candidate in candidate_plans],
        "typed_error_count": classification["typed_error_count"],
        "candidate_plans": candidate_plans,
        **summary,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_PLAN_ONLY,
        "exact_lineage_verified": True,
        "all_candidates_preserved": True,
        "baseline_obligations_present": True,
        "typed_error_obligations_present": classification["typed_error_count"] == 0
        or summary["category_counts"][CATEGORY_ERROR_SPECIFIC] > 0,
        "novel_error_falsification_obligations_present": classification["novelty_counts"][NOVELTY_NOVEL] == 0
        or summary["category_counts"][CATEGORY_NOVELTY] > 0,
        "error_free_mutation_probes_present": all(
            candidate["typed_error_count"] > 0
            or CHECK_ERROR_FREE_MUTATION_PROBE
            in {obligation["check_kind"] for obligation in plan_candidate["obligations"]}
            for candidate, plan_candidate in zip(source_candidates, candidate_plans)
        ),
        "route_specific_obligations_present": classification["typed_error_count"] == 0
        or summary["category_counts"][CATEGORY_ROUTE] > 0,
        "independent_runner_required": True,
        "isolated_execution_required": True,
        "provider_invoked": False,
        "test_generation_performed": False,
        "test_execution_performed": False,
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
        "strengthened_plan_treated_as_test_success": False,
        "obligation_count_treated_as_candidate_quality": False,
        "test_coverage_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    plan = seal(plan, PLAN_DIGEST_FIELD)
    return CodeAIIndependentTestStrengtheningResult(
        STATUS_READY,
        (),
        plan,
        _receipt(plan),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIIndependentTestStrengtheningResult",
    "build_codeai_independent_test_strengthening",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
