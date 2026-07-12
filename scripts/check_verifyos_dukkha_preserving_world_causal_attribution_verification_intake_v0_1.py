#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_world_causal_attribution_verification_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ADDITIONAL_EVIDENCE,
    DISPOSITION_ALTERNATIVE_CAUSE_REVIEW,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CAUSAL_MODEL_REPAIR,
    DISPOSITION_CONFOUNDING_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_COUNTERFACTUAL_REPAIR,
    DISPOSITION_DUKKHA_OVERCLAIM_REJECTED,
    DISPOSITION_INTERVENTION_REPAIR,
    DISPOSITION_MEASUREMENT_REPAIR,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_SELECTION_BIAS_REVIEW,
    DISPOSITION_SUPPORTED,
    DISPOSITION_TEMPORAL_REPAIR,
    DISPOSITION_TRUTH_GENERALIZATION_REJECTED,
    DISPOSITION_UNCERTAINTY_REPAIR,
    DISPOSITION_WORLD_REFRESH,
    EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_FACT_DIGEST_FIELD,
    SOURCE_MUTATION_DIGEST_FIELD,
    SOURCE_VERIFICATION_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_verifyos_dukkha_preserving_world_causal_attribution_verification_intake,
    canonical_digest,
    compute_exact_world_causal_attribution_verification_cycle_digest,
    compute_requested_world_causal_attribution_verification_operation_digest,
    compute_world_causal_attribution_evidence_packet_digest,
    compute_world_causal_attribution_verification_bundle_digest,
    compute_world_causal_attribution_verification_intake_context_digest,
    compute_world_causal_attribution_verification_review_certificate_digest,
)
from scripts.check_world_dukkha_preserving_world_fact_confirmation_disposition_intake_v0_1 import (
    _build as build_world_v063,
    _sources as build_v063_sources,
)


def _sources() -> tuple[dict, dict, dict]:
    fact_result = build_world_v063()
    assert fact_result.status == STATUS_READY, fact_result.blockers
    assert fact_result.receipt is not None
    fact = deepcopy(fact_result.receipt)
    verification, mutation = build_v063_sources()
    verification = deepcopy(verification)
    mutation = deepcopy(mutation)
    assert fact["world_fact_confirmation_disposition"] == "world_fact_confirmation_supported"
    assert fact["world_fact_confirmation_state_after"] == STATE_BEFORE
    assert fact["bounded_world_fact_confirmed"] is True
    assert fact["world_fact_confirmed"] is True
    assert fact["causal_attribution_confirmed"] is False
    assert fact["dukkha_reduction_realized_confirmed"] is False
    assert (
        fact["source_world_postcondition_verification_receipt_digest"]
        == verification[SOURCE_VERIFICATION_DIGEST_FIELD]
    )
    assert (
        fact["source_world_mutation_application_receipt_digest"]
        == mutation[SOURCE_MUTATION_DIGEST_FIELD]
    )
    return fact, verification, mutation


