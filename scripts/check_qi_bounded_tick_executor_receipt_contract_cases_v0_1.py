#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES_MANIFEST = ROOT / "validation" / "qi_bounded_tick_executor_receipt_contract_v0_1" / "cases_manifest.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_qi_bounded_tick_executor_receipt_v0_1 import validate_receipt  # noqa: E402


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"not a JSON object: {path}")
    return data


def main() -> int:
    errors: list[str] = []
    manifest = _load_json(CASES_MANIFEST)
    if manifest.get("cases_manifest_version") != "qi_bounded_tick_executor_receipt_contract_cases_v0_1":
        errors.append("bad cases_manifest_version")
    if manifest.get("validator") != "scripts/validate_qi_bounded_tick_executor_receipt_v0_1.py":
        errors.append("bad validator path")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a nonempty list")
        cases = []
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case entry must be object")
            continue
        case_id = str(case.get("case_id") or "")
        if not case_id:
            errors.append("case missing case_id")
            continue
        if case_id in seen:
            errors.append(f"duplicate case_id: {case_id}")
        seen.add(case_id)
        rel = case.get("path")
        if not isinstance(rel, str):
            errors.append(f"case {case_id} missing path")
            continue
        path = ROOT / rel
        if not path.exists():
            errors.append(f"case {case_id} missing file: {rel}")
            continue
        receipt = _load_json(path)
        receipt_errors = validate_receipt(receipt)
        actual_valid = not receipt_errors
        expected_valid = case.get("expected_valid") is True
        if actual_valid != expected_valid:
            errors.append(
                f"case {case_id} expected_valid={expected_valid} actual_valid={actual_valid} errors={receipt_errors}"
            )
        expected_error_contains = case.get("expected_error_contains")
        if expected_valid is False and expected_error_contains:
            combined = "\n".join(receipt_errors)
            if str(expected_error_contains) not in combined:
                errors.append(
                    f"case {case_id} expected error containing {expected_error_contains!r}, got {receipt_errors}"
                )
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi bounded tick executor receipt contract cases v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
