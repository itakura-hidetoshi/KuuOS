#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ADDITIONAL_EVIDENCE,
    DISPOSITION_ADVERSE_REVIEW,
    DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CAUSAL_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    DISPOSITION_DISTRIBUTIONAL_REVIEW,
    DISPOSITION_DUKKHA_REPAIR,
    DISPOSITION_DURABILITY_REVIEW,
    DISPOSITION_FACT_REPAIR,
    DISPOSITION_MAINTENANCE_WINDOW_REPAIR,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_SOURCE_REPAIR,
    DISPOSITION_SUPPORTED,
    DISPOSITION_UNCERTAINTY_REPAIR,
    DISPOSITION_WORLD_REFRESH,
    EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_EVIDENCE_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake,
    canonical_digest,
    compute_exact_future_only_learning_cycle_digest,
    compute_future_only_learning_bundle_digest,
    compute_future_only_learning_evidence_packet_digest,
    compute_future_only_learning_intake_context_digest,
    compute_future_only_learning_review_certificate_digest,
    compute_requested_future_only_learning_operation_digest,
)
from scripts.check_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1 import (
    _build as build_verifyos_v010,
)


def _source() -> dict:
    result = build_verifyos_v010()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    source = deepcopy(result.receipt)
    assert source["verifyos_version"] == "v0.10"
    assert source["realized_dukkha_verification_disposition"] == (
        "realized_dukkha_verification_supported"
    )
    assert source["realized_dukkha_verification_state_after"] == STATE_BEFORE
    assert source["world_fact_confirmed"] is True
    assert source["causal_attribution_confirmed"] is True
    assert source["dukkha_reduction_realized_confirmed"] is True
    assert source["future_learning_intake_admitted"] is True
    return source


