#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.v103_evidence_a import (
    RepositoryCheckpointCreationExecutionReport,
    repository_checkpoint_creation_execution_report_digest,
)
from runtime.v103_receipt_policy import (
    RepositoryCheckpointCreationReceiptPolicy,
    repository_checkpoint_creation_receipt_policy_digest,
)

FORBIDDEN_EFFECTS = (
    "checkpoint_overwrite",
    "force_update",
    "reference_delete",
    "branch_update",
    "tag_update",
    "remote_reference_update",
    "push",
    "index_write",
    "working_tree_write",
    "object_database_write",
    "reflog_write",
    "signing",
)


def canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def snapshot_digest(snapshot: Mapping[str, Any]) -> str:
    payload = dict(snapshot)
    payload.pop("snapshot_digest", None)
    return canonical_digest(payload)


def build_receipt_policy(
    policy_id: str,
    *,
    authorized_observer_ids: tuple[str, ...],
    max_report_age_seconds: int,
    max_observation_age_seconds: int,
    max_external_duration_seconds: int,
) -> RepositoryCheckpointCreationReceiptPolicy:
    policy = RepositoryCheckpointCreationReceiptPolicy(
        policy_id=policy_id,
        authorized_observer_ids=canonical_strings(authorized_observer_ids),
        max_report_age_seconds=max_report_age_seconds,
        max_observation_age_seconds=max_observation_age_seconds,
        max_external_duration_seconds=max_external_duration_seconds,
        required_absent_effects=FORBIDDEN_EFFECTS,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_creation_receipt_policy_digest(policy),
    )
    issues = receipt_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_receipt_policy_invalid:{issues[0]}")
    return policy


def receipt_policy_issues(
    policy: RepositoryCheckpointCreationReceiptPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id or not policy.authorized_observer_ids:
        issues.append("policy_required_field_missing")
    if policy.authorized_observer_ids != canonical_strings(policy.authorized_observer_ids):
        issues.append("policy_observers_not_canonical")
    if min(
        policy.max_report_age_seconds,
        policy.max_observation_age_seconds,
        policy.max_external_duration_seconds,
    ) <= 0:
        issues.append("policy_bound_invalid")
    if policy.required_absent_effects != FORBIDDEN_EFFECTS:
        issues.append("policy_forbidden_effect_set_mismatch")
    if policy.policy_digest != repository_checkpoint_creation_receipt_policy_digest(policy):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def build_execution_report(result, **overrides) -> RepositoryCheckpointCreationExecutionReport:
    values = {
        "report_id": "checkpoint-execution-report-v103",
        "transaction_id": result.transaction_id,
        "authorization_certificate_digest": result.authorization_certificate_digest,
        "execution_policy_digest": result.execution_policy_digest,
        "request_digest": result.request_digest,
        "v102_result_digest": result.result_digest,
        "repository_id": result.repository_id,
        "git_dir_fingerprint": result.git_dir_fingerprint,
        "checkpoint_reference": result.checkpoint_reference,
        "expected_old_oid": result.expected_old_oid,
        "proposed_new_oid": result.proposed_new_oid,
        "authorization_nonce": result.authorization_nonce,
        "executor_id": result.executor_id,
        "executor_sequence_number": 1,
        "creation_attempted": result.compare_and_swap_attempted,
        "compare_and_swap_succeeded": result.compare_and_swap_succeeded,
        "checkpoint_created": result.checkpoint_created,
        "nonce_consumed": result.nonce_consumed,
        "aborted_without_mutation": result.status.endswith("ABORTED"),
        "reported_effects": (),
        "execution_started_at_epoch_seconds": result.execution_completed_at_epoch_seconds,
        "execution_completed_at_epoch_seconds": result.execution_completed_at_epoch_seconds + 1,
        "report_digest": "",
    }
    values.update(overrides)
    report = RepositoryCheckpointCreationExecutionReport(**values)
    report = replace(
        report,
        report_digest=repository_checkpoint_creation_execution_report_digest(report),
    )
    issues = execution_report_issues(report)
    if issues:
        raise ValueError(f"checkpoint_execution_report_invalid:{issues[0]}")
    return report


def execution_report_issues(
    report: RepositoryCheckpointCreationExecutionReport,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        report.report_id,
        report.transaction_id,
        report.repository_id,
        report.checkpoint_reference,
        report.authorization_nonce,
        report.executor_id,
    )
    if any(not value for value in required):
        issues.append("report_required_field_missing")
    if report.executor_sequence_number < 0:
        issues.append("report_sequence_negative")
    if report.execution_completed_at_epoch_seconds < report.execution_started_at_epoch_seconds:
        issues.append("report_time_invalid")
    if report.reported_effects != canonical_strings(report.reported_effects):
        issues.append("report_effects_not_canonical")
    if report.report_digest != repository_checkpoint_creation_execution_report_digest(report):
        issues.append("report_digest_mismatch")
    return tuple(issues)
