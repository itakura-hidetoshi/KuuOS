#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
import time
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_routed_cycle_projection_plan_runner_v0_1 import run_qi_routed_cycle_projection_plan
    from runtime.kuuos_runtime_daemon_qi_projection_plan_readable_summary_v0_1 import compile_qi_projection_plan_readable_summary
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_routed_cycle_projection_plan_runner_v0_1 import run_qi_routed_cycle_projection_plan
    from kuuos_runtime_daemon_qi_projection_plan_readable_summary_v0_1 import compile_qi_projection_plan_readable_summary


@dataclass(frozen=True)
class KuuOSQiSupervisedLoopCycleRecord:
    cycle_index: int
    cycle_dir: str
    input_raw_state_path: str
    routed_projection_plan_result_path: str
    readable_summary_path: str
    recommended_next_runtime_mode: str
    next_tick_preparation: str
    required_pre_tick_actions: list[str]
    projection_statuses: dict[str, str]
    successor_raw_state_path: str | None
    cycle_stop_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class KuuOSQiSupervisedLoopResult:
    loop_version: str
    loop_status: str
    out_dir: str
    cycles_run: int
    max_cycles: int
    final_stop_reason: str
    final_recommended_next_runtime_mode: str | None
    final_next_tick_preparation: str | None
    final_required_pre_tick_actions: list[str]
    cycle_records: list[dict[str, Any]]
    loop_manifest_path: str
    supervised_loop_only: bool
    bounded: bool
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


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _successor_from_routed_result(path: Path) -> str | None:
    payload = _read_json(path)
    value = payload.get("final_raw_state_path")
    return str(value) if value else None


def _cycle_stop_reason(*, next_tick_preparation: str, successor_raw_state_path: str | None, current_raw_state_path: Path) -> str | None:
    if next_tick_preparation == "hold_reobserve":
        return "hold_reobserve_requested"
    if successor_raw_state_path is None:
        return "successor_raw_state_missing"
    if not Path(successor_raw_state_path).is_file():
        return "successor_raw_state_not_found"
    if Path(successor_raw_state_path) == Path(current_raw_state_path):
        return "successor_raw_state_unchanged"
    return None


def run_qi_supervised_loop(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    out_dir: Path,
    max_cycles: int = 3,
    max_daemon_ticks: int = 1,
    max_steps_per_tick: int = 1,
    requested_max_reentry_cycles: int = 1,
    sleep_seconds_between_cycles: float = 0.0,
) -> KuuOSQiSupervisedLoopResult:
    if max_cycles < 1:
        raise ValueError("max_cycles must be >= 1")
    out_dir = Path(out_dir)
    current_raw = Path(raw_state_path)
    records: list[KuuOSQiSupervisedLoopCycleRecord] = []
    final_stop_reason = "max_cycles_reached"

    for cycle_index in range(max_cycles):
        cycle_dir = out_dir / "cycles" / f"cycle_{cycle_index:03d}"
        daemon_dir = cycle_dir / "daemon"
        dispatch_dir = cycle_dir / "dispatch"
        result = run_qi_routed_cycle_projection_plan(
            raw_state_path=current_raw,
            evidence_path=Path(evidence_path),
            daemon_dir=daemon_dir,
            dispatch_dir=dispatch_dir,
            max_daemon_ticks=max_daemon_ticks,
            max_steps_per_tick=max_steps_per_tick,
            requested_max_reentry_cycles=requested_max_reentry_cycles,
        )
        result_path = cycle_dir / "qi_routed_cycle_projection_plan_result_v0_1.json"
        _write_json(result_path, result.to_dict())

        readable = compile_qi_projection_plan_readable_summary(projection_plan_result=result.to_dict())
        readable_path = cycle_dir / "qi_projection_plan_readable_summary_v0_1.txt"
        readable_path.write_text(readable.to_text(), encoding="utf-8")

        successor = _successor_from_routed_result(Path(result.routed_cycle_result_path))
        stop_reason = _cycle_stop_reason(
            next_tick_preparation=result.next_tick_preparation,
            successor_raw_state_path=successor,
            current_raw_state_path=current_raw,
        )
        record = KuuOSQiSupervisedLoopCycleRecord(
            cycle_index=cycle_index,
            cycle_dir=str(cycle_dir),
            input_raw_state_path=str(current_raw),
            routed_projection_plan_result_path=str(result_path),
            readable_summary_path=str(readable_path),
            recommended_next_runtime_mode=result.recommended_next_runtime_mode,
            next_tick_preparation=result.next_tick_preparation,
            required_pre_tick_actions=result.required_pre_tick_actions,
            projection_statuses=result.projection_statuses,
            successor_raw_state_path=successor,
            cycle_stop_reason=stop_reason,
        )
        records.append(record)
        if stop_reason:
            final_stop_reason = stop_reason
            break
        current_raw = Path(successor) if successor else current_raw
        if sleep_seconds_between_cycles > 0 and cycle_index + 1 < max_cycles:
            time.sleep(sleep_seconds_between_cycles)

    last = records[-1] if records else None
    manifest_path = out_dir / "qi_supervised_loop_manifest_v0_1.json"
    result = KuuOSQiSupervisedLoopResult(
        loop_version="kuuos_runtime_daemon_qi_supervised_loop_runner_v0_1",
        loop_status="QI_SUPERVISED_LOOP_COMPLETED",
        out_dir=str(out_dir),
        cycles_run=len(records),
        max_cycles=max_cycles,
        final_stop_reason=final_stop_reason,
        final_recommended_next_runtime_mode=last.recommended_next_runtime_mode if last else None,
        final_next_tick_preparation=last.next_tick_preparation if last else None,
        final_required_pre_tick_actions=last.required_pre_tick_actions if last else [],
        cycle_records=[record.to_dict() for record in records],
        loop_manifest_path=str(manifest_path),
        supervised_loop_only=True,
        bounded=True,
        read_only=True,
    )
    _write_json(manifest_path, result.to_dict())
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi supervised bounded loop v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--max-cycles", type=int, default=3)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds-between-cycles", type=float, default=0.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_supervised_loop(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        out_dir=args.out_dir,
        max_cycles=args.max_cycles,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
        sleep_seconds_between_cycles=args.sleep_seconds_between_cycles,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