def _evidence(source: dict) -> dict:
    source_packet = source["realized_dukkha_verification_evidence_packet"]
    evidence = {
        "source_realized_dukkha_verification_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        "source_realized_dukkha_verification_evidence_packet_digest": source[
            SOURCE_EVIDENCE_DIGEST_FIELD
        ],
        "source_realized_dukkha_verification_review_certificate_digest": source[
            SOURCE_REVIEW_DIGEST_FIELD
        ],
        "source_realized_dukkha_verification_record_digest": source[
            "realized_dukkha_verification_record_digest"
        ],
        "source_realized_dukha_verification_debt_consumption_record_digest": source[
            "realized_dukkha_verification_debt_consumption_record_digest"
        ],
        "source_bounded_realized_dukkha_confirmation_binding_digest": source[
            "bounded_realized_dukkha_confirmation_binding_digest"
        ],
        "source_future_learning_handoff_envelope_digest": source[
            "future_learning_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": source["world_candidate_fact_digest"],
        "world_candidate_relation_digest": source["world_candidate_relation_digest"],
        "resulting_world_state_digest": source["source_world_model_state_digest"],
        "resulting_world_revision": source["source_world_model_revision"],
        "realized_dukha_observation_digest": source_packet[
            "realized_dukkha_observation_digest"
        ],
        "realized_dukha_effect_estimate_digest": source_packet[
            "realized_dukkha_effect_estimate_digest"
        ],
        "learning_target_digest": "learnos-bounded-realized-dukkha-target-v04-001",
        "future_only_learning_delta_digest": "learnos-future-only-delta-v04-001",
        "maintenance_policy_candidate_digest": "learnos-maintenance-policy-candidate-v04-001",
        "maintenance_window_digest": "learnos-maintenance-window-v04-001",
        "durability_monitoring_specification_digest": "learnos-durability-monitor-v04-001",
        "adverse_effect_monitoring_specification_digest": "learnos-adverse-monitor-v04-001",
        "distributional_monitoring_specification_digest": "learnos-distributional-monitor-v04-001",
        "reobservation_trigger_digest": "learnos-reobservation-trigger-v04-001",
        "retention_window_digest": "learnos-retention-window-v04-001",
        "uncertainty_digest": "learnos-future-only-uncertainty-v04-001",
        "calibration_digest": "learnos-future-only-calibration-v04-001",
        "provenance_chain_digests": sorted(
            {
                source[SOURCE_RECEIPT_DIGEST_FIELD],
                source["bounded_realized_dukkha_confirmation_binding_digest"],
                source["future_learning_handoff_envelope_digest"],
                "learnos-future-only-provenance-v04-001",
            }
        ),
        "tamper_evidence_digest": "learnos-future-only-tamper-evidence-v04-001",
        "protected_group_learning_impact_digest": "learnos-protected-group-learning-impact-v04-001",
        "future_subject_learning_impact_digest": "learnos-future-subject-learning-impact-v04-001",
        "evidence_collector_id": "learnos-future-only-evidence-collector-v04",
        "evidence_source_id": "independent-future-only-learning-source-v04",
        "collection_started_epoch": 145,
        "collection_completed_epoch": 146,
        "maximum_collection_duration": 4,
        "independent_future_only_learning_evidence": True,
        "exactly_one_future_only_learning_evidence_collection": True,
        "current_world_mutation_performed": False,
        "current_plan_revised": False,
        "current_policy_activated": False,
        "generalized_benefit_claimed": False,
        "authority_escalation_claimed": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = compute_future_only_learning_evidence_packet_digest(
        evidence
    )
    return evidence


def _review(source: dict, evidence: dict) -> dict:
    review = {
        "source_realized_dukha_verification_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        "source_bounded_realized_dukha_confirmation_binding_digest": source[
            "bounded_realized_dukkha_confirmation_binding_digest"
        ],
        "source_future_learning_handoff_envelope_digest": source[
            "future_learning_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "realized_dukha_effect_estimate_digest": evidence[
            "realized_dukha_effect_estimate_digest"
        ],
        "learning_target_digest": evidence["learning_target_digest"],
        "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": evidence[
            "maintenance_policy_candidate_digest"
        ],
        "reviewer_id": "learnos-future-only-learning-reviewer-v04",
        "verification_method_digest": "learnos-future-only-learning-method-v04-001",
        "verification_evidence_digest": "learnos-future-only-learning-review-evidence-v04-001",
        "review_started_epoch": 146,
        "review_completed_epoch": 147,
        "maximum_review_duration": 4,
        "source_receipt_correspondence_confirmed": True,
        "source_bounded_world_fact_correspondence_confirmed": True,
        "source_causal_attribution_correspondence_confirmed": True,
        "source_realized_dukkha_correspondence_confirmed": True,
        "maintenance_window_adequate": True,
        "durability_monitoring_adequate": True,
        "adverse_effect_monitoring_adequate": True,
        "distributional_monitoring_adequate": True,
        "uncertainty_adequate": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "no_current_state_mutation": True,
        "no_authority_escalation": True,
    }
    review[REVIEW_DIGEST_FIELD] = compute_future_only_learning_review_certificate_digest(review)
    return review


