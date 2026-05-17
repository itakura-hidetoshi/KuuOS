#!/usr/bin/env python3
"""
Validation-case runner for Superstring Emptiness String / Brane / Membrane Runtime v0.1.

Usage:
  python validators/run_superstring_emptiness_string_brane_membrane_cases_v0_1.py \
    validation_cases/superstring_emptiness_string_brane_membrane_validation_cases_v0_1.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Allow running from repository root without packaging.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_superstring_emptiness_string_brane_membrane_v0_1 import validate  # noqa: E402


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: run_superstring_emptiness_string_brane_membrane_cases_v0_1.py cases.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])

    results = []
    all_ok = True
    for case in cases:
        case_id = case.get("case_id", "unknown")
        expected_ok = bool(case.get("expected_ok"))
        expected_decision = case.get("expected_decision")
        packet = case.get("packet", {})
        ok, errors, decision = validate(packet)
        passed = ok == expected_ok and decision == expected_decision
        if not passed:
            all_ok = False
        results.append({
            "case_id": case_id,
            "passed": passed,
            "expected_ok": expected_ok,
            "actual_ok": ok,
            "expected_decision": expected_decision,
            "actual_decision": decision,
            "errors": errors,
        })

    print(json.dumps({"ok": all_ok, "case_count": len(cases), "results": results}, ensure_ascii=False, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
