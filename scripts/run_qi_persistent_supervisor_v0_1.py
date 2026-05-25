#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_v0_1 import run_qi_persistent_supervisor


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_overview(result) -> str:
    lines = [
        "Qi Persistent Supervisor — Operator Overview",
        f"supervisor_status: {result.supervisor_status}",
        f"iterations_run: {result.iterations_run}",
        f"max_outer_iterations: {result.max_outer_iterations}",
        f"total_cycles_run: {result.total_cycles_run}",
        f"total_control_checks: {result.total_control_checks}",
        f"final_stop_reason: {result.final_stop_reason}",
        f"final_raw_state_path: {result.final_raw_state_path or 'UNKNOWN'}",
        "iteration_records:",
    ]
    for record in result.iteration_records:
        lines.append(
            f"- iteration {record['iteration_index']}: allowed={record['loop_allowed']} "
            f"control={record['control_status']} reason={record['control_reason']} "
            f"cycles={record['cycles_run']} stop={record['final_stop_reason']}"
        )
    lines.extend([
        "authority: none",
        "scope: persistent-supervisor-bounded-read-only",
    ])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi persistent supervisor skeleton v0.1")
    parser.add_argument("--raw-state", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    parser.add_argument("--out-dir", type=pathlib.Path, required=True)
    parser.add_argument("--control", type=pathlib.Path, required=True)
    parser.add_argument("--max-outer-iterations", type=int, default=3)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds-between-iterations", type=float, default=0.0)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors: list[str] = []
    if not args.raw_state.is_file():
        errors.append(f"raw_state_not_found:{args.raw_state}")
    if not args.evidence.is_file():
        errors.append(f"evidence_not_found:{args.evidence}")
    if not args.control.is_file():
        errors.append(f"control_not_found:{args.control}")
    if args.max_outer_iterations < 1:
        errors.append("max_outer_iterations_must_be_at_least_1")
    if args.sleep_seconds_between_iterations < 0:
        errors.append("sleep_seconds_between_iterations_must_be_nonnegative")
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2

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
    result_path = args.out_dir / "qi_persistent_supervisor_result_v0_1.json"
    overview_path = args.out_dir / "qi_persistent_supervisor_overview_v0_1.txt"
    operator_manifest_path = args.out_dir / "qi_persistent_supervisor_operator_manifest_v0_1.json"
    overview = build_overview(result)

    write_json(result_path, result.to_dict())
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    overview_path.write_text(overview, encoding="utf-8")
    write_json(operator_manifest_path, {
        "manifest_version": "qi_persistent_supervisor_operator_manifest_v0_1",
        "control_path": str(args.control),
        "supervisor_manifest_path": result.supervisor_manifest_path,
        "result_path": str(result_path),
        "overview_path": str(overview_path),
        "iterations_run": result.iterations_run,
        "max_outer_iterations": result.max_outer_iterations,
        "total_cycles_run": result.total_cycles_run,
        "total_control_checks": result.total_control_checks,
        "final_stop_reason": result.final_stop_reason,
        "authority": "none",
        "scope": "persistent_supervisor_bounded_read_only",
    })

    if not args.quiet:
        print(overview, end="")
        print(f"operator_manifest: {operator_manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
