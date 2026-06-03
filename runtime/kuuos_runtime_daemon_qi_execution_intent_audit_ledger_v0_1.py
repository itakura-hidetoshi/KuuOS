#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiExecutionIntentAuditLedgerResult:
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
    execution_audit_receipt_id: str | None
    source_engine_packet_id: str | None
    selected_action: str | None
    execution_mode: str | None
    execution_intent_staged: bool
    execution_committed: bool
    selected_reason: str | None
    append_only_enforced: bool
    intent_receipt_only: bool
    read_only_receipt: bool
    projection_only_receipt: bool
    runtime_control_performed: bool
    scheduler_bypass_performed: bool
    notification_sent: bool
    ticket_created: bool
    handover_performed: bool
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
    authority: str = "qi_execution_intent_audit_ledger_append_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


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
    return _entry_digest(entries[-1]) if entries else None


def _root_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    return _sha_obj({"entry_digests": [_entry_digest(entry) for entry in entries]})


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "execution_committed",
        "runtime_control_performed",
        "scheduler_bypass_performed",
        "notification_sent",
        "ticket_created",
        "handover_performed",
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


def append_qi_execution_intent_audit_receipt(
    *,
    engine_packet: Mapping[str, Any],
    ledger_path: str | pathlib.Path,
    ledger_context: Mapping[str, Any] | None = None,
) -> QiExecutionIntentAuditLedgerResult:
    packet = _mapping(engine_packet)
    ctx = _mapping(ledger_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("execution_intent_audit_ledger_enabled") is not True:
        blockers.append("execution_intent_audit_ledger_enabled_not_true")
    if ctx.get("append_only_required") is not True:
        blockers.append("append_only_required_not_true")
    if ctx.get("intent_receipt_only_required") is not True:
        blockers.append("intent_receipt_only_required_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("request_runtime_control") is True:
        blockers.append("runtime_control_requested")
    if ctx.get("request_scheduler_bypass") is True:
        blockers.append("scheduler_bypass_requested")
    if ctx.get("request_notification_send") is True:
        blockers.append("notification_send_requested")
    if ctx.get("request_ticket_create") is True:
        blockers.append("ticket_create_requested")
    if ctx.get("request_handover_perform") is True:
        blockers.append("handover_perform_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if packet.get("engine_status") != "QI_AUTONOMOUS_EXECUTION_ENGINE_READY":
        blockers.append("engine_not_ready")
    if packet.get("receipt_only") is not True:
        blockers.append("engine_not_receipt_only")
    if packet.get("read_only") is not True:
        blockers.append("engine_not_read_only")
    if packet.get("projection_only") is not True:
        blockers.append("engine_not_projection_only")
    _require_false("engine", packet, blockers)

    intent = _mapping(packet.get("execution_intent_packet"))
    if intent:
        if intent.get("receipt_only") is not True:
            blockers.append("intent_not_receipt_only")
        if intent.get("read_only") is not True:
            blockers.append("intent_not_read_only")
        if intent.get("projection_only") is not True:
            blockers.append("intent_not_projection_only")
        _require_false("intent", intent, blockers)
    else:
        warnings.append("execution_intent_packet_missing_optional")

    path = pathlib.Path(ledger_path)
    try:
        existing = _read_jsonl(path)
    except Exception as exc:  # pragma: no cover
        existing = []
        blockers.append("execution_audit_ledger_parse_failed")
        warnings.append(str(exc))
    prior_count = len(existing)
    prev_digest = _last_digest(existing)
    material = {
        "entry_kind": "qi_execution_intent_audit_receipt_v0_1",
        "source_engine_packet_id": packet.get("engine_packet_id"),
        "selected_action": packet.get("selected_action"),
        "execution_mode": packet.get("execution_mode"),
        "execution_intent_staged": packet.get("execution_intent_staged") is True,
        "execution_committed": False,
        "selected_reason": packet.get("selected_reason"),
        "process_tensor_guard_passed": packet.get("process_tensor_guard_passed") is True,
        "decisionos_guard_passed": packet.get("decisionos_guard_passed") is True,
        "cbf_guard_passed": packet.get("cbf_guard_passed") is True,
        "token_guard_passed": packet.get("token_guard_passed") is True,
        "authority_guard_passed": packet.get("authority_guard_passed") is True,
        "recovery_guard_passed": packet.get("recovery_guard_passed") is True,
        "nonmarkov_guard_passed": packet.get("nonmarkov_guard_passed") is True,
        "prev_entry_digest": prev_digest,
        "prior_entry_count": prior_count,
        "append_only": True,
        "intent_receipt_only": True,
        "read_only_receipt": True,
        "projection_only_receipt": True,
        "runtime_control_performed": False,
        "scheduler_bypass_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "handover_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    }
    entry_digest = _sha_obj(material)
    receipt_id = "qi-exec-audit-" + entry_digest[:16]
    audit_entry = dict(material)
    audit_entry.update({
        "execution_audit_receipt_id": receipt_id,
        "entry_digest": entry_digest,
        "ledger_version": "kuuos_runtime_daemon_qi_execution_intent_audit_ledger_v0_1",
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
    return QiExecutionIntentAuditLedgerResult(
        ledger_version="kuuos_runtime_daemon_qi_execution_intent_audit_ledger_v0_1",
        ledger_status="QI_EXECUTION_INTENT_AUDIT_LEDGER_APPENDED" if ready and append_performed else ("QI_EXECUTION_INTENT_AUDIT_LEDGER_READY" if ready else "QI_EXECUTION_INTENT_AUDIT_LEDGER_BLOCKED"),
        ledger_path=str(path),
        append_requested=append_requested,
        ledger_append_performed=append_performed,
        prior_entry_count=prior_count,
        final_entry_count=len(final_entries),
        prev_entry_digest=prev_digest,
        entry_digest=entry_digest if ready else None,
        audit_root_digest=root_digest,
        execution_audit_receipt_id=receipt_id if ready else None,
        source_engine_packet_id=str(packet.get("engine_packet_id")) if packet.get("engine_packet_id") else None,
        selected_action=str(packet.get("selected_action")) if packet.get("selected_action") else None,
        execution_mode=str(packet.get("execution_mode")) if packet.get("execution_mode") else None,
        execution_intent_staged=packet.get("execution_intent_staged") is True,
        execution_committed=False,
        selected_reason=str(packet.get("selected_reason")) if packet.get("selected_reason") else None,
        append_only_enforced=True,
        intent_receipt_only=True,
        read_only_receipt=True,
        projection_only_receipt=True,
        runtime_control_performed=False,
        scheduler_bypass_performed=False,
        notification_sent=False,
        ticket_created=False,
        handover_performed=False,
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
