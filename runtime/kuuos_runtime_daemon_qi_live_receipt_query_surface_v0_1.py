#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiLiveReceiptQuerySnapshot:
    snapshot_version: str
    query_status: str
    snapshot_id: str
    source_ingestion_receipt_id: str | None
    incident_id: str | None
    external_case_number: int | None
    external_case_url: str | None
    archive_key: str | None
    archive_record_hash: str | None
    idempotency_digest: str | None
    query_mode: str
    replay_query_key: str
    operator_summary: str
    live_receipt_query_rendered: bool
    replay_packet_rendered: bool
    dashboard_ready: bool
    read_only_surface: bool
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
    query_blockers: list[str]
    query_warnings: list[str]
    authority: str = "live_receipt_query_surface"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_live_receipt_query_snapshot(
    *,
    live_ingestion_receipt: Mapping[str, Any],
    query_context: Mapping[str, Any] | None = None,
) -> QiLiveReceiptQuerySnapshot:
    receipt = _mapping(live_ingestion_receipt)
    ctx = _mapping(query_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("live_receipt_query_enabled") is not True:
        blockers.append("live_receipt_query_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if receipt.get("ingestion_status") != "QI_LIVE_RECEIPT_INGESTION_READY":
        blockers.append("live_ingestion_receipt_not_ready")
    if receipt.get("live_receipt_ingested") is not True:
        blockers.append("live_receipt_ingested_not_true")

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

    archive_key = receipt.get("archive_key")
    archive_record_hash = receipt.get("archive_record_hash")
    idempotency_digest = receipt.get("idempotency_digest")
    if not archive_key:
        blockers.append("archive_key_missing")
    if not archive_record_hash:
        blockers.append("archive_record_hash_missing")
    if not idempotency_digest:
        blockers.append("idempotency_digest_missing")

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

    source_id = receipt.get("ingestion_receipt_id")
    incident_id = receipt.get("incident_id")
    query_mode = str(ctx.get("query_mode", "operator_replay_query"))
    replay_query_key = str(ctx.get("replay_query_key") or f"qi/live/{source_id or 'unknown'}")
    material = {
        "source_ingestion_receipt_id": source_id,
        "incident_id": incident_id,
        "external_case_number": external_case_number_int,
        "external_case_url": external_case_url,
        "archive_record_hash": archive_record_hash,
        "idempotency_digest": idempotency_digest,
        "replay_query_key": replay_query_key,
    }
    snapshot_id = "qi-live-query-" + _digest(material)[:16]
    ready = not blockers
    if ready and receipt.get("connector_executor_performed") is not True:
        warnings.append("connector_executor_not_marked_performed")

    summary = (
        f"Live receipt {source_id or 'unknown'} for incident {incident_id or 'unknown'} "
        f"maps to external case {external_case_number_int} at {external_case_url or 'missing'}; "
        f"archive={archive_key or 'missing'}"
    )

    return QiLiveReceiptQuerySnapshot(
        snapshot_version="kuuos_runtime_daemon_qi_live_receipt_query_surface_v0_1",
        query_status="QI_LIVE_RECEIPT_QUERY_SNAPSHOT_READY" if ready else "QI_LIVE_RECEIPT_QUERY_SNAPSHOT_BLOCKED",
        snapshot_id=snapshot_id,
        source_ingestion_receipt_id=str(source_id) if source_id is not None else None,
        incident_id=str(incident_id) if incident_id is not None else None,
        external_case_number=external_case_number_int,
        external_case_url=str(external_case_url) if external_case_url else None,
        archive_key=str(archive_key) if archive_key else None,
        archive_record_hash=str(archive_record_hash) if archive_record_hash else None,
        idempotency_digest=str(idempotency_digest) if idempotency_digest else None,
        query_mode=query_mode,
        replay_query_key=replay_query_key,
        operator_summary=summary,
        live_receipt_query_rendered=True,
        replay_packet_rendered=True,
        dashboard_ready=ready,
        read_only_surface=ctx.get("read_only_surface_required") is True,
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
        query_blockers=blockers,
        query_warnings=warnings,
    )
