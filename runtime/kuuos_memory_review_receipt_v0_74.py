#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_review_request_v0_74 import VERSION

APPROVE_MEMORY_SELECTION = "APPROVE_MEMORY_SELECTION"
REJECT_MEMORY_SELECTION = "REJECT_MEMORY_SELECTION"
REQUEST_REEVALUATION = "REQUEST_REEVALUATION"
ALLOWED_DECISIONS = frozenset({
    APPROVE_MEMORY_SELECTION,
    REJECT_MEMORY_SELECTION,
    REQUEST_REEVALUATION,
})


@dataclass(frozen=True)
class MemoryReviewReceipt:
    status: str
    decision: str
    request_digest: str
    selection_record_digest: str
    reviewer_id: str
    reviewer_class: str
    source_history_digest: str
    source_kernel_digest: str
    family_digest: str
    selected_member_digest: str
    selected_deformation_digest: str
    selected_kernel_digest: str
    selected_connection_digest: str
    rollback_target_digest: str
    valid_from_epoch: int
    valid_until_epoch: int
    decided_at_epoch: int
    production_application_authority: bool
    writes_enabled: bool
    live_application_enabled: bool
    permission_expansion_enabled: bool
    rollback_target_replacement_enabled: bool
    issues: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def memory_review_receipt_digest(receipt: MemoryReviewReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
