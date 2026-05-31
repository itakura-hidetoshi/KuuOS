#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiStaticPublicationIndexRegistry:
    registry_version: str
    registry_status: str
    publication_receipt_id: str
    source_surface_id: str | None
    html_artifact_name: str | None
    html_sha256: str | None
    html_bytes: int | None
    publication_path: str
    publication_uri: str
    index_registry_key: str
    index_entry_hash: str
    registry_mode: str
    static_dashboard_published: bool
    index_entry_registered: bool
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
    registry_blockers: list[str]
    registry_warnings: list[str]
    authority: str = "static_publication_index_registry"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_static_publication_index_registry(
    *,
    static_dashboard_surface: Mapping[str, Any],
    publication_context: Mapping[str, Any] | None = None,
) -> QiStaticPublicationIndexRegistry:
    surface = _mapping(static_dashboard_surface)
    ctx = _mapping(publication_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("static_publication_index_enabled") is not True:
        blockers.append("static_publication_index_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if surface.get("surface_status") != "QI_STATIC_DASHBOARD_SURFACE_READY":
        blockers.append("static_dashboard_surface_not_ready")
    if surface.get("dashboard_artifact_ready") is not True:
        blockers.append("dashboard_artifact_not_ready")
    if surface.get("static_html_rendered") is not True:
        blockers.append("static_html_not_rendered")
    if surface.get("js_enabled") is not False:
        blockers.append("js_enabled_not_false")
    if surface.get("external_network_required") is not False:
        blockers.append("external_network_required_not_false")

    source_surface_id = surface.get("surface_id")
    html_artifact_name = surface.get("html_artifact_name")
    html_sha256 = surface.get("html_sha256")
    html_bytes = surface.get("html_bytes")
    try:
        html_bytes_int = int(html_bytes) if html_bytes is not None else None
    except (TypeError, ValueError):
        html_bytes_int = None
        blockers.append("html_bytes_invalid")

    for key, value in {
        "source_surface_id": source_surface_id,
        "html_artifact_name": html_artifact_name,
        "html_sha256": html_sha256,
        "html_bytes": html_bytes_int,
    }.items():
        if value in (None, ""):
            blockers.append(f"{key}_missing")

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
        if surface.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    registry_mode = str(ctx.get("registry_mode", "static_artifact_index"))
    publication_base = str(ctx.get("publication_base", "static/qi-dashboard"))
    artifact_name = str(html_artifact_name or "qi-dashboard-missing.html")
    publication_path = str(ctx.get("publication_path") or f"{publication_base.rstrip('/')}/{artifact_name}")
    publication_uri = str(ctx.get("publication_uri") or f"file://{publication_path}")
    index_registry_key = str(ctx.get("index_registry_key") or f"qi/static-dashboard/{source_surface_id or 'unknown'}")
    index_entry = {
        "source_surface_id": source_surface_id,
        "html_artifact_name": html_artifact_name,
        "html_sha256": html_sha256,
        "html_bytes": html_bytes_int,
        "publication_path": publication_path,
        "publication_uri": publication_uri,
        "index_registry_key": index_registry_key,
        "registry_mode": registry_mode,
    }
    index_entry_hash = _digest(index_entry)
    publication_receipt_id = "qi-static-pub-" + index_entry_hash[:16]
    ready = not blockers
    if ready and not publication_uri.startswith(("file://", "https://", "http://")):
        warnings.append("publication_uri_scheme_unusual")

    return QiStaticPublicationIndexRegistry(
        registry_version="kuuos_runtime_daemon_qi_static_publication_index_registry_v0_1",
        registry_status="QI_STATIC_PUBLICATION_INDEX_REGISTRY_READY" if ready else "QI_STATIC_PUBLICATION_INDEX_REGISTRY_BLOCKED",
        publication_receipt_id=publication_receipt_id,
        source_surface_id=str(source_surface_id) if source_surface_id else None,
        html_artifact_name=str(html_artifact_name) if html_artifact_name else None,
        html_sha256=str(html_sha256) if html_sha256 else None,
        html_bytes=html_bytes_int,
        publication_path=publication_path,
        publication_uri=publication_uri,
        index_registry_key=index_registry_key,
        index_entry_hash=index_entry_hash,
        registry_mode=registry_mode,
        static_dashboard_published=ready,
        index_entry_registered=ready,
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
        registry_blockers=blockers,
        registry_warnings=warnings,
    )
