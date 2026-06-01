#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiOperatorSurfaceBaselineEstablishedPacket:
    packet_version: str
    established_status: str
    established_packet_id: str
    source_declaration_id: str | None
    source_finality_packet_id: str | None
    source_catalog_id: str | None
    release_marker: str | None
    release_marker_hash: str | None
    navigation_landing_uri: str | None
    navigation_landing_hash: str | None
    html_artifact_name: str | None
    html_sha256: str | None
    catalog_entry_count: int
    operator_surface_baseline_established: bool
    navigation_chain_finalized: bool
    release_ready_confirmed: bool
    additive_only_future_required: bool
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
    established_blockers: list[str]
    established_warnings: list[str]
    authority: str = "operator_surface_baseline_established_packet"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_operator_surface_baseline_established_packet(
    *,
    chain_declaration: Mapping[str, Any],
    established_context: Mapping[str, Any] | None = None,
) -> QiOperatorSurfaceBaselineEstablishedPacket:
    declaration = _mapping(chain_declaration)
    ctx = _mapping(established_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("operator_surface_baseline_established_enabled") is not True:
        blockers.append("operator_surface_baseline_established_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if ctx.get("additive_only_future_required") is not True:
        blockers.append("additive_only_future_required_not_true")
    if declaration.get("declaration_status") != "QI_OPERATOR_NAVIGATION_CHAIN_FINAL_DECLARATION_READY":
        blockers.append("chain_declaration_not_ready")
    if declaration.get("chain_finalized") is not True:
        blockers.append("chain_finalized_not_true")
    if declaration.get("release_ready_confirmed") is not True:
        blockers.append("release_ready_not_confirmed")
    if declaration.get("final_declaration_rendered") is not True:
        blockers.append("final_declaration_not_rendered")
    if declaration.get("additive_only_future_required") is not True:
        blockers.append("source_additive_only_not_true")
    if declaration.get("read_only_surface") is not True:
        blockers.append("source_not_read_only")
    if declaration.get("js_enabled") is not False:
        blockers.append("js_enabled_not_false")
    if declaration.get("external_network_required") is not False:
        blockers.append("external_network_required_not_false")

    fields = {
        "source_declaration_id": declaration.get("declaration_id"),
        "source_finality_packet_id": declaration.get("source_finality_packet_id"),
        "source_catalog_id": declaration.get("source_catalog_id"),
        "release_marker": declaration.get("release_marker"),
        "release_marker_hash": declaration.get("release_marker_hash"),
        "navigation_landing_uri": declaration.get("navigation_landing_uri"),
        "navigation_landing_hash": declaration.get("navigation_landing_hash"),
        "html_artifact_name": declaration.get("html_artifact_name"),
        "html_sha256": declaration.get("html_sha256"),
    }
    for name, value in fields.items():
        if value in (None, ""):
            blockers.append(f"{name}_missing")

    try:
        catalog_entry_count = int(declaration.get("catalog_entry_count", 0) or 0)
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
        if declaration.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    material = {
        "source_declaration_id": declaration.get("declaration_id"),
        "release_marker_hash": declaration.get("release_marker_hash"),
        "navigation_landing_hash": declaration.get("navigation_landing_hash"),
        "html_sha256": declaration.get("html_sha256"),
        "packet_name": "QI_DAEMON_OPERATOR_SURFACE_BASELINE_ESTABLISHED_PACKET_V0_1",
    }
    established_packet_id = "qi-operator-surface-established-" + _digest(material)[:16]
    established = not blockers
    if established and catalog_entry_count == 1:
        warnings.append("single_entry_operator_surface_baseline")

    return QiOperatorSurfaceBaselineEstablishedPacket(
        packet_version="kuuos_runtime_daemon_qi_operator_surface_baseline_established_packet_v0_1",
        established_status="QI_OPERATOR_SURFACE_BASELINE_ESTABLISHED_PACKET_READY" if established else "QI_OPERATOR_SURFACE_BASELINE_ESTABLISHED_PACKET_BLOCKED",
        established_packet_id=established_packet_id,
        source_declaration_id=str(fields["source_declaration_id"]) if fields["source_declaration_id"] else None,
        source_finality_packet_id=str(fields["source_finality_packet_id"]) if fields["source_finality_packet_id"] else None,
        source_catalog_id=str(fields["source_catalog_id"]) if fields["source_catalog_id"] else None,
        release_marker=str(fields["release_marker"]) if fields["release_marker"] else None,
        release_marker_hash=str(fields["release_marker_hash"]) if fields["release_marker_hash"] else None,
        navigation_landing_uri=str(fields["navigation_landing_uri"]) if fields["navigation_landing_uri"] else None,
        navigation_landing_hash=str(fields["navigation_landing_hash"]) if fields["navigation_landing_hash"] else None,
        html_artifact_name=str(fields["html_artifact_name"]) if fields["html_artifact_name"] else None,
        html_sha256=str(fields["html_sha256"]) if fields["html_sha256"] else None,
        catalog_entry_count=catalog_entry_count,
        operator_surface_baseline_established=established,
        navigation_chain_finalized=declaration.get("chain_finalized") is True,
        release_ready_confirmed=declaration.get("release_ready_confirmed") is True,
        additive_only_future_required=ctx.get("additive_only_future_required") is True,
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
        established_blockers=blockers,
        established_warnings=warnings,
    )
