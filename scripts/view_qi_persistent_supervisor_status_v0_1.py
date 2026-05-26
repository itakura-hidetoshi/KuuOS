#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_status_view_v0_1 import compile_qi_persistent_supervisor_status_view


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_overview(view) -> str:
    lines = [
        "Qi Persistent Supervisor Status — Operator View",
        f"status_view_status: {view.status_view_status}",
        f"supervisor_status: {view.supervisor_status or 'UNKNOWN'}",
        f"iterations_run: {view.iterations_run}",
        f"total_cycles_run: {view.total_cycles_run}",
        f"total_control_checks: {view.total_control_checks}",
        f"final_stop_reason: {view.final_stop_reason or 'UNKNOWN'}",
        f"latest_iteration_index: {view.latest_iteration_index if view.latest_iteration_index is not None else 'UNKNOWN'}",
        f"latest_heartbeat_path: {view.latest_heartbeat_path or 'UNKNOWN'}",
        f"latest_status_path: {view.latest_status_path or 'UNKNOWN'}",
        f"process_tensor_advantage_score: {view.process_tensor_advantage_score if view.process_tensor_advantage_score is not None else 'UNKNOWN'}",
        f"process_tensor_advantage_level: {view.process_tensor_advantage_level or 'UNKNOWN'}",
        f"recommended_next_process_focus: {view.recommended_next_process_focus or 'UNKNOWN'}",
        f"recommended_probe_type: {view.recommended_probe_type or 'UNKNOWN'}",
        f"probe_target_time_slice: {view.probe_target_time_slice or 'UNKNOWN'}",
        f"probe_risk_level: {view.probe_risk_level or 'UNKNOWN'}",
        "view_blockers:",
    ]
    if view.view_blockers:
        lines.extend([f"- {item}" for item in view.view_blockers])
    else:
        lines.append("- none")
    lines.append("view_warnings:")
    if view.view_warnings:
        lines.extend([f"- {item}" for item in view.view_warnings])
    else:
        lines.append("- none")
    lines.extend([
        "authority: none",
        "scope: persistent-supervisor-status-read-only",
    ])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="View KuuOS Qi persistent supervisor status v0.1")
    parser.add_argument("--out-dir", type=pathlib.Path, required=True)
    parser.add_argument("--write-json", type=pathlib.Path, default=None)
    parser.add_argument("--write-text", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    view = compile_qi_persistent_supervisor_status_view(out_dir=args.out_dir)
    overview = build_overview(view)
    if args.write_json:
        write_json(args.write_json, view.to_dict())
    if args.write_text:
        args.write_text.parent.mkdir(parents=True, exist_ok=True)
        args.write_text.write_text(overview, encoding="utf-8")
    if not args.quiet:
        print(overview, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
