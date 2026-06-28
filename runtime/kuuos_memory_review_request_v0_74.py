#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_review_identity_v0_74 import ALLOWED_REVIEWER_CLASSES
from runtime.kuuos_memory_selection_v0_73 import MemorySelectionRecord

VERSION = "kuuos_memory_selection_review_v0_74"


@dataclass(frozen=True)
class MemoryReviewRequest:
    request_id: str
    requester_id: str
    selection_record_digest: str
    source_history_digest: str
    source_kernel_digest: str
    family_digest: str
    selected_member_digest: str
    selected_deformation_digest: str
    selected_kernel_digest: str
    selected_connection_digest: str
    rollback_target_digest: str
    allowed_reviewer_classes: tuple[str, ...]
    valid_from_epoch: int
    valid_until_epoch: int
    request_digest: str
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.request_id or not self.requester_id:
            raise ValueError("memory_review_request_identity_missing")
        if self.valid_from_epoch < 0 or self.valid_until_epoch <= self.valid_from_epoch:
            raise ValueError("memory_review_request_window_invalid")
        if not self.allowed_reviewer_classes:
            raise ValueError("memory_review_reviewer_scope_empty")
        if any(item not in ALLOWED_REVIEWER_CLASSES for item in self.allowed_reviewer_classes):
            raise ValueError("memory_review_reviewer_scope_invalid")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_reviewer_classes"] = list(self.allowed_reviewer_classes)
        return payload


def memory_review_request_digest(request: MemoryReviewRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


def build_memory_review_request(
    request_id: str,
    requester_id: str,
    selection: MemorySelectionRecord,
    allowed_reviewer_classes: tuple[str, ...],
    valid_from_epoch: int,
    valid_until_epoch: int,
) -> MemoryReviewRequest:
    if not selection.selected_member_digest:
        raise ValueError("memory_review_selection_missing")
    request = MemoryReviewRequest(
        request_id,
        requester_id,
        selection.record_digest,
        selection.source_history_digest,
        selection.source_kernel_digest,
        selection.family_digest,
        selection.selected_member_digest,
        selection.selected_deformation_digest,
        selection.selected_kernel_digest,
        selection.selected_connection_digest,
        selection.source_kernel_digest,
        tuple(dict.fromkeys(allowed_reviewer_classes)),
        valid_from_epoch,
        valid_until_epoch,
        "",
    )
    return replace(request, request_digest=memory_review_request_digest(request))
