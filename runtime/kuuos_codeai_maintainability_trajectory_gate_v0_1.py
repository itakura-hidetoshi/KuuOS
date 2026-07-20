from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_SELECTED,
    DECISION_DIGEST_FIELD as SOURCE_SELECTION_DECISION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_SELECTION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import (
    MEMORY_SNAPSHOT_DIGEST_FIELD as SOURCE_MEMORY_SNAPSHOT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_MEMORY_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_maintainability_trajectory_gate_checks_v0_1 import (
    build_axis_assessment,
    validate_memory_pair,
    validate_selection_pair,
    validate_trajectory_evidence_packet,
)
from runtime.kuuos_codeai_maintainability_trajectory_gate_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAIMaintainabilityTrajectoryGateResult:
    return CodeAIMaintainabilityTrajectoryGateResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(decision: dict[str, Any]) -> dict[str, Any]:
    admitted = decision["gate_decision"] == GATE_ADMITTED
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "maintainability_trajectory_gate_decision_digest": decision[
            DECISION_DIGEST_FIELD
        ],
        "gate_request_digest": decision["gate_request_digest"],
        "gate_policy_digest": decision["gate_policy_digest"],
        "trajectory_evidence_packet_digest": decision[
            "trajectory_evidence_packet_digest"
        ],
        "selection_decision_digest": decision["selection_decision_digest"],
        "selection_receipt_digest": decision["selection_receipt_digest"],
        "memory_snapshot_digest": decision["memory_snapshot_digest"],
        "memory_receipt_digest": decision["memory_receipt_digest"],
        "repository_full_name": decision["repository_full_name"],
        "source_commit_sha": decision["source_commit_sha"],
        "selected_candidate_id": decision["selected_candidate_id"],
        "selected_candidate_digest": decision["selected_candidate_digest"],
        "gate_decision": decision["gate_decision"],
        "decision_reason": decision["decision_reason"],
        "decision_reasons": decision["decision_reasons"],
        "axis_count": decision["axis_count"],
        "improved_axis_count": decision["improved_axis_count"],
        "total_regression": decision["total_regression"],
        "candidate_admitted": admitted,
        "candidate_held": not admitted,
        "maintainability_gate_decision_recorded": True,
        "maintainability_gate_authority_bounded_to_decision": True,
        "memory_hint_available": decision["memory_hint_available"],
        "memory_hint_used_as_threshold_waiver": False,
        "test_execution_performed_by_kernel": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "bounded_measurement_treated_as_future_proof": False,
        "maintainability_gate_treated_as_correctness_proof": False,
        "maintainability_gate_treated_as_probability": False,
        "held_treated_as_rejection": False,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_maintainability_trajectory_gate(
    *,
    selection_decision: Any,
    selection_receipt: Any,
    memory_snapshot: Any,
    memory_receipt: Any,
    trajectory_evidence_packet: Any,
    gate_request: Any,
    gate_policy: Any,
) -> CodeAIMaintainabilityTrajectoryGateResult:
    selection = mapping(selection_decision)
    selection_route = mapping(selection_receipt)
    memory = mapping(memory_snapshot)
    memory_route = mapping(memory_receipt)
    evidence = mapping(trajectory_evidence_packet)
    request = mapping(gate_request)
    policy = mapping(gate_policy)
    if any(
        value is None
        for value in (
            selection,
            selection_route,
            memory,
            memory_route,
            evidence,
            request,
            policy,
        )
    ):
        return _blocked("maintainability_gate_input_not_mapping")

    assert selection is not None
    assert selection_route is not None
    assert memory is not None
    assert memory_route is not None
    assert evidence is not None
    assert request is not None
    assert policy is not None

    issues = (
        validate_request(request)
        + validate_policy(policy)
        + validate_selection_pair(selection, selection_route)
        + validate_memory_pair(memory, memory_route)
        + validate_trajectory_evidence_packet(evidence)
    )
    if issues:
        return _blocked(*issues)

    required_policy = (
        "require_source_selection_selected",
        "require_exact_lineage",
        "require_complete_axis_coverage",
        "require_independent_assessor",
        "require_independent_reviewer",
        "require_isolated_candidate_evaluation",
        "require_source_correspondence",
        "require_exact_memory_binding",
        "require_live_repository_unchanged",
        "allow_maintainability_gate_decision",
    )
    disabled = [field for field in required_policy if policy[field] is not True]
    if disabled:
        return _blocked(
            "maintainability_policy_required_guarantee_disabled:"
            + ",".join(disabled)
        )

    forbidden_policy = (
        "allow_memory_threshold_waiver",
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_selection_authority",
        "allow_verification_authority",
        "allow_repair_authority",
        "allow_execution_authority",
        "allow_git_authority",
    )
    enabled = [field for field in forbidden_policy if policy[field] is not False]
    if enabled:
        return _blocked(
            "maintainability_policy_effect_authority_or_waiver_enabled:"
            + ",".join(enabled)
        )

    claimed = [
        field
        for field in (
            "claims_selection_authority",
            "claims_verification_authority",
            "claims_repair_authority",
            "claims_execution_authority",
            "claims_git_authority",
        )
        if request[field] is not False
    ]
    if claimed:
        return _blocked(
            "maintainability_request_claims_downstream_authority:"
            + ",".join(claimed)
        )
    if request["unresolved_maintainability_questions"]:
        return _blocked("maintainability_unresolved_questions_present")

    selection_digest = str(selection[SOURCE_SELECTION_DECISION_DIGEST_FIELD])
    selection_receipt_digest = str(
        selection_route[SOURCE_SELECTION_RECEIPT_DIGEST_FIELD]
    )
    memory_digest = str(memory[SOURCE_MEMORY_SNAPSHOT_DIGEST_FIELD])
    memory_receipt_digest = str(memory_route[SOURCE_MEMORY_RECEIPT_DIGEST_FIELD])
    evidence_digest = str(evidence[EVIDENCE_PACKET_DIGEST_FIELD])

    exact_pairs = (
        (
            request["selection_decision_digest"],
            selection_digest,
            "request_selection_decision_digest_mismatch",
        ),
        (
            request["selection_receipt_digest"],
            selection_receipt_digest,
            "request_selection_receipt_digest_mismatch",
        ),
        (
            request["memory_snapshot_digest"],
            memory_digest,
            "request_memory_snapshot_digest_mismatch",
        ),
        (
            request["memory_receipt_digest"],
            memory_receipt_digest,
            "request_memory_receipt_digest_mismatch",
        ),
        (
            request["trajectory_evidence_packet_digest"],
            evidence_digest,
            "request_trajectory_evidence_digest_mismatch",
        ),
        (
            request["repository_full_name"],
            selection["repository_full_name"],
            "request_repository_mismatch",
        ),
        (
            request["source_commit_sha"],
            selection["source_commit_sha"],
            "request_source_commit_mismatch",
        ),
        (
            request["source_repository_snapshot_digest"],
            selection["source_repository_snapshot_digest"],
            "request_source_snapshot_mismatch",
        ),
        (
            request["selected_candidate_id"],
            selection["selected_candidate_id"],
            "request_selected_candidate_id_mismatch",
        ),
        (
            request["selected_candidate_digest"],
            selection["selected_candidate_digest"],
            "request_selected_candidate_digest_mismatch",
        ),
        (
            policy["expected_selection_decision_digest"],
            selection_digest,
            "policy_selection_decision_digest_mismatch",
        ),
        (
            policy["expected_selection_receipt_digest"],
            selection_receipt_digest,
            "policy_selection_receipt_digest_mismatch",
        ),
        (
            policy["expected_memory_snapshot_digest"],
            memory_digest,
            "policy_memory_snapshot_digest_mismatch",
        ),
        (
            policy["expected_memory_receipt_digest"],
            memory_receipt_digest,
            "policy_memory_receipt_digest_mismatch",
        ),
        (
            policy["expected_trajectory_evidence_packet_digest"],
            evidence_digest,
            "policy_trajectory_evidence_digest_mismatch",
        ),
        (
            policy["expected_repository_full_name"],
            selection["repository_full_name"],
            "policy_repository_mismatch",
        ),
        (
            policy["expected_source_commit_sha"],
            selection["source_commit_sha"],
            "policy_source_commit_mismatch",
        ),
        (
            policy["expected_source_repository_snapshot_digest"],
            selection["source_repository_snapshot_digest"],
            "policy_source_snapshot_mismatch",
        ),
        (
            policy["expected_selected_candidate_id"],
            selection["selected_candidate_id"],
            "policy_selected_candidate_id_mismatch",
        ),
        (
            policy["expected_selected_candidate_digest"],
            selection["selected_candidate_digest"],
            "policy_selected_candidate_digest_mismatch",
        ),
        (
            evidence["selection_decision_digest"],
            selection_digest,
            "trajectory_packet_selection_decision_digest_mismatch",
        ),
        (
            evidence["selection_receipt_digest"],
            selection_receipt_digest,
            "trajectory_packet_selection_receipt_digest_mismatch",
        ),
        (
            evidence["memory_snapshot_digest"],
            memory_digest,
            "trajectory_packet_memory_snapshot_digest_mismatch",
        ),
        (
            evidence["memory_receipt_digest"],
            memory_receipt_digest,
            "trajectory_packet_memory_receipt_digest_mismatch",
        ),
        (
            evidence["repository_full_name"],
            selection["repository_full_name"],
            "trajectory_packet_repository_mismatch",
        ),
        (
            evidence["source_commit_sha"],
            selection["source_commit_sha"],
            "trajectory_packet_source_commit_mismatch",
        ),
        (
            evidence["source_repository_snapshot_digest"],
            selection["source_repository_snapshot_digest"],
            "trajectory_packet_source_snapshot_mismatch",
        ),
        (
            evidence["selected_candidate_id"],
            selection["selected_candidate_id"],
            "trajectory_packet_selected_candidate_id_mismatch",
        ),
        (
            evidence["selected_candidate_digest"],
            selection["selected_candidate_digest"],
            "trajectory_packet_selected_candidate_digest_mismatch",
        ),
    )
    correspondence_issues = [
        code for left, right, code in exact_pairs if left != right
    ]
    if correspondence_issues:
        return _blocked(*correspondence_issues)

    if selection["decision"] != DECISION_SELECTED:
        return _blocked("source_selection_not_selected")
    if selection["candidate_selected"] is not True:
        return _blocked("source_selection_candidate_not_selected")

    memory_pairs = (
        (
            memory["repository_full_name"],
            selection["repository_full_name"],
            "memory_repository_mismatch",
        ),
        (
            memory["source_commit_sha"],
            selection["source_commit_sha"],
            "memory_source_commit_mismatch",
        ),
        (
            memory["source_repository_snapshot_digest"],
            selection["source_repository_snapshot_digest"],
            "memory_source_snapshot_mismatch",
        ),
    )
    memory_issues = [code for left, right, code in memory_pairs if left != right]
    query_binding = mapping(memory["query_version_binding"])
    if query_binding is None:
        memory_issues.append("memory_query_binding_missing")
    else:
        query_pairs = (
            (
                query_binding.get("repository_full_name"),
                selection["repository_full_name"],
                "memory_query_repository_mismatch",
            ),
            (
                query_binding.get("source_commit_sha"),
                selection["source_commit_sha"],
                "memory_query_source_commit_mismatch",
            ),
            (
                query_binding.get("source_repository_snapshot_digest"),
                selection["source_repository_snapshot_digest"],
                "memory_query_source_snapshot_mismatch",
            ),
            (
                query_binding.get("source_candidate_digest"),
                selection["selected_candidate_digest"],
                "memory_query_selected_candidate_digest_mismatch",
            ),
        )
        memory_issues.extend(
            code for left, right, code in query_pairs if left != right
        )
    for index, entry in enumerate(memory["matched_entries"]):
        if entry["source_candidate_digest"] != selection["selected_candidate_digest"]:
            memory_issues.append(
                f"memory_matched_entry_candidate_digest_mismatch:{index}"
            )
        if entry["candidate_id"] != selection["selected_candidate_id"]:
            memory_issues.append(
                f"memory_matched_entry_candidate_id_mismatch:{index}"
            )
    if memory_issues:
        return _blocked(*memory_issues)

    evaluation_epoch = int(policy["evaluation_epoch"])
    request_epoch = int(request["request_created_epoch"])
    evidence_epoch = int(evidence["evidence_created_epoch"])
    if not (
        evaluation_epoch - int(policy["maximum_request_age"])
        <= request_epoch
        <= evaluation_epoch
    ):
        return _blocked("maintainability_request_window_invalid")
    if not (
        evaluation_epoch - int(policy["maximum_evidence_age"])
        <= evidence_epoch
        <= evaluation_epoch
    ):
        return _blocked("maintainability_evidence_window_invalid")

    role_ids = {
        str(evidence["candidate_producer_id"]),
        str(evidence["independent_assessor_id"]),
        str(evidence["independent_reviewer_id"]),
    }
    if len(role_ids) != 3:
        return _blocked("maintainability_roles_not_separated")

    for field in (
        "external_measurement_reported",
        "independent_assessor_verified",
        "independent_reviewer_verified",
        "isolated_candidate_evaluation_verified",
        "source_correspondence_verified",
        "live_repository_unchanged",
    ):
        if evidence[field] is not True:
            return _blocked("trajectory_packet_required_true:" + field)
    for field in (
        "candidate_producer_involved_in_measurement",
        "repository_mutation_performed",
        "git_effect_performed",
    ):
        if evidence[field] is not False:
            return _blocked("trajectory_packet_forbidden_true:" + field)

    records = evidence["records"]
    if len(records) > int(policy["maximum_trajectory_records"]):
        return _blocked("maintainability_record_budget_exceeded")
    axes = [record["axis"] for record in records]
    if axes != policy["required_axes"]:
        return _blocked("maintainability_axis_coverage_or_order_mismatch")

    record_issues: list[str] = []
    assessments: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        expected_delta = int(record["candidate_value"]) - int(
            record["baseline_value"]
        )
        if record["observed_delta"] != expected_delta:
            record_issues.append(
                f"trajectory_record_observed_delta_mismatch:{index}"
            )
        if record["assessor_id"] != evidence["independent_assessor_id"]:
            record_issues.append(f"trajectory_record_assessor_mismatch:{index}")
        if record["reviewer_id"] != evidence["independent_reviewer_id"]:
            record_issues.append(f"trajectory_record_reviewer_mismatch:{index}")
        for field in (
            "completed",
            "external_measurement",
            "independent_assessor",
            "independent_reviewer",
            "isolated_candidate_evaluation",
            "source_correspondence",
        ):
            if record[field] is not True:
                record_issues.append(
                    f"trajectory_record_required_true:{index}:{field}"
                )
        for field in (
            "candidate_producer_involved",
            "repository_mutation_performed",
            "git_effect_performed",
        ):
            if record[field] is not False:
                record_issues.append(
                    f"trajectory_record_forbidden_true:{index}:{field}"
                )
        assessments.append(
            build_axis_assessment(
                record,
                int(policy["maximum_allowed_increase"][record["axis"]]),
            )
        )
    if record_issues:
        return _blocked(*record_issues)

    exceeded_axes = [
        assessment["axis"]
        for assessment in assessments
        if not assessment["within_axis_limit"]
    ]
    total_regression = sum(
        int(assessment["regression_amount"]) for assessment in assessments
    )
    improved_axis_count = sum(
        1 for assessment in assessments if assessment["improved"]
    )

    reasons: list[str] = []
    if exceeded_axes:
        reasons.append(REASON_AXIS_LIMIT)
    if total_regression > int(policy["maximum_total_regression"]):
        reasons.append(REASON_TOTAL_REGRESSION)
    if improved_axis_count < int(policy["minimum_improved_axes"]):
        reasons.append(REASON_INSUFFICIENT_IMPROVEMENT)

    if reasons:
        gate_decision = GATE_HELD
        decision_reason = reasons[0]
    else:
        gate_decision = GATE_ADMITTED
        decision_reason = REASON_ADMITTED
        reasons = [REASON_ADMITTED]

    memory_hint_available = bool(memory["matched_entry_count"])
    decision = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "gate_request_id": request["gate_request_id"],
        "gate_request_revision": request["gate_request_revision"],
        "gate_request_digest": request[REQUEST_DIGEST_FIELD],
        "gate_policy_digest": policy[POLICY_DIGEST_FIELD],
        "trajectory_evidence_packet_digest": evidence_digest,
        "selection_decision_digest": selection_digest,
        "selection_receipt_digest": selection_receipt_digest,
        "memory_snapshot_digest": memory_digest,
        "memory_receipt_digest": memory_receipt_digest,
        "repository_full_name": selection["repository_full_name"],
        "source_commit_sha": selection["source_commit_sha"],
        "source_repository_snapshot_digest": selection[
            "source_repository_snapshot_digest"
        ],
        "selected_candidate_id": selection["selected_candidate_id"],
        "selected_candidate_digest": selection["selected_candidate_digest"],
        "axis_assessments": assessments,
        "axis_count": len(assessments),
        "exceeded_axes": exceeded_axes,
        "exceeded_axis_count": len(exceeded_axes),
        "improved_axis_count": improved_axis_count,
        "minimum_improved_axes": policy["minimum_improved_axes"],
        "total_regression": total_regression,
        "maximum_total_regression": policy["maximum_total_regression"],
        "gate_decision": gate_decision,
        "decision_reason": decision_reason,
        "decision_reasons": reasons,
        "candidate_admitted": gate_decision == GATE_ADMITTED,
        "candidate_held": gate_decision == GATE_HELD,
        "maintainability_gate_decision_recorded": True,
        "maintainability_gate_authority_exercised": True,
        "maintainability_gate_authority_bounded_to_decision": True,
        "memory_hint_available": memory_hint_available,
        "memory_recommendation": memory["recommendation"],
        "memory_hint_used_as_threshold_waiver": False,
        "historical_repair_outcome_used_as_probability": False,
        "external_measurement_evidence_consumed": True,
        "test_execution_performed_by_kernel": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "bounded_measurement_treated_as_future_proof": False,
        "maintainability_gate_treated_as_correctness_proof": False,
        "maintainability_gate_treated_as_probability": False,
        "held_treated_as_rejection": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_GATE_ONLY,
    }
    decision = seal(decision, DECISION_DIGEST_FIELD)
    return CodeAIMaintainabilityTrajectoryGateResult(
        STATUS_READY,
        (),
        decision,
        _receipt(decision),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIMaintainabilityTrajectoryGateResult",
    "build_codeai_maintainability_trajectory_gate",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
