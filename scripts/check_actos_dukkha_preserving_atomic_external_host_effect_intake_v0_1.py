#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_atomic_external_host_effect_intake_v0_1 import (
    HOST_OUTCOME,
    HOST_RECEIPT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATE_AFTER,
    STATUS_BLOCKED,
    STATUS_READY,
    build_actos_dukkha_preserving_atomic_external_host_effect_intake,
    canonical_digest,
    compute_atomic_external_host_effect_bundle_digest,
    compute_exact_host_effect_intake_cycle_digest,
    compute_external_host_effect_application_receipt_digest,
    compute_host_effect_intake_context_digest,
    compute_host_effect_operation_digest,
    compute_requested_host_effect_intake_operation_digest,
)
from scripts.check_actos_dukkha_preserving_single_use_effect_commit_intake_v0_1 import (
    _build as build_actos_v010_effect_commit,
)


def _source_receipt() -> dict:
    result = build_actos_v010_effect_commit()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _host_receipt(source: dict) -> dict:
    envelope = source["committed_effect_envelope"]
    receipt = {
        "source_effect_commit_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "effect_commit_record_digest": source["effect_commit_record_digest"],
        "committed_effect_envelope_digest": source[
            "committed_effect_envelope_digest"
        ],
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(envelope["requested_effect_tags"]),
        "host_effect_operation_digest": compute_host_effect_operation_digest(source),
        "host_effect_session_id": "actos-host-driver-session-v011-001",
        "host_effect_nonce_digest": "actos-host-driver-nonce-v011-001",
        "host_driver_id": "actos-host-driver-v011",
        "host_target_digest": "actos-host-target-v011",
        "host_effect_started_epoch": 110,
        "host_effect_completed_epoch": 111,
        "maximum_host_effect_duration": 4,
        "host_effect_outcome": HOST_OUTCOME,
        "exactly_one_effect_applied": True,
        "tool_invocation_performed": True,
        "external_side_effect_performed": True,
        "compensation_route_digest": "actos-compensation-route-v011",
        "observation_route_digest": "observeos-host-effect-route-v011",
        "verification_route_digest": "verifyos-host-effect-route-v011",
    }
    receipt[HOST_RECEIPT_DIGEST_FIELD] = (
        compute_external_host_effect_application_receipt_digest(receipt)
    )
    return receipt


