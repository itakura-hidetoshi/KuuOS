#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_adapter_binding_authorization_intake_v0_1 import (
    DISPOSITION_FRESHNESS_REFRESH,
    DISPOSITION_LEASE_REFRESH,
    DISPOSITION_READY,
    DISPOSITION_REGISTRY_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REVERIFY,
    DISPOSITION_WORLD_REFRESH,
    RECEIPT_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATUS_READY,
    build_actos_dukkha_preserving_adapter_binding_authorization_intake,
    canonical_digest,
    compute_adapter_binding_authorization_bundle_digest,
    compute_authorization_context_digest,
    compute_binding_scope_digest,
    compute_effect_ceiling_digest,
    compute_exact_act_cycle_digest,
    compute_exact_intent_digest,
    compute_freshness_observation_digest,
    compute_registry_snapshot_digest,
)
from scripts.check_actos_dukkha_supported_bounded_plan_materialization_intake_v0_1 import (
    _build as build_actos_v05_receipt,
)


ADAPTER_IDS = {
    "analysis_candidate": "adapter.internal.analysis.v01",
    "bounded_hold_candidate": "adapter.internal.hold.v01",
    "condition_reassessment_candidate": "adapter.internal.condition-reassessment.v01",
    "evidence_collection_candidate": "adapter.internal.evidence-collector.v01",
    "review_checkpoint_candidate": "adapter.internal.review-checkpoint.v01",
    "reversible_preparation_candidate": "adapter.internal.reversible-preparer.v01",
    "revision_request_candidate": "adapter.internal.revision-request.v01",
    "termination_candidate": "adapter.internal.termination.v01",
}


def _source_receipt() -> dict:
    result = build_actos_v05_receipt()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _registry(source: dict) -> dict:
    classes_to_effects: dict[str, set[str]] = {}
    for candidate in source["materialization_candidates"]:
        classes_to_effects.setdefault(candidate["materialization_class"], set()).update(
            candidate["effect_tags"]
        )
    entries = []
    for materialization_class in sorted(classes_to_effects):
        adapter_id = ADAPTER_IDS[materialization_class]
        entry = {
            "adapter_id": adapter_id,
            "adapter_class": "internal_bounded_adapter",
            "supported_materialization_classes": [materialization_class],
            "capability_digest": f"capability-{materialization_class}-v01",
            "scope_policy_digest": f"scope-policy-{materialization_class}-v01",
            "effect_ceiling_tags": sorted(classes_to_effects[materialization_class]),
            "active": True,
            "revoked": False,
            "lease_id": f"lease-{adapter_id}",
            "remaining_uses": 3,
        }
        entry["entry_digest"] = canonical_digest(entry)
        entries.append(entry)
    snapshot = {
        "registry_version": "v0.1",
        "issued_epoch": 100,
        "entries": entries,
    }
    snapshot["registry_snapshot_digest"] = compute_registry_snapshot_digest(snapshot)
    return snapshot


def _bindings(source: dict, registry: dict) -> list[dict]:
    entries = {entry["adapter_id"]: entry for entry in registry["entries"]}
    result = []
    for candidate in source["materialization_candidates"]:
        adapter_id = ADAPTER_IDS[candidate["materialization_class"]]
        entry = entries[adapter_id]
        binding = {
            "materialization_candidate_id": candidate[
                "materialization_candidate_id"
            ],
            "adapter_id": adapter_id,
            "adapter_registry_entry_digest": entry["entry_digest"],
            "capability_digest": entry["capability_digest"],
            "scope_digest": compute_binding_scope_digest(candidate),
            "effect_ceiling_digest": compute_effect_ceiling_digest(
                candidate, entry
            ),
            "lease_id": entry["lease_id"],
            "requested_effect_tags": list(candidate["effect_tags"]),
            "binding_state": "bound_not_invoked",
        }
        binding["binding_digest"] = canonical_digest(binding)
        result.append(binding)
    return result


def _context(
    source: dict,
    *,
    completed: list[str] | None = None,
    verifyos_step_reverification_digest: str = "",
) -> dict:
    completed_ids = list(completed or [])
    frontier = source["materialization_candidates"][len(completed_ids)]
    context = {
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_observed_epoch": 100,
        "current_epoch": 102,
        "maximum_freshness_age": 4,
        "completed_materialization_candidate_ids": completed_ids,
        "requested_frontier_candidate_id": frontier[
            "materialization_candidate_id"
        ],
        "session_id": "actos-session-v06-001",
        "intent_digest": "",
        "authorization_nonce_digest": "authorization-nonce-v06-001",
        "prior_session_ids": [],
        "prior_intent_digests": [],
        "prior_authorization_nonce_digests": [],
        "verifyos_step_reverification_digest": (
            verifyos_step_reverification_digest
        ),
        "freshness_observation_digest": "",
        "exact_act_cycle_digest": "",
    }
    context["intent_digest"] = compute_exact_intent_digest(source, frontier)
    context["freshness_observation_digest"] = (
        compute_freshness_observation_digest(source, context)
    )
    context["exact_act_cycle_digest"] = compute_exact_act_cycle_digest(
        source, context, frontier
    )
    context["authorization_context_digest"] = (
        compute_authorization_context_digest(context)
    )
    return context


