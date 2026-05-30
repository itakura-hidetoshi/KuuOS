#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_persistent_event_log_cursor_ledger_v0_1 import update_qi_persistent_event_log_cursor_ledger


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi persistent event log cursor ledger update v0.1")
    parser.add_argument("--tick", type=pathlib.Path, required=True)
    parser.add_argument("--prior-ledger", type=pathlib.Path, default=None)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--token-event", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-ledger", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = update_qi_persistent_event_log_cursor_ledger(
        tick_packet=read_json(args.tick),
        prior_ledger=read_json(args.prior_ledger),
        ledger_context=read_json(args.context),
        token_event=read_json(args.token_event),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_ledger is not None and result.ledger_status == "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_UPDATED":
        args.write_ledger.parent.mkdir(parents=True, exist_ok=True)
        args.write_ledger.write_text(json.dumps(result.next_ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.ledger_status == "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_UPDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
