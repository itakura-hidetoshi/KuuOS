#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_single_use_effect_commit_intake_v0_1 import (
    RECEIPT_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATE_AFTER,
    STATE_BEFORE,
    STATUS_BLOCKED,
    STATUS_READY,
    build_actos_dukkha_preserving_single_use_effect_commit_intake,
    canonical_digest,
    compute_effect_commit_context_digest,
    compute_exact_effect_commit_cycle_digest,
    compute_requested_effect_commit_operation_digest,
    compute_single_use_effect_commit_bundle_digest,
)
from scripts.check_actos_dukkha_preserving_effect_commit_authorization_intake_v0_1 import (
    _build as build_actos_v09_effect_commit_authorization,
)


def _source_receipt() -> dict:
    result = build_actos_v09_effect_commit_authorization()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    receipt = deepcopy(result.receipt)
    assert receipt["authorization_disposition"] == "effect_commit_authorization_ready"
    assert receipt["effect_commit_authorization_admitted"] is True
    assert receipt["effect_commit_state_after"] == STATE_BEFORE
    return receipt


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _context(source: dict) -> dict:
    context = {
        "source_effect_commit_authorization_receipt_digest": source[
            SOURCE_DIGEST_FIELD
        ],
        "source_invocation_receipt_digest": source[
            "source_invocation_receipt_digest"
        ],
        "effect_commit_authorization_record_digest": source[
            "effect_commit_authorization_record_digest"
        ],
        "effect_commit_authorization_token_digest": source[
            "effect_commit_authorization_token_digest"
        ],
        "adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "authorization_receipt_observed_epoch": 107,
        "effect_commit_epoch": 108,
        "maximum_effect_commit_delay": 4,
        "effect_commit_session_id": "actos-effect-commit-session-v010-001",
        "effect_commit_nonce_digest": "actos-effect-commit-nonce-v010-001",
        "prior_consumed_effect_commit_authorization_token_digests": [],
        "prior_effect_commit_nonce_digests": [],
        "prior_committed_authorization_receipt_digests": [],
        "requested_effect_commit_operation_digest": (
            compute_requested_effect_commit_operation_digest(source)
        ),
        "exact_effect_commit_cycle_digest": "",
    }
    context["exact_effect_commit_cycle_digest"] = (
        compute_exact_effect_commit_cycle_digest(source, context)
    )
    context["effect_commit_context_digest"] = compute_effect_commit_context_digest(
        context
    )
    return context


def _redigest_context(
    source: dict,
    context: dict,
    *,
    recompute_operation: bool = True,
) -> dict:
    value = deepcopy(context)
    value["source_effect_commit_authorization_receipt_digest"] = source[
        SOURCE_DIGEST_FIELD
    ]
    value["source_invocation_receipt_digest"] = source[
        "source_invocation_receipt_digest"
    ]
    value["effect_commit_authorization_record_digest"] = source[
        "effect_commit_authorization_record_digest"
    ]
    value["effect_commit_authorization_token_digest"] = source[
        "effect_commit_authorization_token_digest"
    ]
    value["adapter_result_envelope_digest"] = source[
        "adapter_result_envelope_digest"
    ]
    if recompute_operation:
        value["requested_effect_commit_operation_digest"] = (
            compute_requested_effect_commit_operation_digest(source)
        )
    value["exact_effect_commit_cycle_digest"] = (
        compute_exact_effect_commit_cycle_digest(source, value)
    )
    value["effect_commit_context_digest"] = compute_effect_commit_context_digest(
        value
    )
    return value


