#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_rollback_ledger_v0_76 import VERSION

ROLLBACK_COMMITTED = "MEMORY_ROLLBACK_COMMITTED"
ROLLBACK_BLOCKED = "MEMORY_ROLLBACK_BLOCKED"


@dataclass(frozen=True)
class MemoryRollbackReceipt:
    status: str
    request_digest: str
    commit_receipt_digest: str
    state_id: str
    before_state_digest: str
    after_state_digest: str
    before_state_revision: int
    after_state_revision: int
    before_ledger_digest: str
    after_ledger_digest: str
    before_ledger_revision: int
    after_ledger_revision: int
    restored_kernel_digest: str
    restored_connection_digest: str
    rollback_epoch: int
    atomic_commit: bool
    state_write_performed: bool
    live_application_performed: bool
    permission_expansion_performed: bool
    review_authority_reenabled: bool
    issues: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def memory_rollback_receipt_digest(receipt: MemoryRollbackReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
