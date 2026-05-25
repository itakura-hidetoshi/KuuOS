#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import time
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_supervised_loop_control_v0_1 import read_and_compile_qi_supervised_loop_control
    from runtime.kuuos_runtime_daemon_qi_controlled_loop_runner_v0_1 import run_qi_controlled_loop
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_supervised_loop_control_v0_1 import read_and_compile_qi_supervised_loop_control
    from kuuos_runtime_daemon_qi_controlled_loop_runner_v0_1 import run_qi_controlled_loop


@dataclass(frozen=True)
class KuuOSQiPersistentSupervisorIteration:
    iteration_index: int
    iteration_dir: str
    heartbeat_path: str
    status_path: str
    control_status: str
    loop_allowed: bool
    control_reason: str
    controlled_loop_result_path: str | None
    cycles_run: int
    control_checks: int
    final_stop_reason: str
    successor_raw_state_path: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class KuuOSQiPersistentSupervisorResult:
    supervisor_version: str
    supervisor_status: str
    out_dir: str
    control_path: str
    iterations_run: int
    max_outer_iterations: int
    total_cycles_run: int
    total_control_checks: int
    final_stop_reason: str
    final_raw_state_path: str | None
    iteration_records: list[dict[str, Any]]
    supervisor_manifest_path: str
    persistent_supervisor_only: bool
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _last_successor_from_controlled_loop(result_path: Path) -> str | None:
    payload = _read_json(result_path)
    records = payload.get("cycle_records")
    if not isinstance(records, list):
        return None
    for record in reversed(records):
        if isinstance(record, dict) and record.get("loop_allowed"):
            value = record.get("successor_raw_state_path")
            return str(value) if value else None
    return None


