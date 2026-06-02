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

from runtime.kuuos_runtime_daemon_qi_adaptive_window_scheduler_v0_1 import run_qi_adaptive_window_scheduler


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def entries(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict) and isinstance(value.get("entries"), list):
        return [item for item in value["entries"] if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Qi adaptive window scheduler v0.1")
    parser.add_argument("--decisionos", type=pathlib.Path, required=True)
    parser.add_argument("--cbf", type=pathlib.Path, required=True)
    parser.add_argument("--token-ledger", type=pathlib.Path, required=True)
    parser.add_argument("--process-tensor", type=pathlib.Path, required=True)
    parser.add_argument("--memory", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-state", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-proposal", type=pathlib.Path, required=True)
    parser.add_argument("--process-tensor-metrics", type=pathlib.Path, required=True)
    parser.add_argument("--event-log", type=pathlib.Path, required=True)
    parser.add_argument("--ledger-state", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    result = run_qi_adaptive_window_scheduler(
        decisionos_packet=read_json(args.decisionos),
        cbf_packet=read_json(args.cbf),
        token_ledger_packet=read_json(args.token_ledger),
        process_tensor_packet=read_json(args.process_tensor),
        memory_entries=entries(read_json(args.memory)),
        scheduler_state=read_json(args.scheduler_state),
        scheduler_proposal=read_json(args.scheduler_proposal),
        process_tensor_metrics=read_json(args.process_tensor_metrics),
        event_log_path=args.event_log,
        ledger_state_path=args.ledger_state,
        adaptive_context=read_json(args.context),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.adaptive_scheduler_status == "QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
