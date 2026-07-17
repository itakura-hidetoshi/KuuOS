#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import (
    STATUS_BLOCKED,
    STATUS_READY,
    canonical_digest,
    digest_without,
    mapping,
    nat,
    pos,
    strings,
)
from runtime.kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1 import (
    DISPOSITION_SUPPORTED as SOURCE_SUPPORTED,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    STATE_AFTER as SOURCE_STATE,
)

RECEIPT_DIGEST_FIELD = "verifyos_independent_evidence_verification_receipt_digest"
EVIDENCE_DIGEST_FIELD = "independent_verification_evidence_bundle_digest"
EXECUTION_DIGEST_FIELD = "independent_verification_execution_digest"
REVIEW_DIGEST_FIELD = "independent_verification_result_review_digest"
CONTEXT_DIGEST_FIELD = "independent_verification_context_digest"
STATE_AFTER = SOURCE_STATE + "_independent_evidence_verification_recorded"

OUTCOME_PASSED = "passed"
OUTCOME_FAILED = "failed"
OUTCOME_INDETERMINATE = "indeterminate"
OUTCOMES = {OUTCOME_PASSED, OUTCOME_FAILED, OUTCOME_INDETERMINATE}

D_PASSED = "independent_evidence_verification_passed"
D_FAILED = "independent_evidence_verification_failed"
D_INDETERMINATE = "independent_evidence_verification_indeterminate"
D_SOURCE = "source_verification_handoff_repair_required"
D_CORRESPONDENCE = "verification_correspondence_repair_required"
D_INDEPENDENCE = "verifier_independence_repair_required"
D_EVIDENCE = "independent_evidence_integrity_repair_required"
D_PROTOCOL = "verification_protocol_execution_repair_required"
D_REPRODUCTION = "reproduction_execution_repair_required"
D_ACCEPTANCE = "acceptance_adjudication_repair_required"
D_REVIEW = "verification_result_review_repair_required"
D_REPLAY = "verification_replay_conflict_rejected"
D_MUTATION = "current_state_mutation_rejected"
D_AUTHORITY = "authority_escalation_rejected"

OUTCOME_DISPOSITIONS = {D_PASSED, D_FAILED, D_INDETERMINATE}

EVIDENCE_FIELDS = {
    "source_verification_handoff_receipt_digest",
    "source_observability_receipt_digest",
    "source_evidence_snapshot_digests",
    "independent_evidence_source_ids",
    "independent_evidence_artifact_digests",
    "recomputed_sequential_uncertainty_digest",
    "recomputed_conformal_calibration_digest",
    "recomputed_distribution_shift_digest",
    "evidence_integrity_confirmed",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    "evidence_conclusive",
    "evidence_collected_epoch",
    EVIDENCE_DIGEST_FIELD,
}

EXECUTION_FIELDS = {
    "source_verification_handoff_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    "verification_protocol_digest",
    "acceptance_criteria_digest",
    "reproduction_plan_digest",
    "verifier_id",
    "verification_scope",
    "planned_reproduction_attempts",
    "completed_reproduction_attempts",
    "successful_reproduction_attempts",
    "falsification_challenge_executed",
    "falsification_challenge_passed",
    "acceptance_criteria_satisfied",
    "execution_started_epoch",
    "execution_completed_epoch",
    "maximum_execution_duration",
    "observation_recollection_performed",
    "current_state_mutation_performed",
    "authority_escalation_requested",
    "generalized_truth_claimed",
    "causal_verification_claimed",
    "verification_outcome",
    EXECUTION_DIGEST_FIELD,
}

