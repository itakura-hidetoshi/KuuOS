#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_types_v0_1 import *
from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_validation_v0_1 import (
    _correspondence_valid, _fresh_and_replay_closed, _policy_safe,
    _validate_policy, _validate_registry, _validate_request,
    _validate_source_bundle, _validate_store_state,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_adapter_v0_1 import (
    _checkpoint_envelope, _invocation, _next_registry, _next_store_state,
    _synthetic_failed_result, _synthetic_quarantined_result,
    _validate_adapter_result,
)

def build_codeai_durable_git_lifecycle_loop_checkpoint_persistence(
    *,
    source_loop_receipt: Any,
    source_loop_evidence: Any,
    source_loop_registry: Any,
    source_execution_registry: Any,
    source_reobservation_registry: Any,
    source_continuation_registry: Any,
    final_lifecycle_receipt: Any,
    final_lifecycle_state: Any,
    persistence_request: Any,
    persistence_policy: Any,
    persistence_registry: Any,
    checkpoint_store_state: Any,
    adapter: DurableCheckpointPersistenceAdapter,
) -> CodeAIDurableGitLifecycleLoopCheckpointPersistenceResult:
    loop_receipt = _mapping(source_loop_receipt)
    loop_evidence = _mapping(source_loop_evidence)
    loop_registry = _mapping(source_loop_registry)
    execution_registry = _mapping(source_execution_registry)
    reobservation_registry = _mapping(source_reobservation_registry)
    continuation_registry = _mapping(source_continuation_registry)
    lifecycle_receipt = _mapping(final_lifecycle_receipt)
    lifecycle_state = None if final_lifecycle_state is None else _mapping(final_lifecycle_state)
    request = _mapping(persistence_request)
    policy = _mapping(persistence_policy)
    registry = _mapping(persistence_registry)
    store_state = _mapping(checkpoint_store_state)
    issues: list[str] = []
    mappings = (
        (loop_receipt, "source_loop_receipt_not_mapping"),
        (loop_evidence, "source_loop_evidence_not_mapping"),
        (loop_registry, "source_loop_registry_not_mapping"),
        (execution_registry, "source_execution_registry_not_mapping"),
        (reobservation_registry, "source_reobservation_registry_not_mapping"),
        (continuation_registry, "source_continuation_registry_not_mapping"),
        (lifecycle_receipt, "final_lifecycle_receipt_not_mapping"),
        (request, "checkpoint_persistence_request_not_mapping"),
        (policy, "checkpoint_persistence_policy_not_mapping"),
        (registry, "checkpoint_persistence_registry_not_mapping"),
        (store_state, "checkpoint_store_state_not_mapping"),
    )
    for value, issue in mappings:
        if value is None:
            issues.append(issue)
    if final_lifecycle_state is not None and lifecycle_state is None:
        issues.append("final_lifecycle_state_not_mapping")
    if request is not None:
        issues.extend(_validate_request(request))
    if policy is not None:
        issues.extend(_validate_policy(policy))
    if registry is not None:
        issues.extend(_validate_registry(registry))
    if store_state is not None:
        issues.extend(_validate_store_state(store_state))
    if issues or any(value is None for value, _ in mappings):
        return CodeAIDurableGitLifecycleLoopCheckpointPersistenceResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None, None,
        )
    assert loop_receipt is not None and loop_evidence is not None
    assert loop_registry is not None and execution_registry is not None
    assert reobservation_registry is not None and continuation_registry is not None
    assert lifecycle_receipt is not None and request is not None and policy is not None
    assert registry is not None and store_state is not None
    issues.extend(_validate_source_bundle(
        loop_receipt=loop_receipt,
        loop_evidence=loop_evidence,
        loop_registry=loop_registry,
        execution_registry=execution_registry,
        reobservation_registry=reobservation_registry,
        continuation_registry=continuation_registry,
        final_lifecycle_receipt=lifecycle_receipt,
        final_lifecycle_state=lifecycle_state,
    ))
    if not _correspondence_valid(
        loop_receipt=loop_receipt,
        loop_evidence=loop_evidence,
        loop_registry=loop_registry,
        execution_registry=execution_registry,
        reobservation_registry=reobservation_registry,
        continuation_registry=continuation_registry,
        final_lifecycle_receipt=lifecycle_receipt,
        final_lifecycle_state=lifecycle_state,
        request=request,
        policy=policy,
        registry=registry,
        store_state=store_state,
    ):
        issues.append("checkpoint_persistence_correspondence_mismatch")
    if not _policy_safe(request, policy):
        issues.append("checkpoint_persistence_policy_not_safe")
    if not _fresh_and_replay_closed(
        loop_receipt=loop_receipt,
        request=request,
        policy=policy,
        registry=registry,
        store_state=store_state,
    ):
        issues.append("checkpoint_persistence_freshness_capacity_or_replay_violation")
    if issues:
        return CodeAIDurableGitLifecycleLoopCheckpointPersistenceResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None, None,
        )

    envelope = _checkpoint_envelope(
        loop_receipt=loop_receipt,
        loop_evidence=loop_evidence,
        loop_registry=loop_registry,
        execution_registry=execution_registry,
        reobservation_registry=reobservation_registry,
        continuation_registry=continuation_registry,
        final_lifecycle_receipt=lifecycle_receipt,
        final_lifecycle_state=lifecycle_state,
        request=request,
        policy=policy,
    )
    invocation = _invocation(request, policy, envelope)
    adapter_validation_issues: list[str] = []
    try:
        raw_adapter_result = adapter(invocation)
    except Exception as exc:  # Adapter exceptions are recorded, not propagated.
        adapter_result = _synthetic_failed_result(invocation, policy, type(exc).__name__)
    else:
        mapped_result = _mapping(raw_adapter_result)
        if mapped_result is None:
            adapter_validation_issues.append("checkpoint_adapter_result_not_mapping")
            adapter_result = _synthetic_quarantined_result(invocation, policy)
        else:
            adapter_validation_issues.extend(
                _validate_adapter_result(mapped_result, invocation, policy)
            )
            adapter_result = (
                dict(mapped_result)
                if not adapter_validation_issues
                else _synthetic_quarantined_result(invocation, policy)
            )

    committed = adapter_result["status"] == ADAPTER_STATUS_COMMITTED
    if adapter_result["status"] == ADAPTER_STATUS_COMMITTED:
        disposition = DISPOSITION_PERSISTED
    elif adapter_result["status"] == ADAPTER_STATUS_CONFLICT:
        disposition = DISPOSITION_CONFLICT
    elif adapter_result["status"] == ADAPTER_STATUS_FAILED:
        disposition = DISPOSITION_FAILED
    else:
        disposition = DISPOSITION_EVIDENCE_QUARANTINED

    next_registry = _next_registry(
        registry,
        request=request,
        loop_receipt_digest=loop_receipt[LOOP_RECEIPT_DIGEST_FIELD],
        committed=committed,
        epoch=policy["evaluation_epoch"],
    )
    next_store_state = _next_store_state(
        store_state,
        request=request,
        envelope_digest=envelope[CHECKPOINT_ENVELOPE_DIGEST_FIELD],
        committed=committed,
        epoch=policy["evaluation_epoch"],
    )
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_loop_receipt_digest": loop_receipt[LOOP_RECEIPT_DIGEST_FIELD],
        "source_loop_evidence_digest": loop_evidence[LOOP_EVIDENCE_DIGEST_FIELD],
        "source_loop_registry_digest": loop_registry[LOOP_REGISTRY_DIGEST_FIELD],
        "source_execution_registry_digest": execution_registry[EXECUTION_REGISTRY_DIGEST_FIELD],
        "source_reobservation_registry_digest": reobservation_registry[REOBSERVATION_REGISTRY_DIGEST_FIELD],
        "source_continuation_registry_digest": continuation_registry[CONTINUATION_REGISTRY_DIGEST_FIELD],
        "final_lifecycle_receipt_digest": lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "final_lifecycle_state_digest": (
            lifecycle_state[LIFECYCLE_STATE_DIGEST_FIELD] if lifecycle_state is not None else ""
        ),
        "persistence_request_digest": request[REQUEST_DIGEST_FIELD],
        "persistence_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_persistence_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_persistence_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "source_store_state_digest": store_state[STORE_STATE_DIGEST_FIELD],
        "next_store_state_digest": next_store_state[STORE_STATE_DIGEST_FIELD],
        "checkpoint_envelope_digest": envelope[CHECKPOINT_ENVELOPE_DIGEST_FIELD],
        "adapter_invocation_digest": canonical_digest(asdict(invocation)),
        "adapter_result": adapter_result,
        "adapter_result_validation_issues": adapter_validation_issues,
        "adapter_invoked_once": True,
        "checkpoint_write_committed": committed,
        "checkpoint_store_state_advanced": committed,
        "checkpoint_registry_advanced_once": True,
        "resume_input_issued": False,
        "loop_reexecuted": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_loop_receipt_digest": loop_receipt[LOOP_RECEIPT_DIGEST_FIELD],
        "source_loop_evidence_digest": loop_evidence[LOOP_EVIDENCE_DIGEST_FIELD],
        "persistence_request_digest": request[REQUEST_DIGEST_FIELD],
        "persistence_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_persistence_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_persistence_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "source_store_state_digest": store_state[STORE_STATE_DIGEST_FIELD],
        "next_store_state_digest": next_store_state[STORE_STATE_DIGEST_FIELD],
        "checkpoint_envelope_digest": envelope[CHECKPOINT_ENVELOPE_DIGEST_FIELD],
        "persistence_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "adapter_result_digest": adapter_result[ADAPTER_RESULT_DIGEST_FIELD],
        "checkpoint_id": request["checkpoint_id"],
        "checkpoint_revision": request["checkpoint_revision"],
        "loop_id": loop_receipt["loop_id"],
        "lifecycle_id": loop_receipt["lifecycle_id"],
        "repository_full_name": loop_receipt["repository_full_name"],
        "store_id": request["store_id"],
        "codeai_disposition": disposition,
        "operating_mode": "durable_loop_checkpoint_compare_and_swap_persistence",
        "route_receipt_recorded": True,
        "source_loop_receipt_verified": True,
        "source_loop_evidence_verified": True,
        "source_bundle_correspondence_confirmed": True,
        "persistence_nonce_consumed": True,
        "persistence_registry_advanced_once": True,
        "adapter_invoked_once": True,
        "atomic_compare_and_swap_attempted": adapter_result["atomic_compare_and_swap_attempted"],
        "atomic_compare_and_swap_succeeded": adapter_result["atomic_compare_and_swap_succeeded"],
        "checkpoint_persisted": committed,
        "checkpoint_conflict_observed": disposition == DISPOSITION_CONFLICT,
        "checkpoint_persistence_failed": disposition == DISPOSITION_FAILED,
        "checkpoint_evidence_quarantined": disposition == DISPOSITION_EVIDENCE_QUARANTINED,
        "store_state_advanced_once": committed,
        "checkpoint_overwrite_performed": False,
        "checkpoint_delete_performed": False,
        "network_accessed": False,
        "secret_material_read": False,
        "git_effect_performed": False,
        "loop_reexecuted": False,
        "resume_input_issued": False,
        "automatic_resumption_performed": False,
        "adapter_acknowledgement_treated_as_durable_truth": False,
        "checkpoint_treated_as_resumption_authority": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
        "history_read_only": False,
        "future_only": True,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIDurableGitLifecycleLoopCheckpointPersistenceResult(
        STATUS_READY,
        tuple(adapter_validation_issues),
        envelope,
        evidence,
        next_registry,
        next_store_state,
        receipt,
    )
