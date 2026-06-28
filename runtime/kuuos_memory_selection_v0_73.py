#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_assessment_v0_73 import MemoryAssessment


@dataclass(frozen=True)
class MemorySelectionRecord:
    status: str
    source_history_digest: str
    source_kernel_digest: str
    family_digest: str
    selected_member_id: str
    selected_member_digest: str
    selected_deformation_digest: str
    selected_kernel_digest: str
    selected_connection_digest: str
    source_score: float
    selected_score: float
    evaluated_count: int
    accepted_count: int
    source_history_unchanged: bool
    source_kernel_unchanged: bool
    candidate_only: bool
    writes_enabled: bool
    live_application_enabled: bool
    permission_expansion_enabled: bool
    assessments: tuple[MemoryAssessment, ...]
    issues: tuple[str, ...]
    record_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["assessments"] = [item.to_dict() for item in self.assessments]
        payload["issues"] = list(self.issues)
        return payload


def selection_record_digest(record: MemorySelectionRecord) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