REVIEW_FIELDS = {
    "source_verification_handoff_receipt_digest",
    EXECUTION_DIGEST_FIELD,
    "reviewer_id",
    "verifier_independence_confirmed",
    "reviewer_independence_confirmed",
    "evidence_integrity_adequate",
    "protocol_execution_adequate",
    "reproduction_adequate",
    "acceptance_adjudication_adequate",
    "outcome_supported",
    "no_observation_recollection",
    "no_current_state_mutation",
    "no_authority_escalation",
    "no_truth_claim",
    "no_causal_claim",
    "review_started_epoch",
    "review_completed_epoch",
    "maximum_review_duration",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_verification_handoff_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    EXECUTION_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    "source_world_revision",
    "current_world_revision",
    "verification_session_id",
    "verification_nonce_digest",
    "prior_verification_session_ids",
    "prior_verification_nonce_digests",
    "prior_verification_execution_digests",
    "prior_verification_receipt_digests",
    "requested_verification_operation_digest",
    "exact_verification_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass(frozen=True)
class Result:
    status: str
    blockers: list[str]
    receipt: dict[str, Any] | None


def evidence_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, EVIDENCE_DIGEST_FIELD)


def execution_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, EXECUTION_DIGEST_FIELD)


def review_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, REVIEW_DIGEST_FIELD)


def context_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, CONTEXT_DIGEST_FIELD)


def operation_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    execution: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
            "evidence": evidence.get(EVIDENCE_DIGEST_FIELD),
            "execution": execution.get(EXECUTION_DIGEST_FIELD),
            "review": review.get(REVIEW_DIGEST_FIELD),
            "revision": source.get("resulting_world_revision"),
            "before": SOURCE_STATE,
            "after": STATE_AFTER,
        }
    )


def cycle_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    execution: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
            "evidence": evidence.get(EVIDENCE_DIGEST_FIELD),
            "execution": execution.get(EXECUTION_DIGEST_FIELD),
            "review": review.get(REVIEW_DIGEST_FIELD),
            "session": context.get("verification_session_id"),
            "nonce": context.get("verification_nonce_digest"),
            "revision": context.get("current_world_revision"),
            "operation": context.get("requested_verification_operation_digest"),
        }
    )


def bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _duration(value: Mapping[str, Any], start: str, end: str, maximum: str) -> bool:
    a, b, m = value.get(start), value.get(end), value.get(maximum)
    return all(nat(x) for x in (a, b, m)) and a <= b and b - a <= m


def _exact(
    value: Mapping[str, Any],
    expected: Mapping[str, Any],
    prefix: str,
    blockers: list[str],
) -> None:
    blockers.extend(
        f"{prefix}_{key}_mismatch"
        for key, expected_value in expected.items()
        if value.get(key) != expected_value
    )


