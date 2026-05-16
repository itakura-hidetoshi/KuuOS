#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "examples" / "kustring_runtime_v0_2.py"

spec = importlib.util.spec_from_file_location("kustring_runtime_v0_2", RUNTIME_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load runtime module")
runtime = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runtime
spec.loader.exec_module(runtime)


def coerce_value(key: str, value: Any) -> Any:
    if key == "psi_gap" and isinstance(value, str):
        return Fraction(value)
    return value


def packet_from_dict(data: dict[str, Any]) -> Any:
    kwargs = {key: coerce_value(key, value) for key, value in data.items()}
    return runtime.Packet(**kwargs)


def evaluate_file(path: pathlib.Path) -> tuple[list[dict[str, Any]], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    for item in data.get("packets", []):
        packet_id = item.get("id", "unnamed")
        packet = packet_from_dict(item.get("packet", {}))
        out = runtime.evaluate(packet)
        expected = item.get("expected_status")
        if expected is not None and out.get("status") != expected:
            errors.append(f"{packet_id}: expected {expected}, got {out.get('status')}")
        results.append({"id": packet_id, "expected_status": expected, "result": out})
    return results, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="specs/kustring_runtime_packets_v0_2.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = ROOT / args.input
    results, errors = evaluate_file(path)
    if args.json:
        print(json.dumps({"results": results, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['id']}: {item['result']['status']} ({item['result']['reason']})")
        if errors:
            for err in errors:
                print("ERROR:", err)
            return 1
        print("PASS: KuString runtime packet evaluation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())