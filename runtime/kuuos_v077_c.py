#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_memory_application_receipt_v0_75 import MemoryApplicationReceipt
from runtime.kuuos_memory_rollback_ledger_v0_76 import MemoryRollbackLedger
from runtime.kuuos_memory_rollback_receipt_v0_76 import MemoryRollbackReceipt
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState


@dataclass(frozen=True)
class RollbackBindings:
    exact_state: bool
    exact_payload: bool
    revision_successor: bool
    state_chain: bool
    authority_consumed: bool
    ledger_binding: bool


def evaluate_rollback_bindings(
    observed_state: ProductionMemoryState,
    observed_ledger: MemoryRollbackLedger,
    rollback_receipt: MemoryRollbackReceipt,
    commit_receipt: MemoryApplicationReceipt,
) -> RollbackBindings:
    exact_state = (
        rollback_receipt.after_state_digest == observed_state.digest
        and rollback_receipt.after_state_revision == observed_state.revision
        and rollback_receipt.state_id == observed_state.state_id
    )
    exact_payload = (
        rollback_receipt.restored_kernel_digest == observed_state.current_kernel.digest
        and rollback_receipt.restored_connection_digest
        == observed_state.current_connection.digest
        and rollback_receipt.restored_kernel_digest
        == commit_receipt.rollback_target_digest
        and rollback_receipt.restored_kernel_digest
        == commit_receipt.source_kernel_digest
    )
    revision_successor = (
        rollback_receipt.after_state_revision
        == rollback_receipt.before_state_revision + 1
    )
    state_chain = (
        observed_state.previous_state_digest == rollback_receipt.before_state_digest
        and rollback_receipt.before_state_digest == commit_receipt.after_state_digest
        and rollback_receipt.before_state_revision == commit_receipt.after_revision
    )
    authority_consumed = (
        commit_receipt.authority_consumed
        and commit_receipt.review_receipt_digest
        in observed_state.consumed_review_receipts
    )
    ledger_binding = (
        rollback_receipt.after_ledger_digest == observed_ledger.digest
        and rollback_receipt.after_ledger_revision == observed_ledger.revision
        and rollback_receipt.after_ledger_revision
        == rollback_receipt.before_ledger_revision + 1
        and commit_receipt.receipt_digest
        in observed_ledger.rolled_back_commit_receipts
    )
    return RollbackBindings(
        exact_state,
        exact_payload,
        revision_successor,
        state_chain,
        authority_consumed,
        ledger_binding,
    )
