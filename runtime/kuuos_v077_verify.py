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
    ROLLBACK_COMMITTED,
    MemoryRollbackReceipt,
    memory_rollback_receipt_digest,
)
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState
from runtime.kuuos_v077_types import (
    BLOCKED,
    COMMIT_KIND,
    ROLLBACK_KIND,
    VERIFIED,
    MemoryVerificationRecord,
    verification_record_digest,
)


def _seal(record: MemoryVerificationRecord) -> MemoryVerificationRecord:
    return replace(record, record_digest=verification_record_digest(record))


def verify_committed_memory_state(
    observed_state: ProductionMemoryState,
    receipt: MemoryApplicationReceipt,
) -> MemoryVerificationRecord:
    issues: list[str] = []
    if receipt.receipt_digest != memory_application_receipt_digest(receipt):
        issues.append("commit_receipt_digest_mismatch")
    if receipt.status != APPLICATION_COMMITTED:
        issues.append("commit_receipt_not_committed")
    if not receipt.atomic_commit:
        issues.append("commit_not_atomic")
    if not receipt.state_write_performed or not receipt.live_application_performed:
        issues.append("commit_effect_missing")
    if not receipt.authority_consumed:
        issues.append("commit_receipt_authority_not_consumed")
    if receipt.permission_expansion_performed:
        issues.append("commit_permission_expansion")
    if receipt.rollback_target_replaced:
        issues.append("commit_rollback_target_replaced")

    exact_state = (
        receipt.after_state_digest == observed_state.digest
        and receipt.after_revision == observed_state.revision
        and receipt.state_id == observed_state.state_id
    )
    if not exact_state:
        issues.append("commit_observed_state_mismatch")

    exact_payload = (
        receipt.selected_kernel_digest == observed_state.current_kernel.digest
        and receipt.selected_connection_digest == observed_state.current_connection.digest
    )
    if not exact_payload:
        issues.append("commit_observed_payload_mismatch")

    revision_successor = receipt.after_revision == receipt.before_revision + 1
    if not revision_successor:
        issues.append("commit_revision_not_successor")

    state_chain = observed_state.previous_state_digest == receipt.before_state_digest
    if not state_chain:
        issues.append("commit_state_chain_mismatch")

    authority_consumed = (
        receipt.authority_consumed
        and receipt.review_receipt_digest
        in observed_state.consumed_review_receipts
    )
    if not authority_consumed:
        issues.append("commit_authority_consumption_missing")

    status = VERIFIED if not issues else BLOCKED
    return _seal(MemoryVerificationRecord(
        status=status,
        transition_kind=COMMIT_KIND,
        operation_receipt_digest=receipt.receipt_digest,
        commit_receipt_digest=receipt.receipt_digest,
        rollback_receipt_digest="",
        observed_state_digest=observed_state.digest,
        observed_state_revision=observed_state.revision,
        observed_kernel_digest=observed_state.current_kernel.digest,
        observed_connection_digest=observed_state.current_connection.digest,
        observed_ledger_digest="",
        observed_ledger_revision=0,
        exact_state_binding=exact_state,
        exact_payload_binding=exact_payload,
        revision_successor=revision_successor,
        state_chain_preserved=state_chain,
        authority_consumption_preserved=authority_consumed,
        ledger_binding_preserved=True,
        record_only=True,
        writes_enabled=False,
        live_application_enabled=False,
        permission_expansion_enabled=False,
        issues=tuple(dict.fromkeys(issues)),
        record_digest="",
    ))


