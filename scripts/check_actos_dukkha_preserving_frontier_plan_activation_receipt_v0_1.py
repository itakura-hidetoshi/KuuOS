#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_frontier_plan_activation_receipt_v0_1 import (
    RECEIPT_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATUS_READY,
    build_actos_dukkha_preserving_frontier_plan_activation_receipt,
    canonical_digest,
    compute_activation_context_digest,
    compute_exact_activation_cycle_digest,
    compute_frontier_activation_bundle_digest,
    compute_requested_state_transition_digest,
)
from scripts.check_actos_dukkha_preserving_adapter_binding_authorization_intake_v0_1 import (
    _build as build_actos_v06_authorization,
)


def _source_receipt() -> dict:
    result = build_actos_v06_authorization()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _context(source: dict) -> dict:
    record = source["authorization_record"]
    frontier_binding = next(
        binding
        for binding in source["adapter_bindings"]
        if binding["materialization_candidate_id"]
        == source["activation_frontier_candidate_id"]
    )
    context = {
        "source_authorization_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "activation_token_digest": source[
            "activation_authorization_token_digest"
        ],
        "requested_frontier_candidate_id": source[
            "activation_frontier_candidate_id"
        ],
        "requested_frontier_binding_digest": frontier_binding["binding_digest"],
        "requested_frontier_adapter_id": source["frontier_adapter_id"],
        "requested_frontier_lease_id": source["frontier_lease_id"],
        "activation_session_id": record["session_id"],
        "activation_intent_digest": record["intent_digest"],
        "authorization_nonce_digest": record["authorization_nonce_digest"],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "authorization_receipt_observed_epoch": 102,
        "activation_epoch": 103,
        "maximum_activation_delay": 4,
        "prior_consumed_authorization_token_digests": [],
        "prior_activated_frontier_candidate_ids": [],
        "requested_state_transition_digest": (
            compute_requested_state_transition_digest(source)
        ),
        "exact_activation_cycle_digest": "",
    }
    context["exact_activation_cycle_digest"] = (
        compute_exact_activation_cycle_digest(source, context)
    )
    context["activation_context_digest"] = compute_activation_context_digest(
        context
    )
    return context


