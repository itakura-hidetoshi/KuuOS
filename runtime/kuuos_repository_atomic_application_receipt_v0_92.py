#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    APPLICATION_ABORTED,
    APPLICATION_APPLIED,
    RepositoryAtomicApplicationReceipt,
    RepositoryNonceConsumptionReceipt,
    repository_atomic_application_receipt_digest,
    repository_nonce_consumption_receipt_digest,
)


def repository_nonce_consumption_receipt_issues(
    receipt: RepositoryNonceConsumptionReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not receipt.transaction_id or not receipt.authorization_nonce:
        issues.append("nonce_consumption_required_field_missing")
    if receipt.application_committed:
        if receipt.consumed_before or not receipt.consumed_after:
            issues.append("nonce_consumption_commit_state_invalid")
        if receipt.registry_before_digest == receipt.registry_after_digest:
            issues.append("nonce_consumption_registry_not_advanced")
    else:
        if receipt.consumed_before != receipt.consumed_after:
            issues.append("nonce_consumption_abort_state_changed")
        if receipt.registry_before_digest != receipt.registry_after_digest:
            issues.append("nonce_consumption_abort_registry_changed")
    if not receipt.atomic_with_application:
        issues.append("nonce_consumption_not_atomic")
    if receipt.receipt_digest != repository_nonce_consumption_receipt_digest(receipt):
        issues.append("nonce_consumption_receipt_digest_mismatch")
    return tuple(issues)


def repository_atomic_application_receipt_issues(
    receipt: RepositoryAtomicApplicationReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if receipt.status not in (APPLICATION_APPLIED, APPLICATION_ABORTED):
        issues.append("atomic_application_status_invalid")
    prerequisites = all((
        receipt.authorization_valid,
        receipt.authorization_scope_bound,
        receipt.authorization_not_expired_at_completion,
        receipt.application_policy_bound,
        receipt.executor_authorized,
        receipt.transaction_time_order_valid,
        receipt.duration_within_policy,
        receipt.patch_bundle_bound,
        receipt.patch_count_within_policy,
        receipt.patch_paths_unique,
        receipt.patch_paths_exact,
        receipt.patch_before_digests_exact,
        receipt.source_commit_unchanged,
        receipt.source_snapshot_unchanged,
        receipt.object_database_source,
        receipt.working_tree_ignored,
        receipt.nonce_registry_bound,
        receipt.nonce_unused_before,
        receipt.nonce_not_revoked,
        receipt.actual_changed_paths_exact,
        receipt.result_snapshot_materialized,
        receipt.result_observation_exact,
        receipt.result_normal_form_certified,
        receipt.rollback_material_exact,
    ))
    if receipt.application_effect_committed != prerequisites:
        issues.append("atomic_application_effect_commit_mismatch")
    if receipt.nonce_consumption_committed != prerequisites:
        issues.append("atomic_application_nonce_commit_mismatch")
    if receipt.status == APPLICATION_APPLIED and not prerequisites:
        issues.append("atomic_application_applied_without_prerequisites")
    if receipt.status == APPLICATION_ABORTED and prerequisites:
        issues.append("atomic_application_aborted_with_prerequisites")
    if not receipt.atomic_state_transition:
        issues.append("atomic_application_state_transition_not_atomic")
    if receipt.status == APPLICATION_ABORTED and not receipt.failure_no_effect:
        issues.append("atomic_application_abort_has_effect")
    if receipt.status == APPLICATION_APPLIED and receipt.failure_no_effect:
        issues.append("atomic_application_success_marked_no_effect")
    if not receipt.isolated_snapshot_only:
        issues.append("atomic_application_not_isolated")
    if receipt.live_repository_write_performed:
        issues.append("atomic_application_live_write_performed")
    if receipt.commit_created:
        issues.append("atomic_application_unexpected_commit")
    if receipt.reference_mutated:
        issues.append("atomic_application_unexpected_reference_mutation")
    if receipt.receipt_digest != repository_atomic_application_receipt_digest(receipt):
        issues.append("atomic_application_receipt_digest_mismatch")
    return tuple(issues)
