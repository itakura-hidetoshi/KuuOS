#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.v103_receipt_policy import VERSION


@dataclass(frozen=True)
class CheckpointReceiptResult:
    receipt_id: str
    status: str
    transaction_id: str
    result_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def checkpoint_receipt_result_digest(result: CheckpointReceiptResult) -> str:
    payload = result.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
