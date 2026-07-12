#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_world_dukkha_preserving_single_use_world_mutation_application_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_AUTH_EXPIRED,
    DISPOSITION_PATCH_REPAIR,
    DISPOSITION_READY,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_TRUTH_PROMOTION_REJECTED,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    SOURCE_AUTH_REVIEW_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
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


def _source() -> dict:
    result = build_world_v061_authorization()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["world_candidate_commit_authorization_disposition"] == "world_candidate_commit_authorization_ready"
    return deepcopy(result.receipt)


def _review(source: dict) -> dict:
    handoff = source["world_mutation_application_handoff_envelope"]
    review = {
        "source_world_commit_authorization_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "world_candidate_commit_authorization_record_digest": source["world_candidate_commit_authorization_record_digest"],
        "world_mutation_application_handoff_envelope_digest": source["world_mutation_application_handoff_envelope_digest"],
        SOURCE_AUTH_REVIEW_DIGEST_FIELD: source[SOURCE_AUTH_REVIEW_DIGEST_FIELD],
        "world_candidate_envelope_digest": source["source_world_candidate_envelope_digest"],
        "world_candidate_fact_digest": handoff["world_candidate_fact_digest"],
        "world_candidate_relation_digest": handoff["world_candidate_relation_digest"],
        "world_update_patch_digest": handoff["world_update_patch_digest"],
        "world_update_precondition_digest": handoff["world_update_precondition_digest"],
        "world_update_postcondition_digest": handoff["world_update_postcondition_digest"],
        "authorization_scope_digest": handoff["authorization_scope_digest"],
        "authorization_constraints_digest": handoff["authorization_constraints_digest"],
        "authorization_owner_id": handoff["authorization_owner_id"],
        "authorization_expiry_epoch": handoff["authorization_expiry_epoch"],
        "world_mutation_application_policy_digest": handoff["world_mutation_application_policy_digest"],
        "rollback_route_digest": handoff["rollback_route_digest"],
        "compensation_route_digest": handoff["compensation_route_digest"],
        "mutation_engine_id": "world-atomic-mutation-engine-v062",
        "mutation_target_world_binding_digest": source["source_world_binding_digest"],
        "mutation_expected_pre_state_digest": source["source_world_model_state_digest"],
        "mutation_expected_post_state_digest": "world-model-state-v062-post-001",
        "mutation_transaction_id": "world-mutation-transaction-v062-001",
        "application_review_started_epoch": 125,
        "application_review_completed_epoch": 126,
        "maximum_application_review_duration": 4,
        "source_authorization_valid": True,
        "candidate_identity_match": True,
        "patch_identity_match": True,
        "authorization_scope_match": True,
        "authorization_constraints_satisfied": True,
        "authorization_owner_confirmed": True,
        "world_preconditions_satisfied": True,
        "mutation_engine_admitted": True,
        "atomic_application_supported": True,
        "postcondition_observation_route_ready": True,
        "lineage_continuity_preserved": True,
        "responsibility_continuity_preserved": True,
        "dukkha_preservation_supported": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "compensation_route_ready": True,
        "world_fact_claimed": False,
        "causal_attribution_claimed": False,
        "realized_dukkha_reduction_claimed": False,
    }
    review[REVIEW_DIGEST_FIELD] = compute_world_mutation_application_review_certificate_digest(review)
    return review


