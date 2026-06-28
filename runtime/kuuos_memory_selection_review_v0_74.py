#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_memory_review_identity_v0_74 import MemoryReviewerIdentity
from runtime.kuuos_memory_review_receipt_v0_74 import (
    ALLOWED_DECISIONS,
    APPROVE_MEMORY_SELECTION,
    REJECT_MEMORY_SELECTION,
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_review_request_v0_74 import (
    MemoryReviewRequest,
    memory_review_request_digest,
)
from runtime.kuuos_memory_selection_reviewability_v0_74 import selection_review_issues
from runtime.kuuos_memory_selection_v0_73 import (
    MemorySelectionRecord,
    selection_record_digest,
)

REVIEW_APPROVED = "MEMORY_SELECTION_REVIEW_APPROVED"
REVIEW_REJECTED = "MEMORY_SELECTION_REVIEW_REJECTED"
REVIEW_REEVALUATION_REQUESTED = "MEMORY_SELECTION_REEVALUATION_REQUESTED"
REVIEW_BLOCKED = "MEMORY_SELECTION_REVIEW_BLOCKED"


def review_memory_selection(
    request: MemoryReviewRequest,
    selection: MemorySelectionRecord,
    reviewer: MemoryReviewerIdentity,
    decision: str,
    decided_at_epoch: int,
) -> MemoryReviewReceipt:
    issues = list(selection_review_issues(selection))
    if request.request_digest != memory_review_request_digest(request):
        issues.append("memory_review_request_digest_mismatch")
    if selection.record_digest != selection_record_digest(selection):
        issues.append("memory_selection_record_digest_mismatch")
    if request.selection_record_digest != selection.record_digest:
        issues.append("memory_review_selection_record_binding_mismatch")

    bindings = (
        (request.source_history_digest, selection.source_history_digest, "source_history"),
        (request.source_kernel_digest, selection.source_kernel_digest, "source_kernel"),
        (request.family_digest, selection.family_digest, "family"),
        (request.selected_member_digest, selection.selected_member_digest, "selected_member"),
        (
            request.selected_deformation_digest,
            selection.selected_deformation_digest,
            "selected_deformation",
        ),
        (request.selected_kernel_digest, selection.selected_kernel_digest, "selected_kernel"),
        (
            request.selected_connection_digest,
            selection.selected_connection_digest,
            "selected_connection",
        ),
    )
    for requested, recorded, label in bindings:
        if requested != recorded:
            issues.append(f"memory_review_{label}_binding_mismatch")

    if request.rollback_target_digest != selection.source_kernel_digest:
        issues.append("memory_review_rollback_target_mismatch")
    if reviewer.reviewer_class not in request.allowed_reviewer_classes:
        issues.append("memory_review_reviewer_scope_mismatch")
    if decision not in ALLOWED_DECISIONS:
        issues.append("memory_review_decision_invalid")
    if not request.valid_from_epoch <= decided_at_epoch <= request.valid_until_epoch:
        issues.append("memory_review_outside_validity_window")
    issues = list(dict.fromkeys(issues))

    authority = not issues and decision == APPROVE_MEMORY_SELECTION
    if issues:
        status = REVIEW_BLOCKED
    elif decision == APPROVE_MEMORY_SELECTION:
        status = REVIEW_APPROVED
    elif decision == REJECT_MEMORY_SELECTION:
        status = REVIEW_REJECTED
    else:
        status = REVIEW_REEVALUATION_REQUESTED

    receipt = MemoryReviewReceipt(
        status,
        decision,
        request.request_digest,
        selection.record_digest,
        reviewer.reviewer_id,
        reviewer.reviewer_class,
        selection.source_history_digest,
        selection.source_kernel_digest,
        selection.family_digest,
        selection.selected_member_digest,
        selection.selected_deformation_digest,
        selection.selected_kernel_digest,
        selection.selected_connection_digest,
        request.rollback_target_digest,
        request.valid_from_epoch,
        request.valid_until_epoch,
        decided_at_epoch,
        authority,
        False,
        False,
        False,
        False,
        tuple(issues),
        "",
    )
    return replace(receipt, receipt_digest=memory_review_receipt_digest(receipt))
