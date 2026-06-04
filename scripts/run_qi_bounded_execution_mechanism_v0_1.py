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

from runtime.kuuos_runtime_daemon_qi_bounded_execution_mechanism_v0_1 import build_qi_bounded_execution_mechanism


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Qi bounded execution mechanism v0.1")
    parser.add_argument("--engine", type=pathlib.Path, required=True)
    parser.add_argument("--health-chain", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    result = build_qi_bounded_execution_mechanism(
        engine_packet=read_json(args.engine),
        health_packet_chain=read_json(args.health_chain),
        mechanism_context=read_json(args.context),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.mechanism_status == "QI_BOUNDED_EXECUTION_MECHANISM_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
