#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_world_dukkha_preserving_single_use_world_mutation_application_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ATOMICITY_REPAIR,
    DISPOSITION_AUTHORIZATION_REVALIDATION,
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
    DISPOSITION_REVISION_REPAIR,
    DISPOSITION_STORAGE_REPAIR,
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
    build_world_dukkha_preserving_single_use_world_mutation_application_intake,
    canonical_digest,
    compute_exact_world_mutation_application_cycle_digest,
    compute_requested_world_mutation_application_operation_digest,
    compute_world_mutation_application_bundle_digest,
    compute_world_mutation_application_intake_context_digest,
    compute_world_mutation_application_review_certificate_digest,
)
from scripts.check_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1 import (
    _build as build_world_v061_authorization,
)


def _source_receipt() -> dict:
    result = build_world_v061_authorization()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert (
        result.receipt["world_candidate_commit_authorization_disposition"]
        == "world_candidate_commit_authorization_ready"
    )
    assert (
        result.receipt["world_candidate_commit_authorization_state_after"]
        == STATE_BEFORE
    )
    assert (
        result.receipt["single_use_world_candidate_commit_authorization_granted"]
        is True
    )
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _review(source: dict) -> dict:
    handoff = source["world_mutation_application_handoff_envelope"]
    before_revision = source["source_world_model_revision"]
    after_revision = before_revision + 1
    after_state = canonical_digest(
        {
            "before": source["source_world_model_state_digest"],
            "patch": handoff["world_update_patch_digest"],
            "revision": after_revision,
            "candidate": source["source_world_candidate_envelope_digest"],
        }
    )
    transaction = canonical_digest(
        {
            "source_authorization_receipt": source[SOURCE_DIGEST_FIELD],
            "authorization_record": source[
                "world_candidate_commit_authorization_record_digest"
            ],
            "candidate": source["source_world_candidate_envelope_digest"],
            "patch": handoff["world_update_patch_digest"],
            "before_state": source["source_world_model_state_digest"],
            "after_state": after_state,
            "before_revision": before_revision,
            "after_revision": after_revision,
            "owner": handoff["authorization_owner_id"],
        }
    )
    review = {
        "source_world_candidate_commit_authorization_receipt_digest": source[
            SOURCE_DIGEST_FIELD
        ],
        "world_candidate_commit_authorization_record_digest": source[
            "world_candidate_commit_authorization_record_digest"
        ],
        "world_candidate_commit_authorization_debt_consumption_record_digest": source[
            "world_candidate_commit_authorization_debt_consumption_record_digest"
        ],
        "world_mutation_application_handoff_envelope_digest": source[
            "world_mutation_application_handoff_envelope_digest"
        ],
        "source_world_candidate_envelope_digest": source[
            "source_world_candidate_envelope_digest"
        ],
        SOURCE_REVIEW_DIGEST_FIELD: source[SOURCE_REVIEW_DIGEST_FIELD],
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "world_candidate_fact_digest": handoff["world_candidate_fact_digest"],
        "world_candidate_relation_digest": handoff[
            "world_candidate_relation_digest"
        ],
        "world_update_patch_digest": handoff["world_update_patch_digest"],
        "world_update_precondition_digest": handoff[
            "world_update_precondition_digest"
        ],
        "world_update_postcondition_digest": handoff[
            "world_update_postcondition_digest"
        ],
        "authorization_scope_digest": handoff["authorization_scope_digest"],
        "authorization_constraints_digest": handoff[
            "authorization_constraints_digest"
        ],
        "world_mutation_application_policy_digest": handoff[
            "world_mutation_application_policy_digest"
        ],
        "rollback_route_digest": handoff["rollback_route_digest"],
        "compensation_route_digest": handoff["compensation_route_digest"],
        "authorization_owner_id": handoff["authorization_owner_id"],
        "authorization_expiry_epoch": handoff["authorization_expiry_epoch"],
        "world_state_before_digest": source["source_world_model_state_digest"],
        "world_state_after_digest": after_state,
        "world_mutation_transaction_digest": transaction,
        "atomic_application_policy_digest": (
            "world-atomic-mutation-application-policy-v062-001"
        ),
        "persistent_world_storage_target_digest": (
            "world-persistent-storage-target-v062-001"
        ),
        "postcondition_verification_policy_digest": (
            "world-postcondition-verification-policy-v062-001"
        ),
        "mutation_owner_id": handoff["authorization_owner_id"],
        "application_review_started_epoch": 124,
        "application_review_completed_epoch": 125,
        "maximum_application_review_duration": 4,
        "expected_world_model_revision_before": before_revision,
        "expected_world_model_revision_after": after_revision,
        "source_authorization_ready": True,
        "source_authorization_single_use": True,
        "source_authorization_unconsumed": True,
        "candidate_identity_match": True,
        "patch_identity_match": True,
        "world_patch_scope_conformant": True,
        "world_patch_ceiling_not_exceeded": True,
        "world_preconditions_revalidated": True,
        "atomic_application_supported": True,
        "persistent_world_storage_target_available": True,
        "revision_increment_exactly_one": True,
        "world_postconditions_verifiable": True,
        "lineage_continuity_preserved": True,
        "responsibility_continuity_preserved": True,
        "mutation_owner_confirmed": True,
        "dukkha_preservation_supported": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "rollback_route_ready": True,
        "compensation_route_ready": True,
        "no_causal_overclaim": True,
        "no_realized_dukkha_overclaim": True,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
        "tool_invocation_requested": False,
        "external_side_effect_requested": False,
        "world_mutation_already_performed": False,
    }
    review[REVIEW_DIGEST_FIELD] = (
        compute_world_mutation_application_review_certificate_digest(review)
    )
    return review


