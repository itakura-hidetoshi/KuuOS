#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md"
REQUIRED_FILES = [
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR11_MERGE_CLOSURE_v0_1.md",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr11_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
]

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Chain Index v0.1",
    "PASS: MGAP4D external audit readiness PR11 merge closure checked",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR11_MERGE_CLOSURE_v0_1.md",
    "Pull request: `#11`",
    "Pull request title: `Add MGAP4D PR10 merge closure v0.1`",
    "PR head commit: `d633a7c60fff5da9cd86c7a85e51aae60bed3fa8`",
    "Base before merge: `fb082f7caa0b5d009cd0dbca34412047ffe6599e`",
    "Squash merge commit: `d76fc29c09a3c87b27878bb5ec3969512e288cfd`",
    "Merged at: `2026-05-17T03:32:18Z`",
    "PR11 merge closure",
    "same-root, append-only tightening",
]


def main() -> int:
    errors: list[str] = []
    text = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else ""
    if not text:
        errors.append(f"missing file: {INDEX.relative_to(ROOT)}")
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"missing token: {token}")
    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1
    print("PASS: MGAP4D external audit readiness chain index checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
