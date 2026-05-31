#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiCBFResultArchiveReceipt:
    receipt_version: str
    archive_status: str
    archive_receipt_id: str
    source_cbf_certificate_id: str | None
    source_connector_receipt_id: str | None
    incident_id: str | None
    external_case_number: int | None
    external_case_url: str | None
    cbf_ok: bool
    cbf_margin_min: float | None
    cbf_barrier_count: int
    cbf_barrier_digest: str
    archive_key: str
    archive_mode: str
    archive_record_hash: str
    append_only_required: bool
    archive_receipt_rendered: bool
    live_result_archived: bool
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
    archive_blockers: list[str]
    archive_warnings: list[str]
    authority: str = "cbf_result_archive_receipt"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _barriers_digest(cbf_certificate: Mapping[str, Any]) -> str:
    barriers = cbf_certificate.get("cbf_barriers", [])
    material = barriers if isinstance(barriers, list) else []
    return hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _record_hash(record: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(record), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_cbf_result_archive_receipt(
    *,
    cbf_certificate: Mapping[str, Any],
    archive_context: Mapping[str, Any] | None = None,
) -> QiCBFResultArchiveReceipt:
    cert = _mapping(cbf_certificate)
    ctx = _mapping(archive_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("cbf_result_archive_enabled") is not True:
        blockers.append("cbf_result_archive_enabled_not_true")
    if ctx.get("append_only_required") is not True:
        blockers.append("append_only_required_not_true")
    if cert.get("certificate_status") != "QI_CONNECTOR_CBF_GATE_CERTIFICATE_READY":
        blockers.append("cbf_certificate_not_ready")
    if cert.get("cbf_ok") is not True:
        blockers.append("cbf_ok_not_true")
    if cert.get("connector_result_ingested") is not True:
        blockers.append("connector_result_not_ingested")

    external_case_number = cert.get("external_case_number")
    try:
        external_case_number_int = int(external_case_number) if external_case_number is not None else None
    except (TypeError, ValueError):
        external_case_number_int = None
        blockers.append("external_case_number_invalid")
    external_case_url = cert.get("external_case_url")
    if external_case_number_int is None:
        blockers.append("external_case_number_missing")
    if not external_case_url:
        blockers.append("external_case_url_missing")

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
    for flag in forbidden_flags:
        if cert.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    source_cbf_certificate_id = cert.get("certificate_id")
    source_connector_receipt_id = cert.get("source_connector_receipt_id")
    incident_id = cert.get("incident_id")
    barrier_digest = _barriers_digest(cert)
    barriers = cert.get("cbf_barriers", [])
    barrier_count = len(barriers) if isinstance(barriers, list) else 0
    cbf_margin = cert.get("cbf_margin_min")
    try:
        cbf_margin_float = float(cbf_margin) if cbf_margin is not None else None
    except (TypeError, ValueError):
        cbf_margin_float = None
        blockers.append("cbf_margin_invalid")

    archive_mode = str(ctx.get("archive_mode", "append_only_receipt"))
    archive_key = str(ctx.get("archive_key") or f"qi/cbf-result/{source_cbf_certificate_id or 'unknown'}")
    archive_record = {
        "source_cbf_certificate_id": source_cbf_certificate_id,
        "source_connector_receipt_id": source_connector_receipt_id,
        "incident_id": incident_id,
        "external_case_number": external_case_number_int,
        "external_case_url": external_case_url,
        "cbf_ok": cert.get("cbf_ok") is True,
        "cbf_margin_min": cbf_margin_float,
        "cbf_barrier_digest": barrier_digest,
        "archive_key": archive_key,
        "archive_mode": archive_mode,
    }
    record_hash = _record_hash(archive_record)
    receipt_material = {"archive_record_hash": record_hash, "archive_key": archive_key}
    archive_receipt_id = "qi-cbf-archive-" + hashlib.sha256(json.dumps(receipt_material, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    archived = not blockers
    if archived and cbf_margin_float == 0:
        warnings.append("zero_margin_archive")

    return QiCBFResultArchiveReceipt(
        receipt_version="kuuos_runtime_daemon_qi_cbf_result_archive_receipt_v0_1",
        archive_status="QI_CBF_RESULT_ARCHIVE_RECEIPT_READY" if archived else "QI_CBF_RESULT_ARCHIVE_RECEIPT_BLOCKED",
        archive_receipt_id=archive_receipt_id,
        source_cbf_certificate_id=str(source_cbf_certificate_id) if source_cbf_certificate_id is not None else None,
        source_connector_receipt_id=str(source_connector_receipt_id) if source_connector_receipt_id is not None else None,
        incident_id=str(incident_id) if incident_id is not None else None,
        external_case_number=external_case_number_int,
        external_case_url=str(external_case_url) if external_case_url else None,
        cbf_ok=cert.get("cbf_ok") is True,
        cbf_margin_min=cbf_margin_float,
        cbf_barrier_count=barrier_count,
        cbf_barrier_digest=barrier_digest,
        archive_key=archive_key,
        archive_mode=archive_mode,
        archive_record_hash=record_hash,
        append_only_required=ctx.get("append_only_required") is True,
        archive_receipt_rendered=True,
        live_result_archived=archived,
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
        archive_blockers=blockers,
        archive_warnings=warnings,
    )
