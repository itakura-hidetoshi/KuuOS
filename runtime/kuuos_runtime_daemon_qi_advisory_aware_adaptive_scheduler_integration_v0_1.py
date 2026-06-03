#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence
import pathlib

try:
    from runtime.kuuos_runtime_daemon_qi_adaptive_window_scheduler_v0_1 import run_qi_adaptive_window_scheduler
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_adaptive_window_scheduler_v0_1 import run_qi_adaptive_window_scheduler


@dataclass(frozen=True)
class QiAdvisoryAwareAdaptiveSchedulerIntegrationResult:
    integration_version: str
    integration_status: str
    advisory_packet_id: str | None
    source_forecast_packet_id: str | None
    advisory_cadence_mode_hint: str | None
    advisory_min_window_ticks_hint: int
    advisory_max_window_ticks_hint: int
    advisory_reason: str | None
    advisory_applied_as_hint: bool
    advisory_direct_authority: bool
    live_scheduler_still_decides: bool
    integrated_adaptive_context: dict[str, Any]
    delegated_adaptive_status: str | None
    delegated_cadence_mode: str | None
    delegated_recommended_window_ticks: int
    delegated_completed_tick_count: int
    delegated_stop_reason: str | None
    event_log_path: str
    ledger_state_path: str
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    delegated_adaptive_packet: dict[str, Any]
    integration_blockers: list[str]
    integration_warnings: list[str]
    authority: str = "advisory_aware_adaptive_scheduler_integration_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


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
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def run_qi_advisory_aware_adaptive_scheduler_integration(
    *,
    advisory_packet: Mapping[str, Any],
    decisionos_packet: Mapping[str, Any],
    cbf_packet: Mapping[str, Any],
    token_ledger_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    integration_context: Mapping[str, Any] | None = None,
) -> QiAdvisoryAwareAdaptiveSchedulerIntegrationResult:
    advisory = _mapping(advisory_packet)
    ctx = _mapping(integration_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("advisory_aware_scheduler_enabled") is not True:
        blockers.append("advisory_aware_scheduler_enabled_not_true")
    if ctx.get("advisory_only_required") is not True:
        blockers.append("advisory_only_required_not_true")
    if ctx.get("live_scheduler_must_decide") is not True:
        blockers.append("live_scheduler_must_decide_not_true")
    if ctx.get("request_direct_window_set") is True:
        blockers.append("direct_window_set_requested")
    if ctx.get("request_scheduler_execution_without_delegate") is True:
        blockers.append("scheduler_execution_without_delegate_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if advisory.get("bridge_status") != "QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_READY":
        blockers.append("advisory_bridge_not_ready")
    if advisory.get("advisory_only") is not True:
        blockers.append("advisory_only_not_true")
    if advisory.get("scheduler_context_patch_authoritative") is not False:
        blockers.append("advisory_patch_authoritative_not_false")
    if advisory.get("forecast_directly_sets_window") is not False:
        blockers.append("forecast_directly_sets_window_not_false")
    if advisory.get("bounded_hint_enforced") is not True:
        blockers.append("bounded_hint_not_enforced")
    if advisory.get("replaces_forecast_packet") is not False or advisory.get("replaces_ledger_root") is not False:
        blockers.append("advisory_replacement_boundary_not_false")
    _require_false("advisory", advisory, blockers)

    base_min = max(1, _int(ctx.get("base_min_window_ticks"), 1))
    base_max = max(base_min, _int(ctx.get("base_max_window_ticks"), 4))
    absolute_cap = max(1, _int(ctx.get("absolute_max_window_ticks"), 16))
    raw_min_hint = _int(advisory.get("advisory_min_window_ticks_hint"), base_min)
    raw_max_hint = _int(advisory.get("advisory_max_window_ticks_hint"), base_max)
    min_hint = _clamp(raw_min_hint, 1, absolute_cap)
    max_hint = _clamp(raw_max_hint, min_hint, absolute_cap)
    max_hint = min(max_hint, base_max if ctx.get("allow_advisory_expansion") is not True else absolute_cap)
    if max_hint < min_hint:
        min_hint = max_hint
    if raw_max_hint > absolute_cap:
        warnings.append("advisory_max_hint_clamped_to_absolute_cap")

    adaptive_context = {
        "adaptive_window_scheduler_enabled": True,
        "read_only_adaptive_scheduler": True,
        "jsonl_backend_required": True,
        "min_window_ticks": min_hint,
        "max_window_ticks": max_hint,
        "absolute_max_window_ticks": absolute_cap,
        "current_tick": ctx.get("current_tick", _mapping(token_ledger_packet).get("current_tick", 0)),
        "tick_id_prefix": str(ctx.get("tick_id_prefix", "qi-advisory-aware")),
        "process_tensor_schedule": ctx.get("process_tensor_schedule") if isinstance(ctx.get("process_tensor_schedule"), list) else [],
        "memory_complexity_threshold": ctx.get("memory_complexity_threshold", _mapping(process_tensor_packet).get("memory_complexity_threshold", 1.0)),
        "recovery_epsilon": ctx.get("recovery_epsilon", _mapping(process_tensor_packet).get("recovery_epsilon", 0.1)),
        "advisory_packet_id": advisory.get("advisory_packet_id"),
        "advisory_cadence_mode_hint": advisory.get("advisory_cadence_mode_hint"),
        "advisory_reason": advisory.get("advisory_reason"),
    }

    delegated: dict[str, Any] = {}
    if not blockers:
        delegated = run_qi_adaptive_window_scheduler(
            decisionos_packet=decisionos_packet,
            cbf_packet=cbf_packet,
            token_ledger_packet=token_ledger_packet,
            process_tensor_packet=process_tensor_packet,
            memory_entries=memory_entries,
            scheduler_state=scheduler_state,
            scheduler_proposal=scheduler_proposal,
            process_tensor_metrics=process_tensor_metrics,
            event_log_path=event_log_path,
            ledger_state_path=ledger_state_path,
            adaptive_context=adaptive_context,
        ).to_dict()
        if delegated.get("adaptive_scheduler_status") != "QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED":
            blockers.append("delegated_adaptive_scheduler_not_completed")
        _require_false("delegated_adaptive", delegated, blockers)

    ready = not blockers
    return QiAdvisoryAwareAdaptiveSchedulerIntegrationResult(
        integration_version="kuuos_runtime_daemon_qi_advisory_aware_adaptive_scheduler_integration_v0_1",
        integration_status="QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_COMPLETED" if ready else "QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_BLOCKED",
        advisory_packet_id=str(advisory.get("advisory_packet_id")) if advisory.get("advisory_packet_id") else None,
        source_forecast_packet_id=str(advisory.get("source_forecast_packet_id")) if advisory.get("source_forecast_packet_id") else None,
        advisory_cadence_mode_hint=str(advisory.get("advisory_cadence_mode_hint")) if advisory.get("advisory_cadence_mode_hint") else None,
        advisory_min_window_ticks_hint=min_hint,
        advisory_max_window_ticks_hint=max_hint,
        advisory_reason=str(advisory.get("advisory_reason")) if advisory.get("advisory_reason") else None,
        advisory_applied_as_hint=ready,
        advisory_direct_authority=False,
        live_scheduler_still_decides=True,
        integrated_adaptive_context=adaptive_context if ready else {},
        delegated_adaptive_status=str(delegated.get("adaptive_scheduler_status")) if delegated.get("adaptive_scheduler_status") else None,
        delegated_cadence_mode=str(delegated.get("cadence_mode")) if delegated.get("cadence_mode") else None,
        delegated_recommended_window_ticks=int(delegated.get("recommended_window_ticks", 0)) if delegated else 0,
        delegated_completed_tick_count=int(delegated.get("delegated_completed_tick_count", 0)) if delegated else 0,
        delegated_stop_reason=str(delegated.get("delegated_stop_reason")) if delegated.get("delegated_stop_reason") else None,
        event_log_path=str(event_log_path),
        ledger_state_path=str(ledger_state_path),
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        delegated_adaptive_packet=delegated,
        integration_blockers=blockers,
        integration_warnings=warnings,
    )
