#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ADDITIONAL_EVIDENCE,
    DISPOSITION_ADVERSE_OFFSET_REVIEW,
    DISPOSITION_BASELINE_REPAIR,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CAUSAL_BINDING_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_DISTRIBUTIONAL_REVIEW,
    DISPOSITION_DURABILITY_REVIEW,
    DISPOSITION_EFFECT_ESTIMATE_REPAIR,
    DISPOSITION_MEASUREMENT_REPAIR,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_OUTCOME_REPAIR,
    DISPOSITION_OVERCLAIM_REJECTED,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_SUPPORTED,
    DISPOSITION_TEMPORAL_REPAIR,
    DISPOSITION_UNCERTAINTY_REPAIR,
    DISPOSITION_WORLD_REFRESH,
    EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_CAUSAL_DIGEST_FIELD,
    SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD,
    SOURCE_CAUSAL_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake,
    canonical_digest,
    compute_exact_realized_dukkha_verification_cycle_digest,
    compute_realized_dukkha_verification_bundle_digest,
    compute_realized_dukkha_verification_evidence_packet_digest,
    compute_realized_dukkha_verification_intake_context_digest,
    compute_realized_dukkha_verification_review_certificate_digest,
    compute_requested_realized_dukkha_verification_operation_digest,
)
from scripts.check_verifyos_dukkha_preserving_world_causal_attribution_verification_intake_v0_1 import (
    _build as build_verifyos_v09,
)


def _source() -> dict:
    result = build_verifyos_v09()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    source = deepcopy(result.receipt)
    assert (
        source["world_causal_attribution_verification_disposition"]
        == "world_causal_attribution_verification_supported"
    )
    assert source["world_causal_attribution_verification_state_after"] == STATE_BEFORE
    assert source["bounded_world_fact_confirmed"] is True
    assert source["world_fact_confirmed"] is True
    assert source["causal_attribution_confirmed"] is True
    assert source["causal_attribution_scope_exactly_bounded"] is True
    assert source["dukkha_reduction_realized_confirmed"] is False
    assert source["dukkha_realization_verification_intake_admitted"] is True
    assert source["dukkha_realization_verification_receipt_required"] is True
    return source


