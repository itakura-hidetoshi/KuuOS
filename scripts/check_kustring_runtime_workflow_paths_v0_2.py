#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "kustring_runtime_finality_v0_2.yml"

REQUIRED_PATHS = [
    "examples/kustring_runtime_v0_2.py",
    "tests/test_kustring_runtime_v0_2.py",
    "specs/kustring_runtime_packets_v0_2.json",
    "scripts/*kustring_runtime*_v0_2.py",
    "docs/KUSTRING_RUNTIME_*_v0_2.md",
    "docs/kustring_runtime_finality_ci_ledger_v0_2.md",
    ".github/workflows/kustring_runtime_finality_v0_2.yml",
]


def main() -> int:
    if not WORKFLOW.is_file():
        print("ERROR: missing workflow")
        return 1
    text = WORKFLOW.read_text(encoding="utf-8")
    missing = [p for p in REQUIRED_PATHS if p not in text]
    if missing:
        for path in missing:
            print(f"ERROR: workflow path missing: {path}")
        return 1
    print("PASS: KuString runtime workflow path filters checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())