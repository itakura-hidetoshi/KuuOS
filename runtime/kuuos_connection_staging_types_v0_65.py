#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_connection_staging_package_v0_65"
READY = "CONNECTION_STAGING_PACKAGE_READY"
BLOCKED = "CONNECTION_STAGING_PACKAGE_BLOCKED"
SHADOW_PREFIX = "shadow/"


@dataclass(frozen=True)
class ConnectionStagingPackage:
    status: str
    package_id: str
    staging_namespace: str
    source_bundle_digest: str
    proposal_digest: str
    admission_receipt_digest: str
    evaluation_receipt_digest: str
    selected_receipt_digest: str
    candidate_connection_digest: str
    rollback_digest: str
    candidate_connection_payload: Mapping[str, Any]
    immutable: bool
    candidate_only: bool
    production_apply_allowed: bool
    state_write_allowed: bool
    authority_widening_allowed: bool
    blockers: tuple[str, ...]
    package_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_connection_payload"] = dict(self.candidate_connection_payload)
        payload["blockers"] = list(self.blockers)
        return payload


def package_digest(package: ConnectionStagingPackage) -> str:
    payload = package.to_dict()
    payload.pop("package_digest", None)
    return canonical_digest(payload)
