#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_types_v0_1 import *

def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "checkpoint_persistence_request")
    if issues:
        return issues
    for field in _REQUEST_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("checkpoint_persistence_request_invalid_string:" + field)
        elif field != "final_lifecycle_state_digest" and not value[field]:
            issues.append("checkpoint_persistence_request_empty_string:" + field)
    if _nat(value.get("checkpoint_revision"), positive=True) is None:
        issues.append("checkpoint_persistence_request_invalid_checkpoint_revision")
    if _nat(value.get("expected_store_revision")) is None:
        issues.append("checkpoint_persistence_request_invalid_store_revision")
    if _nat(value.get("request_created_epoch")) is None:
        issues.append("checkpoint_persistence_request_invalid_created_epoch")
    for field in (
        "persistence_nonce_digest", "source_loop_receipt_digest",
        "source_loop_evidence_digest", "source_loop_registry_digest",
        "source_execution_registry_digest", "source_reobservation_registry_digest",
        "source_continuation_registry_digest", "final_lifecycle_receipt_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("checkpoint_persistence_request_invalid_digest:" + field)
    state_digest = value.get("final_lifecycle_state_digest")
    if state_digest != "" and (
        not isinstance(state_digest, str) or not _SHA256.fullmatch(state_digest)
    ):
        issues.append("checkpoint_persistence_request_invalid_final_state_digest")
    if not _REPOSITORY.fullmatch(str(value.get("repository_full_name", ""))):
        issues.append("checkpoint_persistence_request_invalid_repository")
    for field in (
        "checkpoint_id", "persistence_session_id", "loop_id", "lifecycle_id",
        "persister_id", "adapter_id", "store_id",
    ):
        if not _IDENTIFIER.fullmatch(str(value.get(field, ""))):
            issues.append("checkpoint_persistence_request_invalid_identifier:" + field)
    for field in (
        "provenance_integrity_confirmed", "source_correspondence_confirmed",
        "persistence_requested",
    ):
        if value.get(field) is not True:
            issues.append("checkpoint_persistence_request_required_true:" + field)
    if not _digest_ok(value, REQUEST_DIGEST_FIELD):
        issues.append("checkpoint_persistence_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "checkpoint_persistence_policy")
    if issues:
        return issues
    for field in _POLICY_STRING_FIELDS:
        if not isinstance(value.get(field), str) or not value[field]:
            issues.append("checkpoint_persistence_policy_invalid_string:" + field)
    for field in _POLICY_LIST_FIELDS:
        if _strings(value.get(field), nonempty=True) is None:
            issues.append("checkpoint_persistence_policy_invalid_list:" + field)
    for field in _POLICY_NAT_FIELDS:
        if _nat(value.get(field), positive=field != "evaluation_epoch") is None:
            issues.append("checkpoint_persistence_policy_invalid_nat:" + field)
    bool_fields = POLICY_FIELDS - _POLICY_STRING_FIELDS - _POLICY_LIST_FIELDS - _POLICY_NAT_FIELDS
    for field in bool_fields:
        if not isinstance(value.get(field), bool):
            issues.append("checkpoint_persistence_policy_invalid_bool:" + field)
    if not _digest_ok(value, POLICY_DIGEST_FIELD):
        issues.append("checkpoint_persistence_policy_digest_mismatch")
    return issues


def _validate_registry(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REGISTRY_FIELDS, "checkpoint_persistence_registry")
    if issues:
        return issues
    if not isinstance(value.get("registry_id"), str) or not value["registry_id"]:
        issues.append("checkpoint_persistence_registry_invalid_id")
    for field in (
        "registry_revision", "persistence_attempt_count",
        "successful_persistence_count", "last_persistence_epoch",
    ):
        if _nat(value.get(field)) is None:
            issues.append("checkpoint_persistence_registry_invalid_nat:" + field)
    nonces = _strings(value.get("consumed_persistence_nonce_digests"))
    loop_receipts = _strings(value.get("persisted_loop_receipt_digests"))
    checkpoint_ids = _strings(value.get("persisted_checkpoint_ids"))
    if nonces is None or not all(_SHA256.fullmatch(item) for item in nonces):
        issues.append("checkpoint_persistence_registry_invalid_nonce_history")
    if loop_receipts is None or not all(_SHA256.fullmatch(item) for item in loop_receipts):
        issues.append("checkpoint_persistence_registry_invalid_receipt_history")
    if checkpoint_ids is None or not all(_IDENTIFIER.fullmatch(item) for item in checkpoint_ids):
        issues.append("checkpoint_persistence_registry_invalid_checkpoint_history")
    if loop_receipts is not None and checkpoint_ids is not None:
        if len(loop_receipts) != len(checkpoint_ids):
            issues.append("checkpoint_persistence_registry_parallel_history_mismatch")
        if value.get("successful_persistence_count") != len(loop_receipts):
            issues.append("checkpoint_persistence_registry_success_count_mismatch")
    if nonces is not None and value.get("persistence_attempt_count") != len(nonces):
        issues.append("checkpoint_persistence_registry_attempt_count_mismatch")
    if value.get("successful_persistence_count", 0) > value.get("persistence_attempt_count", 0):
        issues.append("checkpoint_persistence_registry_success_exceeds_attempts")
    if not _digest_ok(value, REGISTRY_DIGEST_FIELD):
        issues.append("checkpoint_persistence_registry_digest_mismatch")
    return issues


def _validate_store_state(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, STORE_STATE_FIELDS, "checkpoint_store_state")
    if issues:
        return issues
    if value.get("schema_version") != SCHEMA_VERSION:
        issues.append("checkpoint_store_state_schema_mismatch")
    if value.get("profile_version") != PROFILE_VERSION:
        issues.append("checkpoint_store_state_profile_mismatch")
    if not isinstance(value.get("store_id"), str) or not _IDENTIFIER.fullmatch(value["store_id"]):
        issues.append("checkpoint_store_state_invalid_store_id")
    if _nat(value.get("store_revision")) is None:
        issues.append("checkpoint_store_state_invalid_revision")
    if _nat(value.get("last_committed_epoch")) is None:
        issues.append("checkpoint_store_state_invalid_epoch")
    checkpoint_ids = _strings(value.get("checkpoint_ids"))
    envelope_digests = _strings(value.get("checkpoint_envelope_digests"))
    if checkpoint_ids is None or not all(_IDENTIFIER.fullmatch(item) for item in checkpoint_ids):
        issues.append("checkpoint_store_state_invalid_checkpoint_ids")
    if envelope_digests is None or not all(_SHA256.fullmatch(item) for item in envelope_digests):
        issues.append("checkpoint_store_state_invalid_envelope_digests")
    if checkpoint_ids is not None and envelope_digests is not None:
        if len(checkpoint_ids) != len(envelope_digests):
            issues.append("checkpoint_store_state_parallel_history_mismatch")
        if value.get("store_revision") != len(checkpoint_ids):
            issues.append("checkpoint_store_state_revision_count_mismatch")
    if not _digest_ok(value, STORE_STATE_DIGEST_FIELD):
        issues.append("checkpoint_store_state_digest_mismatch")
    return issues


def _validate_source_bundle(
    *,
    loop_receipt: Mapping[str, Any],
    loop_evidence: Mapping[str, Any],
    loop_registry: Mapping[str, Any],
    execution_registry: Mapping[str, Any],
    reobservation_registry: Mapping[str, Any],
    continuation_registry: Mapping[str, Any],
    final_lifecycle_receipt: Mapping[str, Any],
    final_lifecycle_state: Mapping[str, Any] | None,
) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(loop_receipt, LOOP_RECEIPT_DIGEST_FIELD):
        issues.append("source_loop_receipt_digest_mismatch")
    if not _digest_ok(loop_evidence, LOOP_EVIDENCE_DIGEST_FIELD):
        issues.append("source_loop_evidence_digest_mismatch")
    if not _digest_ok(loop_registry, LOOP_REGISTRY_DIGEST_FIELD):
        issues.append("source_loop_registry_digest_mismatch")
    if not _digest_ok(execution_registry, EXECUTION_REGISTRY_DIGEST_FIELD):
        issues.append("source_execution_registry_digest_mismatch")
    if not _digest_ok(reobservation_registry, REOBSERVATION_REGISTRY_DIGEST_FIELD):
        issues.append("source_reobservation_registry_digest_mismatch")
    if not _digest_ok(continuation_registry, CONTINUATION_REGISTRY_DIGEST_FIELD):
        issues.append("source_continuation_registry_digest_mismatch")
    if not _digest_ok(final_lifecycle_receipt, LIFECYCLE_RECEIPT_DIGEST_FIELD):
        issues.append("source_final_lifecycle_receipt_digest_mismatch")
    state_digest = ""
    if final_lifecycle_state is not None:
        if not _digest_ok(final_lifecycle_state, LIFECYCLE_STATE_DIGEST_FIELD):
            issues.append("source_final_lifecycle_state_digest_mismatch")
        else:
            state_digest = final_lifecycle_state[LIFECYCLE_STATE_DIGEST_FIELD]
    correspondence = (
        loop_receipt.get("loop_evidence_digest") == loop_evidence.get(LOOP_EVIDENCE_DIGEST_FIELD)
        and loop_receipt.get("next_loop_registry_digest") == loop_registry.get(LOOP_REGISTRY_DIGEST_FIELD)
        and loop_receipt.get("next_execution_registry_digest") == execution_registry.get(EXECUTION_REGISTRY_DIGEST_FIELD)
        and loop_receipt.get("next_reobservation_registry_digest") == reobservation_registry.get(REOBSERVATION_REGISTRY_DIGEST_FIELD)
        and loop_receipt.get("next_continuation_registry_digest") == continuation_registry.get(CONTINUATION_REGISTRY_DIGEST_FIELD)
        and loop_receipt.get("final_lifecycle_receipt_digest") == final_lifecycle_receipt.get(LIFECYCLE_RECEIPT_DIGEST_FIELD)
        and loop_receipt.get("final_lifecycle_state_digest") == state_digest
        and loop_evidence.get("final_lifecycle_receipt_digest") == final_lifecycle_receipt.get(LIFECYCLE_RECEIPT_DIGEST_FIELD)
        and loop_evidence.get("final_lifecycle_state_digest") == state_digest
        and loop_receipt.get("codeai_disposition") in SUPPORTED_LOOP_DISPOSITIONS
        and loop_receipt.get("route_receipt_recorded") is True
        and loop_receipt.get("initial_lifecycle_receipt_consumed") is True
        and loop_receipt.get("loop_nonce_consumed") is True
        and loop_receipt.get("general_git_authority_granted") is False
        and loop_receipt.get("general_successor_stage_authority_granted") is False
        and loop_receipt.get("active_now") is False
    )
    if not correspondence:
        issues.append("source_loop_bundle_correspondence_mismatch")
    return issues


def _correspondence_valid(
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
    registry: Mapping[str, Any],
    store_state: Mapping[str, Any],
) -> bool:
    final_state_digest = (
        final_lifecycle_state[LIFECYCLE_STATE_DIGEST_FIELD]
        if final_lifecycle_state is not None else ""
    )
    return (
        request["source_loop_receipt_digest"] == loop_receipt[LOOP_RECEIPT_DIGEST_FIELD]
        and request["source_loop_evidence_digest"] == loop_evidence[LOOP_EVIDENCE_DIGEST_FIELD]
        and request["source_loop_registry_digest"] == loop_registry[LOOP_REGISTRY_DIGEST_FIELD]
        and request["source_execution_registry_digest"] == execution_registry[EXECUTION_REGISTRY_DIGEST_FIELD]
        and request["source_reobservation_registry_digest"] == reobservation_registry[REOBSERVATION_REGISTRY_DIGEST_FIELD]
        and request["source_continuation_registry_digest"] == continuation_registry[CONTINUATION_REGISTRY_DIGEST_FIELD]
        and request["final_lifecycle_receipt_digest"] == final_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD]
        and request["final_lifecycle_state_digest"] == final_state_digest
        and request["loop_id"] == loop_receipt["loop_id"]
        and request["lifecycle_id"] == loop_receipt["lifecycle_id"]
        and request["repository_full_name"] == loop_receipt["repository_full_name"]
        and policy["expected_source_loop_receipt_digest"] == loop_receipt[LOOP_RECEIPT_DIGEST_FIELD]
        and policy["expected_source_loop_evidence_digest"] == loop_evidence[LOOP_EVIDENCE_DIGEST_FIELD]
        and policy["expected_repository_full_name"] == loop_receipt["repository_full_name"]
        and request["persister_id"] in policy["authorized_persister_ids"]
        and request["adapter_id"] in policy["allowed_adapter_ids"]
        and request["store_id"] in policy["allowed_store_ids"]
        and request["store_id"] == store_state["store_id"]
        and request["expected_store_revision"] == store_state["store_revision"]
        and registry["persisted_checkpoint_ids"] == store_state["checkpoint_ids"]
        and registry["successful_persistence_count"] == len(store_state["checkpoint_ids"])
    )


def _policy_safe(request: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    required = (
        policy["allow_checkpoint_persistence"],
        policy["require_atomic_compare_and_swap"],
        policy["require_checkpoint_absence"],
        policy["require_nonce_consumption"],
    )
    forbidden = (
        policy["allow_checkpoint_overwrite"],
        policy["allow_checkpoint_delete"],
        policy["allow_network_access"],
        policy["allow_secret_material_read"],
        policy["allow_git_effect"],
        policy["allow_loop_execution"],
        policy["allow_resume_input_issuance"],
        policy["allow_automatic_resumption"],
        policy["allow_general_successor_authority"],
    )
    return (
        all(required)
        and not any(forbidden)
        and request["checkpoint_revision"] == 1
        and request["persistence_requested"] is True
    )


def _fresh_and_replay_closed(
    *,
    loop_receipt: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    registry: Mapping[str, Any],
    store_state: Mapping[str, Any],
) -> bool:
    age = policy["evaluation_epoch"] - request["request_created_epoch"]
    return (
        0 <= age <= policy["maximum_request_age"]
        and request["persistence_nonce_digest"] not in registry["consumed_persistence_nonce_digests"]
        and loop_receipt[LOOP_RECEIPT_DIGEST_FIELD] not in registry["persisted_loop_receipt_digests"]
        and request["checkpoint_id"] not in registry["persisted_checkpoint_ids"]
        and request["checkpoint_id"] not in store_state["checkpoint_ids"]
        and len(registry["consumed_persistence_nonce_digests"]) < policy["maximum_registry_entries"]
        and len(store_state["checkpoint_ids"]) < policy["maximum_store_entries"]
    )
