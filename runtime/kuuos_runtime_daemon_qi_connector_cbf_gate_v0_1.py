#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiConnectorCBFBarrier:
    name: str
    value: float
    threshold: float
    margin: float
    ok: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class QiConnectorCBFGateCertificate:
    certificate_version: str
    certificate_status: str
    certificate_id: str
    source_connector_receipt_id: str | None
    incident_id: str | None
    cbf_ok: bool
    cbf_margin_min: float
    cbf_barriers: list[dict[str, Any]]
    proceed_connector_ingestion: bool
    proceed_reason: str
    connector_result_ingestion_allowed: bool
    connector_result_ingested: bool
    external_case_number: int | None
    external_case_url: str | None
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
    cbf_blockers: list[str]
    cbf_warnings: list[str]
    authority: str = "connector_cbf_gate"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _bool_score(value: bool) -> float:
    return 1.0 if value else -1.0


def _barrier(name: str, value: float, threshold: float = 0.0) -> QiConnectorCBFBarrier:
    margin = float(value) - float(threshold)
    return QiConnectorCBFBarrier(name=name, value=float(value), threshold=float(threshold), margin=margin, ok=margin >= 0.0)


def _stable_certificate_id(connector_receipt: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    material = {
        "source_connector_receipt_id": connector_receipt.get("receipt_id"),
        "incident_id": connector_receipt.get("incident_id"),
        "external_case_number": connector_receipt.get("external_case_number"),
        "external_case_url": connector_receipt.get("external_case_url"),
        "cbf_profile": context.get("cbf_profile"),
    }
    digest = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return f"qi-connector-cbf-{digest[:16]}"


def build_qi_connector_cbf_gate_certificate(
    *,
    connector_receipt: Mapping[str, Any],
    cbf_context: Mapping[str, Any] | None = None,
) -> QiConnectorCBFGateCertificate:
    receipt = _mapping(connector_receipt)
    ctx = _mapping(cbf_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("connector_cbf_gate_enabled") is not True:
        blockers.append("connector_cbf_gate_enabled_not_true")
    if receipt.get("receipt_status") != "QI_CONNECTOR_CASE_RECEIPT_READY":
        blockers.append("connector_receipt_not_ready")

    external_case_number = receipt.get("external_case_number")
    try:
        external_case_number_int = int(external_case_number) if external_case_number is not None else None
    except (TypeError, ValueError):
        external_case_number_int = None
        blockers.append("external_case_number_invalid")

    external_case_url = receipt.get("external_case_url")
    connector_call_performed = receipt.get("connector_call_performed") is True
    external_case_created = receipt.get("external_case_created") is True
    outbound_delivery_performed = receipt.get("outbound_delivery_performed") is True
    idempotency_present = bool(receipt.get("idempotency_key"))
    target_scope_ok = bool(receipt.get("target_repo")) and str(receipt.get("connector_kind")) in {"github_issue", "repository_issue"}
    live_result_present = external_case_number_int is not None and bool(external_case_url)

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
    forbidden_clean = all(receipt.get(flag) is not True for flag in forbidden_flags)

    duplicate_risk_score = float(ctx.get("duplicate_risk_score", 0.0) or 0.0)
    max_duplicate_risk = float(ctx.get("max_duplicate_risk", 0.0) or 0.0)
    scope_risk_score = float(ctx.get("scope_risk_score", 0.0) or 0.0)
    max_scope_risk = float(ctx.get("max_scope_risk", 0.0) or 0.0)

    barriers = [
        _barrier("h_connector_call", _bool_score(connector_call_performed)),
        _barrier("h_external_case_created", _bool_score(external_case_created)),
        _barrier("h_delivery_receipt", _bool_score(outbound_delivery_performed)),
        _barrier("h_live_result_present", _bool_score(live_result_present)),
        _barrier("h_idempotency", _bool_score(idempotency_present)),
        _barrier("h_target_scope", _bool_score(target_scope_ok)),
        _barrier("h_forbidden_clean", _bool_score(forbidden_clean)),
        _barrier("h_duplicate_risk", max_duplicate_risk - duplicate_risk_score),
        _barrier("h_scope_risk", max_scope_risk - scope_risk_score),
    ]
    cbf_margin_min = min((item.margin for item in barriers), default=-1.0)
    cbf_ok = cbf_margin_min >= 0.0 and not blockers
    if not connector_call_performed:
        warnings.append("connector_call_not_performed")
    if not live_result_present:
        warnings.append("live_result_missing")

    proceed = cbf_ok
    proceed_reason = "cbf_all_barriers_nonnegative" if proceed else "cbf_gate_blocked"
    certificate_id = _stable_certificate_id(receipt, ctx)

    return QiConnectorCBFGateCertificate(
        certificate_version="kuuos_runtime_daemon_qi_connector_cbf_gate_v0_1",
        certificate_status="QI_CONNECTOR_CBF_GATE_CERTIFICATE_READY" if not blockers else "QI_CONNECTOR_CBF_GATE_CERTIFICATE_BLOCKED",
        certificate_id=certificate_id,
        source_connector_receipt_id=str(receipt.get("receipt_id")) if receipt.get("receipt_id") is not None else None,
        incident_id=str(receipt.get("incident_id")) if receipt.get("incident_id") is not None else None,
        cbf_ok=cbf_ok,
        cbf_margin_min=cbf_margin_min,
        cbf_barriers=[item.to_dict() for item in barriers],
        proceed_connector_ingestion=proceed,
        proceed_reason=proceed_reason,
        connector_result_ingestion_allowed=proceed,
        connector_result_ingested=proceed,
        external_case_number=external_case_number_int,
        external_case_url=str(external_case_url) if external_case_url else None,
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
        cbf_blockers=blockers,
        cbf_warnings=warnings,
    )
