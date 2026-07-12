#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_effect_commit_authorization_intake_v0_1 import (
    DISPOSITION_CHECKPOINT,
    DISPOSITION_COMPENSATION_REPAIR,
    DISPOSITION_OBSERVATION_REPAIR,
    DISPOSITION_READY,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVERIFY,
    DISPOSITION_SCOPE_REPAIR,
    DISPOSITION_VERIFICATION_REPAIR,
    DISPOSITION_WORLD_REFRESH,
    RECEIPT_DIGEST_FIELD,
    REVIEW_SUPPORTED,
    SOURCE_DIGEST_FIELD,
    STATUS_READY,
    build_actos_dukkha_preserving_effect_commit_authorization_intake,
    canonical_digest,
    compute_effect_commit_authorization_bundle_digest,
    compute_effect_commit_authorization_context_digest,
    compute_effect_commit_intent_digest,
    compute_effect_commit_review_certificate_digest,
    compute_exact_effect_commit_authorization_cycle_digest,
    compute_requested_effect_commit_operation_digest,
)
from scripts.check_actos_dukkha_preserving_bounded_adapter_invocation_v0_1 import (
    _build as build_actos_v08_invocation,
)


def _source_receipt() -> dict:
    result = build_actos_v08_invocation()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _review(source: dict) -> dict:
    certificate = {
        "source_invocation_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "invocation_record_digest": source["invocation_record_digest"],
        "review_disposition": REVIEW_SUPPORTED,
        "dukkha_reduction_support_status": "supported",
        "protected_group_nonexternalization_status": "preserved",
        "future_nonexternalization_status": "preserved",
        "revision_capacity_status": "preserved",
        "persistent_loop_reduction_status": "preserved",
        "effect_scope_status": "exact",
        "effect_ceiling_status": "exact",
        "checkpoint_status": "satisfied",
        "stop_condition_status": "current",
        "compensation_route_status": "ready",
        "observation_route_status": "ready",
        "verification_route_status": "ready",
        "review_epoch": 105,
        "reviewer_responsibility_digest": "actos-effect-review-owner-v09",
    }
    certificate["effect_commit_review_certificate_digest"] = (
        compute_effect_commit_review_certificate_digest(certificate)
    )
    return certificate


def _redigest_review(source: dict, review: dict) -> dict:
    value = deepcopy(review)
    value["source_invocation_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["adapter_result_envelope_digest"] = source[
        "adapter_result_envelope_digest"
    ]
    value["invocation_record_digest"] = source["invocation_record_digest"]
    value.pop("effect_commit_review_certificate_digest", None)
    value["effect_commit_review_certificate_digest"] = (
        compute_effect_commit_review_certificate_digest(value)
    )
    return value


def _context(source: dict, review: dict) -> dict:
    context = {
        "source_invocation_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "effect_commit_review_certificate_digest": review[
            "effect_commit_review_certificate_digest"
        ],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "invocation_receipt_observed_epoch": 105,
        "authorization_epoch": 106,
        "maximum_authorization_delay": 4,
        "commit_session_id": "actos-effect-commit-session-v09-001",
        "commit_intent_digest": compute_effect_commit_intent_digest(
            source, review
        ),
        "commit_authorization_nonce_digest": (
            "actos-effect-commit-authorization-nonce-v09-001"
        ),
        "prior_commit_session_ids": [],
        "prior_commit_authorization_nonce_digests": [],
        "prior_authorized_invocation_receipt_digests": [],
        "requested_effect_commit_operation_digest": (
            compute_requested_effect_commit_operation_digest(source, review)
        ),
        "exact_effect_commit_authorization_cycle_digest": "",
    }
    context["exact_effect_commit_authorization_cycle_digest"] = (
        compute_exact_effect_commit_authorization_cycle_digest(
            source, review, context
        )
    )
    context["effect_commit_authorization_context_digest"] = (
        compute_effect_commit_authorization_context_digest(context)
    )
    return context


def _redigest_context(
    source: dict,
    review: dict,
    context: dict,
    *,
    recompute_operation: bool = True,
) -> dict:
    value = deepcopy(context)
    value["source_invocation_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["adapter_result_envelope_digest"] = source[
        "adapter_result_envelope_digest"
    ]
    value["effect_commit_review_certificate_digest"] = review[
        "effect_commit_review_certificate_digest"
    ]
    value["commit_intent_digest"] = compute_effect_commit_intent_digest(
        source, review
    )
    if recompute_operation:
        value["requested_effect_commit_operation_digest"] = (
            compute_requested_effect_commit_operation_digest(source, review)
        )
    value["exact_effect_commit_authorization_cycle_digest"] = (
        compute_exact_effect_commit_authorization_cycle_digest(
            source, review, value
        )
    )
    value["effect_commit_authorization_context_digest"] = (
        compute_effect_commit_authorization_context_digest(value)
    )
    return value