def _redigest_review(source: dict, review: dict) -> dict:
    value = deepcopy(review)
    handoff = source["world_mutation_application_handoff_envelope"]
    value["source_world_candidate_commit_authorization_receipt_digest"] = source[
        SOURCE_DIGEST_FIELD
    ]
    value["world_candidate_commit_authorization_record_digest"] = source[
        "world_candidate_commit_authorization_record_digest"
    ]
    value["world_candidate_commit_authorization_debt_consumption_record_digest"] = (
        source[
            "world_candidate_commit_authorization_debt_consumption_record_digest"
        ]
    )
    value["world_mutation_application_handoff_envelope_digest"] = source[
        "world_mutation_application_handoff_envelope_digest"
    ]
    value["source_world_candidate_envelope_digest"] = source[
        "source_world_candidate_envelope_digest"
    ]
    value[SOURCE_REVIEW_DIGEST_FIELD] = source[SOURCE_REVIEW_DIGEST_FIELD]
    value["frontier_materialization_candidate_id"] = source[
        "invoked_frontier_candidate_id"
    ]
    value["frontier_adapter_id"] = source["invoked_frontier_adapter_id"]
    value["frontier_binding_digest"] = source["invoked_frontier_binding_digest"]
    for field in (
        "world_candidate_fact_digest",
        "world_candidate_relation_digest",
        "world_update_patch_digest",
        "world_update_precondition_digest",
        "world_update_postcondition_digest",
        "authorization_scope_digest",
        "authorization_constraints_digest",
        "world_mutation_application_policy_digest",
        "rollback_route_digest",
        "compensation_route_digest",
        "authorization_owner_id",
        "authorization_expiry_epoch",
    ):
        value[field] = handoff[field]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_world_mutation_application_review_certificate_digest(value)
    )
    return value


