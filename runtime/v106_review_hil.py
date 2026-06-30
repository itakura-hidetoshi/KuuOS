#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    DISCREPANCY_LOST,
    DISCREPANCY_SUBSTITUTED,
    REVIEW_REQUIRED,
    repository_checkpoint_review_record_digest,
)

REVIEW_AUTOMATIC = "REPOSITORY_CHECKPOINT_REVIEW_AUTOMATIC"


def human_review_required_for(discrepancy_kind: str) -> bool:
    return discrepancy_kind == DISCREPANCY_SUBSTITUTED


def minimize_human_review(record):
    checks = dict(record.checks)
    automatic_followup = bool(
        record.status == REVIEW_REQUIRED
        and record.discrepancy_kind == DISCREPANCY_LOST
        and record.expected_current_oid == "0" * 40
        and checks.get("target_commit_present", False)
        and checks.get("current_state_recheck_stable", False)
        and checks.get("direct_local_sources_only", False)
    )
    if automatic_followup:
        record = replace(
            record,
            status=REVIEW_AUTOMATIC,
            human_review_required=False,
        )
    checks["automatic_followup_eligible"] = automatic_followup
    checks["human_review_required"] = record.human_review_required
    checks["human_review_limited_to_substitution"] = bool(
        not record.human_review_required
        or record.discrepancy_kind == DISCREPANCY_SUBSTITUTED
    )
    record = replace(record, checks=checks, record_digest="")
    return replace(
        record,
        record_digest=repository_checkpoint_review_record_digest(record),
    )
