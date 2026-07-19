#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import *


def _invocation(request: Mapping[str, Any], policy: Mapping[str, Any]) -> DurableCheckpointReadInvocation:
    return DurableCheckpointReadInvocation(
        adapter_id=request["adapter_id"],
        resumption_session_id=request["resumption_session_id"],
        store_id=request["store_id"],
        checkpoint_id=request["checkpoint_id"],
        checkpoint_envelope_digest=request["checkpoint_envelope_digest"],
        maximum_command_count=policy["maximum_adapter_command_count"],
        maximum_output_bytes=policy["maximum_adapter_output_bytes"],
        network_access_allowed=False,
        secret_material_read_allowed=False,
    )


def _validate_checkpoint_envelope(value: Mapping[str, Any], invocation: DurableCheckpointReadInvocation) -> list[str]:
    issues = _exact_fields(value, CHECKPOINT_ENVELOPE_REQUIRED_FIELDS, "checkpoint_envelope")
    if issues:
        return issues
    if not _digest_ok(value, CHECKPOINT_ENVELOPE_DIGEST_FIELD):
        issues.append("checkpoint_envelope_digest_mismatch")
    if value.get(CHECKPOINT_ENVELOPE_DIGEST_FIELD) != invocation.checkpoint_envelope_digest:
        issues.append("checkpoint_envelope_unexpected_digest")
    if value.get("checkpoint_id") != invocation.checkpoint_id:
        issues.append("checkpoint_envelope_checkpoint_id_mismatch")
    if value.get("checkpoint_revision") != 1:
        issues.append("checkpoint_envelope_revision_mismatch")
    if value.get("resume_input_issued") is not False:
        issues.append("checkpoint_envelope_prior_resume_input")
    if value.get("automatic_resumption_performed") is not False:
        issues.append("checkpoint_envelope_prior_automatic_resumption")
    if value.get("general_successor_stage_authority_granted") is not False:
        issues.append("checkpoint_envelope_prior_general_authority")
    return issues


def _validate_read_result(
    value: Mapping[str, Any],
    invocation: DurableCheckpointReadInvocation,
    policy: Mapping[str, Any],
) -> list[str]:
    issues = _exact_fields(value, READ_RESULT_FIELDS, "checkpoint_read_result")
    if issues:
        return issues
    for field in (
        "adapter_id", "adapter_session_id", "store_id", "checkpoint_id",
        "checkpoint_envelope_digest", "status", "exception_type",
    ):
        if not isinstance(value.get(field), str):
            issues.append("checkpoint_read_result_invalid_string:" + field)
    for field in ("command_count", "output_bytes", "completed_epoch"):
        if _nat(value.get(field)) is None:
            issues.append("checkpoint_read_result_invalid_nat:" + field)
    bool_fields = {
        "checkpoint_found", "checkpoint_read_performed", "network_accessed",
        "secret_material_read", "git_effect_performed", "loop_executed",
        "resume_input_issued", "arbitrary_command_executed",
    }
    for field in bool_fields:
        if not isinstance(value.get(field), bool):
            issues.append("checkpoint_read_result_invalid_bool:" + field)
    envelope = value.get("checkpoint_envelope")
    if envelope is not None and not isinstance(envelope, Mapping):
        issues.append("checkpoint_read_result_envelope_not_mapping")
    if not isinstance(value.get(READ_RESULT_DIGEST_FIELD), str) or not _SHA256.fullmatch(
        value[READ_RESULT_DIGEST_FIELD]
    ):
        issues.append("checkpoint_read_result_invalid_digest")
    elif not _digest_ok(value, READ_RESULT_DIGEST_FIELD):
        issues.append("checkpoint_read_result_digest_mismatch")
    if issues:
        return issues
    if value["adapter_id"] != invocation.adapter_id:
        issues.append("checkpoint_read_result_adapter_mismatch")
    if value["adapter_session_id"] != invocation.resumption_session_id:
        issues.append("checkpoint_read_result_session_mismatch")
    if value["store_id"] != invocation.store_id:
        issues.append("checkpoint_read_result_store_mismatch")
    if value["checkpoint_id"] != invocation.checkpoint_id:
        issues.append("checkpoint_read_result_checkpoint_mismatch")
    if value["checkpoint_envelope_digest"] != invocation.checkpoint_envelope_digest:
        issues.append("checkpoint_read_result_checkpoint_digest_mismatch")
    if value["command_count"] > invocation.maximum_command_count:
        issues.append("checkpoint_read_result_command_budget_exceeded")
    if value["output_bytes"] > invocation.maximum_output_bytes:
        issues.append("checkpoint_read_result_output_budget_exceeded")
    if value["completed_epoch"] != policy["evaluation_epoch"]:
        issues.append("checkpoint_read_result_epoch_mismatch")
    if any(
        value[field] for field in (
            "network_accessed", "secret_material_read", "git_effect_performed",
            "loop_executed", "resume_input_issued", "arbitrary_command_executed",
        )
    ):
        issues.append("checkpoint_read_result_forbidden_effect")
    status = value["status"]
    if status not in {ADAPTER_STATUS_VERIFIED, ADAPTER_STATUS_UNAVAILABLE, ADAPTER_STATUS_FAILED}:
        issues.append("checkpoint_read_result_invalid_status")
    elif status == ADAPTER_STATUS_VERIFIED:
        if not (
            value["checkpoint_found"] is True
            and value["checkpoint_read_performed"] is True
            and isinstance(envelope, Mapping)
            and value["exception_type"] == ""
        ):
            issues.append("checkpoint_read_result_invalid_verified_semantics")
        elif isinstance(envelope, Mapping):
            issues.extend(_validate_checkpoint_envelope(envelope, invocation))
    elif status == ADAPTER_STATUS_UNAVAILABLE:
        if not (
            value["checkpoint_found"] is False
            and value["checkpoint_read_performed"] is True
            and envelope is None
        ):
            issues.append("checkpoint_read_result_invalid_unavailable_semantics")
    else:
        if not (value["checkpoint_found"] is False and envelope is None):
            issues.append("checkpoint_read_result_invalid_failure_semantics")
    return issues


