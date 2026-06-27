#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

VERSION = "kuuos_connection_orbit_validation_v0_67"
READY = "CONNECTION_ORBIT_VALIDATION_READY"
BLOCKED = "CONNECTION_ORBIT_VALIDATION_BLOCKED"


@dataclass(frozen=True)
class OrbitSampleReceipt:
    sample_id: str
    source_curvature_residual: float
    shadow_curvature_residual: float
    source_holonomy_residual: float
    shadow_holonomy_residual: float
    relative_curvature_nonincreasing: bool
    relative_memory_holonomy_preserved: bool
    fields_synchronized: bool
    source_bindings_synchronized: bool
    admissible: bool
    blockers: tuple[str, ...]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


@dataclass(frozen=True)
class ConnectionOrbitValidationReceipt:
    status: str
    source_bundle_digest_before: str
    source_bundle_digest_after: str
    shadow_bundle_digest: str
    shadow_receipt_digest: str
    rollback_bundle_digest: str
    sample_receipts: tuple[OrbitSampleReceipt, ...]
    sample_count: int
    all_samples_admissible: bool
    rollback_reconstruction_exact: bool
    source_unchanged: bool
    orbit_only: bool
    production_apply_ready: bool
    state_write_performed: bool
    authority_widened: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["sample_receipts"] = [sample.to_dict() for sample in self.sample_receipts]
        payload["blockers"] = list(self.blockers)
        return payload
