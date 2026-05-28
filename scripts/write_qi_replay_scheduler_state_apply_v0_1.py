#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_replay_scheduler_state_apply_v0_1 import apply_qi_replay_scheduler_state


def read_json(path: pathlib.Path | None):
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi replay scheduler state apply result v0.1")
    parser.add_argument("--replay", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-state", type=pathlib.Path, default=None)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-state", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = apply_qi_replay_scheduler_state(
        replay_packet=read_json(args.replay),
        scheduler_state=read_json(args.scheduler_state),
        apply_context=read_json(args.context),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_state is not None and result.apply_status == "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED":
        args.write_state.parent.mkdir(parents=True, exist_ok=True)
        args.write_state.write_text(json.dumps(result.next_scheduler_state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.apply_status == "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
