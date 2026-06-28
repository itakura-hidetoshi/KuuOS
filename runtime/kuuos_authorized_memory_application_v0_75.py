#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_memory_application_receipt_v0_75 import (
    APPLICATION_BLOCKED,
    APPLICATION_COMMITTED,
    MemoryApplicationReceipt,
    memory_application_receipt_digest,
)
from runtime.kuuos_memory_application_request_v0_75 import (
    MemoryApplicationRequest,
    memory_application_request_digest,
)
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import REVIEW_APPROVED
from runtime.kuuos_nonmarkov_memory_connection_v0_72 import NonMarkovMemoryConnection
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState


def apply_approved_memory_selection(
    state: ProductionMemoryState,
    request: MemoryApplicationRequest,
    review: MemoryReviewReceipt,
    selected_connection: NonMarkovMemoryConnection,
) -> tuple[ProductionMemoryState, MemoryApplicationReceipt]:
    issues: list[str] = []
    before_digest = state.digest
    if request.request_digest != memory_application_request_digest(request):
        issues.append("memory_application_request_digest_mismatch")
    if review.receipt_digest != memory_review_receipt_digest(review):
        issues.append("memory_application_review_receipt_digest_mismatch")
    if request.review_receipt_digest != review.receipt_digest:
        issues.append("memory_application_review_binding_mismatch")
    if review.status != REVIEW_APPROVED:
        issues.append("memory_application_review_not_approved")
    if review.decision != APPROVE_MEMORY_SELECTION:
        issues.append("memory_application_decision_not_approval")
    if not review.production_application_authority:
        issues.append("memory_application_authority_missing")
    if review.writes_enabled or review.live_application_enabled:
        issues.append("memory_application_review_boundary_invalid")
    if review.permission_expansion_enabled:
        issues.append("memory_application_permission_expansion_requested")
    if review.rollback_target_replacement_enabled:
        issues.append("memory_application_rollback_replacement_requested")
    if not review.valid_from_epoch <= request.apply_epoch <= review.valid_until_epoch:
        issues.append("memory_application_outside_validity_window")
    if request.apply_epoch < review.decided_at_epoch:
        issues.append("memory_application_precedes_review")

    if request.target_state_id != state.state_id:
        issues.append("memory_application_state_id_mismatch")
    if request.expected_state_digest != before_digest:
        issues.append("memory_application_state_digest_mismatch")
    if request.expected_revision != state.revision:
        issues.append("memory_application_revision_mismatch")
    if review.receipt_digest in state.consumed_review_receipts:
        issues.append("memory_application_review_already_consumed")

    source_digest = state.current_kernel.digest
    source_bindings = (
        (request.source_kernel_digest, source_digest, "request_source_kernel"),
        (review.source_kernel_digest, source_digest, "review_source_kernel"),
        (request.rollback_target_digest, source_digest, "request_rollback_target"),
        (review.rollback_target_digest, source_digest, "review_rollback_target"),
    )
    for declared, actual, label in source_bindings:
        if declared != actual:
            issues.append(f"memory_application_{label}_mismatch")

    selected_kernel_digest = selected_connection.memory_kernel.digest
    selected_connection_digest = selected_connection.digest
    selected_bindings = (
        (request.selected_kernel_digest, selected_kernel_digest, "request_selected_kernel"),
        (review.selected_kernel_digest, selected_kernel_digest, "review_selected_kernel"),
        (
            request.selected_connection_digest,
            selected_connection_digest,
            "request_selected_connection",
        ),
        (
            review.selected_connection_digest,
            selected_connection_digest,
            "review_selected_connection",
        ),
    )
    for declared, actual, label in selected_bindings:
        if declared != actual:
            issues.append(f"memory_application_{label}_mismatch")

    if selected_connection.memory_kernel.source_history_digest != state.history_digest:
        issues.append("memory_application_history_binding_mismatch")
    if selected_connection.memory_kernel.source_module_digest != state.module_digest:
        issues.append("memory_application_module_binding_mismatch")
    if (
        selected_connection.base_connection.digest
        != state.current_connection.base_connection.digest
    ):
        issues.append("memory_application_base_connection_mismatch")
    issues = list(dict.fromkeys(issues))

    if issues:
        receipt = MemoryApplicationReceipt(
            APPLICATION_BLOCKED,
            request.request_digest,
            review.receipt_digest,
            state.state_id,
            before_digest,
            before_digest,
            state.revision,
            state.revision,
            source_digest,
            selected_kernel_digest,
            selected_connection_digest,
            state.current_kernel.digest,
            request.apply_epoch,
            False,
            False,
            False,
            False,
            False,
            False,
            tuple(issues),
            "",
        )
        return state, replace(
            receipt,
            receipt_digest=memory_application_receipt_digest(receipt),
        )

    updated = ProductionMemoryState(
        state.state_id,
        state.revision + 1,
        state.history_digest,
        state.module_digest,
        selected_connection.memory_kernel,
        selected_connection,
        state.consumed_review_receipts + (review.receipt_digest,),
        before_digest,
    )
    receipt = MemoryApplicationReceipt(
        APPLICATION_COMMITTED,
        request.request_digest,
        review.receipt_digest,
        state.state_id,
        before_digest,
        updated.digest,
        state.revision,
        updated.revision,
        source_digest,
        selected_kernel_digest,
        selected_connection_digest,
        source_digest,
        request.apply_epoch,
        True,
        True,
        True,
        True,
        False,
        False,
        (),
        "",
    )
    return updated, replace(
        receipt,
        receipt_digest=memory_application_receipt_digest(receipt),
    )
