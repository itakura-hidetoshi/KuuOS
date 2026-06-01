#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiOperatorNavigationChainFinalDeclaration:
    declaration_version: str
    declaration_status: str
    declaration_id: str
    source_finality_packet_id: str | None
    source_smoke_receipt_id: str | None
    source_landing_receipt_id: str | None
    source_catalog_id: str | None
    release_marker: str | None
    release_marker_hash: str | None
    navigation_landing_uri: str | None
    navigation_landing_hash: str | None
    html_artifact_name: str | None
    html_sha256: str | None
    catalog_entry_count: int
    chain_finalized: bool
    release_ready_confirmed: bool
    final_declaration_rendered: bool
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
    declaration_blockers: list[str]
    declaration_warnings: list[str]
    authority: str = "operator_navigation_chain_final_declaration"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_operator_navigation_chain_final_declaration(
    *,
    finality_packet: Mapping[str, Any],
    declaration_context: Mapping[str, Any] | None = None,
) -> QiOperatorNavigationChainFinalDeclaration:
    packet = _mapping(finality_packet)
    ctx = _mapping(declaration_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("chain_final_declaration_enabled") is not True:
        blockers.append("chain_final_declaration_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if ctx.get("additive_only_future_required") is not True:
        blockers.append("additive_only_future_required_not_true")
    if packet.get("finality_status") != "QI_OPERATOR_NAVIGATION_FINALITY_PACKET_READY":
        blockers.append("finality_packet_not_ready")
    if packet.get("operator_navigation_final") is not True:
        blockers.append("operator_navigation_final_not_true")
    if packet.get("release_marker_rendered") is not True:
        blockers.append("release_marker_not_rendered")
    if packet.get("entrypoint_ready_confirmed") is not True:
        blockers.append("entrypoint_ready_not_confirmed")
    if packet.get("published_landing_confirmed") is not True:
        blockers.append("published_landing_not_confirmed")
    if packet.get("read_only_surface") is not True:
        blockers.append("finality_packet_not_read_only")
    if packet.get("js_enabled") is not False:
        blockers.append("js_enabled_not_false")
    if packet.get("external_network_required") is not False:
        blockers.append("external_network_required_not_false")

    fields = {
        "source_finality_packet_id": packet.get("finality_packet_id"),
        "source_smoke_receipt_id": packet.get("source_smoke_receipt_id"),
        "source_landing_receipt_id": packet.get("source_landing_receipt_id"),
        "source_catalog_id": packet.get("source_catalog_id"),
        "release_marker": packet.get("release_marker"),
        "release_marker_hash": packet.get("release_marker_hash"),
        "navigation_landing_uri": packet.get("navigation_landing_uri"),
        "navigation_landing_hash": packet.get("navigation_landing_hash"),
        "html_artifact_name": packet.get("html_artifact_name"),
        "html_sha256": packet.get("html_sha256"),
    }
    for name, value in fields.items():
        if value in (None, ""):
            blockers.append(f"{name}_missing")

    try:
        catalog_entry_count = int(packet.get("catalog_entry_count", 0) or 0)
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
        if packet.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    declaration_material = {
        "source_finality_packet_id": packet.get("finality_packet_id"),
        "release_marker_hash": packet.get("release_marker_hash"),
        "navigation_landing_hash": packet.get("navigation_landing_hash"),
        "html_sha256": packet.get("html_sha256"),
        "declaration_name": "QI_DAEMON_OPERATOR_NAVIGATION_CHAIN_FINAL_DECLARATION_V0_1",
    }
    declaration_id = "qi-nav-chain-final-" + _digest(declaration_material)[:16]
    final = not blockers
    if final and catalog_entry_count == 1:
        warnings.append("single_entry_chain_finalized")

    return QiOperatorNavigationChainFinalDeclaration(
        declaration_version="kuuos_runtime_daemon_qi_operator_navigation_chain_final_declaration_v0_1",
        declaration_status="QI_OPERATOR_NAVIGATION_CHAIN_FINAL_DECLARATION_READY" if final else "QI_OPERATOR_NAVIGATION_CHAIN_FINAL_DECLARATION_BLOCKED",
        declaration_id=declaration_id,
        source_finality_packet_id=str(fields["source_finality_packet_id"]) if fields["source_finality_packet_id"] else None,
        source_smoke_receipt_id=str(fields["source_smoke_receipt_id"]) if fields["source_smoke_receipt_id"] else None,
        source_landing_receipt_id=str(fields["source_landing_receipt_id"]) if fields["source_landing_receipt_id"] else None,
        source_catalog_id=str(fields["source_catalog_id"]) if fields["source_catalog_id"] else None,
        release_marker=str(fields["release_marker"]) if fields["release_marker"] else None,
        release_marker_hash=str(fields["release_marker_hash"]) if fields["release_marker_hash"] else None,
        navigation_landing_uri=str(fields["navigation_landing_uri"]) if fields["navigation_landing_uri"] else None,
        navigation_landing_hash=str(fields["navigation_landing_hash"]) if fields["navigation_landing_hash"] else None,
        html_artifact_name=str(fields["html_artifact_name"]) if fields["html_artifact_name"] else None,
        html_sha256=str(fields["html_sha256"]) if fields["html_sha256"] else None,
        catalog_entry_count=catalog_entry_count,
        chain_finalized=final,
        release_ready_confirmed=final,
        final_declaration_rendered=True,
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
        declaration_blockers=blockers,
        declaration_warnings=warnings,
    )