def _evidence(source: dict) -> dict:
    causal = source["world_causal_attribution_evidence_packet"]
    evidence = {
        "source_world_causal_attribution_verification_receipt_digest": source[
            SOURCE_CAUSAL_DIGEST_FIELD
        ],
        "source_world_fact_confirmation_receipt_digest": source[
            "source_world_fact_confirmation_receipt_digest"
        ],
        "source_world_causal_attribution_evidence_packet_digest": source[
            SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD
        ],
        "source_world_causal_attribution_verification_review_certificate_digest": source[
            SOURCE_CAUSAL_REVIEW_DIGEST_FIELD
        ],
        "source_world_causal_attribution_verification_record_digest": source[
            "world_causal_attribution_verification_record_digest"
        ],
        "source_world_causal_attribution_verification_debt_consumption_record_digest": source[
            "world_causal_attribution_verification_debt_consumption_record_digest"
        ],
        "source_bounded_world_causal_attribution_binding_digest": source[
            "bounded_world_causal_attribution_binding_digest"
        ],
        "source_dukkha_realization_verification_handoff_envelope_digest": source[
            "dukkha_realization_verification_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": source["world_candidate_fact_digest"],
        "world_candidate_relation_digest": source["world_candidate_relation_digest"],
        "resulting_world_state_digest": source["source_world_model_state_digest"],
        "resulting_world_revision": source["source_world_model_revision"],
        "persistent_world_storage_target_digest": source[
            "source_persistent_world_storage_target_digest"
        ],
        "expected_world_update_postcondition_digest": causal[
            "expected_world_update_postcondition_digest"
        ],
        "causal_model_digest": causal["causal_model_digest"],
        "causal_query_digest": causal["causal_query_digest"],
        "intervention_digest": causal["intervention_digest"],
        "counterfactual_estimand_digest": causal["counterfactual_estimand_digest"],
        "realized_dukkha_observation_digest": causal[
            "realized_dukkha_observation_digest"
        ],
        "baseline_dukkha_assessment_digest": "verifyos-dukkha-baseline-v010-001",
        "post_intervention_dukkha_assessment_digest": (
            "verifyos-dukkha-post-intervention-v010-001"
        ),
        "dukkha_outcome_measure_specification_digest": (
            "verifyos-dukkha-outcome-measure-v010-001"
        ),
        "dukkha_assessment_window_digest": "verifyos-dukkha-window-v010-001",
        "minimum_clinically_meaningful_reduction_digest": (
            "verifyos-dukkha-mcmr-v010-001"
        ),
        "realized_dukkha_effect_estimate_digest": (
            "verifyos-dukkha-effect-estimate-v010-001"
        ),
        "realized_dukkha_effect_direction_digest": (
            "verifyos-dukkha-effect-direction-reduction-v010-001"
        ),
        "realized_dukkha_effect_magnitude_digest": (
            "verifyos-dukkha-effect-magnitude-v010-001"
        ),
        "realized_dukkha_confidence_interval_digest": (
            "verifyos-dukkha-confidence-interval-v010-001"
        ),
        "durability_evidence_digest": "verifyos-dukkha-durability-v010-001",
        "adverse_effect_offset_assessment_digest": (
            "verifyos-dukkha-adverse-offset-v010-001"
        ),
        "distributional_impact_assessment_digest": (
            "verifyos-dukkha-distributional-impact-v010-001"
        ),
        "protected_group_realized_dukkha_impact_digest": (
            "verifyos-dukkha-protected-group-impact-v010-001"
        ),
        "future_subject_realized_dukkha_impact_digest": (
            "verifyos-dukkha-future-subject-impact-v010-001"
        ),
        "uncertainty_digest": "verifyos-dukkha-uncertainty-v010-001",
        "calibration_digest": "verifyos-dukkha-calibration-v010-001",
        "provenance_chain_digests": sorted(
            {
                source[SOURCE_CAUSAL_DIGEST_FIELD],
                source["bounded_world_causal_attribution_binding_digest"],
                source["dukkha_realization_verification_handoff_envelope_digest"],
                "verifyos-dukkha-provenance-v010-001",
            }
        ),
        "tamper_evidence_digest": "verifyos-dukkha-tamper-evidence-v010-001",
        "evidence_collector_id": "verifyos-dukkha-evidence-collector-v010",
        "evidence_source_id": "independent-dukkha-outcome-source-v010",
        "collection_started_epoch": 138,
        "collection_completed_epoch": 139,
        "maximum_collection_duration": 4,
        "independent_realized_dukkha_evidence": True,
        "exactly_one_realized_dukkha_evidence_collection": True,
        "world_mutation_performed_by_evidence_collector": False,
        "causal_attribution_reopened": False,
        "realized_dukkha_reduction_preconfirmed": False,
        "generalized_benefit_claimed": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = (
        compute_realized_dukkha_verification_evidence_packet_digest(evidence)
    )
    return evidence


def _review(source: dict, evidence: dict) -> dict:
    review = {
        "source_world_causal_attribution_verification_receipt_digest": source[
            SOURCE_CAUSAL_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        "source_bounded_world_causal_attribution_binding_digest": source[
            "bounded_world_causal_attribution_binding_digest"
        ],
        "source_dukkha_realization_verification_handoff_envelope_digest": source[
            "dukkha_realization_verification_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "causal_model_digest": evidence["causal_model_digest"],
        "causal_query_digest": evidence["causal_query_digest"],
        "intervention_digest": evidence["intervention_digest"],
        "counterfactual_estimand_digest": evidence["counterfactual_estimand_digest"],
        "realized_dukkha_observation_digest": evidence[
            "realized_dukkha_observation_digest"
        ],
        "baseline_dukkha_assessment_digest": evidence[
            "baseline_dukkha_assessment_digest"
        ],
        "post_intervention_dukkha_assessment_digest": evidence[
            "post_intervention_dukkha_assessment_digest"
        ],
        "dukkha_outcome_measure_specification_digest": evidence[
            "dukkha_outcome_measure_specification_digest"
        ],
        "dukkha_assessment_window_digest": evidence[
            "dukkha_assessment_window_digest"
        ],
        "minimum_clinically_meaningful_reduction_digest": evidence[
            "minimum_clinically_meaningful_reduction_digest"
        ],
        "realized_dukkha_effect_estimate_digest": evidence[
            "realized_dukkha_effect_estimate_digest"
        ],
        "reviewer_id": "verifyos-realized-dukkha-reviewer-v010",
        "verification_method_digest": "verifyos-realized-dukkha-method-v010-001",
        "verification_evidence_digest": (
            "verifyos-realized-dukkha-review-evidence-v010-001"
        ),
        "verification_review_started_epoch": 139,
        "verification_review_completed_epoch": 140,
        "maximum_verification_review_duration": 4,
        "source_bounded_world_fact_confirmed": True,
        "source_causal_attribution_confirmed": True,
        "causal_binding_correspondence_confirmed": True,
        "baseline_correspondence_confirmed": True,
        "post_intervention_outcome_correspondence_confirmed": True,
        "measurement_validity_adequate": True,
        "assessment_window_adequate": True,
        "clinically_meaningful_reduction_supported": True,
        "effect_direction_supports_reduction": True,
        "effect_magnitude_adequate": True,
        "durability_adequate": True,
        "adverse_effect_offset_acceptable": True,
        "distributional_impact_acceptable": True,
        "uncertainty_adequate": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "exact_bounded_scope_preserved": True,
        "causal_attribution_reopened": False,
        "realized_dukkha_reduction_preconfirmed": False,
        "generalized_benefit_claimed": False,
    }
    review[REVIEW_DIGEST_FIELD] = (
        compute_realized_dukkha_verification_review_certificate_digest(review)
    )
    return review


def _context(source: dict, evidence: dict, review: dict) -> dict:
    source_epoch = source["world_causal_attribution_verification_record"][
        "world_causal_attribution_verification_intake_epoch"
    ]
    context = {
        "source_world_causal_attribution_verification_receipt_digest": source[
            SOURCE_CAUSAL_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source["source_world_model_state_digest"],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_persistent_world_storage_target_digest": source[
            "source_persistent_world_storage_target_digest"
        ],
        "current_world_lineage_digest": canonical_digest(
            source["resulting_lineage_digests"]
        ),
        "source_world_causal_attribution_verification_epoch": source_epoch,
        "realized_dukkha_verification_intake_epoch": source_epoch + 3,
        "maximum_realized_dukkha_verification_intake_delay": 8,
        "realized_dukkha_verification_intake_session_id": (
            "verifyos-realized-dukkha-intake-v010-001"
        ),
        "realized_dukkha_verification_intake_nonce_digest": (
            "verifyos-realized-dukkha-nonce-v010-001"
        ),
        "prior_realized_dukkha_verification_intake_session_ids": [],
        "prior_realized_dukkha_evidence_packet_digests": [],
        "prior_realized_dukkha_verification_review_certificate_digests": [],
        "prior_realized_dukkha_verification_intake_nonce_digests": [],
        "prior_realized_dukkha_confirmed_causal_verification_receipt_digests": [],
        "requested_realized_dukkha_verification_operation_digest": (
            compute_requested_realized_dukkha_verification_operation_digest(
                source, evidence, review
            )
        ),
        "exact_realized_dukkha_verification_cycle_digest": "",
    }
    context["exact_realized_dukkha_verification_cycle_digest"] = (
        compute_exact_realized_dukkha_verification_cycle_digest(
            source, evidence, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = (
        compute_realized_dukkha_verification_intake_context_digest(context)
    )
    return context


def _redigest_evidence(evidence: dict) -> dict:
    value = deepcopy(evidence)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_realized_dukkha_verification_evidence_packet_digest(value)
    )
    return value


def _redigest_review(review: dict, evidence: dict) -> dict:
    value = deepcopy(review)
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_realized_dukkha_verification_review_certificate_digest(value)
    )
    return value


def _redigest_context(
    source: dict, evidence: dict, review: dict, context: dict
) -> dict:
    value = deepcopy(context)
    value["source_world_causal_attribution_verification_receipt_digest"] = source[
        SOURCE_CAUSAL_DIGEST_FIELD
    ]
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_realized_dukkha_verification_operation_digest"] = (
        compute_requested_realized_dukkha_verification_operation_digest(
            source, evidence, review
        )
    )
    value["exact_realized_dukkha_verification_cycle_digest"] = (
        compute_exact_realized_dukkha_verification_cycle_digest(
            source, evidence, review, value
        )
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_realized_dukkha_verification_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    source = deepcopy(
        overrides.pop("source_world_causal_attribution_verification_receipt", None)
        or _source()
    )
    evidence = deepcopy(
        overrides.pop("realized_dukkha_verification_evidence_packet", None)
        or _evidence(source)
    )
    review = deepcopy(
        overrides.pop("realized_dukkha_verification_review_certificate", None)
        or _review(source, evidence)
    )
    context = deepcopy(
        overrides.pop("realized_dukkha_verification_intake_context", None)
        or _context(source, evidence, review)
    )

    source_digest = source.get(SOURCE_CAUSAL_DIGEST_FIELD, "causal-v09-missing")
    evidence_digest = evidence.get(EVIDENCE_DIGEST_FIELD, "dukkha-evidence-v010-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "dukkha-review-v010-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "dukkha-context-v010-missing")

    expected_source = overrides.pop(
        "expected_source_world_causal_attribution_verification_receipt_digest",
        source_digest,
    )
    expected_evidence = overrides.pop(
        "expected_realized_dukkha_verification_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_realized_dukkha_verification_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_realized_dukkha_verification_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "realized_dukkha_verification_policy_digest",
        "verifyos-dukkha-preserving-realized-dukkha-policy-v010",
    )
    responsibility = overrides.pop(
        "realized_dukkha_verification_responsibility_digest",
        "verifyos-realized-dukkha-responsibility-v010",
    )
    request_id = overrides.pop(
        "realized_dukkha_verification_request_id",
        "verifyos-realized-dukkha-verification-v010-001",
    )
    bundle = overrides.pop(
        "realized_dukkha_verification_bundle_digest",
        compute_realized_dukkha_verification_bundle_digest(
            source_world_causal_attribution_verification_receipt_digest=source_digest,
            expected_source_world_causal_attribution_verification_receipt_digest=(
                expected_source
            ),
            source_world_fact_confirmation_receipt_digest=source.get(
                "source_world_fact_confirmation_receipt_digest"
            ),
            source_world_causal_attribution_evidence_packet_digest=source.get(
                SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD
            ),
            source_world_causal_attribution_verification_review_certificate_digest=source.get(
                SOURCE_CAUSAL_REVIEW_DIGEST_FIELD
            ),
            source_world_causal_attribution_verification_record_digest=source.get(
                "world_causal_attribution_verification_record_digest"
            ),
            source_world_causal_attribution_verification_debt_consumption_record_digest=source.get(
                "world_causal_attribution_verification_debt_consumption_record_digest"
            ),
            source_bounded_world_causal_attribution_binding_digest=source.get(
                "bounded_world_causal_attribution_binding_digest"
            ),
            source_dukkha_realization_verification_handoff_envelope_digest=source.get(
                "dukkha_realization_verification_handoff_envelope_digest"
            ),
            realized_dukkha_verification_evidence_packet_digest=evidence_digest,
            expected_realized_dukkha_verification_evidence_packet_digest=(
                expected_evidence
            ),
            realized_dukkha_verification_review_certificate_digest=review_digest,
            expected_realized_dukkha_verification_review_certificate_digest=(
                expected_review
            ),
            realized_dukkha_verification_intake_context_digest=context_digest,
            expected_realized_dukkha_verification_intake_context_digest=(
                expected_context
            ),
            requested_realized_dukkha_verification_operation_digest=context.get(
                "requested_realized_dukkha_verification_operation_digest"
            ),
            exact_realized_dukkha_verification_cycle_digest=context.get(
                "exact_realized_dukkha_verification_cycle_digest"
            ),
            realized_dukkha_verification_policy_digest=policy,
            realized_dukkha_verification_responsibility_digest=responsibility,
            realized_dukkha_verification_request_id=request_id,
        ),
    )

    args = {
        "source_world_causal_attribution_verification_receipt": source,
        "expected_source_world_causal_attribution_verification_receipt_digest": expected_source,
        "realized_dukkha_verification_evidence_packet": evidence,
        "expected_realized_dukkha_verification_evidence_packet_digest": expected_evidence,
        "realized_dukkha_verification_review_certificate": review,
        "expected_realized_dukkha_verification_review_certificate_digest": expected_review,
        "realized_dukkha_verification_intake_context": context,
        "expected_realized_dukkha_verification_intake_context_digest": expected_context,
        "realized_dukkha_verification_policy_digest": policy,
        "realized_dukkha_verification_responsibility_digest": responsibility,
        "realized_dukkha_verification_request_id": request_id,
        "realized_dukkha_verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake(
        **args
    )


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["realized_dukkha_verification_disposition"] == disposition
    assert result.receipt["verifyos_version"] == "v0.10"
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
            source_world_causal_attribution_verification_receipt=source,
            realized_dukkha_verification_evidence_packet=evidence,
            realized_dukkha_verification_review_certificate=review,
            realized_dukkha_verification_intake_context=context,
        ),
        disposition,
    )


def main() -> int:
    supported = _assert_disposition(_build(), DISPOSITION_SUPPORTED)
    assert supported["realized_dukkha_verification_state_before"] == STATE_BEFORE
    assert supported["realized_dukkha_verification_state_after"] == STATE_AFTER_SUPPORTED
    assert supported["bounded_world_fact_confirmed"] is True
    assert supported["world_fact_confirmed"] is True
    assert supported["causal_attribution_confirmed"] is True
    assert supported["causal_attribution_scope_exactly_bounded"] is True
    assert supported["dukkha_reduction_realized_confirmed"] is True
    assert supported["dukkha_reduction_realized_scope_exactly_bounded"] is True
    assert supported["realized_dukkha_verification_debt_consumed"] is True
    assert supported["realized_dukkha_verification_debt_open"] is False
    assert supported["persistent_world_state_changed_by_dukkha_verification"] is False
    assert supported["world_model_revision_incremented_by_dukkha_verification"] is False
    assert supported["world_mutation_reperformed"] is False
    assert supported["tool_invocation_performed"] is False
    assert supported["external_side_effect_performed"] is False
    assert supported["automatic_plan_completion"] is False
    assert supported["bounded_realized_dukkha_confirmation_binding"] is not None
    assert supported["future_learning_handoff_envelope"] is not None
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in supported.items() if key != RECEIPT_DIGEST_FIELD}
    )

    blocked = _build(
        expected_source_world_causal_attribution_verification_receipt_digest="wrong"
    )
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert (
        "source_world_causal_attribution_verification_expected_binding_mismatch"
        in blocked.blockers
    )

    source = _source()
    evidence = _evidence(source)
    review = _review(source, evidence)
    context = _context(source, evidence, review)

    world_context = deepcopy(context)
    world_context["current_world_model_state_digest"] = "stale-world-state"
    world_context = _redigest_context(source, evidence, review, world_context)
    _assert_disposition(
        _build(realized_dukkha_verification_intake_context=world_context),
        DISPOSITION_WORLD_REFRESH,
    )

    stale_context = deepcopy(context)
    stale_context["realized_dukkha_verification_intake_epoch"] = (
        stale_context["source_world_causal_attribution_verification_epoch"]
        + stale_context["maximum_realized_dukkha_verification_intake_delay"]
        + 1
    )
    stale_context = _redigest_context(source, evidence, review, stale_context)
    _assert_disposition(
        _build(realized_dukkha_verification_intake_context=stale_context),
        DISPOSITION_CONTEXT_REFRESH,
    )

    stale_review = deepcopy(review)
    stale_review["verification_review_completed_epoch"] = (
        stale_review["verification_review_started_epoch"]
        + stale_review["maximum_verification_review_duration"]
        + 1
    )
    stale_review = _redigest_review(stale_review, evidence)
    stale_review_context = _redigest_context(
        source, evidence, stale_review, _context(source, evidence, stale_review)
    )
    _assert_disposition(
        _build(
            realized_dukkha_verification_review_certificate=stale_review,
            realized_dukkha_verification_intake_context=stale_review_context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    non_independent = deepcopy(evidence)
    non_independent["independent_realized_dukkha_evidence"] = False
    non_independent = _redigest_evidence(non_independent)
    non_independent_review = _redigest_review(review, non_independent)
    non_independent_context = _redigest_context(
        source,
        non_independent,
        non_independent_review,
        _context(source, non_independent, non_independent_review),
    )
    _assert_disposition(
        _build(
            realized_dukkha_verification_evidence_packet=non_independent,
            realized_dukkha_verification_review_certificate=non_independent_review,
            realized_dukkha_verification_intake_context=non_independent_context,
        ),
        DISPOSITION_ADDITIONAL_EVIDENCE,
    )

    replay_context = deepcopy(context)
    replay_context[
        "prior_realized_dukkha_confirmed_causal_verification_receipt_digests"
    ] = [source[SOURCE_CAUSAL_DIGEST_FIELD]]
    replay_context = _redigest_context(source, evidence, review, replay_context)
    _assert_disposition(
        _build(realized_dukkha_verification_intake_context=replay_context),
        DISPOSITION_REPLAY_REJECTED,
    )

    _review_route(
        "causal_binding_correspondence_confirmed",
        False,
        DISPOSITION_CAUSAL_BINDING_REPAIR,
    )
    _review_route("baseline_correspondence_confirmed", False, DISPOSITION_BASELINE_REPAIR)
    _review_route(
        "post_intervention_outcome_correspondence_confirmed",
        False,
        DISPOSITION_OUTCOME_REPAIR,
    )
    _review_route("measurement_validity_adequate", False, DISPOSITION_MEASUREMENT_REPAIR)
    _review_route("assessment_window_adequate", False, DISPOSITION_TEMPORAL_REPAIR)
    _review_route(
        "clinically_meaningful_reduction_supported",
        False,
        DISPOSITION_EFFECT_ESTIMATE_REPAIR,
    )
    _review_route("durability_adequate", False, DISPOSITION_DURABILITY_REVIEW)
    _review_route(
        "adverse_effect_offset_acceptable",
        False,
        DISPOSITION_ADVERSE_OFFSET_REVIEW,
    )
    _review_route(
        "distributional_impact_acceptable",
        False,
        DISPOSITION_DISTRIBUTIONAL_REVIEW,
    )
    _review_route("uncertainty_adequate", False, DISPOSITION_UNCERTAINTY_REPAIR)
    _review_route("calibration_adequate", False, DISPOSITION_CALIBRATION_REPAIR)
    _review_route(
        "provenance_continuity_preserved",
        False,
        DISPOSITION_PROVENANCE_REPAIR,
    )
    _review_route(
        "protected_group_nonexternalization_supported",
        False,
        DISPOSITION_NONEXTERNALIZATION_REVIEW,
    )
    _review_route("generalized_benefit_claimed", True, DISPOSITION_OVERCLAIM_REJECTED)

    unsupported = _review(source, evidence)
    unsupported["durability_adequate"] = False
    unsupported = _redigest_review(unsupported, evidence)
    unsupported_context = _redigest_context(
        source, evidence, unsupported, _context(source, evidence, unsupported)
    )
    routed = _assert_disposition(
        _build(
            realized_dukkha_verification_review_certificate=unsupported,
            realized_dukkha_verification_intake_context=unsupported_context,
        ),
        DISPOSITION_DURABILITY_REVIEW,
    )
    assert routed["realized_dukkha_verification_state_after"] == STATE_BEFORE
    assert routed["world_fact_confirmed"] is True
    assert routed["causal_attribution_confirmed"] is True
    assert routed["dukkha_reduction_realized_confirmed"] is False
    assert routed["realized_dukkha_verification_debt_open"] is True
    assert routed[
        "source_world_causal_attribution_verification_receipt_replay_closed"
    ] is False

    print(
        "PASS: VerifyOS v0.10 realized-dukkha verification disposition intake "
        "validated through the actual WORLD v0.62 / VerifyOS v0.8 / WORLD v0.63 / "
        "VerifyOS v0.9 receipt chain"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
