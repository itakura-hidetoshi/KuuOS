#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


SEVERITY_RANK = {
    "info": 1,
    "warning": 2,
    "critical": 3,
}


@dataclass(frozen=True)
class QiIncidentAlertSummary:
    alert_name: str
    status: str
    severity: str
    authority: str | None
    summary: str | None
    description: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class QiIncidentHandoffPacket:
    packet_version: str
    handoff_status: str
    incident_id: str
    route_key: str
    source_system: str
    alert_count: int
    firing_count: int
    resolved_count: int
    max_severity: str
    manual_review_required: bool
    recommended_action: str
    handoff_mode: str
    alert_summaries: list[dict[str, Any]]
    exporter_status: str | None
    watchdog_exit_code: int | None
    read_only_required: bool
    review_only_required: bool
    incident_handoff_packet_rendered: bool
    external_notification_send_performed: bool
    alertmanager_mutation_performed: bool
    ticket_created: bool
    pagerduty_triggered: bool
    slack_message_sent: bool
    email_sent: bool
    webhook_called: bool
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
    handoff_blockers: list[str]
    handoff_warnings: list[str]
    authority: str = "incident_handoff_review_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _str_or_none(value: Any) -> str | None:
    return str(value) if value is not None else None


def _severity_max(values: list[str]) -> str:
    if not values:
        return "info"
    return max(values, key=lambda item: SEVERITY_RANK.get(item, 0))


def _stable_incident_id(payload: Mapping[str, Any], summaries: list[QiIncidentAlertSummary]) -> str:
    material = {
        "receiver": payload.get("receiver"),
        "group_key": payload.get("groupKey"),
        "alerts": [summary.to_dict() for summary in summaries],
    }
    digest = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return f"qi-incident-{digest[:16]}"


def _summarize_alerts(payload: Mapping[str, Any]) -> list[QiIncidentAlertSummary]:
    summaries: list[QiIncidentAlertSummary] = []
    for item in _list(payload.get("alerts")):
        alert = _mapping(item)
        labels = _mapping(alert.get("labels"))
        annotations = _mapping(alert.get("annotations"))
        summaries.append(
            QiIncidentAlertSummary(
                alert_name=str(labels.get("alertname", "unknown_alert")),
                status=str(alert.get("status", payload.get("status", "unknown"))),
                severity=str(labels.get("severity", "info")),
                authority=_str_or_none(labels.get("authority")),
                summary=_str_or_none(annotations.get("summary")),
                description=_str_or_none(annotations.get("description")),
            )
        )
    return summaries


def build_qi_incident_handoff_packet(
    *,
    alertmanager_payload: Mapping[str, Any],
    exporter_snapshot: Mapping[str, Any] | None = None,
    handoff_context: Mapping[str, Any] | None = None,
) -> QiIncidentHandoffPacket:
    ctx = _mapping(handoff_context)
    payload = _mapping(alertmanager_payload)
    exporter = _mapping(exporter_snapshot)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("review_only_required") is not True:
        blockers.append("review_only_required_not_true")
    if ctx.get("incident_handoff_enabled") is not True:
        blockers.append("incident_handoff_enabled_not_true")

    for key in (
        "request_external_notification_send",
        "request_ticket_create",
        "request_pagerduty_trigger",
        "request_slack_message",
        "request_email_send",
        "request_webhook_call",
        "request_daemon_restart",
        "request_daemon_stop",
        "request_daemon_resume",
        "request_probe_execution",
        "request_world_update",
        "request_memory_write",
        "request_control_packet_mutation",
        "request_auto_remediation",
    ):
        if ctx.get(key) is True:
            blockers.append(key)

    summaries = _summarize_alerts(payload)
    if not summaries:
        blockers.append("alerts_missing")

    severities = [summary.severity for summary in summaries]
    max_severity = _severity_max(severities)
    firing_count = sum(1 for summary in summaries if summary.status == "firing")
    resolved_count = sum(1 for summary in summaries if summary.status == "resolved")
    if any(summary.authority not in (None, "read_only_alert") for summary in summaries):
        warnings.append("non_read_only_alert_authority_label")

    watchdog_exit_code_value = exporter.get("watchdog_exit_code")
    try:
        watchdog_exit_code = int(watchdog_exit_code_value) if watchdog_exit_code_value is not None else None
    except (TypeError, ValueError):
        watchdog_exit_code = None
        warnings.append("watchdog_exit_code_non_integer")

    manual_review_required = firing_count > 0 or max_severity in ("warning", "critical") or watchdog_exit_code in (1, 2)
    if max_severity == "critical" or watchdog_exit_code == 2:
        recommended_action = "manual_incident_review_required"
    elif manual_review_required:
        recommended_action = "manual_review_recommended"
    else:
        recommended_action = "observe_only"

    incident_id = _stable_incident_id(payload, summaries)
    route_key = str(ctx.get("route_key", payload.get("receiver", "qi-jsonl-review")))
    source_system = str(ctx.get("source_system", "prometheus_alertmanager"))
    handoff_ok = not blockers

    return QiIncidentHandoffPacket(
        packet_version="kuuos_runtime_daemon_qi_incident_handoff_packet_v0_1",
        handoff_status="QI_INCIDENT_HANDOFF_PACKET_READY" if handoff_ok else "QI_INCIDENT_HANDOFF_PACKET_BLOCKED",
        incident_id=incident_id,
        route_key=route_key,
        source_system=source_system,
        alert_count=len(summaries),
        firing_count=firing_count,
        resolved_count=resolved_count,
        max_severity=max_severity,
        manual_review_required=manual_review_required,
        recommended_action=recommended_action,
        handoff_mode="review_only_packet",
        alert_summaries=[summary.to_dict() for summary in summaries],
        exporter_status=_str_or_none(exporter.get("exporter_status")),
        watchdog_exit_code=watchdog_exit_code,
        read_only_required=ctx.get("read_only_required") is True,
        review_only_required=ctx.get("review_only_required") is True,
        incident_handoff_packet_rendered=True,
        external_notification_send_performed=False,
        alertmanager_mutation_performed=False,
        ticket_created=False,
        pagerduty_triggered=False,
        slack_message_sent=False,
        email_sent=False,
        webhook_called=False,
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
        handoff_blockers=blockers,
        handoff_warnings=warnings,
    )
