#!/usr/bin/env python3
"""Run v0.2 validation cases for Superstring Emptiness String / Brane / Membrane Runtime."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_superstring_emptiness_string_brane_membrane_v0_2 import validate  # noqa: E402


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: run_superstring_emptiness_string_brane_membrane_cases_v0_2.py cases.json", file=sys.stderr)
        return 2
    data: Dict[str, Any] = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    results = []
    all_ok = True
    for case in data.get("cases", []):
        ok, errors, decision = validate(case.get("packet", {}))
        expected_ok = bool(case.get("expected_ok"))
        expected_decision = case.get("expected_decision")
        passed = ok == expected_ok and decision == expected_decision
        all_ok = all_ok and passed
        results.append({
            "case_id": case.get("case_id", "unknown"),
            "passed": passed,
            "expected_ok": expected_ok,
            "actual_ok": ok,
            "expected_decision": expected_decision,
            "actual_decision": decision,
            "errors": errors,
        })
    print(json.dumps({"ok": all_ok, "case_count": len(results), "results": results}, ensure_ascii=False, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
