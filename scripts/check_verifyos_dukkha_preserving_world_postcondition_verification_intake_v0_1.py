#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_world_postcondition_verification_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ADDITIONAL_EVIDENCE,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_CORRESPONDENCE_REPAIR,
    DISPOSITION_DUKKHA_REVIEW,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_POSTCONDITION_REPAIR,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_REVISION_MISMATCH,
    DISPOSITION_STATE_MISMATCH,
    DISPOSITION_STORAGE_REPAIR,
    DISPOSITION_SUPPORTED,
    DISPOSITION_TRUTH_PROMOTION_REJECTED,
    DISPOSITION_WORLD_REFRESH,
    EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_verifyos_dukkha_preserving_world_postcondition_verification_intake,
    canonical_digest,
    compute_exact_world_postcondition_verification_cycle_digest,
    compute_requested_world_postcondition_verification_operation_digest,
    compute_world_postcondition_evidence_packet_digest,
    compute_world_postcondition_verification_bundle_digest,
    compute_world_postcondition_verification_intake_context_digest,
    compute_world_postcondition_verification_review_certificate_digest,
)
from scripts.check_world_dukkha_preserving_single_use_world_mutation_application_intake_v0_1 import (
    _build as build_world_v062_mutation,
)


def _source() -> dict:
    result = build_world_v062_mutation()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert (
        result.receipt["world_mutation_application_disposition"]
        == "world_mutation_application_ready"
    )
    assert result.receipt["world_mutation_application_state_after"] == STATE_BEFORE
    assert result.receipt["world_postcondition_verification_debt_open"] is True
    return deepcopy(result.receipt)


