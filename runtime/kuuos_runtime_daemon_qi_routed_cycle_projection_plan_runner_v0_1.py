#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_routed_daemon_cycle_runner_v0_1 import run_qi_routed_daemon_cycle
    from runtime.kuuos_runtime_daemon_qi_projection_summary_plan_bridge_runner_v0_1 import run_qi_projection_summary_plan_bridge
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_routed_daemon_cycle_runner_v0_1 import run_qi_routed_daemon_cycle
    from kuuos_runtime_daemon_qi_projection_summary_plan_bridge_runner_v0_1 import run_qi_projection_summary_plan_bridge


@dataclass(frozen=True)
class KuuOSQiRoutedCycleProjectionPlanResult:
    runner_version: str
    runner_status: str
    daemon_dir: str
    dispatch_dir: str
    routed_cycle_result_path: str
    projection_plan_bridge_result_path: str
    qi_routed_cycle_operational_summary_path: str
    qi_next_runtime_mode_plan_path: str
    recommended_next_runtime_mode: str
    recommended_next_reason: str
    next_tick_preparation: str
    required_pre_tick_actions: list[str]
    projection_statuses: dict[str, str]
    bridge_only: bool
    read_only: bool
    plan_only: bool
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


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_qi_routed_cycle_projection_plan(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    daemon_dir: Path,
    dispatch_dir: Path,
    max_daemon_ticks: int = 1,
    max_steps_per_tick: int = 1,
    sleep_seconds: float = 0.0,
    state_bundle_path: Path | None = None,
    requested_max_reentry_cycles: int = 2,
) -> KuuOSQiRoutedCycleProjectionPlanResult:
    daemon_dir = Path(daemon_dir)
    dispatch_dir = Path(dispatch_dir)
    routed = run_qi_routed_daemon_cycle(
        raw_state_path=raw_state_path,
        evidence_path=evidence_path,
        daemon_dir=daemon_dir,
        dispatch_dir=dispatch_dir,
        max_daemon_ticks=max_daemon_ticks,
        max_steps_per_tick=max_steps_per_tick,
        sleep_seconds=sleep_seconds,
        state_bundle_path=state_bundle_path,
        requested_max_reentry_cycles=requested_max_reentry_cycles,
    )
    routed_path = dispatch_dir / "qi_routed_daemon_cycle_result_v0_1.json"
    _write_json(routed_path, routed.to_dict())

    bridge = run_qi_projection_summary_plan_bridge(daemon_dir=daemon_dir, dispatch_dir=dispatch_dir)
    bridge_path = dispatch_dir / "qi_projection_summary_plan_bridge_result_v0_1.json"
    _write_json(bridge_path, bridge.to_dict())

    return KuuOSQiRoutedCycleProjectionPlanResult(
        runner_version="kuuos_runtime_daemon_qi_routed_cycle_projection_plan_runner_v0_1",
        runner_status="QI_ROUTED_CYCLE_PROJECTION_PLAN_COMPILED",
        daemon_dir=str(daemon_dir),
        dispatch_dir=str(dispatch_dir),
        routed_cycle_result_path=str(routed_path),
        projection_plan_bridge_result_path=str(bridge_path),
        qi_routed_cycle_operational_summary_path=bridge.refreshed_operational_summary_path,
        qi_next_runtime_mode_plan_path=bridge.refreshed_next_runtime_plan_path,
        recommended_next_runtime_mode=bridge.recommended_next_runtime_mode,
        recommended_next_reason=bridge.recommended_next_reason,
        next_tick_preparation=bridge.next_tick_preparation,
        required_pre_tick_actions=bridge.required_pre_tick_actions,
        projection_statuses=bridge.projection_statuses,
        bridge_only=True,
        read_only=True,
        plan_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi routed cycle projection plan v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=2)
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_routed_cycle_projection_plan(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        daemon_dir=args.daemon_dir,
        dispatch_dir=args.dispatch_dir,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        sleep_seconds=args.sleep_seconds,
        state_bundle_path=args.state_bundle,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
    )
    if args.write_summary:
        _write_json(args.dispatch_dir / "qi_routed_cycle_projection_plan_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
