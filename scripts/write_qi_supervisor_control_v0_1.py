#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_supervised_loop_control_v0_1 import compile_qi_supervised_loop_control


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write KuuOS Qi supervisor control packet v0.1")
    parser.add_argument("--write", type=pathlib.Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--allow", action="store_true")
    mode.add_argument("--stop", action="store_true")
    mode.add_argument("--disable", action="store_true")
    parser.add_argument("--max-cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds-between-cycles", type=float, default=0.0)
    parser.add_argument("--reason", type=str, default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors: list[str] = []
    if args.max_cycles < 1:
        errors.append("max_cycles_must_be_at_least_1")
    if args.sleep_seconds_between_cycles < 0:
        errors.append("sleep_seconds_between_cycles_must_be_nonnegative")
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2

    if args.allow:
        enabled = True
        stop_requested = False
        mode_name = "allow"
    elif args.stop:
        enabled = True
        stop_requested = True
        mode_name = "stop"
    else:
        enabled = False
        stop_requested = False
        mode_name = "disable"

    packet = {
        "control_packet_version": "qi_supervisor_control_packet_v0_1",
        "written_at_utc": utc_now(),
        "mode": mode_name,
        "enabled": enabled,
        "stop_requested": stop_requested,
        "max_cycles": args.max_cycles,
        "sleep_seconds_between_cycles": args.sleep_seconds_between_cycles,
        "operator_reason": args.reason,
        "authority": "none",
        "scope": "supervisor_control_packet_only",
    }
    control = compile_qi_supervised_loop_control(control_packet=packet)
    write_json(args.write, packet)
    control_path = args.write.with_name(args.write.stem + "_compiled_v0_1.json")
    write_json(control_path, control.to_dict())

    if not args.quiet:
        print(json.dumps({
            "control_packet_path": str(args.write),
            "compiled_control_path": str(control_path),
            "mode": mode_name,
            "loop_allowed": control.loop_allowed,
            "control_status": control.control_status,
            "control_reason": control.control_reason,
            "authority": "none",
        }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