def _evidence(source: dict) -> dict:
    handoff = source["world_postcondition_verification_handoff_envelope"]
    source_review = source["world_mutation_application_review_certificate"]
    evidence = {
        "source_world_mutation_application_receipt_digest": source[
            SOURCE_DIGEST_FIELD
        ],
        "world_mutation_application_record_digest": source[
            "world_mutation_application_record_digest"
        ],
        "world_candidate_commit_authorization_consumption_record_digest": source[
            "world_candidate_commit_authorization_consumption_record_digest"
        ],
        "world_mutation_record_digest": source["world_mutation_record_digest"],
        "persisted_world_candidate_envelope_digest": source[
            "persisted_world_candidate_envelope_digest"
        ],
        "world_postcondition_verification_handoff_envelope_digest": source[
            "world_postcondition_verification_handoff_envelope_digest"
        ],
        "world_mutation_transaction_digest": handoff[
            "world_mutation_transaction_digest"
        ],
        "expected_world_update_postcondition_digest": handoff[
            "world_update_postcondition_digest"
        ],
        "observed_world_state_digest": handoff["world_state_after_digest"],
        "observed_world_model_revision": handoff["world_model_revision_after"],
        "observed_persistent_world_storage_target_digest": source_review[
            "persistent_world_storage_target_digest"
        ],
        "evidence_collector_id": "verifyos-world-postcondition-collector-v08",
        "evidence_source_id": "world-persistent-storage-readback-v08",
        "collection_started_epoch": 127,
        "collection_completed_epoch": 128,
        "maximum_collection_duration": 4,
        "raw_post_application_artifact_digest": (
            "world-post-application-artifact-v08-001"
        ),
        "uncertainty_digest": "world-postcondition-uncertainty-v08-001",
        "calibration_digest": "world-postcondition-calibration-v08-001",
        "provenance_chain_digests": sorted(
            {
                source[SOURCE_DIGEST_FIELD],
                source["world_mutation_record_digest"],
                source["persisted_world_candidate_envelope_digest"],
                "world-storage-readback-provenance-v08-001",
            }
        ),
        "tamper_evidence_digest": "world-postcondition-tamper-evidence-v08-001",
        "protected_group_observed_impact_digest": (
            "world-postcondition-protected-group-impact-v08-001"
        ),
        "future_subject_observed_impact_digest": (
            "world-postcondition-future-subject-impact-v08-001"
        ),
        "realized_dukkha_observation_digest": (
            "world-postcondition-realized-dukkha-observation-v08-001"
        ),
        "independent_post_application_evidence": True,
        "exactly_one_post_application_evidence_collection": True,
        "world_mutation_performed_by_evidence_collector": False,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = (
        compute_world_postcondition_evidence_packet_digest(evidence)
    )
    return evidence


def _review(source: dict, evidence: dict) -> dict:
    handoff = source["world_postcondition_verification_handoff_envelope"]
    review = {
        "source_world_mutation_application_receipt_digest": source[
            SOURCE_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        "world_mutation_application_record_digest": source[
            "world_mutation_application_record_digest"
        ],
        "world_mutation_record_digest": source["world_mutation_record_digest"],
        "persisted_world_candidate_envelope_digest": source[
            "persisted_world_candidate_envelope_digest"
        ],
        "world_mutation_transaction_digest": handoff[
            "world_mutation_transaction_digest"
        ],
        "expected_world_update_postcondition_digest": handoff[
            "world_update_postcondition_digest"
        ],
        "verifier_id": "verifyos-world-postcondition-verifier-v08",
        "verification_method_digest": "world-postcondition-method-v08-001",
        "verification_evidence_digest": "world-postcondition-evidence-v08-001",
        "verification_review_started_epoch": 128,
        "verification_review_completed_epoch": 129,
        "maximum_verification_review_duration": 4,
        "source_mutation_applied": True,
        "mutation_transaction_correspondence_confirmed": True,
        "world_state_digest_matches": True,
        "world_revision_matches": True,
        "world_storage_persistence_confirmed": True,
        "world_postcondition_satisfied": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "realized_dukkha_assessment_adequate": True,
        "no_truth_overclaim": True,
        "no_causal_overclaim": True,
        "no_realized_dukkha_overclaim": True,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    review[REVIEW_DIGEST_FIELD] = (
        compute_world_postcondition_verification_review_certificate_digest(review)
    )
    return review


def _context(source: dict, evidence: dict, review: dict) -> dict:
    applied_epoch = source["world_mutation_application_record"][
        "world_mutation_application_intake_epoch"
    ]
    persisted = source["persisted_world_candidate_envelope"]
    context = {
        "source_world_mutation_application_receipt_digest": source[
            SOURCE_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": persisted["world_state_after_digest"],
        "current_world_model_revision": persisted["world_model_revision_after"],
        "current_world_lineage_digest": canonical_digest(
            source["resulting_lineage_digests"]
        ),
        "source_world_mutation_applied_epoch": applied_epoch,
        "world_postcondition_verification_intake_epoch": applied_epoch + 4,
        "maximum_world_postcondition_verification_intake_delay": 8,
        "world_postcondition_verification_intake_session_id": (
            "verifyos-world-postcondition-intake-v08-001"
        ),
        "world_postcondition_verification_intake_nonce_digest": (
            "verifyos-world-postcondition-nonce-v08-001"
        ),
        "prior_world_postcondition_verification_intake_session_ids": [],
        "prior_world_postcondition_evidence_packet_digests": [],
        "prior_world_postcondition_verification_review_certificate_digests": [],
        "prior_world_postcondition_verification_intake_nonce_digests": [],
        "prior_verified_world_mutation_application_receipt_digests": [],
        "requested_world_postcondition_verification_operation_digest": (
            compute_requested_world_postcondition_verification_operation_digest(
                source, evidence, review
            )
        ),
        "exact_world_postcondition_verification_cycle_digest": "",
    }
    context["exact_world_postcondition_verification_cycle_digest"] = (
        compute_exact_world_postcondition_verification_cycle_digest(
            source, evidence, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = (
        compute_world_postcondition_verification_intake_context_digest(context)
    )
    return context


def _redigest_evidence(evidence: dict) -> dict:
    value = deepcopy(evidence)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_world_postcondition_evidence_packet_digest(value)
    )
    return value


def _redigest_review(source: dict, evidence: dict, review: dict) -> dict:
    value = deepcopy(review)
    value["source_world_mutation_application_receipt_digest"] = source[
        SOURCE_DIGEST_FIELD
    ]
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_world_postcondition_verification_review_certificate_digest(value)
    )
    return value


def _redigest_context(
    source: dict, evidence: dict, review: dict, context: dict
) -> dict:
    value = deepcopy(context)
    value["source_world_mutation_application_receipt_digest"] = source[
        SOURCE_DIGEST_FIELD
    ]
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_postcondition_verification_operation_digest"] = (
        compute_requested_world_postcondition_verification_operation_digest(
            source, evidence, review
        )
    )
    value["exact_world_postcondition_verification_cycle_digest"] = (
        compute_exact_world_postcondition_verification_cycle_digest(
            source, evidence, review, value
        )
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_world_postcondition_verification_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    source = deepcopy(
        overrides.pop("source_world_mutation_application_receipt", None) or _source()
    )
    evidence = deepcopy(
        overrides.pop("world_postcondition_evidence_packet", None) or _evidence(source)
    )
    review = deepcopy(
        overrides.pop(
            "world_postcondition_verification_review_certificate", None
        )
        or _review(source, evidence)
    )
    context = deepcopy(
        overrides.pop("world_postcondition_verification_intake_context", None)
        or _context(source, evidence, review)
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v062-missing")
    evidence_digest = evidence.get(EVIDENCE_DIGEST_FIELD, "evidence-v08-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "review-v08-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "context-v08-missing")

    expected_source = overrides.pop(
        "expected_source_world_mutation_application_receipt_digest", source_digest
    )
    expected_evidence = overrides.pop(
        "expected_world_postcondition_evidence_packet_digest", evidence_digest
    )
    expected_review = overrides.pop(
        "expected_world_postcondition_verification_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_world_postcondition_verification_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "world_postcondition_verification_policy_digest",
        "verifyos-dukkha-preserving-world-postcondition-policy-v08",
    )
    responsibility = overrides.pop(
        "world_postcondition_verification_responsibility_digest",
        "verifyos-world-postcondition-responsibility-v08",
    )
    request_id = overrides.pop(
        "world_postcondition_verification_request_id",
        "verifyos-world-postcondition-verification-v08-001",
    )
    bundle = overrides.pop(
        "world_postcondition_verification_bundle_digest",
        compute_world_postcondition_verification_bundle_digest(
            source_world_mutation_application_receipt_digest=source_digest,
            expected_source_world_mutation_application_receipt_digest=expected_source,
            world_mutation_application_record_digest=source.get(
                "world_mutation_application_record_digest"
            ),
            world_mutation_record_digest=source.get("world_mutation_record_digest"),
            persisted_world_candidate_envelope_digest=source.get(
                "persisted_world_candidate_envelope_digest"
            ),
            world_postcondition_evidence_packet_digest=evidence_digest,
            expected_world_postcondition_evidence_packet_digest=expected_evidence,
            world_postcondition_verification_review_certificate_digest=review_digest,
            expected_world_postcondition_verification_review_certificate_digest=(
                expected_review
            ),
            world_postcondition_verification_intake_context_digest=context_digest,
            expected_world_postcondition_verification_intake_context_digest=(
                expected_context
            ),
            requested_world_postcondition_verification_operation_digest=context.get(
                "requested_world_postcondition_verification_operation_digest"
            ),
            exact_world_postcondition_verification_cycle_digest=context.get(
                "exact_world_postcondition_verification_cycle_digest"
            ),
            world_postcondition_verification_policy_digest=policy,
            world_postcondition_verification_responsibility_digest=responsibility,
            world_postcondition_verification_request_id=request_id,
        ),
    )

    args = {
        "source_world_mutation_application_receipt": source,
        "expected_source_world_mutation_application_receipt_digest": expected_source,
        "world_postcondition_evidence_packet": evidence,
        "expected_world_postcondition_evidence_packet_digest": expected_evidence,
        "world_postcondition_verification_review_certificate": review,
        "expected_world_postcondition_verification_review_certificate_digest": (
            expected_review
        ),
        "world_postcondition_verification_intake_context": context,
        "expected_world_postcondition_verification_intake_context_digest": (
            expected_context
        ),
        "world_postcondition_verification_policy_digest": policy,
        "world_postcondition_verification_responsibility_digest": responsibility,
        "world_postcondition_verification_request_id": request_id,
        "world_postcondition_verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_dukkha_preserving_world_postcondition_verification_intake(
        **args
    )


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert (
        result.receipt["world_postcondition_verification_disposition"]
        == disposition
    )
    assert result.receipt["verifyos_version"] == "v0.8"
    return result.receipt


def _review_route(field: str, value, disposition: str) -> None:
    source = _source()
    evidence = _evidence(source)
    review = _review(source, evidence)
    review[field] = value
    review = _redigest_review(source, evidence, review)
    context = _redigest_context(
        source, evidence, review, _context(source, evidence, review)
    )
    _assert_disposition(
        _build(
            source_world_mutation_application_receipt=source,
            world_postcondition_evidence_packet=evidence,
            world_postcondition_verification_review_certificate=review,
            world_postcondition_verification_intake_context=context,
        ),
        disposition,
    )


def main() -> int:
    supported = _assert_disposition(_build(), DISPOSITION_SUPPORTED)
    assert supported["world_postcondition_verification_state_before"] == STATE_BEFORE
    assert (
        supported["world_postcondition_verification_state_after"]
        == STATE_AFTER_SUPPORTED
    )
    assert supported["world_postcondition_verification_supported"] is True
    assert supported["world_postcondition_verification_debt_consumed"] is True
    assert supported["world_postcondition_verification_debt_open"] is False
    assert supported["world_fact_confirmation_intake_admitted"] is True
    assert supported["world_fact_confirmation_completed"] is False
    assert supported["persistent_world_model_state_unchanged_by_verifier"] is True
    assert supported["persistent_world_state_changed_by_verifier"] is False
    assert supported["world_fact_confirmed"] is False
    assert supported["causal_attribution_confirmed"] is False
    assert supported["dukkha_reduction_realized_confirmed"] is False
    assert supported["tool_invocation_performed"] is False
    assert supported["external_side_effect_performed"] is False
    assert supported["world_mutation_authority_granted"] is False
    assert supported["world_fact_confirmation_handoff_envelope"] is not None
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: value
            for key, value in supported.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )

    blocked = _build(
        expected_source_world_mutation_application_receipt_digest="wrong"
    )
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert (
        "source_world_mutation_application_expected_binding_mismatch"
        in blocked.blockers
    )

    source = _source()
    evidence = _evidence(source)
    review = _review(source, evidence)

    context = _context(source, evidence, review)
    context["current_world_model_state_digest"] = "stale-world-state"
    context = _redigest_context(source, evidence, review, context)
    _assert_disposition(
        _build(
            source_world_mutation_application_receipt=source,
            world_postcondition_evidence_packet=evidence,
            world_postcondition_verification_review_certificate=review,
            world_postcondition_verification_intake_context=context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )

    context = _context(source, evidence, review)
    context["source_world_mutation_applied_epoch"] = 100
    context = _redigest_context(source, evidence, review, context)
    _assert_disposition(
        _build(
            source_world_mutation_application_receipt=source,
            world_postcondition_evidence_packet=evidence,
            world_postcondition_verification_review_certificate=review,
            world_postcondition_verification_intake_context=context,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    review_refresh = _review(source, evidence)
    review_refresh["verification_review_started_epoch"] = 100
    review_refresh["verification_review_completed_epoch"] = 110
    review_refresh["maximum_verification_review_duration"] = 4
    review_refresh = _redigest_review(source, evidence, review_refresh)
    context = _redigest_context(
        source,
        evidence,
        review_refresh,
        _context(source, evidence, review_refresh),
    )
    _assert_disposition(
        _build(
            source_world_mutation_application_receipt=source,
            world_postcondition_evidence_packet=evidence,
            world_postcondition_verification_review_certificate=review_refresh,
            world_postcondition_verification_intake_context=context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    additional = _evidence(source)
    additional["independent_post_application_evidence"] = False
    additional = _redigest_evidence(additional)
    additional_review = _redigest_review(
        source, additional, _review(source, additional)
    )
    additional_context = _redigest_context(
        source,
        additional,
        additional_review,
        _context(source, additional, additional_review),
    )
    _assert_disposition(
        _build(
            source_world_mutation_application_receipt=source,
            world_postcondition_evidence_packet=additional,
            world_postcondition_verification_review_certificate=additional_review,
            world_postcondition_verification_intake_context=additional_context,
        ),
        DISPOSITION_ADDITIONAL_EVIDENCE,
    )

    _review_route(
        "mutation_transaction_correspondence_confirmed",
        False,
        DISPOSITION_CORRESPONDENCE_REPAIR,
    )
    _review_route(
        "world_state_digest_matches", False, DISPOSITION_STATE_MISMATCH
    )
    _review_route("world_revision_matches", False, DISPOSITION_REVISION_MISMATCH)
    _review_route(
        "world_storage_persistence_confirmed", False, DISPOSITION_STORAGE_REPAIR
    )
    _review_route(
        "world_postcondition_satisfied", False, DISPOSITION_POSTCONDITION_REPAIR
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
        "realized_dukkha_assessment_adequate", False, DISPOSITION_DUKKHA_REVIEW
    )
    _review_route(
        "world_fact_claimed", True, DISPOSITION_TRUTH_PROMOTION_REJECTED
    )

    replay_context = _context(source, evidence, review)
    replay_context["prior_world_postcondition_verification_intake_session_ids"] = [
        replay_context["world_postcondition_verification_intake_session_id"]
    ]
    replay_context = _redigest_context(source, evidence, review, replay_context)
    _assert_disposition(
        _build(
            source_world_mutation_application_receipt=source,
            world_postcondition_evidence_packet=evidence,
            world_postcondition_verification_review_certificate=review,
            world_postcondition_verification_intake_context=replay_context,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )

    print("PASS: VerifyOS v0.8 WORLD postcondition verification intake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
