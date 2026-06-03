#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


CANONICAL_CHAIN = [
    "qi_daemon_operator_surface_confirmed_baseline_packet",
    "qi_autonomous_tick_policy_kernel",
    "qi_autonomous_tick_policy_receipt_loop_binding",
    "qi_autonomous_multi_tick_window_governor",
    "qi_adaptive_window_scheduler",
    "qi_rhythm_memory_cadence_history_layer",
    "qi_append_only_rhythm_receipt_ledger",
    "qi_rhythm_trend_forecast",
    "qi_forecast_to_scheduler_advisory_bridge",
    "qi_advisory_aware_adaptive_scheduler_integration",
    "qi_end_to_end_cadence_cycle_packet",
    "qi_cadence_loop_confirmed_baseline_packet",
]


@dataclass(frozen=True)
class QiCadenceSuperchainFinalityPacketResult:
    finality_packet_version: str
    finality_packet_status: str
    finality_packet_id: str
    superchain_root_digest: str
    source_baseline_packet_id: str | None
    source_baseline_root_digest: str | None
    source_cycle_packet_id: str | None
    source_cycle_root_digest: str | None
    source_cycle_lineage_digest: str | None
    chain_index_count: int
    canonical_chain_complete: bool
    finality_confirmed: bool
    receipt_only_finality_packet: bool
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
    superchain_index: list[str]
    finality_packet: dict[str, Any]
    finality_blockers: list[str]
    finality_warnings: list[str]
    authority: str = "qi_cadence_superchain_finality_receipt_only"

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


def build_qi_cadence_superchain_finality_packet(
    *,
    baseline_packet: Mapping[str, Any],
    finality_context: Mapping[str, Any] | None = None,
) -> QiCadenceSuperchainFinalityPacketResult:
    baseline = _mapping(baseline_packet)
    ctx = _mapping(finality_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("cadence_superchain_finality_enabled") is not True:
        blockers.append("cadence_superchain_finality_enabled_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("finality_required") is not True:
        blockers.append("finality_required_not_true")
    if ctx.get("request_runtime_execution") is True:
        blockers.append("runtime_execution_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if baseline.get("baseline_packet_status") != "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_READY":
        blockers.append("baseline_packet_not_ready")
    if baseline.get("confirmed_baseline") is not True:
        blockers.append("confirmed_baseline_not_true")
    if baseline.get("autonomous_qi_cadence_loop_confirmed") is not True:
        blockers.append("autonomous_qi_cadence_loop_not_confirmed")
    if baseline.get("receipt_only_baseline_packet") is not True:
        blockers.append("baseline_packet_not_receipt_only")
    if baseline.get("cycle_lineage_preserved") is not True:
        blockers.append("cycle_lineage_not_preserved")
    if baseline.get("no_authority_boundary_preserved") is not True:
        blockers.append("no_authority_boundary_not_preserved")
    _require_false("baseline", baseline, blockers)

    source_baseline_id = baseline.get("baseline_packet_id")
    source_baseline_root = baseline.get("baseline_root_digest")
    source_cycle_id = baseline.get("source_cycle_packet_id")
    source_cycle_root = baseline.get("source_cycle_root_digest")
    source_cycle_lineage = baseline.get("source_cycle_lineage_digest")
    if not source_baseline_id:
        blockers.append("source_baseline_packet_id_missing")
    if not source_baseline_root:
        blockers.append("source_baseline_root_digest_missing")
    if not source_cycle_id:
        warnings.append("source_cycle_packet_id_missing_optional")
    if not source_cycle_root:
        warnings.append("source_cycle_root_digest_missing_optional")
    if not source_cycle_lineage:
        warnings.append("source_cycle_lineage_digest_missing_optional")

    provided_chain = ctx.get("superchain_index")
    if isinstance(provided_chain, list) and all(isinstance(item, str) for item in provided_chain):
        chain = provided_chain
    else:
        chain = CANONICAL_CHAIN
    canonical_complete = all(item in chain for item in CANONICAL_CHAIN)
    if not canonical_complete:
        blockers.append("canonical_chain_incomplete")

    material = {
        "baseline_packet_id": source_baseline_id,
        "baseline_root_digest": source_baseline_root,
        "cycle_packet_id": source_cycle_id,
        "cycle_root_digest": source_cycle_root,
        "cycle_lineage_digest": source_cycle_lineage,
        "superchain_index": chain,
        "finality_context_id": ctx.get("finality_context_id"),
        "receipt_only": True,
        "finality_confirmed": True,
    }
    root_digest = _sha_obj(material)
    packet_id = "qi-cadence-finality-" + root_digest[:16]
    ready = not blockers
    packet = dict(material)
    packet.update({
        "finality_packet_id": packet_id,
        "finality_packet_version": "kuuos_runtime_daemon_qi_cadence_superchain_finality_packet_v0_1",
        "finality_packet_status": "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY" if ready else "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_BLOCKED",
        "superchain_root_digest": root_digest,
        "canonical_chain_complete": canonical_complete,
        "receipt_only_finality_packet": True,
        "no_authority_boundary_preserved": True,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    })

    return QiCadenceSuperchainFinalityPacketResult(
        finality_packet_version="kuuos_runtime_daemon_qi_cadence_superchain_finality_packet_v0_1",
        finality_packet_status="QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY" if ready else "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_BLOCKED",
        finality_packet_id=packet_id,
        superchain_root_digest=root_digest,
        source_baseline_packet_id=str(source_baseline_id) if source_baseline_id else None,
        source_baseline_root_digest=str(source_baseline_root) if source_baseline_root else None,
        source_cycle_packet_id=str(source_cycle_id) if source_cycle_id else None,
        source_cycle_root_digest=str(source_cycle_root) if source_cycle_root else None,
        source_cycle_lineage_digest=str(source_cycle_lineage) if source_cycle_lineage else None,
        chain_index_count=len(chain),
        canonical_chain_complete=canonical_complete,
        finality_confirmed=ready,
        receipt_only_finality_packet=True,
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
        superchain_index=chain,
        finality_packet=packet if ready else {},
        finality_blockers=blockers,
        finality_warnings=warnings,
    )