def _synthetic_result(
    invocation: DurableCheckpointReadInvocation,
    policy: Mapping[str, Any],
    *,
    status: str,
    exception_type: str,
) -> dict[str, Any]:
    value = {
        "adapter_id": invocation.adapter_id,
        "adapter_session_id": invocation.resumption_session_id,
        "store_id": invocation.store_id,
        "checkpoint_id": invocation.checkpoint_id,
        "checkpoint_envelope_digest": invocation.checkpoint_envelope_digest,
        "checkpoint_envelope": None,
        "status": status,
        "command_count": 0,
        "output_bytes": 0,
        "completed_epoch": policy["evaluation_epoch"],
        "checkpoint_found": False,
        "checkpoint_read_performed": False,
        "network_accessed": False,
        "secret_material_read": False,
        "git_effect_performed": False,
        "loop_executed": False,
        "resume_input_issued": False,
        "arbitrary_command_executed": False,
        "exception_type": exception_type,
    }
    value[READ_RESULT_DIGEST_FIELD] = canonical_digest(value)
    return value


def _resume_input(
    *,
    persistence_receipt: Mapping[str, Any],
    checkpoint_envelope: Mapping[str, Any],
    persistence_registry: Mapping[str, Any],
    store_state: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "resume_input_id": request["resumption_session_id"] + ":resume-input",
        "checkpoint_id": request["checkpoint_id"],
        "checkpoint_envelope_digest": request["checkpoint_envelope_digest"],
        "source_persistence_receipt_digest": persistence_receipt[PERSISTENCE_RECEIPT_DIGEST_FIELD],
        "source_persistence_registry_digest": persistence_registry[PERSISTENCE_REGISTRY_DIGEST_FIELD],
        "source_store_state_digest": store_state[STORE_STATE_DIGEST_FIELD],
        "loop_id": checkpoint_envelope["loop_id"],
        "lifecycle_id": checkpoint_envelope["lifecycle_id"],
        "repository_full_name": checkpoint_envelope["repository_full_name"],
        "loop_disposition": checkpoint_envelope["loop_disposition"],
        "prior_effect_count": checkpoint_envelope["effect_count"],
        "prior_maximum_effect_count": checkpoint_envelope["maximum_effect_count"],
        "final_lifecycle_receipt_digest": checkpoint_envelope["final_lifecycle_receipt_digest"],
        "final_lifecycle_state_digest": checkpoint_envelope["final_lifecycle_state_digest"],
        "final_lifecycle_completed": checkpoint_envelope["final_lifecycle_completed"],
        "final_execution_lease_issued": checkpoint_envelope["final_execution_lease_issued"],
        "resume_effect_budget": request["requested_resume_effect_budget"],
        "resume_execution_command_budget": request["requested_resume_execution_command_budget"],
        "resume_execution_output_bytes": request["requested_resume_execution_output_bytes"],
        "issued_epoch": policy["evaluation_epoch"],
        "future_only": True,
        "active_now": False,
        "loop_execution_authorized": False,
        "git_effect_authorized": False,
        "automatic_resumption_authorized": False,
        "general_successor_stage_authority_granted": False,
    }
    value[RESUME_INPUT_DIGEST_FIELD] = canonical_digest(value)
    return value


def _next_registry(
    registry: Mapping[str, Any],
    *,
    request: Mapping[str, Any],
    persistence_receipt_digest: str,
    admitted: bool,
    epoch: int,
) -> dict[str, Any]:
    value = dict(registry)
    value["registry_revision"] += 1
    value["consumed_resumption_nonce_digests"] = [
        *value["consumed_resumption_nonce_digests"], request["resumption_nonce_digest"]
    ]
    value["resumption_attempt_count"] += 1
    value["last_resumption_epoch"] = epoch
    if admitted:
        value["admitted_checkpoint_ids"] = [
            *value["admitted_checkpoint_ids"], request["checkpoint_id"]
        ]
        value["admitted_checkpoint_envelope_digests"] = [
            *value["admitted_checkpoint_envelope_digests"], request["checkpoint_envelope_digest"]
        ]
        value["admitted_persistence_receipt_digests"] = [
            *value["admitted_persistence_receipt_digests"], persistence_receipt_digest
        ]
        value["successful_resumption_admission_count"] += 1
    value.pop(REGISTRY_DIGEST_FIELD, None)
    value[REGISTRY_DIGEST_FIELD] = canonical_digest(value)
    return value
