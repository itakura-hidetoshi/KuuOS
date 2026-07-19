#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import *


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "resumption_admission_request")
    if issues:
        return issues
    string_fields = REQUEST_FIELDS - {
        "requested_resume_effect_budget", "requested_resume_execution_command_budget",
        "requested_resume_execution_output_bytes", "request_created_epoch",
        "provenance_integrity_confirmed", "source_correspondence_confirmed",
        "checkpoint_read_requested", "resumption_input_requested", REQUEST_DIGEST_FIELD,
    }
    for field in string_fields:
        if not isinstance(value.get(field), str) or not value[field]:
            issues.append("resumption_admission_request_invalid_string:" + field)
    for field in (
        "requested_resume_effect_budget", "requested_resume_execution_command_budget",
        "requested_resume_execution_output_bytes", "request_created_epoch",
    ):
        if _nat(value.get(field), positive=field != "request_created_epoch") is None:
            issues.append("resumption_admission_request_invalid_nat:" + field)
    for field in (
        "provenance_integrity_confirmed", "source_correspondence_confirmed",
        "checkpoint_read_requested", "resumption_input_requested",
    ):
        if not isinstance(value.get(field), bool):
            issues.append("resumption_admission_request_invalid_bool:" + field)
    for field in (
        "resumption_nonce_digest", "checkpoint_envelope_digest",
        "source_persistence_receipt_digest", "source_persistence_evidence_digest",
        "source_persistence_registry_digest", "source_store_state_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("resumption_admission_request_invalid_digest:" + field)
    if not _REPOSITORY.fullmatch(value["repository_full_name"]):
        issues.append("resumption_admission_request_invalid_repository")
    for field in (
        "resumption_session_id", "checkpoint_id", "loop_id", "lifecycle_id",
        "store_id", "reader_id", "adapter_id",
    ):
        if not _IDENTIFIER.fullmatch(value[field]):
            issues.append("resumption_admission_request_invalid_identifier:" + field)
    if not _digest_ok(value, REQUEST_DIGEST_FIELD):
        issues.append("resumption_admission_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "resumption_admission_policy")
    if issues:
        return issues
    for field in (
        "expected_source_persistence_receipt_digest",
        "expected_source_persistence_evidence_digest",
        "expected_checkpoint_envelope_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("resumption_admission_policy_invalid_digest:" + field)
    if not isinstance(value.get("expected_repository_full_name"), str) or not _REPOSITORY.fullmatch(
        value["expected_repository_full_name"]
    ):
        issues.append("resumption_admission_policy_invalid_repository")
    for field in ("authorized_reader_ids", "allowed_adapter_ids", "allowed_store_ids"):
        parsed = _strings(value.get(field), nonempty=True)
        if parsed is None or not all(_IDENTIFIER.fullmatch(item) for item in parsed):
            issues.append("resumption_admission_policy_invalid_list:" + field)
    for field in (
        "maximum_request_age", "maximum_registry_entries",
        "maximum_adapter_command_count", "maximum_adapter_output_bytes",
        "maximum_resume_effect_budget", "maximum_resume_execution_command_budget",
        "maximum_resume_execution_output_bytes", "evaluation_epoch",
    ):
        if _nat(value.get(field), positive=field != "evaluation_epoch") is None:
            issues.append("resumption_admission_policy_invalid_nat:" + field)
    bool_fields = POLICY_FIELDS - {
        "expected_source_persistence_receipt_digest",
        "expected_source_persistence_evidence_digest",
        "expected_checkpoint_envelope_digest", "expected_repository_full_name",
        "authorized_reader_ids", "allowed_adapter_ids", "allowed_store_ids",
        "maximum_request_age", "maximum_registry_entries",
        "maximum_adapter_command_count", "maximum_adapter_output_bytes",
        "maximum_resume_effect_budget", "maximum_resume_execution_command_budget",
        "maximum_resume_execution_output_bytes", "evaluation_epoch", POLICY_DIGEST_FIELD,
    }
    for field in bool_fields:
        if not isinstance(value.get(field), bool):
            issues.append("resumption_admission_policy_invalid_bool:" + field)
    if not _digest_ok(value, POLICY_DIGEST_FIELD):
        issues.append("resumption_admission_policy_digest_mismatch")
    return issues


def _validate_registry(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REGISTRY_FIELDS, "resumption_admission_registry")
    if issues:
        return issues
    if not isinstance(value.get("registry_id"), str) or not _IDENTIFIER.fullmatch(value["registry_id"]):
        issues.append("resumption_admission_registry_invalid_id")
    for field in (
        "registry_revision", "resumption_attempt_count",
        "successful_resumption_admission_count", "last_resumption_epoch",
    ):
        if _nat(value.get(field)) is None:
            issues.append("resumption_admission_registry_invalid_nat:" + field)
    histories = {
        "consumed_resumption_nonce_digests": _strings(value.get("consumed_resumption_nonce_digests")),
        "admitted_checkpoint_ids": _strings(value.get("admitted_checkpoint_ids")),
        "admitted_checkpoint_envelope_digests": _strings(value.get("admitted_checkpoint_envelope_digests")),
        "admitted_persistence_receipt_digests": _strings(value.get("admitted_persistence_receipt_digests")),
    }
    for field, parsed in histories.items():
        if parsed is None:
            issues.append("resumption_admission_registry_invalid_history:" + field)
    if histories["consumed_resumption_nonce_digests"] is not None and not all(
        _SHA256.fullmatch(item) for item in histories["consumed_resumption_nonce_digests"]
    ):
        issues.append("resumption_admission_registry_invalid_nonce_digest")
    for field in ("admitted_checkpoint_envelope_digests", "admitted_persistence_receipt_digests"):
        parsed = histories[field]
        if parsed is not None and not all(_SHA256.fullmatch(item) for item in parsed):
            issues.append("resumption_admission_registry_invalid_digest_history:" + field)
    checkpoint_ids = histories["admitted_checkpoint_ids"]
    if checkpoint_ids is not None and not all(_IDENTIFIER.fullmatch(item) for item in checkpoint_ids):
        issues.append("resumption_admission_registry_invalid_checkpoint_id")
    if all(histories[field] is not None for field in histories):
        successful = len(histories["admitted_checkpoint_ids"] or ())
        if not (
            successful == len(histories["admitted_checkpoint_envelope_digests"] or ())
            == len(histories["admitted_persistence_receipt_digests"] or ())
        ):
            issues.append("resumption_admission_registry_parallel_history_mismatch")
        if value["successful_resumption_admission_count"] != successful:
            issues.append("resumption_admission_registry_success_count_mismatch")
        if value["resumption_attempt_count"] != len(histories["consumed_resumption_nonce_digests"] or ()):
            issues.append("resumption_admission_registry_attempt_count_mismatch")
        if value["registry_revision"] != value["resumption_attempt_count"]:
            issues.append("resumption_admission_registry_revision_count_mismatch")
    if value.get("successful_resumption_admission_count", 0) > value.get("resumption_attempt_count", 0):
        issues.append("resumption_admission_registry_success_exceeds_attempts")
    if not _digest_ok(value, REGISTRY_DIGEST_FIELD):
        issues.append("resumption_admission_registry_digest_mismatch")
    return issues


def _validate_sources(
    persistence_receipt: Mapping[str, Any],
    persistence_evidence: Mapping[str, Any],
    persistence_registry: Mapping[str, Any],
    store_state: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(persistence_receipt, PERSISTENCE_RECEIPT_DIGEST_FIELD):
        issues.append("source_persistence_receipt_digest_mismatch")
    if not _digest_ok(persistence_evidence, PERSISTENCE_EVIDENCE_DIGEST_FIELD):
        issues.append("source_persistence_evidence_digest_mismatch")
    if not _digest_ok(persistence_registry, PERSISTENCE_REGISTRY_DIGEST_FIELD):
        issues.append("source_persistence_registry_digest_mismatch")
    if not _digest_ok(store_state, STORE_STATE_DIGEST_FIELD):
        issues.append("source_store_state_digest_mismatch")
    checkpoint_id = persistence_receipt.get("checkpoint_id")
    checkpoint_digest = persistence_receipt.get("checkpoint_envelope_digest")
    correspondence = (
        persistence_receipt.get("codeai_disposition") == DISPOSITION_PERSISTED
        and persistence_receipt.get("checkpoint_persisted") is True
        and persistence_receipt.get("checkpoint_conflict_observed") is False
        and persistence_receipt.get("checkpoint_persistence_failed") is False
        and persistence_receipt.get("checkpoint_evidence_quarantined") is False
        and persistence_receipt.get("resume_input_issued") is False
        and persistence_receipt.get("automatic_resumption_performed") is False
        and persistence_receipt.get("general_successor_stage_authority_granted") is False
        and persistence_receipt.get("persistence_evidence_digest")
            == persistence_evidence.get(PERSISTENCE_EVIDENCE_DIGEST_FIELD)
        and persistence_receipt.get("next_persistence_registry_digest")
            == persistence_registry.get(PERSISTENCE_REGISTRY_DIGEST_FIELD)
        and persistence_receipt.get("next_store_state_digest")
            == store_state.get(STORE_STATE_DIGEST_FIELD)
        and checkpoint_id in store_state.get("checkpoint_ids", [])
        and checkpoint_digest in store_state.get("checkpoint_envelope_digests", [])
        and checkpoint_id in persistence_registry.get("persisted_checkpoint_ids", [])
        and persistence_receipt.get("source_loop_receipt_digest")
            in persistence_registry.get("persisted_loop_receipt_digests", [])
    )
    if not correspondence:
        issues.append("source_persistence_bundle_correspondence_mismatch")
    return issues


def _correspondence_valid(
    *,
    persistence_receipt: Mapping[str, Any],
    persistence_evidence: Mapping[str, Any],
    persistence_registry: Mapping[str, Any],
    store_state: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    return (
        request["source_persistence_receipt_digest"] == persistence_receipt[PERSISTENCE_RECEIPT_DIGEST_FIELD]
        and request["source_persistence_evidence_digest"] == persistence_evidence[PERSISTENCE_EVIDENCE_DIGEST_FIELD]
        and request["source_persistence_registry_digest"] == persistence_registry[PERSISTENCE_REGISTRY_DIGEST_FIELD]
        and request["source_store_state_digest"] == store_state[STORE_STATE_DIGEST_FIELD]
        and request["checkpoint_id"] == persistence_receipt["checkpoint_id"]
        and request["checkpoint_envelope_digest"] == persistence_receipt["checkpoint_envelope_digest"]
        and request["loop_id"] == persistence_receipt["loop_id"]
        and request["lifecycle_id"] == persistence_receipt["lifecycle_id"]
        and request["repository_full_name"] == persistence_receipt["repository_full_name"]
        and request["store_id"] == persistence_receipt["store_id"] == store_state["store_id"]
        and policy["expected_source_persistence_receipt_digest"] == persistence_receipt[PERSISTENCE_RECEIPT_DIGEST_FIELD]
        and policy["expected_source_persistence_evidence_digest"] == persistence_evidence[PERSISTENCE_EVIDENCE_DIGEST_FIELD]
        and policy["expected_checkpoint_envelope_digest"] == persistence_receipt["checkpoint_envelope_digest"]
        and policy["expected_repository_full_name"] == persistence_receipt["repository_full_name"]
        and request["reader_id"] in policy["authorized_reader_ids"]
        and request["adapter_id"] in policy["allowed_adapter_ids"]
        and request["store_id"] in policy["allowed_store_ids"]
    )


def _policy_safe(request: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    required = (
        policy["allow_checkpoint_read"], policy["require_committed_checkpoint"],
        policy["require_exact_checkpoint_envelope_digest"],
        policy["require_nonce_consumption"], policy["allow_resumption_input_issuance"],
    )
    forbidden = (
        policy["allow_loop_execution"], policy["allow_git_effect"],
        policy["allow_automatic_resumption"], policy["allow_network_access"],
        policy["allow_secret_material_read"], policy["allow_general_successor_authority"],
    )
    return (
        all(required) and not any(forbidden)
        and request["checkpoint_read_requested"] is True
        and request["resumption_input_requested"] is True
        and request["provenance_integrity_confirmed"] is True
        and request["source_correspondence_confirmed"] is True
        and request["requested_resume_effect_budget"] <= policy["maximum_resume_effect_budget"]
        and request["requested_resume_execution_command_budget"] <= policy["maximum_resume_execution_command_budget"]
        and request["requested_resume_execution_output_bytes"] <= policy["maximum_resume_execution_output_bytes"]
    )


def _fresh_and_replay_closed(
    request: Mapping[str, Any], policy: Mapping[str, Any], registry: Mapping[str, Any]
) -> bool:
    age = policy["evaluation_epoch"] - request["request_created_epoch"]
    return (
        0 <= age <= policy["maximum_request_age"]
        and request["resumption_nonce_digest"] not in registry["consumed_resumption_nonce_digests"]
        and request["checkpoint_id"] not in registry["admitted_checkpoint_ids"]
        and request["checkpoint_envelope_digest"] not in registry["admitted_checkpoint_envelope_digests"]
        and request["source_persistence_receipt_digest"] not in registry["admitted_persistence_receipt_digests"]
        and len(registry["consumed_resumption_nonce_digests"]) < policy["maximum_registry_entries"]
    )
