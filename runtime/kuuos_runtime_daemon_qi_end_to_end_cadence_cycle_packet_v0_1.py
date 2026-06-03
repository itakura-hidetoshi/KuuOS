#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiEndToEndCadenceCyclePacketResult:
    cycle_packet_version: str
    cycle_packet_status: str
    cycle_packet_id: str
    source_advisory_packet_id: str | None
    source_forecast_packet_id: str | None
    source_ledger_root_digest: str | None
    source_last_entry_digest: str | None
    advisory_aware_integration_status: str | None
    delegated_adaptive_status: str | None
    delegated_cadence_mode: str | None
    delegated_recommended_window_ticks: int
    delegated_completed_tick_count: int
    delegated_stop_reason: str | None
    cadence_cycle_closed: bool
    scheduler_bypass_performed: bool
    receipt_only_cycle_packet: bool
    lineage_complete: bool
    no_authority_boundary_preserved: bool
    cycle_root_digest: str
    cycle_lineage_digest: str
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    cycle_packet: dict[str, Any]
    cycle_blockers: list[str]
    cycle_warnings: list[str]
    authority: str = "end_to_end_cadence_cycle_packet_receipt_only"

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


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
        "scheduler_bypass_performed",
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_end_to_end_cadence_cycle_packet(
    *,
    advisory_aware_integration_packet: Mapping[str, Any],
    cycle_context: Mapping[str, Any] | None = None,
) -> QiEndToEndCadenceCyclePacketResult:
    packet = _mapping(advisory_aware_integration_packet)
    ctx = _mapping(cycle_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("end_to_end_cadence_cycle_packet_enabled") is not True:
        blockers.append("end_to_end_cadence_cycle_packet_enabled_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("scheduler_bypass_forbidden") is not True:
        blockers.append("scheduler_bypass_forbidden_not_true")
    if ctx.get("request_scheduler_execution") is True:
        blockers.append("scheduler_execution_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if packet.get("integration_status") != "QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_COMPLETED":
        blockers.append("advisory_aware_integration_not_completed")
    if packet.get("advisory_applied_as_hint") is not True:
        blockers.append("advisory_not_applied_as_hint")
    if packet.get("advisory_direct_authority") is not False:
        blockers.append("advisory_direct_authority_not_false")
    if packet.get("live_scheduler_still_decides") is not True:
        blockers.append("live_scheduler_still_decides_not_true")
    _require_false("advisory_aware_integration", packet, blockers)

    delegated = _mapping(packet.get("delegated_adaptive_packet"))
    if delegated:
        if delegated.get("adaptive_scheduler_status") != "QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED":
            blockers.append("delegated_adaptive_scheduler_not_completed")
        if delegated.get("delegates_only_to_multi_tick_window_governor") is not True:
            blockers.append("delegated_adaptive_not_delegating_to_window_governor")
        _require_false("delegated_adaptive", delegated, blockers)
    else:
        blockers.append("delegated_adaptive_packet_missing")

    source_advisory = packet.get("advisory_packet_id")
    source_forecast = packet.get("source_forecast_packet_id")
    source_ledger = None
    source_last = None
    context_patch = _mapping(packet.get("integrated_adaptive_context"))
    if source_advisory is None:
        blockers.append("source_advisory_packet_id_missing")
    source_forecast = source_forecast or context_patch.get("source_forecast_packet_id")
    delegated_advisory = context_patch.get("advisory_packet_id")
    if delegated_advisory and source_advisory and delegated_advisory != source_advisory:
        blockers.append("advisory_packet_id_mismatch")

    source_ledger = packet.get("source_ledger_root_digest") or context_patch.get("source_ledger_root_digest")
    source_last = packet.get("source_last_entry_digest") or context_patch.get("source_last_entry_digest")
    # Older integration packets may not carry ledger digests directly; keep them optional but visible.
    if source_ledger is None:
        warnings.append("source_ledger_root_digest_missing_optional")
    if source_last is None:
        warnings.append("source_last_entry_digest_missing_optional")

    lineage = {
        "advisory_packet_id": source_advisory,
        "forecast_packet_id": source_forecast,
        "ledger_root_digest": source_ledger,
        "last_entry_digest": source_last,
        "integration_status": packet.get("integration_status"),
        "delegated_adaptive_status": packet.get("delegated_adaptive_status"),
        "delegated_cadence_mode": packet.get("delegated_cadence_mode"),
        "delegated_recommended_window_ticks": packet.get("delegated_recommended_window_ticks"),
        "delegated_completed_tick_count": packet.get("delegated_completed_tick_count"),
        "delegated_stop_reason": packet.get("delegated_stop_reason"),
    }
    lineage_digest = _sha_obj(lineage)
    cycle_core = {
        "lineage_digest": lineage_digest,
        "receipt_only": True,
        "scheduler_bypass_performed": False,
        "no_authority_boundary_preserved": True,
        "cycle_context_id": ctx.get("cycle_context_id"),
    }
    cycle_root_digest = _sha_obj(cycle_core)
    cycle_packet_id = "qi-cadence-cycle-" + cycle_root_digest[:16]
    ready = not blockers
    cycle_packet = {
        "cycle_packet_id": cycle_packet_id,
        "cycle_packet_version": "kuuos_runtime_daemon_qi_end_to_end_cadence_cycle_packet_v0_1",
        "cycle_packet_status": "QI_END_TO_END_CADENCE_CYCLE_PACKET_READY" if ready else "QI_END_TO_END_CADENCE_CYCLE_PACKET_BLOCKED",
        "cycle_root_digest": cycle_root_digest,
        "cycle_lineage_digest": lineage_digest,
        "lineage": lineage,
        "cadence_cycle_closed": ready,
        "receipt_only_cycle_packet": True,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    }

    return QiEndToEndCadenceCyclePacketResult(
        cycle_packet_version="kuuos_runtime_daemon_qi_end_to_end_cadence_cycle_packet_v0_1",
        cycle_packet_status="QI_END_TO_END_CADENCE_CYCLE_PACKET_READY" if ready else "QI_END_TO_END_CADENCE_CYCLE_PACKET_BLOCKED",
        cycle_packet_id=cycle_packet_id,
        source_advisory_packet_id=str(source_advisory) if source_advisory else None,
        source_forecast_packet_id=str(source_forecast) if source_forecast else None,
        source_ledger_root_digest=str(source_ledger) if source_ledger else None,
        source_last_entry_digest=str(source_last) if source_last else None,
        advisory_aware_integration_status=str(packet.get("integration_status")) if packet.get("integration_status") else None,
        delegated_adaptive_status=str(packet.get("delegated_adaptive_status")) if packet.get("delegated_adaptive_status") else None,
        delegated_cadence_mode=str(packet.get("delegated_cadence_mode")) if packet.get("delegated_cadence_mode") else None,
        delegated_recommended_window_ticks=_int(packet.get("delegated_recommended_window_ticks"), 0),
        delegated_completed_tick_count=_int(packet.get("delegated_completed_tick_count"), 0),
        delegated_stop_reason=str(packet.get("delegated_stop_reason")) if packet.get("delegated_stop_reason") else None,
        cadence_cycle_closed=ready,
        scheduler_bypass_performed=False,
        receipt_only_cycle_packet=True,
        lineage_complete=source_advisory is not None and packet.get("integration_status") is not None and packet.get("delegated_adaptive_status") is not None,
        no_authority_boundary_preserved=True,
        cycle_root_digest=cycle_root_digest,
        cycle_lineage_digest=lineage_digest,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        cycle_packet=cycle_packet if ready else {},
        cycle_blockers=blockers,
        cycle_warnings=warnings,
    )