def _evidence(fact: dict, verification: dict, mutation: dict) -> dict:
    evidence = {
        "source_world_fact_confirmation_receipt_digest": fact[
            SOURCE_FACT_DIGEST_FIELD
        ],
        "source_world_postcondition_verification_receipt_digest": verification[
            SOURCE_VERIFICATION_DIGEST_FIELD
        ],
        "source_world_mutation_application_receipt_digest": mutation[
            SOURCE_MUTATION_DIGEST_FIELD
        ],
        "source_world_fact_confirmation_review_certificate_digest": fact[
            "world_fact_confirmation_review_certificate_digest"
        ],
        "source_world_fact_confirmation_record_digest": fact[
            "world_fact_confirmation_record_digest"
        ],
        "source_world_fact_confirmation_debt_consumption_record_digest": fact[
            "world_fact_confirmation_debt_consumption_record_digest"
        ],
        "source_bounded_world_fact_status_binding_digest": fact[
            "bounded_world_fact_status_binding_digest"
        ],
        "source_causal_attribution_verification_handoff_envelope_digest": fact[
            "causal_attribution_verification_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": fact["world_candidate_fact_digest"],
        "world_candidate_relation_digest": fact["world_candidate_relation_digest"],
        "resulting_world_state_digest": fact["source_world_model_state_digest"],
        "resulting_world_revision": fact["source_world_model_revision"],
        "persistent_world_storage_target_digest": fact[
            "source_persistent_world_storage_target_digest"
        ],
        "expected_world_update_postcondition_digest": fact[
            "expected_world_update_postcondition_digest"
        ],
        "causal_model_digest": "verifyos-world-causal-model-v09-001",
        "causal_query_digest": "verifyos-world-causal-query-v09-001",
        "intervention_digest": "verifyos-world-intervention-v09-001",
        "exposure_digest": "verifyos-world-exposure-v09-001",
        "outcome_digest": "verifyos-world-outcome-v09-001",
        "counterfactual_estimand_digest": "verifyos-world-counterfactual-estimand-v09-001",
        "identification_assumption_digests": sorted(
            {
                "causal-consistency-v09-001",
                "causal-positivity-v09-001",
                "causal-exchangeability-v09-001",
            }
        ),
        "confounder_set_digests": sorted(
            {
                "causal-preexisting-world-context-v09-001",
                "causal-observation-window-v09-001",
            }
        ),
        "adjustment_strategy_digest": "verifyos-world-adjustment-strategy-v09-001",
        "temporal_ordering_evidence_digest": "verifyos-world-temporal-ordering-v09-001",
        "intervention_correspondence_evidence_digest": (
            "verifyos-world-intervention-correspondence-v09-001"
        ),
        "counterfactual_support_evidence_digest": (
            "verifyos-world-counterfactual-support-v09-001"
        ),
        "alternative_cause_assessment_digest": (
            "verifyos-world-alternative-cause-assessment-v09-001"
        ),
        "selection_bias_assessment_digest": (
            "verifyos-world-selection-bias-assessment-v09-001"
        ),
        "measurement_validity_assessment_digest": (
            "verifyos-world-measurement-validity-v09-001"
        ),
        "uncertainty_digest": "verifyos-world-causal-uncertainty-v09-001",
        "calibration_digest": "verifyos-world-causal-calibration-v09-001",
        "provenance_chain_digests": sorted(
            {
                fact[SOURCE_FACT_DIGEST_FIELD],
                fact["bounded_world_fact_status_binding_digest"],
                fact["causal_attribution_verification_handoff_envelope_digest"],
                "verifyos-world-causal-provenance-v09-001",
            }
        ),
        "tamper_evidence_digest": "verifyos-world-causal-tamper-evidence-v09-001",
        "protected_group_causal_impact_digest": (
            "verifyos-world-protected-group-causal-impact-v09-001"
        ),
        "future_subject_causal_impact_digest": (
            "verifyos-world-future-subject-causal-impact-v09-001"
        ),
        "realized_dukkha_observation_digest": fact[
            "realized_dukkha_observation_digest"
        ],
        "evidence_collector_id": "verifyos-world-causal-evidence-collector-v09",
        "evidence_source_id": "independent-world-causal-evidence-source-v09",
        "collection_started_epoch": 134,
        "collection_completed_epoch": 135,
        "maximum_collection_duration": 4,
        "independent_causal_evidence": True,
        "exactly_one_causal_evidence_collection": True,
        "world_mutation_performed_by_causal_evidence_collector": False,
        "generalized_truth_claimed": False,
        "causal_attribution_preconfirmed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = (
        compute_world_causal_attribution_evidence_packet_digest(evidence)
    )
    return evidence


def _review(
    fact: dict,
    verification: dict,
    mutation: dict,
    evidence: dict,
) -> dict:
    review = {
        "source_world_fact_confirmation_receipt_digest": fact[
            SOURCE_FACT_DIGEST_FIELD
        ],
        "source_world_postcondition_verification_receipt_digest": verification[
            SOURCE_VERIFICATION_DIGEST_FIELD
        ],
        "source_world_mutation_application_receipt_digest": mutation[
            SOURCE_MUTATION_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        "source_bounded_world_fact_status_binding_digest": fact[
            "bounded_world_fact_status_binding_digest"
        ],
        "source_causal_attribution_verification_handoff_envelope_digest": fact[
            "causal_attribution_verification_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence[
            "world_candidate_relation_digest"
        ],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "persistent_world_storage_target_digest": evidence[
            "persistent_world_storage_target_digest"
        ],
        "expected_world_update_postcondition_digest": evidence[
            "expected_world_update_postcondition_digest"
        ],
        "causal_model_digest": evidence["causal_model_digest"],
        "causal_query_digest": evidence["causal_query_digest"],
        "intervention_digest": evidence["intervention_digest"],
        "exposure_digest": evidence["exposure_digest"],
        "outcome_digest": evidence["outcome_digest"],
        "counterfactual_estimand_digest": evidence[
            "counterfactual_estimand_digest"
        ],
        "reviewer_id": "verifyos-world-causal-attribution-reviewer-v09",
        "verification_method_digest": "verifyos-world-causal-method-v09-001",
        "verification_evidence_digest": "verifyos-world-causal-review-evidence-v09-001",
        "verification_review_started_epoch": 135,
        "verification_review_completed_epoch": 136,
        "maximum_verification_review_duration": 4,
        "source_bounded_world_fact_confirmed": True,
        "causal_model_adequate": True,
        "causal_query_exactly_bounded": True,
        "intervention_correspondence_confirmed": True,
        "temporal_ordering_confirmed": True,
        "confounding_control_adequate": True,
        "counterfactual_support_adequate": True,
        "alternative_causes_assessed": True,
        "selection_bias_adequate": True,
        "measurement_validity_adequate": True,
        "uncertainty_adequate": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "no_truth_generalization": True,
        "no_dukkha_realization_overclaim": True,
        "generalized_truth_claimed": False,
        "causal_attribution_preconfirmed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    review[REVIEW_DIGEST_FIELD] = (
        compute_world_causal_attribution_verification_review_certificate_digest(
            review
        )
    )
    return review


def _context(
    fact: dict,
    verification: dict,
    mutation: dict,
    evidence: dict,
    review: dict,
) -> dict:
    source_epoch = fact["world_fact_confirmation_record"][
        "world_fact_confirmation_intake_epoch"
    ]
    context = {
        "source_world_fact_confirmation_receipt_digest": fact[
            SOURCE_FACT_DIGEST_FIELD
        ],
        "source_world_postcondition_verification_receipt_digest": verification[
            SOURCE_VERIFICATION_DIGEST_FIELD
        ],
        "source_world_mutation_application_receipt_digest": mutation[
            SOURCE_MUTATION_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": fact["source_world_binding_digest"],
        "current_world_model_state_digest": fact["source_world_model_state_digest"],
        "current_world_model_revision": fact["source_world_model_revision"],
        "current_persistent_world_storage_target_digest": fact[
            "source_persistent_world_storage_target_digest"
        ],
        "current_world_lineage_digest": canonical_digest(
            fact["resulting_lineage_digests"]
        ),
        "source_world_fact_confirmation_epoch": source_epoch,
        "world_causal_attribution_verification_intake_epoch": source_epoch + 3,
        "maximum_world_causal_attribution_verification_intake_delay": 8,
        "world_causal_attribution_verification_intake_session_id": (
            "verifyos-world-causal-attribution-intake-v09-001"
        ),
        "world_causal_attribution_verification_intake_nonce_digest": (
            "verifyos-world-causal-attribution-nonce-v09-001"
        ),
        "prior_world_causal_attribution_verification_intake_session_ids": [],
        "prior_world_causal_attribution_evidence_packet_digests": [],
        "prior_world_causal_attribution_verification_review_certificate_digests": [],
        "prior_world_causal_attribution_verification_intake_nonce_digests": [],
        "prior_causally_verified_world_fact_confirmation_receipt_digests": [],
        "requested_world_causal_attribution_verification_operation_digest": (
            compute_requested_world_causal_attribution_verification_operation_digest(
                fact, evidence, review
            )
        ),
        "exact_world_causal_attribution_verification_cycle_digest": "",
    }
    context["exact_world_causal_attribution_verification_cycle_digest"] = (
        compute_exact_world_causal_attribution_verification_cycle_digest(
            fact, evidence, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = (
        compute_world_causal_attribution_verification_intake_context_digest(context)
    )
    return context


def _redigest_evidence(evidence: dict) -> dict:
    value = deepcopy(evidence)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_world_causal_attribution_evidence_packet_digest(value)
    )
    return value


def _redigest_review(review: dict, evidence: dict) -> dict:
    value = deepcopy(review)
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_world_causal_attribution_verification_review_certificate_digest(
            value
        )
    )
    return value


def _redigest_context(
    fact: dict,
    verification: dict,
    mutation: dict,
    evidence: dict,
    review: dict,
    context: dict,
) -> dict:
    value = deepcopy(context)
    value["source_world_fact_confirmation_receipt_digest"] = fact[
        SOURCE_FACT_DIGEST_FIELD
    ]
    value["source_world_postcondition_verification_receipt_digest"] = verification[
        SOURCE_VERIFICATION_DIGEST_FIELD
    ]
    value["source_world_mutation_application_receipt_digest"] = mutation[
        SOURCE_MUTATION_DIGEST_FIELD
    ]
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_causal_attribution_verification_operation_digest"] = (
        compute_requested_world_causal_attribution_verification_operation_digest(
            fact, evidence, review
        )
    )
    value["exact_world_causal_attribution_verification_cycle_digest"] = (
        compute_exact_world_causal_attribution_verification_cycle_digest(
            fact, evidence, review, value
        )
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_world_causal_attribution_verification_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    default_fact, default_verification, default_mutation = _sources()
    fact = deepcopy(
        overrides.pop("source_world_fact_confirmation_receipt", None)
        or default_fact
    )
    verification = deepcopy(
        overrides.pop("source_world_postcondition_verification_receipt", None)
        or default_verification
    )
    mutation = deepcopy(
        overrides.pop("source_world_mutation_application_receipt", None)
        or default_mutation
    )
    evidence = deepcopy(
        overrides.pop("world_causal_attribution_evidence_packet", None)
        or _evidence(fact, verification, mutation)
    )
    review = deepcopy(
        overrides.pop(
            "world_causal_attribution_verification_review_certificate", None
        )
        or _review(fact, verification, mutation, evidence)
    )
    context = deepcopy(
        overrides.pop(
            "world_causal_attribution_verification_intake_context", None
        )
        or _context(fact, verification, mutation, evidence, review)
    )

    fact_digest = fact.get(SOURCE_FACT_DIGEST_FIELD, "fact-v063-missing")
    verification_digest = verification.get(
        SOURCE_VERIFICATION_DIGEST_FIELD, "verification-v08-missing"
    )
    mutation_digest = mutation.get(
        SOURCE_MUTATION_DIGEST_FIELD, "mutation-v062-missing"
    )
    evidence_digest = evidence.get(EVIDENCE_DIGEST_FIELD, "causal-evidence-v09-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "causal-review-v09-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "causal-context-v09-missing")

    expected_fact = overrides.pop(
        "expected_source_world_fact_confirmation_receipt_digest", fact_digest
    )
    expected_verification = overrides.pop(
        "expected_source_world_postcondition_verification_receipt_digest",
        verification_digest,
    )
    expected_mutation = overrides.pop(
        "expected_source_world_mutation_application_receipt_digest",
        mutation_digest,
    )
    expected_evidence = overrides.pop(
        "expected_world_causal_attribution_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_world_causal_attribution_verification_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_world_causal_attribution_verification_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "world_causal_attribution_verification_policy_digest",
        "verifyos-dukkha-preserving-world-causal-attribution-policy-v09",
    )
    responsibility = overrides.pop(
        "world_causal_attribution_verification_responsibility_digest",
        "verifyos-world-causal-attribution-responsibility-v09",
    )
    request_id = overrides.pop(
        "world_causal_attribution_verification_request_id",
        "verifyos-world-causal-attribution-verification-v09-001",
    )
    bundle = overrides.pop(
        "world_causal_attribution_verification_bundle_digest",
        compute_world_causal_attribution_verification_bundle_digest(
            source_world_fact_confirmation_receipt_digest=fact_digest,
            expected_source_world_fact_confirmation_receipt_digest=expected_fact,
            source_world_postcondition_verification_receipt_digest=verification_digest,
            expected_source_world_postcondition_verification_receipt_digest=(
                expected_verification
            ),
            source_world_mutation_application_receipt_digest=mutation_digest,
            expected_source_world_mutation_application_receipt_digest=expected_mutation,
            source_world_fact_confirmation_review_certificate_digest=fact.get(
                "world_fact_confirmation_review_certificate_digest"
            ),
            source_world_fact_confirmation_record_digest=fact.get(
                "world_fact_confirmation_record_digest"
            ),
            source_world_fact_confirmation_debt_consumption_record_digest=fact.get(
                "world_fact_confirmation_debt_consumption_record_digest"
            ),
            source_bounded_world_fact_status_binding_digest=fact.get(
                "bounded_world_fact_status_binding_digest"
            ),
            source_causal_attribution_verification_handoff_envelope_digest=fact.get(
                "causal_attribution_verification_handoff_envelope_digest"
            ),
            world_causal_attribution_evidence_packet_digest=evidence_digest,
            expected_world_causal_attribution_evidence_packet_digest=expected_evidence,
            world_causal_attribution_verification_review_certificate_digest=review_digest,
            expected_world_causal_attribution_verification_review_certificate_digest=(
                expected_review
            ),
            world_causal_attribution_verification_intake_context_digest=context_digest,
            expected_world_causal_attribution_verification_intake_context_digest=(
                expected_context
            ),
            requested_world_causal_attribution_verification_operation_digest=context.get(
                "requested_world_causal_attribution_verification_operation_digest"
            ),
            exact_world_causal_attribution_verification_cycle_digest=context.get(
                "exact_world_causal_attribution_verification_cycle_digest"
            ),
            world_causal_attribution_verification_policy_digest=policy,
            world_causal_attribution_verification_responsibility_digest=responsibility,
            world_causal_attribution_verification_request_id=request_id,
        ),
    )
    args = {
        "source_world_fact_confirmation_receipt": fact,
        "expected_source_world_fact_confirmation_receipt_digest": expected_fact,
        "source_world_postcondition_verification_receipt": verification,
        "expected_source_world_postcondition_verification_receipt_digest": (
            expected_verification
        ),
        "source_world_mutation_application_receipt": mutation,
        "expected_source_world_mutation_application_receipt_digest": expected_mutation,
        "world_causal_attribution_evidence_packet": evidence,
        "expected_world_causal_attribution_evidence_packet_digest": expected_evidence,
        "world_causal_attribution_verification_review_certificate": review,
        "expected_world_causal_attribution_verification_review_certificate_digest": (
            expected_review
        ),
        "world_causal_attribution_verification_intake_context": context,
        "expected_world_causal_attribution_verification_intake_context_digest": (
            expected_context
        ),
        "world_causal_attribution_verification_policy_digest": policy,
        "world_causal_attribution_verification_responsibility_digest": responsibility,
        "world_causal_attribution_verification_request_id": request_id,
        "world_causal_attribution_verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_dukkha_preserving_world_causal_attribution_verification_intake(
        **args
    )


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert (
        result.receipt["world_causal_attribution_verification_disposition"]
        == disposition
    )
    assert result.receipt["verifyos_version"] == "v0.9"
    return result.receipt


def _review_route(field: str, value, disposition: str) -> None:
    fact, verification, mutation = _sources()
    evidence = _evidence(fact, verification, mutation)
    review = _review(fact, verification, mutation, evidence)
    review[field] = value
    review = _redigest_review(review, evidence)
    context = _redigest_context(
        fact,
        verification,
        mutation,
        evidence,
        review,
        _context(fact, verification, mutation, evidence, review),
    )
    _assert_disposition(
        _build(
            source_world_fact_confirmation_receipt=fact,
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_causal_attribution_evidence_packet=evidence,
            world_causal_attribution_verification_review_certificate=review,
            world_causal_attribution_verification_intake_context=context,
        ),
        disposition,
    )


def main() -> int:
    supported = _assert_disposition(_build(), DISPOSITION_SUPPORTED)
    assert supported["world_causal_attribution_verification_state_before"] == STATE_BEFORE
    assert (
        supported["world_causal_attribution_verification_state_after"]
        == STATE_AFTER_SUPPORTED
    )
    assert supported["bounded_world_fact_confirmed"] is True
    assert supported["world_fact_confirmed"] is True
    assert supported["causal_attribution_confirmed"] is True
    assert supported["causal_attribution_scope_exactly_bounded"] is True
    assert supported["dukkha_reduction_realized_confirmed"] is False
    assert supported["world_causal_attribution_verification_debt_consumed"] is True
    assert supported["world_causal_attribution_verification_debt_open"] is False
    assert supported["dukkha_realization_verification_intake_admitted"] is True
    assert supported["persistent_world_state_changed_by_causal_verification"] is False
    assert supported["world_model_revision_incremented_by_causal_verification"] is False
    assert supported["world_mutation_reperformed"] is False
    assert supported["tool_invocation_performed"] is False
    assert supported["external_side_effect_performed"] is False
    assert supported["bounded_world_causal_attribution_binding"] is not None
    assert supported["dukkha_realization_verification_handoff_envelope"] is not None
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: value
            for key, value in supported.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )

    blocked = _build(
        expected_source_world_fact_confirmation_receipt_digest="wrong"
    )
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert (
        "source_world_fact_confirmation_expected_binding_mismatch"
        in blocked.blockers
    )

    fact, verification, mutation = _sources()
    evidence = _evidence(fact, verification, mutation)
    review = _review(fact, verification, mutation, evidence)

    context = _context(fact, verification, mutation, evidence, review)
    context["current_world_model_state_digest"] = "stale-world-state"
    context = _redigest_context(
        fact, verification, mutation, evidence, review, context
    )
    _assert_disposition(
        _build(
            source_world_fact_confirmation_receipt=fact,
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_causal_attribution_evidence_packet=evidence,
            world_causal_attribution_verification_review_certificate=review,
            world_causal_attribution_verification_intake_context=context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )

    context = _context(fact, verification, mutation, evidence, review)
    context["source_world_fact_confirmation_epoch"] = 100
    context = _redigest_context(
        fact, verification, mutation, evidence, review, context
    )
    _assert_disposition(
        _build(
            source_world_fact_confirmation_receipt=fact,
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_causal_attribution_evidence_packet=evidence,
            world_causal_attribution_verification_review_certificate=review,
            world_causal_attribution_verification_intake_context=context,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    review_refresh = _review(fact, verification, mutation, evidence)
    review_refresh["verification_review_started_epoch"] = 100
    review_refresh["verification_review_completed_epoch"] = 110
    review_refresh["maximum_verification_review_duration"] = 4
    review_refresh = _redigest_review(review_refresh, evidence)
    context = _redigest_context(
        fact,
        verification,
        mutation,
        evidence,
        review_refresh,
        _context(fact, verification, mutation, evidence, review_refresh),
    )
    _assert_disposition(
        _build(
            source_world_fact_confirmation_receipt=fact,
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_causal_attribution_evidence_packet=evidence,
            world_causal_attribution_verification_review_certificate=review_refresh,
            world_causal_attribution_verification_intake_context=context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    additional = _evidence(fact, verification, mutation)
    additional["independent_causal_evidence"] = False
    additional = _redigest_evidence(additional)
    additional_review = _redigest_review(
        _review(fact, verification, mutation, additional), additional
    )
    additional_context = _redigest_context(
        fact,
        verification,
        mutation,
        additional,
        additional_review,
        _context(fact, verification, mutation, additional, additional_review),
    )
    _assert_disposition(
        _build(
            source_world_fact_confirmation_receipt=fact,
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_causal_attribution_evidence_packet=additional,
            world_causal_attribution_verification_review_certificate=additional_review,
            world_causal_attribution_verification_intake_context=additional_context,
        ),
        DISPOSITION_ADDITIONAL_EVIDENCE,
    )

    for field, disposition in (
        ("causal_model_adequate", DISPOSITION_CAUSAL_MODEL_REPAIR),
        ("intervention_correspondence_confirmed", DISPOSITION_INTERVENTION_REPAIR),
        ("temporal_ordering_confirmed", DISPOSITION_TEMPORAL_REPAIR),
        ("confounding_control_adequate", DISPOSITION_CONFOUNDING_REPAIR),
        ("counterfactual_support_adequate", DISPOSITION_COUNTERFACTUAL_REPAIR),
        ("alternative_causes_assessed", DISPOSITION_ALTERNATIVE_CAUSE_REVIEW),
        ("selection_bias_adequate", DISPOSITION_SELECTION_BIAS_REVIEW),
        ("measurement_validity_adequate", DISPOSITION_MEASUREMENT_REPAIR),
        ("uncertainty_adequate", DISPOSITION_UNCERTAINTY_REPAIR),
        ("calibration_adequate", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
        (
            "protected_group_nonexternalization_supported",
            DISPOSITION_NONEXTERNALIZATION_REVIEW,
        ),
        ("no_truth_generalization", DISPOSITION_TRUTH_GENERALIZATION_REJECTED),
        (
            "no_dukkha_realization_overclaim",
            DISPOSITION_DUKKHA_OVERCLAIM_REJECTED,
        ),
    ):
        _review_route(field, False, disposition)

    replay_context = _context(fact, verification, mutation, evidence, review)
    replay_context[
        "prior_world_causal_attribution_verification_intake_session_ids"
    ] = [replay_context["world_causal_attribution_verification_intake_session_id"]]
    replay_context = _redigest_context(
        fact, verification, mutation, evidence, review, replay_context
    )
    replay = _assert_disposition(
        _build(
            source_world_fact_confirmation_receipt=fact,
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_causal_attribution_evidence_packet=evidence,
            world_causal_attribution_verification_review_certificate=review,
            world_causal_attribution_verification_intake_context=replay_context,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )
    assert replay["world_fact_confirmed"] is True
    assert replay["causal_attribution_confirmed"] is False
    assert replay["dukkha_reduction_realized_confirmed"] is False
    assert replay["world_causal_attribution_verification_debt_open"] is True

    print("PASS: VerifyOS v0.9 WORLD causal-attribution verification intake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
