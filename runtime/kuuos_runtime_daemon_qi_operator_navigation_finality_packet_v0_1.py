#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiOperatorNavigationFinalityPacket:
    packet_version: str
    finality_status: str
    finality_packet_id: str
    source_smoke_receipt_id: str | None
    source_landing_receipt_id: str | None
    source_catalog_id: str | None
    navigation_landing_key: str | None
    navigation_landing_uri: str | None
    navigation_landing_hash: str | None
    html_artifact_name: str | None
    html_sha256: str | None
    catalog_entry_count: int
    release_marker: str
    release_marker_hash: str
    operator_navigation_final: bool
    release_marker_rendered: bool
    entrypoint_ready_confirmed: bool
    published_landing_confirmed: bool
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
    finality_blockers: list[str]
    finality_warnings: list[str]
    authority: str = "operator_navigation_finality_packet"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_operator_navigation_finality_packet(
    *,
    smoke_receipt: Mapping[str, Any],
    finality_context: Mapping[str, Any] | None = None,
) -> QiOperatorNavigationFinalityPacket:
    smoke = _mapping(smoke_receipt)
    ctx = _mapping(finality_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("operator_navigation_finality_enabled") is not True:
        blockers.append("operator_navigation_finality_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if smoke.get("smoke_status") != "QI_OPERATOR_ENTRYPOINT_SMOKE_RECEIPT_READY":
        blockers.append("smoke_receipt_not_ready")
    if smoke.get("operator_entrypoint_ready") is not True:
        blockers.append("operator_entrypoint_not_ready")
    if smoke.get("published_landing_receipt_ready") is not True:
        blockers.append("published_landing_not_ready")
    if smoke.get("entrypoint_uri_resolved") is not True:
        blockers.append("entrypoint_uri_not_resolved")
    if smoke.get("entrypoint_hash_confirmed") is not True:
        blockers.append("entrypoint_hash_not_confirmed")
    if smoke.get("read_only_surface") is not True:
        blockers.append("smoke_not_read_only")
    if smoke.get("js_enabled") is not False:
        blockers.append("js_enabled_not_false")
    if smoke.get("external_network_required") is not False:
        blockers.append("external_network_required_not_false")

    fields = {
        "source_smoke_receipt_id": smoke.get("smoke_receipt_id"),
        "source_landing_receipt_id": smoke.get("source_landing_receipt_id"),
        "source_catalog_id": smoke.get("source_catalog_id"),
        "navigation_landing_key": smoke.get("navigation_landing_key"),
        "navigation_landing_uri": smoke.get("navigation_landing_uri"),
        "navigation_landing_hash": smoke.get("navigation_landing_hash"),
        "html_artifact_name": smoke.get("html_artifact_name"),
        "html_sha256": smoke.get("html_sha256"),
    }
    for name, value in fields.items():
        if value in (None, ""):
            blockers.append(f"{name}_missing")

    try:
        catalog_entry_count = int(smoke.get("catalog_entry_count", 0) or 0)
    except (TypeError, ValueError):
        catalog_entry_count = 0
        blockers.append("catalog_entry_count_invalid")
    if catalog_entry_count <= 0:
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
        if smoke.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    release_marker = str(ctx.get("release_marker") or "QI_OPERATOR_NAVIGATION_ENTRYPOINT_RELEASED_V0_1")
    marker_material = {
        "release_marker": release_marker,
        "source_smoke_receipt_id": smoke.get("smoke_receipt_id"),
        "navigation_landing_uri": smoke.get("navigation_landing_uri"),
        "navigation_landing_hash": smoke.get("navigation_landing_hash"),
        "html_sha256": smoke.get("html_sha256"),
    }
    release_marker_hash = _digest(marker_material)
    finality_packet_id = "qi-nav-finality-" + release_marker_hash[:16]
    final = not blockers
    if final and catalog_entry_count == 1:
        warnings.append("single_entry_finality")

    return QiOperatorNavigationFinalityPacket(
        packet_version="kuuos_runtime_daemon_qi_operator_navigation_finality_packet_v0_1",
        finality_status="QI_OPERATOR_NAVIGATION_FINALITY_PACKET_READY" if final else "QI_OPERATOR_NAVIGATION_FINALITY_PACKET_BLOCKED",
        finality_packet_id=finality_packet_id,
        source_smoke_receipt_id=str(fields["source_smoke_receipt_id"]) if fields["source_smoke_receipt_id"] else None,
        source_landing_receipt_id=str(fields["source_landing_receipt_id"]) if fields["source_landing_receipt_id"] else None,
        source_catalog_id=str(fields["source_catalog_id"]) if fields["source_catalog_id"] else None,
        navigation_landing_key=str(fields["navigation_landing_key"]) if fields["navigation_landing_key"] else None,
        navigation_landing_uri=str(fields["navigation_landing_uri"]) if fields["navigation_landing_uri"] else None,
        navigation_landing_hash=str(fields["navigation_landing_hash"]) if fields["navigation_landing_hash"] else None,
        html_artifact_name=str(fields["html_artifact_name"]) if fields["html_artifact_name"] else None,
        html_sha256=str(fields["html_sha256"]) if fields["html_sha256"] else None,
        catalog_entry_count=catalog_entry_count,
        release_marker=release_marker,
        release_marker_hash=release_marker_hash,
        operator_navigation_final=final,
        release_marker_rendered=True,
        entrypoint_ready_confirmed=smoke.get("operator_entrypoint_ready") is True,
        published_landing_confirmed=smoke.get("published_landing_receipt_ready") is True,
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
        finality_blockers=blockers,
        finality_warnings=warnings,
    )
