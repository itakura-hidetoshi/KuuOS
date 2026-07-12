#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_observed_host_effect_verification_intake_v0_1 import (
    DISPOSITION_ADDITIONAL_OBSERVATION,
    DISPOSITION_CALIBRATION_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_DUKKHA_CONTRADICTED,
    DISPOSITION_EFFECT_CONTRACT_REPAIR,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_SUPPORTED,
    DISPOSITION_WORLD_REFRESH,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATE_AFTER_VERIFIED,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_verifyos_dukkha_preserving_observed_host_effect_verification_intake,
    canonical_digest,
    compute_effect_verification_review_certificate_digest,
    compute_exact_verification_cycle_digest,
    compute_observed_host_effect_verification_bundle_digest,
    compute_requested_verification_operation_digest,
    compute_verification_intake_context_digest,
)
from scripts.check_observeos_dukkha_preserving_external_host_effect_observation_intake_v0_1 import (
    _build as build_observeos_v005_observation,
)


def _source_receipt() -> dict:
    result = build_observeos_v005_observation()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _review(source: dict) -> dict:
    handoff = source["verification_handoff_envelope"]
    certificate = {
        "source_observation_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "observation_record_digest": source["observation_record_digest"],
        "verification_handoff_envelope_digest": source[
            "verification_handoff_envelope_digest"
        ],
        "independent_observation_evidence_packet_digest": source[
            "independent_observation_evidence_packet_digest"
        ],
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(handoff["requested_effect_tags"]),
        "observed_value_digest": handoff["observed_value_digest"],
        "uncertainty_digest": handoff["uncertainty_digest"],
        "calibration_digest": handoff["calibration_digest"],
        "provenance_chain_digests": list(handoff["provenance_chain_digests"]),
        "expected_effect_contract_digest": "verifyos-effect-contract-v007",
        "verification_method_digest": "verifyos-verification-method-v007",
        "verification_evidence_digest": "verifyos-verification-evidence-v007",
        "dukkha_impact_assessment_digest": "verifyos-dukkha-impact-v007",
        "protected_group_impact_assessment_digest": "verifyos-protected-group-impact-v007",
        "future_subject_impact_assessment_digest": "verifyos-future-subject-impact-v007",
        "verifier_id": "verifyos-independent-verifier-v007",
        "verification_started_epoch": 116,
        "verification_completed_epoch": 117,
        "maximum_verification_duration": 4,
        "effect_identity_match": True,
        "evidence_sufficient": True,
        "uncertainty_acceptable": True,
        "calibration_sufficient": True,
        "provenance_complete": True,
        "effect_scope_conformant": True,
        "effect_ceiling_not_exceeded": True,
        "checkpoint_guards_satisfied": True,
        "stop_conditions_satisfied": True,
        "dukkha_preservation_supported": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
    }
    certificate[REVIEW_DIGEST_FIELD] = compute_effect_verification_review_certificate_digest(certificate)
    return certificate