def _build(**overrides):
    source_override = overrides.pop("source_invocation_receipt", None)
    source = deepcopy(
        _source_receipt() if source_override is None else source_override
    )

    review_override = overrides.pop("effect_commit_review_certificate", None)
    review = deepcopy(
        _review(source)
        if review_override is None and source
        else (review_override or {})
    )

    context_override = overrides.pop(
        "effect_commit_authorization_context", None
    )
    context = deepcopy(
        _context(source, review)
        if context_override is None and source and review
        else (context_override or {})
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v08-missing")
    review_digest = review.get(
        "effect_commit_review_certificate_digest", "review-v09-missing"
    )
    context_digest = context.get(
        "effect_commit_authorization_context_digest", "context-v09-missing"
    )
    expected_source = overrides.pop(
        "expected_source_invocation_receipt_digest", source_digest
    )
    expected_review = overrides.pop(
        "expected_effect_commit_review_certificate_digest", review_digest
    )
    expected_context = overrides.pop(
        "expected_effect_commit_authorization_context_digest", context_digest
    )
    policy = overrides.pop(
        "effect_commit_authorization_policy_digest",
        "actos-effect-commit-authorization-policy-v09",
    )
    owner = overrides.pop(
        "actos_effect_commit_authorization_responsibility_digest",
        "actos-effect-commit-authorization-owner-v09",
    )
    request_id = overrides.pop(
        "effect_commit_authorization_request_id",
        "actos-effect-commit-authorization-v09-001",
    )
    bundle = overrides.pop(
        "effect_commit_authorization_bundle_digest",
        compute_effect_commit_authorization_bundle_digest(
            source_invocation_receipt_digest=source_digest,
            expected_source_invocation_receipt_digest=expected_source,
            invocation_record_digest=source.get(
                "invocation_record_digest", "invocation-record-missing"
            ),
            adapter_result_envelope_digest=source.get(
                "adapter_result_envelope_digest", "result-envelope-missing"
            ),
            lease_consumption_record_digest=source.get(
                "lease_consumption_record_digest", "lease-record-missing"
            ),
            effect_commit_review_certificate_digest=review_digest,
            expected_effect_commit_review_certificate_digest=expected_review,
            effect_commit_authorization_context_digest=context_digest,
            expected_effect_commit_authorization_context_digest=(
                expected_context
            ),
            requested_effect_commit_operation_digest=context.get(
                "requested_effect_commit_operation_digest",
                "commit-operation-missing",
            ),
            exact_effect_commit_authorization_cycle_digest=context.get(
                "exact_effect_commit_authorization_cycle_digest",
                "commit-cycle-missing",
            ),
            effect_commit_authorization_policy_digest=policy,
            actos_effect_commit_authorization_responsibility_digest=owner,
            effect_commit_authorization_request_id=request_id,
        ),
    )
    args = {
        "source_invocation_receipt": source,
        "expected_source_invocation_receipt_digest": expected_source,
        "effect_commit_review_certificate": review,
        "expected_effect_commit_review_certificate_digest": expected_review,
        "effect_commit_authorization_context": context,
        "expected_effect_commit_authorization_context_digest": expected_context,
        "effect_commit_authorization_policy_digest": policy,
        "actos_effect_commit_authorization_responsibility_digest": owner,
        "effect_commit_authorization_request_id": request_id,
        "effect_commit_authorization_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_preserving_effect_commit_authorization_intake(
        **args
    )


def _assert_not_authorized(result, disposition: str) -> None:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["authorization_disposition"] == disposition
    assert receipt["effect_commit_authorization_admitted"] is False
    assert receipt["effect_commit_authorization_receipt_issued"] is False
    assert receipt["single_use_effect_commit_authorization_reserved"] is False
    assert receipt["effect_commit_authorization_token_digest"] == ""
    assert receipt["effect_commit_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["persistent_world_state_unchanged"] is True


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["actos_version"] == "v0.9"
    assert receipt["status"] == (
        "ACTOS_DUKKHA_PRESERVING_EFFECT_COMMIT_AUTHORIZATION_ROUTED"
    )
    assert receipt["authorization_disposition"] == DISPOSITION_READY
    assert receipt["effect_commit_authorization_admitted"] is True
    assert receipt["effect_commit_authorization_receipt_issued"] is True
    assert receipt["single_use_effect_commit_authorization_reserved"] is True
    assert receipt["effect_commit_authorization_token_digest"]
    assert receipt["effect_commit_state_before"] == (
        "invoked_effect_not_committed"
    )
    assert receipt["effect_commit_state_after"] == "authorized_not_committed"
    assert receipt["effect_commit_intake_admitted"] is True
    assert receipt["adapter_invocation_performed"] is True
    assert receipt["adapter_lease_use_consumed"] is True
    assert receipt["effect_commit_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["persistent_world_state_unchanged"] is True
    assert receipt["dukkha_reduction_support_preserved"] is True
    assert receipt["protected_group_nonexternalization_preserved"] is True
    assert receipt["future_nonexternalization_preserved"] is True
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: value
            for key, value in receipt.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )

    source = _source_receipt()
    review = _review(source)

    changed_world = _context(source, review)
    changed_world["current_world_model_state_digest"] = "world-changed"
    changed_world = _redigest_context(source, review, changed_world)
    _assert_not_authorized(
        _build(effect_commit_authorization_context=changed_world),
        DISPOSITION_WORLD_REFRESH,
    )

    stale = _context(source, review)
    stale["authorization_epoch"] = 120
    stale = _redigest_context(source, review, stale)
    _assert_not_authorized(
        _build(effect_commit_authorization_context=stale),
        DISPOSITION_REVERIFY,
    )

    replay_session = _context(source, review)
    replay_session["prior_commit_session_ids"] = [
        replay_session["commit_session_id"]
    ]
    replay_session = _redigest_context(source, review, replay_session)
    _assert_not_authorized(
        _build(effect_commit_authorization_context=replay_session),
        DISPOSITION_REPLAY_REJECTED,
    )

    replay_nonce = _context(source, review)
    replay_nonce["prior_commit_authorization_nonce_digests"] = [
        replay_nonce["commit_authorization_nonce_digest"]
    ]
    replay_nonce = _redigest_context(source, review, replay_nonce)
    _assert_not_authorized(
        _build(effect_commit_authorization_context=replay_nonce),
        DISPOSITION_REPLAY_REJECTED,
    )

    replay_source = _context(source, review)
    replay_source["prior_authorized_invocation_receipt_digests"] = [
        source[SOURCE_DIGEST_FIELD]
    ]
    replay_source = _redigest_context(source, review, replay_source)
    _assert_not_authorized(
        _build(effect_commit_authorization_context=replay_source),
        DISPOSITION_REPLAY_REJECTED,
    )

    unsupported_review = deepcopy(review)
    unsupported_review["review_disposition"] = "indeterminate"
    unsupported_review = _redigest_review(source, unsupported_review)
    _assert_not_authorized(
        _build(effect_commit_review_certificate=unsupported_review),
        DISPOSITION_REVERIFY,
    )

    scope_review = deepcopy(review)
    scope_review["effect_scope_status"] = "expanded"
    scope_review = _redigest_review(source, scope_review)
    _assert_not_authorized(
        _build(effect_commit_review_certificate=scope_review),
        DISPOSITION_SCOPE_REPAIR,
    )

    checkpoint_review = deepcopy(review)
    checkpoint_review["checkpoint_status"] = "required"
    checkpoint_review = _redigest_review(source, checkpoint_review)
    _assert_not_authorized(
        _build(effect_commit_review_certificate=checkpoint_review),
        DISPOSITION_CHECKPOINT,
    )

    observation_review = deepcopy(review)
    observation_review["observation_route_status"] = "missing"
    observation_review = _redigest_review(source, observation_review)
    _assert_not_authorized(
        _build(effect_commit_review_certificate=observation_review),
        DISPOSITION_OBSERVATION_REPAIR,
    )

    verification_review = deepcopy(review)
    verification_review["verification_route_status"] = "missing"
    verification_review = _redigest_review(source, verification_review)
    _assert_not_authorized(
        _build(effect_commit_review_certificate=verification_review),
        DISPOSITION_VERIFICATION_REPAIR,
    )

    compensation_review = deepcopy(review)
    compensation_review["compensation_route_status"] = "missing"
    compensation_review = _redigest_review(source, compensation_review)
    _assert_not_authorized(
        _build(effect_commit_review_certificate=compensation_review),
        DISPOSITION_COMPENSATION_REPAIR,
    )

    promoted_source = deepcopy(source)
    promoted_source["effect_commit_performed"] = True
    promoted_source = _redigest_source(promoted_source)

    changed_envelope_source = deepcopy(source)
    changed_envelope_source["adapter_result_envelope"][
        "effect_commit_state"
    ] = "committed"
    changed_envelope_source["adapter_result_envelope_digest"] = canonical_digest(
        changed_envelope_source["adapter_result_envelope"]
    )
    changed_envelope_source = _redigest_source(changed_envelope_source)

    bad_review = deepcopy(review)
    bad_review["source_invocation_receipt_digest"] = "wrong-source"
    bad_review.pop("effect_commit_review_certificate_digest", None)
    bad_review["effect_commit_review_certificate_digest"] = (
        compute_effect_commit_review_certificate_digest(bad_review)
    )

    wrong_operation = _context(source, review)
    wrong_operation["requested_effect_commit_operation_digest"] = (
        "wrong-operation"
    )
    wrong_operation = _redigest_context(
        source, review, wrong_operation, recompute_operation=False
    )

    blocked = [
        _build(source_invocation_receipt={}),
        _build(effect_commit_review_certificate={}),
        _build(effect_commit_authorization_context={}),
        _build(expected_source_invocation_receipt_digest="wrong"),
        _build(expected_effect_commit_review_certificate_digest="wrong"),
        _build(expected_effect_commit_authorization_context_digest="wrong"),
        _build(effect_commit_authorization_bundle_digest="wrong"),
        _build(source_invocation_receipt=promoted_source),
        _build(source_invocation_receipt=changed_envelope_source),
        _build(effect_commit_review_certificate=bad_review),
        _build(effect_commit_authorization_context=wrong_operation),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.receipt is None

    print(
        "PASS: ActOS Dukkha-Preserving Effect Commit Authorization "
        "Intake Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
