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
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr9_merge_closure_v0_1.py",
    ROOT / "scripts" / "check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
    ROOT / ".github" / "workflows" / "mgap4d_external_audit_readiness_ci_ledger_v0_1.yml",
]

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Chain Index v0.1",
    "bash scripts/check.sh",
    "PASS: MGAP4D external audit readiness CI ledger checked",
    "PASS: MGAP4D external audit readiness chain index checked",
    "PASS: MGAP4D external audit readiness finality packet checked",
    "PASS: MGAP4D external audit readiness post-merge green receipt checked",
    "PASS: MGAP4D external audit readiness post-merge receipt closure checked",
    "PASS: MGAP4D external audit readiness PR8 merge closure checked",
    "PASS: MGAP4D external audit readiness PR9 merge closure checked",
    "PASS: MGAP4D external audit readiness bundle manifest checked",
    "PASS: KuuOS all governance full checks completed",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR9_MERGE_CLOSURE_v0_1.md",
    "Pull request: `#7`",
    "Pull request: `#8`",
    "Pull request: `#9`",
    "PR head commit: `dec5e66ee46c2649cddb6273b55136cf844d4bbc`",
    "PR head commit: `98792d7e7ebd426f16c4b74eb868162d3cce09a2`",
    "PR head commit: `0563ea21fd1922ca4979f7bc876aa11246aa4837`",
    "Squash merge commit: `7f53a0adff847b59f7356875e1102fb7e3faf9fe`",
    "Squash merge commit: `d29468a831baff2c1cda847124f43a05d5574fb1`",
    "Squash merge commit: `f840ab0e8d497049ab232f187bb681c3337a3f30`",
    "Merged at: `2026-05-17T00:35:13Z`",
    "Merged at: `2026-05-17T02:02:06Z`",
    "Merged at: `2026-05-17T02:32:35Z`",
    "post-merge receipt closure surface",
    "PR8 merge closure surface",
    "PR9 merge closure surface",
    "PR #7 merge integration evidence",
    "PR #8 merge integration evidence",
    "PR #9 merge integration evidence",
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
