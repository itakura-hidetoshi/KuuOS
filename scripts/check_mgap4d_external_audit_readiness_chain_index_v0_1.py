#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md"
REQUIRED_FILES = [
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR9_MERGE_CLOSURE_v0_1.md",
    ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr9_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
    ROOT / ".github" / "workflows" / "all_governance_validation.yml",
]

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Chain Index v0.1",
    "bash scripts/check.sh",
    "PASS: MGAP4D external audit readiness PR8 merge closure checked",
    "PASS: MGAP4D external audit readiness PR9 merge closure checked",
    "PASS: MGAP4D external audit readiness PR10 merge closure checked",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    "Pull request: `#10`",
    "Pull request title: `Add MGAP4D PR9 merge closure v0.1`",
    "PR head commit: `294df8a141c5a0d0c18c5c61306acaf9fc06eddd`",
    "Base before merge: `f840ab0e8d497049ab232f187bb681c3337a3f30`",
    "Squash merge commit: `fb082f7caa0b5d009cd0dbca34412047ffe6599e`",
    "Merged at: `2026-05-17T03:01:08Z`",
    "PR10 merge closure surface",
    "PR #10 merge integration evidence",
    "traceability surface only",
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
