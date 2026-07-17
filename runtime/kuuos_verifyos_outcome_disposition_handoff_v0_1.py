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
    strings,
)
from runtime.kuuos_verifyos_independent_evidence_verification_v0_1 import (
    DISPOSITION_FAILED as SOURCE_FAILED,
    DISPOSITION_INDETERMINATE as SOURCE_INDETERMINATE,
    DISPOSITION_PASSED as SOURCE_PASSED,
    OUTCOME_FAILED,
    OUTCOME_INDETERMINATE,
    OUTCOME_PASSED,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    STATE_AFTER as SOURCE_STATE,
)

RECEIPT_DIGEST_FIELD = "verifyos_outcome_disposition_handoff_receipt_digest"
REQUEST_DIGEST_FIELD = "outcome_disposition_request_digest"
REVIEW_DIGEST_FIELD = "outcome_disposition_review_digest"
CONTEXT_DIGEST_FIELD = "outcome_disposition_context_digest"
STATE_AFTER = SOURCE_STATE + "_outcome_disposition_handoff_prepared"

CANDIDATE_ADOPT = "adopt_candidate"
CANDIDATE_REJECT = "reject_candidate"
CANDIDATE_DEFER = "defer_candidate"
CANDIDATE_REOBSERVE = "reobservation_candidate"
CANDIDATES = {
    CANDIDATE_ADOPT,
    CANDIDATE_REJECT,
    CANDIDATE_DEFER,
    CANDIDATE_REOBSERVE,
}

D_ADOPT = "adopt_disposition_candidate_prepared"
D_REJECT = "reject_disposition_candidate_prepared"
D_DEFER = "defer_disposition_candidate_prepared"
D_REOBSERVE = "reobservation_disposition_candidate_prepared"
D_SOURCE = "source_verification_receipt_repair_required"
D_OUTCOME = "verification_outcome_correspondence_repair_required"
D_AUTHORITY_REVIEW = "disposition_authority_review_repair_required"
D_EVIDENCE = "evidence_preservation_repair_required"
D_APPEAL = "appeal_route_repair_required"
D_DEBT = "verification_debt_preservation_repair_required"
D_WINDOW = "disposition_window_repair_required"
D_REPLAY = "disposition_replay_conflict_rejected"
D_MUTATION = "current_state_mutation_rejected"
D_AUTHORITY = "authority_escalation_rejected"

CANDIDATE_DISPOSITIONS = {D_ADOPT, D_REJECT, D_DEFER, D_REOBSERVE}

REQUEST_FIELDS = {
    "source_verification_receipt_digest",
    "source_verification_outcome",
    "requested_disposition_candidate",
    "disposition_authority_source_digest",
    "disposition_policy_digest",
    "governance_review_route_digest",
    "appeal_review_route_digest",
    "evidence_preservation_digest",
    "source_evidence_artifact_digests",
    "reobservation_scope_digests",
    "preserve_verification_debt",
    "requester_id",
    "request_created_epoch",
    "request_expires_epoch",
    "maximum_request_duration",
    "current_state_mutation_requested",
    "policy_activation_requested",
    "execution_requested",
    "generalized_truth_claimed",
    "causal_attribution_claimed",
    REQUEST_DIGEST_FIELD,
}

REVIEW_FIELDS = {
    "source_verification_receipt_digest",
    REQUEST_DIGEST_FIELD,
    "reviewer_id",
    "reviewer_independence_confirmed",
    "outcome_correspondence_confirmed",
    "authority_source_adequate",
    "evidence_preservation_confirmed",
    "appeal_route_confirmed",
    "open_debt_preserved",
    "world_mutation_not_authorized",
    "policy_activation_not_authorized",
    "execution_not_authorized",
    "no_truth_claim",
    "no_causal_claim",
    "review_started_epoch",
    "review_completed_epoch",
    "maximum_review_duration",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_verification_receipt_digest",
    REQUEST_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    "source_world_revision",
    "current_world_revision",
    "disposition_session_id",
    "disposition_nonce_digest",
    "prior_disposition_session_ids",
    "prior_disposition_nonce_digests",
    "prior_disposition_request_digests",
    "prior_disposition_receipt_digests",
    "requested_disposition_operation_digest",
    "exact_disposition_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass(frozen=True)
class Result:
    status: str
    blockers: list[str]
    receipt: dict[str, Any] | None


def request_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, REQUEST_DIGEST_FIELD)


