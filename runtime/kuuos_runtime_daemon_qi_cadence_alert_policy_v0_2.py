#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiCadenceAlertPolicyResult:
    alert_policy_version: str
    alert_policy_status: str
    alert_packet_id: str
    source_metrics_packet_id: str | None
    source_finality_packet_id: str | None
    alert_severity: str
    alert_count: int
    alert_reasons: list[str]
    incident_surface: dict[str, Any]
    read_only_incident_surface: bool
    alert_policy_projection_only: bool
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
    alert_packet: dict[str, Any]
    alert_blockers: list[str]
    alert_warnings: list[str]
    authority: str = "qi_cadence_alert_policy_read_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "runtime_control_authority",
        "scheduler_bypass_performed",
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _severity(reasons: list[str]) -> str:
    critical = {"scheduler_bypass_detected", "memory_write_detected", "world_update_detected", "probe_execution_detected"}
    high = {"finality_not_confirmed", "canonical_chain_incomplete", "no_authority_boundary_missing"}
    if any(item in critical for item in reasons):
        return "critical"
    if any(item in high for item in reasons):
        return "high"
    if reasons:
        return "medium"
    return "none"


def build_qi_cadence_alert_policy(
    *,
    observability_packet: Mapping[str, Any],
    alert_context: Mapping[str, Any] | None = None,
) -> QiCadenceAlertPolicyResult:
    packet = _mapping(observability_packet)
    ctx = _mapping(alert_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("cadence_alert_policy_enabled") is not True:
        blockers.append("cadence_alert_policy_enabled_not_true")
    if ctx.get("read_only_incident_surface_required") is not True:
        blockers.append("read_only_incident_surface_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
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

    if packet.get("observability_status") != "QI_CADENCE_OBSERVABILITY_PROJECTION_READY":
        blockers.append("observability_projection_not_ready")
    if packet.get("projection_only") is not True:
        blockers.append("observability_not_projection_only")
    if packet.get("dashboard_projection_only") is not True:
        blockers.append("dashboard_not_projection_only")
    _require_false("observability", packet, blockers)

    reasons: list[str] = []
    if _int(packet.get("finality_confirmed_gauge"), 0) != 1:
        reasons.append("finality_not_confirmed")
    if _int(packet.get("canonical_chain_complete_gauge"), 0) != 1:
        reasons.append("canonical_chain_incomplete")
    if _int(packet.get("no_authority_boundary_gauge"), 0) != 1:
        reasons.append("no_authority_boundary_missing")
    if _int(packet.get("scheduler_bypass_gauge"), 0) != 0:
        reasons.append("scheduler_bypass_detected")
    if _int(packet.get("memory_write_gauge"), 0) != 0:
        reasons.append("memory_write_detected")
    if _int(packet.get("memory_append_gauge"), 0) != 0:
        reasons.append("memory_append_detected")
    if _int(packet.get("world_update_gauge"), 0) != 0:
        reasons.append("world_update_detected")
    if _int(packet.get("probe_execution_gauge"), 0) != 0:
        reasons.append("probe_execution_detected")

    severity = _severity(reasons)
    core = {
        "source_metrics_packet_id": packet.get("metrics_packet_id"),
        "source_finality_packet_id": packet.get("source_finality_packet_id"),
        "alert_severity": severity,
        "alert_reasons": reasons,
        "read_only": True,
    }
    alert_packet_id = "qi-cadence-alert-" + _sha_obj(core)[:16]
    incident_surface = {
        "surface_kind": "qi_cadence_read_only_incident_surface_v0_2",
        "alert_packet_id": alert_packet_id,
        "severity": severity,
        "reasons": reasons,
        "recommended_review_surfaces": [
            "cadence_finality_packet",
            "cadence_observability_projection",
            "governance_validation_runs",
        ] if reasons else [],
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "projection_only": True,
    }
    alert_packet = dict(core)
    alert_packet.update({
        "alert_packet_id": alert_packet_id,
        "alert_policy_version": "kuuos_runtime_daemon_qi_cadence_alert_policy_v0_2",
        "alert_policy_status": "QI_CADENCE_ALERT_POLICY_READY" if not blockers else "QI_CADENCE_ALERT_POLICY_BLOCKED",
        "incident_surface": incident_surface,
        "read_only_incident_surface": True,
        "alert_policy_projection_only": True,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })
    ready = not blockers
    return QiCadenceAlertPolicyResult(
        alert_policy_version="kuuos_runtime_daemon_qi_cadence_alert_policy_v0_2",
        alert_policy_status="QI_CADENCE_ALERT_POLICY_READY" if ready else "QI_CADENCE_ALERT_POLICY_BLOCKED",
        alert_packet_id=alert_packet_id,
        source_metrics_packet_id=str(packet.get("metrics_packet_id")) if packet.get("metrics_packet_id") else None,
        source_finality_packet_id=str(packet.get("source_finality_packet_id")) if packet.get("source_finality_packet_id") else None,
        alert_severity=severity,
        alert_count=len(reasons),
        alert_reasons=reasons,
        incident_surface=incident_surface if ready else {},
        read_only_incident_surface=True,
        alert_policy_projection_only=True,
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
        alert_packet=alert_packet if ready else {},
        alert_blockers=blockers,
        alert_warnings=warnings,
    )
