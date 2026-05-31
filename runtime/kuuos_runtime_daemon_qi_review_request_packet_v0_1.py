#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiReviewRequestPacket:
    packet_version: str
    packet_status: str
    packet_id: str
    incident_id: str
    source_handoff_status: str | None
    max_severity: str
    recommended_action: str | None
    manual_review_required: bool
    request_mode: str
    outbound_review_message_rendered: bool
    case_open_request_rendered: bool
    outbound_review_message: dict[str, Any]
    case_open_request: dict[str, Any]
    read_only_required: bool
    request_packet_only_required: bool
    explicit_delivery_gate_required: bool
    outbound_delivery_performed: bool
    case_opened: bool
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
    packet_blockers: list[str]
    packet_warnings: list[str]
    authority: str = "review_request_packet_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _alert_lines(handoff: Mapping[str, Any]) -> list[str]:
    raw = handoff.get("alert_summaries")
    lines: list[str] = []
    if isinstance(raw, list):
        for item in raw:
            alert = _mapping(item)
            name = str(alert.get("alert_name", "unknown_alert"))
            severity = str(alert.get("severity", "info"))
            status = str(alert.get("status", "unknown"))
            summary = str(alert.get("summary", ""))
            lines.append(f"- [{severity}/{status}] {name}: {summary}")
    return lines or ["- no alert summaries provided"]


def _stable_packet_id(incident_id: str, message: Mapping[str, Any], case_request: Mapping[str, Any]) -> str:
    material = {"incident_id": incident_id, "message": dict(message), "case_request": dict(case_request)}
    digest = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return f"qi-review-request-{digest[:16]}"


def build_qi_review_request_packet(
    *,
    incident_handoff_packet: Mapping[str, Any],
    request_context: Mapping[str, Any] | None = None,
) -> QiReviewRequestPacket:
    ctx = _mapping(request_context)
    handoff = _mapping(incident_handoff_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("request_packet_only_required") is not True:
        blockers.append("request_packet_only_required_not_true")
    if ctx.get("explicit_delivery_gate_required") is not True:
        blockers.append("explicit_delivery_gate_required_not_true")
    if ctx.get("review_request_packet_enabled") is not True:
        blockers.append("review_request_packet_enabled_not_true")

    for key in (
        "perform_outbound_delivery",
        "perform_case_open",
        "perform_daemon_restart",
        "perform_daemon_stop",
        "perform_daemon_resume",
        "perform_probe_execution",
        "perform_world_update",
        "perform_memory_write",
        "perform_control_packet_mutation",
        "perform_auto_remediation",
    ):
        if ctx.get(key) is True:
            blockers.append(key)

    incident_id = str(handoff.get("incident_id", "unknown-incident"))
    handoff_status = handoff.get("handoff_status")
    if handoff_status != "QI_INCIDENT_HANDOFF_PACKET_READY":
        warnings.append("handoff_not_ready")
    severity = str(handoff.get("max_severity", "info"))
    recommended_action = handoff.get("recommended_action")
    manual_review_required = handoff.get("manual_review_required") is True
    alert_text = "\n".join(_alert_lines(handoff))
    subject = f"KuuOS Qi incident review request: {incident_id} ({severity})"
    body = (
        f"Incident: {incident_id}\n"
        f"Severity: {severity}\n"
        f"Recommended action: {recommended_action}\n"
        f"Manual review required: {manual_review_required}\n\n"
        f"Alerts:\n{alert_text}\n\n"
        "Boundary: request packet only. No outbound delivery or case opening has been performed."
    )
    labels = ["kuuos", "qi-jsonl", "incident-review", severity]
    message = {
        "request_type": "outbound_review_message_request",
        "route": str(ctx.get("review_route", "external-review-inbox")),
        "subject": subject,
        "body": body,
        "severity": severity,
        "incident_id": incident_id,
        "delivery_performed": False,
        "delivery_authority_granted": False,
    }
    case_request = {
        "request_type": "case_open_request",
        "system": str(ctx.get("case_system", "review-queue")),
        "title": subject,
        "body": body,
        "severity": severity,
        "incident_id": incident_id,
        "labels": labels,
        "case_opened": False,
        "case_open_authority_granted": False,
    }
    packet_id = _stable_packet_id(incident_id, message, case_request)
    ready = not blockers
    return QiReviewRequestPacket(
        packet_version="kuuos_runtime_daemon_qi_review_request_packet_v0_1",
        packet_status="QI_REVIEW_REQUEST_PACKET_READY" if ready else "QI_REVIEW_REQUEST_PACKET_BLOCKED",
        packet_id=packet_id,
        incident_id=incident_id,
        source_handoff_status=str(handoff_status) if handoff_status is not None else None,
        max_severity=severity,
        recommended_action=str(recommended_action) if recommended_action is not None else None,
        manual_review_required=manual_review_required,
        request_mode="request_packet_only",
        outbound_review_message_rendered=True,
        case_open_request_rendered=True,
        outbound_review_message=message,
        case_open_request=case_request,
        read_only_required=ctx.get("read_only_required") is True,
        request_packet_only_required=ctx.get("request_packet_only_required") is True,
        explicit_delivery_gate_required=ctx.get("explicit_delivery_gate_required") is True,
        outbound_delivery_performed=False,
        case_opened=False,
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
        packet_blockers=blockers,
        packet_warnings=warnings,
    )
