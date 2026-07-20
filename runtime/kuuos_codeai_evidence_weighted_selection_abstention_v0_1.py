from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    OBLIGATION_DIGEST_FIELD,
    PLAN_DIGEST_FIELD as STRENGTHENING_PLAN_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as STRENGTHENING_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import *
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_checks_v0_1 import (
    score_candidate,
    validate_evidence_packet,
    validate_source_pair,
)


def _blocked(*issues: str) -> CodeAIEvidenceWeightedSelectionAbstentionResult:
    return CodeAIEvidenceWeightedSelectionAbstentionResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(decision: dict[str, Any]) -> dict[str, Any]:
    selected = decision["decision"] == DECISION_SELECTED
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "decision_digest": decision[DECISION_DIGEST_FIELD],
        "selection_request_digest": decision["selection_request_digest"],
        "selection_policy_digest": decision["selection_policy_digest"],
        "evidence_packet_digest": decision["evidence_packet_digest"],
        "strengthening_plan_digest": decision["strengthening_plan_digest"],
        "strengthening_receipt_digest": decision["strengthening_receipt_digest"],
        "repository_full_name": decision["repository_full_name"],
        "source_commit_sha": decision["source_commit_sha"],
        "decision": decision["decision"],
        "decision_reason": decision["decision_reason"],
        "selected_candidate_id": decision["selected_candidate_id"],
        "candidate_count": decision["candidate_count"],
        "eligible_candidate_count": decision["eligible_candidate_count"],
        "evidence_record_count": decision["evidence_record_count"],
        "ranking_performed": True,
        "selection_decision_recorded": True,
        "candidate_selected": selected,
        "abstention_recorded": not selected,
        "selection_authority_exercised": selected,
        "selection_authority_bounded_to_decision": True,
        "test_execution_performed_by_kernel": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "score_treated_as_probability": False,
        "score_treated_as_correctness_proof": False,
        "selection_treated_as_correctness_proof": False,
        "abstention_treated_as_rejection": False,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_evidence_weighted_selection_abstention(
    *,
    strengthening_plan: Any,
    strengthening_receipt: Any,
    evidence_packet: Any,
    selection_request: Any,
    selection_policy: Any,
) -> CodeAIEvidenceWeightedSelectionAbstentionResult:
    plan = mapping(strengthening_plan)
    receipt = mapping(strengthening_receipt)
    evidence = mapping(evidence_packet)
    request = mapping(selection_request)
    policy = mapping(selection_policy)
    if any(value is None for value in (plan, receipt, evidence, request, policy)):
        return _blocked("selection_input_not_mapping")

    assert plan is not None
    assert receipt is not None
    assert evidence is not None
    assert request is not None
    assert policy is not None

    issues = (
        validate_request(request)
        + validate_policy(policy)
        + validate_source_pair(plan, receipt)
        + validate_evidence_packet(evidence)
    )
    if issues:
        return _blocked(*issues)

    required_policy_fields = (
        "require_exact_lineage",
        "require_complete_obligation_coverage",
        "require_independent_runner",
        "require_independent_reviewer",
        "require_isolated_execution",
        "require_source_correspondence",
        "require_admissible_source_classification",
        "require_all_obligations_passed",
        "allow_selection_decision",
    )
    disabled = [field for field in required_policy_fields if policy[field] is not True]
    if disabled:
        return _blocked("selection_policy_required_guarantee_disabled:" + ",".join(disabled))
    forbidden_effect_fields = (
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    if any(policy[field] for field in forbidden_effect_fields):
        return _blocked("selection_policy_downstream_effect_or_authority_enabled")
    if request["claims_execution_authority"] or request["claims_git_authority"]:
        return _blocked("selection_request_claims_downstream_authority")
    if request["unresolved_selection_questions"]:
        return _blocked("selection_unresolved_questions_present")

    plan_digest = str(plan[STRENGTHENING_PLAN_DIGEST_FIELD])
    receipt_digest = str(receipt[STRENGTHENING_RECEIPT_DIGEST_FIELD])
    evidence_digest = str(evidence[EVIDENCE_PACKET_DIGEST_FIELD])
    exact_pairs = (
        (request["repository_full_name"], plan["repository_full_name"], "request_repository_mismatch"),
        (request["source_commit_sha"], plan["source_commit_sha"], "request_source_commit_mismatch"),
        (request["strengthening_plan_digest"], plan_digest, "request_plan_digest_mismatch"),
        (request["strengthening_receipt_digest"], receipt_digest, "request_receipt_digest_mismatch"),
        (request["evidence_packet_digest"], evidence_digest, "request_evidence_digest_mismatch"),
        (policy["expected_repository_full_name"], plan["repository_full_name"], "policy_repository_mismatch"),
        (policy["expected_source_commit_sha"], plan["source_commit_sha"], "policy_source_commit_mismatch"),
        (policy["expected_strengthening_plan_digest"], plan_digest, "policy_plan_digest_mismatch"),
        (policy["expected_strengthening_receipt_digest"], receipt_digest, "policy_receipt_digest_mismatch"),
        (policy["expected_evidence_packet_digest"], evidence_digest, "policy_evidence_digest_mismatch"),
        (evidence["repository_full_name"], plan["repository_full_name"], "evidence_repository_mismatch"),
        (evidence["source_commit_sha"], plan["source_commit_sha"], "evidence_source_commit_mismatch"),
        (evidence["strengthening_plan_digest"], plan_digest, "evidence_plan_digest_mismatch"),
        (evidence["strengthening_receipt_digest"], receipt_digest, "evidence_receipt_digest_mismatch"),
    )
    correspondence_issues = [code for left, right, code in exact_pairs if left != right]
    if correspondence_issues:
        return _blocked(*correspondence_issues)

    evaluation_epoch = int(policy["evaluation_epoch"])
    request_epoch = int(request["request_created_epoch"])
    evidence_epoch = int(evidence["evidence_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= request_epoch <= evaluation_epoch:
        return _blocked("selection_request_window_invalid")
    if not evaluation_epoch - int(policy["maximum_evidence_age"]) <= evidence_epoch <= evaluation_epoch:
        return _blocked("selection_evidence_window_invalid")

    if evidence["candidate_producer_id"] in {evidence["independent_runner_id"], evidence["independent_reviewer_id"]}:
        return _blocked("selection_evidence_candidate_producer_not_independent")
    if evidence["independent_runner_id"] == evidence["independent_reviewer_id"]:
        return _blocked("selection_evidence_runner_reviewer_not_independent")
    for field in (
        "external_test_execution_reported",
        "independent_runner_verified",
        "independent_reviewer_verified",
        "isolated_execution_verified",
        "source_correspondence_verified",
    ):
        if evidence[field] is not True:
            return _blocked("selection_evidence_required_true:" + field)
    for field in (
        "candidate_producer_involved_in_evidence",
        "repository_mutation_performed",
        "git_effect_performed",
    ):
        if evidence[field] is not False:
            return _blocked("selection_evidence_forbidden_true:" + field)

    candidate_plans = plan["candidate_plans"]
    candidate_evidence = evidence["candidate_results"]
    if len(candidate_plans) > policy["maximum_candidates"]:
        return _blocked("selection_candidate_budget_exceeded")
    if evidence["evidence_record_count"] > policy["maximum_evidence_records"]:
        return _blocked("selection_evidence_record_budget_exceeded")
    if [item["candidate_id"] for item in candidate_evidence] != plan["candidate_ids"]:
        return _blocked("selection_evidence_candidate_order_mismatch")

    evidence_by_candidate = {item["candidate_id"]: item for item in candidate_evidence}
    coverage_issues: list[str] = []
    for candidate in candidate_plans:
        evidence_candidate = evidence_by_candidate[candidate["candidate_id"]]
        if evidence_candidate["candidate_sequence"] != candidate["candidate_sequence"]:
            coverage_issues.append("selection_evidence_candidate_sequence_mismatch:" + candidate["candidate_id"])
            continue
        obligations = candidate["obligations"]
        records = evidence_candidate["obligation_results"]
        if len(records) != len(obligations):
            coverage_issues.append("selection_evidence_obligation_count_mismatch:" + candidate["candidate_id"])
            continue
        for obligation, record in zip(obligations, records):
            pairs = (
                (record["obligation_id"], obligation["obligation_id"]),
                (record["obligation_digest"], obligation[OBLIGATION_DIGEST_FIELD]),
                (record["category"], obligation["category"]),
                (record["check_kind"], obligation["check_kind"]),
                (record["candidate_id"], candidate["candidate_id"]),
                (record["candidate_sequence"], candidate["candidate_sequence"]),
            )
            if any(left != right for left, right in pairs):
                coverage_issues.append("selection_evidence_obligation_correspondence_mismatch:" + obligation["obligation_id"])
            if record["runner_id"] != evidence["independent_runner_id"]:
                coverage_issues.append("selection_evidence_runner_mismatch:" + obligation["obligation_id"])
            if record["reviewer_id"] != evidence["independent_reviewer_id"]:
                coverage_issues.append("selection_evidence_reviewer_mismatch:" + obligation["obligation_id"])
            for field in (
                "completed", "external_execution", "independent_runner", "independent_reviewer",
                "isolated_execution", "source_correspondence",
            ):
                if record[field] is not True:
                    coverage_issues.append("selection_evidence_record_required_true:" + obligation["obligation_id"] + ":" + field)
            for field in ("candidate_producer_involved", "repository_mutation_performed", "git_effect_performed"):
                if record[field] is not False:
                    coverage_issues.append("selection_evidence_record_forbidden_true:" + obligation["obligation_id"] + ":" + field)
    if coverage_issues:
        return _blocked(*coverage_issues)

    scorecards = [
        score_candidate(
            candidate,
            evidence_by_candidate[candidate["candidate_id"]],
            policy["category_weights"],
            bool(policy["require_admissible_source_classification"]),
            bool(policy["require_all_obligations_passed"]),
        )
        for candidate in candidate_plans
    ]
    ordered = sorted(
        scorecards,
        key=lambda item: (0 if item["eligible"] else 1, -int(item["evidence_score"]), int(item["candidate_sequence"]), str(item["candidate_id"])),
    )
    for rank, scorecard in enumerate(ordered, start=1):
        scorecard["rank"] = rank

    eligible = [item for item in ordered if item["eligible"]]
    selected_candidate_id = ""
    selected_candidate_digest = ""
    selected_score = 0
    runner_up_score = 0
    score_margin = 0
    if not eligible:
        decision_value = DECISION_ABSTAINED
        reason = REASON_NO_ELIGIBLE
    else:
        top = eligible[0]
        selected_score = int(top["evidence_score"])
        runner_up_score = int(eligible[1]["evidence_score"]) if len(eligible) > 1 else 0
        score_margin = selected_score - runner_up_score
        if selected_score < int(policy["minimum_evidence_score"]):
            decision_value = DECISION_ABSTAINED
            reason = REASON_BELOW_THRESHOLD
        elif len(eligible) > 1 and selected_score == runner_up_score:
            decision_value = DECISION_ABSTAINED
            reason = REASON_TIED_TOP
        elif len(eligible) > 1 and score_margin < int(policy["minimum_score_margin"]):
            decision_value = DECISION_ABSTAINED
            reason = REASON_INSUFFICIENT_MARGIN
        else:
            decision_value = DECISION_SELECTED
            reason = REASON_SELECTED
            selected_candidate_id = str(top["candidate_id"])
            selected_candidate_digest = str(top["source_candidate_digest"])
            top["candidate_selected"] = True

    decision = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "selection_id": request["selection_id"],
        "selection_revision": request["selection_revision"],
        "selection_request_digest": request[REQUEST_DIGEST_FIELD],
        "selection_policy_digest": policy[POLICY_DIGEST_FIELD],
        "evidence_packet_digest": evidence_digest,
        "strengthening_plan_digest": plan_digest,
        "strengthening_receipt_digest": receipt_digest,
        "repository_full_name": plan["repository_full_name"],
        "source_commit_sha": plan["source_commit_sha"],
        "source_repository_snapshot_digest": plan["source_repository_snapshot_digest"],
        "candidate_count": len(candidate_plans),
        "candidate_ids": plan["candidate_ids"],
        "evidence_record_count": evidence["evidence_record_count"],
        "category_weights": dict(policy["category_weights"]),
        "minimum_evidence_score": policy["minimum_evidence_score"],
        "minimum_score_margin": policy["minimum_score_margin"],
        "candidate_scorecards": ordered,
        "eligible_candidate_count": len(eligible),
        "decision": decision_value,
        "decision_reason": reason,
        "selected_candidate_id": selected_candidate_id,
        "selected_candidate_digest": selected_candidate_digest,
        "selected_evidence_score": selected_score,
        "runner_up_evidence_score": runner_up_score,
        "score_margin": score_margin,
        "ranking_performed": True,
        "selection_decision_recorded": True,
        "candidate_selected": decision_value == DECISION_SELECTED,
        "abstention_recorded": decision_value == DECISION_ABSTAINED,
        "selection_authority_exercised": decision_value == DECISION_SELECTED,
        "selection_authority_bounded_to_decision": True,
        "external_test_execution_evidence_consumed": True,
        "test_execution_performed_by_kernel": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "score_treated_as_probability": False,
        "score_treated_as_correctness_proof": False,
        "selection_treated_as_correctness_proof": False,
        "abstention_treated_as_rejection": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    decision = seal(decision, DECISION_DIGEST_FIELD)
    return CodeAIEvidenceWeightedSelectionAbstentionResult(
        STATUS_READY,
        (),
        decision,
        _receipt(decision),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEvidenceWeightedSelectionAbstentionResult",
    "build_codeai_evidence_weighted_selection_abstention",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