def _redigest_host_receipt(
    source: dict, host_receipt: dict, *, recompute_operation: bool = True
) -> dict:
    value = deepcopy(host_receipt)
    value["source_effect_commit_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["effect_commit_record_digest"] = source["effect_commit_record_digest"]
    value["committed_effect_envelope_digest"] = source[
        "committed_effect_envelope_digest"
    ]
    value["frontier_materialization_candidate_id"] = source[
        "invoked_frontier_candidate_id"
    ]
    value["frontier_adapter_id"] = source["invoked_frontier_adapter_id"]
    value["frontier_binding_digest"] = source["invoked_frontier_binding_digest"]
    value["requested_effect_tags"] = list(
        source["committed_effect_envelope"]["requested_effect_tags"]
    )
    if recompute_operation:
        value["host_effect_operation_digest"] = compute_host_effect_operation_digest(
            source
        )
    value.pop(HOST_RECEIPT_DIGEST_FIELD, None)
    value[HOST_RECEIPT_DIGEST_FIELD] = (
        compute_external_host_effect_application_receipt_digest(value)
    )
    return value


def _context(source: dict, host_receipt: dict) -> dict:
    context = {
        "source_effect_commit_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "effect_commit_record_digest": source["effect_commit_record_digest"],
        "committed_effect_envelope_digest": source[
            "committed_effect_envelope_digest"
        ],
        HOST_RECEIPT_DIGEST_FIELD: host_receipt[HOST_RECEIPT_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_commit_receipt_observed_epoch": 111,
        "host_effect_intake_epoch": 112,
        "maximum_host_effect_intake_delay": 4,
        "host_effect_intake_session_id": "actos-host-effect-intake-v011-001",
        "host_effect_intake_nonce_digest": "actos-host-effect-intake-nonce-v011-001",
        "prior_host_effect_intake_session_ids": [],
        "prior_host_effect_application_receipt_digests": [],
        "prior_host_effect_intake_nonce_digests": [],
        "prior_applied_committed_effect_envelope_digests": [],
        "requested_host_effect_intake_operation_digest": (
            compute_requested_host_effect_intake_operation_digest(
                source, host_receipt
            )
        ),
        "exact_host_effect_intake_cycle_digest": "",
    }
    context["exact_host_effect_intake_cycle_digest"] = (
        compute_exact_host_effect_intake_cycle_digest(
            source, host_receipt, context
        )
    )
    context["host_effect_intake_context_digest"] = (
        compute_host_effect_intake_context_digest(context)
    )
    return context


def _redigest_context(
    source: dict,
    host_receipt: dict,
    context: dict,
    *,
    recompute_operation: bool = True,
) -> dict:
    value = deepcopy(context)
    value["source_effect_commit_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["effect_commit_record_digest"] = source["effect_commit_record_digest"]
    value["committed_effect_envelope_digest"] = source[
        "committed_effect_envelope_digest"
    ]
    value[HOST_RECEIPT_DIGEST_FIELD] = host_receipt[HOST_RECEIPT_DIGEST_FIELD]
    if recompute_operation:
        value["requested_host_effect_intake_operation_digest"] = (
            compute_requested_host_effect_intake_operation_digest(
                source, host_receipt
            )
        )
    value["exact_host_effect_intake_cycle_digest"] = (
        compute_exact_host_effect_intake_cycle_digest(
            source, host_receipt, value
        )
    )
    value["host_effect_intake_context_digest"] = (
        compute_host_effect_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    source_override = overrides.pop("source_effect_commit_receipt", None)
    source = deepcopy(
        _source_receipt() if source_override is None else source_override
    )

    host_override = overrides.pop(
        "external_host_effect_application_receipt", None
    )
    host_receipt = deepcopy(
        _host_receipt(source)
        if host_override is None and source
        else (host_override or {})
    )

    context_override = overrides.pop("host_effect_intake_context", None)
    context = deepcopy(
        _context(source, host_receipt)
        if context_override is None and source and host_receipt
        else (context_override or {})
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v010-missing")
    host_digest = host_receipt.get(
        HOST_RECEIPT_DIGEST_FIELD, "host-receipt-v011-missing"
    )
    context_digest = context.get(
        "host_effect_intake_context_digest", "context-v011-missing"
    )
    expected_source = overrides.pop(
        "expected_source_effect_commit_receipt_digest", source_digest
    )
    expected_host = overrides.pop(
        "expected_external_host_effect_application_receipt_digest", host_digest
    )
    expected_context = overrides.pop(
        "expected_host_effect_intake_context_digest", context_digest
    )
    policy = overrides.pop(
        "host_effect_intake_policy_digest",
        "actos-atomic-external-host-effect-policy-v011",
    )
    owner = overrides.pop(
        "actos_host_effect_intake_responsibility_digest",
        "actos-atomic-external-host-effect-owner-v011",
    )
    request_id = overrides.pop(
        "host_effect_intake_request_id",
        "actos-atomic-external-host-effect-v011-001",
    )
    bundle = overrides.pop(
        "atomic_external_host_effect_bundle_digest",
        compute_atomic_external_host_effect_bundle_digest(
            source_effect_commit_receipt_digest=source_digest,
            expected_source_effect_commit_receipt_digest=expected_source,
            effect_commit_record_digest=source.get(
                "effect_commit_record_digest", "commit-record-missing"
            ),
            committed_effect_envelope_digest=source.get(
                "committed_effect_envelope_digest", "committed-envelope-missing"
            ),
            authorization_consumption_record_digest=source.get(
                "authorization_consumption_record_digest",
                "authorization-consumption-missing",
            ),
            external_host_effect_application_receipt_digest=host_digest,
            expected_external_host_effect_application_receipt_digest=expected_host,
            host_effect_intake_context_digest=context_digest,
            expected_host_effect_intake_context_digest=expected_context,
            requested_host_effect_intake_operation_digest=context.get(
                "requested_host_effect_intake_operation_digest",
                "host-intake-operation-missing",
            ),
            exact_host_effect_intake_cycle_digest=context.get(
                "exact_host_effect_intake_cycle_digest",
                "host-intake-cycle-missing",
            ),
            host_effect_intake_policy_digest=policy,
            actos_host_effect_intake_responsibility_digest=owner,
            host_effect_intake_request_id=request_id,
        ),
    )
    args = {
        "source_effect_commit_receipt": source,
        "expected_source_effect_commit_receipt_digest": expected_source,
        "external_host_effect_application_receipt": host_receipt,
        "expected_external_host_effect_application_receipt_digest": expected_host,
        "host_effect_intake_context": context,
        "expected_host_effect_intake_context_digest": expected_context,
        "host_effect_intake_policy_digest": policy,
        "actos_host_effect_intake_responsibility_digest": owner,
        "host_effect_intake_request_id": request_id,
        "atomic_external_host_effect_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_preserving_atomic_external_host_effect_intake(
        **args
    )


def _assert_blocked(result, blocker: str) -> None:
    assert result.status == STATUS_BLOCKED
    assert result.receipt is None
    assert blocker in result.blockers, result.blockers


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["host_effect_state_after"] == STATE_AFTER
    assert receipt["external_host_effect_performed"] is True
    assert receipt["host_driver_tool_invocation_performed"] is True
    assert receipt["kernel_tool_invocation_performed"] is False
    assert receipt["persistent_world_model_state_unchanged"] is True
    assert receipt["world_fact_confirmed"] is False
    assert receipt["observation_intake_admitted"] is True
    assert receipt["observation_performed"] is False
    assert receipt["verification_completed"] is False
    assert receipt["verification_debt_open"] is True
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {k: v for k, v in receipt.items() if k != RECEIPT_DIGEST_FIELD}
    )

    _assert_blocked(
        _build(source_effect_commit_receipt={}),
        "source_effect_commit_receipt_missing",
    )
    _assert_blocked(
        _build(external_host_effect_application_receipt={}),
        "external_host_effect_application_receipt_missing",
    )
    _assert_blocked(
        _build(host_effect_intake_context={}),
        "host_effect_intake_context_missing",
    )
    _assert_blocked(
        _build(expected_source_effect_commit_receipt_digest="wrong-source"),
        "source_effect_commit_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(
            expected_external_host_effect_application_receipt_digest="wrong-host"
        ),
        "external_host_effect_application_receipt_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(expected_host_effect_intake_context_digest="wrong-context"),
        "host_effect_intake_context_expected_binding_mismatch",
    )

    source = _source_receipt()
    source["external_host_effect_performed"] = True
    source = _redigest_source(source)
    _assert_blocked(
        _build(source_effect_commit_receipt=source),
        "source_boundary_external_host_effect_performed_promoted",
    )

    source = _source_receipt()
    source["committed_effect_envelope"]["external_host_effect_state"] = "applied"
    source["committed_effect_envelope_digest"] = canonical_digest(
        source["committed_effect_envelope"]
    )
    source = _redigest_source(source)
    _assert_blocked(
        _build(source_effect_commit_receipt=source),
        "source_committed_effect_envelope_external_host_effect_state_mismatch",
    )

    source = _source_receipt()
    host_receipt = _host_receipt(source)
    host_receipt["host_effect_outcome"] = "unknown"
    host_receipt = _redigest_host_receipt(source, host_receipt)
    _assert_blocked(
        _build(external_host_effect_application_receipt=host_receipt),
        "external_host_effect_application_host_effect_outcome_mismatch",
    )

    host_receipt = _host_receipt(source)
    host_receipt["exactly_one_effect_applied"] = False
    host_receipt = _redigest_host_receipt(source, host_receipt)
    _assert_blocked(
        _build(external_host_effect_application_receipt=host_receipt),
        "external_host_effect_application_exactly_one_effect_applied_mismatch",
    )

    host_receipt = _host_receipt(source)
    host_receipt["tool_invocation_performed"] = False
    host_receipt = _redigest_host_receipt(source, host_receipt)
    _assert_blocked(
        _build(external_host_effect_application_receipt=host_receipt),
        "external_host_effect_application_tool_invocation_performed_mismatch",
    )

    host_receipt = _host_receipt(source)
    host_receipt["host_effect_operation_digest"] = "tampered-operation"
    host_receipt = _redigest_host_receipt(
        source, host_receipt, recompute_operation=False
    )
    _assert_blocked(
        _build(external_host_effect_application_receipt=host_receipt),
        "external_host_effect_application_host_effect_operation_digest_mismatch",
    )

    host_receipt = _host_receipt(source)
    host_receipt["host_effect_completed_epoch"] = 200
    host_receipt = _redigest_host_receipt(source, host_receipt)
    _assert_blocked(
        _build(external_host_effect_application_receipt=host_receipt),
        "external_host_effect_application_duration_invalid",
    )

    host_receipt = _host_receipt(source)
    context = _context(source, host_receipt)
    context["current_world_model_revision"] += 1
    context = _redigest_context(source, host_receipt, context)
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "host_effect_intake_world_refresh_required",
    )

    context = _context(source, host_receipt)
    context["host_effect_intake_epoch"] = 200
    context = _redigest_context(source, host_receipt, context)
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "host_effect_intake_expired",
    )

    context = _context(source, host_receipt)
    context["prior_host_effect_intake_session_ids"] = [
        context["host_effect_intake_session_id"]
    ]
    context = _redigest_context(source, host_receipt, context)
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "host_effect_intake_session_replay_rejected",
    )

    context = _context(source, host_receipt)
    context["prior_host_effect_application_receipt_digests"] = [
        host_receipt[HOST_RECEIPT_DIGEST_FIELD]
    ]
    context = _redigest_context(source, host_receipt, context)
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "host_effect_application_receipt_replay_rejected",
    )

    context = _context(source, host_receipt)
    context["prior_host_effect_intake_nonce_digests"] = [
        context["host_effect_intake_nonce_digest"]
    ]
    context = _redigest_context(source, host_receipt, context)
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "host_effect_intake_nonce_replay_rejected",
    )

    context = _context(source, host_receipt)
    context["prior_applied_committed_effect_envelope_digests"] = [
        source["committed_effect_envelope_digest"]
    ]
    context = _redigest_context(source, host_receipt, context)
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "committed_effect_envelope_replay_rejected",
    )

    context = _context(source, host_receipt)
    context["requested_host_effect_intake_operation_digest"] = "tampered"
    context = _redigest_context(
        source, host_receipt, context, recompute_operation=False
    )
    _assert_blocked(
        _build(host_effect_intake_context=context),
        "host_effect_intake_context_operation_digest_mismatch",
    )

    _assert_blocked(
        _build(atomic_external_host_effect_bundle_digest="wrong-bundle"),
        "atomic_external_host_effect_bundle_digest_mismatch",
    )

    print(
        "PASS: ActOS v0.11 dukkha-preserving atomic external host-effect "
        "intake actual-chain validation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