def _redigest_context(source: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["requested_state_transition_digest"] = (
        compute_requested_state_transition_digest(source)
    )
    value["exact_activation_cycle_digest"] = (
        compute_exact_activation_cycle_digest(source, value)
    )
    value["activation_context_digest"] = compute_activation_context_digest(value)
    return value


def _build(**overrides):
    source_override = overrides.pop("source_authorization_receipt", None)
    source = deepcopy(
        _source_receipt() if source_override is None else source_override
    )
    context_override = overrides.pop("activation_context", None)
    context = deepcopy(
        _context(source)
        if context_override is None and source
        else (context_override or {})
    )
    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v06-missing")
    context_digest = context.get(
        "activation_context_digest", "activation-context-missing"
    )
    expected_source = overrides.pop(
        "expected_source_authorization_receipt_digest", source_digest
    )
    expected_context = overrides.pop(
        "expected_activation_context_digest", context_digest
    )
    policy = overrides.pop(
        "activation_policy_digest", "actos-frontier-activation-policy-v07"
    )
    owner = overrides.pop(
        "actos_activation_responsibility_digest",
        "actos-frontier-activation-owner-v07",
    )
    request_id = overrides.pop(
        "activation_request_id", "actos-frontier-activation-v07-001"
    )
    bundle = overrides.pop(
        "activation_bundle_digest",
        compute_frontier_activation_bundle_digest(
            source_authorization_receipt_digest=source_digest,
            expected_source_authorization_receipt_digest=expected_source,
            activation_authorization_token_digest=source.get(
                "activation_authorization_token_digest", "token-missing"
            ),
            authorization_record_digest=source.get(
                "authorization_record_digest", "record-missing"
            ),
            activation_context_digest=context_digest,
            expected_activation_context_digest=expected_context,
            requested_state_transition_digest=context.get(
                "requested_state_transition_digest", "transition-missing"
            ),
            exact_activation_cycle_digest=context.get(
                "exact_activation_cycle_digest", "cycle-missing"
            ),
            activation_policy_digest=policy,
            actos_activation_responsibility_digest=owner,
            activation_request_id=request_id,
        ),
    )
    args = {
        "source_authorization_receipt": source,
        "expected_source_authorization_receipt_digest": expected_source,
        "activation_context": context,
        "expected_activation_context_digest": expected_context,
        "activation_policy_digest": policy,
        "actos_activation_responsibility_digest": owner,
        "activation_request_id": request_id,
        "activation_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_preserving_frontier_plan_activation_receipt(
        **args
    )


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["actos_version"] == "v0.7"
    assert receipt["status"] == (
        "ACTOS_DUKKHA_PRESERVING_FRONTIER_PLAN_ACTIVATION_READY"
    )
    assert receipt["activation_authorization_consumed"] is True
    assert receipt["activation_authorization_token_marked_consumed"] is True
    assert receipt["single_use_authorization_replay_closed"] is True
    assert receipt["plan_activation_performed"] is True
    assert receipt["frontier_candidate_activated"] is True
    assert receipt["exactly_one_frontier_activated"] is True
    assert receipt["activation_state_before"] == "bound_not_invoked"
    assert receipt["activation_state_after"] == "activated_not_invoked"
    assert receipt["adapter_invocation_intake_admitted"] is True
    assert receipt["adapter_lease_use_consumed"] is False
    assert receipt["adapter_invocation_performed"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["execution_permission"] is False
    assert receipt["persistent_world_state_unchanged"] is True
    assert receipt["active_now"] is False
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
    replay_token_context["prior_consumed_authorization_token_digests"] = [
        source["activation_authorization_token_digest"]
    ]
    replay_token_context = _redigest_context(source, replay_token_context)

    replay_frontier_context = _context(source)
    replay_frontier_context["prior_activated_frontier_candidate_ids"] = [
        source["activation_frontier_candidate_id"]
    ]
    replay_frontier_context = _redigest_context(source, replay_frontier_context)

    stale_context = _context(source)
    stale_context["activation_epoch"] = 110
    stale_context = _redigest_context(source, stale_context)

    changed_world_context = _context(source)
    changed_world_context["current_world_model_state_digest"] = "changed-world"
    changed_world_context = _redigest_context(source, changed_world_context)

    bad_token_context = _context(source)
    bad_token_context["activation_token_digest"] = "wrong-token"
    bad_token_context = _redigest_context(source, bad_token_context)

    promoted_source = _source_receipt()
    promoted_source["adapter_invocation_performed"] = True
    promoted_source = _redigest_source(promoted_source)

    nonready_source = _source_receipt()
    nonready_source["authorization_disposition"] = "world_refresh_required"
    nonready_source["activation_authorization_admitted"] = False
    nonready_source["activation_authorization_receipt_issued"] = False
    nonready_source["single_use_authorization_reserved"] = False
    nonready_source["activation_authorization_token_digest"] = ""
    nonready_source = _redigest_source(nonready_source)

    blocked = [
        _build(source_authorization_receipt={}),
        _build(activation_context={}),
        _build(expected_source_authorization_receipt_digest="wrong"),
        _build(expected_activation_context_digest="wrong"),
        _build(activation_bundle_digest="wrong"),
        _build(activation_context=replay_token_context),
        _build(activation_context=replay_frontier_context),
        _build(activation_context=stale_context),
        _build(activation_context=changed_world_context),
        _build(activation_context=bad_token_context),
        _build(source_authorization_receipt=promoted_source),
        _build(source_authorization_receipt=nonready_source),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.receipt is None

    print(
        "PASS: ActOS Dukkha-Preserving Frontier Plan Activation "
        "Receipt Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
