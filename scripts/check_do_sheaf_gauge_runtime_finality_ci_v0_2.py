#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "do_sheaf_gauge_runtime_finality_v0_2.yml"

REQUIRED = [
    "Dependent Origination Sheaf Gauge Runtime Finality v0.2",
    "workflow_dispatch",
    "actions/checkout@v4",
    "actions/setup-python@v5",
    "python-version: '3.12'",
    "python3 scripts/run_do_sheaf_gauge_runtime_finality_checks_v0_2.py",
]


def main() -> int:
    errors: list[str] = []
    if not WORKFLOW.is_file():
        errors.append("missing workflow")
    else:
        text = WORKFLOW.read_text(encoding="utf-8")
        for token in REQUIRED:
            if token not in text:
                errors.append(f"workflow missing: {token}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: DO sheaf gauge runtime finality CI workflow checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
