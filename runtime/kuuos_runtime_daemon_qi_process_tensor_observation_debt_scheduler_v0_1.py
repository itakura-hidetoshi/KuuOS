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
class KuuOSQiProcessTensorObservationDebtSchedule:
    scheduler_version: str
    scheduler_status: str
    observation_debt_status: str
    recommended_observation_action: str
    observation_priority: str
    observation_urgency_score: float
    observation_targets: list[str]
    reobserve_targets: list[str]
    compaction_targets: list[str]
    hold_reasons: list[str]
    missing_process_requirements: list[str]
    required_evidence_updates: list[str]
    process_history_requirements: list[str]
    process_history_length: int
    qi_process_tensor_visible: bool
    transition_continuity_visible: bool
    memory_continuity_visible: bool
    nonmarkov_memory_visible: bool
    health_next_operator_action: str | None
    recoverability_status: str | None
    recovery_unsafe: bool
    recovery_blockers: list[str]
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


def _summary_from_status(daemon_dir: Path) -> dict[str, Any]:
    status = read_runtime_daemon_status(daemon_dir)
    summary = status.latest_qi_process_tensor_summary
    return dict(summary) if isinstance(summary, Mapping) else {}


def _dedup(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def compile_qi_process_tensor_observation_debt_schedule(
    *,
    process_tensor_summary: Mapping[str, Any] | None = None,
    health_projection: Mapping[str, Any] | None = None,
    recoverability_projection: Mapping[str, Any] | None = None,
) -> KuuOSQiProcessTensorObservationDebtSchedule:
    summary = process_tensor_summary or {}
    health = health_projection or {}
    recoverability = recoverability_projection or {}

    process_visible = _b(summary.get("process_tensor_visible"))
    transition_visible = _b(summary.get("transition_continuity_visible"))
    memory_visible = _b(summary.get("memory_continuity_visible"))
    nonmarkov_visible = _b(summary.get("nonmarkov_memory_visible"))
    history_len = _i(summary.get("process_history_length"), 0)
    missing = _lst(summary.get("missing_process_requirements"))

    health_action = health.get("next_operator_action")
    recoverability_status = recoverability.get("recoverability_status") or health.get("recoverability_status")
    recovery_unsafe = _b(recoverability.get("recovery_unsafe") or health.get("recovery_unsafe"))
    recovery_blockers = _lst(recoverability.get("recovery_blockers") or health.get("recovery_blockers"))

    observation_targets: list[str] = []
    reobserve_targets: list[str] = []
    compaction_targets: list[str] = []
    hold_reasons: list[str] = []
    required_evidence_updates: list[str] = []
    history_requirements: list[str] = []
    urgency = 0.0

    if recovery_unsafe:
        hold_reasons.append("recovery_unsafe")
        urgency = max(urgency, 1.0)

    if not process_visible:
        observation_targets.extend(["physical_process_visible", "thermodynamic_activity_visible", "process_history"])
        required_evidence_updates.extend(["physical_process_evidence", "thermodynamic_activity_evidence", "process_history_support"])
        history_requirements.append("add_at_least_three_process_history_steps_or_explicit_process_tensor")
        urgency = max(urgency, 0.95)

    if history_len < 3:
        observation_targets.append("process_history_min_length")
        history_requirements.append("process_history_length_at_least_3")
        urgency = max(urgency, 0.8)

    if not transition_visible:
        reobserve_targets.extend(["transition_continuity", "adjacent_process_step_links"])
        required_evidence_updates.append("transition_visibility_evidence")
        urgency = max(urgency, 0.85)

    if not memory_visible:
        observation_targets.extend(["memory_continuity", "process_step_memory_links"])
        required_evidence_updates.append("memory_link_evidence")
        urgency = max(urgency, 0.75)

    if not nonmarkov_visible:
        reobserve_targets.extend(["nonmarkov_memory_link", "process_tensor_history_dependence"])
        required_evidence_updates.append("nonmarkov_memory_evidence")
        urgency = max(urgency, 0.55)

    if health_action == "compact_trace":
        compaction_targets.extend(["step_trace", "process_history", "state_bundle"])
        urgency = max(urgency, 0.7)
    elif health_action == "hold":
        hold_reasons.append("health_projection_requests_hold")
        urgency = max(urgency, 0.9)
    elif health_action == "reobserve":
        reobserve_targets.append("health_projection_reobserve_target")
        urgency = max(urgency, 0.75)

    for blocker in recovery_blockers:
        if blocker == "observation_debt":
            observation_targets.append("observation_debt_blocker")
        elif blocker == "transition_gap":
            reobserve_targets.append("transition_gap_blocker")
        elif blocker == "memory_gap":
            observation_targets.append("memory_gap_blocker")
        elif blocker == "compaction_debt":
            compaction_targets.append("compaction_debt_blocker")
        elif blocker in {"boundary_blocker", "reentry_blocker"}:
            hold_reasons.append(blocker)

    observation_targets = _dedup(observation_targets)
    reobserve_targets = _dedup(reobserve_targets)
    compaction_targets = _dedup(compaction_targets)
    hold_reasons = _dedup(hold_reasons)
    required_evidence_updates = _dedup(required_evidence_updates)
    history_requirements = _dedup(history_requirements + missing)

    if hold_reasons:
        status = "OBSERVATION_DEBT_HELD"
        action = "hold"
        priority = "critical" if recovery_unsafe else "high"
    elif compaction_targets and not observation_targets and not reobserve_targets:
        status = "TRACE_COMPACTION_DEBT"
        action = "compact_trace"
        priority = "medium"
    elif observation_targets:
        status = "OBSERVATION_DEBT_OPEN"
        action = "observe"
        priority = "high" if urgency >= 0.8 else "medium"
    elif reobserve_targets:
        status = "REOBSERVATION_DEBT_OPEN"
        action = "reobserve"
        priority = "high" if urgency >= 0.8 else "medium"
    else:
        status = "NO_OBSERVATION_DEBT"
        action = "no_action"
        priority = "low"

    return KuuOSQiProcessTensorObservationDebtSchedule(
        scheduler_version="kuuos_runtime_daemon_qi_process_tensor_observation_debt_scheduler_v0_1",
        scheduler_status="QI_PROCESS_TENSOR_OBSERVATION_DEBT_SCHEDULED",
        observation_debt_status=status,
        recommended_observation_action=action,
        observation_priority=priority,
        observation_urgency_score=round(max(0.0, min(1.0, urgency)), 6),
        observation_targets=observation_targets,
        reobserve_targets=reobserve_targets,
        compaction_targets=compaction_targets,
        hold_reasons=hold_reasons,
        missing_process_requirements=missing,
        required_evidence_updates=required_evidence_updates,
        process_history_requirements=history_requirements,
        process_history_length=history_len,
        qi_process_tensor_visible=process_visible,
        transition_continuity_visible=transition_visible,
        memory_continuity_visible=memory_visible,
        nonmarkov_memory_visible=nonmarkov_visible,
        health_next_operator_action=str(health_action) if health_action is not None else None,
        recoverability_status=str(recoverability_status) if recoverability_status is not None else None,
        recovery_unsafe=recovery_unsafe,
        recovery_blockers=recovery_blockers,
        runtime_hot_path_tier="T0_hot_path_observation_scheduler",
        validation_tier="T3_runtime_full_check",
    )


def read_and_compile_qi_process_tensor_observation_debt_schedule(daemon_dir: Path) -> KuuOSQiProcessTensorObservationDebtSchedule:
    daemon_dir = Path(daemon_dir)
    return compile_qi_process_tensor_observation_debt_schedule(
        process_tensor_summary=_summary_from_status(daemon_dir),
        health_projection=_read_json(daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json") or {},
        recoverability_projection=_read_json(daemon_dir / "daemon_qi_process_tensor_recoverability_projection_v0_1.json") or {},
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor observation debt schedule v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    schedule = read_and_compile_qi_process_tensor_observation_debt_schedule(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_observation_debt_schedule_v0_1.json", schedule.to_dict())
    print(json.dumps(schedule.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
