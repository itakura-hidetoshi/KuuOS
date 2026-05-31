#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiLiveReceiptIngestion:
    receipt_version: str
    ingestion_status: str
    ingestion_receipt_id: str
    source_archive_receipt_id: str | None
    source_cbf_certificate_id: str | None
    incident_id: str | None
    external_case_number: int | None
    external_case_url: str | None
    live_result_archived: bool
    archive_record_hash: str | None
    archive_key: str | None
    ingestion_mode: str
    idempotency_key: str | None
    idempotency_digest: str
    live_receipt_ingested: bool
    connector_executor_performed: bool
    connector_executor_result_ingested: bool
    external_result_confirmed: bool
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
    ingestion_blockers: list[str]
    ingestion_warnings: list[str]
    authority: str = "live_receipt_ingestion"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_live_receipt_ingestion(
    *,
    archive_receipt: Mapping[str, Any],
    ingestion_context: Mapping[str, Any] | None = None,
) -> QiLiveReceiptIngestion:
    receipt = _mapping(archive_receipt)
    ctx = _mapping(ingestion_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("live_receipt_ingestion_enabled") is not True:
        blockers.append("live_receipt_ingestion_enabled_not_true")
    if receipt.get("archive_status") != "QI_CBF_RESULT_ARCHIVE_RECEIPT_READY":
        blockers.append("archive_receipt_not_ready")
    if receipt.get("live_result_archived") is not True:
        blockers.append("live_result_archived_not_true")

    external_case_number = receipt.get("external_case_number")
    try:
        external_case_number_int = int(external_case_number) if external_case_number is not None else None
    except (TypeError, ValueError):
        external_case_number_int = None
        blockers.append("external_case_number_invalid")
    external_case_url = receipt.get("external_case_url")
    if external_case_number_int is None:
        blockers.append("external_case_number_missing")
    if not external_case_url:
        blockers.append("external_case_url_missing")

    archive_record_hash = receipt.get("archive_record_hash")
    if not archive_record_hash:
        blockers.append("archive_record_hash_missing")
    archive_key = receipt.get("archive_key")
    if not archive_key:
        blockers.append("archive_key_missing")

    idempotency_key = ctx.get("idempotency_key") or receipt.get("archive_record_hash") or receipt.get("archive_receipt_id")
    if not idempotency_key:
        blockers.append("idempotency_key_missing")
    idempotency_payload = {
        "source_archive_receipt_id": receipt.get("archive_receipt_id"),
        "archive_record_hash": archive_record_hash,
        "external_case_number": external_case_number_int,
        "external_case_url": external_case_url,
        "idempotency_key": idempotency_key,
    }
    idempotency_digest = _digest(idempotency_payload)

    executor_performed = ctx.get("connector_executor_performed") is True
    external_result_confirmed = ctx.get("external_result_confirmed") is True
    if executor_performed and not external_result_confirmed:
        warnings.append("executor_performed_without_external_result_confirmation")

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
        if receipt.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    live_ingested = not blockers
    ingestion_material = {
        "archive_receipt_id": receipt.get("archive_receipt_id"),
        "source_cbf_certificate_id": receipt.get("source_cbf_certificate_id"),
        "incident_id": receipt.get("incident_id"),
        "external_case_number": external_case_number_int,
        "external_case_url": external_case_url,
        "idempotency_digest": idempotency_digest,
    }
    ingestion_receipt_id = "qi-live-ingest-" + _digest(ingestion_material)[:16]

    return QiLiveReceiptIngestion(
        receipt_version="kuuos_runtime_daemon_qi_live_receipt_ingestion_v0_1",
        ingestion_status="QI_LIVE_RECEIPT_INGESTION_READY" if live_ingested else "QI_LIVE_RECEIPT_INGESTION_BLOCKED",
        ingestion_receipt_id=ingestion_receipt_id,
        source_archive_receipt_id=str(receipt.get("archive_receipt_id")) if receipt.get("archive_receipt_id") is not None else None,
        source_cbf_certificate_id=str(receipt.get("source_cbf_certificate_id")) if receipt.get("source_cbf_certificate_id") is not None else None,
        incident_id=str(receipt.get("incident_id")) if receipt.get("incident_id") is not None else None,
        external_case_number=external_case_number_int,
        external_case_url=str(external_case_url) if external_case_url else None,
        live_result_archived=receipt.get("live_result_archived") is True,
        archive_record_hash=str(archive_record_hash) if archive_record_hash else None,
        archive_key=str(archive_key) if archive_key else None,
        ingestion_mode=str(ctx.get("ingestion_mode", "live_result_receipt_ingestion")),
        idempotency_key=str(idempotency_key) if idempotency_key else None,
        idempotency_digest=idempotency_digest,
        live_receipt_ingested=live_ingested,
        connector_executor_performed=executor_performed,
        connector_executor_result_ingested=live_ingested and executor_performed,
        external_result_confirmed=external_result_confirmed,
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
        ingestion_blockers=blockers,
        ingestion_warnings=warnings,
    )