def verify_rolled_back_memory_state(
    observed_state: ProductionMemoryState,
    observed_ledger: MemoryRollbackLedger,
    rollback_receipt: MemoryRollbackReceipt,
    commit_receipt: MemoryApplicationReceipt,
) -> MemoryVerificationRecord:
    issues: list[str] = []
    if rollback_receipt.receipt_digest != memory_rollback_receipt_digest(rollback_receipt):
        issues.append("rollback_receipt_digest_mismatch")
    if commit_receipt.receipt_digest != memory_application_receipt_digest(commit_receipt):
        issues.append("rollback_commit_receipt_digest_mismatch")
    if rollback_receipt.commit_receipt_digest != commit_receipt.receipt_digest:
        issues.append("rollback_commit_receipt_binding_mismatch")
    if commit_receipt.status != APPLICATION_COMMITTED:
        issues.append("rollback_source_commit_not_committed")
    if not commit_receipt.atomic_commit:
        issues.append("rollback_source_commit_not_atomic")
    if not commit_receipt.authority_consumed:
        issues.append("rollback_source_authority_not_consumed")
    if rollback_receipt.status != ROLLBACK_COMMITTED:
        issues.append("rollback_receipt_not_committed")
    if not rollback_receipt.atomic_commit:
        issues.append("rollback_not_atomic")
    if not rollback_receipt.state_write_performed or not rollback_receipt.live_application_performed:
        issues.append("rollback_effect_missing")
    if rollback_receipt.permission_expansion_performed:
        issues.append("rollback_permission_expansion")
    if rollback_receipt.review_authority_reenabled:
        issues.append("rollback_authority_reenabled")

    exact_state = (
        rollback_receipt.after_state_digest == observed_state.digest
        and rollback_receipt.after_state_revision == observed_state.revision
        and rollback_receipt.state_id == observed_state.state_id
    )
    if not exact_state:
        issues.append("rollback_observed_state_mismatch")

    exact_payload = (
        rollback_receipt.restored_kernel_digest == observed_state.current_kernel.digest
        and rollback_receipt.restored_connection_digest
        == observed_state.current_connection.digest
        and rollback_receipt.restored_kernel_digest
        == commit_receipt.rollback_target_digest
        and rollback_receipt.restored_kernel_digest
        == commit_receipt.source_kernel_digest
    )
    if not exact_payload:
        issues.append("rollback_observed_payload_mismatch")

    revision_successor = (
        rollback_receipt.after_state_revision
        == rollback_receipt.before_state_revision + 1
    )
    if not revision_successor:
        issues.append("rollback_revision_not_successor")

    state_chain = (
        observed_state.previous_state_digest == rollback_receipt.before_state_digest
        and rollback_receipt.before_state_digest == commit_receipt.after_state_digest
        and rollback_receipt.before_state_revision == commit_receipt.after_revision
    )
    if not state_chain:
        issues.append("rollback_state_chain_mismatch")

    authority_consumed = (
        commit_receipt.authority_consumed
        and commit_receipt.review_receipt_digest
        in observed_state.consumed_review_receipts
    )
    if not authority_consumed:
        issues.append("rollback_authority_consumption_missing")

    ledger_binding = (
        rollback_receipt.after_ledger_digest == observed_ledger.digest
        and rollback_receipt.after_ledger_revision == observed_ledger.revision
        and rollback_receipt.after_ledger_revision
        == rollback_receipt.before_ledger_revision + 1
        and commit_receipt.receipt_digest
        in observed_ledger.rolled_back_commit_receipts
    )
    if not ledger_binding:
        issues.append("rollback_observed_ledger_mismatch")

    status = VERIFIED if not issues else BLOCKED
    return _seal(MemoryVerificationRecord(
        status=status,
        transition_kind=ROLLBACK_KIND,
        operation_receipt_digest=rollback_receipt.receipt_digest,
        commit_receipt_digest=commit_receipt.receipt_digest,
        rollback_receipt_digest=rollback_receipt.receipt_digest,
        observed_state_digest=observed_state.digest,
        observed_state_revision=observed_state.revision,
        observed_kernel_digest=observed_state.current_kernel.digest,
        observed_connection_digest=observed_state.current_connection.digest,
        observed_ledger_digest=observed_ledger.digest,
        observed_ledger_revision=observed_ledger.revision,
        exact_state_binding=exact_state,
        exact_payload_binding=exact_payload,
        revision_successor=revision_successor,
        state_chain_preserved=state_chain,
        authority_consumption_preserved=authority_consumed,
        ledger_binding_preserved=ledger_binding,
        record_only=True,
        writes_enabled=False,
        live_application_enabled=False,
        permission_expansion_enabled=False,
        issues=tuple(dict.fromkeys(issues)),
        record_digest="",
    ))
