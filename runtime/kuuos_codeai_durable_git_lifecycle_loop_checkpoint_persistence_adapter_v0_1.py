#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_types_v0_1 import *

def _checkpoint_envelope(
    *,
    loop_receipt: Mapping[str, Any],
    loop_evidence: Mapping[str, Any],
    loop_registry: Mapping[str, Any],
    execution_registry: Mapping[str, Any],
    reobservation_registry: Mapping[str, Any],
    continuation_registry: Mapping[str, Any],
    final_lifecycle_receipt: Mapping[str, Any],
    final_lifecycle_state: Mapping[str, Any] | None,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "checkpoint_id": request["checkpoint_id"],
        "checkpoint_revision": request["checkpoint_revision"],
        "source_loop_receipt_digest": loop_receipt[LOOP_RECEIPT_DIGEST_FIELD],
        "source_loop_evidence_digest": loop_evidence[LOOP_EVIDENCE_DIGEST_FIELD],
        "source_loop_registry_digest": loop_registry[LOOP_REGISTRY_DIGEST_FIELD],
        "source_execution_registry_digest": execution_registry[EXECUTION_REGISTRY_DIGEST_FIELD],
        "source_reobservation_registry_digest": reobservation_registry[REOBSERVATION_REGISTRY_DIGEST_FIELD],
        "source_continuation_registry_digest": continuation_registry[CONTINUATION_REGISTRY_DIGEST_FIELD],
        "final_lifecycle_receipt_digest": final_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "final_lifecycle_state_digest": (
            final_lifecycle_state[LIFECYCLE_STATE_DIGEST_FIELD]
            if final_lifecycle_state is not None else ""
        ),
        "loop_id": loop_receipt["loop_id"],
        "lifecycle_id": loop_receipt["lifecycle_id"],
        "repository_full_name": loop_receipt["repository_full_name"],
        "loop_disposition": loop_receipt["codeai_disposition"],
        "effect_count": loop_receipt["effect_count"],
        "maximum_effect_count": loop_receipt["maximum_effect_count"],
        "final_lifecycle_completed": loop_receipt["final_lifecycle_completed"],
        "final_execution_lease_issued": loop_receipt["final_execution_lease_issued"],
        "persistence_request_digest": request[REQUEST_DIGEST_FIELD],
        "persistence_policy_digest": policy[POLICY_DIGEST_FIELD],
        "created_epoch": policy["evaluation_epoch"],
        "resume_input_issued": False,
        "automatic_resumption_performed": False,
        "general_successor_stage_authority_granted": False,
    }
    value[CHECKPOINT_ENVELOPE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _invocation(
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    envelope: Mapping[str, Any],
) -> DurableCheckpointPersistenceInvocation:
    return DurableCheckpointPersistenceInvocation(
        adapter_id=request["adapter_id"],
        persistence_session_id=request["persistence_session_id"],
        store_id=request["store_id"],
        checkpoint_id=request["checkpoint_id"],
        expected_store_revision=request["expected_store_revision"],
        checkpoint_envelope_digest=envelope[CHECKPOINT_ENVELOPE_DIGEST_FIELD],
        checkpoint_envelope=dict(envelope),
        maximum_command_count=policy["maximum_adapter_command_count"],
        maximum_output_bytes=policy["maximum_adapter_output_bytes"],
        network_access_allowed=False,
        secret_material_read_allowed=False,
    )


def _validate_adapter_result(
    value: Mapping[str, Any],
    invocation: DurableCheckpointPersistenceInvocation,
    policy: Mapping[str, Any],
) -> list[str]:
    issues = _exact_fields(value, ADAPTER_RESULT_FIELDS, "checkpoint_adapter_result")
    if issues:
        return issues
    for field in (
        "adapter_id", "adapter_session_id", "store_id", "checkpoint_id",
        "checkpoint_envelope_digest", "status", "exception_type",
    ):
        if not isinstance(value.get(field), str):
            issues.append("checkpoint_adapter_result_invalid_string:" + field)
    for field in (
        "expected_store_revision", "observed_store_revision", "committed_store_revision",
        "command_count", "output_bytes", "completed_epoch",
    ):
        if _nat(value.get(field)) is None:
            issues.append("checkpoint_adapter_result_invalid_nat:" + field)
    bool_fields = ADAPTER_RESULT_FIELDS - {
        "adapter_id", "adapter_session_id", "store_id", "checkpoint_id",
        "checkpoint_envelope_digest", "status", "exception_type",
        "expected_store_revision", "observed_store_revision", "committed_store_revision",
        "command_count", "output_bytes", "completed_epoch", ADAPTER_RESULT_DIGEST_FIELD,
    }
    for field in bool_fields:
        if not isinstance(value.get(field), bool):
            issues.append("checkpoint_adapter_result_invalid_bool:" + field)
    if not isinstance(value.get(ADAPTER_RESULT_DIGEST_FIELD), str) or not _SHA256.fullmatch(
        value[ADAPTER_RESULT_DIGEST_FIELD]
    ):
        issues.append("checkpoint_adapter_result_invalid_digest")
    elif not _digest_ok(value, ADAPTER_RESULT_DIGEST_FIELD):
        issues.append("checkpoint_adapter_result_digest_mismatch")
    if issues:
        return issues
    if value["adapter_id"] != invocation.adapter_id:
        issues.append("checkpoint_adapter_result_adapter_mismatch")
    if value["adapter_session_id"] != invocation.persistence_session_id:
        issues.append("checkpoint_adapter_result_session_mismatch")
    if value["store_id"] != invocation.store_id:
        issues.append("checkpoint_adapter_result_store_mismatch")
    if value["checkpoint_id"] != invocation.checkpoint_id:
        issues.append("checkpoint_adapter_result_checkpoint_mismatch")
    if value["expected_store_revision"] != invocation.expected_store_revision:
        issues.append("checkpoint_adapter_result_expected_revision_mismatch")
    if value["checkpoint_envelope_digest"] != invocation.checkpoint_envelope_digest:
        issues.append("checkpoint_adapter_result_envelope_mismatch")
    if value["command_count"] > invocation.maximum_command_count:
        issues.append("checkpoint_adapter_result_command_budget_exceeded")
    if value["output_bytes"] > invocation.maximum_output_bytes:
        issues.append("checkpoint_adapter_result_output_budget_exceeded")
    if value["completed_epoch"] != policy["evaluation_epoch"]:
        issues.append("checkpoint_adapter_result_epoch_mismatch")
    forbidden = (
        value["checkpoint_overwritten"], value["checkpoint_deleted"],
        value["network_accessed"], value["secret_material_read"],
        value["git_effect_performed"], value["loop_executed"],
        value["resume_input_issued"], value["arbitrary_command_executed"],
    )
    if any(forbidden):
        issues.append("checkpoint_adapter_result_forbidden_effect")
    status = value["status"]
    if status not in {ADAPTER_STATUS_COMMITTED, ADAPTER_STATUS_CONFLICT, ADAPTER_STATUS_FAILED}:
        issues.append("checkpoint_adapter_result_invalid_status")
    elif status == ADAPTER_STATUS_COMMITTED:
        if not (
            value["observed_store_revision"] == invocation.expected_store_revision
            and value["committed_store_revision"] == invocation.expected_store_revision + 1
            and value["atomic_compare_and_swap_attempted"] is True
            and value["atomic_compare_and_swap_succeeded"] is True
            and value["checkpoint_absent_before_write"] is True
            and value["write_committed"] is True
            and value["exception_type"] == ""
        ):
            issues.append("checkpoint_adapter_result_invalid_commit_semantics")
    elif status == ADAPTER_STATUS_CONFLICT:
        if not (
            value["observed_store_revision"] != invocation.expected_store_revision
            and value["committed_store_revision"] == value["observed_store_revision"]
            and value["atomic_compare_and_swap_attempted"] is True
            and value["atomic_compare_and_swap_succeeded"] is False
            and value["write_committed"] is False
        ):
            issues.append("checkpoint_adapter_result_invalid_conflict_semantics")
    else:
        if not (
            value["committed_store_revision"] == value["observed_store_revision"]
            and value["atomic_compare_and_swap_succeeded"] is False
            and value["write_committed"] is False
        ):
            issues.append("checkpoint_adapter_result_invalid_failure_semantics")
    return issues


def _synthetic_failed_result(
    invocation: DurableCheckpointPersistenceInvocation,
    policy: Mapping[str, Any],
    exception_type: str,
) -> dict[str, Any]:
    value = {
        "adapter_id": invocation.adapter_id,
        "adapter_session_id": invocation.persistence_session_id,
        "store_id": invocation.store_id,
        "checkpoint_id": invocation.checkpoint_id,
        "expected_store_revision": invocation.expected_store_revision,
        "observed_store_revision": invocation.expected_store_revision,
        "committed_store_revision": invocation.expected_store_revision,
        "checkpoint_envelope_digest": invocation.checkpoint_envelope_digest,
        "status": ADAPTER_STATUS_FAILED,
        "command_count": 0,
        "output_bytes": 0,
        "completed_epoch": policy["evaluation_epoch"],
        "atomic_compare_and_swap_attempted": False,
        "atomic_compare_and_swap_succeeded": False,
        "checkpoint_absent_before_write": False,
        "write_committed": False,
        "checkpoint_overwritten": False,
        "checkpoint_deleted": False,
        "network_accessed": False,
        "secret_material_read": False,
        "git_effect_performed": False,
        "loop_executed": False,
        "resume_input_issued": False,
        "arbitrary_command_executed": False,
        "exception_type": exception_type,
    }
    value[ADAPTER_RESULT_DIGEST_FIELD] = canonical_digest(value)
    return value


def _synthetic_quarantined_result(
    invocation: DurableCheckpointPersistenceInvocation,
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = _synthetic_failed_result(invocation, policy, "malformed_adapter_result")
    value["status"] = ADAPTER_STATUS_QUARANTINED
    value[ADAPTER_RESULT_DIGEST_FIELD] = canonical_digest(
        {k: v for k, v in value.items() if k != ADAPTER_RESULT_DIGEST_FIELD}
    )
    return value


def _next_registry(
    registry: Mapping[str, Any],
    *,
    request: Mapping[str, Any],
    loop_receipt_digest: str,
    committed: bool,
    epoch: int,
) -> dict[str, Any]:
    value = dict(registry)
    value["registry_revision"] += 1
    value["consumed_persistence_nonce_digests"] = [
        *registry["consumed_persistence_nonce_digests"],
        request["persistence_nonce_digest"],
    ]
    value["persistence_attempt_count"] += 1
    value["last_persistence_epoch"] = epoch
    if committed:
        value["persisted_loop_receipt_digests"] = [
            *registry["persisted_loop_receipt_digests"], loop_receipt_digest,
        ]
        value["persisted_checkpoint_ids"] = [
            *registry["persisted_checkpoint_ids"], request["checkpoint_id"],
        ]
        value["successful_persistence_count"] += 1
    value[REGISTRY_DIGEST_FIELD] = canonical_digest(
        {k: v for k, v in value.items() if k != REGISTRY_DIGEST_FIELD}
    )
    return value


def _next_store_state(
    store_state: Mapping[str, Any],
    *,
    request: Mapping[str, Any],
    envelope_digest: str,
    committed: bool,
    epoch: int,
) -> dict[str, Any]:
    if not committed:
        return dict(store_state)
    value = dict(store_state)
    value["store_revision"] += 1
    value["checkpoint_ids"] = [*store_state["checkpoint_ids"], request["checkpoint_id"]]
    value["checkpoint_envelope_digests"] = [
        *store_state["checkpoint_envelope_digests"], envelope_digest,
    ]
    value["last_committed_epoch"] = epoch
    value[STORE_STATE_DIGEST_FIELD] = canonical_digest(
        {k: v for k, v in value.items() if k != STORE_STATE_DIGEST_FIELD}
    )
    return value