def review_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, REVIEW_DIGEST_FIELD)


def context_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, CONTEXT_DIGEST_FIELD)


def operation_digest(
    source: Mapping[str, Any], request: Mapping[str, Any], review: Mapping[str, Any]
) -> str:
    return canonical_digest(
        {
            "source": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
            "outcome": source.get("verification_outcome"),
            "request": request.get(REQUEST_DIGEST_FIELD),
            "review": review.get(REVIEW_DIGEST_FIELD),
            "revision": source.get("resulting_world_revision"),
            "before": SOURCE_STATE,
            "after": STATE_AFTER,
        }
    )


def cycle_digest(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
            "request": request.get(REQUEST_DIGEST_FIELD),
            "review": review.get(REVIEW_DIGEST_FIELD),
            "session": context.get("disposition_session_id"),
            "nonce": context.get("disposition_nonce_digest"),
            "revision": context.get("current_world_revision"),
            "operation": context.get("requested_disposition_operation_digest"),
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


def build_verifyos_outcome_disposition_handoff(
    *,
    source_verification_receipt: Mapping[str, Any],
    expected_source_verification_receipt_digest: str,
    outcome_disposition_request: Mapping[str, Any],
    expected_outcome_disposition_request_digest: str,
    outcome_disposition_review: Mapping[str, Any],
    expected_outcome_disposition_review_digest: str,
    outcome_disposition_context: Mapping[str, Any],
    expected_outcome_disposition_context_digest: str,
    disposition_policy_digest: str,
    verifyos_responsibility_digest: str,
    disposition_handoff_id: str,
    disposition_bundle_digest: str,
) -> Result:
    source, request, review, context = map(
        mapping,
        (
            source_verification_receipt,
            outcome_disposition_request,
            outcome_disposition_review,
            outcome_disposition_context,
        ),
    )
    blockers: list[str] = []
    if not all((source, request, review, context)):
        return Result(STATUS_BLOCKED, ["outcome_disposition_input_missing"], None)

    source_digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    request_value_digest = request.get(REQUEST_DIGEST_FIELD, "")
    review_value_digest = review.get(REVIEW_DIGEST_FIELD, "")
    context_value_digest = context.get(CONTEXT_DIGEST_FIELD, "")

    checks = (
        (
            source_digest == digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD),
            "source_verification_receipt_digest_mismatch",
        ),
        (
            source_digest == expected_source_verification_receipt_digest,
            "source_verification_expected_binding_mismatch",
        ),
        (set(request) == REQUEST_FIELDS, "disposition_request_schema_invalid"),
        (
            request_value_digest == request_digest(request),
            "disposition_request_digest_mismatch",
        ),
        (
            request_value_digest == expected_outcome_disposition_request_digest,
            "disposition_request_expected_binding_mismatch",
        ),
        (set(review) == REVIEW_FIELDS, "disposition_review_schema_invalid"),
        (
            review_value_digest == review_digest(review),
            "disposition_review_digest_mismatch",
        ),
        (
            review_value_digest == expected_outcome_disposition_review_digest,
            "disposition_review_expected_binding_mismatch",
        ),
        (set(context) == CONTEXT_FIELDS, "disposition_context_schema_invalid"),
        (
            context_value_digest == context_digest(context),
            "disposition_context_digest_mismatch",
        ),
        (
            context_value_digest == expected_outcome_disposition_context_digest,
            "disposition_context_expected_binding_mismatch",
        ),
    )
    blockers.extend(name for ok, name in checks if not ok)

    _exact(
        source,
        {
            "kernel": "VerifyOS Independent Evidence Verification Kernel",
            "kernel_version": "v0.1",
            "verifyos_version": "v0.14",
            "status": "VERIFYOS_INDEPENDENT_EVIDENCE_VERIFICATION_ROUTED",
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
        },
        "source",
        blockers,
    )
    _exact(
        request,
        {
            "source_verification_receipt_digest": source_digest,
            "source_verification_outcome": source.get("verification_outcome"),
            "disposition_policy_digest": disposition_policy_digest,
            "source_evidence_artifact_digests": source.get(
                "independent_evidence_artifact_digests"
            ),
        },
        "request",
        blockers,
    )
    _exact(
        review,
        {
            "source_verification_receipt_digest": source_digest,
            REQUEST_DIGEST_FIELD: request_value_digest,
        },
        "review",
        blockers,
    )
    _exact(
        context,
        {
            "source_verification_receipt_digest": source_digest,
            REQUEST_DIGEST_FIELD: request_value_digest,
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
        "independent_evidence_artifact_digests",
    ):
        if not strings(source.get(field))[0]:
            blockers.append(f"source_{field}_invalid")
    if not strings(request.get("source_evidence_artifact_digests"))[0]:
        blockers.append("source_evidence_artifact_digests_invalid")
    if not strings(request.get("reobservation_scope_digests"), True)[0]:
        blockers.append("reobservation_scope_digests_invalid")
    for field in (
        "prior_disposition_session_ids",
        "prior_disposition_nonce_digests",
        "prior_disposition_request_digests",
        "prior_disposition_receipt_digests",
    ):
        if not strings(context.get(field), True)[0]:
            blockers.append(f"{field}_invalid")
    if request.get("requested_disposition_candidate") not in CANDIDATES:
        blockers.append("requested_disposition_candidate_invalid")
    if any(
        not isinstance(value, str) or not value
        for value in (
            request.get("disposition_authority_source_digest"),
            request.get("governance_review_route_digest"),
            request.get("evidence_preservation_digest"),
            request.get("requester_id"),
            review.get("reviewer_id"),
            disposition_policy_digest,
            verifyos_responsibility_digest,
            disposition_handoff_id,
        )
    ):
        blockers.append("disposition_metadata_invalid")

    if context.get("requested_disposition_operation_digest") != operation_digest(
        source, request, review
    ):
        blockers.append("disposition_operation_digest_mismatch")
    if context.get("exact_disposition_cycle_digest") != cycle_digest(
        source, request, review, context
    ):
        blockers.append("disposition_cycle_digest_mismatch")

    computed_bundle = bundle_digest(
        source_verification_receipt_digest=source_digest,
        outcome_disposition_request_digest=request_value_digest,
        outcome_disposition_review_digest=review_value_digest,
        outcome_disposition_context_digest=context_value_digest,
        requested_disposition_operation_digest=context.get(
            "requested_disposition_operation_digest"
        ),
        exact_disposition_cycle_digest=context.get("exact_disposition_cycle_digest"),
        disposition_policy_digest=disposition_policy_digest,
        verifyos_responsibility_digest=verifyos_responsibility_digest,
        disposition_handoff_id=disposition_handoff_id,
    )
    if computed_bundle != disposition_bundle_digest:
        blockers.append("disposition_bundle_digest_mismatch")
    if blockers:
        return Result(STATUS_BLOCKED, sorted(set(blockers)), None)

    outcome = source.get("verification_outcome")
    source_disposition = source.get("verification_disposition")
    source_completion_valid = all(
        (
            source.get("verification_receipt_recorded") is True,
            source.get("independent_evidence_verification_executed") is True,
            source.get("verification_completed") is True,
        )
    )
    source_outcome_valid = source_completion_valid and any(
        (
            source_disposition == SOURCE_PASSED
            and outcome == OUTCOME_PASSED
            and source.get("verification_debt_open") is False
            and source.get("reobservation_required") is False,
            source_disposition == SOURCE_FAILED
            and outcome == OUTCOME_FAILED
            and source.get("verification_debt_open") is False
            and source.get("reobservation_required") is False,
            source_disposition == SOURCE_INDETERMINATE
            and outcome == OUTCOME_INDETERMINATE
            and source.get("verification_debt_open") is True
            and source.get("reobservation_required") is True,
        )
    )
    world_current = (
        context.get("current_world_revision") == source.get("resulting_world_revision")
    )
    requested_candidate = request.get("requested_disposition_candidate")
    outcome_correspondence = all(
        (
            review.get("outcome_correspondence_confirmed") is True,
            any(
                (
                    outcome == OUTCOME_PASSED
                    and requested_candidate == CANDIDATE_ADOPT,
                    outcome == OUTCOME_FAILED
                    and requested_candidate == CANDIDATE_REJECT,
                    outcome == OUTCOME_INDETERMINATE
                    and requested_candidate in {CANDIDATE_DEFER, CANDIDATE_REOBSERVE},
                )
            ),
        )
    )
    reviewer_independent = all(
        (
            review.get("reviewer_independence_confirmed") is True,
            review.get("reviewer_id")
            not in {
                request.get("requester_id"),
                source.get("verifier_id"),
                source.get("reviewer_id"),
            },
        )
    )
    authority_review_adequate = all(
        (
            reviewer_independent,
            review.get("authority_source_adequate") is True,
        )
    )
    evidence_preserved = all(
        (
            review.get("evidence_preservation_confirmed") is True,
            request.get("source_evidence_artifact_digests")
            == source.get("independent_evidence_artifact_digests"),
        )
    )
    appeal_adequate = (
        requested_candidate != CANDIDATE_REJECT
        or all(
            (
                isinstance(request.get("appeal_review_route_digest"), str),
                bool(request.get("appeal_review_route_digest")),
                review.get("appeal_route_confirmed") is True,
            )
        )
    )
    debt_preserved = (
        outcome != OUTCOME_INDETERMINATE
        or all(
            (
                request.get("preserve_verification_debt") is True,
                review.get("open_debt_preserved") is True,
            )
        )
    )
    reobservation_scope_adequate = (
        requested_candidate != CANDIDATE_REOBSERVE
        or bool(request.get("reobservation_scope_digests"))
    )
    request_current = _duration(
        request,
        "request_created_epoch",
        "request_expires_epoch",
        "maximum_request_duration",
    )
    review_current = _duration(
        review,
        "review_started_epoch",
        "review_completed_epoch",
        "maximum_review_duration",
    )
    replay = any(
        (
            context.get("disposition_session_id")
            in context.get("prior_disposition_session_ids", []),
            context.get("disposition_nonce_digest")
            in context.get("prior_disposition_nonce_digests", []),
            request_value_digest in context.get("prior_disposition_request_digests", []),
            disposition_bundle_digest
            in context.get("prior_disposition_receipt_digests", []),
        )
    )
    mutation = any(
        (
            request.get("current_state_mutation_requested") is True,
            review.get("world_mutation_not_authorized") is not True,
        )
    )
    authority = any(
        (
            request.get("policy_activation_requested") is True,
            request.get("execution_requested") is True,
            request.get("generalized_truth_claimed") is True,
            request.get("causal_attribution_claimed") is True,
            review.get("policy_activation_not_authorized") is not True,
            review.get("execution_not_authorized") is not True,
            review.get("no_truth_claim") is not True,
            review.get("no_causal_claim") is not True,
        )
    )

    if replay:
        disposition = D_REPLAY
    elif not source_outcome_valid or not world_current:
        disposition = D_SOURCE
    elif not outcome_correspondence:
        disposition = D_OUTCOME
    elif not authority_review_adequate:
        disposition = D_AUTHORITY_REVIEW
    elif not evidence_preserved:
        disposition = D_EVIDENCE
    elif not appeal_adequate:
        disposition = D_APPEAL
    elif not debt_preserved or not reobservation_scope_adequate:
        disposition = D_DEBT
    elif not request_current or not review_current:
        disposition = D_WINDOW
    elif mutation:
        disposition = D_MUTATION
    elif authority:
        disposition = D_AUTHORITY
    elif requested_candidate == CANDIDATE_ADOPT:
        disposition = D_ADOPT
    elif requested_candidate == CANDIDATE_REJECT:
        disposition = D_REJECT
    elif requested_candidate == CANDIDATE_DEFER:
        disposition = D_DEFER
    else:
        disposition = D_REOBSERVE

    candidate_prepared = disposition in CANDIDATE_DISPOSITIONS
    candidate = requested_candidate if candidate_prepared else None
    lineage = sorted(
        set(source["resulting_lineage_digests"])
        | {
            source_digest,
            request_value_digest,
            review_value_digest,
            context_value_digest,
            disposition_bundle_digest,
        }
    )
    responsibility = sorted(
        set(source["resulting_responsibility_lineage_digests"])
        | {verifyos_responsibility_digest}
    )
    receipt = {
        "kernel": "VerifyOS Outcome Disposition Handoff Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.15",
        "status": "VERIFYOS_OUTCOME_DISPOSITION_HANDOFF_ROUTED",
        "source_verification_receipt_digest": source_digest,
        REQUEST_DIGEST_FIELD: request_value_digest,
        REVIEW_DIGEST_FIELD: review_value_digest,
        CONTEXT_DIGEST_FIELD: context_value_digest,
        "disposition_policy_digest": disposition_policy_digest,
        "verifyos_responsibility_digest": verifyos_responsibility_digest,
        "disposition_handoff_id": disposition_handoff_id,
        "disposition_bundle_digest": disposition_bundle_digest,
        "outcome_disposition_handoff_disposition": disposition,
        "source_verification_outcome": outcome,
        "outcome_disposition_candidate": candidate,
        "outcome_disposition_state_before": SOURCE_STATE,
        "outcome_disposition_state_after": STATE_AFTER if candidate_prepared else SOURCE_STATE,
        "outcome_disposition_handoff_prepared": candidate_prepared,
        "world_disposition_candidate_generated": candidate_prepared,
        "adopt_candidate_generated": candidate == CANDIDATE_ADOPT,
        "reject_candidate_generated": candidate == CANDIDATE_REJECT,
        "defer_candidate_generated": candidate == CANDIDATE_DEFER,
        "reobservation_candidate_generated": candidate == CANDIDATE_REOBSERVE,
        "governance_review_required": candidate_prepared,
        "fresh_world_authorization_required": candidate_prepared,
        "appeal_review_required": candidate == CANDIDATE_REJECT,
        "evidence_preserved": candidate_prepared,
        "verification_debt_open": source["verification_debt_open"],
        "reobservation_required": source["reobservation_required"],
        "world_disposition_completed": False,
        "world_commit_ready": False,
        "persistent_world_state_changed_by_handoff": False,
        "world_model_revision_incremented_by_handoff": False,
        "current_plan_revised_by_handoff": False,
        "current_policy_activated_by_handoff": False,
        "learning_delta_activated_by_handoff": False,
        "observation_recollection_performed_by_kernel": False,
        "tool_invocation_performed_by_kernel": False,
        "external_side_effect_performed_by_kernel": False,
        "generalized_truth_claimed": False,
        "causal_attribution_claimed": False,
        "world_adoption_authority_granted": False,
        "world_rejection_authority_granted": False,
        "world_mutation_authority_granted": False,
        "policy_activation_authority_granted": False,
        "execution_authority_granted": False,
        "observation_execution_authority_granted": False,
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
        "requester_id": request["requester_id"],
        "reviewer_id": review["reviewer_id"],
        "source_evidence_artifact_digests": request[
            "source_evidence_artifact_digests"
        ],
        "reobservation_scope_digests": request["reobservation_scope_digests"],
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return Result(STATUS_READY, [], receipt)


VerifyOSOutcomeDispositionHandoffResult = Result
compute_outcome_disposition_request_digest = request_digest
compute_outcome_disposition_review_digest = review_digest
compute_outcome_disposition_context_digest = context_digest
compute_requested_disposition_operation_digest = operation_digest
compute_exact_disposition_cycle_digest = cycle_digest
compute_outcome_disposition_bundle_digest = bundle_digest

DISPOSITION_ADOPT = D_ADOPT
DISPOSITION_REJECT = D_REJECT
DISPOSITION_DEFER = D_DEFER
DISPOSITION_REOBSERVE = D_REOBSERVE
DISPOSITION_SOURCE_REPAIR = D_SOURCE
DISPOSITION_OUTCOME_REPAIR = D_OUTCOME
DISPOSITION_AUTHORITY_REVIEW_REPAIR = D_AUTHORITY_REVIEW
DISPOSITION_EVIDENCE_REPAIR = D_EVIDENCE
DISPOSITION_APPEAL_REPAIR = D_APPEAL
DISPOSITION_DEBT_REPAIR = D_DEBT
DISPOSITION_WINDOW_REPAIR = D_WINDOW
DISPOSITION_REPLAY_REJECTED = D_REPLAY
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = D_MUTATION
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = D_AUTHORITY
