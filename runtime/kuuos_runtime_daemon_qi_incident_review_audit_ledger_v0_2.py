#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiIncidentReviewAuditLedgerResult:
    ledger_version: str
    ledger_status: str
    ledger_path: str
    append_requested: bool
    ledger_append_performed: bool
    prior_entry_count: int
    final_entry_count: int
    prev_entry_digest: str | None
    entry_digest: str | None
    audit_root_digest: str | None
    audit_receipt_id: str | None
    source_alert_packet_id: str | None
    source_metrics_packet_id: str | None
    alert_severity: str | None
    alert_count: int
    append_only_enforced: bool
    read_only_review_receipt: bool
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
    audit_entry: dict[str, Any]
    ledger_blockers: list[str]
    ledger_warnings: list[str]
    authority: str = "qi_incident_review_audit_ledger_append_only"

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


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _entry_digest(entry: Mapping[str, Any]) -> str:
    value = entry.get("entry_digest")
    return str(value) if value else _sha_obj(entry)


def _last_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    return _entry_digest(entries[-1])


def _root_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    return _sha_obj({"entry_digests": [_entry_digest(entry) for entry in entries]})


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
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


def append_qi_incident_review_audit_receipt(
    *,
    alert_policy_packet: Mapping[str, Any],
    ledger_path: str | pathlib.Path,
    ledger_context: Mapping[str, Any] | None = None,
) -> QiIncidentReviewAuditLedgerResult:
    packet = _mapping(alert_policy_packet)
    ctx = _mapping(ledger_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("incident_review_audit_ledger_enabled") is not True:
        blockers.append("incident_review_audit_ledger_enabled_not_true")
    if ctx.get("append_only_required") is not True:
        blockers.append("append_only_required_not_true")
    if ctx.get("read_only_review_required") is not True:
        blockers.append("read_only_review_required_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
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

    if packet.get("alert_policy_status") != "QI_CADENCE_ALERT_POLICY_READY":
        blockers.append("alert_policy_not_ready")
    if packet.get("read_only_incident_surface") is not True:
        blockers.append("incident_surface_not_read_only")
    if packet.get("alert_policy_projection_only") is not True:
        blockers.append("alert_policy_not_projection_only")
    _require_false("alert_policy", packet, blockers)

    incident = _mapping(packet.get("incident_surface"))
    if incident:
        if incident.get("projection_only") is not True:
            blockers.append("incident_surface_not_projection_only")
        _require_false("incident_surface", incident, blockers)
    else:
        warnings.append("incident_surface_missing_optional")

    path = pathlib.Path(ledger_path)
    try:
        existing = _read_jsonl(path)
    except Exception as exc:  # pragma: no cover
        existing = []
        blockers.append("ledger_jsonl_parse_failed")
        warnings.append(str(exc))
    prior_count = len(existing)
    prev_digest = _last_digest(existing)
    material = {
        "entry_kind": "qi_incident_review_audit_receipt_v0_2",
        "source_alert_packet_id": packet.get("alert_packet_id"),
        "source_metrics_packet_id": packet.get("source_metrics_packet_id"),
        "source_finality_packet_id": packet.get("source_finality_packet_id"),
        "alert_severity": packet.get("alert_severity"),
        "alert_count": packet.get("alert_count"),
        "alert_reasons": packet.get("alert_reasons") if isinstance(packet.get("alert_reasons"), list) else [],
        "incident_surface_kind": incident.get("surface_kind"),
        "prev_entry_digest": prev_digest,
        "prior_entry_count": prior_count,
        "append_only": True,
        "read_only_review_receipt": True,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    }
    entry_digest = _sha_obj(material)
    receipt_id = "qi-incident-audit-" + entry_digest[:16]
    audit_entry = dict(material)
    audit_entry.update({
        "audit_receipt_id": receipt_id,
        "entry_digest": entry_digest,
        "ledger_version": "kuuos_runtime_daemon_qi_incident_review_audit_ledger_v0_2",
    })
    append_requested = ctx.get("append_receipt") is not False
    append_performed = False
    if not blockers and append_requested:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(audit_entry, ensure_ascii=False, sort_keys=True) + "\n")
        append_performed = True
    final_entries = _read_jsonl(path) if path.is_file() else existing
    root_digest = _root_digest(final_entries)
    ready = not blockers
    return QiIncidentReviewAuditLedgerResult(
        ledger_version="kuuos_runtime_daemon_qi_incident_review_audit_ledger_v0_2",
        ledger_status="QI_INCIDENT_REVIEW_AUDIT_LEDGER_APPENDED" if ready and append_performed else ("QI_INCIDENT_REVIEW_AUDIT_LEDGER_READY" if ready else "QI_INCIDENT_REVIEW_AUDIT_LEDGER_BLOCKED"),
        ledger_path=str(path),
        append_requested=append_requested,
        ledger_append_performed=append_performed,
        prior_entry_count=prior_count,
        final_entry_count=len(final_entries),
        prev_entry_digest=prev_digest,
        entry_digest=entry_digest if ready else None,
        audit_root_digest=root_digest,
        audit_receipt_id=receipt_id if ready else None,
        source_alert_packet_id=str(packet.get("alert_packet_id")) if packet.get("alert_packet_id") else None,
        source_metrics_packet_id=str(packet.get("source_metrics_packet_id")) if packet.get("source_metrics_packet_id") else None,
        alert_severity=str(packet.get("alert_severity")) if packet.get("alert_severity") else None,
        alert_count=_int(packet.get("alert_count"), 0),
        append_only_enforced=True,
        read_only_review_receipt=True,
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
        audit_entry=audit_entry if ready else {},
        ledger_blockers=blockers,
        ledger_warnings=warnings,
    )
