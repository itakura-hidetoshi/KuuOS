#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, pathlib, sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_v13_21 import build_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", type=pathlib.Path, required=True)
    parser.add_argument("--license", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = build_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge(
        runtime_context=read_json(args.context),
        v13_8_to_v12_5_guarded_execution_receipt_bridge_license=read_json(args.license),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload.get("status", "").endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main())
