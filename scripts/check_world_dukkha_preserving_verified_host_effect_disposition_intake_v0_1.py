#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_world_dukkha_preserving_verified_host_effect_disposition_intake_v0_1 import (
    DISPOSITION_ADDITIONAL_OBSERVATION,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_DUKKHA_REALIZATION_REVIEW,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_READY,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_TRUTH_PROMOTION_REJECTED,
    DISPOSITION_VERIFICATION_REPAIR,
    DISPOSITION_WORLD_PATCH_REPAIR,
    DISPOSITION_WORLD_REFRESH,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_READY,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_world_dukkha_preserving_verified_host_effect_disposition_intake,
    canonical_digest,
    compute_exact_world_disposition_cycle_digest,
    compute_requested_world_disposition_operation_digest,
    compute_verified_host_effect_world_disposition_bundle_digest,
    compute_world_disposition_intake_context_digest,
    compute_world_disposition_review_certificate_digest,
)
from scripts.check_verifyos_dukkha_preserving_observed_host_effect_verification_intake_v0_1 import (
    _build as build_verifyos_v007_verification,
)


def _source_receipt() -> dict:
    result = build_verifyos_v007_verification()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["verification_disposition"] == "effect_verification_supported"
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _review(source: dict) -> dict:
    handoff = source["world_disposition_handoff_envelope"]
    review = {
        "source_verification_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "verification_record_digest": source["verification_record_digest"],
        "world_disposition_handoff_envelope_digest": source[
            "world_disposition_handoff_envelope_digest"
        ],
        SOURCE_REVIEW_DIGEST_FIELD: source[SOURCE_REVIEW_DIGEST_FIELD],
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(handoff["requested_effect_tags"]),
        "observed_value_digest": handoff["observed_value_digest"],
        "uncertainty_digest": handoff["uncertainty_digest"],
        "calibration_digest": handoff["calibration_digest"],
        "provenance_chain_digests": list(handoff["provenance_chain_digests"]),
        "world_candidate_fact_digest": "world-candidate-fact-v060-001",
        "world_candidate_relation_digest": "world-candidate-relation-v060-001",
        "world_update_patch_digest": "world-update-patch-v060-001",
        "world_update_precondition_digest": "world-update-precondition-v060-001",
        "world_update_postcondition_digest": "world-update-postcondition-v060-001",
        "causal_model_claim_digest": "world-causal-model-claim-v060-001",
        "realized_dukkha_assessment_digest": "world-realized-dukkha-assessment-v060-001",
        "protected_group_realized_impact_digest": "world-protected-group-impact-v060-001",
        "future_subject_realized_impact_digest": "world-future-subject-impact-v060-001",
        "world_disposition_reviewer_id": "world-independent-disposition-reviewer-v060",
        "world_disposition_review_started_epoch": 119,
        "world_disposition_review_completed_epoch": 120,
        "maximum_world_disposition_review_duration": 4,
        "source_verification_supported": True,
        "evidence_sufficient_for_world_candidate": True,
        "uncertainty_acceptable_for_world_candidate": True,
        "calibration_sufficient": True,
        "provenance_complete": True,
        "effect_identity_match": True,
        "world_patch_scope_conformant": True,
        "world_patch_ceiling_not_exceeded": True,
        "lineage_continuity_preserved": True,
        "responsibility_continuity_preserved": True,
        "dukkha_realization_assessment_sufficient": True,
        "no_causal_overclaim": True,
        "no_realized_dukkha_overclaim": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "compensation_route_ready": True,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    review[REVIEW_DIGEST_FIELD] = compute_world_disposition_review_certificate_digest(review)
    return review


def _redigest_review(source: dict, review: dict) -> dict:
    value = deepcopy(review)
    handoff = source["world_disposition_handoff_envelope"]
    value["source_verification_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["verification_record_digest"] = source["verification_record_digest"]
    value["world_disposition_handoff_envelope_digest"] = source[
        "world_disposition_handoff_envelope_digest"
    ]
    value[SOURCE_REVIEW_DIGEST_FIELD] = source[SOURCE_REVIEW_DIGEST_FIELD]
    value["frontier_materialization_candidate_id"] = source["invoked_frontier_candidate_id"]
    value["frontier_adapter_id"] = source["invoked_frontier_adapter_id"]
    value["frontier_binding_digest"] = source["invoked_frontier_binding_digest"]
    value["requested_effect_tags"] = list(handoff["requested_effect_tags"])
    value["observed_value_digest"] = handoff["observed_value_digest"]
    value["uncertainty_digest"] = handoff["uncertainty_digest"]
    value["calibration_digest"] = handoff["calibration_digest"]
    value["provenance_chain_digests"] = list(handoff["provenance_chain_digests"])
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = compute_world_disposition_review_certificate_digest(value)
    return value


def _context(source: dict, review: dict) -> dict:
    context = {
        "source_verification_receipt_digest": source[SOURCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source["source_world_model_state_digest"],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_verification_receipt_verified_epoch": 120,
        "world_disposition_intake_epoch": 121,
        "maximum_world_disposition_intake_delay": 4,
        "world_disposition_intake_session_id": "world-disposition-intake-v060-001",
        "world_disposition_intake_nonce_digest": "world-disposition-nonce-v060-001",
        "prior_world_disposition_intake_session_ids": [],
        "prior_world_disposition_review_certificate_digests": [],
        "prior_world_disposition_intake_nonce_digests": [],
        "prior_disposed_source_verification_receipt_digests": [],
        "requested_world_disposition_operation_digest": compute_requested_world_disposition_operation_digest(
            source, review
        ),
        "exact_world_disposition_cycle_digest": "",
    }
    context["exact_world_disposition_cycle_digest"] = compute_exact_world_disposition_cycle_digest(
        source, review, context
    )
    context["world_disposition_intake_context_digest"] = compute_world_disposition_intake_context_digest(
        context
    )
    return context


def _redigest_context(source: dict, review: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["source_verification_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_disposition_operation_digest"] = compute_requested_world_disposition_operation_digest(
        source, review
    )
    value["exact_world_disposition_cycle_digest"] = compute_exact_world_disposition_cycle_digest(
        source, review, value
    )
    value["world_disposition_intake_context_digest"] = compute_world_disposition_intake_context_digest(
        value
    )
    return value


def _build(**overrides):
    source_override = overrides.pop("source_verification_receipt", None)
    source = deepcopy(_source_receipt() if source_override is None else source_override)
    review_override = overrides.pop("world_disposition_review_certificate", None)
    review = deepcopy(_review(source) if review_override is None and source else (review_override or {}))
    context_override = overrides.pop("world_disposition_intake_context", None)
    context = deepcopy(_context(source, review) if context_override is None and source and review else (context_override or {}))

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v007-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "review-v060-missing")
    context_digest = context.get("world_disposition_intake_context_digest", "context-v060-missing")
    expected_source = overrides.pop("expected_source_verification_receipt_digest", source_digest)
    expected_review = overrides.pop(
        "expected_world_disposition_review_certificate_digest", review_digest
    )
    expected_context = overrides.pop(
        "expected_world_disposition_intake_context_digest", context_digest
    )
    policy = overrides.pop(
        "world_disposition_intake_policy_digest",
        "world-dukkha-preserving-verified-effect-disposition-policy-v060",
    )
    owner = overrides.pop(
        "world_disposition_responsibility_digest",
        "world-verified-effect-disposition-owner-v060",
    )
    request_id = overrides.pop(
        "world_disposition_request_id",
        "world-verified-host-effect-disposition-v060-001",
    )
    bundle = overrides.pop(
        "verified_host_effect_world_disposition_bundle_digest",
        compute_verified_host_effect_world_disposition_bundle_digest(
            source_verification_receipt_digest=source_digest,
            expected_source_verification_receipt_digest=expected_source,
            verification_record_digest=source.get("verification_record_digest", "verification-record-missing"),
            world_disposition_handoff_envelope_digest=source.get(
                "world_disposition_handoff_envelope_digest", "handoff-missing"
            ),
            world_disposition_review_certificate_digest=review_digest,
            expected_world_disposition_review_certificate_digest=expected_review,
            world_disposition_intake_context_digest=context_digest,
            expected_world_disposition_intake_context_digest=expected_context,
            requested_world_disposition_operation_digest=context.get(
                "requested_world_disposition_operation_digest", "operation-missing"
            ),
            exact_world_disposition_cycle_digest=context.get(
                "exact_world_disposition_cycle_digest", "cycle-missing"
            ),
            world_disposition_intake_policy_digest=policy,
            world_disposition_responsibility_digest=owner,
            world_disposition_request_id=request_id,
        ),
    )
    args = {
        "source_verification_receipt": source,
        "expected_source_verification_receipt_digest": expected_source,
        "world_disposition_review_certificate": review,
        "expected_world_disposition_review_certificate_digest": expected_review,
        "world_disposition_intake_context": context,
        "expected_world_disposition_intake_context_digest": expected_context,
        "world_disposition_intake_policy_digest": policy,
        "world_disposition_responsibility_digest": owner,
        "world_disposition_request_id": request_id,
        "verified_host_effect_world_disposition_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_world_dukkha_preserving_verified_host_effect_disposition_intake(**args)


def _assert_blocked(result, blocker: str) -> None:
    assert result.status == STATUS_BLOCKED
    assert result.receipt is None
    assert blocker in result.blockers, result.blockers


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["world_disposition"] == disposition
    return result.receipt


def _assert_nonready(receipt: dict) -> None:
    assert receipt["world_version"] == "v0.60"
    assert receipt["world_disposition_state_before"] == STATE_BEFORE
    assert receipt["world_disposition_state_after"] == STATE_BEFORE
    assert receipt["world_candidate_prepared"] is False
    assert receipt["exactly_one_world_candidate_prepared"] is False
    assert receipt["world_disposition_debt_consumed"] is False
    assert receipt["world_disposition_debt_open"] is True
    assert receipt["source_verification_receipt_replay_closed"] is False
    assert receipt["world_candidate_envelope"] is None
    assert receipt["world_candidate_envelope_digest"] == ""
    assert receipt["world_commit_authorization_intake_admitted"] is False
    assert receipt["persistent_world_model_state_unchanged"] is True
    assert receipt["world_fact_confirmed"] is False
    assert receipt["causal_attribution_confirmed"] is False
    assert receipt["dukkha_reduction_realized_confirmed"] is False


def main() -> int:
    ready = _assert_disposition(_build(), DISPOSITION_READY)
    assert ready["world_version"] == "v0.60"
    assert ready["world_disposition_state_before"] == STATE_BEFORE
    assert ready["world_disposition_state_after"] == STATE_AFTER_READY
    assert ready["world_candidate_prepared"] is True
    assert ready["exactly_one_world_candidate_prepared"] is True
    assert ready["world_disposition_debt_consumed"] is True
    assert ready["world_disposition_debt_open"] is False
    assert ready["source_verification_receipt_replay_closed"] is True
    assert ready["world_commit_authorization_intake_admitted"] is True
    assert ready["world_commit_authorization_completed"] is False
    assert ready["persistent_world_model_state_unchanged"] is True
    assert ready["world_fact_confirmed"] is False
    assert ready["causal_attribution_confirmed"] is False
    assert ready["dukkha_reduction_realized_confirmed"] is False
    assert ready["tool_invocation_performed"] is False
    assert ready["external_side_effect_performed"] is False
    candidate = ready["world_candidate_envelope"]
    assert candidate["world_candidate_state"] == "prepared_not_committed"
    assert candidate["world_fact_state"] == "candidate_only_not_fact"
    assert candidate["world_commit_authorization_intake_admitted"] is True
    assert ready[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in ready.items() if key != RECEIPT_DIGEST_FIELD}
    )

    _assert_blocked(_build(source_verification_receipt={}), "source_verification_receipt_missing")
    _assert_blocked(
        _build(world_disposition_review_certificate={}),
        "world_disposition_review_certificate_missing",
    )
    _assert_blocked(
        _build(world_disposition_intake_context={}),
        "world_disposition_intake_context_missing",
    )
    _assert_blocked(
        _build(expected_source_verification_receipt_digest="wrong-source"),
        "source_verification_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(expected_world_disposition_review_certificate_digest="wrong-review"),
        "world_disposition_review_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(expected_world_disposition_intake_context_digest="wrong-context"),
        "world_disposition_intake_context_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(verified_host_effect_world_disposition_bundle_digest="wrong-bundle"),
        "verified_host_effect_world_disposition_bundle_digest_mismatch",
    )

    source = _source_receipt()
    source["world_fact_confirmed"] = True
    source = _redigest_source(source)
    _assert_blocked(
        _build(source_verification_receipt=source),
        "source_boundary_world_fact_confirmed_promoted",
    )

    source = _source_receipt()
    review = _review(source)
    context = _context(source, review)
    context["current_world_model_revision"] += 1
    context = _redigest_context(source, review, context)
    receipt = _assert_disposition(
        _build(
            source_verification_receipt=source,
            world_disposition_review_certificate=review,
            world_disposition_intake_context=context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )
    _assert_nonready(receipt)

    context = _context(source, review)
    context["world_disposition_intake_epoch"] = 140
    context = _redigest_context(source, review, context)
    _assert_nonready(
        _assert_disposition(
            _build(
                source_verification_receipt=source,
                world_disposition_review_certificate=review,
                world_disposition_intake_context=context,
            ),
            DISPOSITION_CONTEXT_REFRESH,
        )
    )

    review = _review(source)
    review["world_disposition_review_completed_epoch"] = 140
    review = _redigest_review(source, review)
    _assert_nonready(
        _assert_disposition(
            _build(
                source_verification_receipt=source,
                world_disposition_review_certificate=review,
            ),
            DISPOSITION_REVIEW_REFRESH,
        )
    )

    for field, disposition in (
        ("evidence_sufficient_for_world_candidate", DISPOSITION_ADDITIONAL_OBSERVATION),
        ("source_verification_supported", DISPOSITION_VERIFICATION_REPAIR),
        ("calibration_sufficient", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_complete", DISPOSITION_PROVENANCE_REPAIR),
        ("world_patch_scope_conformant", DISPOSITION_WORLD_PATCH_REPAIR),
        (
            "protected_group_nonexternalization_supported",
            DISPOSITION_NONEXTERNALIZATION_REVIEW,
        ),
        (
            "dukkha_realization_assessment_sufficient",
            DISPOSITION_DUKKHA_REALIZATION_REVIEW,
        ),
        ("world_fact_claimed", DISPOSITION_TRUTH_PROMOTION_REJECTED),
    ):
        review = _review(source)
        review[field] = True if field == "world_fact_claimed" else False
        review = _redigest_review(source, review)
        _assert_nonready(
            _assert_disposition(
                _build(
                    source_verification_receipt=source,
                    world_disposition_review_certificate=review,
                ),
                disposition,
            )
        )

    review = _review(source)
    context = _context(source, review)
    context["prior_world_disposition_intake_session_ids"] = [
        context["world_disposition_intake_session_id"]
    ]
    context = _redigest_context(source, review, context)
    _assert_nonready(
        _assert_disposition(
            _build(
                source_verification_receipt=source,
                world_disposition_review_certificate=review,
                world_disposition_intake_context=context,
            ),
            DISPOSITION_REPLAY_REJECTED,
        )
    )

    print(
        "PASS: WORLD v0.60 dukkha-preserving verified host-effect disposition "
        "intake validates ready, refresh, repair, review, truth-rejection, replay, "
        "and fail-closed paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
