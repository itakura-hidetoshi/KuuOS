#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    DISCREPANCY_EVIDENCE_INVALID,
    DISCREPANCY_LOST,
    DISCREPANCY_NONE,
    DISCREPANCY_OTHER,
    DISCREPANCY_SUBSTITUTED,
    REVIEW_AUTOMATIC_REPAIR_ELIGIBLE,
    REVIEW_CLEAN,
    REVIEW_REJECTED,
    REVIEW_REQUIRED,
    repository_checkpoint_review_record_digest,
)
from runtime.v106_review_core import construct_repository_checkpoint_review_record


def construct_bounded_checkpoint_review_record(
    review_id,
    stability_certificate,
    v105_context,
    policy,
    observation,
    *,
    evaluated_at_epoch_seconds: int,
):
    record = construct_repository_checkpoint_review_record(
        review_id,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    checks = dict(record.checks)
    if record.discrepancy_kind == DISCREPANCY_SUBSTITUTED:
        record = replace(
            record,
            status=REVIEW_REQUIRED,
            automatic_repair_eligible=False,
            human_review_required=True,
        )
        checks["automatic_local_repair_eligible"] = False
        checks["human_review_required"] = True
        checks["existing_nonzero_oid_replacement_requires_human_review"] = True
    else:
        checks["existing_nonzero_oid_replacement_requires_human_review"] = False
    record = replace(record, checks=checks, record_digest="")
    return replace(
        record,
        record_digest=repository_checkpoint_review_record_digest(record),
    )


def review_repository_checkpoint_discrepancy(
    review_id,
    stability_certificate,
    v105_context,
    policy,
    observation,
    *,
    evaluated_at_epoch_seconds: int,
):
    if not review_id:
        raise ValueError("checkpoint_review_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("checkpoint_review_evaluation_time_negative")
    record = construct_bounded_checkpoint_review_record(
        review_id,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_review_record_issues(
        record,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_review_record_invalid:{issues[0]}")
    return record


def repository_checkpoint_review_record_issues(
    record,
    stability_certificate,
    v105_context,
    policy,
    observation,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_bounded_checkpoint_review_record(
        record.review_id,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("checkpoint_review_recomputation_mismatch")
    if record.status not in (
        REVIEW_CLEAN,
        REVIEW_AUTOMATIC_REPAIR_ELIGIBLE,
        REVIEW_REQUIRED,
        REVIEW_REJECTED,
    ):
        issues.append("checkpoint_review_status_invalid")
    if record.discrepancy_kind not in (
        DISCREPANCY_NONE,
        DISCREPANCY_LOST,
        DISCREPANCY_SUBSTITUTED,
        DISCREPANCY_OTHER,
        DISCREPANCY_EVIDENCE_INVALID,
    ):
        issues.append("checkpoint_review_discrepancy_invalid")
    if record.automatic_repair_eligible != (
        record.status == REVIEW_AUTOMATIC_REPAIR_ELIGIBLE
    ):
        issues.append("checkpoint_review_automatic_boundary_mismatch")
    if record.human_review_required != (record.status == REVIEW_REQUIRED):
        issues.append("checkpoint_review_human_boundary_mismatch")
    if record.automatic_repair_eligible and record.human_review_required:
        issues.append("checkpoint_review_boundary_overlap")
    if record.status == REVIEW_REQUIRED and (
        record.discrepancy_kind != DISCREPANCY_SUBSTITUTED
    ):
        issues.append("checkpoint_review_human_scope_too_broad")
    forbidden_claims = (
        "review_granted_repository_change_authority",
        "review_performed_reference_mutation",
        "review_performed_object_write",
        "review_invoked_live_git_command",
        "review_mutated_live_repository",
        "review_consumed_nonce",
    )
    if any(record.checks.get(key, False) for key in forbidden_claims):
        issues.append("checkpoint_review_forbidden_claim")
    if record.record_digest != repository_checkpoint_review_record_digest(record):
        issues.append("checkpoint_review_record_digest_mismatch")
    return tuple(issues)
