#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiForecastToSchedulerAdvisoryBridgeResult:
    bridge_version: str
    bridge_status: str
    advisory_packet_id: str
    source_forecast_packet_id: str | None
    source_ledger_root_digest: str | None
    source_last_entry_digest: str | None
    forecast_window_bias: str | None
    forecast_cadence_mode_hint: str | None
    forecast_risk_class: str | None
    forecast_confidence: float
    advisory_min_window_ticks_hint: int
    advisory_max_window_ticks_hint: int
    advisory_cadence_mode_hint: str
    advisory_stop_on_observe_hint: bool
    advisory_stop_on_full_history_hint: bool
    advisory_stop_on_freeze_hint: bool
    advisory_reason: str
    advisory_only: bool
    scheduler_context_patch_authoritative: bool
    forecast_directly_sets_window: bool
    bounded_hint_enforced: bool
    replaces_forecast_packet: bool
    replaces_ledger_root: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    advisory_context_patch: dict[str, Any]
    bridge_blockers: list[str]
    bridge_warnings: list[str]
    authority: str = "forecast_to_scheduler_advisory_bridge_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _map_bias_to_bounds(bias: str, cadence: str, risk: str, confidence: float, base_min: int, base_max: int, absolute_cap: int) -> tuple[int, int, str, str]:
    if risk == "critical" or bias == "freeze_guarded":
        return 1, 1, "single_tick_high_pressure", "critical_or_freeze_forecast"
    if bias == "full_history_guarded":
        return 1, 1, "full_history_single_tick", "full_history_forecast"
    if bias == "observe_first":
        return 1, min(base_max, 1), "observe_first_single_tick", "observe_forecast"
    if bias == "contract_window" or risk == "moderate" and cadence == "single_tick_high_pressure":
        return 1, min(base_max, 2), cadence or "single_tick_high_pressure", "pressure_contract_forecast"
    if bias == "expand_if_low_pressure" and risk == "low" and confidence >= 0.5:
        return base_min, min(max(base_max, 4), absolute_cap), cadence or "wide_compressed_window", "stable_low_pressure_forecast"
    return base_min, min(base_max, 4), cadence or "moderate_guarded_window", "steady_forecast"


def build_qi_forecast_to_scheduler_advisory_bridge(
    *,
    forecast_packet: Mapping[str, Any],
    bridge_context: Mapping[str, Any] | None = None,
) -> QiForecastToSchedulerAdvisoryBridgeResult:
    forecast = _mapping(forecast_packet)
    ctx = _mapping(bridge_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("forecast_to_scheduler_bridge_enabled") is not True:
        blockers.append("forecast_to_scheduler_bridge_enabled_not_true")
    if ctx.get("advisory_only_required") is not True:
        blockers.append("advisory_only_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    if ctx.get("request_direct_window_set") is True:
        blockers.append("direct_window_set_requested")
    if ctx.get("request_scheduler_execution") is True:
        blockers.append("scheduler_execution_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")
    if forecast.get("forecast_status") != "QI_RHYTHM_TREND_FORECAST_READY":
        blockers.append("forecast_not_ready")
    if forecast.get("projection_only") is not True:
        blockers.append("forecast_not_projection_only")
    if forecast.get("replaces_ledger_root") is not False:
        blockers.append("forecast_replaces_ledger_root_not_false")
    if forecast.get("memory_write_performed") is not False or forecast.get("memory_append_performed") is not False:
        blockers.append("forecast_memory_boundary_not_false")
    if forecast.get("probe_execution_performed") is not False:
        blockers.append("forecast_probe_boundary_not_false")

    base_min = max(1, _int(ctx.get("base_min_window_ticks"), 1))
    base_max = max(base_min, _int(ctx.get("base_max_window_ticks"), 4))
    absolute_cap = max(1, _int(ctx.get("absolute_max_window_ticks"), 16))
    base_max = min(base_max, absolute_cap)
    confidence = _float(forecast.get("forecast_confidence"), 0.0)
    bias = str(forecast.get("forecast_window_bias") or "hold_steady")
    cadence = str(forecast.get("forecast_cadence_mode_hint") or "moderate_guarded_window")
    risk = str(forecast.get("forecast_risk_class") or "moderate")
    min_hint, max_hint, cadence_hint, reason = _map_bias_to_bounds(bias, cadence, risk, confidence, base_min, base_max, absolute_cap)
    min_hint = _clamp(min_hint, 1, absolute_cap)
    max_hint = _clamp(max_hint, min_hint, absolute_cap)

    patch_core = {
        "source_forecast_packet_id": forecast.get("forecast_packet_id"),
        "source_ledger_root_digest": forecast.get("ledger_root_digest"),
        "source_last_entry_digest": forecast.get("source_last_entry_digest"),
        "forecast_window_bias": bias,
        "forecast_cadence_mode_hint": cadence,
        "forecast_risk_class": risk,
        "forecast_confidence": confidence,
        "advisory_min_window_ticks_hint": min_hint,
        "advisory_max_window_ticks_hint": max_hint,
        "advisory_cadence_mode_hint": cadence_hint,
        "advisory_reason": reason,
        "advisory_only": True,
    }
    packet_id = "qi-forecast-advisory-" + _sha_obj(patch_core)[:16]
    patch = dict(patch_core)
    patch.update({
        "advisory_packet_id": packet_id,
        "bridge_version": "kuuos_runtime_daemon_qi_forecast_to_scheduler_advisory_bridge_v0_1",
        "scheduler_context_patch_authoritative": False,
        "forecast_directly_sets_window": False,
        "bounded_hint_enforced": True,
        "projection_only": True,
        "replaces_forecast_packet": False,
        "replaces_ledger_root": False,
        "stop_on_observe_hint": True,
        "stop_on_full_history_hint": True,
        "stop_on_freeze_hint": True,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    })
    ready = not blockers
    return QiForecastToSchedulerAdvisoryBridgeResult(
        bridge_version="kuuos_runtime_daemon_qi_forecast_to_scheduler_advisory_bridge_v0_1",
        bridge_status="QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_READY" if ready else "QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_BLOCKED",
        advisory_packet_id=packet_id,
        source_forecast_packet_id=str(forecast.get("forecast_packet_id")) if forecast.get("forecast_packet_id") else None,
        source_ledger_root_digest=str(forecast.get("ledger_root_digest")) if forecast.get("ledger_root_digest") else None,
        source_last_entry_digest=str(forecast.get("source_last_entry_digest")) if forecast.get("source_last_entry_digest") else None,
        forecast_window_bias=bias,
        forecast_cadence_mode_hint=cadence,
        forecast_risk_class=risk,
        forecast_confidence=confidence,
        advisory_min_window_ticks_hint=min_hint,
        advisory_max_window_ticks_hint=max_hint,
        advisory_cadence_mode_hint=cadence_hint,
        advisory_stop_on_observe_hint=True,
        advisory_stop_on_full_history_hint=True,
        advisory_stop_on_freeze_hint=True,
        advisory_reason=reason,
        advisory_only=True,
        scheduler_context_patch_authoritative=False,
        forecast_directly_sets_window=False,
        bounded_hint_enforced=True,
        replaces_forecast_packet=False,
        replaces_ledger_root=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        advisory_context_patch=patch if ready else {},
        bridge_blockers=blockers,
        bridge_warnings=warnings,
    )
