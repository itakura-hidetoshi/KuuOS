#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_memory_application_receipt_v0_75 import MemoryApplicationReceipt
from runtime.kuuos_memory_rollback_ledger_v0_76 import MemoryRollbackLedger
from runtime.kuuos_memory_rollback_receipt_v0_76 import MemoryRollbackReceipt
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState
from runtime.kuuos_v077_b import rollback_receipt_issues
from runtime.kuuos_v077_c import evaluate_rollback_bindings
from runtime.kuuos_v077_runtime import seal_verification_record
from runtime.kuuos_v077_types import (
    BLOCKED,
    ROLLBACK_KIND,
    VERIFIED,
    MemoryVerificationRecord,
)


def verify_rolled_back_memory_state(
    observed_state: ProductionMemoryState,
    observed_ledger: MemoryRollbackLedger,
    rollback_receipt: MemoryRollbackReceipt,
    commit_receipt: MemoryApplicationReceipt,
) -> MemoryVerificationRecord:
    issues = rollback_receipt_issues(rollback_receipt, commit_receipt)
    bindings = evaluate_rollback_bindings(
        observed_state,
        observed_ledger,
        rollback_receipt,
        commit_receipt,
    )
    if not bindings.exact_state:
        issues.append("rollback_observed_state_mismatch")
    if not bindings.exact_payload:
        issues.append("rollback_observed_payload_mismatch")
    if not bindings.revision_successor:
        issues.append("rollback_revision_not_successor")
    if not bindings.state_chain:
        issues.append("rollback_state_chain_mismatch")
    if not bindings.authority_consumed:
        issues.append("rollback_authority_consumption_missing")
    if not bindings.ledger_binding:
        issues.append("rollback_observed_ledger_mismatch")

    return seal_verification_record(MemoryVerificationRecord(
        status=VERIFIED if not issues else BLOCKED,
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
        exact_state_binding=bindings.exact_state,
        exact_payload_binding=bindings.exact_payload,
        revision_successor=bindings.revision_successor,
        state_chain_preserved=bindings.state_chain,
        authority_consumption_preserved=bindings.authority_consumed,
        ledger_binding_preserved=bindings.ledger_binding,
        record_only=True,
        writes_enabled=False,
        live_application_enabled=False,
        permission_expansion_enabled=False,
        issues=tuple(dict.fromkeys(issues)),
        record_digest="",
    ))
