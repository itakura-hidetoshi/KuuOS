#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiRhythmTrendForecastResult:
    forecast_version: str
    forecast_status: str
    ledger_path: str
    ledger_entry_count: int
    ledger_root_digest: str | None
    source_last_entry_digest: str | None
    trend_window_size: int
    pressure_trend: str
    stability_trend: str
    completion_trend: str
    observe_trend: str
    full_history_trend: str
    freeze_trend: str
    mean_pressure_score: float
    mean_stability_score: float
    mean_completion_ratio: float
    observe_ratio: float
    full_history_ratio: float
    freeze_ratio: float
    forecast_window_bias: str
    forecast_cadence_mode_hint: str
    forecast_risk_class: str
    forecast_confidence: float
    forecast_packet_id: str
    projection_only: bool
    replaces_ledger_root: bool
    trend_summary_authority: str
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    forecast_packet: dict[str, Any]
    forecast_blockers: list[str]
    forecast_warnings: list[str]
    authority: str = "rhythm_trend_forecast_projection_only"

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


def _mean(values: list[float], default: float = 0.0) -> float:
    return sum(values) / len(values) if values else default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            entries.append(value)
    return entries


def _entry_payload(entry: Mapping[str, Any]) -> Mapping[str, Any]:
    candidate = entry.get("source_candidate")
    return candidate if isinstance(candidate, Mapping) else entry


def _entry_digest(entry: Mapping[str, Any]) -> str:
    digest = entry.get("entry_digest")
    return str(digest) if digest else _sha_obj(entry)


def _ledger_root_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    return _sha_obj({"entry_digests": [_entry_digest(entry) for entry in entries]})


def _slope(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mx = sum(xs) / n
    my = sum(values) / n
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, values)) / denom


def _trend(values: list[float], up: str, down: str, flat: str, threshold: float = 0.03) -> str:
    s = _slope(values)
    if s > threshold:
        return up
    if s < -threshold:
        return down
    return flat


def _ratio(entries: list[Mapping[str, Any]], pred) -> float:
    return sum(1 for entry in entries if pred(entry)) / len(entries) if entries else 0.0


def _completion_ratio(entry: Mapping[str, Any]) -> float:
    payload = _entry_payload(entry)
    rec = max(1, _int(payload.get("recommended_window_ticks"), _int(entry.get("recommended_window_ticks"), 1)))
    comp = _int(payload.get("delegated_completed_tick_count"), _int(entry.get("delegated_completed_tick_count"), 0))
    return max(0.0, min(1.0, comp / rec))


def _stop_reason(entry: Mapping[str, Any]) -> str:
    payload = _entry_payload(entry)
    return str(payload.get("delegated_stop_reason") or entry.get("delegated_stop_reason") or "")


def _forecast_bias(*, pressure: float, stability: float, completion: float, observe: float, full: float, freeze: float, pressure_trend: str, stability_trend: str) -> tuple[str, str, str]:
    if freeze >= 0.15:
        return "freeze_guarded", "single_tick_high_pressure", "critical"
    if full >= 0.25:
        return "full_history_guarded", "full_history_single_tick", "high"
    if observe >= 0.30:
        return "observe_first", "observe_first_single_tick", "high"
    if pressure >= 0.75 or pressure_trend == "pressure_rising":
        return "contract_window", "single_tick_high_pressure", "moderate"
    if stability >= 0.75 and completion >= 0.75 and stability_trend != "stability_falling":
        return "expand_if_low_pressure", "wide_compressed_window", "low"
    return "hold_steady", "moderate_guarded_window", "moderate"