def build_verifyos_independent_evidence_verification(
    *,
    source_verification_handoff_receipt: Mapping[str, Any],
    expected_source_verification_handoff_receipt_digest: str,
    independent_verification_evidence_bundle: Mapping[str, Any],
    expected_independent_verification_evidence_bundle_digest: str,
    independent_verification_execution: Mapping[str, Any],
    expected_independent_verification_execution_digest: str,
    independent_verification_result_review: Mapping[str, Any],
    expected_independent_verification_result_review_digest: str,
    independent_verification_context: Mapping[str, Any],
    expected_independent_verification_context_digest: str,
    verification_policy_digest: str,
    verifyos_responsibility_digest: str,
    verification_id: str,
    verification_bundle_digest: str,
) -> Result:
    source, evidence, execution, review, context = map(
        mapping,
        (
            source_verification_handoff_receipt,
            independent_verification_evidence_bundle,
            independent_verification_execution,
            independent_verification_result_review,
            independent_verification_context,
        ),
    )
    blockers: list[str] = []
    if not all((source, evidence, execution, review, context)):
        return Result(STATUS_BLOCKED, ["independent_verification_input_missing"], None)

    source_digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    evidence_value_digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    execution_value_digest = execution.get(EXECUTION_DIGEST_FIELD, "")
    review_value_digest = review.get(REVIEW_DIGEST_FIELD, "")
    context_value_digest = context.get(CONTEXT_DIGEST_FIELD, "")

    checks = (
        (
            source_digest == digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD),
            "source_handoff_receipt_digest_mismatch",
        ),
        (
            source_digest == expected_source_verification_handoff_receipt_digest,
            "source_handoff_expected_binding_mismatch",
        ),
        (set(evidence) == EVIDENCE_FIELDS, "evidence_bundle_schema_invalid"),
        (
            evidence_value_digest == evidence_digest(evidence),
            "independent_evidence_bundle_digest_mismatch",
        ),
        (
            evidence_value_digest
            == expected_independent_verification_evidence_bundle_digest,
            "evidence_bundle_expected_binding_mismatch",
        ),
        (set(execution) == EXECUTION_FIELDS, "verification_execution_schema_invalid"),
        (
            execution_value_digest == execution_digest(execution),
            "verification_execution_digest_mismatch",
        ),
        (
            execution_value_digest == expected_independent_verification_execution_digest,
            "verification_execution_expected_binding_mismatch",
        ),
        (set(review) == REVIEW_FIELDS, "verification_review_schema_invalid"),
        (
            review_value_digest == review_digest(review),
            "verification_review_digest_mismatch",
        ),
        (
            review_value_digest
            == expected_independent_verification_result_review_digest,
            "verification_review_expected_binding_mismatch",
        ),
        (set(context) == CONTEXT_FIELDS, "verification_context_schema_invalid"),
        (
            context_value_digest == context_digest(context),
            "verification_context_digest_mismatch",
        ),
        (
            context_value_digest == expected_independent_verification_context_digest,
            "verification_context_expected_binding_mismatch",
        ),
    )
    blockers.extend(name for ok, name in checks if not ok)

    _exact(
        source,
        {
            "kernel": "VerifyOS Sequential Epistemic Observation Verification Handoff Kernel",
            "kernel_version": "v0.1",
            "verifyos_version": "v0.13",
            "status": "VERIFYOS_SEQUENTIAL_EPISTEMIC_VERIFICATION_HANDOFF_ROUTED",
            "persistent_world_state_changed_by_handoff": False,
            "world_model_revision_incremented_by_handoff": False,
            "current_plan_revised_by_handoff": False,
            "current_policy_activated_by_handoff": False,
            "learning_delta_activated_by_handoff": False,
            "tool_invocation_performed": False,
            "external_side_effect_performed": False,
            "generalized_truth_claimed": False,
            "causal_verification_claimed": False,
            "selection_authority_granted_to_verifyos": False,
            "world_mutation_authority_granted": False,
            "policy_activation_authority_granted": False,
            "execution_authority_granted": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        },
        "source",
        blockers,
    )
    _exact(
        evidence,
        {
            "source_verification_handoff_receipt_digest": source_digest,
            "source_observability_receipt_digest": source.get(
                "source_observability_receipt_digest"
            ),
            "source_evidence_snapshot_digests": source.get("evidence_snapshot_digests"),
        },
        "evidence",
        blockers,
    )
    _exact(
        execution,
        {
            "source_verification_handoff_receipt_digest": source_digest,
            EVIDENCE_DIGEST_FIELD: evidence_value_digest,
            "verifier_id": source.get("verifier_id"),
            "verification_scope": source.get("verification_scope"),
        },
        "execution",
        blockers,
    )
    _exact(
        review,
        {
            "source_verification_handoff_receipt_digest": source_digest,
            EXECUTION_DIGEST_FIELD: execution_value_digest,
        },
        "review",
        blockers,
    )
    _exact(
        context,
        {
            "source_verification_handoff_receipt_digest": source_digest,
            EVIDENCE_DIGEST_FIELD: evidence_value_digest,
            EXECUTION_DIGEST_FIELD: execution_value_digest,
            REVIEW_DIGEST_FIELD: review_value_digest,
            "source_world_revision": source.get("resulting_world_revision"),
        },
        "context",
        blockers,
    )

    for field in (
        "source_lineage_digests",
        "resulting_lineage_digests",
        "source_responsibility_lineage_digests",
        "resulting_responsibility_lineage_digests",
    ):
        if not strings(source.get(field))[0]:
            blockers.append(f"{field}_invalid")
    for field in (
        "source_evidence_snapshot_digests",
        "independent_evidence_source_ids",
        "independent_evidence_artifact_digests",
    ):
        if not strings(evidence.get(field))[0]:
            blockers.append(f"{field}_invalid")
    if not strings(execution.get("verification_scope"))[0]:
        blockers.append("verification_scope_invalid")
    for field in (
        "prior_verification_session_ids",
        "prior_verification_nonce_digests",
        "prior_verification_execution_digests",
        "prior_verification_receipt_digests",
    ):
        if not strings(context.get(field), True)[0]:
            blockers.append(f"{field}_invalid")

    if context.get("requested_verification_operation_digest") != operation_digest(
        source, evidence, execution, review
    ):
        blockers.append("verification_operation_digest_mismatch")
    if context.get("exact_verification_cycle_digest") != cycle_digest(
        source, evidence, execution, review, context
    ):
        blockers.append("verification_cycle_digest_mismatch")
    if any(
        not isinstance(value, str) or not value
        for value in (
            verification_policy_digest,
            verifyos_responsibility_digest,
            verification_id,
        )
    ):
        blockers.append("verification_metadata_invalid")

    computed_bundle = bundle_digest(
        source_verification_handoff_receipt_digest=source_digest,
        independent_verification_evidence_bundle_digest=evidence_value_digest,
        independent_verification_execution_digest=execution_value_digest,
        independent_verification_result_review_digest=review_value_digest,
        independent_verification_context_digest=context_value_digest,
        requested_verification_operation_digest=context.get(
            "requested_verification_operation_digest"
        ),
        exact_verification_cycle_digest=context.get("exact_verification_cycle_digest"),
        verification_policy_digest=verification_policy_digest,
        verifyos_responsibility_digest=verifyos_responsibility_digest,
        verification_id=verification_id,
    )
    if computed_bundle != verification_bundle_digest:
        blockers.append("verification_bundle_digest_mismatch")
    if blockers:
        return Result(STATUS_BLOCKED, sorted(set(blockers)), None)

    source_supported = all(
        (
            source.get("verification_handoff_disposition") == SOURCE_SUPPORTED,
            source.get("verification_handoff_state_after") == SOURCE_STATE,
            source.get("verification_request_recorded") is True,
            source.get("independent_verification_handoff_prepared") is True,
            source.get("verification_completed") is False,
            source.get("verification_debt_open") is True,
        )
    )
    world_current = (
        context.get("current_world_revision") == source.get("resulting_world_revision")
    )
    correspondence = all(
        (
            evidence.get("source_correspondence_confirmed") is True,
            evidence.get("source_observability_receipt_digest")
            == source.get("source_observability_receipt_digest"),
        )
    )
    independence = all(
        (
            review.get("verifier_independence_confirmed") is True,
            review.get("reviewer_independence_confirmed") is True,
            isinstance(review.get("reviewer_id"), str),
            bool(review.get("reviewer_id")),
            review.get("reviewer_id")
            not in {source.get("verifier_id"), source.get("reviewer_id")},
        )
    )
    evidence_adequate = all(
        (
            evidence.get("evidence_integrity_confirmed") is True,
            evidence.get("provenance_integrity_confirmed") is True,
            review.get("evidence_integrity_adequate") is True,
        )
    )
    execution_current = _duration(
        execution,
        "execution_started_epoch",
        "execution_completed_epoch",
        "maximum_execution_duration",
    )
    review_current = _duration(
        review,
        "review_started_epoch",
        "review_completed_epoch",
        "maximum_review_duration",
    )
    protocol_adequate = all(
        (
            execution_current,
            execution.get("falsification_challenge_executed") is True,
            review.get("protocol_execution_adequate") is True,
        )
    )
    planned = execution.get("planned_reproduction_attempts")
    completed = execution.get("completed_reproduction_attempts")
    successful = execution.get("successful_reproduction_attempts")
    reproduction_counts_valid = (
        pos(planned) and nat(completed) and nat(successful) and successful <= completed
    )
    outcome = execution.get("verification_outcome")
    passed_semantics = all(
        (
            outcome == OUTCOME_PASSED,
            reproduction_counts_valid,
            completed >= planned if reproduction_counts_valid else False,
            successful >= planned if reproduction_counts_valid else False,
            execution.get("falsification_challenge_passed") is True,
            execution.get("acceptance_criteria_satisfied") is True,
            evidence.get("evidence_conclusive") is True,
        )
    )
    failed_semantics = all(
        (
            outcome == OUTCOME_FAILED,
            reproduction_counts_valid,
            completed >= planned if reproduction_counts_valid else False,
            evidence.get("evidence_conclusive") is True,
            any(
                (
                    execution.get("falsification_challenge_passed") is False,
                    execution.get("acceptance_criteria_satisfied") is False,
                )
            ),
        )
    )
    indeterminate_semantics = all(
        (
            outcome == OUTCOME_INDETERMINATE,
            reproduction_counts_valid,
            any(
                (
                    completed < planned if reproduction_counts_valid else False,
                    evidence.get("evidence_conclusive") is False,
                )
            ),
        )
    )
    outcome_semantics_valid = any(
        (passed_semantics, failed_semantics, indeterminate_semantics)
    )
    reproduction_adequate = all(
        (reproduction_counts_valid, review.get("reproduction_adequate") is True)
    )
    acceptance_adequate = all(
        (
            outcome in OUTCOMES,
            outcome_semantics_valid,
            review.get("acceptance_adjudication_adequate") is True,
        )
    )
    review_adequate = all(
        (review_current, review.get("outcome_supported") is True)
    )
    replay = any(
        (
            context.get("verification_session_id")
            in context.get("prior_verification_session_ids", []),
            context.get("verification_nonce_digest")
            in context.get("prior_verification_nonce_digests", []),
            execution_value_digest
            in context.get("prior_verification_execution_digests", []),
            verification_bundle_digest
            in context.get("prior_verification_receipt_digests", []),
        )
    )
    mutation = any(
        (
            execution.get("observation_recollection_performed") is True,
            execution.get("current_state_mutation_performed") is True,
            review.get("no_observation_recollection") is not True,
            review.get("no_current_state_mutation") is not True,
        )
    )
    authority = any(
        (
            execution.get("authority_escalation_requested") is True,
            execution.get("generalized_truth_claimed") is True,
            execution.get("causal_verification_claimed") is True,
            review.get("no_authority_escalation") is not True,
            review.get("no_truth_claim") is not True,
            review.get("no_causal_claim") is not True,
        )
    )

    if replay:
        disposition = D_REPLAY
    elif not source_supported or not world_current:
        disposition = D_SOURCE
    elif not correspondence:
        disposition = D_CORRESPONDENCE
    elif not independence:
        disposition = D_INDEPENDENCE
    elif not evidence_adequate:
        disposition = D_EVIDENCE
    elif not protocol_adequate:
        disposition = D_PROTOCOL
    elif not reproduction_adequate:
        disposition = D_REPRODUCTION
    elif not acceptance_adequate:
        disposition = D_ACCEPTANCE
    elif not review_adequate:
        disposition = D_REVIEW
    elif mutation:
        disposition = D_MUTATION
    elif authority:
        disposition = D_AUTHORITY
    elif outcome == OUTCOME_PASSED:
        disposition = D_PASSED
    elif outcome == OUTCOME_FAILED:
        disposition = D_FAILED
    else:
        disposition = D_INDETERMINATE

    outcome_recorded = disposition in OUTCOME_DISPOSITIONS
    recorded_outcome = outcome if outcome_recorded else None
    debt_open = disposition == D_INDETERMINATE or not outcome_recorded
    reobservation_required = disposition == D_INDETERMINATE
    lineage = sorted(
        set(source["resulting_lineage_digests"])
        | {
            source_digest,
            evidence_value_digest,
            execution_value_digest,
            review_value_digest,
            context_value_digest,
            verification_bundle_digest,
        }
    )
    responsibility = sorted(
        set(source["resulting_responsibility_lineage_digests"])
        | {verifyos_responsibility_digest}
    )
    receipt = {
        "kernel": "VerifyOS Independent Evidence Verification Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.14",
        "status": "VERIFYOS_INDEPENDENT_EVIDENCE_VERIFICATION_ROUTED",
        "source_verification_handoff_receipt_digest": source_digest,
        EVIDENCE_DIGEST_FIELD: evidence_value_digest,
        EXECUTION_DIGEST_FIELD: execution_value_digest,
        REVIEW_DIGEST_FIELD: review_value_digest,
        CONTEXT_DIGEST_FIELD: context_value_digest,
        "verification_policy_digest": verification_policy_digest,
        "verifyos_responsibility_digest": verifyos_responsibility_digest,
        "verification_id": verification_id,
        "verification_bundle_digest": verification_bundle_digest,
        "verification_disposition": disposition,
        "verification_outcome": recorded_outcome,
        "verification_state_before": SOURCE_STATE,
        "verification_state_after": STATE_AFTER if outcome_recorded else SOURCE_STATE,
        "source_verification_handoff_prepared": source[
            "independent_verification_handoff_prepared"
        ],
        "independent_evidence_bundle_bound": outcome_recorded,
        "verification_protocol_executed": outcome_recorded,
        "reproduction_plan_executed": outcome_recorded,
        "falsification_challenge_executed": outcome_recorded,
        "verification_result_reviewed": outcome_recorded,
        "verification_receipt_recorded": outcome_recorded,
        "independent_evidence_verification_executed": outcome_recorded,
        "verification_completed": outcome_recorded,
        "verification_debt_open": debt_open,
        "reobservation_required": reobservation_required,
        "world_disposition_candidate_generated": False,
        "persistent_world_state_changed_by_verification": False,
        "world_model_revision_incremented_by_verification": False,
        "current_plan_revised_by_verification": False,
        "current_policy_activated_by_verification": False,
        "learning_delta_activated_by_verification": False,
        "tool_invocation_performed_by_kernel": False,
        "external_side_effect_performed_by_kernel": False,
        "generalized_truth_claimed": False,
        "causal_attribution_claimed": False,
        "world_adoption_authority_granted": False,
        "world_rejection_authority_granted": False,
        "world_mutation_authority_granted": False,
        "policy_activation_authority_granted": False,
        "execution_authority_granted": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "source_world_revision": source["resulting_world_revision"],
        "resulting_world_revision": source["resulting_world_revision"],
        "source_lineage_digests": source["resulting_lineage_digests"],
        "resulting_lineage_digests": lineage,
        "source_responsibility_lineage_digests": source[
            "resulting_responsibility_lineage_digests"
        ],
        "resulting_responsibility_lineage_digests": responsibility,
        "verifier_id": execution["verifier_id"],
        "reviewer_id": review["reviewer_id"],
        "verification_scope": execution["verification_scope"],
        "independent_evidence_artifact_digests": evidence[
            "independent_evidence_artifact_digests"
        ],
        "completed_reproduction_attempts": completed,
        "successful_reproduction_attempts": successful,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return Result(STATUS_READY, [], receipt)


VerifyOSIndependentEvidenceVerificationResult = Result
compute_independent_verification_evidence_bundle_digest = evidence_digest
compute_independent_verification_execution_digest = execution_digest
compute_independent_verification_result_review_digest = review_digest
compute_independent_verification_context_digest = context_digest
compute_requested_verification_operation_digest = operation_digest
compute_exact_verification_cycle_digest = cycle_digest
compute_verification_bundle_digest = bundle_digest

DISPOSITION_PASSED = D_PASSED
DISPOSITION_FAILED = D_FAILED
DISPOSITION_INDETERMINATE = D_INDETERMINATE
DISPOSITION_SOURCE_REPAIR = D_SOURCE
DISPOSITION_CORRESPONDENCE_REPAIR = D_CORRESPONDENCE
DISPOSITION_INDEPENDENCE_REPAIR = D_INDEPENDENCE
DISPOSITION_EVIDENCE_REPAIR = D_EVIDENCE
DISPOSITION_PROTOCOL_REPAIR = D_PROTOCOL
DISPOSITION_REPRODUCTION_REPAIR = D_REPRODUCTION
DISPOSITION_ACCEPTANCE_REPAIR = D_ACCEPTANCE
DISPOSITION_REVIEW_REPAIR = D_REVIEW
DISPOSITION_REPLAY_REJECTED = D_REPLAY
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = D_MUTATION
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = D_AUTHORITY
