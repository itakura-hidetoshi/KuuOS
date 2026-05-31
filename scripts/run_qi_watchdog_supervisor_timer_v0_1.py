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

from runtime.kuuos_runtime_daemon_qi_watchdog_supervisor_timer_v0_1 import (
    build_qi_watchdog_supervisor_timer_report,
)


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Qi watchdog supervisor timer v0.1")
    parser.add_argument("--daemon-status", type=pathlib.Path, required=True)
    parser.add_argument("--event-log", type=pathlib.Path, required=True)
    parser.add_argument("--ledger-state", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-prometheus", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    result = build_qi_watchdog_supervisor_timer_report(
        daemon_status_path=args.daemon_status,
        event_log_path=args.event_log,
        ledger_state_path=args.ledger_state,
        supervisor_context=read_json(args.context),
        max_iterations=args.max_iterations,
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_prometheus is not None:
        args.write_prometheus.parent.mkdir(parents=True, exist_ok=True)
        args.write_prometheus.write_text(result.prometheus_text, encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return result.watchdog_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
