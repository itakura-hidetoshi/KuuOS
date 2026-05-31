#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiConnectorCaseReceipt:
    receipt_version: str
    receipt_status: str
    receipt_id: str
    source_case_receipt_id: str | None
    incident_id: str | None
    connector_kind: str
    target_repo: str | None
    external_case_title: str
    external_case_body: str
    external_labels: list[str]
    connector_mode: str
    approved: bool
    approved_by: str | None
    idempotency_key: str | None
    connector_gate_satisfied: bool
    external_case_payload_rendered: bool
    connector_call_performed: bool
    external_case_created: bool
    external_case_number: int | None
    external_case_url: str | None
    outbound_delivery_performed: bool
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
    authority: str = "connector_case_adapter"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list_str(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _stable_receipt_id(case_receipt: Mapping[str, Any], ctx: Mapping[str, Any]) -> str:
    material = {
        "source_case_receipt_id": case_receipt.get("receipt_id"),
        "incident_id": case_receipt.get("incident_id"),
        "connector_kind": ctx.get("connector_kind"),
        "target_repo": ctx.get("target_repo"),
        "idempotency_key": case_receipt.get("idempotency_key") or ctx.get("idempotency_key"),
    }
    digest = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return f"qi-connector-case-{digest[:16]}"


def build_qi_connector_case_receipt(
    *,
    approved_case_receipt: Mapping[str, Any],
    connector_context: Mapping[str, Any] | None = None,
) -> QiConnectorCaseReceipt:
    case_receipt = _mapping(approved_case_receipt)
    ctx = _mapping(connector_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if case_receipt.get("receipt_status") != "QI_APPROVED_CASE_OPENER_RECEIPT_READY":
        blockers.append("approved_case_receipt_not_ready")
    if case_receipt.get("case_opened") is not True:
        blockers.append("local_case_not_opened")
    if ctx.get("connector_case_adapter_enabled") is not True:
        blockers.append("connector_case_adapter_enabled_not_true")
    if ctx.get("approved") is not True:
        blockers.append("approved_not_true")
    if not ctx.get("approved_by"):
        blockers.append("approved_by_missing")
    if not (case_receipt.get("idempotency_key") or ctx.get("idempotency_key")):
        blockers.append("idempotency_key_missing")

    connector_kind = str(ctx.get("connector_kind", "github_issue"))
    target_repo = str(ctx.get("target_repo")) if ctx.get("target_repo") is not None else None
    if connector_kind == "github_issue" and not target_repo:
        blockers.append("target_repo_missing")

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

    incident_id = str(case_receipt.get("incident_id")) if case_receipt.get("incident_id") is not None else None
    title = str(ctx.get("external_case_title") or case_receipt.get("case_title") or f"KuuOS Qi external case {incident_id}")
    labels = _list_str(ctx.get("external_labels")) or _list_str(case_receipt.get("case_labels")) or ["kuuos", "qi-jsonl", "external-case"]
    source_receipt_id = str(case_receipt.get("receipt_id")) if case_receipt.get("receipt_id") is not None else None
    body = str(ctx.get("external_case_body") or (
        f"KuuOS Qi connector case\n\n"
        f"Incident: {incident_id}\n"
        f"Source receipt: {source_receipt_id}\n"
        f"Idempotency key: {case_receipt.get('idempotency_key') or ctx.get('idempotency_key')}\n\n"
        "This case was produced by the Qi connector case adapter."
    ))

    connector_call_performed = ctx.get("connector_call_performed") is True
    external_case_number = ctx.get("external_case_number")
    external_case_url = ctx.get("external_case_url")
    if connector_call_performed and external_case_number is None:
        blockers.append("external_case_number_missing")
    if connector_call_performed and not external_case_url:
        blockers.append("external_case_url_missing")

    connector_gate_satisfied = not blockers
    external_case_created = connector_call_performed and connector_gate_satisfied
    outbound_delivery_performed = external_case_created
    receipt_id = _stable_receipt_id(case_receipt, ctx)
    status = "QI_CONNECTOR_CASE_RECEIPT_READY" if connector_gate_satisfied else "QI_CONNECTOR_CASE_RECEIPT_BLOCKED"
    if connector_gate_satisfied and not connector_call_performed:
        warnings.append("payload_ready_connector_call_not_performed")

    return QiConnectorCaseReceipt(
        receipt_version="kuuos_runtime_daemon_qi_connector_case_adapter_v0_1",
        receipt_status=status,
        receipt_id=receipt_id,
        source_case_receipt_id=source_receipt_id,
        incident_id=incident_id,
        connector_kind=connector_kind,
        target_repo=target_repo,
        external_case_title=title,
        external_case_body=body,
        external_labels=labels,
        connector_mode=str(ctx.get("connector_mode", "github_issue_connector")),
        approved=ctx.get("approved") is True,
        approved_by=str(ctx.get("approved_by")) if ctx.get("approved_by") else None,
        idempotency_key=str(case_receipt.get("idempotency_key") or ctx.get("idempotency_key")) if (case_receipt.get("idempotency_key") or ctx.get("idempotency_key")) else None,
        connector_gate_satisfied=connector_gate_satisfied,
        external_case_payload_rendered=True,
        connector_call_performed=connector_call_performed,
        external_case_created=external_case_created,
        external_case_number=int(external_case_number) if external_case_number is not None else None,
        external_case_url=str(external_case_url) if external_case_url else None,
        outbound_delivery_performed=outbound_delivery_performed,
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
