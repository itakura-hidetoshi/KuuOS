#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_jsonl_persistent_daemon_wrapper_v0_1 import run_qi_jsonl_persistent_daemon_wrapper


def read_json(path: pathlib.Path | None):
    if path is None or not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_entries(value):
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("entries"), list):
            return [item for item in value["entries"] if isinstance(item, dict)]
        return [value]
    return []


def normalize_dict(value):
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi JSONL persistent daemon wrapper result v0.1")
    parser.add_argument("--memory", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-state", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-proposal", type=pathlib.Path, required=True)
    parser.add_argument("--process-tensor-metrics", type=pathlib.Path, required=True)
    parser.add_argument("--event-log", type=pathlib.Path, required=True)
    parser.add_argument("--ledger-state", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--start-tick", type=int, required=True)
    parser.add_argument("--tick-count", type=int, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = run_qi_jsonl_persistent_daemon_wrapper(
        memory_entries=normalize_entries(read_json(args.memory)),
        scheduler_state=normalize_dict(read_json(args.scheduler_state)),
        scheduler_proposal=normalize_dict(read_json(args.scheduler_proposal)),
        process_tensor_metrics=normalize_dict(read_json(args.process_tensor_metrics)),
        event_log_path=args.event_log,
        ledger_state_path=args.ledger_state,
        start_tick=args.start_tick,
        tick_count=args.tick_count,
        wrapper_context=normalize_dict(read_json(args.context)),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.wrapper_status == "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
