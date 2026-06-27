#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_connection_candidate_admission_v0_63"
REQUEST_VERSION = "kuuos_connection_admission_request_v0_63"
LICENSE_VERSION = "kuuos_connection_admission_license_v0_63"

ADMIT = "ADMIT"
REJECT = "REJECT"
DEFER = "DEFER"
ALLOWED_DECISIONS = {ADMIT, REJECT, DEFER}

READY = "READY_FOR_STAGED_CONNECTION_UPDATE"
REJECTED = "CONNECTION_CANDIDATE_REJECTED"
DEFERRED = "CONNECTION_CANDIDATE_DEFERRED"
BLOCKED = "CONNECTION_CANDIDATE_ADMISSION_BLOCKED"

STAGING_SCOPE = "stage_connection_candidate"
EXTERNAL_SUPERVISOR_CLASS = "external_human_or_governed_supervisor"


@dataclass(frozen=True)
class ConnectionAdmissionRequest:
    request_id: str
    requested_by: str
    source_bundle_digest: str
    proposal_digest: str
    selected_receipt_digest: str
    candidate_connection_digest: str
    rollback_digest: str
    requested_scope: str
    candidate_only: bool
    state_write_requested: bool
    request_digest: str
    version: str = REQUEST_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SupervisorAdmissionLicense:
    license_id: str
    supervisor_id: str
    supervisor_class: str
    decision: str
    bound_request_digest: str
    bound_source_bundle_digest: str
    bound_selected_receipt_digest: str
    bound_candidate_connection_digest: str
    bound_rollback_digest: str
    allowed_scopes: tuple[str, ...]
    valid_from_epoch: int
    valid_through_epoch: int
    production_apply_allowed: bool
    state_write_allowed: bool
    privilege_escalation_allowed: bool
    license_digest: str
    version: str = LICENSE_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_scopes"] = list(self.allowed_scopes)
        return payload


@dataclass(frozen=True)
class ConnectionAdmissionReceipt:
    status: str
    request_digest: str
    license_digest: str
    proposal_digest: str
    selected_receipt_digest: str
    source_bundle_digest: str
    candidate_connection_digest: str
    rollback_digest: str
    supervisor_id: str
    decision: str
    staging_scope: str
    staging_ready: bool
    production_apply_ready: bool
    candidate_only: bool
    state_write_performed: bool
    authority_widened: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        payload["warnings"] = list(self.warnings)
        return payload


def digest_without(value: dict[str, Any], field: str) -> str:
    payload = dict(value)
    payload.pop(field, None)
    return canonical_digest(payload)


def request_digest(request: ConnectionAdmissionRequest) -> str:
    return digest_without(request.to_dict(), "request_digest")


def license_digest(license_packet: SupervisorAdmissionLicense) -> str:
    return digest_without(license_packet.to_dict(), "license_digest")
