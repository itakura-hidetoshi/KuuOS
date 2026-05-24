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
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_projection_output_writer_v0_1 import write_qi_projection_outputs
    from kuuos_runtime_daemon_qi_routed_cycle_operational_summary_v0_1 import compile_qi_routed_cycle_operational_summary


@dataclass(frozen=True)
class KuuOSQiProjectionSummaryBridgeResult:
    bridge_version: str
    bridge_status: str
    daemon_dir: str
    dispatch_dir: str
    projection_writer_result_path: str
    refreshed_operational_summary_path: str
    recoverability_projection_path: str
    health_projection_path: str
    observation_debt_schedule_path: str
    trace_compaction_plan_path: str
    recoverability_status: str
    daemon_health_status: str
    observation_debt_status: str
    compaction_plan_status: str
    recommended_next_runtime_mode: str
    recommended_next_reason: str
    compact_before_next_tick: bool
    reobserve_before_next_tick: bool
    hold_until_observation: bool
    bridge_only: bool
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
    if not Path(path).is_file():
        return {}
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_qi_projection_summary_bridge(*, daemon_dir: Path, dispatch_dir: Path) -> KuuOSQiProjectionSummaryBridgeResult:
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

    return KuuOSQiProjectionSummaryBridgeResult(
        bridge_version="kuuos_runtime_daemon_qi_projection_summary_bridge_runner_v0_1",
        bridge_status="QI_PROJECTION_SUMMARY_BRIDGE_COMPILED",
        daemon_dir=str(daemon_dir),
        dispatch_dir=str(dispatch_dir),
        projection_writer_result_path=str(projection_result_path),
        refreshed_operational_summary_path=str(summary_path),
        recoverability_projection_path=projection.recoverability_projection_path,
        health_projection_path=projection.health_projection_path,
        observation_debt_schedule_path=projection.observation_debt_schedule_path,
        trace_compaction_plan_path=projection.trace_compaction_plan_path,
        recoverability_status=projection.recoverability_status,
        daemon_health_status=projection.daemon_health_status,
        observation_debt_status=projection.observation_debt_status,
        compaction_plan_status=projection.compaction_plan_status,
        recommended_next_runtime_mode=summary.recommended_next_runtime_mode,
        recommended_next_reason=summary.recommended_next_reason,
        compact_before_next_tick=summary.compact_before_next_tick,
        reobserve_before_next_tick=summary.reobserve_before_next_tick,
        hold_until_observation=summary.hold_until_observation,
        bridge_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi projection summary bridge v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_projection_summary_bridge(daemon_dir=args.daemon_dir, dispatch_dir=args.dispatch_dir)
    if args.write_summary:
        _write_json(args.dispatch_dir / "qi_projection_summary_bridge_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
