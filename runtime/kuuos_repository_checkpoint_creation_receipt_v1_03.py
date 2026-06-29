#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.v103_receipt_core import construct_receipt
from runtime.v103_receipt_helpers import (
    build_execution_report,
    build_receipt_policy,
    execution_report_issues,
    receipt_policy_issues,
    snapshot_digest,
)
from runtime.v103_receipt_policy import RECEIPT_CONFIRMED, RECEIPT_REJECTED
from runtime.v103_result import checkpoint_receipt_result_digest

build_repository_checkpoint_creation_receipt_policy = build_receipt_policy
build_repository_checkpoint_creation_execution_report = build_execution_report
repository_checkpoint_creation_receipt_policy_issues = receipt_policy_issues
repository_checkpoint_creation_execution_report_issues = execution_report_issues


def _signed_snapshot(values: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = dict(values)
    snapshot["snapshot_digest"] = ""
    snapshot["snapshot_digest"] = snapshot_digest(snapshot)
    return snapshot


def build_repository_checkpoint_reference_snapshot(
    snapshot_id: str,
    observer_id: str,
    transaction_id: str,
    state,
    *,
    sequence_number: int,
    recorded_at_epoch_seconds: int,
) -> dict[str, Any]:
    return _signed_snapshot(
        {
            "snapshot_id": snapshot_id,
            "observer_id": observer_id,
            "transaction_id": transaction_id,
            "repository_id": state.repository_id,
            "git_dir_fingerprint": state.git_dir_fingerprint,
            "checkpoint_reference": state.checkpoint_reference,
            "observed_oid": state.current_oid,
            "direct": state.direct,
            "symbolic": state.symbolic,
            "reference_store_read": state.reference_store_source,
            "working_tree_read": state.working_tree_source,
            "reflog_read": state.reflog_source,
            "remote_read": state.remote_source,
            "checkpoint_state_sequence_number": state.sequence_number,
            "sequence_number": sequence_number,
            "recorded_at_epoch_seconds": recorded_at_epoch_seconds,
        }
    )


def build_repository_checkpoint_nonce_registry_snapshot(
    snapshot_id: str,
    observer_id: str,
    transaction_id: str,
    registry,
    *,
    sequence_number: int,
    recorded_at_epoch_seconds: int,
) -> dict[str, Any]:
    return _signed_snapshot(
        {
            "snapshot_id": snapshot_id,
            "observer_id": observer_id,
            "transaction_id": transaction_id,
            "registry_id": registry.registry_id,
            "authority_id": registry.authority_id,
            "upstream_snapshot_digest": registry.upstream_snapshot_digest,
            "consumed_nonces": list(registry.consumed_nonces),
            "revoked_nonces": list(registry.revoked_nonces),
            "nonce_registry_sequence_number": registry.sequence_number,
            "sequence_number": sequence_number,
            "recorded_at_epoch_seconds": recorded_at_epoch_seconds,
        }
    )


def build_repository_checkpoint_identity_snapshot(
    snapshot_id: str,
    observer_id: str,
    transaction_id: str,
    *,
    pre_repository_id: str,
    post_repository_id: str,
    pre_git_dir_fingerprint: str,
    post_git_dir_fingerprint: str,
    sequence_number: int,
    recorded_at_epoch_seconds: int,
) -> dict[str, Any]:
    return _signed_snapshot(
        {
            "snapshot_id": snapshot_id,
            "observer_id": observer_id,
            "transaction_id": transaction_id,
            "pre_repository_id": pre_repository_id,
            "post_repository_id": post_repository_id,
            "pre_git_dir_fingerprint": pre_git_dir_fingerprint,
            "post_git_dir_fingerprint": post_git_dir_fingerprint,
            "sequence_number": sequence_number,
            "recorded_at_epoch_seconds": recorded_at_epoch_seconds,
        }
    )


def certify_repository_checkpoint_creation_receipt(
    receipt_id: str,
    result,
    final_checkpoint_state,
    final_nonce_registry,
    v102_inputs: Mapping[str, Any],
    policy,
    execution_report,
    reference_snapshot: Mapping[str, Any],
    nonce_registry_snapshot: Mapping[str, Any],
    identity_snapshot: Mapping[str, Any],
    *,
    evaluated_at_epoch_seconds: int,
):
    if not receipt_id:
        raise ValueError("checkpoint_creation_receipt_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("checkpoint_creation_receipt_time_negative")
    for issues, prefix in (
        (receipt_policy_issues(policy), "checkpoint_receipt_policy_invalid"),
        (execution_report_issues(execution_report), "checkpoint_execution_report_invalid"),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    receipt = construct_receipt(
        receipt_id,
        result,
        final_checkpoint_state,
        final_nonce_registry,
        v102_inputs,
        policy,
        execution_report,
        reference_snapshot,
        nonce_registry_snapshot,
        identity_snapshot,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_creation_receipt_issues(
        receipt,
        result,
        final_checkpoint_state,
        final_nonce_registry,
        v102_inputs,
        policy,
        execution_report,
        reference_snapshot,
        nonce_registry_snapshot,
        identity_snapshot,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_creation_receipt_invalid:{issues[0]}")
    return receipt


def repository_checkpoint_creation_receipt_issues(
    receipt,
    result,
    final_checkpoint_state,
    final_nonce_registry,
    v102_inputs: Mapping[str, Any],
    policy,
    execution_report,
    reference_snapshot: Mapping[str, Any],
    nonce_registry_snapshot: Mapping[str, Any],
    identity_snapshot: Mapping[str, Any],
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_receipt(
        receipt.receipt_id,
        result,
        final_checkpoint_state,
        final_nonce_registry,
        v102_inputs,
        policy,
        execution_report,
        reference_snapshot,
        nonce_registry_snapshot,
        identity_snapshot,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if receipt.to_dict() != expected.to_dict():
        issues.append("checkpoint_receipt_recomputation_mismatch")
    if receipt.status not in (RECEIPT_CONFIRMED, RECEIPT_REJECTED):
        issues.append("checkpoint_receipt_status_invalid")
    for key in (
        "external_report_independently_trusted",
        "live_execution_proven",
        "receipt_performed_checkpoint_mutation",
        "receipt_performed_nonce_consumption",
        "receipt_invoked_live_git_command",
        "receipt_mutated_live_repository",
    ):
        if receipt.checks.get(key):
            issues.append("checkpoint_receipt_forbidden_claim")
            break
    if receipt.status == RECEIPT_CONFIRMED and not receipt.checks.get(
        "supplied_external_report_consistent"
    ):
        issues.append("checkpoint_receipt_confirmed_without_consistency")
    if receipt.receipt_digest != checkpoint_receipt_result_digest(receipt):
        issues.append("checkpoint_receipt_digest_mismatch")
    return tuple(issues)
