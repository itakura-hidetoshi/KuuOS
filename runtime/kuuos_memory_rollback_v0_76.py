#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_memory_application_receipt_v0_75 import (
    APPLICATION_COMMITTED,
    MemoryApplicationReceipt,
    memory_application_receipt_digest,
)
from runtime.kuuos_memory_rollback_ledger_v0_76 import MemoryRollbackLedger
from runtime.kuuos_memory_rollback_receipt_v0_76 import (
    ROLLBACK_BLOCKED,
    ROLLBACK_COMMITTED,
    MemoryRollbackReceipt,
    memory_rollback_receipt_digest,
)
from runtime.kuuos_memory_rollback_request_v0_76 import (
    MemoryRollbackRequest,
    memory_rollback_request_digest,
)
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState


def rollback_memory_commit(
    current_state: ProductionMemoryState,
    rollback_state: ProductionMemoryState,
    ledger: MemoryRollbackLedger,
    request: MemoryRollbackRequest,
    commit_receipt: MemoryApplicationReceipt,
) -> tuple[ProductionMemoryState, MemoryRollbackLedger, MemoryRollbackReceipt]:
    issues: list[str] = []
    current_digest = current_state.digest
    ledger_digest = ledger.digest
    if request.request_digest != memory_rollback_request_digest(request):
        issues.append("memory_rollback_request_digest_mismatch")
    if commit_receipt.receipt_digest != memory_application_receipt_digest(commit_receipt):
        issues.append("memory_rollback_commit_receipt_digest_mismatch")
    if request.commit_receipt_digest != commit_receipt.receipt_digest:
        issues.append("memory_rollback_commit_binding_mismatch")
    if commit_receipt.status != APPLICATION_COMMITTED:
        issues.append("memory_rollback_source_not_committed")
    if not commit_receipt.atomic_commit:
        issues.append("memory_rollback_source_not_atomic")
    if not commit_receipt.state_write_performed or not commit_receipt.live_application_performed:
        issues.append("memory_rollback_source_effect_missing")
    if commit_receipt.permission_expansion_performed:
        issues.append("memory_rollback_source_permission_expansion")
    if commit_receipt.rollback_target_replaced:
        issues.append("memory_rollback_source_target_replaced")

    if request.target_state_id != current_state.state_id:
        issues.append("memory_rollback_state_id_mismatch")
    if request.expected_state_digest != current_digest:
        issues.append("memory_rollback_state_digest_mismatch")
    if request.expected_state_revision != current_state.revision:
        issues.append("memory_rollback_state_revision_mismatch")
    if commit_receipt.after_state_digest != current_digest:
        issues.append("memory_rollback_commit_after_state_mismatch")
    if commit_receipt.after_revision != current_state.revision:
        issues.append("memory_rollback_commit_after_revision_mismatch")
    if commit_receipt.selected_kernel_digest != current_state.current_kernel.digest:
        issues.append("memory_rollback_current_kernel_mismatch")
    if commit_receipt.selected_connection_digest != current_state.current_connection.digest:
        issues.append("memory_rollback_current_connection_mismatch")

    if request.rollback_state_digest != rollback_state.digest:
        issues.append("memory_rollback_snapshot_digest_mismatch")
    if commit_receipt.before_state_digest != rollback_state.digest:
        issues.append("memory_rollback_commit_before_state_mismatch")
    if current_state.previous_state_digest != rollback_state.digest:
        issues.append("memory_rollback_state_chain_mismatch")
    if commit_receipt.before_revision != rollback_state.revision:
        issues.append("memory_rollback_snapshot_revision_mismatch")
    if request.rollback_kernel_digest != rollback_state.current_kernel.digest:
        issues.append("memory_rollback_kernel_binding_mismatch")
    if request.rollback_connection_digest != rollback_state.current_connection.digest:
        issues.append("memory_rollback_connection_binding_mismatch")
    if commit_receipt.rollback_target_digest != rollback_state.current_kernel.digest:
        issues.append("memory_rollback_target_mismatch")
    if commit_receipt.source_kernel_digest != rollback_state.current_kernel.digest:
        issues.append("memory_rollback_source_kernel_mismatch")
    if rollback_state.state_id != current_state.state_id:
        issues.append("memory_rollback_snapshot_state_id_mismatch")
    if rollback_state.history_digest != current_state.history_digest:
        issues.append("memory_rollback_history_binding_mismatch")
    if rollback_state.module_digest != current_state.module_digest:
        issues.append("memory_rollback_module_binding_mismatch")
    if (
        rollback_state.current_connection.base_connection.digest
        != current_state.current_connection.base_connection.digest
    ):
        issues.append("memory_rollback_base_connection_mismatch")

    if request.expected_ledger_digest != ledger_digest:
        issues.append("memory_rollback_ledger_digest_mismatch")
    if request.expected_ledger_revision != ledger.revision:
        issues.append("memory_rollback_ledger_revision_mismatch")
    if commit_receipt.receipt_digest in ledger.rolled_back_commit_receipts:
        issues.append("memory_rollback_commit_already_rolled_back")
    if request.rollback_epoch < commit_receipt.applied_at_epoch:
        issues.append("memory_rollback_precedes_commit")
    if commit_receipt.review_receipt_digest not in current_state.consumed_review_receipts:
        issues.append("memory_rollback_review_consumption_missing")
    issues = list(dict.fromkeys(issues))

    if issues:
        receipt = MemoryRollbackReceipt(
            ROLLBACK_BLOCKED,
            request.request_digest,
            commit_receipt.receipt_digest,
            current_state.state_id,
            current_digest,
            current_digest,
            current_state.revision,
            current_state.revision,
            ledger_digest,
            ledger_digest,
            ledger.revision,
            ledger.revision,
            rollback_state.current_kernel.digest,
            rollback_state.current_connection.digest,
            request.rollback_epoch,
            False,
            False,
            False,
            False,
            False,
            tuple(issues),
            "",
        )
        return current_state, ledger, replace(
            receipt,
            receipt_digest=memory_rollback_receipt_digest(receipt),
        )

    restored = ProductionMemoryState(
        current_state.state_id,
        current_state.revision + 1,
        current_state.history_digest,
        current_state.module_digest,
        rollback_state.current_kernel,
        rollback_state.current_connection,
        current_state.consumed_review_receipts,
        current_digest,
    )
    updated_ledger = MemoryRollbackLedger(
        ledger.ledger_id,
        ledger.revision + 1,
        ledger.rolled_back_commit_receipts + (commit_receipt.receipt_digest,),
        ledger_digest,
    )
    receipt = MemoryRollbackReceipt(
        ROLLBACK_COMMITTED,
        request.request_digest,
        commit_receipt.receipt_digest,
        current_state.state_id,
        current_digest,
        restored.digest,
        current_state.revision,
        restored.revision,
        ledger_digest,
        updated_ledger.digest,
        ledger.revision,
        updated_ledger.revision,
        restored.current_kernel.digest,
        restored.current_connection.digest,
        request.rollback_epoch,
        True,
        True,
        True,
        False,
        False,
        (),
        "",
    )
    return restored, updated_ledger, replace(
        receipt,
        receipt_digest=memory_rollback_receipt_digest(receipt),
    )
