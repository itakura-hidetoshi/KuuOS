#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_v0_1 import run_qi_persistent_supervisor


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(profile_dir: pathlib.Path, value: Any) -> pathlib.Path | None:
    if value is None:
        return None
    path = pathlib.Path(str(value))
    if path.is_absolute():
        return path
    return (profile_dir / path).resolve()


def build_overview(result, profile_path: pathlib.Path) -> str:
    lines = [
        "Qi Persistent Supervisor Profile — Operator Overview",
        f"profile_path: {profile_path}",
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
        "scope: persistent-supervisor-profile-bounded-read-only",
    ])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi persistent supervisor from profile v0.1")
    parser.add_argument("--profile", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    profile_path = args.profile
    errors: list[str] = []
    if not profile_path.is_file():
        print(f"ERROR: profile_not_found:{profile_path}", file=sys.stderr)
        return 2

    profile = read_json(profile_path)
    profile_dir = profile_path.parent
    raw_state = resolve_path(profile_dir, profile.get("raw_state_path"))
    evidence = resolve_path(profile_dir, profile.get("evidence_path"))
    control = resolve_path(profile_dir, profile.get("control_path"))
    out_dir = resolve_path(profile_dir, profile.get("out_dir"))

    for label, path in [
        ("raw_state_path", raw_state),
        ("evidence_path", evidence),
        ("control_path", control),
    ]:
        if path is None:
            errors.append(f"missing_profile_field:{label}")
        elif not path.is_file():
            errors.append(f"path_not_found:{label}:{path}")
    if out_dir is None:
        errors.append("missing_profile_field:out_dir")

    max_outer_iterations = int(profile.get("max_outer_iterations", 1))
    max_daemon_ticks = int(profile.get("max_daemon_ticks", 1))
    max_steps_per_tick = int(profile.get("max_steps_per_tick", 1))
    requested_max_reentry_cycles = int(profile.get("requested_max_reentry_cycles", 1))
    sleep_seconds_between_iterations = float(profile.get("sleep_seconds_between_iterations", 0.0))

    if max_outer_iterations < 1:
        errors.append("max_outer_iterations_must_be_at_least_1")
    if max_daemon_ticks < 1:
        errors.append("max_daemon_ticks_must_be_at_least_1")
    if max_steps_per_tick < 1:
        errors.append("max_steps_per_tick_must_be_at_least_1")
    if requested_max_reentry_cycles < 0:
        errors.append("requested_max_reentry_cycles_must_be_nonnegative")
    if sleep_seconds_between_iterations < 0:
        errors.append("sleep_seconds_between_iterations_must_be_nonnegative")

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2

    result = run_qi_persistent_supervisor(
        raw_state_path=raw_state,
        evidence_path=evidence,
        out_dir=out_dir,
        control_path=control,
        max_outer_iterations=max_outer_iterations,
        max_daemon_ticks=max_daemon_ticks,
        max_steps_per_tick=max_steps_per_tick,
        requested_max_reentry_cycles=requested_max_reentry_cycles,
        sleep_seconds_between_iterations=sleep_seconds_between_iterations,
    )
    result_path = out_dir / "qi_persistent_supervisor_profile_result_v0_1.json"
    overview_path = out_dir / "qi_persistent_supervisor_profile_overview_v0_1.txt"
    operator_manifest_path = out_dir / "qi_persistent_supervisor_profile_operator_manifest_v0_1.json"
    overview = build_overview(result, profile_path)
    write_json(result_path, result.to_dict())
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    overview_path.write_text(overview, encoding="utf-8")
    write_json(operator_manifest_path, {
        "manifest_version": "qi_persistent_supervisor_profile_operator_manifest_v0_1",
        "profile_path": str(profile_path),
        "control_path": str(control),
        "supervisor_manifest_path": result.supervisor_manifest_path,
        "result_path": str(result_path),
        "overview_path": str(overview_path),
        "iterations_run": result.iterations_run,
        "max_outer_iterations": result.max_outer_iterations,
        "total_cycles_run": result.total_cycles_run,
        "total_control_checks": result.total_control_checks,
        "final_stop_reason": result.final_stop_reason,
        "authority": "none",
        "scope": "persistent_supervisor_profile_bounded_read_only",
    })
    if not args.quiet:
        print(overview, end="")
        print(f"operator_manifest: {operator_manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
