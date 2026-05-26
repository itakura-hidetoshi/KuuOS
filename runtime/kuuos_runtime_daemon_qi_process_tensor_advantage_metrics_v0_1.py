#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProcessTensorAdvantageMetrics:
    metrics_version: str
    metrics_status: str
    history_depth: int
    transition_visibility_ratio: float
    memory_link_density: float
    nonmarkov_link_density: float
    multi_time_correlation_visibility: float
    recoverability_branching_capacity: float
    observation_debt_resolution_priority: float
    memory_kernel_preservation_score: float
    safe_reentry_window_score: float
    process_tensor_advantage_score: float
    process_tensor_advantage_level: str
    recommended_next_process_focus: str
    blockers: list[str]
    warnings: list[str]
    metrics_only: bool
    read_only: bool
    grants_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _clamp01(value: float) -> float:
    if value < 0:
        return 0.0
    if value > 1:
        return 1.0
    return round(value, 6)


def _history(raw_state: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = raw_state.get("process_history", [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _ratio(history: list[dict[str, Any]], key: str) -> float:
    if not history:
        return 0.0
    return _clamp01(sum(1 for item in history if bool(item.get(key))) / len(history))


def _projection_status(projection_summary: Mapping[str, Any], key: str) -> str | None:
    statuses = projection_summary.get("projection_statuses")
    if isinstance(statuses, dict):
        value = statuses.get(key)
        return str(value) if value is not None else None
    value = projection_summary.get(key)
    return str(value) if value is not None else None


def _status_score(status: str | None) -> float:
    if status is None:
        return 0.5
    normalized = status.lower()
    if any(token in normalized for token in ["ready", "ok", "low", "clear", "valid", "available"]):
        return 1.0
    if any(token in normalized for token in ["watch", "medium", "partial", "needs"]):
        return 0.5
    if any(token in normalized for token in ["blocked", "hold", "high", "missing", "debt"]):
        return 0.0
    return 0.5


def _level(score: float, blockers: list[str]) -> str:
    if blockers:
        return "blocked"
    if score >= 0.75:
        return "high"
    if score >= 0.5:
        return "medium"
    if score >= 0.25:
        return "low"
    return "minimal"


def _focus(*, blockers: list[str], observation_priority: float, recoverability_capacity: float, memory_score: float, safe_reentry: float) -> str:
    if blockers:
        return "repair_process_tensor_inputs"
    if observation_priority >= 0.7:
        return "resolve_observation_debt"
    if recoverability_capacity < 0.4:
        return "open_recoverability_branch"
    if memory_score < 0.5:
        return "preserve_memory_kernel"
    if safe_reentry < 0.5:
        return "widen_safe_reentry_window"
    return "continue_process_tensor_supervision"


def compute_qi_process_tensor_advantage_metrics(
    *,
    raw_state: Mapping[str, Any],
    projection_summary: Mapping[str, Any] | None = None,
) -> QiProcessTensorAdvantageMetrics:
    summary = projection_summary or {}
    history = _history(raw_state)
    depth = len(history)
    blockers: list[str] = []
    warnings: list[str] = []

    if depth == 0:
        blockers.append("process_history_missing")
    if not raw_state.get("physical_process_visible", False):
        warnings.append("physical_process_visibility_missing")
    if not raw_state.get("thermodynamic_activity_visible", False):
        warnings.append("thermodynamic_activity_visibility_missing")

    transition_ratio = _ratio(history, "transition_visible")
    memory_density = _ratio(history, "memory_link_visible")
    nonmarkov_density = _ratio(history, "nonmarkov_link_visible")
    multi_time_visibility = _clamp01((transition_ratio + memory_density + nonmarkov_density) / 3.0)

    recovery_status_score = _status_score(_projection_status(summary, "recoverability"))
    health_status_score = _status_score(_projection_status(summary, "health"))
    observation_status_score = _status_score(_projection_status(summary, "observation_debt"))
    compaction_status_score = _status_score(_projection_status(summary, "trace_compaction"))

    recoverability_branching_capacity = _clamp01((multi_time_visibility * 0.45) + (nonmarkov_density * 0.25) + (recovery_status_score * 0.30))
    observation_debt_resolution_priority = _clamp01((1.0 - observation_status_score) * 0.55 + (1.0 - multi_time_visibility) * 0.25 + (1.0 - transition_ratio) * 0.20)
    memory_kernel_preservation_score = _clamp01((memory_density * 0.50) + (compaction_status_score * 0.30) + (nonmarkov_density * 0.20))
    safe_reentry_window_score = _clamp01((recoverability_branching_capacity * 0.45) + (health_status_score * 0.35) + (memory_kernel_preservation_score * 0.20))

    advantage_score = _clamp01(
        0.22 * multi_time_visibility
        + 0.22 * recoverability_branching_capacity
        + 0.18 * memory_kernel_preservation_score
        + 0.18 * safe_reentry_window_score
        + 0.12 * nonmarkov_density
        + 0.08 * (1.0 - observation_debt_resolution_priority)
    )
    level = _level(advantage_score, blockers)
    focus = _focus(
        blockers=blockers,
        observation_priority=observation_debt_resolution_priority,
        recoverability_capacity=recoverability_branching_capacity,
        memory_score=memory_kernel_preservation_score,
        safe_reentry=safe_reentry_window_score,
    )

    status = "QI_PROCESS_TENSOR_ADVANTAGE_READY" if not blockers else "QI_PROCESS_TENSOR_ADVANTAGE_BLOCKED"
    return QiProcessTensorAdvantageMetrics(
        metrics_version="kuuos_runtime_daemon_qi_process_tensor_advantage_metrics_v0_1",
        metrics_status=status,
        history_depth=depth,
        transition_visibility_ratio=transition_ratio,
        memory_link_density=memory_density,
        nonmarkov_link_density=nonmarkov_density,
        multi_time_correlation_visibility=multi_time_visibility,
        recoverability_branching_capacity=recoverability_branching_capacity,
        observation_debt_resolution_priority=observation_debt_resolution_priority,
        memory_kernel_preservation_score=memory_kernel_preservation_score,
        safe_reentry_window_score=safe_reentry_window_score,
        process_tensor_advantage_score=advantage_score,
        process_tensor_advantage_level=level,
        recommended_next_process_focus=focus,
        blockers=blockers,
        warnings=warnings,
        metrics_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compute KuuOS Qi process tensor advantage metrics v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--projection-summary", type=Path, default=None)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw_state = _read_json(args.raw_state)
    projection_summary = _read_json(args.projection_summary) if args.projection_summary else {}
    result = compute_qi_process_tensor_advantage_metrics(raw_state=raw_state, projection_summary=projection_summary)
    if args.write:
        _write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.metrics_status == "QI_PROCESS_TENSOR_ADVANTAGE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