def _redigest_review(source: dict, review: dict) -> dict:
    value = deepcopy(review)
    handoff = source["verification_handoff_envelope"]
    value["source_observation_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["observation_record_digest"] = source["observation_record_digest"]
    value["verification_handoff_envelope_digest"] = source["verification_handoff_envelope_digest"]
    value["independent_observation_evidence_packet_digest"] = source[
        "independent_observation_evidence_packet_digest"
    ]
    value["frontier_materialization_candidate_id"] = source["invoked_frontier_candidate_id"]
    value["frontier_adapter_id"] = source["invoked_frontier_adapter_id"]
    value["frontier_binding_digest"] = source["invoked_frontier_binding_digest"]
    value["requested_effect_tags"] = list(handoff["requested_effect_tags"])
    value["observed_value_digest"] = handoff["observed_value_digest"]
    value["uncertainty_digest"] = handoff["uncertainty_digest"]
    value["calibration_digest"] = handoff["calibration_digest"]
    value["provenance_chain_digests"] = list(handoff["provenance_chain_digests"])
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = compute_effect_verification_review_certificate_digest(value)
    return value


def _context(source: dict, review: dict) -> dict:
    context = {
        "source_observation_receipt_digest": source[SOURCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source["source_world_model_state_digest"],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_observation_receipt_observed_epoch": 117,
        "verification_intake_epoch": 118,
        "maximum_verification_intake_delay": 4,
        "verification_intake_session_id": "verifyos-verification-intake-v007-001",
        "verification_intake_nonce_digest": "verifyos-verification-nonce-v007-001",
        "prior_verification_intake_session_ids": [],
        "prior_verification_review_certificate_digests": [],
        "prior_verification_intake_nonce_digests": [],
        "prior_verified_source_observation_receipt_digests": [],
        "requested_verification_operation_digest": compute_requested_verification_operation_digest(source, review),
        "exact_verification_cycle_digest": "",
    }
    context["exact_verification_cycle_digest"] = compute_exact_verification_cycle_digest(source, review, context)
    context["verification_intake_context_digest"] = compute_verification_intake_context_digest(context)
    return context


def _redigest_context(source: dict, review: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["source_observation_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_verification_operation_digest"] = compute_requested_verification_operation_digest(source, review)
    value["exact_verification_cycle_digest"] = compute_exact_verification_cycle_digest(source, review, value)
    value["verification_intake_context_digest"] = compute_verification_intake_context_digest(value)
    return value


def _build(**overrides):
    source_override = overrides.pop("source_observation_receipt", None)
    source = deepcopy(_source_receipt() if source_override is None else source_override)
    review_override = overrides.pop("effect_verification_review_certificate", None)
    review = deepcopy(_review(source) if review_override is None and source else (review_override or {}))
    context_override = overrides.pop("verification_intake_context", None)
    context = deepcopy(_context(source, review) if context_override is None and source and review else (context_override or {}))
    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v005-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "review-v007-missing")
    context_digest = context.get("verification_intake_context_digest", "context-v007-missing")
    expected_source = overrides.pop("expected_source_observation_receipt_digest", source_digest)
    expected_review = overrides.pop("expected_effect_verification_review_certificate_digest", review_digest)
    expected_context = overrides.pop("expected_verification_intake_context_digest", context_digest)
    policy = overrides.pop("verification_intake_policy_digest", "verifyos-dukkha-preserving-observed-effect-policy-v007")
    owner = overrides.pop("verifyos_verification_responsibility_digest", "verifyos-observed-effect-verification-owner-v007")
    request_id = overrides.pop("verification_intake_request_id", "verifyos-observed-host-effect-verification-v007-001")
    bundle = overrides.pop(
        "observed_host_effect_verification_bundle_digest",
        compute_observed_host_effect_verification_bundle_digest(
            source_observation_receipt_digest=source_digest,
            expected_source_observation_receipt_digest=expected_source,
            observation_record_digest=source.get("observation_record_digest", "observation-record-missing"),
            verification_handoff_envelope_digest=source.get("verification_handoff_envelope_digest", "handoff-missing"),
            effect_verification_review_certificate_digest=review_digest,
            expected_effect_verification_review_certificate_digest=expected_review,
            verification_intake_context_digest=context_digest,
            expected_verification_intake_context_digest=expected_context,
            requested_verification_operation_digest=context.get("requested_verification_operation_digest", "operation-missing"),
            exact_verification_cycle_digest=context.get("exact_verification_cycle_digest", "cycle-missing"),
            verification_intake_policy_digest=policy,
            verifyos_verification_responsibility_digest=owner,
            verification_intake_request_id=request_id,
        ),
    )
    args = {
        "source_observation_receipt": source,
        "expected_source_observation_receipt_digest": expected_source,
        "effect_verification_review_certificate": review,
        "expected_effect_verification_review_certificate_digest": expected_review,
        "verification_intake_context": context,
        "expected_verification_intake_context_digest": expected_context,
        "verification_intake_policy_digest": policy,
        "verifyos_verification_responsibility_digest": owner,
        "verification_intake_request_id": request_id,
        "observed_host_effect_verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_dukkha_preserving_observed_host_effect_verification_intake(**args)


def _assert_blocked(result, blocker: str) -> None:
    assert result.status == STATUS_BLOCKED
    assert result.receipt is None
    assert blocker in result.blockers, result.blockers


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["verification_disposition"] == disposition
    return result.receipt


def main() -> int:
    supported = _assert_disposition(_build(), DISPOSITION_SUPPORTED)
    assert supported["verification_state_before"] == STATE_BEFORE
    assert supported["verification_state_after"] == STATE_AFTER_VERIFIED
    assert supported["verification_completed"] is True
    assert supported["verification_debt_consumed"] is True
    assert supported["verification_debt_open"] is False
    assert supported["effect_conformance_verified"] is True
    assert supported["world_disposition_intake_admitted"] is True
    assert supported["persistent_world_model_state_unchanged"] is True
    assert supported["world_fact_confirmed"] is False
    assert supported["causal_attribution_confirmed"] is False
    assert supported["dukkha_reduction_realized_confirmed"] is False
    assert supported["tool_invocation_performed"] is False
    assert supported["external_side_effect_performed"] is False
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {k: v for k, v in supported.items() if k != RECEIPT_DIGEST_FIELD}
    )

    _assert_blocked(_build(source_observation_receipt={}), "source_observation_receipt_missing")
    _assert_blocked(_build(effect_verification_review_certificate={}), "effect_verification_review_certificate_missing")
    _assert_blocked(_build(verification_intake_context={}), "verification_intake_context_missing")
    _assert_blocked(_build(expected_source_observation_receipt_digest="wrong-source"), "source_observation_expected_binding_mismatch")
    _assert_blocked(_build(expected_effect_verification_review_certificate_digest="wrong-review"), "effect_verification_review_expected_binding_mismatch")
    _assert_blocked(_build(expected_verification_intake_context_digest="wrong-context"), "verification_intake_context_expected_binding_mismatch")

    source = _source_receipt()
    source["verification_completed"] = True
    source = _redigest_source(source)
    _assert_blocked(_build(source_observation_receipt=source), "source_boundary_verification_completed_promoted")

    source = _source_receipt()
    review = _review(source)
    review["world_fact_claimed"] = True
    review = _redigest_review(source, review)
    _assert_blocked(
        _build(source_observation_receipt=source, effect_verification_review_certificate=review),
        "effect_verification_review_world_fact_claimed_mismatch",
    )

    review = _review(source)
    context = _context(source, review)
    context["current_world_model_revision"] += 1
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(source_observation_receipt=source, effect_verification_review_certificate=review, verification_intake_context=context),
        DISPOSITION_WORLD_REFRESH,
    )

    context = _context(source, review)
    context["verification_intake_epoch"] = 130
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(source_observation_receipt=source, effect_verification_review_certificate=review, verification_intake_context=context),
        DISPOSITION_CONTEXT_REFRESH,
    )

    review = _review(source)
    review["verification_completed_epoch"] = 130
    review = _redigest_review(source, review)
    _assert_disposition(
        _build(source_observation_receipt=source, effect_verification_review_certificate=review),
        DISPOSITION_REVIEW_REFRESH,
    )

    for field, disposition in (
        ("evidence_sufficient", DISPOSITION_ADDITIONAL_OBSERVATION),
        ("calibration_sufficient", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_complete", DISPOSITION_PROVENANCE_REPAIR),
        ("effect_scope_conformant", DISPOSITION_EFFECT_CONTRACT_REPAIR),
        ("protected_group_nonexternalization_supported", DISPOSITION_NONEXTERNALIZATION_REVIEW),
        ("dukkha_preservation_supported", DISPOSITION_DUKKHA_CONTRADICTED),
    ):
        review = _review(source)
        review[field] = False
        review = _redigest_review(source, review)
        receipt = _assert_disposition(
            _build(source_observation_receipt=source, effect_verification_review_certificate=review),
            disposition,
        )
        assert receipt["verification_state_after"] == STATE_BEFORE
        assert receipt["verification_completed"] is False
        assert receipt["verification_debt_open"] is True
        assert receipt["world_disposition_intake_admitted"] is False

    review = _review(source)
    context = _context(source, review)
    context["prior_verification_intake_session_ids"] = [context["verification_intake_session_id"]]
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(source_observation_receipt=source, effect_verification_review_certificate=review, verification_intake_context=context),
        DISPOSITION_REPLAY_REJECTED,
    )

    _assert_blocked(
        _build(observed_host_effect_verification_bundle_digest="wrong-bundle"),
        "observed_host_effect_verification_bundle_digest_mismatch",
    )

    print("VerifyOS dukkha-preserving observed host-effect verification intake v0.1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
