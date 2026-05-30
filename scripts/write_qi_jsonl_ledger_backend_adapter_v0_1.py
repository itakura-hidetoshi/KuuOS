#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_jsonl_ledger_backend_adapter_v0_1 import apply_qi_jsonl_ledger_backend_adapter


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi JSONL ledger backend adapter result v0.1")
    parser.add_argument("--tick", type=pathlib.Path, required=True)
    parser.add_argument("--event-log", type=pathlib.Path, required=True)
    parser.add_argument("--ledger-state", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, required=True)
    parser.add_argument("--token-event", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = apply_qi_jsonl_ledger_backend_adapter(
        tick_packet=read_json(args.tick),
        event_log_path=args.event_log,
        ledger_state_path=args.ledger_state,
        ledger_context=read_json(args.context),
        token_event=read_json(args.token_event),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.backend_status == "QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
