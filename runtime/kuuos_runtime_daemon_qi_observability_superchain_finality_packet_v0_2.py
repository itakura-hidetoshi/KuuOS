#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


OBSERVABILITY_CHAIN = [
    "qi_cadence_observability_projection",
    "qi_cadence_alert_policy",
    "qi_incident_review_audit_ledger",
    "qi_observability_audit_trend_summary",
    "qi_observability_health_baseline_packet",
]


@dataclass(frozen=True)
class QiObservabilitySuperchainFinalityPacketResult:
    finality_version: str
    finality_status: str
    finality_packet_id: str
    finality_root_digest: str
    source_health_baseline_packet_id: str | None
    source_health_baseline_root_digest: str | None
    source_trend_packet_id: str | None
    source_audit_root_digest: str | None
    source_last_entry_digest: str | None
    mean_reliability_score: float
    reliability_class: str | None
    observability_chain_complete: bool
    observability_finality_confirmed: bool
    receipt_only_finality_packet: bool
    read_only_finality_packet: bool
    projection_only: bool
    ledger_append_performed: bool
    notification_sent: bool
    ticket_created: bool
    runtime_control_authority: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    observability_chain: list[str]
    finality_packet: dict[str, Any]
    finality_blockers: list[str]
    finality_warnings: list[str]
    authority: str = "qi_observability_superchain_finality_receipt_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "ledger_append_performed",
        "notification_sent",
        "ticket_created",
        "runtime_control_authority",
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


def build_qi_observability_superchain_finality_packet(
    *,
    health_baseline_packet: Mapping[str, Any],
    finality_context: Mapping[str, Any] | None = None,
) -> QiObservabilitySuperchainFinalityPacketResult:
    health = _mapping(health_baseline_packet)
    ctx = _mapping(finality_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("observability_superchain_finality_enabled") is not True:
        blockers.append("observability_superchain_finality_enabled_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    if ctx.get("request_ledger_append") is True:
        blockers.append("ledger_append_requested")
    if ctx.get("request_notification_send") is True:
        blockers.append("notification_send_requested")
    if ctx.get("request_ticket_create") is True:
        blockers.append("ticket_create_requested")
    if ctx.get("request_runtime_control") is True:
        blockers.append("runtime_control_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if health.get("health_baseline_status") != "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_READY":
        blockers.append("health_baseline_not_ready")
    if health.get("observability_health_confirmed") is not True:
        blockers.append("observability_health_not_confirmed")
    if health.get("confirmed_observability_packet") is not True:
        blockers.append("confirmed_observability_packet_not_true")
    if health.get("receipt_only_health_baseline") is not True:
        blockers.append("health_baseline_not_receipt_only")
    if health.get("read_only_health_baseline") is not True:
        blockers.append("health_baseline_not_read_only")
    if health.get("projection_only") is not True:
        blockers.append("health_baseline_not_projection_only")
    _require_false("health_baseline", health, blockers)

    provided_chain = ctx.get("observability_chain")
    if isinstance(provided_chain, list) and all(isinstance(item, str) for item in provided_chain):
        chain = provided_chain
    else:
        chain = OBSERVABILITY_CHAIN
    chain_complete = all(item in chain for item in OBSERVABILITY_CHAIN)
    if not chain_complete:
        blockers.append("observability_chain_incomplete")

    material = {
        "source_health_baseline_packet_id": health.get("health_baseline_packet_id"),
        "source_health_baseline_root_digest": health.get("health_baseline_root_digest"),
        "source_trend_packet_id": health.get("source_trend_packet_id"),
        "source_audit_root_digest": health.get("source_audit_root_digest"),
        "source_last_entry_digest": health.get("source_last_entry_digest"),
        "mean_reliability_score": health.get("mean_reliability_score"),
        "reliability_class": health.get("reliability_class"),
        "observability_chain": chain,
        "finality_context_id": ctx.get("finality_context_id"),
        "receipt_only": True,
        "read_only": True,
        "projection_only": True,
    }
    root_digest = _sha_obj(material)
    packet_id = "qi-observe-finality-" + root_digest[:16]
    ready = not blockers
    packet = dict(material)
    packet.update({
        "finality_packet_id": packet_id,
        "finality_version": "kuuos_runtime_daemon_qi_observability_superchain_finality_packet_v0_2",
        "finality_status": "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_READY" if ready else "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_BLOCKED",
        "finality_root_digest": root_digest,
        "observability_chain_complete": chain_complete,
        "observability_finality_confirmed": ready,
        "receipt_only_finality_packet": True,
        "read_only_finality_packet": True,
        "projection_only": True,
        "ledger_append_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })

    return QiObservabilitySuperchainFinalityPacketResult(
        finality_version="kuuos_runtime_daemon_qi_observability_superchain_finality_packet_v0_2",
        finality_status="QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_READY" if ready else "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_BLOCKED",
        finality_packet_id=packet_id,
        finality_root_digest=root_digest,
        source_health_baseline_packet_id=str(health.get("health_baseline_packet_id")) if health.get("health_baseline_packet_id") else None,
        source_health_baseline_root_digest=str(health.get("health_baseline_root_digest")) if health.get("health_baseline_root_digest") else None,
        source_trend_packet_id=str(health.get("source_trend_packet_id")) if health.get("source_trend_packet_id") else None,
        source_audit_root_digest=str(health.get("source_audit_root_digest")) if health.get("source_audit_root_digest") else None,
        source_last_entry_digest=str(health.get("source_last_entry_digest")) if health.get("source_last_entry_digest") else None,
        mean_reliability_score=_float(health.get("mean_reliability_score"), 0.0),
        reliability_class=str(health.get("reliability_class")) if health.get("reliability_class") else None,
        observability_chain_complete=chain_complete,
        observability_finality_confirmed=ready,
        receipt_only_finality_packet=True,
        read_only_finality_packet=True,
        projection_only=True,
        ledger_append_performed=False,
        notification_sent=False,
        ticket_created=False,
        runtime_control_authority=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        observability_chain=chain,
        finality_packet=packet if ready else {},
        finality_blockers=blockers,
        finality_warnings=warnings,
    )
