#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_routed_cycle_projection_plan_runner_v0_1 import run_qi_routed_cycle_projection_plan
from runtime.kuuos_runtime_daemon_qi_projection_plan_readable_summary_v0_1 import compile_qi_projection_plan_readable_summary


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi daemon once and write operator-readable outputs v0.1")
    parser.add_argument("--raw-state", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    parser.add_argument("--out-dir", type=pathlib.Path, required=True)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--state-bundle", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors: list[str] = []
    if not args.raw_state.is_file():
        errors.append(f"raw_state_not_found:{args.raw_state}")
    if not args.evidence.is_file():
        errors.append(f"evidence_not_found:{args.evidence}")
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2

    out_dir = args.out_dir
    daemon_dir = out_dir / "daemon"
    dispatch_dir = out_dir / "dispatch"
    result = run_qi_routed_cycle_projection_plan(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        daemon_dir=daemon_dir,
        dispatch_dir=dispatch_dir,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        sleep_seconds=args.sleep_seconds,
        state_bundle_path=args.state_bundle,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
    )
    result_path = out_dir / "qi_daemon_once_result_v0_1.json"
    write_json(result_path, result.to_dict())

    readable = compile_qi_projection_plan_readable_summary(projection_plan_result=result.to_dict())
    readable_json_path = out_dir / "qi_daemon_once_readable_summary_v0_1.json"
    readable_text_path = out_dir / "qi_daemon_once_readable_summary_v0_1.txt"
    write_json(readable_json_path, readable.to_dict())
    write_text(readable_text_path, readable.to_text())

    manifest = {
        "manifest_version": "qi_daemon_once_operator_outputs_v0_1",
        "result_path": str(result_path),
        "readable_json_path": str(readable_json_path),
        "readable_text_path": str(readable_text_path),
        "daemon_dir": str(daemon_dir),
        "dispatch_dir": str(dispatch_dir),
        "recommended_next_runtime_mode": result.recommended_next_runtime_mode,
        "next_tick_preparation": result.next_tick_preparation,
        "required_pre_tick_actions": result.required_pre_tick_actions,
        "projection_statuses": result.projection_statuses,
        "authority": "none",
        "scope": "operator_cli_once_read_only",
    }
    manifest_path = out_dir / "qi_daemon_once_manifest_v0_1.json"
    write_json(manifest_path, manifest)

    if not args.quiet:
        print(readable.to_text(), end="")
        print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
