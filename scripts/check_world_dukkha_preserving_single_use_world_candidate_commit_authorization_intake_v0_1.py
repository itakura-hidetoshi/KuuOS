#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_CANDIDATE_REVALIDATION,
    DISPOSITION_COMPENSATION_REPAIR,
    DISPOSITION_CONTEXT_REFRESH,
    DISPOSITION_DUKKHA_REVIEW,
    DISPOSITION_EXPIRED,
    DISPOSITION_NONEXTERNALIZATION_REVIEW,
    DISPOSITION_OWNER_REJECTED,
    DISPOSITION_PATCH_REPAIR,
    DISPOSITION_POSTCONDITION_REPAIR,
    DISPOSITION_PRECONDITION_REPAIR,
    DISPOSITION_PROVENANCE_REPAIR,
    DISPOSITION_READY,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_TRUTH_PROMOTION_REJECTED,
    DISPOSITION_WORLD_REFRESH,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_READY,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake,
    canonical_digest,
    compute_exact_world_candidate_commit_authorization_cycle_digest,
    compute_requested_world_candidate_commit_authorization_operation_digest,
    compute_world_candidate_commit_authorization_bundle_digest,
    compute_world_candidate_commit_authorization_intake_context_digest,
    compute_world_candidate_commit_authorization_review_certificate_digest,
)
from scripts.check_world_dukkha_preserving_verified_host_effect_disposition_intake_v0_1 import (
    _build as build_world_v060_disposition,
)


def _source_receipt() -> dict:
    result = build_world_v060_disposition()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["world_disposition"] == "world_candidate_admission_ready"
    assert result.receipt["world_candidate_prepared"] is True
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _review(source: dict) -> dict:
    candidate = source["world_candidate_envelope"]
    review = {
        "source_world_disposition_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "world_disposition_record_digest": source["world_disposition_record_digest"],
        "world_candidate_envelope_digest": source["world_candidate_envelope_digest"],
        SOURCE_REVIEW_DIGEST_FIELD: source[SOURCE_REVIEW_DIGEST_FIELD],
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(candidate["requested_effect_tags"]),
        "observed_value_digest": candidate["observed_value_digest"],
        "uncertainty_digest": candidate["uncertainty_digest"],
        "calibration_digest": candidate["calibration_digest"],
        "provenance_chain_digests": list(candidate["provenance_chain_digests"]),
        "world_candidate_fact_digest": candidate["world_candidate_fact_digest"],
        "world_candidate_relation_digest": candidate["world_candidate_relation_digest"],
        "world_update_patch_digest": candidate["world_update_patch_digest"],
        "world_update_precondition_digest": candidate["world_update_precondition_digest"],
        "world_update_postcondition_digest": candidate["world_update_postcondition_digest"],
        "causal_model_claim_digest": candidate["causal_model_claim_digest"],
        "realized_dukkha_assessment_digest": candidate["realized_dukkha_assessment_digest"],
        "protected_group_realized_impact_digest": "world-protected-group-realized-impact-v061-001",
        "future_subject_realized_impact_digest": "world-future-subject-realized-impact-v061-001",
        "authorization_scope_digest": "world-commit-authorization-scope-v061-001",
        "authorization_constraints_digest": "world-commit-authorization-constraints-v061-001",
        "world_mutation_application_policy_digest": "world-mutation-application-policy-v061-001",
        "rollback_route_digest": "world-rollback-route-v061-001",
        "compensation_route_digest": "world-compensation-route-v061-001",
        "authorization_owner_id": "world-commit-authorization-owner-v061",
        "authorization_review_started_epoch": 122,
        "authorization_review_completed_epoch": 123,
        "maximum_authorization_review_duration": 4,
        "authorization_expiry_epoch": 127,
        "source_world_candidate_prepared": True,
        "candidate_identity_match": True,
        "world_patch_scope_authorizable": True,
        "world_patch_ceiling_not_exceeded": True,
        "world_preconditions_satisfied": True,
        "world_postconditions_verifiable": True,
        "lineage_continuity_preserved": True,
        "responsibility_continuity_preserved": True,
        "authorization_owner_confirmed": True,
        "single_use_authorization_supported": True,
        "dukkha_preservation_supported": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "compensation_route_ready": True,
        "no_causal_overclaim": True,
        "no_realized_dukkha_overclaim": True,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
        "world_mutation_performed": False,
    }
    review[REVIEW_DIGEST_FIELD] = (
        compute_world_candidate_commit_authorization_review_certificate_digest(review)
    )
    return review


