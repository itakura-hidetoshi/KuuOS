#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

VERSION = "kuuos_connection_shadow_materialization_v0_66"
READY = "CONNECTION_SHADOW_MATERIALIZATION_READY"
BLOCKED = "CONNECTION_SHADOW_MATERIALIZATION_BLOCKED"


@dataclass(frozen=True)
class ConnectionShadowReceipt:
    status: str
    source_bundle_digest_before: str
    source_bundle_digest_after: str
    source_connection_digest: str
    staging_package_digest: str
    staging_namespace: str
    candidate_connection_digest: str
    rollback_bundle_digest: str
    shadow_bundle_digest: str
    source_curvature: float | None
    shadow_curvature: float | None
    curvature_nonincreasing: bool
    memory_holonomy_preserved: bool
    fields_preserved: bool
    source_bindings_preserved: bool
    source_unchanged: bool
    rollback_witness_ready: bool
    shadow_only: bool
    production_apply_ready: bool
    state_write_performed: bool
    authority_widened: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload
