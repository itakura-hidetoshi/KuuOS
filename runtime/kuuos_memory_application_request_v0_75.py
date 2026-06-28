#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_review_receipt_v0_74 import MemoryReviewReceipt
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState

VERSION = "kuuos_authorized_memory_application_v0_75"


@dataclass(frozen=True)
class MemoryApplicationRequest:
    request_id: str
    target_state_id: str
    expected_state_digest: str
    expected_revision: int
    review_receipt_digest: str
    source_kernel_digest: str
    selected_kernel_digest: str
    selected_connection_digest: str
    rollback_target_digest: str
    apply_epoch: int
    request_digest: str
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.request_id or not self.target_state_id:
            raise ValueError("memory_application_request_identity_missing")
        if self.expected_revision < 0 or self.apply_epoch < 0:
            raise ValueError("memory_application_request_epoch_invalid")
        bindings = (
            self.expected_state_digest,
            self.review_receipt_digest,
            self.source_kernel_digest,
            self.selected_kernel_digest,
            self.selected_connection_digest,
            self.rollback_target_digest,
        )
        if any(not value for value in bindings):
            raise ValueError("memory_application_request_binding_missing")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def memory_application_request_digest(request: MemoryApplicationRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


def build_memory_application_request(
    request_id: str,
    state: ProductionMemoryState,
    review: MemoryReviewReceipt,
    apply_epoch: int,
) -> MemoryApplicationRequest:
    request = MemoryApplicationRequest(
        request_id,
        state.state_id,
        state.digest,
        state.revision,
        review.receipt_digest,
        review.source_kernel_digest,
        review.selected_kernel_digest,
        review.selected_connection_digest,
        review.rollback_target_digest,
        apply_epoch,
        "",
    )
    return replace(request, request_digest=memory_application_request_digest(request))
