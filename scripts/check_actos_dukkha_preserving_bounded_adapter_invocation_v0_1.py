#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_bounded_adapter_invocation_v0_1 import (
    ACTIVATION_DIGEST_FIELD,
    AUTHORIZATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    STATUS_READY,
    build_actos_dukkha_preserving_bounded_adapter_invocation,
    canonical_digest,
    compute_bounded_adapter_invocation_bundle_digest,
    compute_exact_invocation_cycle_digest,
    compute_invocation_context_digest,
    compute_invocation_intent_digest,
    compute_lease_reservation_digest,
    compute_requested_operation_digest,
)
from scripts.check_actos_dukkha_preserving_adapter_binding_authorization_intake_v0_1 import (
    _build as build_actos_v06_authorization,
)
from scripts.check_actos_dukkha_preserving_frontier_plan_activation_receipt_v0_1 import (
    _build as build_actos_v07_activation,
)


def _source_pair() -> tuple[dict, dict]:
    authorization_result = build_actos_v06_authorization()
    assert authorization_result.status == STATUS_READY, authorization_result.blockers
    assert authorization_result.receipt is not None
    authorization = deepcopy(authorization_result.receipt)

    activation_result = build_actos_v07_activation(
        source_authorization_receipt=authorization
    )
    assert activation_result.status == STATUS_READY, activation_result.blockers
    assert activation_result.receipt is not None
    activation = deepcopy(activation_result.receipt)
    return authorization, activation


def _redigest_activation(activation: dict) -> dict:
    value = deepcopy(activation)
    value.pop(ACTIVATION_DIGEST_FIELD, None)
    value[ACTIVATION_DIGEST_FIELD] = canonical_digest(value)
    return value


def _redigest_authorization(authorization: dict) -> dict:
    value = deepcopy(authorization)
    value.pop(AUTHORIZATION_DIGEST_FIELD, None)
    value[AUTHORIZATION_DIGEST_FIELD] = canonical_digest(value)
    return value


def _frontier_binding(activation: dict, authorization: dict) -> dict:
    return next(
        binding
        for binding in authorization["adapter_bindings"]
        if binding["materialization_candidate_id"]
        == activation["activated_frontier_candidate_id"]
    )


def _context(activation: dict, authorization: dict) -> dict:
    binding = _frontier_binding(activation, authorization)
    context = {
        "source_activation_receipt_digest": activation[ACTIVATION_DIGEST_FIELD],
        "source_authorization_receipt_digest": authorization[
            AUTHORIZATION_DIGEST_FIELD
        ],
        "requested_frontier_candidate_id": activation[
            "activated_frontier_candidate_id"
        ],
        "requested_frontier_adapter_id": activation[
            "activated_frontier_adapter_id"
        ],
        "requested_frontier_binding_digest": activation[
            "activated_frontier_binding_digest"
        ],
        "requested_frontier_lease_id": activation[
            "activated_frontier_lease_id"
        ],
        "lease_reservation_digest": compute_lease_reservation_digest(
            authorization
        ),
        "invocation_session_id": "actos-invocation-session-v08-001",
        "invocation_intent_digest": compute_invocation_intent_digest(
            activation, binding
        ),
        "invocation_nonce_digest": "actos-invocation-nonce-v08-001",
        "current_world_binding_digest": activation[
            "source_world_binding_digest"
        ],
        "current_world_model_state_digest": activation[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": activation[
            "source_world_model_revision"
        ],
        "current_world_lineage_digest": activation[
            "source_world_lineage_digest"
        ],
        "activation_receipt_observed_epoch": 103,
        "invocation_epoch": 104,
        "maximum_invocation_delay": 4,
        "prior_consumed_lease_reservation_digests": [],
        "prior_invocation_nonce_digests": [],
        "prior_invoked_frontier_candidate_ids": [],
        "requested_operation_digest": compute_requested_operation_digest(
            activation, binding
        ),
        "exact_invocation_cycle_digest": "",
    }
    context["exact_invocation_cycle_digest"] = (
        compute_exact_invocation_cycle_digest(
            activation, authorization, context
        )
    )
    context["invocation_context_digest"] = compute_invocation_context_digest(
        context
    )
    return context


