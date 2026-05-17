#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR9_MERGE_CLOSURE_v0_1.md"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness PR9 Merge Closure v0.1",
    "Status: PR9_MERGE_CLOSURE_RECORDED",
    "Date: 2026-05-17",
    "Repository: itakura-hidetoshi/KuuOS",
    "Closure kind: PR9 merge integration closure",
    "PR #9 integrated the MGAP4D PR8 merge closure layer into `main`",
    "append-only closure surface for traceability",
    "does not replace the PR8 merge closure, PR #7 closure, post-merge green receipt, finality packet, chain index, CI ledger, or bundle manifest",
    "Pull request: `#9`",
    "Pull request title: `Add MGAP4D PR8 merge closure v0.1`",
    "PR head commit: `0563ea21fd1922ca4979f7bc876aa11246aa4837`",
    "Base before merge: `d29468a831baff2c1cda847124f43a05d5574fb1`",
    "Squash merge commit: `f840ab0e8d497049ab232f187bb681c3337a3f30`",
    "Merged at: `2026-05-17T02:32:35Z`",
    "Changed files: `9`",
    "Additions: `275`",
    "Deletions: `5`",
    "Emptiness Two Truths Runtime Audit Validation` — success — workflow run ID `25979054833`",
    "MGAP4D External Audit Readiness CI Ledger v0.1` — success — workflow run ID `25979054838`",
    "Core Governance Validation` — success — workflow run ID `25979054848`",
    "All Governance Validation` — success — workflow run ID `25979054835`",
    "The squash merge commit `f840ab0e8d497049ab232f187bb681c3337a3f30` exists on `main`",
    "Add MGAP4D PR8 merge closure v0.1",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
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
    "A successful PR merge does not grant truth authority.",
    "A successful PR merge does not grant execution authority.",
    "A successful PR merge does not grant clinical authority.",
    "PR9 merge closure does not imply independent external audit acceptance.",
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
    "PR merge proves theorem truth",
    "PR merge grants proof authority",
    "PR merge grants truth authority",
    "PR merge grants execution authority",
    "PR merge grants clinical authority",
]


def main() -> int:
    errors: list[str] = []
    if not CLOSURE.is_file():
        errors.append(f"missing file: {CLOSURE.relative_to(ROOT)}")
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

    print("PASS: MGAP4D external audit readiness PR9 merge closure checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
