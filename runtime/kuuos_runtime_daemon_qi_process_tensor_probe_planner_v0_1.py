#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProcessTensorProbePlan:
    planner_version: str
    probe_plan_status: str
    recommended_probe_type: str
    probe_target_time_slice: str
    probe_expected_recoverability_gain: float
    probe_expected_observation_debt_reduction: float
    probe_risk_level: str
    probe_blockers: list[str]
    probe_warnings: list[str]
    probe_plan_only: bool
    read_only: bool
    metrics_only: bool
    authority: str = "none"
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _clamp01(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 0.0
    if numeric < 0:
        return 0.0
    if numeric > 1:
        return 1.0
    return round(numeric, 6)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _latest_metrics(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    for key in ("latest_process_tensor_advantage_metrics", "process_tensor_advantage_metrics"):
        nested = payload.get(key)
        if isinstance(nested, Mapping):
            return nested
    return payload


def _history(raw_state: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = raw_state.get("process_history", [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _target_slice(raw_state: Mapping[str, Any], observation_debt: Mapping[str, Any]) -> str:
    for key in ("highest_priority_time_slice", "target_time_slice", "latest_debt_time_slice", "time_slice"):
        if observation_debt.get(key):
            return str(observation_debt[key])
    history = _history(raw_state)
    if history:
        latest = history[-1]
        for key in ("time_slice", "tick_id", "step_id", "timestamp"):
            if latest.get(key):
                return str(latest[key])
    return "latest_visible_process_slice"


def _status_score(status: Any) -> float:
    if status is None:
        return 0.5
    text = str(status).lower()
    if any(t in text for t in ("ready", "ok", "low", "clear", "valid", "available")):
        return 1.0
    if any(t in text for t in ("watch", "medium", "partial", "needs", "unknown")):
        return 0.5
    if any(t in text for t in ("blocked", "hold", "high", "missing", "debt", "unsafe")):
        return 0.0
    return 0.5


def _observation_priority(metrics: Mapping[str, Any], debt: Mapping[str, Any], summary: Mapping[str, Any]) -> float:
    for key in ("observation_debt_resolution_priority", "priority"):
        if debt.get(key) is not None:
            return _clamp01(debt[key])
    pending = debt.get("pending_count", debt.get("unresolved_count"))
    if isinstance(pending, (int, float)):
        return _clamp01(pending / 5.0)
    statuses = summary.get("projection_statuses")
    status = statuses.get("observation_debt") if isinstance(statuses, Mapping) else summary.get("observation_debt")
    if status is not None:
        return _clamp01(1.0 - _status_score(status))
    return _clamp01(metrics.get("observation_debt_resolution_priority", 0.0))


def _recoverability_score(recovery: Mapping[str, Any], summary: Mapping[str, Any]) -> float:
    for key in ("recoverability_score", "recoverability_branching_capacity", "score"):
        if recovery.get(key) is not None:
            return _clamp01(recovery[key])
    if recovery.get("status") is not None:
        return _status_score(recovery["status"])
    statuses = summary.get("projection_statuses")
    status = statuses.get("recoverability") if isinstance(statuses, Mapping) else summary.get("recoverability")
    return _status_score(status)


def _choose_probe(metrics: Mapping[str, Any], obs: float, rec: float, rec_status: float, mem: float, safe: float, nonmarkov: float, multi: float, transition: float) -> str:
    focus = str(metrics.get("recommended_next_process_focus", ""))
    if focus == "resolve_observation_debt" or obs >= 0.72:
        return "observation_debt_probe"
    if focus == "open_recoverability_branch" or rec < 0.4 or rec_status < 0.35:
        return "recoverability_branch_probe"
    if focus == "preserve_memory_kernel" or mem < 0.45:
        return "memory_kernel_probe"
    if focus == "widen_safe_reentry_window" or safe < 0.45:
        return "safe_reentry_window_probe"
    if nonmarkov < 0.45:
        return "nonmarkov_memory_link_probe"
    if multi < 0.55 or transition < 0.55:
        return "multi_time_correlation_probe"
    return "continue_process_tensor_supervision_probe"


def _risk(safe: float, mem: float, obs: float, rec_status: float) -> str:
    if safe < 0.25 or mem < 0.25:
        return "high"
    if safe < 0.5 or mem < 0.5 or rec_status < 0.35 or obs >= 0.8:
        return "medium"
    return "low"


def _expected_gain(probe: str, rec: float, rec_status: float, mem: float, safe: float, nonmarkov: float, multi: float) -> float:
    rec_gap = 1.0 - max(rec, rec_status)
    if probe == "recoverability_branch_probe":
        return _clamp01(0.55 * rec_gap + 0.20 * (1.0 - safe) + 0.10 * nonmarkov)
    if probe == "safe_reentry_window_probe":
        return _clamp01(0.35 * (1.0 - safe) + 0.25 * rec_gap + 0.15 * mem)
    if probe == "memory_kernel_probe":
        return _clamp01(0.20 * rec_gap + 0.25 * (1.0 - mem) + 0.10 * nonmarkov)
    if probe == "nonmarkov_memory_link_probe":
        return _clamp01(0.25 * (1.0 - nonmarkov) + 0.20 * rec_gap)
    if probe == "multi_time_correlation_probe":
        return _clamp01(0.25 * (1.0 - multi) + 0.15 * rec_gap)
    if probe == "observation_debt_probe":
        return _clamp01(0.15 * rec_gap + 0.10 * (1.0 - multi))
    return _clamp01(0.05 * (1.0 - rec))


def _expected_debt_reduction(probe: str, obs: float, transition: float, multi: float) -> float:
    if probe == "observation_debt_probe":
        return _clamp01(0.60 * obs + 0.20 * (1.0 - transition) + 0.10 * (1.0 - multi))
    if probe == "multi_time_correlation_probe":
        return _clamp01(0.25 * obs + 0.25 * (1.0 - multi))
    if probe == "nonmarkov_memory_link_probe":
        return _clamp01(0.20 * obs + 0.10 * (1.0 - multi))
    if probe == "recoverability_branch_probe":
        return _clamp01(0.15 * obs)
    if probe == "safe_reentry_window_probe":
        return _clamp01(0.10 * obs)
    if probe == "memory_kernel_probe":
        return _clamp01(0.08 * obs)
    return _clamp01(0.03 * obs)


def plan_qi_process_tensor_probe(
    *,
    latest_process_tensor_advantage_metrics: Mapping[str, Any],
    raw_state: Mapping[str, Any] | None = None,
    projection_summary: Mapping[str, Any] | None = None,
    observation_debt: Mapping[str, Any] | None = None,
    recoverability_status: Mapping[str, Any] | None = None,
    memory_kernel_preservation_score: float | None = None,
    safe_reentry_window_score: float | None = None,
) -> QiProcessTensorProbePlan:
    metrics = _latest_metrics(_mapping(latest_process_tensor_advantage_metrics))
    state = _mapping(raw_state or {})
    summary = _mapping(projection_summary or {})
    debt = _mapping(observation_debt or {})
    recovery = _mapping(recoverability_status or {})
    blockers: list[str] = []
    warnings: list[str] = []

    if not metrics:
        blockers.append("process_tensor_advantage_metrics_missing")
    if metrics and metrics.get("metrics_status") != "QI_PROCESS_TENSOR_ADVANTAGE_READY":
        blockers.append("process_tensor_advantage_not_ready")
    if str(metrics.get("process_tensor_advantage_level", "")).lower() == "blocked":
        blockers.append("process_tensor_advantage_level_blocked")
    if int(metrics.get("history_depth", 0) or 0) <= 0:
        blockers.append("process_history_missing")

    transition = _clamp01(metrics.get("transition_visibility_ratio", 0.0))
    nonmarkov = _clamp01(metrics.get("nonmarkov_link_density", 0.0))
    multi = _clamp01(metrics.get("multi_time_correlation_visibility", 0.0))
    rec = _clamp01(metrics.get("recoverability_branching_capacity", 0.0))
    mem = _clamp01(memory_kernel_preservation_score if memory_kernel_preservation_score is not None else metrics.get("memory_kernel_preservation_score", 0.0))
    safe = _clamp01(safe_reentry_window_score if safe_reentry_window_score is not None else metrics.get("safe_reentry_window_score", 0.0))
    obs = _observation_priority(metrics, debt, summary)
    rec_status = _recoverability_score(recovery, summary)

    if mem < 0.35:
        warnings.append("memory_kernel_preservation_low")
    if safe < 0.35:
        warnings.append("safe_reentry_window_narrow")
    if obs >= 0.75:
        warnings.append("observation_debt_priority_high")

    target = _target_slice(state, debt)
    if blockers:
        return QiProcessTensorProbePlan(
            planner_version="kuuos_runtime_daemon_qi_process_tensor_probe_planner_v0_1",
            probe_plan_status="QI_PROCESS_TENSOR_PROBE_PLAN_BLOCKED",
            recommended_probe_type="repair_process_tensor_inputs",
            probe_target_time_slice=target,
            probe_expected_recoverability_gain=0.0,
            probe_expected_observation_debt_reduction=0.0,
            probe_risk_level="blocked",
            probe_blockers=blockers,
            probe_warnings=warnings,
            probe_plan_only=True,
            read_only=True,
            metrics_only=True,
        )

    probe = _choose_probe(metrics, obs, rec, rec_status, mem, safe, nonmarkov, multi, transition)
    status = "QI_PROCESS_TENSOR_PROBE_PLAN_READY_WITH_WARNINGS" if warnings else "QI_PROCESS_TENSOR_PROBE_PLAN_READY"
    return QiProcessTensorProbePlan(
        planner_version="kuuos_runtime_daemon_qi_process_tensor_probe_planner_v0_1",
        probe_plan_status=status,
        recommended_probe_type=probe,
        probe_target_time_slice=target,
        probe_expected_recoverability_gain=_expected_gain(probe, rec, rec_status, mem, safe, nonmarkov, multi),
        probe_expected_observation_debt_reduction=_expected_debt_reduction(probe, obs, transition, multi),
        probe_risk_level=_risk(safe, mem, obs, rec_status),
        probe_blockers=[],
        probe_warnings=warnings,
        probe_plan_only=True,
        read_only=True,
        metrics_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan KuuOS Qi process tensor probes v0.1 without executing them")
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--raw-state", type=Path, default=None)
    parser.add_argument("--projection-summary", type=Path, default=None)
    parser.add_argument("--observation-debt", type=Path, default=None)
    parser.add_argument("--recoverability-status", type=Path, default=None)
    parser.add_argument("--memory-kernel-preservation-score", type=float, default=None)
    parser.add_argument("--safe-reentry-window-score", type=float, default=None)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    plan = plan_qi_process_tensor_probe(
        latest_process_tensor_advantage_metrics=_read_json(args.metrics),
        raw_state=_read_json(args.raw_state),
        projection_summary=_read_json(args.projection_summary),
        observation_debt=_read_json(args.observation_debt),
        recoverability_status=_read_json(args.recoverability_status),
        memory_kernel_preservation_score=args.memory_kernel_preservation_score,
        safe_reentry_window_score=args.safe_reentry_window_score,
    )
    if args.write:
        _write_json(args.write, plan.to_dict())
    print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if plan.probe_plan_status != "QI_PROCESS_TENSOR_PROBE_PLAN_BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
