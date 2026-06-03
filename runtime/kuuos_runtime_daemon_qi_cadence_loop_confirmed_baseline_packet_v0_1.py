#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiCadenceLoopConfirmedBaselinePacketResult:
    baseline_packet_version: str
    baseline_packet_status: str
    baseline_packet_id: str
    baseline_root_digest: str
    source_cycle_packet_id: str | None
    source_cycle_root_digest: str | None
    source_cycle_lineage_digest: str | None
    source_advisory_packet_id: str | None
    source_forecast_packet_id: str | None
    source_ledger_root_digest: str | None
    source_last_entry_digest: str | None
    confirmed_baseline: bool
    autonomous_qi_cadence_loop_confirmed: bool
    receipt_only_baseline_packet: bool
    cycle_lineage_preserved: bool
    no_authority_boundary_preserved: bool
    scheduler_bypass_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    baseline_packet: dict[str, Any]
    baseline_blockers: list[str]
    baseline_warnings: list[str]
    authority: str = "autonomous_qi_cadence_loop_confirmed_baseline_receipt_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
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


def build_qi_cadence_loop_confirmed_baseline_packet(
    *,
    cycle_packet: Mapping[str, Any],
    baseline_context: Mapping[str, Any] | None = None,
) -> QiCadenceLoopConfirmedBaselinePacketResult:
    cycle = _mapping(cycle_packet)
    ctx = _mapping(baseline_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("cadence_loop_confirmed_baseline_enabled") is not True:
        blockers.append("cadence_loop_confirmed_baseline_enabled_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("confirmed_baseline_required") is not True:
        blockers.append("confirmed_baseline_required_not_true")
    if ctx.get("request_runtime_execution") is True:
        blockers.append("runtime_execution_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if cycle.get("cycle_packet_status") != "QI_END_TO_END_CADENCE_CYCLE_PACKET_READY":
        blockers.append("cycle_packet_not_ready")
    if cycle.get("cadence_cycle_closed") is not True:
        blockers.append("cadence_cycle_not_closed")
    if cycle.get("receipt_only_cycle_packet") is not True:
        blockers.append("cycle_packet_not_receipt_only")
    if cycle.get("lineage_complete") is not True:
        blockers.append("cycle_lineage_not_complete")
    if cycle.get("no_authority_boundary_preserved") is not True:
        blockers.append("cycle_no_authority_boundary_not_preserved")
    _require_false("cycle", cycle, blockers)

    root_digest = cycle.get("cycle_root_digest")
    lineage_digest = cycle.get("cycle_lineage_digest")
    if not root_digest:
        blockers.append("cycle_root_digest_missing")
    if not lineage_digest:
        blockers.append("cycle_lineage_digest_missing")
    lineage = _mapping(_mapping(cycle.get("cycle_packet")).get("lineage"))
    source_advisory = cycle.get("source_advisory_packet_id") or lineage.get("advisory_packet_id")
    source_forecast = cycle.get("source_forecast_packet_id") or lineage.get("forecast_packet_id")
    source_ledger = cycle.get("source_ledger_root_digest") or lineage.get("ledger_root_digest")
    source_last = cycle.get("source_last_entry_digest") or lineage.get("last_entry_digest")
    if not source_advisory:
        blockers.append("source_advisory_packet_id_missing")
    if not source_forecast:
        warnings.append("source_forecast_packet_id_missing_optional")
    if not source_ledger:
        warnings.append("source_ledger_root_digest_missing_optional")
    if not source_last:
        warnings.append("source_last_entry_digest_missing_optional")

    material = {
        "cycle_packet_id": cycle.get("cycle_packet_id"),
        "cycle_root_digest": root_digest,
        "cycle_lineage_digest": lineage_digest,
        "source_advisory_packet_id": source_advisory,
        "source_forecast_packet_id": source_forecast,
        "source_ledger_root_digest": source_ledger,
        "source_last_entry_digest": source_last,
        "baseline_context_id": ctx.get("baseline_context_id"),
        "receipt_only": True,
        "confirmed_baseline": True,
        "autonomous_qi_cadence_loop_confirmed": True,
    }
    baseline_root_digest = _sha_obj(material)
    baseline_packet_id = "qi-cadence-baseline-" + baseline_root_digest[:16]
    ready = not blockers
    baseline_packet = dict(material)
    baseline_packet.update({
        "baseline_packet_id": baseline_packet_id,
        "baseline_packet_version": "kuuos_runtime_daemon_qi_cadence_loop_confirmed_baseline_packet_v0_1",
        "baseline_packet_status": "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_READY" if ready else "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_BLOCKED",
        "baseline_root_digest": baseline_root_digest,
        "cycle_lineage_preserved": True,
        "no_authority_boundary_preserved": True,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    })

    return QiCadenceLoopConfirmedBaselinePacketResult(
        baseline_packet_version="kuuos_runtime_daemon_qi_cadence_loop_confirmed_baseline_packet_v0_1",
        baseline_packet_status="QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_READY" if ready else "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_BLOCKED",
        baseline_packet_id=baseline_packet_id,
        baseline_root_digest=baseline_root_digest,
        source_cycle_packet_id=str(cycle.get("cycle_packet_id")) if cycle.get("cycle_packet_id") else None,
        source_cycle_root_digest=str(root_digest) if root_digest else None,
        source_cycle_lineage_digest=str(lineage_digest) if lineage_digest else None,
        source_advisory_packet_id=str(source_advisory) if source_advisory else None,
        source_forecast_packet_id=str(source_forecast) if source_forecast else None,
        source_ledger_root_digest=str(source_ledger) if source_ledger else None,
        source_last_entry_digest=str(source_last) if source_last else None,
        confirmed_baseline=ready,
        autonomous_qi_cadence_loop_confirmed=ready,
        receipt_only_baseline_packet=True,
        cycle_lineage_preserved=True,
        no_authority_boundary_preserved=True,
        scheduler_bypass_performed=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        baseline_packet=baseline_packet if ready else {},
        baseline_blockers=blockers,
        baseline_warnings=warnings,
    )
