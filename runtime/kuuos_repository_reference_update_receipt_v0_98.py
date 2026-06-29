#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
from typing import Any, Mapping

from runtime.kuuos_repository_atomic_reference_update_types_v0_97 import (
    REFERENCE_UPDATE_COMMITTED,
    RepositoryAtomicReferenceUpdateResult,
    RepositoryReferenceNonceRegistry,
    RepositoryReferenceState,
)
from runtime.kuuos_repository_atomic_reference_update_v0_97 import (
    repository_atomic_reference_update_result_issues,
    repository_reference_nonce_registry_issues,
    repository_reference_state_issues,
)
from runtime.kuuos_repository_reference_update_receipt_types_v0_98 import (
    RECEIPT_COMMITTED,
    RECEIPT_REJECTED,
    RepositoryPostReferenceObservation,
    RepositoryReferenceNonceConsumptionReceipt,
    RepositoryReferenceUpdateExecutionReport,
    RepositoryReferenceUpdateReceipt,
    RepositoryReferenceUpdateReceiptPolicy,
    repository_post_reference_observation_digest,
    repository_reference_nonce_consumption_receipt_digest,
    repository_reference_update_execution_report_digest,
    repository_reference_update_receipt_digest,
    repository_reference_update_receipt_policy_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_reference_update_receipt_policy(
    policy_id: str,
    *,
    authorized_observer_ids: tuple[str, ...],
    max_execution_report_age_seconds: int,
    max_post_reference_observation_age_seconds: int,
    max_nonce_consumption_receipt_age_seconds: int,
) -> RepositoryReferenceUpdateReceiptPolicy:
    policy = RepositoryReferenceUpdateReceiptPolicy(
        policy_id=policy_id,
        authorized_observer_ids=_canonical_strings(authorized_observer_ids),
        max_execution_report_age_seconds=max_execution_report_age_seconds,
        max_post_reference_observation_age_seconds=(
            max_post_reference_observation_age_seconds
        ),
        max_nonce_consumption_receipt_age_seconds=(
            max_nonce_consumption_receipt_age_seconds
        ),
        require_exact_transaction_binding=True,
        require_reference_store_source=True,
        require_working_tree_ignored=True,
        require_atomic_reference_nonce_transition=True,
        allow_force_update=False,
        allow_reference_delete=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_reference_update_receipt_policy_digest(policy),
    )
    issues = repository_reference_update_receipt_policy_issues(policy)
    if issues:
        raise ValueError(f"reference_update_receipt_policy_invalid:{issues[0]}")
    return policy


def repository_reference_update_receipt_policy_issues(
    policy: RepositoryReferenceUpdateReceiptPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("reference_update_receipt_policy_id_missing")
    if (
        policy.authorized_observer_ids
        != _canonical_strings(policy.authorized_observer_ids)
        or not policy.authorized_observer_ids
        or any(not value for value in policy.authorized_observer_ids)
    ):
        issues.append("reference_update_receipt_observer_ids_invalid")
    if any(
        value <= 0
        for value in (
            policy.max_execution_report_age_seconds,
            policy.max_post_reference_observation_age_seconds,
            policy.max_nonce_consumption_receipt_age_seconds,
        )
    ):
        issues.append("reference_update_receipt_policy_bound_invalid")
    if not all(
        (
            policy.require_exact_transaction_binding,
            policy.require_reference_store_source,
            policy.require_working_tree_ignored,
            policy.require_atomic_reference_nonce_transition,
        )
    ):
        issues.append("reference_update_receipt_required_safeguard_disabled")
    if policy.allow_force_update:
        issues.append("reference_update_receipt_force_policy_forbidden")
    if policy.allow_reference_delete:
        issues.append("reference_update_receipt_delete_policy_forbidden")
    if policy.allow_push:
        issues.append("reference_update_receipt_push_policy_forbidden")
    if policy.policy_digest != repository_reference_update_receipt_policy_digest(policy):
        issues.append("reference_update_receipt_policy_digest_mismatch")
    return tuple(issues)


def build_repository_reference_update_execution_report(
    report_id: str,
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    *,
    executor_id: str,
    reference_update_attempted: bool,
    reference_update_performed: bool,
    compare_and_swap_succeeded: bool,
    branch_updated: bool,
    nonce_consumed: bool,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
    force_update_performed: bool = False,
    reference_delete_performed: bool = False,
    head_updated: bool = False,
    tag_updated: bool = False,
    remote_reference_updated: bool = False,
    push_performed: bool = False,
    index_write_performed: bool = False,
    working_tree_write_performed: bool = False,
    object_database_write_performed: bool = False,
    signing_performed: bool = False,
) -> RepositoryReferenceUpdateExecutionReport:
    report = RepositoryReferenceUpdateExecutionReport(
        report_id=report_id,
        transaction_id=atomic_update_result.transaction_id,
        atomic_update_result_digest=atomic_update_result.result_digest,
        repository_id=atomic_update_result.repository_id,
        git_dir_fingerprint=atomic_update_result.git_dir_fingerprint,
        target_reference=atomic_update_result.target_reference,
        expected_old_oid=atomic_update_result.expected_old_oid,
        proposed_new_oid=atomic_update_result.proposed_new_oid,
        authorization_nonce=atomic_update_result.authorization_nonce,
        executor_id=executor_id,
        reference_update_attempted=reference_update_attempted,
        reference_update_performed=reference_update_performed,
        compare_and_swap_succeeded=compare_and_swap_succeeded,
        branch_updated=branch_updated,
        nonce_consumed=nonce_consumed,
        force_update_performed=force_update_performed,
        reference_delete_performed=reference_delete_performed,
        head_updated=head_updated,
        tag_updated=tag_updated,
        remote_reference_updated=remote_reference_updated,
        push_performed=push_performed,
        index_write_performed=index_write_performed,
        working_tree_write_performed=working_tree_write_performed,
        object_database_write_performed=object_database_write_performed,
        signing_performed=signing_performed,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        report_digest="",
    )
    report = replace(
        report,
        report_digest=repository_reference_update_execution_report_digest(report),
    )
    issues = repository_reference_update_execution_report_issues(report)
    if issues:
        raise ValueError(f"reference_update_execution_report_invalid:{issues[0]}")
    return report


def repository_reference_update_execution_report_issues(
    report: RepositoryReferenceUpdateExecutionReport,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            report.report_id,
            report.transaction_id,
            report.repository_id,
            report.target_reference,
            report.authorization_nonce,
            report.executor_id,
        )
    ):
        issues.append("reference_update_execution_report_required_field_missing")
    for digest in (
        report.atomic_update_result_digest,
        report.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("reference_update_execution_report_digest_invalid")
            break
    if not _HEX40.fullmatch(report.expected_old_oid):
        issues.append("reference_update_execution_report_old_oid_invalid")
    if not _HEX40.fullmatch(report.proposed_new_oid):
        issues.append("reference_update_execution_report_new_oid_invalid")
    if (
        report.execution_started_at_epoch_seconds < 0
        or report.execution_completed_at_epoch_seconds
        < report.execution_started_at_epoch_seconds
    ):
        issues.append("reference_update_execution_report_time_invalid")
    if report.report_digest != repository_reference_update_execution_report_digest(
        report
    ):
        issues.append("reference_update_execution_report_digest_mismatch")
    return tuple(issues)


def build_repository_post_reference_observation(
    observation_id: str,
    observer_id: str,
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    final_reference_state: RepositoryReferenceState,
    *,
    observed_at_epoch_seconds: int,
) -> RepositoryPostReferenceObservation:
    observation = RepositoryPostReferenceObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        transaction_id=atomic_update_result.transaction_id,
        repository_id=final_reference_state.repository_id,
        git_dir_fingerprint=final_reference_state.git_dir_fingerprint,
        target_reference=final_reference_state.target_reference,
        observed_oid=final_reference_state.current_oid,
        direct=final_reference_state.direct,
        symbolic=final_reference_state.symbolic,
        reference_store_read=final_reference_state.reference_store_source,
        working_tree_read=final_reference_state.working_tree_source,
        sequence_number=final_reference_state.sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        receipt_digest="",
    )
    observation = replace(
        observation,
        receipt_digest=repository_post_reference_observation_digest(observation),
    )
    issues = repository_post_reference_observation_issues(observation)
    if issues:
        raise ValueError(f"post_reference_observation_invalid:{issues[0]}")
    return observation


def repository_post_reference_observation_issues(
    observation: RepositoryPostReferenceObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            observation.observation_id,
            observation.observer_id,
            observation.transaction_id,
            observation.repository_id,
            observation.target_reference,
        )
    ):
        issues.append("post_reference_observation_required_field_missing")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("post_reference_observation_git_dir_fingerprint_invalid")
    if not _HEX40.fullmatch(observation.observed_oid):
        issues.append("post_reference_observation_oid_invalid")
    if observation.sequence_number < 0:
        issues.append("post_reference_observation_sequence_negative")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("post_reference_observation_time_negative")
    if observation.receipt_digest != repository_post_reference_observation_digest(
        observation
    ):
        issues.append("post_reference_observation_digest_mismatch")
    return tuple(issues)