def _context(source: dict, review: dict) -> dict:
    authorized_epoch = source["world_candidate_commit_authorization_record"][
        "world_commit_authorization_intake_epoch"
    ]
    context = {
        "source_world_candidate_commit_authorization_receipt_digest": source[
            SOURCE_DIGEST_FIELD
        ],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_world_candidate_commit_authorized_epoch": authorized_epoch,
        "world_mutation_application_intake_epoch": authorized_epoch + 2,
        "maximum_world_mutation_application_intake_delay": 4,
        "world_mutation_application_intake_session_id": (
            "world-mutation-application-intake-v062-001"
        ),
        "world_mutation_application_intake_nonce_digest": (
            "world-mutation-application-nonce-v062-001"
        ),
        "prior_world_mutation_application_intake_session_ids": [],
        "prior_world_mutation_application_review_certificate_digests": [],
        "prior_world_mutation_application_intake_nonce_digests": [],
        "prior_consumed_source_authorization_receipt_digests": [],
        "prior_applied_world_mutation_transaction_digests": [],
        "requested_world_mutation_application_operation_digest": (
            compute_requested_world_mutation_application_operation_digest(
                source, review
            )
        ),
        "exact_world_mutation_application_cycle_digest": "",
    }
    context["exact_world_mutation_application_cycle_digest"] = (
        compute_exact_world_mutation_application_cycle_digest(
            source, review, context
        )
    )
    context[CONTEXT_DIGEST_FIELD] = (
        compute_world_mutation_application_intake_context_digest(context)
    )
    return context