def build_qi_rhythm_trend_forecast(
    *,
    ledger_path: str | pathlib.Path,
    forecast_context: Mapping[str, Any] | None = None,
) -> QiRhythmTrendForecastResult:
    ctx = _mapping(forecast_context)
    path = pathlib.Path(ledger_path)
    blockers: list[str] = []
    warnings: list[str] = []
    if ctx.get("rhythm_trend_forecast_enabled") is not True:
        blockers.append("rhythm_trend_forecast_enabled_not_true")
    if ctx.get("read_only_forecast") is not True:
        blockers.append("read_only_forecast_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")
    if ctx.get("replace_ledger_root") is True:
        blockers.append("replace_ledger_root_requested")

    try:
        entries = _read_jsonl(path)
    except Exception as exc:  # pragma: no cover
        entries = []
        blockers.append("ledger_jsonl_parse_failed")
        warnings.append(str(exc))
    if not entries:
        blockers.append("ledger_empty")

    requested_window = max(1, _int(ctx.get("trend_window_size"), 8))
    window_entries = entries[-requested_window:]
    payloads = [_entry_payload(entry) for entry in window_entries]
    pressure_values = [_float(payload.get("process_tensor_pressure_score"), _float(entry.get("process_tensor_pressure_score"), 0.0)) for entry, payload in zip(window_entries, payloads)]
    stability_values = [_float(entry.get("rhythm_stability_score"), _float(payload.get("rhythm_stability_score"), 0.0)) for entry, payload in zip(window_entries, payloads)]
    completion_values = [_completion_ratio(entry) for entry in window_entries]
    observe_ratio = _ratio(window_entries, lambda e: _stop_reason(e) == "process_tensor_observe_required")
    full_ratio = _ratio(window_entries, lambda e: _stop_reason(e) in {"process_tensor_full_history_required", "process_tensor_full_history_after_tick"})
    freeze_ratio = _ratio(window_entries, lambda e: _stop_reason(e) == "freeze_required")

    mean_pressure = _mean(pressure_values)
    mean_stability = _mean(stability_values)
    mean_completion = _mean(completion_values)
    pressure_tr = _trend(pressure_values, "pressure_rising", "pressure_falling", "pressure_flat")
    stability_tr = _trend(stability_values, "stability_rising", "stability_falling", "stability_flat")
    completion_tr = _trend(completion_values, "completion_rising", "completion_falling", "completion_flat")
    observe_tr = "observe_stop_present" if observe_ratio > 0 else "observe_stop_absent"
    full_tr = "full_history_stop_present" if full_ratio > 0 else "full_history_stop_absent"
    freeze_tr = "freeze_stop_present" if freeze_ratio > 0 else "freeze_stop_absent"
    bias, cadence_hint, risk_class = _forecast_bias(
        pressure=mean_pressure,
        stability=mean_stability,
        completion=mean_completion,
        observe=observe_ratio,
        full=full_ratio,
        freeze=freeze_ratio,
        pressure_trend=pressure_tr,
        stability_trend=stability_tr,
    )
    confidence = max(0.0, min(1.0, len(window_entries) / max(1, requested_window)))
    root_digest = _ledger_root_digest(entries)
    last_digest = _entry_digest(entries[-1]) if entries else None
    packet_core = {
        "ledger_root_digest": root_digest,
        "source_last_entry_digest": last_digest,
        "trend_window_size": len(window_entries),
        "pressure_trend": pressure_tr,
        "stability_trend": stability_tr,
        "completion_trend": completion_tr,
        "forecast_window_bias": bias,
        "forecast_cadence_mode_hint": cadence_hint,
        "forecast_risk_class": risk_class,
        "projection_only": True,
    }
    packet_id = "qi-rhythm-forecast-" + _sha_obj(packet_core)[:16]
    forecast_packet = dict(packet_core)
    forecast_packet.update({
        "forecast_packet_id": packet_id,
        "forecast_version": "kuuos_runtime_daemon_qi_rhythm_trend_forecast_v0_1",
        "mean_pressure_score": mean_pressure,
        "mean_stability_score": mean_stability,
        "mean_completion_ratio": mean_completion,
        "observe_ratio": observe_ratio,
        "full_history_ratio": full_ratio,
        "freeze_ratio": freeze_ratio,
        "replaces_ledger_root": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })
    ready = not blockers
    return QiRhythmTrendForecastResult(
        forecast_version="kuuos_runtime_daemon_qi_rhythm_trend_forecast_v0_1",
        forecast_status="QI_RHYTHM_TREND_FORECAST_READY" if ready else "QI_RHYTHM_TREND_FORECAST_BLOCKED",
        ledger_path=str(path),
        ledger_entry_count=len(entries),
        ledger_root_digest=root_digest,
        source_last_entry_digest=last_digest,
        trend_window_size=len(window_entries),
        pressure_trend=pressure_tr,
        stability_trend=stability_tr,
        completion_trend=completion_tr,
        observe_trend=observe_tr,
        full_history_trend=full_tr,
        freeze_trend=freeze_tr,
        mean_pressure_score=mean_pressure,
        mean_stability_score=mean_stability,
        mean_completion_ratio=mean_completion,
        observe_ratio=observe_ratio,
        full_history_ratio=full_ratio,
        freeze_ratio=freeze_ratio,
        forecast_window_bias=bias,
        forecast_cadence_mode_hint=cadence_hint,
        forecast_risk_class=risk_class,
        forecast_confidence=confidence,
        forecast_packet_id=packet_id,
        projection_only=True,
        replaces_ledger_root=False,
        trend_summary_authority="projection_only_not_receipt_root",
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        forecast_packet=forecast_packet if ready else {},
        forecast_blockers=blockers,
        forecast_warnings=warnings,
    )