def _context(source: dict, review: dict) -> dict:
    context = {
        "source_world_commit_authorization_receipt_digest": source[SOURCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review[REVIEW_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source["source_world_model_state_digest"],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_authorization_issued_epoch": 124,
        "world_mutation_application_intake_epoch": 126,
        "maximum_world_mutation_application_intake_delay": 4,
        "world_mutation_application_intake_session_id": "world-mutation-application-v062-001",
        "world_mutation_application_intake_nonce_digest": "world-mutation-application-nonce-v062-001",
        "prior_world_mutation_application_intake_session_ids": [],
        "prior_world_mutation_application_review_certificate_digests": [],
        "prior_world_mutation_application_intake_nonce_digests": [],
        "prior_applied_world_commit_authorization_receipt_digests": [],
        "requested_world_mutation_application_operation_digest": compute_requested_world_mutation_application_operation_digest(source, review),
        "exact_world_mutation_application_cycle_digest": "",
    }
    context["exact_world_mutation_application_cycle_digest"] = compute_exact_world_mutation_application_cycle_digest(source, review, context)
    context[CONTEXT_DIGEST_FIELD] = compute_world_mutation_application_intake_context_digest(context)
    return context


def _redigest_review(review: dict) -> dict:
    value = deepcopy(review)
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = compute_world_mutation_application_review_certificate_digest(value)
    return value


def _redigest_context(source: dict, review: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["source_world_commit_authorization_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = review[REVIEW_DIGEST_FIELD]
    value["requested_world_mutation_application_operation_digest"] = compute_requested_world_mutation_application_operation_digest(source, review)
    value["exact_world_mutation_application_cycle_digest"] = compute_exact_world_mutation_application_cycle_digest(source, review, value)
    value[CONTEXT_DIGEST_FIELD] = compute_world_mutation_application_intake_context_digest(value)
    return value


def _build(source: dict | None = None, review: dict | None = None, context: dict | None = None, **overrides):
    source = deepcopy(source or _source())
    review = deepcopy(review or _review(source))
    context = deepcopy(context or _context(source, review))
    source_digest = source[SOURCE_DIGEST_FIELD]
    review_digest = review[REVIEW_DIGEST_FIELD]
    context_digest = context[CONTEXT_DIGEST_FIELD]
    expected_source = overrides.pop("expected_source_world_commit_authorization_receipt_digest", source_digest)
    expected_review = overrides.pop("expected_world_mutation_application_review_certificate_digest", review_digest)
    expected_context = overrides.pop("expected_world_mutation_application_intake_context_digest", context_digest)
    policy = "world-dukkha-preserving-mutation-application-policy-v062"
    owner = "world-mutation-application-owner-v062"
    request_id = "world-mutation-application-v062-001"
    bundle = compute_world_mutation_application_bundle_digest(
        source_world_commit_authorization_receipt_digest=source_digest,
        expected_source_world_commit_authorization_receipt_digest=expected_source,
        world_candidate_commit_authorization_record_digest=source["world_candidate_commit_authorization_record_digest"],
        world_mutation_application_handoff_envelope_digest=source["world_mutation_application_handoff_envelope_digest"],
        world_mutation_application_review_certificate_digest=review_digest,
        expected_world_mutation_application_review_certificate_digest=expected_review,
        world_mutation_application_intake_context_digest=context_digest,
        expected_world_mutation_application_intake_context_digest=expected_context,
        requested_world_mutation_application_operation_digest=context["requested_world_mutation_application_operation_digest"],
        exact_world_mutation_application_cycle_digest=context["exact_world_mutation_application_cycle_digest"],
        world_mutation_application_policy_digest=policy,
        world_mutation_application_responsibility_digest=owner,
        world_mutation_application_request_id=request_id,
    )
    return build_world_dukkha_preserving_single_use_world_mutation_application_intake(
        source_world_commit_authorization_receipt=source,
        expected_source_world_commit_authorization_receipt_digest=expected_source,
        world_mutation_application_review_certificate=review,
        expected_world_mutation_application_review_certificate_digest=expected_review,
        world_mutation_application_intake_context=context,
        expected_world_mutation_application_intake_context_digest=expected_context,
        world_mutation_application_policy_digest=policy,
        world_mutation_application_responsibility_digest=owner,
        world_mutation_application_request_id=request_id,
        world_mutation_application_bundle_digest=overrides.pop("world_mutation_application_bundle_digest", bundle),
        **overrides,
    )


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    receipt = ready.receipt
    assert receipt is not None
    assert receipt["world_version"] == "v0.62"
    assert receipt["world_mutation_application_disposition"] == DISPOSITION_READY
    assert receipt["world_mutation_application_state_before"] == STATE_BEFORE
    assert receipt["world_mutation_application_state_after"] == STATE_AFTER_READY
    assert receipt["world_mutation_application_performed"] is True
    assert receipt["world_mutation_applied_atomically"] is True
    assert receipt["single_use_authorization_consumed"] is True
    assert receipt["world_candidate_commit_completed"] is True
    assert receipt["persistent_world_model_state_changed"] is True
    assert receipt["world_model_revision_incremented_once"] is True
    assert receipt["post_application_verification_completed"] is False
    assert receipt["world_fact_confirmed"] is False
    assert receipt["causal_attribution_confirmed"] is False
    assert receipt["dukkha_reduction_realized_confirmed"] is False
    assert receipt["general_world_mutation_authority_granted"] is False
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest({k: v for k, v in receipt.items() if k != RECEIPT_DIGEST_FIELD})

    source = _source(); review = _review(source); context = _context(source, review)
    review["authorization_expiry_epoch"] = 125
    review = _redigest_review(review); context = _redigest_context(source, review, context)
    expired = _build(source, review, context)
    assert expired.receipt and expired.receipt["world_mutation_application_disposition"] == DISPOSITION_AUTH_EXPIRED

    source = _source(); review = _review(source); context = _context(source, review)
    review["patch_identity_match"] = False
    review = _redigest_review(review); context = _redigest_context(source, review, context)
    repair = _build(source, review, context)
    assert repair.receipt and repair.receipt["world_mutation_application_disposition"] == DISPOSITION_PATCH_REPAIR

    source = _source(); review = _review(source); context = _context(source, review)
    review["world_fact_claimed"] = True
    review = _redigest_review(review); context = _redigest_context(source, review, context)
    truth = _build(source, review, context)
    assert truth.receipt and truth.receipt["world_mutation_application_disposition"] == DISPOSITION_TRUTH_PROMOTION_REJECTED

    source = _source(); review = _review(source); context = _context(source, review)
    context["prior_world_mutation_application_intake_session_ids"] = [context["world_mutation_application_intake_session_id"]]
    context = _redigest_context(source, review, context)
    replay = _build(source, review, context)
    assert replay.receipt and replay.receipt["world_mutation_application_disposition"] == DISPOSITION_REPLAY_REJECTED

    blocked = _build(expected_source_world_commit_authorization_receipt_digest="wrong")
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    print("PASS: WORLD v0.62 single-use mutation application intake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
