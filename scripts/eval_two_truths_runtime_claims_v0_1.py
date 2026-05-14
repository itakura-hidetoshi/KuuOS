#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "examples" / "two_truths_runtime_v0_1.py"

spec = importlib.util.spec_from_file_location("two_truths_runtime_v0_1", RUNTIME_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load two truths runtime module")
runtime = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runtime
spec.loader.exec_module(runtime)


def claim_from_dict(data: dict[str, Any]) -> Any:
    return runtime.TwoTruthsClaim(**data)


def evaluate_file(path: pathlib.Path) -> tuple[list[dict[str, Any]], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    for item in data.get("claims", []):
        claim_id = item.get("id", "unnamed")
        out = runtime.evaluate_two_truths(claim_from_dict(item.get("claim", {})))
        expected = item.get("expected_status")
        if expected is not None and out.get("status") != expected:
            errors.append(f"{claim_id}: expected {expected}, got {out.get('status')}")
        results.append({"id": claim_id, "expected_status": expected, "result": out})
    return results, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="specs/two_truths_runtime_claims_v0_1.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results, errors = evaluate_file(ROOT / args.input)
    if args.json:
        print(json.dumps({"results": results, "errors": errors}, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for item in results:
            print(f"{item['id']}: {item['result']['status']} ({item['result']['reason']})")
        if errors:
            for err in errors:
                print("ERROR:", err)
            return 1
        print("PASS: Two Truths runtime claim evaluation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
