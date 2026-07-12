#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_world_dukkha_preserving_world_fact_confirmation_disposition_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ADDITIONAL_EVIDENCE,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CAUSAL_OVERCLAIM_REJECTED,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_DUKKHA_OVERCLAIM_REJECTED,
    DISPOSITION_FACT_REPAIR,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_RELATION_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_REVISION_REPAIR,
    DISPOSITION_STATE_REPAIR,
    DISPOSITION_STORAGE_REPAIR,
    DISPOSITION_SUPPORTED,
    DISPOSITION_TRUTH_PROMOTION_REJECTED,
    DISPOSITION_WORLD_REFRESH,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_EVIDENCE_DIGEST_FIELD,
    SOURCE_MUTATION_DIGEST_FIELD,
    SOURCE_VERIFICATION_DIGEST_FIELD,
    SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_world_dukkha_preserving_world_fact_confirmation_disposition_intake,
    canonical_digest,
    compute_exact_world_fact_confirmation_cycle_digest,
    compute_requested_world_fact_confirmation_operation_digest,
    compute_world_fact_confirmation_bundle_digest,
    compute_world_fact_confirmation_intake_context_digest,
    compute_world_fact_confirmation_review_certificate_digest,
)
from scripts.check_verifyos_dukkha_preserving_world_postcondition_verification_intake_v0_1 import (
    _build as build_verifyos_v08,
    _source as build_world_v062_source,
)


def _sources() -> tuple[dict, dict]:
    verification_result = build_verifyos_v08()
    assert verification_result.status == STATUS_READY, verification_result.blockers
    assert verification_result.receipt is not None
    verification = deepcopy(verification_result.receipt)
    mutation = deepcopy(build_world_v062_source())
    assert (
        verification["world_postcondition_verification_disposition"]
        == "world_postcondition_verification_supported"
    )
    assert verification["world_postcondition_verification_state_after"] == STATE_BEFORE
    assert verification["world_fact_confirmation_receipt_required"] is True
    assert verification["world_fact_confirmed"] is False
    assert (
        verification["source_world_mutation_application_receipt_digest"]
        == mutation[SOURCE_MUTATION_DIGEST_FIELD]
    )
    return verification, mutation


def _review(verification: dict, mutation: dict) -> dict:
    evidence = verification["world_postcondition_evidence_packet"]
    persisted = mutation["persisted_world_candidate_envelope"]
    mutation_record = mutation["world_mutation_record"]
    application_review = mutation["world_mutation_application_review_certificate"]
    review = {
        "source_world_postcondition_verification_receipt_digest": verification[
            SOURCE_VERIFICATION_DIGEST_FIELD
        ],
        "source_world_mutation_application_receipt_digest": mutation[
            SOURCE_MUTATION_DIGEST_FIELD
        ],
        "source_world_postcondition_evidence_packet_digest": verification[
            SOURCE_EVIDENCE_DIGEST_FIELD
        ],
        "source_world_postcondition_verification_review_certificate_digest": (
            verification[SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD]
        ),
        "source_world_postcondition_verification_record_digest": verification[
            "world_postcondition_verification_record_digest"
        ],
        "source_world_postcondition_verification_debt_consumption_record_digest": (
            verification[
                "world_postcondition_verification_debt_consumption_record_digest"
            ]
        ),
        "source_world_fact_confirmation_handoff_envelope_digest": verification[
            "world_fact_confirmation_handoff_envelope_digest"
        ],
        "source_world_mutation_record_digest": mutation["world_mutation_record_digest"],
        "source_persisted_world_candidate_envelope_digest": mutation[
            "persisted_world_candidate_envelope_digest"
        ],
        "world_mutation_transaction_digest": mutation_record[
            "world_mutation_transaction_digest"
        ],
        "world_candidate_fact_digest": persisted["world_candidate_fact_digest"],
        "world_candidate_relation_digest": persisted[
            "world_candidate_relation_digest"
        ],
        "resulting_world_state_digest": persisted["world_state_after_digest"],
        "resulting_world_revision": persisted["world_model_revision_after"],
        "persistent_world_storage_target_digest": application_review[
            "persistent_world_storage_target_digest"
        ],
        "expected_world_update_postcondition_digest": mutation_record[
            "world_update_postcondition_digest"
        ],
        "uncertainty_digest": evidence["uncertainty_digest"],
        "calibration_digest": evidence["calibration_digest"],
        "provenance_chain_digests": evidence["provenance_chain_digests"],
        "protected_group_observed_impact_digest": evidence[
            "protected_group_observed_impact_digest"
        ],
        "future_subject_observed_impact_digest": evidence[
            "future_subject_observed_impact_digest"
        ],
        "realized_dukkha_observation_digest": evidence[
            "realized_dukkha_observation_digest"
        ],
        "fact_confirmation_reviewer_id": "world-fact-confirmation-reviewer-v063",
        "fact_confirmation_method_digest": "world-bounded-fact-method-v063-001",
        "fact_confirmation_evidence_digest": "world-bounded-fact-evidence-v063-001",
        "fact_confirmation_review_started_epoch": 131,
        "fact_confirmation_review_completed_epoch": 132,
        "maximum_fact_confirmation_review_duration": 4,
        "source_postcondition_verification_supported": True,
        "postcondition_evidence_sufficient": True,
        "candidate_fact_correspondence_confirmed": True,
        "candidate_relation_correspondence_confirmed": True,
        "world_state_correspondence_confirmed": True,
        "world_revision_correspondence_confirmed": True,
        "storage_persistence_confirmed": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "exact_bounded_fact_scope_preserved": True,
        "generalized_truth_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    review[REVIEW_DIGEST_FIELD] = (
        compute_world_fact_confirmation_review_certificate_digest(review)
    )
    return review


