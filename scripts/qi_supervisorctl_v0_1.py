#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_qi_persistent_supervisor_profile_v0_1 import validate_profile
from scripts.run_qi_persistent_supervisor_profile_v0_1 import main as run_profile_main
from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_status_view_v0_1 import compile_qi_persistent_supervisor_status_view
from runtime.kuuos_runtime_daemon_qi_supervised_loop_control_v0_1 import compile_qi_supervised_loop_control


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(profile_dir: pathlib.Path, value: Any) -> pathlib.Path | None:
    if value is None:
        return None
    path = pathlib.Path(str(value))
    return path if path.is_absolute() else (profile_dir / path).resolve()


def control_path_from_profile(profile_path: pathlib.Path) -> pathlib.Path | None:
    profile = read_json(profile_path)
    return resolve_path(profile_path.parent, profile.get("control_path"))


def out_dir_from_profile(profile_path: pathlib.Path) -> pathlib.Path | None:
    profile = read_json(profile_path)
    return resolve_path(profile_path.parent, profile.get("out_dir"))


def write_control_packet(path: pathlib.Path, *, mode: str, max_cycles: int, sleep_seconds_between_cycles: float, reason: str | None) -> dict[str, Any]:
    if mode == "allow":
        enabled = True
        stop_requested = False
    elif mode == "stop":
        enabled = True
        stop_requested = True
    elif mode == "disable":
        enabled = False
        stop_requested = False
    else:
        raise ValueError(f"unsupported mode: {mode}")
    packet = {
        "control_packet_version": "qi_supervisor_control_packet_v0_1",
        "written_at_utc": utc_now(),
        "mode": mode,
        "enabled": enabled,
        "stop_requested": stop_requested,
        "max_cycles": max_cycles,
        "sleep_seconds_between_cycles": sleep_seconds_between_cycles,
        "operator_reason": reason,
        "authority": "none",
        "scope": "supervisor_control_packet_only",
    }
    control = compile_qi_supervised_loop_control(control_packet=packet)
    write_json(path, packet)
    compiled_path = path.with_name(path.stem + "_compiled_v0_1.json")
    write_json(compiled_path, control.to_dict())
    return {
        "operation": f"control_{mode}",
        "control_packet_path": str(path),
        "compiled_control_path": str(compiled_path),
        "mode": mode,
        "loop_allowed": control.loop_allowed,
        "control_status": control.control_status,
        "control_reason": control.control_reason,
        "authority": "none",
    }


def command_validate(args: argparse.Namespace) -> int:
    result = validate_profile(args.profile)
    if args.write:
        write_json(args.write, result.to_dict())
    if not args.quiet:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.validation_status == "QI_PERSISTENT_SUPERVISOR_PROFILE_VALID" else 1


def command_control(args: argparse.Namespace, mode: str) -> int:
    errors: list[str] = []
    if args.max_cycles < 1:
        errors.append("max_cycles_must_be_at_least_1")
    if args.sleep_seconds_between_cycles < 0:
        errors.append("sleep_seconds_between_cycles_must_be_nonnegative")
    control_path = args.control
    if control_path is None:
        if args.profile is None:
            errors.append("control_or_profile_required")
        else:
            control_path = control_path_from_profile(args.profile)
    if control_path is None:
        errors.append("control_path_missing")
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2
    result = write_control_packet(
        pathlib.Path(control_path),
        mode=mode,
        max_cycles=args.max_cycles,
        sleep_seconds_between_cycles=args.sleep_seconds_between_cycles,
        reason=args.reason,
    )
    if not args.quiet:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_run(args: argparse.Namespace) -> int:
    argv = ["--profile", str(args.profile)]
    if args.quiet:
        argv.append("--quiet")
    return int(run_profile_main(argv))


def command_status(args: argparse.Namespace) -> int:
    out_dir = args.out_dir
    if out_dir is None:
        if args.profile is None:
            print("ERROR: out_dir_or_profile_required", file=sys.stderr)
            return 2
        out_dir = out_dir_from_profile(args.profile)
    if out_dir is None:
        print("ERROR: out_dir_missing", file=sys.stderr)
        return 2
    view = compile_qi_persistent_supervisor_status_view(out_dir=pathlib.Path(out_dir))
    overview_lines = [
        "Qi Supervisorctl Status v0.1",
        f"status_view_status: {view.status_view_status}",
        f"supervisor_status: {view.supervisor_status or 'UNKNOWN'}",
        f"iterations_run: {view.iterations_run}",
        f"total_cycles_run: {view.total_cycles_run}",
        f"total_control_checks: {view.total_control_checks}",
        f"final_stop_reason: {view.final_stop_reason or 'UNKNOWN'}",
        f"latest_heartbeat_path: {view.latest_heartbeat_path or 'UNKNOWN'}",
        f"latest_status_path: {view.latest_status_path or 'UNKNOWN'}",
        f"process_tensor_advantage_score: {view.process_tensor_advantage_score if view.process_tensor_advantage_score is not None else 'UNKNOWN'}",
        f"process_tensor_advantage_level: {view.process_tensor_advantage_level or 'UNKNOWN'}",
        f"recommended_next_process_focus: {view.recommended_next_process_focus or 'UNKNOWN'}",
        "authority: none",
        "scope: supervisorctl-status-read-only",
    ]
    if args.write_json:
        write_json(args.write_json, view.to_dict())
    if args.write_text:
        args.write_text.parent.mkdir(parents=True, exist_ok=True)
        args.write_text.write_text("\n".join(overview_lines) + "\n", encoding="utf-8")
    if not args.quiet:
        print("\n".join(overview_lines))
    return 0 if view.status_view_status == "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KuuOS Qi supervisorctl v0.1")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate profile")
    validate.add_argument("--profile", type=pathlib.Path, required=True)
    validate.add_argument("--write", type=pathlib.Path, default=None)
    validate.add_argument("--quiet", action="store_true")
    validate.set_defaults(func=command_validate)

    run = sub.add_parser("run", help="run profile with preflight validation")
    run.add_argument("--profile", type=pathlib.Path, required=True)
    run.add_argument("--quiet", action="store_true")
    run.set_defaults(func=command_run)

    status = sub.add_parser("status", help="read supervisor status")
    status.add_argument("--profile", type=pathlib.Path, default=None)
    status.add_argument("--out-dir", type=pathlib.Path, default=None)
    status.add_argument("--write-json", type=pathlib.Path, default=None)
    status.add_argument("--write-text", type=pathlib.Path, default=None)
    status.add_argument("--quiet", action="store_true")
    status.set_defaults(func=command_status)

    for name, mode in [("allow", "allow"), ("stop", "stop"), ("disable", "disable")]:
        cmd = sub.add_parser(name, help=f"write {mode} control packet")
        cmd.add_argument("--profile", type=pathlib.Path, default=None)
        cmd.add_argument("--control", type=pathlib.Path, default=None)
        cmd.add_argument("--max-cycles", type=int, default=1)
        cmd.add_argument("--sleep-seconds-between-cycles", type=float, default=0.0)
        cmd.add_argument("--reason", type=str, default=None)
        cmd.add_argument("--quiet", action="store_true")
        cmd.set_defaults(func=lambda args, mode=mode: command_control(args, mode))

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