def build_repository_reference_nonce_consumption_receipt(
    receipt_id: str,
    observer_id: str,
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    source_nonce_registry: RepositoryReferenceNonceRegistry,
    final_nonce_registry: RepositoryReferenceNonceRegistry,
    *,
    consumed_at_epoch_seconds: int,
) -> RepositoryReferenceNonceConsumptionReceipt:
    receipt = RepositoryReferenceNonceConsumptionReceipt(
        receipt_id=receipt_id,
        observer_id=observer_id,
        transaction_id=atomic_update_result.transaction_id,
        authorization_nonce=atomic_update_result.authorization_nonce,
        authority_id=final_nonce_registry.authority_id,
        source_registry_digest=source_nonce_registry.registry_digest,
        final_registry_digest=final_nonce_registry.registry_digest,
        consumed=(
            atomic_update_result.authorization_nonce
            in final_nonce_registry.consumed_nonces
        ),
        revoked=(
            atomic_update_result.authorization_nonce in final_nonce_registry.revoked_nonces
        ),
        final_sequence_number=final_nonce_registry.sequence_number,
        consumed_at_epoch_seconds=consumed_at_epoch_seconds,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_reference_nonce_consumption_receipt_digest(receipt),
    )
    issues = repository_reference_nonce_consumption_receipt_issues(receipt)
    if issues:
        raise ValueError(f"reference_nonce_consumption_receipt_invalid:{issues[0]}")
    return receipt


