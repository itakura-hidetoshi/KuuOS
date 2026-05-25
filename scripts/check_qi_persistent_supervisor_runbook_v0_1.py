#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "qi_persistent_supervisor_operator_runbook_v0_1.md"

REQUIRED_TERMS = [
    "write_qi_supervisor_control_v0_1.py",
    "run_qi_persistent_supervisor_v0_1.py",
    "view_qi_persistent_supervisor_status_v0_1.py",
    "--allow",
    "--stop",
    "--disable",
    "--max-outer-iterations",
    "qi_persistent_supervisor_result_v0_1.json",
    "qi_persistent_supervisor_overview_v0_1.txt",
    "qi_persistent_supervisor_operator_manifest_v0_1.json",
    "qi_persistent_supervisor_manifest_v0_1.json",
    "latest_heartbeat_path",
    "latest_status_path",
    "no unbounded daemon loop",
    "control packet required",
    "no next tick execution authority",
    "no memory overwrite authority",
    "python scripts/check_qi_supervisor_control_writer_v0_1.py",
    "python scripts/check_qi_persistent_supervisor_operator_cli_v0_1.py",
    "python scripts/check_qi_persistent_supervisor_status_view_cli_v0_1.py",
]


def main() -> int:
    if not DOC.is_file():
        print(f"ERROR: missing runbook: {DOC}")
        return 1
    text = DOC.read_text(encoding="utf-8")
    missing = [term for term in REQUIRED_TERMS if term not in text]
    if missing:
        for term in missing:
            print(f"ERROR: missing runbook term: {term}")
        return 1
    print("PASS: Qi persistent supervisor runbook check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
