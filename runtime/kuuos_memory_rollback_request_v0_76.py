#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_application_receipt_v0_75 import MemoryApplicationReceipt
from runtime.kuuos_memory_rollback_ledger_v0_76 import (
    VERSION,
    MemoryRollbackLedger,
)
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState


@dataclass(frozen=True)
class MemoryRollbackRequest:
    request_id: str
    target_state_id: str
    expected_state_digest: str
    expected_state_revision: int
    expected_ledger_digest: str
    expected_ledger_revision: int
    commit_receipt_digest: str
    rollback_state_digest: str
    rollback_kernel_digest: str
    rollback_connection_digest: str
    rollback_epoch: int
    request_digest: str
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.request_id or not self.target_state_id:
            raise ValueError("memory_rollback_request_identity_missing")
        if self.expected_state_revision < 0 or self.expected_ledger_revision < 0:
            raise ValueError("memory_rollback_request_revision_invalid")
        if self.rollback_epoch < 0:
            raise ValueError("memory_rollback_request_epoch_invalid")
        bindings = (
            self.expected_state_digest,
            self.expected_ledger_digest,
            self.commit_receipt_digest,
            self.rollback_state_digest,
            self.rollback_kernel_digest,
            self.rollback_connection_digest,
        )
        if any(not value for value in bindings):
            raise ValueError("memory_rollback_request_binding_missing")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def memory_rollback_request_digest(request: MemoryRollbackRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


def build_memory_rollback_request(
    request_id: str,
    current_state: ProductionMemoryState,
    rollback_state: ProductionMemoryState,
    ledger: MemoryRollbackLedger,
    commit_receipt: MemoryApplicationReceipt,
    rollback_epoch: int,
) -> MemoryRollbackRequest:
    request = MemoryRollbackRequest(
        request_id,
        current_state.state_id,
        current_state.digest,
        current_state.revision,
        ledger.digest,
        ledger.revision,
        commit_receipt.receipt_digest,
        rollback_state.digest,
        rollback_state.current_kernel.digest,
        rollback_state.current_connection.digest,
        rollback_epoch,
        "",
    )
    return replace(request, request_digest=memory_rollback_request_digest(request))
