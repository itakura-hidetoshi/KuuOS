#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_application_request_v0_75 import VERSION

APPLICATION_COMMITTED = "MEMORY_APPLICATION_COMMITTED"
APPLICATION_BLOCKED = "MEMORY_APPLICATION_BLOCKED"


@dataclass(frozen=True)
class MemoryApplicationReceipt:
    status: str
    request_digest: str
    review_receipt_digest: str
    state_id: str
    before_state_digest: str
    after_state_digest: str
    before_revision: int
    after_revision: int
    source_kernel_digest: str
    selected_kernel_digest: str
    selected_connection_digest: str
    rollback_target_digest: str
    applied_at_epoch: int
    authority_consumed: bool
    atomic_commit: bool
    state_write_performed: bool
    live_application_performed: bool
    permission_expansion_performed: bool
    rollback_target_replaced: bool
    issues: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def memory_application_receipt_digest(receipt: MemoryApplicationReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