def _redigest_review(source: dict, review: dict) -> dict:
    value = deepcopy(review)
    candidate = source["world_candidate_envelope"]
    value["source_world_disposition_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["world_disposition_record_digest"] = source["world_disposition_record_digest"]
    value["world_candidate_envelope_digest"] = source["world_candidate_envelope_digest"]
    value[SOURCE_REVIEW_DIGEST_FIELD] = source[SOURCE_REVIEW_DIGEST_FIELD]
    value["frontier_materialization_candidate_id"] = source["invoked_frontier_candidate_id"]
    value["frontier_adapter_id"] = source["invoked_frontier_adapter_id"]
    value["frontier_binding_digest"] = source["invoked_frontier_binding_digest"]
    for field in ("requested_effect_tags", "provenance_chain_digests"):
        value[field] = list(candidate[field])
    for field in (
        "observed_value_digest",
        "uncertainty_digest",
        "calibration_digest",
        "world_candidate_fact_digest",
        "world_candidate_relation_digest",
        "world_update_patch_digest",
        "world_update_precondition_digest",
        "world_update_postcondition_digest",
        "causal_model_claim_digest",
        "realized_dukkha_assessment_digest",
    ):
        value[field] = candidate[field]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_world_candidate_commit_authorization_review_certificate_digest(value)
    )
    return value


