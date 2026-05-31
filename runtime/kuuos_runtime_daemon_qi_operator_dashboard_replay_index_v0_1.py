#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiOperatorDashboardReplayIndex:
    index_version: str
    index_status: str
    dashboard_packet_id: str
    source_query_snapshot_id: str | None
    incident_id: str | None
    external_case_number: int | None
    external_case_url: str | None
    replay_query_key: str | None
    archive_key: str | None
    archive_record_hash: str | None
    idempotency_digest: str | None
    operator_summary: str | None
    dashboard_title: str
    dashboard_cards: list[dict[str, Any]]
    replay_index_key: str
    replay_index_hash: str
    dashboard_packet_rendered: bool
    replay_index_rendered: bool
    operator_dashboard_ready: bool
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
    dashboard_blockers: list[str]
    dashboard_warnings: list[str]
    authority: str = "operator_dashboard_replay_index"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def build_qi_operator_dashboard_replay_index(
    *,
    query_snapshot: Mapping[str, Any],
    dashboard_context: Mapping[str, Any] | None = None,
) -> QiOperatorDashboardReplayIndex:
    snapshot = _mapping(query_snapshot)
    ctx = _mapping(dashboard_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("operator_dashboard_enabled") is not True:
        blockers.append("operator_dashboard_enabled_not_true")
    if ctx.get("read_only_surface_required") is not True:
        blockers.append("read_only_surface_required_not_true")
    if snapshot.get("query_status") != "QI_LIVE_RECEIPT_QUERY_SNAPSHOT_READY":
        blockers.append("query_snapshot_not_ready")
    if snapshot.get("dashboard_ready") is not True:
        blockers.append("query_dashboard_not_ready")
    if snapshot.get("read_only_surface") is not True:
        blockers.append("query_surface_not_read_only")

    external_case_number = snapshot.get("external_case_number")
    try:
        external_case_number_int = int(external_case_number) if external_case_number is not None else None
    except (TypeError, ValueError):
        external_case_number_int = None
        blockers.append("external_case_number_invalid")
    external_case_url = snapshot.get("external_case_url")
    replay_query_key = snapshot.get("replay_query_key")
    archive_key = snapshot.get("archive_key")
    archive_record_hash = snapshot.get("archive_record_hash")
    idempotency_digest = snapshot.get("idempotency_digest")
    source_query_snapshot_id = snapshot.get("snapshot_id")
    incident_id = snapshot.get("incident_id")
    operator_summary = snapshot.get("operator_summary")

    required_fields = {
        "external_case_number": external_case_number_int,
        "external_case_url": external_case_url,
        "replay_query_key": replay_query_key,
        "archive_key": archive_key,
        "archive_record_hash": archive_record_hash,
        "idempotency_digest": idempotency_digest,
        "source_query_snapshot_id": source_query_snapshot_id,
    }
    for name, value in required_fields.items():
        if value is None or value == "":
            blockers.append(f"{name}_missing")

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
        if snapshot.get(flag) is True or ctx.get(flag) is True:
            blockers.append(f"forbidden_flag_true:{flag}")

    dashboard_title = str(ctx.get("dashboard_title", "Qi Live Receipt Operator Dashboard"))
    cards = [
        {
            "card": "incident",
            "incident_id": incident_id,
            "summary": operator_summary,
        },
        {
            "card": "external_case",
            "external_case_number": external_case_number_int,
            "external_case_url": external_case_url,
        },
        {
            "card": "replay",
            "replay_query_key": replay_query_key,
            "archive_key": archive_key,
            "archive_record_hash": archive_record_hash,
        },
        {
            "card": "idempotency",
            "idempotency_digest": idempotency_digest,
        },
    ]
    replay_index_key = str(ctx.get("replay_index_key") or f"qi/replay/{replay_query_key or source_query_snapshot_id or 'unknown'}")
    index_material = {
        "source_query_snapshot_id": source_query_snapshot_id,
        "incident_id": incident_id,
        "external_case_number": external_case_number_int,
        "external_case_url": external_case_url,
        "replay_query_key": replay_query_key,
        "archive_record_hash": archive_record_hash,
        "idempotency_digest": idempotency_digest,
        "replay_index_key": replay_index_key,
    }
    replay_index_hash = _digest(index_material)
    dashboard_packet_id = "qi-dashboard-" + replay_index_hash[:16]
    ready = not blockers
    if ready and not operator_summary:
        warnings.append("operator_summary_missing")

    return QiOperatorDashboardReplayIndex(
        index_version="kuuos_runtime_daemon_qi_operator_dashboard_replay_index_v0_1",
        index_status="QI_OPERATOR_DASHBOARD_REPLAY_INDEX_READY" if ready else "QI_OPERATOR_DASHBOARD_REPLAY_INDEX_BLOCKED",
        dashboard_packet_id=dashboard_packet_id,
        source_query_snapshot_id=str(source_query_snapshot_id) if source_query_snapshot_id else None,
        incident_id=str(incident_id) if incident_id is not None else None,
        external_case_number=external_case_number_int,
        external_case_url=str(external_case_url) if external_case_url else None,
        replay_query_key=str(replay_query_key) if replay_query_key else None,
        archive_key=str(archive_key) if archive_key else None,
        archive_record_hash=str(archive_record_hash) if archive_record_hash else None,
        idempotency_digest=str(idempotency_digest) if idempotency_digest else None,
        operator_summary=str(operator_summary) if operator_summary else None,
        dashboard_title=dashboard_title,
        dashboard_cards=cards,
        replay_index_key=replay_index_key,
        replay_index_hash=replay_index_hash,
        dashboard_packet_rendered=True,
        replay_index_rendered=True,
        operator_dashboard_ready=ready,
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
        dashboard_blockers=blockers,
        dashboard_warnings=warnings,
    )