def run_qi_persistent_supervisor(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    out_dir: Path,
    control_path: Path,
    max_outer_iterations: int = 3,
    max_daemon_ticks: int = 1,
    max_steps_per_tick: int = 1,
    requested_max_reentry_cycles: int = 1,
    sleep_seconds_between_iterations: float = 0.0,
) -> KuuOSQiPersistentSupervisorResult:
    if max_outer_iterations < 1:
        raise ValueError("max_outer_iterations must be >= 1")
    if sleep_seconds_between_iterations < 0:
        raise ValueError("sleep_seconds_between_iterations must be >= 0")

    out_dir = Path(out_dir)
    control_path = Path(control_path)
    current_raw = Path(raw_state_path)
    records: list[KuuOSQiPersistentSupervisorIteration] = []
    total_cycles_run = 0
    total_control_checks = 0
    final_stop_reason = "max_outer_iterations_reached"

    for iteration_index in range(max_outer_iterations):
        iteration_dir = out_dir / "iterations" / f"iteration_{iteration_index:03d}"
        heartbeat_path = iteration_dir / "heartbeat_v0_1.json"
        status_path = iteration_dir / "status_v0_1.json"
        control = read_and_compile_qi_supervised_loop_control(control_path)
        heartbeat = {
            "heartbeat_version": "qi_persistent_supervisor_heartbeat_v0_1",
            "iteration_index": iteration_index,
            "heartbeat_utc": _utc_now(),
            "control_status": control.control_status,
            "loop_allowed": control.loop_allowed,
            "control_reason": control.control_reason,
            "authority": "none",
        }
        _write_json(heartbeat_path, heartbeat)

        if not control.loop_allowed:
            status = {
                "status_version": "qi_persistent_supervisor_status_v0_1",
                "iteration_index": iteration_index,
                "status": "QI_PERSISTENT_SUPERVISOR_STOPPED_BY_CONTROL",
                "final_stop_reason": control.control_reason,
                "cycles_run": 0,
                "control_checks": 1,
                "authority": "none",
            }
            _write_json(status_path, status)
            records.append(KuuOSQiPersistentSupervisorIteration(
                iteration_index=iteration_index,
                iteration_dir=str(iteration_dir),
                heartbeat_path=str(heartbeat_path),
                status_path=str(status_path),
                control_status=control.control_status,
                loop_allowed=False,
                control_reason=control.control_reason,
                controlled_loop_result_path=None,
                cycles_run=0,
                control_checks=1,
                final_stop_reason=control.control_reason,
                successor_raw_state_path=None,
            ))
            total_control_checks += 1
            final_stop_reason = control.control_reason
            break

        loop_dir = iteration_dir / "controlled_loop"
        loop = run_qi_controlled_loop(
            raw_state_path=current_raw,
            evidence_path=Path(evidence_path),
            out_dir=loop_dir,
            control_path=control_path,
            max_daemon_ticks=max_daemon_ticks,
            max_steps_per_tick=max_steps_per_tick,
            requested_max_reentry_cycles=requested_max_reentry_cycles,
        )
        loop_result_path = iteration_dir / "qi_controlled_loop_result_v0_1.json"
        _write_json(loop_result_path, loop.to_dict())
        successor = _last_successor_from_controlled_loop(loop_result_path)
        status = {
            "status_version": "qi_persistent_supervisor_status_v0_1",
            "iteration_index": iteration_index,
            "status": "QI_PERSISTENT_SUPERVISOR_ITERATION_COMPLETED",
            "cycles_run": loop.cycles_run,
            "control_checks": loop.control_checks,
            "final_stop_reason": loop.final_stop_reason,
            "successor_raw_state_path": successor,
            "authority": "none",
        }
        _write_json(status_path, status)
        records.append(KuuOSQiPersistentSupervisorIteration(
            iteration_index=iteration_index,
            iteration_dir=str(iteration_dir),
            heartbeat_path=str(heartbeat_path),
            status_path=str(status_path),
            control_status=control.control_status,
            loop_allowed=True,
            control_reason=control.control_reason,
            controlled_loop_result_path=str(loop_result_path),
            cycles_run=loop.cycles_run,
            control_checks=loop.control_checks,
            final_stop_reason=loop.final_stop_reason,
            successor_raw_state_path=successor,
        ))
        total_cycles_run += loop.cycles_run
        total_control_checks += loop.control_checks
        if loop.final_stop_reason != "max_cycles_reached":
            final_stop_reason = loop.final_stop_reason
            break
        if successor and Path(successor).is_file() and Path(successor) != current_raw:
            current_raw = Path(successor)
        if sleep_seconds_between_iterations > 0 and iteration_index + 1 < max_outer_iterations:
            time.sleep(sleep_seconds_between_iterations)

    final_raw = str(current_raw) if current_raw else None
    manifest_path = out_dir / "qi_persistent_supervisor_manifest_v0_1.json"
    result = KuuOSQiPersistentSupervisorResult(
        supervisor_version="kuuos_runtime_daemon_qi_persistent_supervisor_v0_1",
        supervisor_status="QI_PERSISTENT_SUPERVISOR_COMPLETED",
        out_dir=str(out_dir),
        control_path=str(control_path),
        iterations_run=len(records),
        max_outer_iterations=max_outer_iterations,
        total_cycles_run=total_cycles_run,
        total_control_checks=total_control_checks,
        final_stop_reason=final_stop_reason,
        final_raw_state_path=final_raw,
        iteration_records=[record.to_dict() for record in records],
        supervisor_manifest_path=str(manifest_path),
        persistent_supervisor_only=True,
        bounded=True,
        read_only=True,
    )
    _write_json(manifest_path, result.to_dict())
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi persistent supervisor skeleton v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--control", type=Path, required=True)
    parser.add_argument("--max-outer-iterations", type=int, default=3)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds-between-iterations", type=float, default=0.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_persistent_supervisor(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        out_dir=args.out_dir,
        control_path=args.control,
        max_outer_iterations=args.max_outer_iterations,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
        sleep_seconds_between_iterations=args.sleep_seconds_between_iterations,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