def _context(source: dict, review: dict) -> dict:
    context = {
        "source_world_disposition_receipt_digest": source[SOURCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source["source_world_model_state_digest"],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_world_candidate_prepared_epoch": 121,
        "world_commit_authorization_intake_epoch": 124,
        "maximum_world_commit_authorization_intake_delay": 4,
        "world_commit_authorization_intake_session_id": "world-commit-authorization-intake-v061-001",
        "world_commit_authorization_intake_nonce_digest": "world-commit-authorization-nonce-v061-001",
        "prior_world_commit_authorization_intake_session_ids": [],
        "prior_world_candidate_commit_authorization_review_certificate_digests": [],
        "prior_world_commit_authorization_intake_nonce_digests": [],
        "prior_authorized_world_candidate_envelope_digests": [],
        "requested_world_candidate_commit_authorization_operation_digest": compute_requested_world_candidate_commit_authorization_operation_digest(
            source, review
        ),
        "exact_world_candidate_commit_authorization_cycle_digest": "",
    }
    context["exact_world_candidate_commit_authorization_cycle_digest"] = (
        compute_exact_world_candidate_commit_authorization_cycle_digest(
            source, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = (
        compute_world_candidate_commit_authorization_intake_context_digest(context)
    )
    return context


def _redigest_context(source: dict, review: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["source_world_disposition_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_candidate_commit_authorization_operation_digest"] = (
        compute_requested_world_candidate_commit_authorization_operation_digest(
            source, review
        )
    )
    value["exact_world_candidate_commit_authorization_cycle_digest"] = (
        compute_exact_world_candidate_commit_authorization_cycle_digest(
            source, review, value
        )
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_world_candidate_commit_authorization_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    source_override = overrides.pop("source_world_disposition_receipt", None)
    source = deepcopy(_source_receipt() if source_override is None else source_override)
    review_override = overrides.pop(
        "world_candidate_commit_authorization_review_certificate", None
    )
    review = deepcopy(
        _review(source) if review_override is None and source else (review_override or {})
    )
    context_override = overrides.pop(
        "world_candidate_commit_authorization_intake_context", None
    )
    context = deepcopy(
        _context(source, review)
        if context_override is None and source and review
        else (context_override or {})
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v060-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "review-v061-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "context-v061-missing")
    expected_source = overrides.pop(
        "expected_source_world_disposition_receipt_digest", source_digest
    )
    expected_review = overrides.pop(
        "expected_world_candidate_commit_authorization_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_world_candidate_commit_authorization_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "world_candidate_commit_authorization_policy_digest",
        "world-dukkha-preserving-single-use-commit-authorization-policy-v061",
    )
    owner = overrides.pop(
        "world_candidate_commit_authorization_responsibility_digest",
        "world-single-use-commit-authorization-owner-v061",
    )
    request_id = overrides.pop(
        "world_candidate_commit_authorization_request_id",
        "world-candidate-commit-authorization-v061-001",
    )
    bundle = overrides.pop(
        "world_candidate_commit_authorization_bundle_digest",
        compute_world_candidate_commit_authorization_bundle_digest(
            source_world_disposition_receipt_digest=source_digest,
            expected_source_world_disposition_receipt_digest=expected_source,
            world_disposition_record_digest=source.get(
                "world_disposition_record_digest", "world-disposition-record-missing"
            ),
            world_candidate_envelope_digest=source.get(
                "world_candidate_envelope_digest", "world-candidate-envelope-missing"
            ),
            world_candidate_commit_authorization_review_certificate_digest=review_digest,
            expected_world_candidate_commit_authorization_review_certificate_digest=expected_review,
            world_candidate_commit_authorization_intake_context_digest=context_digest,
            expected_world_candidate_commit_authorization_intake_context_digest=expected_context,
            requested_world_candidate_commit_authorization_operation_digest=context.get(
                "requested_world_candidate_commit_authorization_operation_digest",
                "operation-missing",
            ),
            exact_world_candidate_commit_authorization_cycle_digest=context.get(
                "exact_world_candidate_commit_authorization_cycle_digest",
                "cycle-missing",
            ),
            world_candidate_commit_authorization_policy_digest=policy,
            world_candidate_commit_authorization_responsibility_digest=owner,
            world_candidate_commit_authorization_request_id=request_id,
        ),
    )
    args = {
        "source_world_disposition_receipt": source,
        "expected_source_world_disposition_receipt_digest": expected_source,
        "world_candidate_commit_authorization_review_certificate": review,
        "expected_world_candidate_commit_authorization_review_certificate_digest": expected_review,
        "world_candidate_commit_authorization_intake_context": context,
        "expected_world_candidate_commit_authorization_intake_context_digest": expected_context,
        "world_candidate_commit_authorization_policy_digest": policy,
        "world_candidate_commit_authorization_responsibility_digest": owner,
        "world_candidate_commit_authorization_request_id": request_id,
        "world_candidate_commit_authorization_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake(
        **args
    )


def _assert_blocked(result, blocker: str) -> None:
    assert result.status == STATUS_BLOCKED
    assert result.receipt is None
    assert blocker in result.blockers, result.blockers


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["world_candidate_commit_authorization_disposition"] == disposition
    assert result.receipt["world_version"] == "v0.61"
    return result.receipt


def main() -> int:
    ready = _assert_disposition(_build(), DISPOSITION_READY)
    assert ready["world_candidate_commit_authorization_state_before"] == STATE_BEFORE
    assert ready["world_candidate_commit_authorization_state_after"] == STATE_AFTER_READY
    assert ready["world_candidate_commit_authorization_granted"] is True
    assert ready["single_use_world_candidate_commit_authorization_granted"] is True
    assert ready["world_candidate_commit_authorization_debt_consumed"] is True
    assert ready["world_candidate_commit_authorization_debt_open"] is False
    assert ready["world_mutation_application_intake_admitted"] is True
    assert ready["world_mutation_application_completed"] is False
    assert ready["world_candidate_commit_completed"] is False
    assert ready["persistent_world_model_state_unchanged"] is True
    assert ready["world_fact_confirmed"] is False
    assert ready["causal_attribution_confirmed"] is False
    assert ready["dukkha_reduction_realized_confirmed"] is False
    assert ready["tool_invocation_performed"] is False
    assert ready["external_side_effect_performed"] is False
    assert ready["world_mutation_authority_granted"] is False
    assert (
        ready["world_mutation_application_handoff_envelope"]["authorization_state"]
        == "authorized_single_use_not_applied"
    )
    assert ready[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in ready.items() if key != RECEIPT_DIGEST_FIELD}
    )

    _assert_blocked(
        _build(source_world_disposition_receipt={}),
        "source_world_disposition_receipt_missing",
    )
    _assert_blocked(
        _build(world_candidate_commit_authorization_review_certificate={}),
        "world_candidate_commit_authorization_review_certificate_missing",
    )
    _assert_blocked(
        _build(world_candidate_commit_authorization_intake_context={}),
        "world_candidate_commit_authorization_intake_context_missing",
    )
    _assert_blocked(
        _build(expected_source_world_disposition_receipt_digest="wrong-source"),
        "source_world_disposition_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(
            expected_world_candidate_commit_authorization_review_certificate_digest="wrong-review"
        ),
        "world_candidate_commit_authorization_review_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(
            expected_world_candidate_commit_authorization_intake_context_digest="wrong-context"
        ),
        "world_candidate_commit_authorization_intake_context_expected_binding_mismatch",
    )

    source = _source_receipt()
    source["world_commit_authorization_completed"] = True
    source = _redigest_source(source)
    _assert_blocked(
        _build(source_world_disposition_receipt=source),
        "source_boundary_world_commit_authorization_completed_promoted",
    )

    source = _source_receipt()
    source["world_candidate_envelope"]["world_candidate_state"] = "committed"
    source["world_candidate_envelope_digest"] = canonical_digest(
        source["world_candidate_envelope"]
    )
    source = _redigest_source(source)
    _assert_blocked(
        _build(source_world_disposition_receipt=source),
        "source_world_candidate_world_candidate_state_mismatch",
    )

    source = _source_receipt()
    review = _review(source)
    context = _context(source, review)
    context["current_world_model_revision"] += 1
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(
            source_world_disposition_receipt=source,
            world_candidate_commit_authorization_review_certificate=review,
            world_candidate_commit_authorization_intake_context=context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )

    context = _context(source, review)
    context["world_commit_authorization_intake_epoch"] = 140
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(
            source_world_disposition_receipt=source,
            world_candidate_commit_authorization_review_certificate=review,
            world_candidate_commit_authorization_intake_context=context,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    review = _review(source)
    review["authorization_review_completed_epoch"] = 130
    review["authorization_expiry_epoch"] = 132
    review = _redigest_review(source, review)
    _assert_disposition(
        _build(
            source_world_disposition_receipt=source,
            world_candidate_commit_authorization_review_certificate=review,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    review = _review(source)
    review["authorization_expiry_epoch"] = 123
    review = _redigest_review(source, review)
    context = _context(source, review)
    context["world_commit_authorization_intake_epoch"] = 124
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(
            source_world_disposition_receipt=source,
            world_candidate_commit_authorization_review_certificate=review,
            world_candidate_commit_authorization_intake_context=context,
        ),
        DISPOSITION_EXPIRED,
    )

    for field, disposition in (
        ("world_fact_claimed", DISPOSITION_TRUTH_PROMOTION_REJECTED),
        ("authorization_owner_confirmed", DISPOSITION_OWNER_REJECTED),
        ("candidate_identity_match", DISPOSITION_CANDIDATE_REVALIDATION),
        ("world_patch_scope_authorizable", DISPOSITION_PATCH_REPAIR),
        ("world_preconditions_satisfied", DISPOSITION_PRECONDITION_REPAIR),
        ("world_postconditions_verifiable", DISPOSITION_POSTCONDITION_REPAIR),
        ("lineage_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
        (
            "protected_group_nonexternalization_supported",
            DISPOSITION_NONEXTERNALIZATION_REVIEW,
        ),
        ("dukkha_preservation_supported", DISPOSITION_DUKKHA_REVIEW),
        ("compensation_route_ready", DISPOSITION_COMPENSATION_REPAIR),
    ):
        review = _review(source)
        review[field] = not review[field]
        review = _redigest_review(source, review)
        _assert_disposition(
            _build(
                source_world_disposition_receipt=source,
                world_candidate_commit_authorization_review_certificate=review,
            ),
            disposition,
        )

    review = _review(source)
    context = _context(source, review)
    context["prior_authorized_world_candidate_envelope_digests"] = [
        source["world_candidate_envelope_digest"]
    ]
    context = _redigest_context(source, review, context)
    replay = _assert_disposition(
        _build(
            source_world_disposition_receipt=source,
            world_candidate_commit_authorization_review_certificate=review,
            world_candidate_commit_authorization_intake_context=context,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )
    assert replay["world_candidate_commit_authorization_granted"] is False
    assert replay["world_candidate_commit_authorization_debt_open"] is True
    assert replay["world_mutation_application_intake_admitted"] is False
    assert replay["world_mutation_application_handoff_envelope"] is None
    assert replay["world_candidate_commit_authorization_state_after"] == STATE_BEFORE

    print(
        "PASS: WORLD v0.61 dukkha-preserving single-use world-candidate "
        "commit authorization intake"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