def _build(**overrides):
    source_override = overrides.pop(
        "source_effect_commit_authorization_receipt", None
    )
    source = deepcopy(
        _source_receipt() if source_override is None else source_override
    )

    context_override = overrides.pop("effect_commit_context", None)
    context = deepcopy(
        _context(source)
        if context_override is None and source
        else (context_override or {})
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v09-missing")
    context_digest = context.get(
        "effect_commit_context_digest", "context-v010-missing"
    )
    expected_source = overrides.pop(
        "expected_source_effect_commit_authorization_receipt_digest",
        source_digest,
    )
    expected_context = overrides.pop(
        "expected_effect_commit_context_digest", context_digest
    )
    policy = overrides.pop(
        "effect_commit_policy_digest", "actos-effect-commit-policy-v010"
    )
    owner = overrides.pop(
        "actos_effect_commit_responsibility_digest",
        "actos-effect-commit-owner-v010",
    )
    request_id = overrides.pop(
        "effect_commit_request_id", "actos-effect-commit-v010-001"
    )
    bundle = overrides.pop(
        "single_use_effect_commit_bundle_digest",
        compute_single_use_effect_commit_bundle_digest(
            source_effect_commit_authorization_receipt_digest=source_digest,
            expected_source_effect_commit_authorization_receipt_digest=(
                expected_source
            ),
            source_invocation_receipt_digest=source.get(
                "source_invocation_receipt_digest", "invocation-receipt-missing"
            ),
            effect_commit_authorization_record_digest=source.get(
                "effect_commit_authorization_record_digest",
                "authorization-record-missing",
            ),
            effect_commit_authorization_token_digest=source.get(
                "effect_commit_authorization_token_digest",
                "authorization-token-missing",
            ),
            adapter_result_envelope_digest=source.get(
                "adapter_result_envelope_digest", "result-envelope-missing"
            ),
            effect_commit_context_digest=context_digest,
            expected_effect_commit_context_digest=expected_context,
            requested_effect_commit_operation_digest=context.get(
                "requested_effect_commit_operation_digest",
                "effect-commit-operation-missing",
            ),
            exact_effect_commit_cycle_digest=context.get(
                "exact_effect_commit_cycle_digest", "effect-commit-cycle-missing"
            ),
            effect_commit_policy_digest=policy,
            actos_effect_commit_responsibility_digest=owner,
            effect_commit_request_id=request_id,
        ),
    )
    args = {
        "source_effect_commit_authorization_receipt": source,
        "expected_source_effect_commit_authorization_receipt_digest": (
            expected_source
        ),
        "effect_commit_context": context,
        "expected_effect_commit_context_digest": expected_context,
        "effect_commit_policy_digest": policy,
        "actos_effect_commit_responsibility_digest": owner,
        "effect_commit_request_id": request_id,
        "single_use_effect_commit_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_preserving_single_use_effect_commit_intake(**args)


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["actos_version"] == "v0.10"
    assert receipt["status"] == (
        "ACTOS_DUKKHA_PRESERVING_SINGLE_USE_EFFECT_COMMIT_RECORDED"
    )
    assert receipt["effect_commit_state_before"] == STATE_BEFORE
    assert receipt["effect_commit_state_after"] == STATE_AFTER
    assert receipt["effect_commit_authorization_consumed"] is True
    assert receipt["effect_commit_authorization_token_marked_consumed"] is True
    assert receipt[
        "single_use_effect_commit_authorization_replay_closed"
    ] is True
    assert receipt["effect_commit_authorization_double_consumed"] is False
    assert receipt["effect_commit_nonce_consumed"] is True
    assert receipt["effect_commit_nonce_replay_closed"] is True
    assert receipt["source_authorization_replay_closed"] is True
    assert receipt["exactly_one_effect_proposal_committed"] is True
    assert receipt["effect_commit_receipt_issued"] is True
    assert receipt["committed_effect_envelope_issued"] is True
    assert receipt["effect_commit_performed"] is True
    assert receipt["external_host_effect_intake_admitted"] is True
    assert receipt["external_host_effect_performed"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["persistent_world_state_unchanged"] is True
    assert receipt["observation_performed"] is False
    assert receipt["verification_completed"] is False
    assert receipt["verification_debt_open"] is True
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

    replay_token_context = _context(source)
    replay_token_context[
        "prior_consumed_effect_commit_authorization_token_digests"
    ] = [source["effect_commit_authorization_token_digest"]]
    replay_token_context = _redigest_context(source, replay_token_context)

    replay_nonce_context = _context(source)
    replay_nonce_context["prior_effect_commit_nonce_digests"] = [
        replay_nonce_context["effect_commit_nonce_digest"]
    ]
    replay_nonce_context = _redigest_context(source, replay_nonce_context)

    replay_source_context = _context(source)
    replay_source_context["prior_committed_authorization_receipt_digests"] = [
        source[SOURCE_DIGEST_FIELD]
    ]
    replay_source_context = _redigest_context(source, replay_source_context)

    changed_world_context = _context(source)
    changed_world_context["current_world_model_state_digest"] = "changed-world"
    changed_world_context = _redigest_context(source, changed_world_context)

    stale_context = _context(source)
    stale_context["effect_commit_epoch"] = 120
    stale_context = _redigest_context(source, stale_context)

    wrong_operation_context = _context(source)
    wrong_operation_context[
        "requested_effect_commit_operation_digest"
    ] = "wrong-operation"
    wrong_operation_context = _redigest_context(
        source, wrong_operation_context, recompute_operation=False
    )

    nonready_source = deepcopy(source)
    nonready_source["authorization_disposition"] = "world_refresh_required"
    nonready_source["effect_commit_authorization_admitted"] = False
    nonready_source["effect_commit_authorization_receipt_issued"] = False
    nonready_source["single_use_effect_commit_authorization_reserved"] = False
    nonready_source["effect_commit_intake_admitted"] = False
    nonready_source["effect_commit_state_after"] = "invoked_effect_not_committed"
    nonready_source = _redigest_source(nonready_source)

    empty_token_source = deepcopy(source)
    empty_token_source["effect_commit_authorization_token_digest"] = ""
    empty_token_source = _redigest_source(empty_token_source)

    tampered_token_source = deepcopy(source)
    tampered_token_source["effect_commit_authorization_token_digest"] = (
        "tampered-token"
    )
    tampered_token_source = _redigest_source(tampered_token_source)

    promoted_source = deepcopy(source)
    promoted_source["effect_commit_performed"] = True
    promoted_source = _redigest_source(promoted_source)

    scope_source = deepcopy(source)
    scope_source["effect_scope_exact"] = False
    scope_source = _redigest_source(scope_source)

    changed_record_source = deepcopy(source)
    changed_record_source["effect_commit_authorization_record"] = deepcopy(
        changed_record_source["effect_commit_authorization_record"]
    )
    changed_record_source["effect_commit_authorization_record"][
        "effect_commit_state"
    ] = "changed"
    changed_record_source = _redigest_source(changed_record_source)

    blocked = [
        _build(source_effect_commit_authorization_receipt={}),
        _build(effect_commit_context={}),
        _build(
            expected_source_effect_commit_authorization_receipt_digest="wrong"
        ),
        _build(expected_effect_commit_context_digest="wrong"),
        _build(single_use_effect_commit_bundle_digest="wrong"),
        _build(effect_commit_context=replay_token_context),
        _build(effect_commit_context=replay_nonce_context),
        _build(effect_commit_context=replay_source_context),
        _build(effect_commit_context=changed_world_context),
        _build(effect_commit_context=stale_context),
        _build(effect_commit_context=wrong_operation_context),
        _build(source_effect_commit_authorization_receipt=nonready_source),
        _build(source_effect_commit_authorization_receipt=empty_token_source),
        _build(source_effect_commit_authorization_receipt=tampered_token_source),
        _build(source_effect_commit_authorization_receipt=promoted_source),
        _build(source_effect_commit_authorization_receipt=scope_source),
        _build(source_effect_commit_authorization_receipt=changed_record_source),
    ]
    for result in blocked:
        assert result.status == STATUS_BLOCKED, result.receipt
        assert result.blockers
        assert result.receipt is None

    print(
        "PASS: ActOS v0.10 dukkha-preserving single-use effect commit "
        "intake validates ready commit and fail-closed replay/boundary paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