def repository_reference_nonce_consumption_receipt_issues(
    receipt: RepositoryReferenceNonceConsumptionReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            receipt.receipt_id,
            receipt.observer_id,
            receipt.transaction_id,
            receipt.authorization_nonce,
            receipt.authority_id,
        )
    ):
        issues.append("reference_nonce_consumption_required_field_missing")
    for digest in (receipt.source_registry_digest, receipt.final_registry_digest):
        if not _HEX64.fullmatch(digest):
            issues.append("reference_nonce_consumption_registry_digest_invalid")
            break
    if receipt.final_sequence_number < 0:
        issues.append("reference_nonce_consumption_sequence_negative")
    if receipt.consumed_at_epoch_seconds < 0:
        issues.append("reference_nonce_consumption_time_negative")
    if receipt.receipt_digest != repository_reference_nonce_consumption_receipt_digest(
        receipt
    ):
        issues.append("reference_nonce_consumption_digest_mismatch")
    return tuple(issues)


def _atomic_update_issues(
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    final_reference_state: RepositoryReferenceState,
    final_nonce_registry: RepositoryReferenceNonceRegistry,
    atomic_update_inputs: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        return repository_atomic_reference_update_result_issues(
            atomic_update_result,
            final_reference_state,
            final_nonce_registry,
            **dict(atomic_update_inputs),
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("atomic_reference_update_inputs_invalid",)


def _construct_repository_reference_update_receipt(
    receipt_id: str,
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    final_reference_state: RepositoryReferenceState,
    final_nonce_registry: RepositoryReferenceNonceRegistry,
    atomic_update_inputs: Mapping[str, Any],
    policy: RepositoryReferenceUpdateReceiptPolicy,
    execution_report: RepositoryReferenceUpdateExecutionReport,
    post_reference_observation: RepositoryPostReferenceObservation,
    nonce_consumption_receipt: RepositoryReferenceNonceConsumptionReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryReferenceUpdateReceipt:
    source_reference_state = atomic_update_inputs.get("source_reference_state")
    source_nonce_registry = atomic_update_inputs.get("source_nonce_registry")
    atomic_issues = _atomic_update_issues(
        atomic_update_result,
        final_reference_state,
        final_nonce_registry,
        atomic_update_inputs,
    )
    atomic_update_result_valid = not atomic_issues
    atomic_update_committed = bool(
        atomic_update_result_valid
        and atomic_update_result.status == REFERENCE_UPDATE_COMMITTED
        and atomic_update_result.reference_update_transition_committed
        and atomic_update_result.atomic_reference_nonce_transition
        and atomic_update_result.compare_and_swap_succeeded
        and atomic_update_result.nonce_consumed
    )
    atomic_update_binding_exact = bool(
        source_reference_state is not None
        and source_nonce_registry is not None
        and atomic_update_result.source_reference_state_digest
        == source_reference_state.state_digest
        and atomic_update_result.source_nonce_registry_digest
        == source_nonce_registry.registry_digest
        and atomic_update_result.final_reference_state_digest
        == final_reference_state.state_digest
        and atomic_update_result.final_nonce_registry_digest
        == final_nonce_registry.registry_digest
        and final_reference_state.repository_id == atomic_update_result.repository_id
        and final_reference_state.git_dir_fingerprint
        == atomic_update_result.git_dir_fingerprint
        and final_reference_state.target_reference
        == atomic_update_result.target_reference
        and final_reference_state.current_oid == atomic_update_result.proposed_new_oid
        and atomic_update_result.authorization_nonce
        in final_nonce_registry.consumed_nonces
    )
    receipt_policy_valid = not repository_reference_update_receipt_policy_issues(
        policy
    )
    execution_report_valid = not repository_reference_update_execution_report_issues(
        execution_report
    )
    execution_report_binding_exact = bool(
        execution_report.atomic_update_result_digest
        == atomic_update_result.result_digest
        and execution_report.transaction_id == atomic_update_result.transaction_id
        and execution_report.repository_id == atomic_update_result.repository_id
        and execution_report.git_dir_fingerprint
        == atomic_update_result.git_dir_fingerprint
        and execution_report.target_reference == atomic_update_result.target_reference
        and execution_report.expected_old_oid == atomic_update_result.expected_old_oid
        and execution_report.proposed_new_oid == atomic_update_result.proposed_new_oid
        and execution_report.authorization_nonce
        == atomic_update_result.authorization_nonce
        and execution_report.executor_id == atomic_update_result.executor_id
    )
    report_age = (
        evaluated_at_epoch_seconds
        - execution_report.execution_completed_at_epoch_seconds
    )
    execution_report_fresh = bool(
        0 <= report_age <= policy.max_execution_report_age_seconds
    )
    execution_timing_exact = bool(
        execution_report.execution_started_at_epoch_seconds
        == atomic_update_result.execution_started_at_epoch_seconds
        and execution_report.execution_completed_at_epoch_seconds
        == atomic_update_result.execution_completed_at_epoch_seconds
    )

    post_reference_observation_valid = not repository_post_reference_observation_issues(
        post_reference_observation
    )
    post_reference_observation_binding_exact = bool(
        post_reference_observation.transaction_id
        == atomic_update_result.transaction_id
        and post_reference_observation.repository_id
        == atomic_update_result.repository_id
        and post_reference_observation.git_dir_fingerprint
        == atomic_update_result.git_dir_fingerprint
        and post_reference_observation.target_reference
        == atomic_update_result.target_reference
    )
    observation_age = (
        evaluated_at_epoch_seconds
        - post_reference_observation.observed_at_epoch_seconds
    )
    post_reference_observation_fresh = bool(
        0
        <= observation_age
        <= policy.max_post_reference_observation_age_seconds
    )
    post_reference_direct = post_reference_observation.direct
    post_reference_not_symbolic = not post_reference_observation.symbolic
    post_reference_store_source = bool(
        post_reference_observation.reference_store_read
        and policy.require_reference_store_source
    )
    post_reference_working_tree_ignored = bool(
        not post_reference_observation.working_tree_read
        and policy.require_working_tree_ignored
    )
    post_reference_oid_exact = bool(
        post_reference_observation.observed_oid
        == atomic_update_result.proposed_new_oid
        == final_reference_state.current_oid
    )
    post_reference_sequence_exact = (
        post_reference_observation.sequence_number
        == final_reference_state.sequence_number
    )

    nonce_consumption_receipt_valid = not (
        repository_reference_nonce_consumption_receipt_issues(
            nonce_consumption_receipt
        )
    )
    nonce_consumption_receipt_binding_exact = bool(
        source_nonce_registry is not None
        and nonce_consumption_receipt.transaction_id
        == atomic_update_result.transaction_id
        and nonce_consumption_receipt.authorization_nonce
        == atomic_update_result.authorization_nonce
        and nonce_consumption_receipt.authority_id
        == final_nonce_registry.authority_id
        and nonce_consumption_receipt.source_registry_digest
        == source_nonce_registry.registry_digest
        and nonce_consumption_receipt.final_registry_digest
        == final_nonce_registry.registry_digest
        and nonce_consumption_receipt.final_sequence_number
        == final_nonce_registry.sequence_number
    )
    nonce_receipt_age = (
        evaluated_at_epoch_seconds
        - nonce_consumption_receipt.consumed_at_epoch_seconds
    )
    nonce_consumption_receipt_fresh = bool(
        0
        <= nonce_receipt_age
        <= policy.max_nonce_consumption_receipt_age_seconds
    )
    nonce_registry_transition_exact = bool(
        source_nonce_registry is not None
        and final_nonce_registry.sequence_number
        == source_nonce_registry.sequence_number + 1
        and final_nonce_registry.upstream_snapshot_digest
        == source_nonce_registry.registry_digest
        and atomic_update_result.authorization_nonce
        not in source_nonce_registry.consumed_nonces
        and atomic_update_result.authorization_nonce
        in final_nonce_registry.consumed_nonces
    )
    nonce_consumption_confirmed = bool(
        nonce_consumption_receipt.consumed
        and atomic_update_result.authorization_nonce
        in final_nonce_registry.consumed_nonces
    )
    nonce_not_revoked = bool(
        not nonce_consumption_receipt.revoked
        and atomic_update_result.authorization_nonce
        not in final_nonce_registry.revoked_nonces
    )
    observer_authorized = bool(
        post_reference_observation.observer_id
        == nonce_consumption_receipt.observer_id
        and post_reference_observation.observer_id
        in policy.authorized_observer_ids
    )
    transaction_binding_exact = bool(
        policy.require_exact_transaction_binding
        and execution_report.transaction_id
        == post_reference_observation.transaction_id
        == nonce_consumption_receipt.transaction_id
        == atomic_update_result.transaction_id
    )
    no_future_evidence = all(
        value <= evaluated_at_epoch_seconds
        for value in (
            execution_report.execution_started_at_epoch_seconds,
            execution_report.execution_completed_at_epoch_seconds,
            post_reference_observation.observed_at_epoch_seconds,
            nonce_consumption_receipt.consumed_at_epoch_seconds,
        )
    )
    evidence_after_execution = bool(
        execution_report.execution_completed_at_epoch_seconds
        <= post_reference_observation.observed_at_epoch_seconds
        and execution_report.execution_completed_at_epoch_seconds
        <= nonce_consumption_receipt.consumed_at_epoch_seconds
    )
    forbidden_execution_effects = (
        execution_report.force_update_performed,
        execution_report.reference_delete_performed,
        execution_report.head_updated,
        execution_report.tag_updated,
        execution_report.remote_reference_updated,
        execution_report.push_performed,
        execution_report.index_write_performed,
        execution_report.working_tree_write_performed,
        execution_report.object_database_write_performed,
        execution_report.signing_performed,
        policy.allow_force_update,
        policy.allow_reference_delete,
        policy.allow_push,
    )
    no_forbidden_execution_effect = not any(forbidden_execution_effects)
    atomic_reference_nonce_transition_confirmed = bool(
        atomic_update_result.atomic_reference_nonce_transition
        and execution_report.reference_update_performed
        and execution_report.nonce_consumed
        and post_reference_oid_exact
        and nonce_consumption_confirmed
        and nonce_registry_transition_exact
        and policy.require_atomic_reference_nonce_transition
    )
    reference_update_confirmed = bool(
        execution_report.reference_update_attempted
        and execution_report.reference_update_performed
        and execution_report.compare_and_swap_succeeded
        and execution_report.branch_updated
        and post_reference_oid_exact
    )

    committed_inputs = (
        atomic_update_result_valid,
        atomic_update_committed,
        atomic_update_binding_exact,
        receipt_policy_valid,
        execution_report_valid,
        execution_report_binding_exact,
        execution_report_fresh,
        execution_timing_exact,
        execution_report.reference_update_attempted,
        execution_report.reference_update_performed,
        execution_report.compare_and_swap_succeeded,
        execution_report.branch_updated,
        execution_report.nonce_consumed,
        post_reference_observation_valid,
        post_reference_observation_binding_exact,
        post_reference_observation_fresh,
        post_reference_direct,
        post_reference_not_symbolic,
        post_reference_store_source,
        post_reference_working_tree_ignored,
        post_reference_oid_exact,
        post_reference_sequence_exact,
        nonce_consumption_receipt_valid,
        nonce_consumption_receipt_binding_exact,
        nonce_consumption_receipt_fresh,
        nonce_registry_transition_exact,
        nonce_consumption_confirmed,
        nonce_not_revoked,
        observer_authorized,
        transaction_binding_exact,
        no_future_evidence,
        evidence_after_execution,
        no_forbidden_execution_effect,
        atomic_reference_nonce_transition_confirmed,
        reference_update_confirmed,
    )
    committed = all(committed_inputs)
    receipt = RepositoryReferenceUpdateReceipt(
        receipt_id=receipt_id,
        status=RECEIPT_COMMITTED if committed else RECEIPT_REJECTED,
        atomic_update_result_digest=atomic_update_result.result_digest,
        receipt_policy_digest=policy.policy_digest,
        execution_report_digest=execution_report.report_digest,
        post_reference_observation_digest=post_reference_observation.receipt_digest,
        nonce_consumption_receipt_digest=nonce_consumption_receipt.receipt_digest,
        repository_id=atomic_update_result.repository_id,
        git_dir_fingerprint=atomic_update_result.git_dir_fingerprint,
        target_reference=atomic_update_result.target_reference,
        expected_old_oid=atomic_update_result.expected_old_oid,
        proposed_new_oid=atomic_update_result.proposed_new_oid,
        authorization_nonce=atomic_update_result.authorization_nonce,
        transaction_id=atomic_update_result.transaction_id,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        atomic_update_result_valid=atomic_update_result_valid,
        atomic_update_committed=atomic_update_committed,
        atomic_update_binding_exact=atomic_update_binding_exact,
        receipt_policy_valid=receipt_policy_valid,
        execution_report_valid=execution_report_valid,
        execution_report_binding_exact=execution_report_binding_exact,
        execution_report_fresh=execution_report_fresh,
        execution_timing_exact=execution_timing_exact,
        reference_update_attempted=execution_report.reference_update_attempted,
        reference_update_performed=execution_report.reference_update_performed,
        compare_and_swap_succeeded=execution_report.compare_and_swap_succeeded,
        branch_updated=execution_report.branch_updated,
        execution_nonce_consumed=execution_report.nonce_consumed,
        post_reference_observation_valid=post_reference_observation_valid,
        post_reference_observation_binding_exact=(
            post_reference_observation_binding_exact
        ),
        post_reference_observation_fresh=post_reference_observation_fresh,
        post_reference_direct=post_reference_direct,
        post_reference_not_symbolic=post_reference_not_symbolic,
        post_reference_store_source=post_reference_store_source,
        post_reference_working_tree_ignored=(
            post_reference_working_tree_ignored
        ),
        post_reference_oid_exact=post_reference_oid_exact,
        post_reference_sequence_exact=post_reference_sequence_exact,
        nonce_consumption_receipt_valid=nonce_consumption_receipt_valid,
        nonce_consumption_receipt_binding_exact=(
            nonce_consumption_receipt_binding_exact
        ),
        nonce_consumption_receipt_fresh=nonce_consumption_receipt_fresh,
        nonce_registry_transition_exact=nonce_registry_transition_exact,
        nonce_consumption_confirmed=nonce_consumption_confirmed,
        nonce_not_revoked=nonce_not_revoked,
        observer_authorized=observer_authorized,
        transaction_binding_exact=transaction_binding_exact,
        no_future_evidence=no_future_evidence and evidence_after_execution,
        no_forbidden_execution_effect=no_forbidden_execution_effect,
        atomic_reference_nonce_transition_confirmed=(
            atomic_reference_nonce_transition_confirmed
        ),
        reference_update_confirmed=reference_update_confirmed,
        receipt_committed=committed,
        force_update_confirmed=False,
        reference_delete_confirmed=False,
        head_update_confirmed=False,
        tag_update_confirmed=False,
        remote_reference_update_confirmed=False,
        push_confirmed=False,
        index_write_confirmed=False,
        working_tree_write_confirmed=False,
        object_database_write_confirmed=False,
        signing_confirmed=False,
        receipt_performed_reference_mutation=False,
        receipt_performed_nonce_consumption=False,
        receipt_performed_push=False,
        receipt_digest="",
    )
    return replace(
        receipt,
        receipt_digest=repository_reference_update_receipt_digest(receipt),
    )


def certify_repository_reference_update_receipt(
    receipt_id: str,
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    final_reference_state: RepositoryReferenceState,
    final_nonce_registry: RepositoryReferenceNonceRegistry,
    atomic_update_inputs: Mapping[str, Any],
    policy: RepositoryReferenceUpdateReceiptPolicy,
    execution_report: RepositoryReferenceUpdateExecutionReport,
    post_reference_observation: RepositoryPostReferenceObservation,
    nonce_consumption_receipt: RepositoryReferenceNonceConsumptionReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryReferenceUpdateReceipt:
    if not receipt_id:
        raise ValueError("reference_update_receipt_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("reference_update_receipt_evaluated_at_negative")
    atomic_issues = _atomic_update_issues(
        atomic_update_result,
        final_reference_state,
        final_nonce_registry,
        atomic_update_inputs,
    )
    if atomic_issues:
        raise ValueError(f"atomic_reference_update_invalid:{atomic_issues[0]}")
    for issues, prefix in (
        (
            repository_reference_update_receipt_policy_issues(policy),
            "reference_update_receipt_policy_invalid",
        ),
        (
            repository_reference_update_execution_report_issues(execution_report),
            "reference_update_execution_report_invalid",
        ),
        (
            repository_post_reference_observation_issues(
                post_reference_observation
            ),
            "post_reference_observation_invalid",
        ),
        (
            repository_reference_nonce_consumption_receipt_issues(
                nonce_consumption_receipt
            ),
            "reference_nonce_consumption_receipt_invalid",
        ),
        (repository_reference_state_issues(final_reference_state), "final_reference_state_invalid"),
        (
            repository_reference_nonce_registry_issues(final_nonce_registry),
            "final_nonce_registry_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    receipt = _construct_repository_reference_update_receipt(
        receipt_id,
        atomic_update_result,
        final_reference_state,
        final_nonce_registry,
        atomic_update_inputs,
        policy,
        execution_report,
        post_reference_observation,
        nonce_consumption_receipt,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_reference_update_receipt_issues(
        receipt,
        atomic_update_result,
        final_reference_state,
        final_nonce_registry,
        atomic_update_inputs,
        policy,
        execution_report,
        post_reference_observation,
        nonce_consumption_receipt,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"reference_update_receipt_invalid:{issues[0]}")
    return receipt


def repository_reference_update_receipt_issues(
    receipt: RepositoryReferenceUpdateReceipt,
    atomic_update_result: RepositoryAtomicReferenceUpdateResult,
    final_reference_state: RepositoryReferenceState,
    final_nonce_registry: RepositoryReferenceNonceRegistry,
    atomic_update_inputs: Mapping[str, Any],
    policy: RepositoryReferenceUpdateReceiptPolicy,
    execution_report: RepositoryReferenceUpdateExecutionReport,
    post_reference_observation: RepositoryPostReferenceObservation,
    nonce_consumption_receipt: RepositoryReferenceNonceConsumptionReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if _atomic_update_issues(
        atomic_update_result,
        final_reference_state,
        final_nonce_registry,
        atomic_update_inputs,
    ):
        issues.append("atomic_reference_update_invalid")
        return tuple(issues)
    for validator, name in (
        (repository_reference_update_receipt_policy_issues(policy), "policy_invalid"),
        (
            repository_reference_update_execution_report_issues(execution_report),
            "execution_report_invalid",
        ),
        (
            repository_post_reference_observation_issues(
                post_reference_observation
            ),
            "post_reference_observation_invalid",
        ),
        (
            repository_reference_nonce_consumption_receipt_issues(
                nonce_consumption_receipt
            ),
            "nonce_consumption_receipt_invalid",
        ),
    ):
        if validator:
            issues.append(name)
            return tuple(issues)
    expected = _construct_repository_reference_update_receipt(
        receipt.receipt_id,
        atomic_update_result,
        final_reference_state,
        final_nonce_registry,
        atomic_update_inputs,
        policy,
        execution_report,
        post_reference_observation,
        nonce_consumption_receipt,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if receipt.to_dict() != expected.to_dict():
        issues.append("reference_update_receipt_recomputation_mismatch")
    if receipt.status not in (RECEIPT_COMMITTED, RECEIPT_REJECTED):
        issues.append("reference_update_receipt_status_invalid")
    forbidden_receipt_claims = (
        receipt.force_update_confirmed,
        receipt.reference_delete_confirmed,
        receipt.head_update_confirmed,
        receipt.tag_update_confirmed,
        receipt.remote_reference_update_confirmed,
        receipt.push_confirmed,
        receipt.index_write_confirmed,
        receipt.working_tree_write_confirmed,
        receipt.object_database_write_confirmed,
        receipt.signing_confirmed,
        receipt.receipt_performed_reference_mutation,
        receipt.receipt_performed_nonce_consumption,
        receipt.receipt_performed_push,
    )
    if any(forbidden_receipt_claims):
        issues.append("reference_update_receipt_forbidden_effect")
    if receipt.status == RECEIPT_COMMITTED:
        required_true = (
            receipt.atomic_update_result_valid,
            receipt.atomic_update_committed,
            receipt.atomic_update_binding_exact,
            receipt.receipt_policy_valid,
            receipt.execution_report_valid,
            receipt.execution_report_binding_exact,
            receipt.execution_report_fresh,
            receipt.execution_timing_exact,
            receipt.reference_update_attempted,
            receipt.reference_update_performed,
            receipt.compare_and_swap_succeeded,
            receipt.branch_updated,
            receipt.execution_nonce_consumed,
            receipt.post_reference_observation_valid,
            receipt.post_reference_observation_binding_exact,
            receipt.post_reference_observation_fresh,
            receipt.post_reference_direct,
            receipt.post_reference_not_symbolic,
            receipt.post_reference_store_source,
            receipt.post_reference_working_tree_ignored,
            receipt.post_reference_oid_exact,
            receipt.post_reference_sequence_exact,
            receipt.nonce_consumption_receipt_valid,
            receipt.nonce_consumption_receipt_binding_exact,
            receipt.nonce_consumption_receipt_fresh,
            receipt.nonce_registry_transition_exact,
            receipt.nonce_consumption_confirmed,
            receipt.nonce_not_revoked,
            receipt.observer_authorized,
            receipt.transaction_binding_exact,
            receipt.no_future_evidence,
            receipt.no_forbidden_execution_effect,
            receipt.atomic_reference_nonce_transition_confirmed,
            receipt.reference_update_confirmed,
            receipt.receipt_committed,
        )
        if not all(required_true):
            issues.append("reference_update_receipt_committed_invariant_false")
    else:
        if receipt.receipt_committed:
            issues.append("reference_update_receipt_rejected_marked_committed")
    if receipt.receipt_digest != repository_reference_update_receipt_digest(receipt):
        issues.append("reference_update_receipt_digest_mismatch")
    return tuple(issues)
