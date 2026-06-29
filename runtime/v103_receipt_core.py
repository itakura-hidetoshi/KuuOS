#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_repository_atomic_checkpoint_creation_types_v1_02 import (
    CHECKPOINT_CREATION_ABORTED,
    CHECKPOINT_CREATION_COMMITTED,
)
from runtime.kuuos_repository_atomic_checkpoint_creation_v1_02 import (
    repository_atomic_checkpoint_creation_result_issues,
)
from runtime.v103_receipt_helpers import (
    execution_report_issues,
    receipt_policy_issues,
    snapshot_digest,
)
from runtime.v103_receipt_policy import RECEIPT_CONFIRMED, RECEIPT_REJECTED
from runtime.v103_result import CheckpointReceiptResult, checkpoint_receipt_result_digest


def _snapshot_valid(snapshot: Mapping[str, Any], required: tuple[str, ...]) -> bool:
    return bool(
        all(key in snapshot for key in required)
        and snapshot.get("snapshot_digest") == snapshot_digest(snapshot)
    )


def _v102_issues(result, final_state, final_registry, inputs: Mapping[str, Any]):
    try:
        values = dict(inputs)
        values.pop("transaction_id", None)
        return repository_atomic_checkpoint_creation_result_issues(
            result,
            final_state,
            final_registry,
            **values,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("v102_inputs_invalid",)


def construct_receipt(
    receipt_id: str,
    result,
    final_state,
    final_registry,
    v102_inputs: Mapping[str, Any],
    policy,
    report,
    reference_snapshot: Mapping[str, Any],
    nonce_snapshot: Mapping[str, Any],
    identity_snapshot: Mapping[str, Any],
    *,
    evaluated_at_epoch_seconds: int,
) -> CheckpointReceiptResult:
    source_state = v102_inputs.get("source_checkpoint_state")
    source_registry = v102_inputs.get("source_nonce_registry")
    v102_valid = not _v102_issues(result, final_state, final_registry, v102_inputs)
    v102_binding = bool(
        source_state is not None
        and source_registry is not None
        and result.source_checkpoint_state_digest == source_state.state_digest
        and result.final_checkpoint_state_digest == final_state.state_digest
        and result.source_nonce_registry_digest == source_registry.registry_digest
        and result.final_nonce_registry_digest == final_registry.registry_digest
    )
    v102_committed = bool(v102_valid and result.status == CHECKPOINT_CREATION_COMMITTED)
    v102_aborted = bool(v102_valid and result.status == CHECKPOINT_CREATION_ABORTED)
    policy_valid = not receipt_policy_issues(policy)
    report_valid = not execution_report_issues(report)
    report_binding = bool(
        report.transaction_id == result.transaction_id
        and report.authorization_certificate_digest == result.authorization_certificate_digest
        and report.execution_policy_digest == result.execution_policy_digest
        and report.request_digest == result.request_digest
        and report.v102_result_digest == result.result_digest
        and report.repository_id == result.repository_id
        and report.git_dir_fingerprint == result.git_dir_fingerprint
        and report.checkpoint_reference == result.checkpoint_reference
        and report.expected_old_oid == result.expected_old_oid
        and report.proposed_new_oid == result.proposed_new_oid
        and report.authorization_nonce == result.authorization_nonce
        and report.executor_id == result.executor_id
    )
    report_age = evaluated_at_epoch_seconds - report.execution_completed_at_epoch_seconds
    report_fresh = 0 <= report_age <= policy.max_report_age_seconds
    duration = report.execution_completed_at_epoch_seconds - report.execution_started_at_epoch_seconds
    duration_valid = 0 <= duration <= policy.max_external_duration_seconds

    reference_required = (
        "snapshot_id", "observer_id", "transaction_id", "repository_id",
        "git_dir_fingerprint", "checkpoint_reference", "observed_oid",
        "direct", "symbolic", "reference_store_read", "working_tree_read",
        "reflog_read", "remote_read", "checkpoint_state_sequence_number",
        "sequence_number", "recorded_at_epoch_seconds", "snapshot_digest",
    )
    nonce_required = (
        "snapshot_id", "observer_id", "transaction_id", "registry_id",
        "authority_id", "upstream_snapshot_digest", "consumed_nonces",
        "revoked_nonces", "nonce_registry_sequence_number", "sequence_number",
        "recorded_at_epoch_seconds", "snapshot_digest",
    )
    identity_required = (
        "snapshot_id", "observer_id", "transaction_id", "pre_repository_id",
        "post_repository_id", "pre_git_dir_fingerprint",
        "post_git_dir_fingerprint", "sequence_number",
        "recorded_at_epoch_seconds", "snapshot_digest",
    )
    reference_valid = _snapshot_valid(reference_snapshot, reference_required)
    nonce_valid = _snapshot_valid(nonce_snapshot, nonce_required)
    identity_valid = _snapshot_valid(identity_snapshot, identity_required)

    observers = (
        reference_snapshot.get("observer_id"),
        nonce_snapshot.get("observer_id"),
        identity_snapshot.get("observer_id"),
    )
    observer_authorized = bool(
        observers[0] == observers[1] == observers[2]
        and observers[0] in policy.authorized_observer_ids
    )
    transaction_binding = bool(
        report.transaction_id
        == reference_snapshot.get("transaction_id")
        == nonce_snapshot.get("transaction_id")
        == identity_snapshot.get("transaction_id")
        == result.transaction_id
    )
    sequence_ordered = bool(
        report.executor_sequence_number < reference_snapshot.get("sequence_number", -1)
        < nonce_snapshot.get("sequence_number", -1)
        < identity_snapshot.get("sequence_number", -1)
    )
    times = (
        report.execution_started_at_epoch_seconds,
        report.execution_completed_at_epoch_seconds,
        reference_snapshot.get("recorded_at_epoch_seconds", -1),
        nonce_snapshot.get("recorded_at_epoch_seconds", -1),
        identity_snapshot.get("recorded_at_epoch_seconds", -1),
    )
    no_future = bool(
        result.execution_completed_at_epoch_seconds <= times[0]
        and times[0] <= times[1] <= times[2] <= times[3] <= times[4]
        and times[4] <= evaluated_at_epoch_seconds
    )
    observation_fresh = bool(
        all(
            0 <= evaluated_at_epoch_seconds - value <= policy.max_observation_age_seconds
            for value in times[2:]
        )
    )
    no_forbidden = bool(
        not report.reported_effects
        and tuple(policy.required_absent_effects)
    )

    identity_exact = bool(
        identity_snapshot.get("pre_repository_id") == result.repository_id
        == identity_snapshot.get("post_repository_id")
        and identity_snapshot.get("pre_git_dir_fingerprint")
        == result.git_dir_fingerprint
        == identity_snapshot.get("post_git_dir_fingerprint")
    )
    target_state = final_state if v102_committed else source_state
    target_registry = final_registry if v102_committed else source_registry
    reference_exact = bool(
        target_state is not None
        and reference_snapshot.get("repository_id") == target_state.repository_id
        and reference_snapshot.get("git_dir_fingerprint") == target_state.git_dir_fingerprint
        and reference_snapshot.get("checkpoint_reference") == target_state.checkpoint_reference
        and reference_snapshot.get("observed_oid") == target_state.current_oid
        and reference_snapshot.get("direct") == target_state.direct
        and reference_snapshot.get("symbolic") == target_state.symbolic
        and reference_snapshot.get("reference_store_read") == target_state.reference_store_source
        and reference_snapshot.get("working_tree_read") == target_state.working_tree_source
        and reference_snapshot.get("reflog_read") == target_state.reflog_source
        and reference_snapshot.get("remote_read") == target_state.remote_source
        and reference_snapshot.get("checkpoint_state_sequence_number")
        == target_state.sequence_number
    )
    nonce_exact = bool(
        target_registry is not None
        and nonce_snapshot.get("registry_id") == target_registry.registry_id
        and nonce_snapshot.get("authority_id") == target_registry.authority_id
        and nonce_snapshot.get("upstream_snapshot_digest")
        == target_registry.upstream_snapshot_digest
        and tuple(nonce_snapshot.get("consumed_nonces", ()))
        == target_registry.consumed_nonces
        and tuple(nonce_snapshot.get("revoked_nonces", ()))
        == target_registry.revoked_nonces
        and nonce_snapshot.get("nonce_registry_sequence_number")
        == target_registry.sequence_number
    )
    committed_report = bool(
        report.creation_attempted
        and report.compare_and_swap_succeeded
        and report.checkpoint_created
        and report.nonce_consumed
        and not report.aborted_without_mutation
    )
    aborted_report = bool(
        report.creation_attempted == result.compare_and_swap_attempted
        and not report.compare_and_swap_succeeded
        and not report.checkpoint_created
        and not report.nonce_consumed
        and report.aborted_without_mutation
    )
    shared = (
        v102_valid, v102_binding, policy_valid, report_valid, report_binding,
        report_fresh, duration_valid, reference_valid, nonce_valid,
        identity_valid, observer_authorized, transaction_binding,
        sequence_ordered, no_future, observation_fresh, no_forbidden,
        identity_exact, reference_exact, nonce_exact,
    )
    committed_confirmed = bool(v102_committed and committed_report and all(shared))
    aborted_confirmed = bool(v102_aborted and aborted_report and all(shared))
    consistent = committed_confirmed or aborted_confirmed
    checks = {
        "v102_result_valid": v102_valid,
        "v102_result_binding_exact": v102_binding,
        "v102_committed": v102_committed,
        "v102_aborted": v102_aborted,
        "receipt_policy_valid": policy_valid,
        "execution_report_valid": report_valid,
        "execution_report_binding_exact": report_binding,
        "execution_report_fresh": report_fresh,
        "external_execution_duration_within_policy": duration_valid,
        "reference_snapshot_valid": reference_valid,
        "nonce_snapshot_valid": nonce_valid,
        "identity_snapshot_valid": identity_valid,
        "observer_authorized": observer_authorized,
        "transaction_binding_exact": transaction_binding,
        "observation_sequence_ordered": sequence_ordered,
        "no_future_evidence": no_future,
        "observations_fresh": observation_fresh,
        "no_forbidden_execution_effect": no_forbidden,
        "repository_identity_and_git_dir_stable": identity_exact,
        "reference_snapshot_exact": reference_exact,
        "nonce_snapshot_exact": nonce_exact,
        "committed_report_consistent": committed_report,
        "aborted_report_consistent": aborted_report,
        "committed_receipt_confirmed": committed_confirmed,
        "aborted_receipt_confirmed": aborted_confirmed,
        "supplied_external_report_consistent": consistent,
        "external_report_independently_trusted": False,
        "live_execution_proven": False,
        "receipt_performed_checkpoint_mutation": False,
        "receipt_performed_nonce_consumption": False,
        "receipt_invoked_live_git_command": False,
        "receipt_mutated_live_repository": False,
    }
    evidence_digests = {
        "policy": policy.policy_digest,
        "report": report.report_digest,
        "reference_snapshot": str(reference_snapshot.get("snapshot_digest", "")),
        "nonce_snapshot": str(nonce_snapshot.get("snapshot_digest", "")),
        "identity_snapshot": str(identity_snapshot.get("snapshot_digest", "")),
    }
    receipt = CheckpointReceiptResult(
        receipt_id=receipt_id,
        status=RECEIPT_CONFIRMED if consistent else RECEIPT_REJECTED,
        transaction_id=result.transaction_id,
        result_digest=result.result_digest,
        checks=checks,
        evidence_digests=evidence_digests,
        receipt_digest="",
    )
    return replace(receipt, receipt_digest=checkpoint_receipt_result_digest(receipt))
