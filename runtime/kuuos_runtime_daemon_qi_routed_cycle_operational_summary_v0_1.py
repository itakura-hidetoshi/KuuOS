#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiRoutedCycleOperationalSummary:
    summary_version: str
    summary_status: str
    summary_decision: str
    recommended_next_runtime_mode: str
    recommended_next_reason: str
    daemon_status: str | None
    daemon_stop_reason: str | None
    route_decision: str | None
    next_outer_action: str | None
    dispatcher_status: str | None
    recovery_feedback_signal: str | None
    policy_shadow_admission_decision: str | None
    policy_shadow_score: float | None
    policy_shadow_grade: str | None
    health_projection_status: str | None
    recoverability_projection_status: str | None
    observation_debt_status: str | None
    trace_compaction_status: str | None
    compact_before_next_tick: bool
    reobserve_before_next_tick: bool
    hold_until_observation: bool
    bounded_reentry_candidate: bool
    operational_blockers: list[str]
    operational_warnings: list[str]
    operational_positive_signals: list[str]
    source_paths: dict[str, str | None]
    one_page_summary: dict[str, Any]
    operational_summary_only: bool
    read_only: bool
    candidate_only: bool
    nonfinal_marker: bool
    grants_execution_authority: bool = False
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


def _s(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    return str(value) if value is not None else None


def _b(payload: Mapping[str, Any], key: str) -> bool:
    return bool(payload.get(key))


def _f(payload: Mapping[str, Any], key: str) -> float | None:
    if key not in payload or payload.get(key) is None:
        return None
    try:
        return float(payload.get(key))
    except (TypeError, ValueError):
        return None


def compile_qi_routed_cycle_operational_summary(
    *,
    daemon_result: Mapping[str, Any] | None = None,
    route_result: Mapping[str, Any] | None = None,
    dispatch_result: Mapping[str, Any] | None = None,
    recovery_feedback: Mapping[str, Any] | None = None,
    shadow_evaluation: Mapping[str, Any] | None = None,
    shadow_admission: Mapping[str, Any] | None = None,
    health_projection: Mapping[str, Any] | None = None,
    recoverability_projection: Mapping[str, Any] | None = None,
    observation_debt: Mapping[str, Any] | None = None,
    trace_compaction: Mapping[str, Any] | None = None,
    source_paths: Mapping[str, str | None] | None = None,
) -> KuuOSQiRoutedCycleOperationalSummary:
    daemon = daemon_result or {}
    route = route_result or {}
    dispatch = dispatch_result or {}
    feedback = recovery_feedback or {}
    shadow = shadow_evaluation or {}
    admission = shadow_admission or {}
    health = health_projection or {}
    recoverability = recoverability_projection or {}
    debt = observation_debt or {}
    compaction = trace_compaction or {}

    blockers: list[str] = []
    warnings: list[str] = []
    positives: list[str] = []

    compact = _b(daemon, "scheduled_compact_before_next_tick") or _b(compaction, "compact_before_next_tick") or _b(compaction, "compaction_required")
    reobserve = _b(daemon, "scheduled_reobserve_before_next_tick") or _b(debt, "reobserve_before_next_tick") or _b(debt, "observation_required")
    hold = _b(daemon, "scheduled_hold_until_observation") or _s(feedback, "feedback_signal") == "QI_FEEDBACK_HOLD_REQUIRED"
    bounded_reentry = _s(feedback, "feedback_signal") == "QI_FEEDBACK_REENTRY_PERFORMED" or bool(dispatch.get("reentry_cycles_run", 0))

    if not daemon:
        blockers.append("daemon_result_missing")
    if not route:
        warnings.append("route_result_missing")
    if not dispatch:
        warnings.append("dispatch_result_missing")
    if reobserve:
        warnings.append("observation_debt_visible")
    if compact:
        warnings.append("trace_compaction_visible")
    if hold:
        blockers.append("hold_until_observation")
    if _s(admission, "shadow_admission_decision") == "QI_POLICY_FLOW_SHADOW_CANDIDATE_ADMITTED":
        positives.append("shadow_candidate_admitted")
    elif admission:
        warnings.append("shadow_candidate_not_admitted")
    if bounded_reentry:
        positives.append("bounded_reentry_candidate_visible")
    if _s(feedback, "feedback_signal"):
        positives.append(f"feedback:{_s(feedback, 'feedback_signal')}")

    if hold:
        mode = "HOLD_REOBSERVE"
        reason = "hold_until_observation_visible"
    elif reobserve:
        mode = "REOBSERVE"
        reason = "observation_debt_or_reobserve_hint_visible"
    elif compact:
        mode = "COMPACT_TRACE"
        reason = "trace_compaction_hint_visible"
    elif _s(admission, "shadow_admission_decision") == "QI_POLICY_FLOW_SHADOW_CANDIDATE_ADMITTED":
        mode = "SHADOW_READY_FOR_POLICY_FLOW_REVIEW"
        reason = "shadow_admission_passed_read_only"
    elif bounded_reentry:
        mode = "BOUNDED_REENTRY_REVIEW"
        reason = "bounded_reentry_candidate_visible"
    else:
        mode = "NO_CANDIDATE_OBSERVE"
        reason = "no_admitted_shadow_candidate_or_recovery_action"

    summary_decision = "QI_ROUTED_CYCLE_OPERATIONAL_SUMMARY_COMPILED"
    one_page = {
        "next_runtime_mode": mode,
        "reason": reason,
        "daemon": {
            "status": _s(daemon, "daemon_status"),
            "stop_reason": _s(daemon, "stop_reason") or _s(daemon, "daemon_stop_reason"),
            "ticks_run": daemon.get("ticks_run"),
        },
        "runtime": {
            "route_decision": _s(route, "route_decision"),
            "next_outer_action": _s(route, "next_outer_action"),
            "dispatcher_status": _s(dispatch, "dispatcher_status"),
        },
        "qi_process_tensor": {
            "recovery_feedback_signal": _s(feedback, "feedback_signal"),
            "health_projection_status": _s(health, "projection_status") or _s(health, "health_projection_status"),
            "recoverability_projection_status": _s(recoverability, "projection_status") or _s(recoverability, "recoverability_projection_status"),
            "observation_debt_status": _s(debt, "scheduler_status") or _s(debt, "observation_debt_status"),
            "trace_compaction_status": _s(compaction, "planner_status") or _s(compaction, "trace_compaction_status"),
        },
        "policy_shadow": {
            "admission_decision": _s(admission, "shadow_admission_decision"),
            "score": _f(shadow, "candidate_shadow_score"),
            "grade": _s(shadow, "candidate_shadow_grade"),
        },
        "runtime_flags": {
            "compact_before_next_tick": compact,
            "reobserve_before_next_tick": reobserve,
            "hold_until_observation": hold,
            "bounded_reentry_candidate": bounded_reentry,
        },
        "blockers": blockers,
        "warnings": warnings,
        "positive_signals": positives,
    }

    return KuuOSQiRoutedCycleOperationalSummary(
        summary_version="kuuos_runtime_daemon_qi_routed_cycle_operational_summary_v0_1",
        summary_status="QI_ROUTED_CYCLE_OPERATIONAL_SUMMARY_READY",
        summary_decision=summary_decision,
        recommended_next_runtime_mode=mode,
        recommended_next_reason=reason,
        daemon_status=_s(daemon, "daemon_status"),
        daemon_stop_reason=_s(daemon, "stop_reason") or _s(daemon, "daemon_stop_reason"),
        route_decision=_s(route, "route_decision"),
        next_outer_action=_s(route, "next_outer_action"),
        dispatcher_status=_s(dispatch, "dispatcher_status"),
        recovery_feedback_signal=_s(feedback, "feedback_signal"),
        policy_shadow_admission_decision=_s(admission, "shadow_admission_decision"),
        policy_shadow_score=_f(shadow, "candidate_shadow_score"),
        policy_shadow_grade=_s(shadow, "candidate_shadow_grade"),
        health_projection_status=_s(health, "projection_status") or _s(health, "health_projection_status"),
        recoverability_projection_status=_s(recoverability, "projection_status") or _s(recoverability, "recoverability_projection_status"),
        observation_debt_status=_s(debt, "scheduler_status") or _s(debt, "observation_debt_status"),
        trace_compaction_status=_s(compaction, "planner_status") or _s(compaction, "trace_compaction_status"),
        compact_before_next_tick=compact,
        reobserve_before_next_tick=reobserve,
        hold_until_observation=hold,
        bounded_reentry_candidate=bounded_reentry,
        operational_blockers=blockers,
        operational_warnings=warnings,
        operational_positive_signals=positives,
        source_paths=dict(source_paths or {}),
        one_page_summary=one_page,
        operational_summary_only=True,
        read_only=True,
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_routed_cycle_operational_summary(daemon_dir: Path, dispatch_dir: Path) -> KuuOSQiRoutedCycleOperationalSummary:
    daemon_dir = Path(daemon_dir)
    dispatch_dir = Path(dispatch_dir)
    paths = {
        "daemon_result": daemon_dir / "daemon_result_v0_1.json",
        "route_result": dispatch_dir / "qi_runtime_output_action_route_v0_1.json",
        "dispatch_result": dispatch_dir / "qi_runtime_output_action_dispatch_result_v0_1.json",
        "recovery_feedback": dispatch_dir / "qi_recovery_feedback_v0_1.json",
        "shadow_evaluation": dispatch_dir / "qi_policy_flow_candidate_shadow_evaluator_v0_1.json",
        "shadow_admission": dispatch_dir / "qi_policy_flow_candidate_shadow_admission_gate_v0_1.json",
        "health_projection": dispatch_dir / "qi_process_tensor_health_projection_v0_1.json",
        "recoverability_projection": dispatch_dir / "qi_process_tensor_recoverability_projection_v0_1.json",
        "observation_debt": dispatch_dir / "qi_process_tensor_observation_debt_scheduler_v0_1.json",
        "trace_compaction": dispatch_dir / "qi_process_tensor_trace_compaction_planner_v0_1.json",
    }
    return compile_qi_routed_cycle_operational_summary(
        daemon_result=_read_json(paths["daemon_result"]),
        route_result=_read_json(paths["route_result"]),
        dispatch_result=_read_json(paths["dispatch_result"]),
        recovery_feedback=_read_json(paths["recovery_feedback"]),
        shadow_evaluation=_read_json(paths["shadow_evaluation"]),
        shadow_admission=_read_json(paths["shadow_admission"]),
        health_projection=_read_json(paths["health_projection"]),
        recoverability_projection=_read_json(paths["recoverability_projection"]),
        observation_debt=_read_json(paths["observation_debt"]),
        trace_compaction=_read_json(paths["trace_compaction"]),
        source_paths={name: str(path) if path.is_file() else None for name, path in paths.items()},
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi routed cycle operational summary v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = read_and_compile_qi_routed_cycle_operational_summary(args.daemon_dir, args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_routed_cycle_operational_summary_v0_1.json", summary.to_dict())
    print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
