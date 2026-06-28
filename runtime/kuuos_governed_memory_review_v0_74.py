#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_memory_review_identity_v0_74 import MemoryReviewerIdentity
from runtime.kuuos_memory_review_receipt_v0_74 import (
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_review_request_v0_74 import (
    MemoryReviewRequest,
    build_memory_review_request,
)
from runtime.kuuos_memory_selection_review_v0_74 import (
    REVIEW_BLOCKED,
    review_memory_selection,
)
from runtime.kuuos_memory_selection_reviewability_v0_74 import selection_review_issues
from runtime.kuuos_memory_selection_v0_73 import MemorySelectionRecord


def build_governed_memory_review_request(
    request_id: str,
    requester_id: str,
    selection: MemorySelectionRecord,
    allowed_reviewer_classes: tuple[str, ...],
    valid_from_epoch: int,
    valid_until_epoch: int,
) -> MemoryReviewRequest:
    issues = selection_review_issues(selection)
    if issues:
        raise ValueError(issues[0])
    return build_memory_review_request(
        request_id,
        requester_id,
        selection,
        allowed_reviewer_classes,
        valid_from_epoch,
        valid_until_epoch,
    )


def review_governed_memory_selection(
    request: MemoryReviewRequest,
    selection: MemorySelectionRecord,
    reviewer: MemoryReviewerIdentity,
    decision: str,
    decided_at_epoch: int,
) -> MemoryReviewReceipt:
    receipt = review_memory_selection(
        request,
        selection,
        reviewer,
        decision,
        decided_at_epoch,
    )
    selection_issues = selection_review_issues(selection)
    if not selection_issues:
        return receipt
    issues = tuple(dict.fromkeys(receipt.issues + selection_issues))
    blocked = replace(
        receipt,
        status=REVIEW_BLOCKED,
        production_application_authority=False,
        issues=issues,
        receipt_digest="",
    )
    return replace(blocked, receipt_digest=memory_review_receipt_digest(blocked))
