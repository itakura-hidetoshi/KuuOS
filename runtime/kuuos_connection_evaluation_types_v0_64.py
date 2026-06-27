#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

VERSION = "kuuos_connection_evaluation_v0_64"
READY_STATUS = "READY_FOR_CONNECTION_STAGING_REVIEW"
BLOCKED_STATUS = "CONNECTION_EVALUATION_BLOCKED"


@dataclass(frozen=True)
class ConnectionEvaluationPolicy:
    max_cases: int = 32
    tolerance: float = 1e-12
    require_strict_improvement_in_one_case: bool = True

    def __post_init__(self) -> None:
        if not 1 <= self.max_cases <= 256:
            raise ValueError("connection_evaluation_max_cases_invalid")
        if self.tolerance < 0.0 or not math.isfinite(self.tolerance):
            raise ValueError("connection_evaluation_tolerance_invalid")


@dataclass(frozen=True)
class ConnectionEvaluationCaseReceipt:
    case_id: str
    source_bundle_digest: str
    source_curvature: float | None
    candidate_curvature: float | None
    curvature_nonincreasing: bool
    curvature_strictly_decreased: bool
    memory_holonomy_preserved: bool
    fields_preserved: bool
    source_bindings_preserved: bool
    admissible: bool
    blockers: tuple[str, ...]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


@dataclass(frozen=True)
class ConnectionEvaluationReceipt:
    status: str
    source_bundle_digest: str
    proposal_digest: str
    admission_receipt_digest: str
    selected_receipt_digest: str
    candidate_connection_digest: str
    rollback_digest: str
    case_receipts: tuple[ConnectionEvaluationCaseReceipt, ...]
    evaluated_case_count: int
    all_cases_admissible: bool
    strict_improvement_observed: bool
    staging_review_ready: bool
    production_apply_ready: bool
    state_write_performed: bool
    authority_widened: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["case_receipts"] = [case.to_dict() for case in self.case_receipts]
        payload["blockers"] = list(self.blockers)
        return payload
