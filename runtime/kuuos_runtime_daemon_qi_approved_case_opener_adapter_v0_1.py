#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiApprovedCaseOpenerReceipt:
    receipt_version: str
    receipt_status: str
    receipt_id: str
    source_packet_id: str | None
    incident_id: str | None
    case_system: str
    case_title: str
    case_labels: list[str]
    adapter_mode: str
    dry_run: bool
    approved: bool
    approved_by: str | None
    approval_receipt_sha: str | None
    idempotency_key: str | None
    idempotency_key_required: bool
    approval_gate_satisfied: bool
    local_case_receipt_rendered: bool
    case_open_adapter_executed: bool
    case_opened: bool
    outbound_delivery_adapter_executed: bool
    outbound_delivery_performed: bool
    external_api_call_performed: bool
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
    adapter_blockers: list[str]
    adapter_warnings: list[str]
    authority: str = "approved_case_opener_adapter"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list_str(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _stable_receipt_id(packet: Mapping[str, Any], ctx: Mapping[str, Any]) -> str:
    material = {
        "packet_id": packet.get("packet_id"),
        "incident_id": packet.get("incident_id"),
        "idempotency_key": ctx.get("idempotency_key"),
        "approved_by": ctx.get("approved_by"),
        "adapter_mode": ctx.get("adapter_mode"),
    }
    digest = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return f"qi-case-receipt-{digest[:16]}"


def build_qi_approved_case_opener_receipt(
    *,
    review_request_packet: Mapping[str, Any],
    approval_context: Mapping[str, Any] | None = None,
) -> QiApprovedCaseOpenerReceipt:
    packet = _mapping(review_request_packet)
    ctx = _mapping(approval_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if packet.get("packet_status") != "QI_REVIEW_REQUEST_PACKET_READY":
        blockers.append("review_request_packet_not_ready")
    if ctx.get("approved_case_opener_enabled") is not True:
        blockers.append("approved_case_opener_enabled_not_true")
    if ctx.get("idempotency_key_required") is not True:
        blockers.append("idempotency_key_required_not_true")

    dry_run = ctx.get("dry_run") is True
    approved = ctx.get("approved") is True
    approved_by = ctx.get("approved_by")
    approval_receipt_sha = ctx.get("approval_receipt_sha")
    idempotency_key = ctx.get("idempotency_key")
    adapter_mode = str(ctx.get("adapter_mode", "approved_local_case_receipt"))

    if not dry_run:
        if not approved:
            blockers.append("approved_not_true")
        if not approved_by:
            blockers.append("approved_by_missing")
        if not approval_receipt_sha:
            blockers.append("approval_receipt_sha_missing")
    if not idempotency_key:
        blockers.append("idempotency_key_missing")

    for key in (
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

    case_request = _mapping(packet.get("case_open_request"))
    case_system = str(case_request.get("system", ctx.get("case_system", "review-queue")))
    case_title = str(case_request.get("title", f"KuuOS Qi case {packet.get('incident_id', 'unknown')}"))
    case_labels = _list_str(case_request.get("labels")) or ["kuuos", "qi-jsonl", "approved-case"]
    approval_gate_satisfied = not dry_run and approved and bool(approved_by) and bool(approval_receipt_sha) and bool(idempotency_key)
    external_api_call_performed = False

    case_opened = False
    case_open_adapter_executed = False
    if not blockers and approval_gate_satisfied:
        case_open_adapter_executed = True
        case_opened = True
    elif dry_run and not blockers:
        warnings.append("dry_run_no_case_opened")

    receipt_id = _stable_receipt_id(packet, ctx)
    status = "QI_APPROVED_CASE_OPENER_RECEIPT_READY" if not blockers else "QI_APPROVED_CASE_OPENER_RECEIPT_BLOCKED"

    return QiApprovedCaseOpenerReceipt(
        receipt_version="kuuos_runtime_daemon_qi_approved_case_opener_adapter_v0_1",
        receipt_status=status,
        receipt_id=receipt_id,
        source_packet_id=str(packet.get("packet_id")) if packet.get("packet_id") is not None else None,
        incident_id=str(packet.get("incident_id")) if packet.get("incident_id") is not None else None,
        case_system=case_system,
        case_title=case_title,
        case_labels=case_labels,
        adapter_mode=adapter_mode,
        dry_run=dry_run,
        approved=approved,
        approved_by=str(approved_by) if approved_by else None,
        approval_receipt_sha=str(approval_receipt_sha) if approval_receipt_sha else None,
        idempotency_key=str(idempotency_key) if idempotency_key else None,
        idempotency_key_required=ctx.get("idempotency_key_required") is True,
        approval_gate_satisfied=approval_gate_satisfied,
        local_case_receipt_rendered=True,
        case_open_adapter_executed=case_open_adapter_executed,
        case_opened=case_opened,
        outbound_delivery_adapter_executed=False,
        outbound_delivery_performed=False,
        external_api_call_performed=external_api_call_performed,
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
        adapter_blockers=blockers,
        adapter_warnings=warnings,
    )
