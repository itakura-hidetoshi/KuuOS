#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiCadenceObservabilityProjectionResult:
    observability_version: str
    observability_status: str
    metrics_packet_id: str
    source_finality_packet_id: str | None
    source_superchain_root_digest: str | None
    source_baseline_packet_id: str | None
    chain_index_count: int
    canonical_chain_complete_gauge: int
    finality_confirmed_gauge: int
    receipt_only_gauge: int
    no_authority_boundary_gauge: int
    scheduler_bypass_gauge: int
    memory_write_gauge: int
    memory_append_gauge: int
    world_update_gauge: int
    probe_execution_gauge: int
    prometheus_text: str
    dashboard_packet: dict[str, Any]
    projection_only: bool
    dashboard_projection_only: bool
    runtime_control_authority: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    observability_blockers: list[str]
    observability_warnings: list[str]
    authority: str = "qi_cadence_observability_projection_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _gauge_bool(value: Any) -> int:
    return 1 if value is True else 0


def _forbidden_gauge(value: Any) -> int:
    return 1 if value is True else 0


def _metric_line(name: str, value: int | float, labels: Mapping[str, str] | None = None) -> str:
    labels = labels or {}
    if labels:
        body = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{name}{{{body}}} {value}"
    return f"{name} {value}"


def build_qi_cadence_observability_projection(
    *,
    finality_packet: Mapping[str, Any],
    observability_context: Mapping[str, Any] | None = None,
) -> QiCadenceObservabilityProjectionResult:
    packet = _mapping(finality_packet)
    ctx = _mapping(observability_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("cadence_observability_enabled") is not True:
        blockers.append("cadence_observability_enabled_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    if ctx.get("dashboard_projection_only_required") is not True:
        blockers.append("dashboard_projection_only_required_not_true")
    if ctx.get("request_runtime_control") is True:
        blockers.append("runtime_control_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if packet.get("finality_packet_status") != "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY":
        blockers.append("finality_packet_not_ready")
    if packet.get("receipt_only_finality_packet") is not True:
        blockers.append("finality_not_receipt_only")
    if packet.get("no_authority_boundary_preserved") is not True:
        blockers.append("no_authority_boundary_not_preserved")

    labels = {
        "chain": "qi_cadence",
        "version": "v0_2",
    }
    finality_id = str(packet.get("finality_packet_id") or "unknown")
    root_digest = str(packet.get("superchain_root_digest") or "unknown")
    chain_count = int(packet.get("chain_index_count") or len(packet.get("superchain_index") or []))
    finality_g = _gauge_bool(packet.get("finality_confirmed"))
    chain_g = _gauge_bool(packet.get("canonical_chain_complete"))
    receipt_g = _gauge_bool(packet.get("receipt_only_finality_packet"))
    boundary_g = _gauge_bool(packet.get("no_authority_boundary_preserved"))
    bypass_g = _forbidden_gauge(packet.get("scheduler_bypass_performed"))
    memory_write_g = _forbidden_gauge(packet.get("memory_write_performed"))
    memory_append_g = _forbidden_gauge(packet.get("memory_append_performed"))
    world_update_g = _forbidden_gauge(packet.get("world_update_performed"))
    probe_g = _forbidden_gauge(packet.get("probe_execution_performed"))

    material = {
        "finality_packet_id": finality_id,
        "superchain_root_digest": root_digest,
        "chain_index_count": chain_count,
        "finality_confirmed": finality_g,
        "canonical_chain_complete": chain_g,
        "no_authority_boundary_preserved": boundary_g,
        "projection_only": True,
    }
    metrics_packet_id = "qi-cadence-metrics-" + _sha_obj(material)[:16]
    metric_lines = [
        _metric_line("kuuos_qi_cadence_finality_confirmed", finality_g, labels),
        _metric_line("kuuos_qi_cadence_canonical_chain_complete", chain_g, labels),
        _metric_line("kuuos_qi_cadence_receipt_only", receipt_g, labels),
        _metric_line("kuuos_qi_cadence_no_authority_boundary", boundary_g, labels),
        _metric_line("kuuos_qi_cadence_scheduler_bypass", bypass_g, labels),
        _metric_line("kuuos_qi_cadence_memory_write", memory_write_g, labels),
        _metric_line("kuuos_qi_cadence_memory_append", memory_append_g, labels),
        _metric_line("kuuos_qi_cadence_world_update", world_update_g, labels),
        _metric_line("kuuos_qi_cadence_probe_execution", probe_g, labels),
        _metric_line("kuuos_qi_cadence_chain_index_count", chain_count, labels),
    ]
    prometheus_text = "\n".join(metric_lines) + "\n"
    dashboard_packet = {
        "dashboard_uid": "qi-cadence-v0-2",
        "dashboard_title": "Qi Cadence Observability v0.2",
        "projection_only": True,
        "metrics_packet_id": metrics_packet_id,
        "source_finality_packet_id": finality_id,
        "source_superchain_root_digest": root_digest,
        "panels": [
            {"title": "Finality Confirmed", "metric": "kuuos_qi_cadence_finality_confirmed"},
            {"title": "Canonical Chain Complete", "metric": "kuuos_qi_cadence_canonical_chain_complete"},
            {"title": "No Authority Boundary", "metric": "kuuos_qi_cadence_no_authority_boundary"},
            {"title": "Forbidden Runtime Surfaces", "metrics": ["kuuos_qi_cadence_scheduler_bypass", "kuuos_qi_cadence_memory_write", "kuuos_qi_cadence_world_update", "kuuos_qi_cadence_probe_execution"]},
        ],
        "runtime_control_authority": False,
        "memory_write_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    }
    ready = not blockers
    return QiCadenceObservabilityProjectionResult(
        observability_version="kuuos_runtime_daemon_qi_cadence_observability_projection_v0_2",
        observability_status="QI_CADENCE_OBSERVABILITY_PROJECTION_READY" if ready else "QI_CADENCE_OBSERVABILITY_PROJECTION_BLOCKED",
        metrics_packet_id=metrics_packet_id,
        source_finality_packet_id=finality_id if finality_id != "unknown" else None,
        source_superchain_root_digest=root_digest if root_digest != "unknown" else None,
        source_baseline_packet_id=str(packet.get("source_baseline_packet_id")) if packet.get("source_baseline_packet_id") else None,
        chain_index_count=chain_count,
        canonical_chain_complete_gauge=chain_g,
        finality_confirmed_gauge=finality_g,
        receipt_only_gauge=receipt_g,
        no_authority_boundary_gauge=boundary_g,
        scheduler_bypass_gauge=bypass_g,
        memory_write_gauge=memory_write_g,
        memory_append_gauge=memory_append_g,
        world_update_gauge=world_update_g,
        probe_execution_gauge=probe_g,
        prometheus_text=prometheus_text,
        dashboard_packet=dashboard_packet if ready else {},
        projection_only=True,
        dashboard_projection_only=True,
        runtime_control_authority=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        observability_blockers=blockers,
        observability_warnings=warnings,
    )
