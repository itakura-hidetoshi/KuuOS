#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_persistent_process_tensor_daemon_v0_1 import run_qi_persistent_process_tensor_daemon_tick


def read_json(path: pathlib.Path | None):
    if path is None or not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_entries(value) -> list[dict]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("entries"), list):
            return [item for item in value["entries"] if isinstance(item, dict)]
        return [value]
    return []


def normalize_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi persistent process tensor daemon tick v0.1")
    parser.add_argument("--memory", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-state", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-proposal", type=pathlib.Path, required=True)
    parser.add_argument("--process-tensor-metrics", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--current-tick", type=int, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    result = run_qi_persistent_process_tensor_daemon_tick(
        memory_entries=normalize_entries(read_json(args.memory)),
        scheduler_state=normalize_dict(read_json(args.scheduler_state)),
        scheduler_proposal=normalize_dict(read_json(args.scheduler_proposal)),
        process_tensor_metrics=normalize_dict(read_json(args.process_tensor_metrics)),
        runtime_context=normalize_dict(read_json(args.context)),
        current_tick=args.current_tick,
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.daemon_status == "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
