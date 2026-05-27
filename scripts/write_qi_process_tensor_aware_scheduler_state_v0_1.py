#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_1 import step_qi_process_tensor_aware_scheduler_state


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi process tensor aware scheduler state v0.1")
    parser.add_argument("--state", type=pathlib.Path, required=True)
    parser.add_argument("--proposal", type=pathlib.Path, required=True)
    parser.add_argument("--metrics", type=pathlib.Path, required=True)
    parser.add_argument("--current-tick", type=int, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-state", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = step_qi_process_tensor_aware_scheduler_state(
        scheduler_state=read_json(args.state),
        scheduler_proposal=read_json(args.proposal),
        process_tensor_metrics=read_json(args.metrics),
        current_tick=args.current_tick,
    )
    payload = result.to_dict()
    write_json(args.write, payload)
    if args.write_state:
        write_json(args.write_state, payload.get("scheduler_result", {}).get("scheduler_state", {}))
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.adjustment_status == "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
