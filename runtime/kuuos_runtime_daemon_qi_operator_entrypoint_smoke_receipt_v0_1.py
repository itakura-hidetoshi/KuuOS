#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiOperatorEntrypointSmokeReceipt:
    receipt_version: str
    smoke_status: str
    smoke_receipt_id: str
    source_landing_receipt_id: str | None
    source_catalog_id: str | None
    navigation_landing_key: str | None
    navigation_landing_uri: str | None
    navigation_landing_hash: str | None
    html_artifact_name: str | None
    html_sha256: str | None
    catalog_entry_count: int
    entrypoint_uri_resolved: bool
    entrypoint_hash_confirmed: bool
    published_landing_receipt_ready: bool
    operator_entrypoint_ready: bool
    smoke_mode: str
    smoke_summary: str
    read_only_surface: bool
    js_enabled: bool
    external_network_required: bool
    daemon_control_performed: bool
    daemon_restart_performed: bool
    daemon_stop_performed: bool
    daemon_resume_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    auto_remediation_performed: bool
    grants_daemon_control_authority: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    smoke_blockers: list[str]
    smoke_warnings: list[str]
    authority: str = "operator_entrypoint_smoke_receipt"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_operator_entrypoint_smoke_receipt(
    *,
    landing_surface: Mapping[str, Any],
    smoke_context: Mapping[str, Any] | None = None,
) -> QiOperatorEntrypointSmokeReceipt:
    landing = _mapping(landing_surface)
    ctx = _mapping(smoke_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("operator_entrypoint_smoke_enabled") is not True:
        blockers.append("operator_entrypoint_smoke_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if landing.get("landing_status") != "QI_NAVIGATION_LANDING_SURFACE_READY":
        blockers.append("landing_surface_not_ready")
    if landing.get("navigation_entrypoint_ready") is not True:
        blockers.append("navigation_entrypoint_not_ready")
    if landing.get("landing_surface_registered") is not True:
        blockers.append("landing_surface_not_registered")
    if landing.get("read_only_surface") is not True:
        blockers.append("landing_not_read_only")
    if landing.get("js_enabled") is not False:
        blockers.append("js_enabled_not_false")
    if landing.get("external_network_required") is not False:
        blockers.append("external_network_required_not_false")

    source_landing_receipt_id = landing.get("landing_receipt_id")
    source_catalog_id = landing.get("source_catalog_id")
    navigation_landing_key = landing.get("navigation_landing_key")
    navigation_landing_uri = landing.get("navigation_landing_uri")
    navigation_landing_hash = landing.get("navigation_landing_hash")
    html_artifact_name = landing.get("html_artifact_name")
    html_sha256 = landing.get("html_sha256")

    for key, value in {
        "source_landing_receipt_id": source_landing_receipt_id,
        "source_catalog_id": source_catalog_id,
        "navigation_landing_key": navigation_landing_key,
        "navigation_landing_uri": navigation_landing_uri,
        "navigation_landing_hash": navigation_landing_hash,
        "html_artifact_name": html_artifact_name,
        "html_sha256": html_sha256,
    }.items():
        if value in (None, ""):
            blockers.append(f"{key}_missing")

    try:
        catalog_entry_count = int(landing.get("catalog_entry_count", 0) or 0)
    except (TypeError, ValueError):
        catalog_entry_count = 0
        blockers.append("catalog_entry_count_invalid")
    if catalog_entry_count <= 0:
        blockers.append("catalog_entry_count_not_positive")

    expected_uri = ctx.get("expected_navigation_landing_uri")
    if expected_uri and navigation_landing_uri != expected_uri:
        blockers.append("navigation_landing_uri_mismatch")
    observed_hash = ctx.get("observed_navigation_landing_hash") or navigation_landing_hash
    if observed_hash != navigation_landing_hash:
        blockers.append("navigation_landing_hash_mismatch")

    uri = str(navigation_landing_uri or "")
    entrypoint_uri_resolved = uri.startswith(("file://", "https://", "http://")) and not any(b.endswith("_missing") for b in blockers)
    entrypoint_hash_confirmed = bool(navigation_landing_hash) and observed_hash == navigation_landing_hash

    forbidden_flags = [
        "daemon_control_performed",
        "daemon_restart_performed",
        "daemon_stop_performed",
        "daemon_resume_performed",
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "auto_remediation_performed",
        "grants_daemon_control_authority",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
    ]
    for flag in forbidden_flags:
        if landing.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    ready = not blockers and entrypoint_uri_resolved and entrypoint_hash_confirmed
    if ready and uri.startswith("http://"):
        warnings.append("navigation_landing_uri_plain_http")

    smoke_mode = str(ctx.get("smoke_mode", "read_only_entrypoint_receipt"))
    material = {
        "source_landing_receipt_id": source_landing_receipt_id,
        "navigation_landing_uri": navigation_landing_uri,
        "navigation_landing_hash": navigation_landing_hash,
        "html_sha256": html_sha256,
        "smoke_mode": smoke_mode,
    }
    smoke_receipt_id = "qi-entrypoint-smoke-" + _digest(material)[:16]
    smoke_summary = (
        f"Operator entrypoint {navigation_landing_key or 'unknown'} resolves to "
        f"{navigation_landing_uri or 'missing'} with {catalog_entry_count} catalog entries."
    )

    return QiOperatorEntrypointSmokeReceipt(
        receipt_version="kuuos_runtime_daemon_qi_operator_entrypoint_smoke_receipt_v0_1",
        smoke_status="QI_OPERATOR_ENTRYPOINT_SMOKE_RECEIPT_READY" if ready else "QI_OPERATOR_ENTRYPOINT_SMOKE_RECEIPT_BLOCKED",
        smoke_receipt_id=smoke_receipt_id,
        source_landing_receipt_id=str(source_landing_receipt_id) if source_landing_receipt_id else None,
        source_catalog_id=str(source_catalog_id) if source_catalog_id else None,
        navigation_landing_key=str(navigation_landing_key) if navigation_landing_key else None,
        navigation_landing_uri=str(navigation_landing_uri) if navigation_landing_uri else None,
        navigation_landing_hash=str(navigation_landing_hash) if navigation_landing_hash else None,
        html_artifact_name=str(html_artifact_name) if html_artifact_name else None,
        html_sha256=str(html_sha256) if html_sha256 else None,
        catalog_entry_count=catalog_entry_count,
        entrypoint_uri_resolved=entrypoint_uri_resolved,
        entrypoint_hash_confirmed=entrypoint_hash_confirmed,
        published_landing_receipt_ready=ready,
        operator_entrypoint_ready=ready,
        smoke_mode=smoke_mode,
        smoke_summary=smoke_summary,
        read_only_surface=ctx.get("read_only_surface_required") is True,
        js_enabled=False,
        external_network_required=False,
        daemon_control_performed=False,
        daemon_restart_performed=False,
        daemon_stop_performed=False,
        daemon_resume_performed=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        auto_remediation_performed=False,
        grants_daemon_control_authority=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        smoke_blockers=blockers,
        smoke_warnings=warnings,
    )
