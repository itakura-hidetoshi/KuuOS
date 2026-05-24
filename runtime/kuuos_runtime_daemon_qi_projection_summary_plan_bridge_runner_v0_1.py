#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_projection_output_writer_v0_1 import write_qi_projection_outputs
    from runtime.kuuos_runtime_daemon_qi_routed_cycle_operational_summary_v0_1 import compile_qi_routed_cycle_operational_summary
    from runtime.kuuos_runtime_daemon_qi_next_runtime_mode_plan_v0_1 import compile_qi_next_runtime_mode_plan
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_projection_output_writer_v0_1 import write_qi_projection_outputs
    from kuuos_runtime_daemon_qi_routed_cycle_operational_summary_v0_1 import compile_qi_routed_cycle_operational_summary
    from kuuos_runtime_daemon_qi_next_runtime_mode_plan_v0_1 import compile_qi_next_runtime_mode_plan


@dataclass(frozen=True)
class KuuOSQiProjectionSummaryPlanBridgeResult:
    bridge_version: str
    bridge_status: str
    daemon_dir: str
    dispatch_dir: str
    projection_writer_result_path: str
    refreshed_operational_summary_path: str
    refreshed_next_runtime_plan_path: str
    recoverability_projection_path: str
    health_projection_path: str
    observation_debt_schedule_path: str
    trace_compaction_plan_path: str
    recommended_next_runtime_mode: str
    recommended_next_reason: str
    next_tick_preparation: str
    required_pre_tick_actions: list[str]
    projection_statuses: dict[str, str]
    bridge_only: bool
    read_only: bool
    plan_only: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    path = Path(path)
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_qi_projection_summary_plan_bridge(*, daemon_dir: Path, dispatch_dir: Path) -> KuuOSQiProjectionSummaryPlanBridgeResult:
    daemon_dir = Path(daemon_dir)
    dispatch_dir = Path(dispatch_dir)
    projection = write_qi_projection_outputs(daemon_dir)
    projection_result_path = daemon_dir / "daemon_qi_projection_output_writer_result_v0_1.json"
    _write_json(projection_result_path, projection.to_dict())

    daemon_result_path = daemon_dir / "daemon_result_v0_1.json"
    summary = compile_qi_routed_cycle_operational_summary(
        daemon_result=_read_json(daemon_result_path),
        route_result=_read_json(dispatch_dir / "qi_runtime_output_action_route_v0_1.json"),
        dispatch_result=_read_json(dispatch_dir / "qi_runtime_output_action_dispatch_result_v0_1.json"),
        recovery_feedback=_read_json(dispatch_dir / "qi_recovery_feedback_v0_1.json"),
        shadow_evaluation=_read_json(dispatch_dir / "qi_policy_flow_candidate_shadow_evaluator_v0_1.json"),
        shadow_admission=_read_json(dispatch_dir / "qi_policy_flow_candidate_shadow_admission_gate_v0_1.json"),
        health_projection=_read_json(Path(projection.health_projection_path)),
        recoverability_projection=_read_json(Path(projection.recoverability_projection_path)),
        observation_debt=_read_json(Path(projection.observation_debt_schedule_path)),
        trace_compaction=_read_json(Path(projection.trace_compaction_plan_path)),
        source_paths={
            "daemon_result": str(daemon_result_path) if daemon_result_path.is_file() else None,
            "recoverability_projection": projection.recoverability_projection_path,
            "health_projection": projection.health_projection_path,
            "observation_debt": projection.observation_debt_schedule_path,
            "trace_compaction": projection.trace_compaction_plan_path,
        },
    )
    summary_path = dispatch_dir / "qi_routed_cycle_operational_summary_v0_1.json"
    _write_json(summary_path, summary.to_dict())

    plan = compile_qi_next_runtime_mode_plan(
        operational_summary=summary.to_dict(),
        source_operational_summary_path=summary_path,
    )
    plan_path = dispatch_dir / "qi_next_runtime_mode_plan_v0_1.json"
    _write_json(plan_path, plan.to_dict())

    return KuuOSQiProjectionSummaryPlanBridgeResult(
        bridge_version="kuuos_runtime_daemon_qi_projection_summary_plan_bridge_runner_v0_1",
        bridge_status="QI_PROJECTION_SUMMARY_PLAN_BRIDGE_COMPILED",
        daemon_dir=str(daemon_dir),
        dispatch_dir=str(dispatch_dir),
        projection_writer_result_path=str(projection_result_path),
        refreshed_operational_summary_path=str(summary_path),
        refreshed_next_runtime_plan_path=str(plan_path),
        recoverability_projection_path=projection.recoverability_projection_path,
        health_projection_path=projection.health_projection_path,
        observation_debt_schedule_path=projection.observation_debt_schedule_path,
        trace_compaction_plan_path=projection.trace_compaction_plan_path,
        recommended_next_runtime_mode=summary.recommended_next_runtime_mode,
        recommended_next_reason=summary.recommended_next_reason,
        next_tick_preparation=plan.next_tick_preparation,
        required_pre_tick_actions=plan.required_pre_tick_actions,
        projection_statuses={
            "recoverability": projection.recoverability_status,
            "health": projection.daemon_health_status,
            "observation_debt": projection.observation_debt_status,
            "trace_compaction": projection.compaction_plan_status,
        },
        bridge_only=True,
        read_only=True,
        plan_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi projection summary plan bridge v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_projection_summary_plan_bridge(daemon_dir=args.daemon_dir, dispatch_dir=args.dispatch_dir)
    if args.write_summary:
        _write_json(args.dispatch_dir / "qi_projection_summary_plan_bridge_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
