#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

EXTERNAL_REVIEWER = "EXTERNAL_REVIEWER"
GOVERNANCE_REVIEWER = "GOVERNANCE_REVIEWER"
ALLOWED_REVIEWER_CLASSES = frozenset({EXTERNAL_REVIEWER, GOVERNANCE_REVIEWER})


@dataclass(frozen=True)
class MemoryReviewerIdentity:
    reviewer_id: str
    reviewer_class: str

    def __post_init__(self) -> None:
        if not self.reviewer_id:
            raise ValueError("memory_reviewer_id_missing")
        if self.reviewer_class not in ALLOWED_REVIEWER_CLASSES:
            raise ValueError("memory_reviewer_class_not_allowed")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
