#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiNavigationLandingSurface:
    landing_version: str
    landing_status: str
    landing_receipt_id: str
    source_renderer_receipt_id: str | None
    source_catalog_id: str | None
    html_artifact_name: str | None
    html_sha256: str | None
    html_bytes: int | None
    navigation_landing_key: str
    navigation_landing_uri: str
    navigation_landing_hash: str
    catalog_key: str | None
    navigation_index_key: str | None
    navigation_index_hash: str | None
    catalog_entry_count: int
    landing_surface_registered: bool
    navigation_entrypoint_ready: bool
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
    landing_blockers: list[str]
    landing_warnings: list[str]
    authority: str = "navigation_landing_surface"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_navigation_landing_surface(
    *,
    catalog_renderer_receipt: Mapping[str, Any],
    landing_context: Mapping[str, Any] | None = None,
) -> QiNavigationLandingSurface:
    receipt = _mapping(catalog_renderer_receipt)
    ctx = _mapping(landing_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("navigation_landing_surface_enabled") is not True:
        blockers.append("navigation_landing_surface_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if receipt.get("renderer_status") != "QI_CATALOG_STATIC_RENDERER_READY":
        blockers.append("catalog_renderer_not_ready")
    if receipt.get("multi_dashboard_index_ready") is not True:
        blockers.append("multi_dashboard_index_not_ready")
    if receipt.get("catalog_static_html_rendered") is not True:
        blockers.append("catalog_static_html_not_rendered")
    if receipt.get("js_enabled") is not False:
        blockers.append("js_enabled_not_false")
    if receipt.get("external_network_required") is not False:
        blockers.append("external_network_required_not_false")
    if receipt.get("read_only_surface") is not True:
        blockers.append("renderer_not_read_only")

    source_renderer_receipt_id = receipt.get("renderer_receipt_id")
    source_catalog_id = receipt.get("source_catalog_id")
    html_artifact_name = receipt.get("html_artifact_name")
    html_sha256 = receipt.get("html_sha256")
    html_bytes = receipt.get("html_bytes")
    try:
        html_bytes_int = int(html_bytes) if html_bytes is not None else None
    except (TypeError, ValueError):
        html_bytes_int = None
        blockers.append("html_bytes_invalid")

    required = {
        "source_renderer_receipt_id": source_renderer_receipt_id,
        "source_catalog_id": source_catalog_id,
        "html_artifact_name": html_artifact_name,
        "html_sha256": html_sha256,
        "html_bytes": html_bytes_int,
        "catalog_key": receipt.get("catalog_key"),
        "navigation_index_key": receipt.get("navigation_index_key"),
        "navigation_index_hash": receipt.get("navigation_index_hash"),
    }
    for name, value in required.items():
        if value in (None, ""):
            blockers.append(f"{name}_missing")

    catalog_entry_count = receipt.get("catalog_entry_count")
    try:
        catalog_entry_count_int = int(catalog_entry_count) if catalog_entry_count is not None else 0
    except (TypeError, ValueError):
        catalog_entry_count_int = 0
        blockers.append("catalog_entry_count_invalid")
    if catalog_entry_count_int <= 0:
        blockers.append("catalog_entry_count_not_positive")

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
        if receipt.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    publication_base = str(ctx.get("landing_base", "static/qi-dashboard"))
    artifact_name = str(html_artifact_name or "qi-dashboard-catalog-missing.html")
    navigation_landing_key = str(ctx.get("navigation_landing_key") or f"qi/navigation/landing/{source_catalog_id or 'unknown'}")
    navigation_landing_uri = str(ctx.get("navigation_landing_uri") or f"file://{publication_base.rstrip('/')}/{artifact_name}")
    landing_material = {
        "source_renderer_receipt_id": source_renderer_receipt_id,
        "source_catalog_id": source_catalog_id,
        "html_sha256": html_sha256,
        "navigation_landing_key": navigation_landing_key,
        "navigation_landing_uri": navigation_landing_uri,
        "navigation_index_hash": receipt.get("navigation_index_hash"),
    }
    navigation_landing_hash = _digest(landing_material)
    landing_receipt_id = "qi-landing-" + navigation_landing_hash[:16]
    ready = not blockers
    if ready and not navigation_landing_uri.startswith(("file://", "https://", "http://")):
        warnings.append("navigation_landing_uri_scheme_unusual")

    return QiNavigationLandingSurface(
        landing_version="kuuos_runtime_daemon_qi_navigation_landing_surface_v0_1",
        landing_status="QI_NAVIGATION_LANDING_SURFACE_READY" if ready else "QI_NAVIGATION_LANDING_SURFACE_BLOCKED",
        landing_receipt_id=landing_receipt_id,
        source_renderer_receipt_id=str(source_renderer_receipt_id) if source_renderer_receipt_id else None,
        source_catalog_id=str(source_catalog_id) if source_catalog_id else None,
        html_artifact_name=str(html_artifact_name) if html_artifact_name else None,
        html_sha256=str(html_sha256) if html_sha256 else None,
        html_bytes=html_bytes_int,
        navigation_landing_key=navigation_landing_key,
        navigation_landing_uri=navigation_landing_uri,
        navigation_landing_hash=navigation_landing_hash,
        catalog_key=str(receipt.get("catalog_key")) if receipt.get("catalog_key") else None,
        navigation_index_key=str(receipt.get("navigation_index_key")) if receipt.get("navigation_index_key") else None,
        navigation_index_hash=str(receipt.get("navigation_index_hash")) if receipt.get("navigation_index_hash") else None,
        catalog_entry_count=catalog_entry_count_int,
        landing_surface_registered=ready,
        navigation_entrypoint_ready=ready,
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
        landing_blockers=blockers,
        landing_warnings=warnings,
    )
