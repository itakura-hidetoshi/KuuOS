#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_limited_one_shot_execution_authority_grant_gate_v0_1 import evaluate_qi_limited_one_shot_execution_authority_grant


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi limited one-shot execution-authority grant gate v0.1")
    parser.add_argument("--middle-way-scope", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = evaluate_qi_limited_one_shot_execution_authority_grant(
        middle_way_scope_packet=read_json(args.middle_way_scope),
        grant_context=read_json(args.context),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.gate_status == "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