def _context(source: dict, evidence: dict, review: dict) -> dict:
    source_epoch = source["realized_dukkha_verification_record"][
        "realized_dukkha_verification_intake_epoch"
    ]
    context = {
        "source_realized_dukkha_verification_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_persistent_world_storage_target_digest": source[
            "source_persistent_world_storage_target_digest"
        ],
        "source_realized_dukkha_verification_epoch": source_epoch,
        "future_only_learning_intake_epoch": source_epoch + 3,
        "maximum_future_only_learning_intake_delay": 8,
        "future_only_learning_intake_session_id": "learnos-future-only-learning-intake-v04-001",
        "future_only_learning_intake_nonce_digest": "learnos-future-only-learning-nonce-v04-001",
        "prior_future_only_learning_intake_session_ids": [],
        "prior_future_only_learning_evidence_packet_digests": [],
        "prior_future_only_learning_review_certificate_digests": [],
        "prior_future_only_learning_intake_nonce_digests": [],
        "prior_future_only_learning_source_receipt_digests": [],
        "requested_future_only_learning_operation_digest": (
            compute_requested_future_only_learning_operation_digest(
                source, evidence, review
            )
        ),
        "exact_future_only_learning_cycle_digest": "",
    }
    context["exact_future_only_learning_cycle_digest"] = (
        compute_exact_future_only_learning_cycle_digest(
            source, evidence, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = compute_future_only_learning_intake_context_digest(
        context
    )
    return context


def _redigest_evidence(evidence: dict) -> dict:
    value = deepcopy(evidence)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = compute_future_only_learning_evidence_packet_digest(value)
    return value

def _redigest_review(review: dict, evidence: dict) -> dict:
    value = deepcopy(review)
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = compute_future_only_learning_review_certificate_digest(value)
    return value

def _redigest_context(
    source: dict,
    evidence: dict,
    review: dict,
    context: dict,
) -> dict:
    value = deepcopy(context)
    value["source_realized_dukkha_verification_receipt_digest"] = source[
        SOURCE_RECEIPT_DIGEST_FIELD
    ]
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_future_only_learning_operation_digest"] = (
        compute_requested_future_only_learning_operation_digest(
            source, evidence, review
        )
    )
    value["exact_future_only_learning_cycle_digest"] = (
        compute_exact_future_only_learning_cycle_digest(
            source, evidence, review, value
        )
    )
    value.pop(CONTEXT_DIGEST_FIELD, None)
    value[CONTEXT_DIGEST_FIELD] = compute_future_only_learning_intake_context_digest(value)
    return value


def _build(**overrides):
    source = deepcopy(
        overrides.pop("source_realized_dukkha_verification_receipt", None)
        or _source()
    )
    evidence = deepcopy(
        overrides.pop("future_only_learning_evidence_packet", None)
        or _evidence(source)
    )
    review = deepcopy(
        overrides.pop("future_only_learning_review_certificate", None)
        or _review(source, evidence)
    )
    context = deepcopy(
        overrides.pop("future_only_learning_intake_context", None)
        or _context(source, evidence, review)
    )

    source_digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "source-v010-missing")
    evidence_digest = evidence.get(EVIDENCE_DIGEST_FIELD, "learning-evidence-v04-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "learning-review-v04-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "learning-context-v04-missing")

    expected_source = overrides.pop(
        "expected_source_realized_dukkha_verification_receipt_digest",
        source_digest,
    )
    expected_evidence = overrides.pop(
        "expected_future_only_learning_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_future_only_learning_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_future_only_learning_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "future_only_learning_policy_digest",
        "learnos-dukkha-preserving-future-only-learning-policy-v04",
    )
    responsibility = overrides.pop(
        "future_only_learning_responsibility_digest",
        "learnos-future-only-learning-responsibility-v04",
    )
    request_id = overrides.pop(
        "future_only_learning_request_id",
        "learnos-future-only-learning-v04-001",
    )
    bundle = overrides.pop(
        "future_only_learning_bundle_digest",
        compute_future_only_learning_bundle_digest(
            source_realized_dukha_verification_receipt_digest=source_digest,
            expected_source_realized_dukkha_verification_receipt_digest=expected_source,
            future_only_learning_evidence_packet_digest=evidence_digest,
            expected_future_only_learning_evidence_packet_digest=expected_evidence,
            future_only_learning_review_certificate_digest=review_digest,
            expected_future_only_learning_review_certificate_digest=expected_review,
            future_only_learning_intake_context_digest=context_digest,
            expected_future_only_learning_intake_context_digest=expected_context,
            requested_future_only_learning_operation_digest=context.get(
                "requested_future_only_learning_operation_digest"
            ),
            exact_future_only_learning_cycle_digest=context.get(
                "exact_future_only_learning_cycle_digest"
            ),
            future_only_learning_policy_digest=policy,
            future_only_learning_responsibility_digest=responsibility,
            future_only_learning_request_id=request_id,
        ),
    )
    args = {
        "source_realized_dukkha_verification_receipt": source,
        "expected_source_realized_dukkha_verification_receipt_digest": expected_source,
        "future_only_learning_evidence_packet": evidence,
        "expected_future_only_learning_evidence_packet_digest": expected_evidence,
        "future_only_learning_review_certificate": review,
        "expected_future_only_learning_review_certificate_digest": expected_review,
        "future_only_learning_intake_context": context,
        "expected_future_only_learning_intake_context_digest": expected_context,
        "future_only_learning_policy_digest": policy,
        "future_only_learning_responsibility_digest": responsibility,
        "future_only_learning_request_id": request_id,
        "future_only_learning_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake(
        **args
    )


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["future_only_learning_disposition"] == disposition
    assert result.receipt["learnos_version"] == "v0.4"
    return result.receipt