def _redigest_context(source: dict, context: dict) -> dict:
    value = deepcopy(context)
    completed = value["completed_materialization_candidate_ids"]
    frontier = source["materialization_candidates"][len(completed)]
    value["requested_frontier_candidate_id"] = frontier[
        "materialization_candidate_id"
    ]
    value["intent_digest"] = compute_exact_intent_digest(source, frontier)
    value["freshness_observation_digest"] = (
        compute_freshness_observation_digest(source, value)
    )
    value["exact_act_cycle_digest"] = compute_exact_act_cycle_digest(
        source, value, frontier
    )
    value["authorization_context_digest"] = (
        compute_authorization_context_digest(value)
    )
    return value


def _redigest_registry(registry: dict) -> dict:
    value = deepcopy(registry)
    for entry in value["entries"]:
        entry.pop("entry_digest", None)
        entry["entry_digest"] = canonical_digest(entry)
    value["entries"] = sorted(value["entries"], key=lambda item: item["adapter_id"])
    value["registry_snapshot_digest"] = compute_registry_snapshot_digest(value)
    return value


def _build(**overrides):
    source_override = overrides.pop("source_materialization_receipt", None)
    source = deepcopy(
        _source_receipt() if source_override is None else source_override
    )
    registry_override = overrides.pop("adapter_registry_snapshot", None)
    registry = deepcopy(
        _registry(source) if registry_override is None and source else (
            registry_override or {}
        )
    )
    binding_override = overrides.pop("adapter_bindings", None)
    bindings = deepcopy(
        _bindings(source, registry)
        if binding_override is None and source and registry
        else (binding_override or [])
    )
    context_override = overrides.pop("authorization_context", None)
    context = deepcopy(
        _context(source)
        if context_override is None and source
        else (context_override or {})
    )
    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v05-missing")
    registry_digest = registry.get(
        "registry_snapshot_digest", "registry-missing"
    )
    context_digest = context.get(
        "authorization_context_digest", "context-missing"
    )
    expected_source = overrides.pop(
        "expected_source_materialization_receipt_digest", source_digest
    )
    expected_registry = overrides.pop(
        "expected_adapter_registry_snapshot_digest", registry_digest
    )
    expected_context = overrides.pop(
        "expected_authorization_context_digest", context_digest
    )
    policy = overrides.pop(
        "authorization_policy_digest", "actos-authorization-policy-v06"
    )
    owner = overrides.pop(
        "actos_authorization_responsibility_digest",
        "actos-authorization-owner-v06",
    )
    request_id = overrides.pop(
        "authorization_request_id", "actos-authorization-v06-001"
    )
    binding_set_digest = canonical_digest(bindings)
    bundle = overrides.pop(
        "authorization_bundle_digest",
        compute_adapter_binding_authorization_bundle_digest(
            source_materialization_receipt_digest=source_digest,
            expected_source_materialization_receipt_digest=expected_source,
            adapter_registry_snapshot_digest=registry_digest,
            expected_adapter_registry_snapshot_digest=expected_registry,
            adapter_binding_set_digest=binding_set_digest,
            authorization_context_digest=context_digest,
            expected_authorization_context_digest=expected_context,
            authorization_policy_digest=policy,
            actos_authorization_responsibility_digest=owner,
            authorization_request_id=request_id,
        ),
    )
    args = {
        "source_materialization_receipt": source,
        "expected_source_materialization_receipt_digest": expected_source,
        "adapter_registry_snapshot": registry,
        "expected_adapter_registry_snapshot_digest": expected_registry,
        "adapter_bindings": bindings,
        "authorization_context": context,
        "expected_authorization_context_digest": expected_context,
        "authorization_policy_digest": policy,
        "actos_authorization_responsibility_digest": owner,
        "authorization_request_id": request_id,
        "authorization_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_preserving_adapter_binding_authorization_intake(
        **args
    )