def _redigest_context(source: dict, review: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["source_world_candidate_commit_authorization_receipt_digest"] = source[
        SOURCE_DIGEST_FIELD
    ]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_mutation_application_operation_digest"] = (
        compute_requested_world_mutation_application_operation_digest(
            source, review
        )
    )
    value["exact_world_mutation_application_cycle_digest"] = (
        compute_exact_world_mutation_application_cycle_digest(
            source, review, value
        )
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_world_mutation_application_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    source_override = overrides.pop(
        "source_world_candidate_commit_authorization_receipt", None
    )
    source = deepcopy(_source_receipt() if source_override is None else source_override)
    review_override = overrides.pop(
        "world_mutation_application_review_certificate", None
    )
    review = deepcopy(
        _review(source)
        if review_override is None and source
        else (review_override or {})
    )
    context_override = overrides.pop(
        "world_mutation_application_intake_context", None
    )
    context = deepcopy(
        _context(source, review)
        if context_override is None and source and review
        else (context_override or {})
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v061-missing")
    review_digest = review.get(REVIEW_DIGEST_FIELD, "review-v062-missing")
    context_digest = context.get(CONTEXT_DIGEST_FIELD, "context-v062-missing")

    expected_source = overrides.pop(
        "expected_source_world_candidate_commit_authorization_receipt_digest",
        source_digest,
    )
    expected_review = overrides.pop(
        "expected_world_mutation_application_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_world_mutation_application_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "world_mutation_application_policy_digest",
        "world-dukkha-preserving-single-use-mutation-application-policy-v062",
    )
    owner = overrides.pop(
        "world_mutation_application_responsibility_digest",
        "world-single-use-mutation-application-owner-v062",
    )
    request_id = overrides.pop(
        "world_mutation_application_request_id",
        "world-mutation-application-v062-001",
    )
    bundle = overrides.pop(
        "world_mutation_application_bundle_digest",
        compute_world_mutation_application_bundle_digest(
            source_world_candidate_commit_authorization_receipt_digest=source_digest,
            expected_source_world_candidate_commit_authorization_receipt_digest=(
                expected_source
            ),
            world_candidate_commit_authorization_record_digest=source.get(
                "world_candidate_commit_authorization_record_digest",
                "authorization-record-missing",
            ),
            world_mutation_application_handoff_envelope_digest=source.get(
                "world_mutation_application_handoff_envelope_digest",
                "application-handoff-missing",
            ),
            world_mutation_application_review_certificate_digest=review_digest,
            expected_world_mutation_application_review_certificate_digest=(
                expected_review
            ),
            world_mutation_application_intake_context_digest=context_digest,
            expected_world_mutation_application_intake_context_digest=(
                expected_context
            ),
            requested_world_mutation_application_operation_digest=context.get(
                "requested_world_mutation_application_operation_digest",
                "operation-missing",
            ),
            exact_world_mutation_application_cycle_digest=context.get(
                "exact_world_mutation_application_cycle_digest",
                "cycle-missing",
            ),
            world_mutation_transaction_digest=review.get(
                "world_mutation_transaction_digest",
                "transaction-missing",
            ),
            world_mutation_application_policy_digest=policy,
            world_mutation_application_responsibility_digest=owner,
            world_mutation_application_request_id=request_id,
        ),
    )

    args = {
        "source_world_candidate_commit_authorization_receipt": source,
        "expected_source_world_candidate_commit_authorization_receipt_digest": (
            expected_source
        ),
        "world_mutation_application_review_certificate": review,
        "expected_world_mutation_application_review_certificate_digest": (
            expected_review
        ),
        "world_mutation_application_intake_context": context,
        "expected_world_mutation_application_intake_context_digest": (
            expected_context
        ),
        "world_mutation_application_policy_digest": policy,
        "world_mutation_application_responsibility_digest": owner,
        "world_mutation_application_request_id": request_id,
        "world_mutation_application_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_world_dukkha_preserving_single_use_world_mutation_application_intake(
        **args
    )


def _assert_blocked(result, blocker: str) -> None:
    assert result.status == STATUS_BLOCKED
    assert result.receipt is None
    assert blocker in result.blockers, result.blockers


def _assert_disposition(result, disposition: str) -> dict:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["world_mutation_application_disposition"] == disposition
    assert result.receipt["world_version"] == "v0.62"
    return result.receipt


def _review_case(source: dict, field: str, value) -> dict:
    review = _review(source)
    review[field] = value
    return _redigest_review(source, review)


def _run_review_disposition(source: dict, field: str, value, disposition: str) -> None:
    review = _review_case(source, field, value)
    context = _redigest_context(source, review, _context(source, review))
    _assert_disposition(
        _build(
            source_world_candidate_commit_authorization_receipt=source,
            world_mutation_application_review_certificate=review,
            world_mutation_application_intake_context=context,
        ),
        disposition,
    )


def main() -> int:
    ready = _assert_disposition(_build(), DISPOSITION_READY)
    assert ready["world_mutation_application_state_before"] == STATE_BEFORE
    assert ready["world_mutation_application_state_after"] == STATE_AFTER_READY
    assert ready["world_mutation_application_completed"] is True
    assert ready["exactly_one_world_patch_applied"] is True
    assert ready["world_mutation_transaction_atomic"] is True
    assert ready["world_candidate_commit_completed"] is True
    assert (
        ready["single_use_world_candidate_commit_authorization_consumed"]
        is True
    )
    assert ready["persistent_world_model_state_unchanged"] is False
    assert ready["persistent_world_model_state_changed"] is True
    assert ready["world_model_revision_incremented_exactly_once"] is True
    assert ready["world_postcondition_verification_intake_admitted"] is True
    assert ready["world_postcondition_verification_completed"] is False
    assert ready["world_postcondition_verification_debt_open"] is True
    assert ready["world_fact_confirmed"] is False
    assert ready["causal_attribution_confirmed"] is False
    assert ready["dukkha_reduction_realized_confirmed"] is False
    assert ready["tool_invocation_performed"] is False
    assert ready["external_side_effect_performed"] is False
    assert ready["general_world_mutation_authority_granted"] is False
    assert ready["world_mutation_authority_granted"] is False
    assert ready["world_mutation_record"] is not None
    assert ready["persisted_world_candidate_envelope"] is not None
    assert ready["world_postcondition_verification_handoff_envelope"] is not None
    assert ready[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in ready.items() if key != RECEIPT_DIGEST_FIELD}
    )

    _assert_blocked(
        _build(source_world_candidate_commit_authorization_receipt={}),
        "source_world_candidate_commit_authorization_receipt_missing",
    )

    tampered = _source_receipt()
    tampered["world_version"] = "v0.61-tampered"
    _assert_blocked(
        _build(source_world_candidate_commit_authorization_receipt=tampered),
        "source_world_version_mismatch",
    )

    _assert_blocked(
        _build(world_mutation_application_bundle_digest="bundle-mismatch"),
        "world_mutation_application_bundle_digest_mismatch",
    )

    source = _source_receipt()

    context = _context(source, _review(source))
    context["current_world_model_state_digest"] = "stale-world-state"
    context = _redigest_context(source, _review(source), context)
    _assert_disposition(
        _build(
            source_world_candidate_commit_authorization_receipt=source,
            world_mutation_application_intake_context=context,
        ),
        DISPOSITION_WORLD_REFRESH,
    )

    review = _review(source)
    context = _context(source, review)
    context["source_world_candidate_commit_authorized_epoch"] = 100
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(
            source_world_candidate_commit_authorization_receipt=source,
            world_mutation_application_review_certificate=review,
            world_mutation_application_intake_context=context,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    review = _review(source)
    review["application_review_started_epoch"] = 100
    review["application_review_completed_epoch"] = 110
    review["maximum_application_review_duration"] = 4
    review = _redigest_review(source, review)
    context = _redigest_context(source, review, _context(source, review))
    _assert_disposition(
        _build(
            source_world_candidate_commit_authorization_receipt=source,
            world_mutation_application_review_certificate=review,
            world_mutation_application_intake_context=context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    review = _review(source)
    context = _context(source, review)
    context["source_world_candidate_commit_authorized_epoch"] = 126
    context["world_mutation_application_intake_epoch"] = 128
    context["maximum_world_mutation_application_intake_delay"] = 4
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(
            source_world_candidate_commit_authorization_receipt=source,
            world_mutation_application_review_certificate=review,
            world_mutation_application_intake_context=context,
        ),
        DISPOSITION_EXPIRED,
    )

    _run_review_disposition(
        source,
        "source_authorization_unconsumed",
        False,
        DISPOSITION_AUTHORIZATION_REVALIDATION,
    )
    _run_review_disposition(
        source,
        "candidate_identity_match",
        False,
        DISPOSITION_CANDIDATE_REVALIDATION,
    )
    _run_review_disposition(
        source,
        "patch_identity_match",
        False,
        DISPOSITION_PATCH_REPAIR,
    )
    _run_review_disposition(
        source,
        "world_preconditions_revalidated",
        False,
        DISPOSITION_PRECONDITION_REPAIR,
    )
    _run_review_disposition(
        source,
        "atomic_application_supported",
        False,
        DISPOSITION_ATOMICITY_REPAIR,
    )
    _run_review_disposition(
        source,
        "persistent_world_storage_target_available",
        False,
        DISPOSITION_STORAGE_REPAIR,
    )
    _run_review_disposition(
        source,
        "revision_increment_exactly_one",
        False,
        DISPOSITION_REVISION_REPAIR,
    )
    _run_review_disposition(
        source,
        "world_postconditions_verifiable",
        False,
        DISPOSITION_POSTCONDITION_REPAIR,
    )
    _run_review_disposition(
        source,
        "lineage_continuity_preserved",
        False,
        DISPOSITION_PROVENANCE_REPAIR,
    )
    _run_review_disposition(
        source,
        "mutation_owner_confirmed",
        False,
        DISPOSITION_OWNER_REJECTED,
    )
    _run_review_disposition(
        source,
        "protected_group_nonexternalization_supported",
        False,
        DISPOSITION_NONEXTERNALIZATION_REVIEW,
    )
    _run_review_disposition(
        source,
        "dukkha_preservation_supported",
        False,
        DISPOSITION_DUKKHA_REVIEW,
    )
    _run_review_disposition(
        source,
        "compensation_route_ready",
        False,
        DISPOSITION_COMPENSATION_REPAIR,
    )
    _run_review_disposition(
        source,
        "world_fact_claimed",
        True,
        DISPOSITION_TRUTH_PROMOTION_REJECTED,
    )

    review = _review(source)
    context = _context(source, review)
    context["prior_world_mutation_application_intake_session_ids"] = [
        context["world_mutation_application_intake_session_id"]
    ]
    context = _redigest_context(source, review, context)
    _assert_disposition(
        _build(
            source_world_candidate_commit_authorization_receipt=source,
            world_mutation_application_review_certificate=review,
            world_mutation_application_intake_context=context,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )

    print(
        "PASS: WORLD v0.62 dukkha-preserving single-use WORLD mutation "
        "application intake actual chain"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