def _review_route(field: str, value, disposition: str) -> None:
    source = _source()
    evidence = _evidence(source)
    review = _review(source, evidence)
    review[field] = value
    review = _redigest_review(review, evidence)
    context = _redigest_context(
        source, evidence, review, _context(source, evidence, review)
    )
    _assert_disposition(
        _build(
            source_realized_dukha_verification_receipt=source,
            future_only_learning_evidence_packet=evidence,
            future_only_learning_review_certificate=review,
            future_only_learning_intake_context=context,
        ),
        disposition,
    )


def main() -> int:
    supported = _assert_disposition(_build(), DISPOSITION_SUPPORTED)
    assert supported["future_only_learning_state_before"] == STATE_BEFORE
    assert supported["future_only_learning_state_after"] == STATE_AFTER_SUPPORTED
    assert supported["world_fact_confirmed"] is True
    assert supported["causal_attribution_confirmed"] is True
    assert supported["dukkha_reduction_realized_confirmed"] is True
    assert supported["future_only_learning_delta_recorded"] is True
    assert supported["future_only_learning_delta_activated"] is False
    assert supported["maintenance_monitoring_handoff_prepared"] is True
    assert supported["maintenance_monitoring_activated"] is False
    assert supported["persistent_world_state_changed_by_learning"] is False
    assert supported["world_model_revision_incremented_by_learning"] is False
    assert supported["current_plan_revised_by_learning"] is False
    assert supported["current_policy_activated_by_learning"] is False
    assert supported["tool_invocation_performed"] is False
    assert supported["external_side_effect_performed"] is False
    assert supported["future_only"] is True
    assert supported["active_now"] is False
    assert supported["future_only_learning_delta_binding"] is not None
    assert supported["maintenance_monitoring_handoff_envelope"] is not None
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in supported.items() if key != RECEIPT_DIGEST_FIELD}
    )

    blocked = _build(
        expected_source_realized_dukha_verification_receipt_digest="wrong"
    )
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert (
        "source_realized_dukkha_verification_expected_binding_mismatch"
        in blocked.blockers
    )

    source = _source()
    evidence = _evidence(source)
    review = _review(source, evidence)
    context = _context(source, evidence, review)

    world_context = deepcopy(context)
    world_context["current_world_model_state_digest"] = "stale-world"
    world_context = _redigest_context(source, evidence, review, world_context)
    _assert_disposition(
        _build(
            source_realized_dukkha_verification_receipt=source,
            future_only_learning_evidence_packet=evidence,
            future_only_learning_review_certificate=review,
            future_only_learning_intake_context=world_context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )

    delay_context = deepcopy(context)
    delay_context["future_only_learning_intake_epoch"] = (
        delay_context["source_realized_dukkha_verification_epoch"]
        + delay_context["maximum_future_only_learning_intake_delay"]
        + 1
    )
    delay_context = _redigest_context(source, evidence, review, delay_context)
    _assert_disposition(
        _build(
            source_realized_dukha_verification_receipt=source,
            future_only_learning_evidence_packet=evidence,
            future_only_learning_review_certificate=review,
            future_only_learning_intake_context=delay_context,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    replay_context = deepcopy(context)
    replay_context["prior_future_only_learning_intake_session_ids"] = [
        replay_context["future_only_learning_intake_session_id"]
    ]
    replay_context = _redigest_context(source, evidence, review, replay_context)
    _assert_disposition(
        _build(
            source_realized_dukkha_verification_receipt=source,
            future_only_learning_evidence_packet=evidence,
            future_only_learning_review_certificate=review,
            future_only_learning_intake_context=replay_context,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )

    stale_review = deepcopy(review)
    stale_review["review_completed_epoch"] = (
        stale_review["review_started_epoch"]
        + stale_review["maximum_review_duration"]
        + 1
    )
    stale_review = _redigest_review(stale_review, evidence)
    stale_review_context = _redigest_context(
        source, evidence, stale_review, _context(source, evidence, stale_review)
    )
    _assert_disposition(
        _build(
            source_realized_dukkha_verification_receipt=source,
            future_only_learning_evidence_packet=evidence,
            future_only_learning_review_certificate=stale_review,
            future_only_learning_intake_context=stale_review_context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    insufficient = deepcopy(evidence)
    insufficient["independent_future_only_learning_evidence"] = False
    insufficient = _redigest_evidence(insufficient)
    insufficient_review = _redigest_review(review, insufficient)
    insufficient_context = _redigest_context(
        source,
        insufficient,
        insufficient_review,
        _context(source, insufficient, insufficient_review)
    )
    _assert_disposition(
        _build(
            source_realized_dukha_verification_receipt=source,
            future_only_learning_evidence_packet=insufficient,
            future_only_learning_review_certificate=insufficient_review,
            future_only_learning_intake_context=insufficient_context,
        ),
        DISPOSITION_ADDITIONAL_EVIDENCE,
    )

    _review_route(
        "source_receipt_correspondence_confirmed", False, DISPOSITION_SOURCE_REPAIR
    )
    _review_route(
        "source_bounded_world_fact_confirmed", False, DISPOSITION_FACT_REPAIR
    )
    _review_route(
        "source_causal_attribution_confirmed", False, DISPOSITION_CAUSAL_REPAIR
    )
    _review_route(
        "source_realized_dukkha_confirmed", False, DISPOSITION_DUKKHA_REPAIR
    )
    _review_route(
        "maintenance_window_adequate",
        False,
        DISPOSITION_MAINTENANCE_WINDOW_REPAIR,
    )
    _review_route(
        "durability_monitoring_adequate", False, DISPOSITION_DURABILITY_REVIEW
    )
    _review_route(
        "adverse_effect_monitoring_adequate", False, DISPOSITION_ADVERSE_REVIEW
    )
    _review_route(
        "distributional_monitoring_adequate",
        False,
        DISPOSITION_DISTRIBUTIONAL_REVIEW,
    )
    _review_route("uncertainty_adequate", False, DISPOSITION_UNCERTAINTY_REPAIR)
    _review_route("calibration_adequate", False, DISPOSITION_CALIBRATION_REPAIR)
    _review_route(
        "provenance_continuity_preserved", False, DISPOSITION_PROVENANCE_REPAIR
    )
    _review_route(
        "protected_group_nonexternalization_supported",
        False,
        DISPOSITION_NONEXTERNALIZATION_REVIEW,
    )

    mutating = deepcopy(evidence)
    mutating["current_policy_activated"] = True
    mutating = _redigest_evidence(mutating)
    mutating_review = _redigest_review(review, mutating)
    mutating_context = _redigest_context(
        source,
        mutating,
        mutating_review,
        _context(source, mutating, mutating_review),
    )
    _assert_disposition(
        _build(
            source_realized_dukkha_verification_receipt=source,
            future_only_learning_evidence_packet=mutating,
            future_only_learning_review_certificate=mutating_review,
            future_only_learning_intake_context=mutating_context,
        ),
        DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    )

    escalating = deepcopy(evidence)
    escalating["authority_escalation_claimed"] = True
    escalating = _redigest_evidence(escalating)
    escalating_review = _redigest_review(review, escalating)
    escalating_context = _redigest_context(
        source,
        escalating,
        escalating_review,
        _context(source, escalating, escalating_review),
    )
    _assert_disposition(
        _build(
            source_realized_dukha_verification_receipt=source,
            future_only_learning_evidence_packet=escalating,
            future_only_learning_review_certificate=escalating_review,
            future_only_learning_intake_context=escalating_context,
        ),
        DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    )

    print(
        "PASS: LearnOS v0.4 future-only learning maintenance disposition "
        "actual-chain validation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
