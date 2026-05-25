#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_supervised_loop_runner_v0_1 import run_qi_supervised_loop
from runtime.kuuos_runtime_daemon_qi_supervised_loop_control_v0_1 import read_and_compile_qi_supervised_loop_control


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_overview(result, control=None) -> str:
    lines = [
        "Qi Supervised Loop — Operator Overview",
    ]
    if control is not None:
        lines.extend([
            f"control_status: {control.control_status}",
            f"loop_allowed: {control.loop_allowed}",
            f"control_reason: {control.control_reason}",
            f"heartbeat_utc: {control.heartbeat_utc}",
        ])
    lines.extend([
        f"loop_status: {result.loop_status}",
        f"cycles_run: {result.cycles_run}",
        f"max_cycles: {result.max_cycles}",
        f"final_stop_reason: {result.final_stop_reason}",
        f"final_recommended_next_runtime_mode: {result.final_recommended_next_runtime_mode or 'UNKNOWN'}",
        f"final_next_tick_preparation: {result.final_next_tick_preparation or 'UNKNOWN'}",
        "final_required_pre_tick_actions:",
    ])
    if result.final_required_pre_tick_actions:
        lines.extend([f"- {item}" for item in result.final_required_pre_tick_actions])
    else:
        lines.append("- none")
    lines.extend([
        "cycle_records:",
    ])
    for record in result.cycle_records:
        lines.append(
            f"- cycle {record['cycle_index']}: mode={record['recommended_next_runtime_mode']} "
            f"preparation={record['next_tick_preparation']} stop={record['cycle_stop_reason'] or 'continue'}"
        )
    lines.extend([
        "authority: none",
        "scope: supervised-bounded-loop-only",
    ])
    return "\n".join(lines) + "\n"


def blocked_result(*, out_dir: pathlib.Path, control) -> dict:
    return {
        "loop_version": "kuuos_runtime_daemon_qi_supervised_loop_runner_v0_1",
        "loop_status": "QI_SUPERVISED_LOOP_BLOCKED_BY_CONTROL",
        "out_dir": str(out_dir),
        "cycles_run": 0,
        "max_cycles": control.max_cycles,
        "final_stop_reason": control.control_reason,
        "final_recommended_next_runtime_mode": None,
        "final_next_tick_preparation": None,
        "final_required_pre_tick_actions": [],
        "cycle_records": [],
        "loop_manifest_path": str(out_dir / "qi_supervised_loop_manifest_v0_1.json"),
        "supervised_loop_only": True,
        "bounded": True,
        "read_only": True,
        "grants_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_truth_authority": False,
        "grants_final_commitment_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_clinical_authority": False,
        "grants_theorem_authority": False,
        "grants_completed_identity_authority": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi supervised bounded loop v0.1")
    parser.add_argument("--raw-state", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    parser.add_argument("--out-dir", type=pathlib.Path, required=True)
    parser.add_argument("--control", type=pathlib.Path, default=None)
    parser.add_argument("--max-cycles", type=int, default=3)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds-between-cycles", type=float, default=0.0)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors: list[str] = []
    if not args.raw_state.is_file():
        errors.append(f"raw_state_not_found:{args.raw_state}")
    if not args.evidence.is_file():
        errors.append(f"evidence_not_found:{args.evidence}")
    if args.max_cycles < 1:
        errors.append("max_cycles_must_be_at_least_1")
    if args.control is not None and not args.control.is_file():
        errors.append(f"control_not_found:{args.control}")
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2

    control = None
    if args.control is not None:
        control = read_and_compile_qi_supervised_loop_control(args.control)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        write_json(args.out_dir / "qi_supervised_loop_control_v0_1.json", control.to_dict())
        if not control.loop_allowed:
            payload = blocked_result(out_dir=args.out_dir, control=control)
            result_path = args.out_dir / "qi_supervised_loop_result_v0_1.json"
            overview_path = args.out_dir / "qi_supervised_loop_overview_v0_1.txt"
            operator_manifest_path = args.out_dir / "qi_supervised_loop_operator_manifest_v0_1.json"
            write_json(result_path, payload)
            write_json(pathlib.Path(payload["loop_manifest_path"]), payload)
            overview = "\n".join([
                "Qi Supervised Loop — Operator Overview",
                f"control_status: {control.control_status}",
                f"loop_allowed: {control.loop_allowed}",
                f"control_reason: {control.control_reason}",
                "loop_status: QI_SUPERVISED_LOOP_BLOCKED_BY_CONTROL",
                "cycles_run: 0",
                "authority: none",
                "scope: supervised-bounded-loop-only",
            ]) + "\n"
            overview_path.write_text(overview, encoding="utf-8")
            write_json(operator_manifest_path, {
                "manifest_version": "qi_supervised_loop_operator_manifest_v0_1",
                "control_path": str(args.control),
                "control_result_path": str(args.out_dir / "qi_supervised_loop_control_v0_1.json"),
                "loop_manifest_path": payload["loop_manifest_path"],
                "result_path": str(result_path),
                "overview_path": str(overview_path),
                "cycles_run": 0,
                "max_cycles": control.max_cycles,
                "final_stop_reason": control.control_reason,
                "final_next_tick_preparation": None,
                "authority": "none",
                "scope": "supervised_bounded_loop_only",
            })
            if not args.quiet:
                print(overview, end="")
                print(f"operator_manifest: {operator_manifest_path}")
            return 0
        args.max_cycles = control.max_cycles
        args.sleep_seconds_between_cycles = control.sleep_seconds_between_cycles

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
    result_path = args.out_dir / "qi_supervised_loop_result_v0_1.json"
    overview_path = args.out_dir / "qi_supervised_loop_overview_v0_1.txt"
    operator_manifest_path = args.out_dir / "qi_supervised_loop_operator_manifest_v0_1.json"
    overview = build_overview(result, control=control)

    write_json(result_path, result.to_dict())
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    overview_path.write_text(overview, encoding="utf-8")
    write_json(operator_manifest_path, {
        "manifest_version": "qi_supervised_loop_operator_manifest_v0_1",
        "control_path": str(args.control) if args.control else None,
        "control_result_path": str(args.out_dir / "qi_supervised_loop_control_v0_1.json") if control else None,
        "loop_manifest_path": result.loop_manifest_path,
        "result_path": str(result_path),
        "overview_path": str(overview_path),
        "cycles_run": result.cycles_run,
        "max_cycles": result.max_cycles,
        "final_stop_reason": result.final_stop_reason,
        "final_next_tick_preparation": result.final_next_tick_preparation,
        "authority": "none",
        "scope": "supervised_bounded_loop_only",
    })

    if not args.quiet:
        print(overview, end="")
        print(f"operator_manifest: {operator_manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
