#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_controlled_loop_runner_v0_1 import run_qi_controlled_loop


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_overview(result) -> str:
    lines = [
        "Qi Controlled Loop — Operator Overview",
        f"loop_status: {result.loop_status}",
        f"cycles_run: {result.cycles_run}",
        f"control_checks: {result.control_checks}",
        f"max_cycles: {result.max_cycles}",
        f"final_stop_reason: {result.final_stop_reason}",
        f"final_recommended_next_runtime_mode: {result.final_recommended_next_runtime_mode or 'UNKNOWN'}",
        f"final_next_tick_preparation: {result.final_next_tick_preparation or 'UNKNOWN'}",
        "final_required_pre_tick_actions:",
    ]
    if result.final_required_pre_tick_actions:
        lines.extend([f"- {item}" for item in result.final_required_pre_tick_actions])
    else:
        lines.append("- none")
    lines.append("cycle_records:")
    for record in result.cycle_records:
        lines.append(
            f"- cycle {record['cycle_index']}: allowed={record['loop_allowed']} "
            f"control={record['control_status']} reason={record['control_reason']} "
            f"preparation={record['next_tick_preparation'] or 'none'} "
            f"stop={record['cycle_stop_reason'] or 'continue'}"
        )
    lines.extend([
        "authority: none",
        "scope: controlled-loop-read-only",
    ])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi controlled loop v0.1")
    parser.add_argument("--raw-state", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    parser.add_argument("--out-dir", type=pathlib.Path, required=True)
    parser.add_argument("--control", type=pathlib.Path, required=True)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=1)
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
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2

    result = run_qi_controlled_loop(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        out_dir=args.out_dir,
        control_path=args.control,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
    )
    result_path = args.out_dir / "qi_controlled_loop_result_v0_1.json"
    overview_path = args.out_dir / "qi_controlled_loop_overview_v0_1.txt"
    operator_manifest_path = args.out_dir / "qi_controlled_loop_operator_manifest_v0_1.json"
    overview = build_overview(result)

    write_json(result_path, result.to_dict())
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    overview_path.write_text(overview, encoding="utf-8")
    write_json(operator_manifest_path, {
        "manifest_version": "qi_controlled_loop_operator_manifest_v0_1",
        "control_path": str(args.control),
        "loop_manifest_path": result.loop_manifest_path,
        "result_path": str(result_path),
        "overview_path": str(overview_path),
        "cycles_run": result.cycles_run,
        "control_checks": result.control_checks,
        "max_cycles": result.max_cycles,
        "final_stop_reason": result.final_stop_reason,
        "final_next_tick_preparation": result.final_next_tick_preparation,
        "authority": "none",
        "scope": "controlled_loop_read_only",
    })

    if not args.quiet:
        print(overview, end="")
        print(f"operator_manifest: {operator_manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
