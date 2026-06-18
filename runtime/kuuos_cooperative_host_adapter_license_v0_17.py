from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    LICENSE_VERSION,
    READY,
    license_digest,
)

REQUIRED_PERMISSIONS = (
    "bundle_read_allowed",
    "projection_consume_allowed",
    "ticket_claim_allowed",
    "bounded_slice_execute_allowed",
    "bundle_output_write_allowed",
    "receipt_write_allowed",
    "audit_append_allowed",
)


def build_host_license(
    *,
    license_id: str,
    issued_at_ms: int,
    expires_at_ms: int,
    operation_allowlist: Sequence[str],
    max_steps_per_slice: int = 1,
    max_cost_per_slice: float = 1.0,
    lease_duration_ms: int = 60_000,
    in_place_bundle_write_allowed: bool = False,
    permissions: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    allowed = sorted({str(item).strip() for item in operation_allowlist if str(item).strip()})
    if not allowed:
        raise ValueError("host_operation_allowlist_empty")
    issued = max(0, int(issued_at_ms))
    expires = max(0, int(expires_at_ms))
    if expires <= issued:
        raise ValueError("host_license_expiry_invalid")
    grants = {name: True for name in REQUIRED_PERMISSIONS}
    if permissions is not None:
        for name in REQUIRED_PERMISSIONS:
            grants[name] = permissions.get(name) is True
    packet = {
        "version": LICENSE_VERSION,
        "license_status": READY,
        "license_id": str(license_id),
        "issued_at_ms": issued,
        "expires_at_ms": expires,
        "operation_allowlist": allowed,
        "max_jobs_per_invocation": 1,
        "max_steps_per_slice": min(25, max(1, int(max_steps_per_slice))),
        "max_cost_per_slice": max(0.0, float(max_cost_per_slice)),
        "lease_duration_ms": min(86_400_000, max(1, int(lease_duration_ms))),
        "in_place_bundle_write_allowed": bool(in_place_bundle_write_allowed),
        **grants,
        "host_license_digest": "",
    }
    packet["host_license_digest"] = license_digest(packet)
    return packet


def validate_host_license(license_packet: Mapping[str, Any], *, now_ms: int) -> list[str]:
    blockers: list[str] = []
    if str(license_packet.get("version", "")) != LICENSE_VERSION:
        blockers.append("host_license_version_invalid")
    if str(license_packet.get("license_status", "")) != READY:
        blockers.append("host_license_not_ready")
    digest = str(license_packet.get("host_license_digest", ""))
    if not digest or digest != license_digest(license_packet):
        blockers.append("host_license_digest_invalid")
    now = max(0, int(now_ms))
    if int(license_packet.get("issued_at_ms", 0) or 0) > now:
        blockers.append("host_license_not_yet_valid")
    if int(license_packet.get("expires_at_ms", 0) or 0) <= now:
        blockers.append("host_license_expired")
    if int(license_packet.get("max_jobs_per_invocation", 0) or 0) != 1:
        blockers.append("host_license_job_bound_invalid")
    if int(license_packet.get("max_steps_per_slice", 0) or 0) < 1:
        blockers.append("host_license_step_bound_invalid")
    if float(license_packet.get("max_cost_per_slice", -1.0) or 0.0) < 0.0:
        blockers.append("host_license_cost_bound_invalid")
    if int(license_packet.get("lease_duration_ms", 0) or 0) < 1:
        blockers.append("host_license_lease_duration_invalid")
    allowed = license_packet.get("operation_allowlist", [])
    if not isinstance(allowed, list) or not allowed or any(not str(item).strip() for item in allowed):
        blockers.append("host_operation_allowlist_invalid")
    for name in REQUIRED_PERMISSIONS:
        if license_packet.get(name) is not True:
            blockers.append(f"{name}_not_true")
    return blockers
