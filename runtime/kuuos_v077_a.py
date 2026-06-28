#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_memory_application_receipt_v0_75 import (
    APPLICATION_COMMITTED,
    MemoryApplicationReceipt,
    memory_application_receipt_digest,
)
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState
from runtime.kuuos_v077_runtime import seal_verification_record
from runtime.kuuos_v077_types import (
    BLOCKED,
    COMMIT_KIND,
    VERIFIED,
    MemoryVerificationRecord,
)


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
    exact_payload = (
        receipt.selected_kernel_digest == observed_state.current_kernel.digest
        and receipt.selected_connection_digest == observed_state.current_connection.digest
    )
    revision_successor = receipt.after_revision == receipt.before_revision + 1
    state_chain = observed_state.previous_state_digest == receipt.before_state_digest
    authority_consumed = (
        receipt.authority_consumed
        and receipt.review_receipt_digest in observed_state.consumed_review_receipts
    )

    if not exact_state:
        issues.append("commit_observed_state_mismatch")
    if not exact_payload:
        issues.append("commit_observed_payload_mismatch")
    if not revision_successor:
        issues.append("commit_revision_not_successor")
    if not state_chain:
        issues.append("commit_state_chain_mismatch")
    if not authority_consumed:
        issues.append("commit_authority_consumption_missing")

    return seal_verification_record(MemoryVerificationRecord(
        status=VERIFIED if not issues else BLOCKED,
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
