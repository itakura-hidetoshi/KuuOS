#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md"
CHAIN_INDEX = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md"
LEDGER = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md"
POST_MERGE_RECEIPT = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md"
POST_MERGE_CLOSURE = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md"
POST_MERGE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py"
POST_MERGE_CLOSURE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py"
BUNDLE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Finality Packet v0.1",
    "Status: CANDIDATE",
    "Date: 2026-05-16",
    "Repository: itakura-hidetoshi/KuuOS",
    "Root commit: `9147dc5a00e3ffd74b85336e8a26e33091fec9f1`",
    "Post-merge commit: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Post-merge receipt closure commit: `7f53a0adff847b59f7356875e1102fb7e3faf9fe`",
    "append-only closure surface",
    "appends the main-branch post-merge green receipt",
    "appends the PR #7 post-merge receipt closure",
    "does not grant proof, truth, clinical, execution, governance-bypass, journal, community, or external-auditor acceptance authority",
    "bash scripts/check.sh",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    ".github/workflows/mgap4d_external_audit_readiness_ci_ledger_v0_1.yml",
    "Workflow run ID: `25973305278`",
    "Workflow job ID: `76349030859`",
    "Checked commit: `a9f53bad85037169a04aabf13f0296a96bff4530`",
    "Job name: `validate-mgap4d-external-audit-readiness-ledger`",
    "Workflow run ID: `25974130236`",
    "Workflow job ID: `76351200926`",
    "Checked commit: `9147dc5a00e3ffd74b85336e8a26e33091fec9f1`",
    "Job name: `Validate all governance checks`",
    "PASS: KuuOS emptiness two truths runtime audit release bundle manifest v0.1 validates",
    "PASS: MGAP4D external audit readiness CI ledger checked",
    "PASS: MGAP4D external audit readiness chain index checked",
    "PASS: MGAP4D external audit readiness bundle manifest checked",
    "PASS: KuuOS all governance full checks completed",
    "specs/mgap4d_external_audit_readiness_bundle_manifest_v0_1.generated.json",
    "Observed all-governance bundle root hash: `25958353266318c4b0e2a49ae12794c3d6f8abfa03f8fa26361269b5b295c185`",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    "Workflow run ID: `25974409859`",
    "Workflow job ID: `76351949971`",
    "Checked commit: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Branch: `main`",
    "PASS: MGAP4D external audit readiness post-merge green receipt checked",
    "Observed post-merge bundle root hash: `94c379c61e1a405b54dee326a5faad545e0e2c711afbd16f56b9d66e26ea0dff`",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    "Pull request: `#7`",
    "Pull request title: `Add MGAP4D post-merge green receipt v0.1`",
    "PR head commit: `dec5e66ee46c2649cddb6273b55136cf844d4bbc`",
    "Base before merge: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Squash merge commit: `7f53a0adff847b59f7356875e1102fb7e3faf9fe`",
    "Merged at: `2026-05-17T00:35:13Z`",
    "PASS: MGAP4D external audit readiness post-merge receipt closure checked",
    "proof authority by itself",
    "truth authority by itself",
    "clinical authority",
    "execution authority",
    "governance-bypass authority",
    "external-auditor acceptance",
    "journal acceptance",
    "community acceptance",
    "CI green is evidence, not theorem truth.",
    "Hash chain and bundle root are integrity evidence, not proof authority.",
    "External audit readiness is not external audit acceptance.",
    "Post-merge green confirms repository integration, not independent mathematical acceptance.",
    "PR merge success is integration evidence, not theorem truth.",
    "Post-merge receipt closure records integration of the receipt, not independent acceptance.",
    "Finality packet status remains `CANDIDATE` until independent external review accepts it.",
    "same-root, append-only, boundary-preserving, and non-destructive",
    "PASS: MGAP4D external audit readiness finality packet checked",
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
    "CI green proves theorem truth",
    "CI green grants execution authority",
    "CI green grants clinical authority",
    "post-merge green proves theorem truth",
    "post-merge green grants proof authority",
    "PR merge proves theorem truth",
    "PR merge grants proof authority",
    "external audit readiness equals external audit acceptance",
]


def main() -> int:
    errors: list[str] = []
    for path in [
        PACKET,
        CHAIN_INDEX,
        LEDGER,
        POST_MERGE_RECEIPT,
        POST_MERGE_CLOSURE,
        POST_MERGE_CHECKER,
        POST_MERGE_CLOSURE_CHECKER,
        BUNDLE_CHECKER,
    ]:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")

    text = PACKET.read_text(encoding="utf-8") if PACKET.is_file() else ""
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

    print("PASS: MGAP4D external audit readiness finality packet checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
