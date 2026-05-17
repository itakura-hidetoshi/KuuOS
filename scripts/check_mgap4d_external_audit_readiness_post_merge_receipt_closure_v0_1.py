#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Post-Merge Receipt Closure v0.1",
    "Status: POST_MERGE_RECEIPT_CLOSURE_RECORDED",
    "Date: 2026-05-17",
    "Repository: itakura-hidetoshi/KuuOS",
    "Closure kind: post-merge receipt integration closure",
    "post-merge green receipt itself was integrated into `main` through PR #7",
    "append-only closure surface for traceability",
    "does not replace the post-merge green receipt, finality packet, chain index, CI ledger, or bundle manifest",
    "Pull request: `#7`",
    "Pull request title: `Add MGAP4D post-merge green receipt v0.1`",
    "PR head commit: `dec5e66ee46c2649cddb6273b55136cf844d4bbc`",
    "Base before merge: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Squash merge commit: `7f53a0adff847b59f7356875e1102fb7e3faf9fe`",
    "Merged at: `2026-05-17T00:35:13Z`",
    "Changed files: `9`",
    "Additions: `292`",
    "Deletions: `7`",
    "MGAP4D External Audit Readiness CI Ledger v0.1` — success",
    "Emptiness Two Truths Runtime Audit Validation` — success",
    "All Governance Validation` — success",
    "Core Governance Validation` — success",
    "The squash merge commit `7f53a0adff847b59f7356875e1102fb7e3faf9fe` exists on `main`",
    "Add MGAP4D post-merge green receipt v0.1",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    "scripts/run_all_governance_full_checks_v0_1.py",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    "scripts/build_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
    "repository-side traceability evidence only",
    "proof authority by itself",
    "truth authority by itself",
    "clinical authority",
    "execution authority",
    "governance-bypass authority",
    "external-auditor acceptance",
    "journal acceptance",
    "community acceptance",
    "A successful PR merge is integration evidence, not theorem truth.",
    "A successful PR merge does not grant proof authority.",
    "A successful PR merge does not grant execution authority.",
    "A successful PR merge does not grant clinical authority.",
    "Post-merge receipt closure does not imply independent external audit acceptance.",
    "same-root, append-only, boundary-preserving, and non-destructive",
]

FORBIDDEN_TOKENS = [
    "proof_authority_granted: true",
    "truth_authority_granted: true",
    "clinical_authority_granted: true",
    "execution_authority_granted: true",
    "governance_bypass_authority_granted: true",
    "external_auditor_acceptance: true",
    "journal_acceptance: true",
    "community_acceptance: true",
    "successful PR merge proves theorem truth",
    "successful PR merge grants proof authority",
    "successful PR merge grants execution authority",
    "post-merge receipt closure grants external audit acceptance",
]


def main() -> int:
    errors: list[str] = []
    if not CLOSURE.is_file():
        errors.append(f"missing closure: {CLOSURE.relative_to(ROOT)}")
        text = ""
    else:
        text = CLOSURE.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"missing token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"forbidden authority-expansion token: {token}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: MGAP4D external audit readiness post-merge receipt closure checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
