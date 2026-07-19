#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import *
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_validation_v0_1 import (
    _correspondence_valid, _fresh_and_replay_closed, _policy_safe,
    _validate_policy, _validate_registry, _validate_request, _validate_sources,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_adapter_v0_1 import (
    _invocation, _next_registry, _resume_input, _synthetic_result,
    _validate_read_result,
)


def build_codeai_durable_git_lifecycle_loop_resumption_admission(
    *,
    persistence_receipt: Any,
    persistence_evidence: Any,
    persistence_registry: Any,
    checkpoint_store_state: Any,
    resumption_request: Any,
    resumption_policy: Any,
    resumption_registry: Any,
    read_adapter: DurableCheckpointReadAdapter,
) -> CodeAIDurableGitLifecycleLoopResumptionAdmissionResult:
    source_receipt = _mapping(persistence_receipt)
    source_evidence = _mapping(persistence_evidence)
    source_registry = _mapping(persistence_registry)
    store_state = _mapping(checkpoint_store_state)
    request = _mapping(resumption_request)
    policy = _mapping(resumption_policy)
    registry = _mapping(resumption_registry)
    issues: list[str] = []
    for value, issue in (
        (source_receipt, "persistence_receipt_not_mapping"),
        (source_evidence, "persistence_evidence_not_mapping"),
        (source_registry, "persistence_registry_not_mapping"),
        (store_state, "checkpoint_store_state_not_mapping"),
        (request, "resumption_request_not_mapping"),
        (policy, "resumption_policy_not_mapping"),
        (registry, "resumption_registry_not_mapping"),
    ):
        if value is None:
            issues.append(issue)
    if request is not None:
        issues.extend(_validate_request(request))
    if policy is not None:
        issues.extend(_validate_policy(policy))
    if registry is not None:
        issues.extend(_validate_registry(registry))
    if issues or any(value is None for value in (
        source_receipt, source_evidence, source_registry, store_state, request, policy, registry
    )):
        return CodeAIDurableGitLifecycleLoopResumptionAdmissionResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None
        )
    assert source_receipt is not None and source_evidence is not None
    assert source_registry is not None and store_state is not None
    assert request is not None and policy is not None and registry is not None
    issues.extend(_validate_sources(source_receipt, source_evidence, source_registry, store_state))
    if not _correspondence_valid(
        persistence_receipt=source_receipt,
        persistence_evidence=source_evidence,
        persistence_registry=source_registry,
        store_state=store_state,
        request=request,
        policy=policy,
    ):
        issues.append("resumption_admission_correspondence_mismatch")
    if not _policy_safe(request, policy):
        issues.append("resumption_admission_policy_not_safe")
    if not _fresh_and_replay_closed(request, policy, registry):
        issues.append("resumption_admission_freshness_capacity_or_replay_violation")
    if issues:
        return CodeAIDurableGitLifecycleLoopResumptionAdmissionResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None
        )

    invocation = _invocation(request, policy)
    adapter_validation_issues: list[str] = []
    try:
        raw_read_result = read_adapter(invocation)
    except Exception as exc:
        read_result = _synthetic_result(
            invocation, policy, status=ADAPTER_STATUS_FAILED, exception_type=type(exc).__name__
        )
    else:
        mapped = _mapping(raw_read_result)
        if mapped is None:
            adapter_validation_issues.append("checkpoint_read_result_not_mapping")
            read_result = _synthetic_result(
                invocation, policy, status=ADAPTER_STATUS_QUARANTINED,
                exception_type="InvalidAdapterResult",
            )
        else:
            adapter_validation_issues.extend(_validate_read_result(mapped, invocation, policy))
            read_result = dict(mapped) if not adapter_validation_issues else _synthetic_result(
                invocation, policy, status=ADAPTER_STATUS_QUARANTINED,
                exception_type="InvalidAdapterEvidence",
            )

    admitted = read_result["status"] == ADAPTER_STATUS_VERIFIED
    checkpoint_envelope: Mapping[str, Any] | None = (
        read_result["checkpoint_envelope"] if admitted else None
    )
    resume_input = (
        _resume_input(
            persistence_receipt=source_receipt,
            checkpoint_envelope=checkpoint_envelope,
            persistence_registry=source_registry,
            store_state=store_state,
            request=request,
            policy=policy,
        )
        if checkpoint_envelope is not None else None
    )
    if admitted:
        disposition = DISPOSITION_ADMITTED
    elif read_result["status"] == ADAPTER_STATUS_UNAVAILABLE:
        disposition = DISPOSITION_UNAVAILABLE
    elif read_result["status"] == ADAPTER_STATUS_FAILED:
        disposition = DISPOSITION_FAILED
    else:
        disposition = DISPOSITION_EVIDENCE_QUARANTINED
    next_registry = _next_registry(
        registry,
        request=request,
        persistence_receipt_digest=source_receipt[PERSISTENCE_RECEIPT_DIGEST_FIELD],
        admitted=admitted,
        epoch=policy["evaluation_epoch"],
    )
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_persistence_receipt_digest": source_receipt[PERSISTENCE_RECEIPT_DIGEST_FIELD],
        "source_persistence_evidence_digest": source_evidence[PERSISTENCE_EVIDENCE_DIGEST_FIELD],
        "source_persistence_registry_digest": source_registry[PERSISTENCE_REGISTRY_DIGEST_FIELD],
        "source_store_state_digest": store_state[STORE_STATE_DIGEST_FIELD],
        "resumption_request_digest": request[REQUEST_DIGEST_FIELD],
        "resumption_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_resumption_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_resumption_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "checkpoint_envelope_digest": request["checkpoint_envelope_digest"],
        "read_adapter_invocation_digest": canonical_digest(asdict(invocation)),
        "read_result": read_result,
        "read_result_validation_issues": adapter_validation_issues,
        "read_adapter_invoked_once": True,
        "checkpoint_read_verified": admitted,
        "resume_input_issued": admitted,
        "resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD] if resume_input else "",
        "loop_executed": False,
        "git_effect_performed": False,
        "automatic_resumption_performed": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_persistence_receipt_digest": source_receipt[PERSISTENCE_RECEIPT_DIGEST_FIELD],
        "source_persistence_evidence_digest": source_evidence[PERSISTENCE_EVIDENCE_DIGEST_FIELD],
        "source_persistence_registry_digest": source_registry[PERSISTENCE_REGISTRY_DIGEST_FIELD],
        "source_store_state_digest": store_state[STORE_STATE_DIGEST_FIELD],
        "resumption_request_digest": request[REQUEST_DIGEST_FIELD],
        "resumption_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_resumption_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_resumption_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "resumption_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "checkpoint_read_result_digest": read_result[READ_RESULT_DIGEST_FIELD],
        "resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD] if resume_input else "",
        "checkpoint_id": request["checkpoint_id"],
        "checkpoint_envelope_digest": request["checkpoint_envelope_digest"],
        "loop_id": request["loop_id"],
        "lifecycle_id": request["lifecycle_id"],
        "repository_full_name": request["repository_full_name"],
        "store_id": request["store_id"],
        "codeai_disposition": disposition,
        "operating_mode": "durable_checkpoint_read_and_resumption_input_admission",
        "route_receipt_recorded": True,
        "source_persistence_bundle_verified": True,
        "resumption_nonce_consumed": True,
        "resumption_registry_advanced_once": True,
        "read_adapter_invoked_once": True,
        "checkpoint_read_verified": admitted,
        "checkpoint_unavailable": disposition == DISPOSITION_UNAVAILABLE,
        "checkpoint_read_failed": disposition == DISPOSITION_FAILED,
        "checkpoint_read_evidence_quarantined": disposition == DISPOSITION_EVIDENCE_QUARANTINED,
        "resume_input_issued": admitted,
        "loop_execution_performed": False,
        "git_effect_performed": False,
        "automatic_resumption_performed": False,
        "network_accessed": False,
        "secret_material_read": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
        "future_only": True,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIDurableGitLifecycleLoopResumptionAdmissionResult(
        STATUS_READY, tuple(adapter_validation_issues), resume_input, evidence,
        next_registry, receipt,
    )
