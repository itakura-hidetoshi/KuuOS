#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md"
REQUIRED_FILES = [
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR9_MERGE_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
]

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Finality Packet v0.1",
    "Status: CANDIDATE",
    "PR10 merge closure commit: `fb082f7caa0b5d009cd0dbca34412047ffe6599e`",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py",
    "Pull request: `#10`",
    "PR head commit: `294df8a141c5a0d0c18c5c61306acaf9fc06eddd`",
    "Squash merge commit: `fb082f7caa0b5d009cd0dbca34412047ffe6599e`",
    "Merged at: `2026-05-17T03:01:08Z`",
    "PASS: MGAP4D external audit readiness PR10 merge closure checked",
    "PASS: MGAP4D external audit readiness finality packet checked",
    "PASS: MGAP4D external audit readiness bundle manifest checked",
    "PASS: KuuOS all governance full checks completed",
]


def main() -> int:
    errors: list[str] = []
    text = PACKET.read_text(encoding="utf-8") if PACKET.is_file() else ""
    if not text:
        errors.append(f"missing file: {PACKET.relative_to(ROOT)}")
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
    print("PASS: MGAP4D external audit readiness finality packet checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
