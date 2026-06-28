#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_memory_application_receipt_v0_75 import (
    APPLICATION_COMMITTED,
    MemoryApplicationReceipt,
    memory_application_receipt_digest,
)
from runtime.kuuos_memory_rollback_receipt_v0_76 import (
    ROLLBACK_COMMITTED,
    MemoryRollbackReceipt,
    memory_rollback_receipt_digest,
)


def rollback_receipt_issues(
    rollback_receipt: MemoryRollbackReceipt,
    commit_receipt: MemoryApplicationReceipt,
) -> list[str]:
    issues: list[str] = []
    if rollback_receipt.receipt_digest != memory_rollback_receipt_digest(rollback_receipt):
        issues.append("rollback_receipt_digest_mismatch")
    if commit_receipt.receipt_digest != memory_application_receipt_digest(commit_receipt):
        issues.append("rollback_commit_receipt_digest_mismatch")
    if rollback_receipt.commit_receipt_digest != commit_receipt.receipt_digest:
        issues.append("rollback_commit_receipt_binding_mismatch")
    if commit_receipt.status != APPLICATION_COMMITTED or not commit_receipt.atomic_commit:
        issues.append("rollback_source_commit_invalid")
    if not commit_receipt.authority_consumed:
        issues.append("rollback_source_authority_not_consumed")
    if rollback_receipt.status != ROLLBACK_COMMITTED or not rollback_receipt.atomic_commit:
        issues.append("rollback_receipt_invalid")
    if not rollback_receipt.state_write_performed or not rollback_receipt.live_application_performed:
        issues.append("rollback_effect_missing")
    if rollback_receipt.permission_expansion_performed:
        issues.append("rollback_permission_expansion")
    if rollback_receipt.review_authority_reenabled:
        issues.append("rollback_authority_reenabled")
    return issues
