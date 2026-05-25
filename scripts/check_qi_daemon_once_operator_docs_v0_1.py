#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "qi_daemon_once_operator_v0_1.md"

REQUIRED_TERMS = [
    "run_qi_daemon_once_v0_1.py",
    "--raw-state",
    "--evidence",
    "--out-dir",
    "qi_daemon_once_result_v0_1.json",
    "qi_daemon_once_readable_summary_v0_1.json",
    "qi_daemon_once_readable_summary_v0_1.txt",
    "qi_daemon_once_manifest_v0_1.json",
    "recommended_next_runtime_mode",
    "next_tick_preparation",
    "required_pre_tick_actions",
    "projection_statuses",
    "authority: none",
    "one-shot only",
    "no autonomous daemon loop",
    "no next tick execution authority",
    "no policy mutation authority",
    "no belief update authority",
    "no memory overwrite authority",
    "no truth authority",
    "python scripts/check_qi_daemon_once_operator_cli_v0_1.py",
]


def main() -> int:
    if not DOC.is_file():
        print(f"ERROR: missing docs file: {DOC}")
        return 1
    text = DOC.read_text(encoding="utf-8")
    missing = [term for term in REQUIRED_TERMS if term not in text]
    if missing:
        for term in missing:
            print(f"ERROR: missing docs term: {term}")
        return 1
    print("PASS: Qi daemon once operator docs check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
