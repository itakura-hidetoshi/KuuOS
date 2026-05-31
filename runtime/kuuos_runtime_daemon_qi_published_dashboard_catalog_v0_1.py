#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiPublishedDashboardCatalog:
    catalog_version: str
    catalog_status: str
    catalog_id: str
    catalog_key: str
    catalog_entry_count: int
    navigation_index_key: str
    navigation_index_hash: str
    latest_publication_receipt_id: str | None
    latest_publication_uri: str | None
    entries: list[dict[str, Any]]
    published_dashboard_catalog_rendered: bool
    operator_navigation_index_rendered: bool
    read_only_surface: bool
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
    catalog_blockers: list[str]
    catalog_warnings: list[str]
    authority: str = "published_dashboard_catalog"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _entry_from_registry(registry: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "publication_receipt_id": registry.get("publication_receipt_id"),
        "source_surface_id": registry.get("source_surface_id"),
        "html_artifact_name": registry.get("html_artifact_name"),
        "html_sha256": registry.get("html_sha256"),
        "html_bytes": registry.get("html_bytes"),
        "publication_path": registry.get("publication_path"),
        "publication_uri": registry.get("publication_uri"),
        "index_registry_key": registry.get("index_registry_key"),
        "index_entry_hash": registry.get("index_entry_hash"),
        "registry_mode": registry.get("registry_mode"),
    }


def build_qi_published_dashboard_catalog(
    *,
    registry_entries: list[Mapping[str, Any]],
    catalog_context: Mapping[str, Any] | None = None,
) -> QiPublishedDashboardCatalog:
    ctx = _mapping(catalog_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("published_dashboard_catalog_enabled") is not True:
        blockers.append("published_dashboard_catalog_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")

    entries: list[dict[str, Any]] = []
    raw_entries = [_mapping(item) for item in registry_entries]
    if not raw_entries:
        blockers.append("registry_entries_missing")
    for idx, registry in enumerate(raw_entries):
        if registry.get("registry_status") != "QI_STATIC_PUBLICATION_INDEX_REGISTRY_READY":
            blockers.append(f"registry_entry_{idx}_not_ready")
        if registry.get("static_dashboard_published") is not True:
            blockers.append(f"registry_entry_{idx}_not_published")
        if registry.get("index_entry_registered") is not True:
            blockers.append(f"registry_entry_{idx}_not_registered")
        if registry.get("js_enabled") is not False:
            blockers.append(f"registry_entry_{idx}_js_enabled")
        if registry.get("external_network_required") is not False:
            blockers.append(f"registry_entry_{idx}_external_network_required")
        for required in ("publication_receipt_id", "publication_uri", "index_entry_hash", "html_sha256"):
            if not registry.get(required):
                blockers.append(f"registry_entry_{idx}_{required}_missing")
        entries.append(_entry_from_registry(registry))

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
    for idx, registry in enumerate(raw_entries):
        for flag in forbidden_flags:
            if registry.get(flag) is True:
                blockers.append(f"registry_entry_{idx}_forbidden_flag_true:{flag}")
    for flag in forbidden_flags:
        if ctx.get(flag) is True:
            blockers.append(f"context_forbidden_flag_true:{flag}")

    entries_sorted = sorted(entries, key=lambda item: str(item.get("publication_receipt_id") or ""))
    catalog_key = str(ctx.get("catalog_key", "qi/published-dashboard/catalog"))
    navigation_index_key = str(ctx.get("navigation_index_key", "qi/published-dashboard/navigation"))
    navigation_material = {
        "catalog_key": catalog_key,
        "navigation_index_key": navigation_index_key,
        "entries": entries_sorted,
    }
    navigation_index_hash = _digest(navigation_material)
    catalog_id = "qi-dashboard-catalog-" + navigation_index_hash[:16]
    latest = entries_sorted[-1] if entries_sorted else {}
    ready = not blockers
    if ready and len(entries_sorted) == 1:
        warnings.append("single_entry_catalog")

    return QiPublishedDashboardCatalog(
        catalog_version="kuuos_runtime_daemon_qi_published_dashboard_catalog_v0_1",
        catalog_status="QI_PUBLISHED_DASHBOARD_CATALOG_READY" if ready else "QI_PUBLISHED_DASHBOARD_CATALOG_BLOCKED",
        catalog_id=catalog_id,
        catalog_key=catalog_key,
        catalog_entry_count=len(entries_sorted),
        navigation_index_key=navigation_index_key,
        navigation_index_hash=navigation_index_hash,
        latest_publication_receipt_id=str(latest.get("publication_receipt_id")) if latest.get("publication_receipt_id") else None,
        latest_publication_uri=str(latest.get("publication_uri")) if latest.get("publication_uri") else None,
        entries=entries_sorted,
        published_dashboard_catalog_rendered=True,
        operator_navigation_index_rendered=True,
        read_only_surface=ctx.get("read_only_surface_required") is True,
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
        catalog_blockers=blockers,
        catalog_warnings=warnings,
    )
