#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiCadenceV02ReleaseEstablishedPacketResult:
    packet_version: str
    packet_status: str
    release_packet_id: str
    release_root_digest: str
    established_packet_id: str
    established_root_digest: str
    source_cadence_finality_packet_id: str | None
    source_cadence_superchain_root_digest: str | None
    source_observability_finality_packet_id: str | None
    source_observability_finality_root_digest: str | None
    v0_2_release_ready: bool
    v0_2_established: bool
    cadence_finality_confirmed: bool
    observability_finality_confirmed: bool
    release_receipt_only: bool
    established_receipt_only: bool
    read_only_release: bool
    projection_only: bool
    ledger_append_performed: bool
    notification_sent: bool
    ticket_created: bool
    runtime_control_authority: bool
    scheduler_bypass_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    release_packet: dict[str, Any]
    established_packet: dict[str, Any]
    release_blockers: list[str]
    release_warnings: list[str]
    authority: str = "qi_cadence_v0_2_release_established_receipt_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "ledger_append_performed",
        "notification_sent",
        "ticket_created",
        "runtime_control_authority",
        "scheduler_bypass_performed",
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_cadence_v0_2_release_established_packet(
    *,
    cadence_finality_packet: Mapping[str, Any],
    observability_finality_packet: Mapping[str, Any],
    release_context: Mapping[str, Any] | None = None,
) -> QiCadenceV02ReleaseEstablishedPacketResult:
    cadence = _mapping(cadence_finality_packet)
    observe = _mapping(observability_finality_packet)
    ctx = _mapping(release_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("qi_cadence_v0_2_release_enabled") is not True:
        blockers.append("qi_cadence_v0_2_release_enabled_not_true")
    if ctx.get("established_packet_required") is not True:
        blockers.append("established_packet_required_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    if ctx.get("request_runtime_control") is True:
        blockers.append("runtime_control_requested")
    if ctx.get("request_scheduler_bypass") is True:
        blockers.append("scheduler_bypass_requested")
    if ctx.get("request_ledger_append") is True:
        blockers.append("ledger_append_requested")
    if ctx.get("request_notification_send") is True:
        blockers.append("notification_send_requested")
    if ctx.get("request_ticket_create") is True:
        blockers.append("ticket_create_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if cadence.get("finality_packet_status") != "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY":
        blockers.append("cadence_finality_not_ready")
    if cadence.get("finality_confirmed") is not True:
        blockers.append("cadence_finality_not_confirmed")
    if cadence.get("receipt_only_finality_packet") is not True:
        blockers.append("cadence_finality_not_receipt_only")
    if cadence.get("canonical_chain_complete") is not True:
        blockers.append("cadence_canonical_chain_not_complete")
    if cadence.get("no_authority_boundary_preserved") is not True:
        blockers.append("cadence_no_authority_boundary_not_preserved")
    _require_false("cadence_finality", cadence, blockers)

    if observe.get("finality_status") != "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_READY":
        blockers.append("observability_finality_not_ready")
    if observe.get("observability_finality_confirmed") is not True:
        blockers.append("observability_finality_not_confirmed")
    if observe.get("receipt_only_finality_packet") is not True:
        blockers.append("observability_finality_not_receipt_only")
    if observe.get("read_only_finality_packet") is not True:
        blockers.append("observability_finality_not_read_only")
    if observe.get("projection_only") is not True:
        blockers.append("observability_finality_not_projection_only")
    if observe.get("observability_chain_complete") is not True:
        blockers.append("observability_chain_not_complete")
    _require_false("observability_finality", observe, blockers)

    material = {
        "cadence_finality_packet_id": cadence.get("finality_packet_id"),
        "cadence_superchain_root_digest": cadence.get("superchain_root_digest"),
        "observability_finality_packet_id": observe.get("finality_packet_id"),
        "observability_finality_root_digest": observe.get("finality_root_digest"),
        "release_context_id": ctx.get("release_context_id"),
        "version": "v0.2",
        "receipt_only": True,
        "read_only": True,
        "projection_only": True,
    }
    release_root = _sha_obj(material)
    release_id = "qi-cadence-v0-2-release-" + release_root[:16]
    established_material = dict(material)
    established_material.update({"release_root_digest": release_root, "established": True})
    established_root = _sha_obj(established_material)
    established_id = "qi-cadence-v0-2-established-" + established_root[:16]
    ready = not blockers

    release_packet = dict(material)
    release_packet.update({
        "release_packet_id": release_id,
        "release_root_digest": release_root,
        "release_version": "kuuos_runtime_daemon_qi_cadence_v0_2_release_established_packet",
        "release_status": "QI_CADENCE_V0_2_RELEASE_PACKET_READY" if ready else "QI_CADENCE_V0_2_RELEASE_PACKET_BLOCKED",
        "v0_2_release_ready": ready,
        "release_receipt_only": True,
        "read_only_release": True,
        "projection_only": True,
        "ledger_append_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })
    established_packet = dict(established_material)
    established_packet.update({
        "established_packet_id": established_id,
        "established_root_digest": established_root,
        "established_status": "QI_CADENCE_V0_2_ESTABLISHED_PACKET_READY" if ready else "QI_CADENCE_V0_2_ESTABLISHED_PACKET_BLOCKED",
        "v0_2_established": ready,
        "established_receipt_only": True,
        "read_only_release": True,
        "projection_only": True,
        "ledger_append_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })

    return QiCadenceV02ReleaseEstablishedPacketResult(
        packet_version="kuuos_runtime_daemon_qi_cadence_v0_2_release_established_packet",
        packet_status="QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_READY" if ready else "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_BLOCKED",
        release_packet_id=release_id,
        release_root_digest=release_root,
        established_packet_id=established_id,
        established_root_digest=established_root,
        source_cadence_finality_packet_id=str(cadence.get("finality_packet_id")) if cadence.get("finality_packet_id") else None,
        source_cadence_superchain_root_digest=str(cadence.get("superchain_root_digest")) if cadence.get("superchain_root_digest") else None,
        source_observability_finality_packet_id=str(observe.get("finality_packet_id")) if observe.get("finality_packet_id") else None,
        source_observability_finality_root_digest=str(observe.get("finality_root_digest")) if observe.get("finality_root_digest") else None,
        v0_2_release_ready=ready,
        v0_2_established=ready,
        cadence_finality_confirmed=cadence.get("finality_confirmed") is True,
        observability_finality_confirmed=observe.get("observability_finality_confirmed") is True,
        release_receipt_only=True,
        established_receipt_only=True,
        read_only_release=True,
        projection_only=True,
        ledger_append_performed=False,
        notification_sent=False,
        ticket_created=False,
        runtime_control_authority=False,
        scheduler_bypass_performed=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        release_packet=release_packet if ready else {},
        established_packet=established_packet if ready else {},
        release_blockers=blockers,
        release_warnings=warnings,
    )