def _context(verification: dict, mutation: dict, review: dict) -> dict:
    verification_epoch = verification["world_postcondition_verification_record"][
        "world_postcondition_verification_intake_epoch"
    ]
    persisted = mutation["persisted_world_candidate_envelope"]
    application_review = mutation["world_mutation_application_review_certificate"]
    context = {
        "source_world_postcondition_verification_receipt_digest": verification[
            SOURCE_VERIFICATION_DIGEST_FIELD
        ],
        "source_world_mutation_application_receipt_digest": mutation[
            SOURCE_MUTATION_DIGEST_FIELD
        ],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": verification["source_world_binding_digest"],
        "current_world_model_state_digest": persisted["world_state_after_digest"],
        "current_world_model_revision": persisted["world_model_revision_after"],
        "current_persistent_world_storage_target_digest": application_review[
            "persistent_world_storage_target_digest"
        ],
        "current_world_lineage_digest": canonical_digest(
            verification["resulting_lineage_digests"]
        ),
        "source_postcondition_verification_epoch": verification_epoch,
        "world_fact_confirmation_intake_epoch": verification_epoch + 3,
        "maximum_world_fact_confirmation_intake_delay": 8,
        "world_fact_confirmation_intake_session_id": (
            "world-fact-confirmation-intake-v063-001"
        ),
        "world_fact_confirmation_intake_nonce_digest": (
            "world-fact-confirmation-nonce-v063-001"
        ),
        "prior_world_fact_confirmation_intake_session_ids": [],
        "prior_world_fact_confirmation_review_certificate_digests": [],
        "prior_world_fact_confirmation_intake_nonce_digests": [],
        "prior_confirmed_world_postcondition_verification_receipt_digests": [],
        "requested_world_fact_confirmation_operation_digest": (
            compute_requested_world_fact_confirmation_operation_digest(
                verification, mutation, review
            )
        ),
        "exact_world_fact_confirmation_cycle_digest": "",
    }
    context["exact_world_fact_confirmation_cycle_digest"] = (
        compute_exact_world_fact_confirmation_cycle_digest(
            verification, mutation, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = (
        compute_world_fact_confirmation_intake_context_digest(context)
    )
    return context


def _redigest_review(review: dict) -> dict:
    value = deepcopy(review)
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_world_fact_confirmation_review_certificate_digest(value)
    )
    return value


def _redigest_context(
    verification: dict, mutation: dict, review: dict, context: dict
) -> dict:
    value = deepcopy(context)
    value["source_world_postcondition_verification_receipt_digest"] = verification[
        SOURCE_VERIFICATION_DIGEST_FIELD
    ]
    value["source_world_mutation_application_receipt_digest"] = mutation[
        SOURCE_MUTATION_DIGEST_FIELD
    ]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_fact_confirmation_operation_digest"] = (
        compute_requested_world_fact_confirmation_operation_digest(
            verification, mutation, review
        )
    )
    value["exact_world_fact_confirmation_cycle_digest"] = (
        compute_exact_world_fact_confirmation_cycle_digest(
            verification, mutation, review, value
        )
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_world_fact_confirmation_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    default_verification, default_mutation = _sources()
    verification = deepcopy(
        overrides.pop("source_world_postcondition_verification_receipt", None)
        or default_verification
    )
    mutation = deepcopy(
        overrides.pop("source_world_mutation_application_receipt", None)
        or default_mutation
    )
    review = deepcopy(
        overrides.pop("world_fact_confirmation_review_certificate", None)
        or _review(verification, mutation)
    )
    context = deepcopy(
        overrides.pop("world_fact_confirmation_intake_context", None)
        or _context(verification, mutation, review)
    )

    verification_digest = verification.get(
        SOURCE_VERIFICATION_DIGEST_FIELD, "verification-v08-missing"
    )
    mutation_digest = mutation.get(
        SOURCE_MUTATION_DIGEST_FIELD, "mutation-v062-missing"
    )
    review_digest = review.get(REVIEW_DIGEST_FIELD, "review-v063-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "context-v063-missing")

    expected_verification = overrides.pop(
        "expected_source_world_postcondition_verification_receipt_digest",
        verification_digest,
    )
    expected_mutation = overrides.pop(
        "expected_source_world_mutation_application_receipt_digest", mutation_digest
    )
    expected_review = overrides.pop(
        "expected_world_fact_confirmation_review_certificate_digest", review_digest
    )
    expected_context = overrides.pop(
        "expected_world_fact_confirmation_intake_context_digest", context_digest
    )
    policy = overrides.pop(
        "world_fact_confirmation_policy_digest",
        "world-dukkha-preserving-bounded-fact-confirmation-policy-v063",
    )
    responsibility = overrides.pop(
        "world_fact_confirmation_responsibility_digest",
        "world-bounded-fact-confirmation-responsibility-v063",
    )
    request_id = overrides.pop(
        "world_fact_confirmation_request_id",
        "world-fact-confirmation-v063-001",
    )
    bundle = overrides.pop(
        "world_fact_confirmation_bundle_digest",
        compute_world_fact_confirmation_bundle_digest(
            source_world_postcondition_verification_receipt_digest=verification_digest,
            expected_source_world_postcondition_verification_receipt_digest=(
                expected_verification
            ),
            source_world_mutation_application_receipt_digest=mutation_digest,
            expected_source_world_mutation_application_receipt_digest=expected_mutation,
            source_world_postcondition_evidence_packet_digest=verification.get(
                SOURCE_EVIDENCE_DIGEST_FIELD
            ),
            source_world_postcondition_verification_review_certificate_digest=(
                verification.get(SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD)
            ),
            source_world_postcondition_verification_record_digest=verification.get(
                "world_postcondition_verification_record_digest"
            ),
            source_world_postcondition_verification_debt_consumption_record_digest=(
                verification.get(
                    "world_postcondition_verification_debt_consumption_record_digest"
                )
            ),
            source_world_fact_confirmation_handoff_envelope_digest=verification.get(
                "world_fact_confirmation_handoff_envelope_digest"
            ),
            source_world_mutation_record_digest=mutation.get(
                "world_mutation_record_digest"
            ),
            source_persisted_world_candidate_envelope_digest=mutation.get(
                "persisted_world_candidate_envelope_digest"
            ),
            world_candidate_fact_digest=review.get("world_candidate_fact_digest"),
            world_candidate_relation_digest=review.get(
                "world_candidate_relation_digest"
            ),
            resulting_world_state_digest=review.get("resulting_world_state_digest"),
            resulting_world_revision=review.get("resulting_world_revision"),
            persistent_world_storage_target_digest=review.get(
                "persistent_world_storage_target_digest"
            ),
            expected_world_update_postcondition_digest=review.get(
                "expected_world_update_postcondition_digest"
            ),
            world_fact_confirmation_review_certificate_digest=review_digest,
            expected_world_fact_confirmation_review_certificate_digest=expected_review,
            world_fact_confirmation_intake_context_digest=context_digest,
            expected_world_fact_confirmation_intake_context_digest=expected_context,
            requested_world_fact_confirmation_operation_digest=context.get(
                "requested_world_fact_confirmation_operation_digest"
            ),
            exact_world_fact_confirmation_cycle_digest=context.get(
                "exact_world_fact_confirmation_cycle_digest"
            ),
            world_fact_confirmation_policy_digest=policy,
            world_fact_confirmation_responsibility_digest=responsibility,
            world_fact_confirmation_request_id=request_id,
        ),
    )

    args = {
        "source_world_postcondition_verification_receipt": verification,
        "expected_source_world_postcondition_verification_receipt_digest": (
            expected_verification
        ),
        "source_world_mutation_application_receipt": mutation,
        "expected_source_world_mutation_application_receipt_digest": expected_mutation,
        "world_fact_confirmation_review_certificate": review,
        "expected_world_fact_confirmation_review_certificate_digest": expected_review,
        "world_fact_confirmation_intake_context": context,
        "expected_world_fact_confirmation_intake_context_digest": expected_context,
        "world_fact_confirmation_policy_digest": policy,
        "world_fact_confirmation_responsibility_digest": responsibility,
        "world_fact_confirmation_request_id": request_id,
        "world_fact_confirmation_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_world_dukkha_preserving_world_fact_confirmation_disposition_intake(
        **args
    )


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["world_fact_confirmation_disposition"] == disposition
    assert result.receipt["world_version"] == "v0.63"
    return result.receipt


def _review_route(field: str, value, disposition: str) -> None:
    verification, mutation = _sources()
    review = _review(verification, mutation)
    review[field] = value
    review = _redigest_review(review)
    context = _redigest_context(
        verification,
        mutation,
        review,
        _context(verification, mutation, review),
    )
    _assert_disposition(
        _build(
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_fact_confirmation_review_certificate=review,
            world_fact_confirmation_intake_context=context,
        ),
        disposition,
    )


def main() -> int:
    supported = _assert_disposition(_build(), DISPOSITION_SUPPORTED)
    assert supported["world_fact_confirmation_state_before"] == STATE_BEFORE
    assert supported["world_fact_confirmation_state_after"] == STATE_AFTER_SUPPORTED
    assert supported["world_fact_confirmation_supported"] is True
    assert supported["world_fact_confirmation_debt_consumed"] is True
    assert supported["world_fact_confirmation_debt_open"] is False
    assert supported["bounded_world_fact_confirmed"] is True
    assert supported["world_fact_confirmed"] is True
    assert supported["world_fact_confirmation_scope_exactly_bounded"] is True
    assert supported["generalized_world_truth_confirmed"] is False
    assert supported["causal_attribution_confirmed"] is False
    assert supported["dukkha_reduction_realized_confirmed"] is False
    assert supported["persistent_world_model_state_unchanged_by_fact_confirmation"] is True
    assert supported["persistent_world_state_changed_by_fact_confirmation"] is False
    assert supported["world_model_revision_incremented_by_fact_confirmation"] is False
    assert supported["world_mutation_reperformed"] is False
    assert supported["world_patch_reapplied"] is False
    assert supported["tool_invocation_performed"] is False
    assert supported["external_side_effect_performed"] is False
    assert supported["world_mutation_authority_granted"] is False
    assert supported["bounded_world_fact_status_binding"] is not None
    assert supported["causal_attribution_verification_handoff_envelope"] is not None
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: value
            for key, value in supported.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )

    blocked = _build(
        expected_source_world_postcondition_verification_receipt_digest="wrong"
    )
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert (
        "source_world_postcondition_verification_expected_binding_mismatch"
        in blocked.blockers
    )

    verification, mutation = _sources()
    review = _review(verification, mutation)

    context = _context(verification, mutation, review)
    context["current_world_model_state_digest"] = "stale-world-state"
    context = _redigest_context(verification, mutation, review, context)
    refreshed = _assert_disposition(
        _build(
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_fact_confirmation_review_certificate=review,
            world_fact_confirmation_intake_context=context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )
    assert refreshed["world_fact_confirmed"] is False
    assert refreshed["world_fact_confirmation_debt_open"] is True
    assert (
        refreshed["source_world_postcondition_verification_receipt_replay_closed"]
        is False
    )

    context = _context(verification, mutation, review)
    context["world_fact_confirmation_intake_epoch"] = (
        context["source_postcondition_verification_epoch"] + 20
    )
    context = _redigest_context(verification, mutation, review, context)
    _assert_disposition(
        _build(
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_fact_confirmation_review_certificate=review,
            world_fact_confirmation_intake_context=context,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    review_refresh = _review(verification, mutation)
    review_refresh["fact_confirmation_review_started_epoch"] = 100
    review_refresh["fact_confirmation_review_completed_epoch"] = 110
    review_refresh["maximum_fact_confirmation_review_duration"] = 4
    review_refresh = _redigest_review(review_refresh)
    context = _redigest_context(
        verification,
        mutation,
        review_refresh,
        _context(verification, mutation, review_refresh),
    )
    _assert_disposition(
        _build(
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_fact_confirmation_review_certificate=review_refresh,
            world_fact_confirmation_intake_context=context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    _review_route(
        "postcondition_evidence_sufficient", False, DISPOSITION_ADDITIONAL_EVIDENCE
    )
    _review_route(
        "candidate_fact_correspondence_confirmed", False, DISPOSITION_FACT_REPAIR
    )
    _review_route(
        "candidate_relation_correspondence_confirmed",
        False,
        DISPOSITION_RELATION_REPAIR,
    )
    _review_route(
        "world_state_correspondence_confirmed", False, DISPOSITION_STATE_REPAIR
    )
    _review_route(
        "world_revision_correspondence_confirmed", False, DISPOSITION_REVISION_REPAIR
    )
    _review_route(
        "storage_persistence_confirmed", False, DISPOSITION_STORAGE_REPAIR
    )
    _review_route("calibration_adequate", False, DISPOSITION_CALIBRATION_REPAIR)
    _review_route(
        "provenance_continuity_preserved", False, DISPOSITION_PROVENANCE_REPAIR
    )
    _review_route(
        "protected_group_nonexternalization_supported",
        False,
        DISPOSITION_NONEXTERNALIZATION_REVIEW,
    )
    _review_route(
        "causal_attribution_claimed",
        True,
        DISPOSITION_CAUSAL_OVERCLAIM_REJECTED,
    )
    _review_route(
        "realized_dukkha_reduction_claimed",
        True,
        DISPOSITION_DUKKHA_OVERCLAIM_REJECTED,
    )
    _review_route(
        "generalized_truth_claimed", True, DISPOSITION_TRUTH_PROMOTION_REJECTED
    )

    replay_context = _context(verification, mutation, review)
    replay_context[
        "prior_world_fact_confirmation_intake_session_ids"
    ] = [replay_context["world_fact_confirmation_intake_session_id"]]
    replay_context = _redigest_context(
        verification, mutation, review, replay_context
    )
    _assert_disposition(
        _build(
            source_world_postcondition_verification_receipt=verification,
            source_world_mutation_application_receipt=mutation,
            world_fact_confirmation_review_certificate=review,
            world_fact_confirmation_intake_context=replay_context,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )

    print("PASS: WORLD v0.63 bounded WORLD fact-confirmation disposition intake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
