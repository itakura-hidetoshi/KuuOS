#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
except ModuleNotFoundError:
    from kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status


@dataclass(frozen=True)
class KuuOSQiProcessTensorTraceCompactionPlan:
    planner_version: str
    planner_status: str
    compaction_plan_status: str
    recommended_compaction_action: str
    compaction_priority: str
    compaction_urgency_score: float
    retain_targets: list[str]
    summarize_targets: list[str]
    compact_targets: list[str]
    carry_forward_targets: list[str]
    no_compaction_targets: list[str]
    compaction_blockers: list[str]
    process_history_length: int
    qi_process_tensor_visible: bool
    transition_continuity_visible: bool
    memory_continuity_visible: bool
    nonmarkov_memory_visible: bool
    observation_debt_status: str | None
    observation_action: str | None
    health_next_operator_action: str | None
    recoverability_status: str | None
    runtime_hot_path_tier: str
    validation_tier: str
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _b(value: Any) -> bool:
    return bool(value)


def _i(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _lst(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []


def _dedup(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _summary_from_status(daemon_dir: Path) -> dict[str, Any]:
    status = read_runtime_daemon_status(daemon_dir)
    summary = status.latest_qi_process_tensor_summary
    return dict(summary) if isinstance(summary, Mapping) else {}


def compile_qi_process_tensor_trace_compaction_plan(
    *,
    process_tensor_summary: Mapping[str, Any] | None = None,
    health_projection: Mapping[str, Any] | None = None,
    recoverability_projection: Mapping[str, Any] | None = None,
    observation_debt_schedule: Mapping[str, Any] | None = None,
) -> KuuOSQiProcessTensorTraceCompactionPlan:
    summary = process_tensor_summary or {}
    health = health_projection or {}
    recoverability = recoverability_projection or {}
    observation = observation_debt_schedule or {}

    process_visible = _b(summary.get("process_tensor_visible"))
    transition_visible = _b(summary.get("transition_continuity_visible"))
    memory_visible = _b(summary.get("memory_continuity_visible"))
    nonmarkov_visible = _b(summary.get("nonmarkov_memory_visible"))
    history_len = _i(summary.get("process_history_length"), 0)

    health_action = health.get("next_operator_action")
    recoverability_status = recoverability.get("recoverability_status") or health.get("recoverability_status")
    observation_status = observation.get("observation_debt_status")
    observation_action = observation.get("recommended_observation_action")
    compaction_targets_from_observation = _lst(observation.get("compaction_targets"))
    hold_reasons = _lst(observation.get("hold_reasons"))

    retain_targets: list[str] = []
    summarize_targets: list[str] = []
    compact_targets: list[str] = []
    carry_forward_targets: list[str] = []
    no_compaction_targets: list[str] = []
    blockers: list[str] = []
    urgency = 0.0

    retain_targets.extend([
        "daemon_result_v0_1.json",
        "daemon_qi_process_tensor_health_projection_v0_1.json",
        "daemon_qi_process_tensor_recoverability_projection_v0_1.json",
    ])
    carry_forward_targets.extend(["latest_raw_state", "latest_state_bundle"])

    if hold_reasons:
        blockers.extend(hold_reasons)
        no_compaction_targets.extend(["step_trace", "process_history", "state_bundle"])
        urgency = max(urgency, 0.9)

    if not process_visible:
        blockers.append("process_tensor_not_visible")
        no_compaction_targets.append("process_history")
        urgency = max(urgency, 0.85)

    if not transition_visible:
        blockers.append("transition_continuity_missing")
        retain_targets.append("adjacent_transition_edges")
        no_compaction_targets.append("transition_witnesses")
        urgency = max(urgency, 0.75)

    if not memory_visible:
        blockers.append("memory_continuity_missing")
        retain_targets.append("memory_link_witnesses")
        no_compaction_targets.append("memory_continuity_witnesses")
        urgency = max(urgency, 0.7)

    if not nonmarkov_visible:
        blockers.append("nonmarkov_memory_missing")
        retain_targets.append("nonmarkov_history_witnesses")
        no_compaction_targets.append("nonmarkov_memory_witnesses")
        urgency = max(urgency, 0.6)

    if history_len >= 5:
        summarize_targets.append("older_process_history_prefix")
        compact_targets.append("older_step_trace_prefix")
        urgency = max(urgency, 0.5)
    if history_len >= 10:
        summarize_targets.append("middle_process_history_window")
        compact_targets.append("middle_step_trace_window")
        urgency = max(urgency, 0.75)

    if health_action == "compact_trace" or observation_action == "compact_trace":
        compact_targets.extend(compaction_targets_from_observation or ["step_trace", "process_history", "state_bundle"])
        summarize_targets.extend(["process_history_summary", "step_trace_summary"])
        urgency = max(urgency, 0.8)

    if recoverability_status in {"UNSAFE_RECOVERY", "LOCAL_RECOVERY_BLOCKED"}:
        blockers.append(str(recoverability_status))
        no_compaction_targets.extend(["executor_receipt", "invocation_boundary", "reentry_license_gate"])
        urgency = max(urgency, 0.95)

    retain_targets = _dedup(retain_targets)
    summarize_targets = _dedup(summarize_targets)
    compact_targets = _dedup(compact_targets)
    carry_forward_targets = _dedup(carry_forward_targets)
    no_compaction_targets = _dedup(no_compaction_targets)
    blockers = _dedup(blockers)

    if blockers:
        status = "COMPACTION_HELD"
        action = "hold_compaction"
        priority = "critical" if "UNSAFE_RECOVERY" in blockers else "high"
    elif compact_targets:
        status = "COMPACTION_READY"
        action = "compact_trace"
        priority = "high" if urgency >= 0.75 else "medium"
    elif summarize_targets:
        status = "SUMMARY_ONLY_COMPACTION_READY"
        action = "summarize_trace"
        priority = "medium"
    else:
        status = "NO_COMPACTION_DEBT"
        action = "no_action"
        priority = "low"

    return KuuOSQiProcessTensorTraceCompactionPlan(
        planner_version="kuuos_runtime_daemon_qi_process_tensor_trace_compaction_planner_v0_1",
        planner_status="QI_PROCESS_TENSOR_TRACE_COMPACTION_PLANNED",
        compaction_plan_status=status,
        recommended_compaction_action=action,
        compaction_priority=priority,
        compaction_urgency_score=round(max(0.0, min(1.0, urgency)), 6),
        retain_targets=retain_targets,
        summarize_targets=summarize_targets,
        compact_targets=compact_targets,
        carry_forward_targets=carry_forward_targets,
        no_compaction_targets=no_compaction_targets,
        compaction_blockers=blockers,
        process_history_length=history_len,
        qi_process_tensor_visible=process_visible,
        transition_continuity_visible=transition_visible,
        memory_continuity_visible=memory_visible,
        nonmarkov_memory_visible=nonmarkov_visible,
        observation_debt_status=str(observation_status) if observation_status is not None else None,
        observation_action=str(observation_action) if observation_action is not None else None,
        health_next_operator_action=str(health_action) if health_action is not None else None,
        recoverability_status=str(recoverability_status) if recoverability_status is not None else None,
        runtime_hot_path_tier="T0_hot_path_compaction_planner",
        validation_tier="T3_runtime_full_check",
    )


def read_and_compile_qi_process_tensor_trace_compaction_plan(daemon_dir: Path) -> KuuOSQiProcessTensorTraceCompactionPlan:
    daemon_dir = Path(daemon_dir)
    return compile_qi_process_tensor_trace_compaction_plan(
        process_tensor_summary=_summary_from_status(daemon_dir),
        health_projection=_read_json(daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json") or {},
        recoverability_projection=_read_json(daemon_dir / "daemon_qi_process_tensor_recoverability_projection_v0_1.json") or {},
        observation_debt_schedule=_read_json(daemon_dir / "daemon_qi_process_tensor_observation_debt_schedule_v0_1.json") or {},
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor trace compaction plan v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    plan = read_and_compile_qi_process_tensor_trace_compaction_plan(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_trace_compaction_plan_v0_1.json", plan.to_dict())
    print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