def _assert_not_authorized(result, disposition: str) -> None:
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    assert result.receipt["authorization_disposition"] == disposition
    assert result.receipt["activation_authorization_admitted"] is False
    assert result.receipt["activation_authorization_receipt_issued"] is False
    assert result.receipt["adapter_invocation_performed"] is False
    assert result.receipt["execution_permission"] is False


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["actos_version"] == "v0.6"
    assert receipt["status"] == (
        "ACTOS_DUKKHA_PRESERVING_ADAPTER_BINDING_AUTHORIZATION_ROUTED"
    )
    assert receipt["authorization_disposition"] == DISPOSITION_READY
    assert receipt["activation_authorization_admitted"] is True
    assert receipt["activation_authorization_receipt_issued"] is True
    assert receipt["single_use_authorization_reserved"] is True
    assert receipt["remaining_uses_after_reservation"] + 1 == (
        receipt["remaining_uses_before_reservation"]
    )
    assert receipt["adapter_binding_count"] == 4
    assert receipt["all_materialization_candidates_bound"] is True
    assert receipt["one_to_one_candidate_binding_preserved"] is True
    assert receipt["dukkha_reduction_support_preserved"] is True
    assert receipt["protected_group_nonexternalization_preserved"] is True
    assert receipt["future_nonexternalization_preserved"] is True
    assert receipt["plan_activated"] is False
    assert receipt["adapter_invocation_performed"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["execution_permission"] is False
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: value
            for key, value in receipt.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )

    source = _source_receipt()
    registry = _registry(source)

    world_context = _context(source)
    world_context["current_world_model_state_digest"] = "world-state-changed"
    world_context = _redigest_context(source, world_context)
    _assert_not_authorized(
        _build(authorization_context=world_context),
        DISPOSITION_WORLD_REFRESH,
    )

    stale_context = _context(source)
    stale_context["current_epoch"] = 110
    stale_context = _redigest_context(source, stale_context)
    _assert_not_authorized(
        _build(authorization_context=stale_context),
        DISPOSITION_FRESHNESS_REFRESH,
    )

    replay_context = _context(source)
    replay_context["prior_session_ids"] = [replay_context["session_id"]]
    replay_context = _redigest_context(source, replay_context)
    _assert_not_authorized(
        _build(authorization_context=replay_context),
        DISPOSITION_REPLAY_REJECTED,
    )

    revoked_registry = deepcopy(registry)
    frontier_adapter = ADAPTER_IDS[
        source["materialization_candidates"][0]["materialization_class"]
    ]
    for entry in revoked_registry["entries"]:
        if entry["adapter_id"] == frontier_adapter:
            entry["revoked"] = True
    revoked_registry = _redigest_registry(revoked_registry)
    _assert_not_authorized(
        _build(
            adapter_registry_snapshot=revoked_registry,
            adapter_bindings=_bindings(source, revoked_registry),
        ),
        DISPOSITION_REGISTRY_REPAIR,
    )

    exhausted_registry = deepcopy(registry)
    for entry in exhausted_registry["entries"]:
        if entry["adapter_id"] == frontier_adapter:
            entry["remaining_uses"] = 0
    exhausted_registry = _redigest_registry(exhausted_registry)
    _assert_not_authorized(
        _build(
            adapter_registry_snapshot=exhausted_registry,
            adapter_bindings=_bindings(source, exhausted_registry),
        ),
        DISPOSITION_LEASE_REFRESH,
    )

    completed = [
        candidate["materialization_candidate_id"]
        for candidate in source["materialization_candidates"][:3]
    ]
    irreversible_context = _context(source, completed=completed)
    _assert_not_authorized(
        _build(authorization_context=irreversible_context),
        DISPOSITION_REVERIFY,
    )

    reverified_context = _context(
        source,
        completed=completed,
        verifyos_step_reverification_digest="verifyos-step04-reverified-v01",
    )
    reverified = _build(authorization_context=reverified_context)
    assert reverified.status == STATUS_READY, reverified.blockers
    assert reverified.receipt is not None
    assert reverified.receipt["authorization_disposition"] == DISPOSITION_READY
    assert reverified.receipt["activation_authorization_admitted"] is True
    assert reverified.receipt["frontier_candidate_irreversible"] is True

    promoted_source = _source_receipt()
    promoted_source["execution_permission"] = True
    promoted_source = _redigest_source(promoted_source)

    malformed_registry = _registry(source)
    malformed_registry["registry_snapshot_digest"] = "wrong"

    widened_bindings = _bindings(source, registry)
    widened_bindings[0]["requested_effect_tags"] = ["tool_invocation"]
    widened_bindings[0]["binding_digest"] = canonical_digest(
        {
            key: value
            for key, value in widened_bindings[0].items()
            if key != "binding_digest"
        }
    )

    skipped_context = _context(source)
    skipped_context["completed_materialization_candidate_ids"] = [
        source["materialization_candidates"][1][
            "materialization_candidate_id"
        ]
    ]
    skipped_context["authorization_context_digest"] = (
        compute_authorization_context_digest(skipped_context)
    )

    blocked = [
        _build(source_materialization_receipt={}),
        _build(expected_source_materialization_receipt_digest="wrong"),
        _build(adapter_registry_snapshot=malformed_registry),
        _build(expected_adapter_registry_snapshot_digest="wrong"),
        _build(adapter_bindings=widened_bindings),
        _build(expected_authorization_context_digest="wrong"),
        _build(authorization_bundle_digest="wrong"),
        _build(source_materialization_receipt=promoted_source),
        _build(authorization_context=skipped_context),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.receipt is None

    print(
        "PASS: ActOS Dukkha-Preserving Adapter Binding and "
        "Activation Authorization Intake Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