def _redigest_context(
    activation: dict,
    authorization: dict,
    context: dict,
    *,
    recompute_operation: bool = True,
) -> dict:
    value = deepcopy(context)
    binding = _frontier_binding(activation, authorization)
    value["source_activation_receipt_digest"] = activation[
        ACTIVATION_DIGEST_FIELD
    ]
    value["source_authorization_receipt_digest"] = authorization[
        AUTHORIZATION_DIGEST_FIELD
    ]
    value["lease_reservation_digest"] = compute_lease_reservation_digest(
        authorization
    )
    value["invocation_intent_digest"] = compute_invocation_intent_digest(
        activation, binding
    )
    if recompute_operation:
        value["requested_operation_digest"] = compute_requested_operation_digest(
            activation, binding
        )
    value["exact_invocation_cycle_digest"] = (
        compute_exact_invocation_cycle_digest(
            activation, authorization, value
        )
    )
    value["invocation_context_digest"] = compute_invocation_context_digest(value)
    return value


def _build(**overrides):
    authorization_override = overrides.pop("source_authorization_receipt", None)
    activation_override = overrides.pop("source_activation_receipt", None)
    if authorization_override is None and activation_override is None:
        authorization, activation = _source_pair()
    else:
        if authorization_override is None:
            authorization, _ = _source_pair()
        else:
            authorization = deepcopy(authorization_override)
        if activation_override is None:
            if authorization:
                activation_result = build_actos_v07_activation(
                    source_authorization_receipt=authorization
                )
                activation = (
                    deepcopy(activation_result.receipt)
                    if activation_result.status == STATUS_READY
                    and activation_result.receipt is not None
                    else {}
                )
            else:
                activation = {}
        else:
            activation = deepcopy(activation_override)

    context_override = overrides.pop("invocation_context", None)
    context = deepcopy(
        _context(activation, authorization)
        if context_override is None and activation and authorization
        else (context_override or {})
    )
    activation_digest = activation.get(
        ACTIVATION_DIGEST_FIELD, "activation-v07-missing"
    )
    authorization_digest = authorization.get(
        AUTHORIZATION_DIGEST_FIELD, "authorization-v06-missing"
    )
    context_digest = context.get(
        "invocation_context_digest", "invocation-context-missing"
    )
    expected_activation = overrides.pop(
        "expected_source_activation_receipt_digest", activation_digest
    )
    expected_authorization = overrides.pop(
        "expected_source_authorization_receipt_digest", authorization_digest
    )
    expected_context = overrides.pop(
        "expected_invocation_context_digest", context_digest
    )
    policy = overrides.pop(
        "invocation_policy_digest", "actos-bounded-invocation-policy-v08"
    )
    owner = overrides.pop(
        "actos_invocation_responsibility_digest",
        "actos-bounded-invocation-owner-v08",
    )
    request_id = overrides.pop(
        "invocation_request_id", "actos-bounded-invocation-v08-001"
    )
    binding = (
        _frontier_binding(activation, authorization)
        if activation and authorization
        else {}
    )
    bundle = overrides.pop(
        "invocation_bundle_digest",
        compute_bounded_adapter_invocation_bundle_digest(
            source_activation_receipt_digest=activation_digest,
            expected_source_activation_receipt_digest=expected_activation,
            source_authorization_receipt_digest=authorization_digest,
            expected_source_authorization_receipt_digest=expected_authorization,
            source_activation_record_digest=activation.get(
                "activation_record_digest", "activation-record-missing"
            ),
            frontier_binding_digest=binding.get(
                "binding_digest", "binding-missing"
            ),
            lease_reservation_digest=context.get(
                "lease_reservation_digest", "reservation-missing"
            ),
            invocation_context_digest=context_digest,
            expected_invocation_context_digest=expected_context,
            requested_operation_digest=context.get(
                "requested_operation_digest", "operation-missing"
            ),
            exact_invocation_cycle_digest=context.get(
                "exact_invocation_cycle_digest", "cycle-missing"
            ),
            invocation_policy_digest=policy,
            actos_invocation_responsibility_digest=owner,
            invocation_request_id=request_id,
        ),
    )
    args = {
        "source_activation_receipt": activation,
        "expected_source_activation_receipt_digest": expected_activation,
        "source_authorization_receipt": authorization,
        "expected_source_authorization_receipt_digest": expected_authorization,
        "invocation_context": context,
        "expected_invocation_context_digest": expected_context,
        "invocation_policy_digest": policy,
        "actos_invocation_responsibility_digest": owner,
        "invocation_request_id": request_id,
        "invocation_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_preserving_bounded_adapter_invocation(**args)


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["actos_version"] == "v0.8"
    assert receipt["status"] == (
        "ACTOS_DUKKHA_PRESERVING_BOUNDED_ADAPTER_INVOCATION_RECORDED"
    )
    assert receipt["invocation_state_before"] == "activated_not_invoked"
    assert receipt["invocation_state_after"] == "invoked_effect_not_committed"
    assert receipt["adapter_invocation_performed"] is True
    assert receipt["adapter_host_invocation_performed"] is True
    assert receipt["exactly_one_adapter_invoked"] is True
    assert receipt["adapter_lease_reservation_consumed"] is True
    assert receipt["adapter_lease_use_consumed"] is True
    assert receipt["adapter_lease_double_decremented"] is False
    assert receipt["remaining_uses_at_invocation"] == receipt[
        "remaining_uses_after_reservation"
    ]
    assert receipt["invocation_nonce_replay_closed"] is True
    assert receipt["frontier_invocation_replay_closed"] is True
    assert receipt["effect_proposal_recorded"] is True
    assert receipt["effect_commit_required"] is True
    assert receipt["effect_commit_performed"] is False
    assert receipt["observation_intake_required"] is True
    assert receipt["verification_debt_open"] is True
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["execution_permission"] is False
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

    authorization, activation = _source_pair()
    reservation = compute_lease_reservation_digest(authorization)

    replay_reservation_context = _context(activation, authorization)
    replay_reservation_context[
        "prior_consumed_lease_reservation_digests"
    ] = [reservation]
    replay_reservation_context = _redigest_context(
        activation, authorization, replay_reservation_context
    )

    replay_nonce_context = _context(activation, authorization)
    replay_nonce_context["prior_invocation_nonce_digests"] = [
        replay_nonce_context["invocation_nonce_digest"]
    ]
    replay_nonce_context = _redigest_context(
        activation, authorization, replay_nonce_context
    )

    replay_frontier_context = _context(activation, authorization)
    replay_frontier_context["prior_invoked_frontier_candidate_ids"] = [
        activation["activated_frontier_candidate_id"]
    ]
    replay_frontier_context = _redigest_context(
        activation, authorization, replay_frontier_context
    )

    stale_context = _context(activation, authorization)
    stale_context["invocation_epoch"] = 112
    stale_context = _redigest_context(activation, authorization, stale_context)

    changed_world_context = _context(activation, authorization)
    changed_world_context["current_world_model_state_digest"] = "changed-world"
    changed_world_context = _redigest_context(
        activation, authorization, changed_world_context
    )

    wrong_operation_context = _context(activation, authorization)
    wrong_operation_context["requested_operation_digest"] = "wrong-operation"
    wrong_operation_context = _redigest_context(
        activation,
        authorization,
        wrong_operation_context,
        recompute_operation=False,
    )

    promoted_activation = deepcopy(activation)
    promoted_activation["adapter_invocation_performed"] = True
    promoted_activation = _redigest_activation(promoted_activation)

    consumed_lease_activation = deepcopy(activation)
    consumed_lease_activation["adapter_lease_use_consumed"] = True
    consumed_lease_activation = _redigest_activation(consumed_lease_activation)

    mismatched_authorization = deepcopy(authorization)
    mismatched_authorization["remaining_uses_after_reservation"] = 0
    mismatched_authorization = _redigest_authorization(mismatched_authorization)

    blocked = [
        _build(source_activation_receipt={}),
        _build(source_authorization_receipt={}),
        _build(invocation_context={}),
        _build(expected_source_activation_receipt_digest="wrong"),
        _build(expected_source_authorization_receipt_digest="wrong"),
        _build(expected_invocation_context_digest="wrong"),
        _build(invocation_bundle_digest="wrong"),
        _build(invocation_context=replay_reservation_context),
        _build(invocation_context=replay_nonce_context),
        _build(invocation_context=replay_frontier_context),
        _build(invocation_context=stale_context),
        _build(invocation_context=changed_world_context),
        _build(invocation_context=wrong_operation_context),
        _build(
            source_activation_receipt=promoted_activation,
            source_authorization_receipt=authorization,
        ),
        _build(
            source_activation_receipt=consumed_lease_activation,
            source_authorization_receipt=authorization,
        ),
        _build(
            source_activation_receipt=activation,
            source_authorization_receipt=mismatched_authorization,
        ),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.receipt is None

    print(
        "PASS: ActOS Dukkha-Preserving Bounded Adapter Invocation "
        "Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
