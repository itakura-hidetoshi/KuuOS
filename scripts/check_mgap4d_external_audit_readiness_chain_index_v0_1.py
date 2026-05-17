#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md"
LEDGER = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md"
FINALITY = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md"
POST_MERGE_RECEIPT = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md"
POST_MERGE_CLOSURE = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md"
PR8_MERGE_CLOSURE = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md"
CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py"
FINALITY_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_finality_packet_v0_1.py"
POST_MERGE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py"
POST_MERGE_CLOSURE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py"
PR8_MERGE_CLOSURE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py"
BUNDLE_CHECKER = ROOT / "scripts" / "check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py"
WORKFLOW = ROOT / ".github" / "workflows" / "mgap4d_external_audit_readiness_ci_ledger_v0_1.yml"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Chain Index v0.1",
    "machine-checkable ledger surface and an append-only finality packet",
    "bash scripts/check.sh",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    ".github/workflows/mgap4d_external_audit_readiness_ci_ledger_v0_1.yml",
    "Workflow run ID: `25973305278`",
    "Workflow job ID: `76349030859`",
    "Checked commit: `a9f53bad85037169a04aabf13f0296a96bff4530`",
    "Job name: `validate-mgap4d-external-audit-readiness-ledger`",
    "PASS: MGAP4D external audit readiness CI ledger checked",
    "PASS: MGAP4D external audit readiness chain index checked",
    "Exact green required by ledger checker",
    "exact run ID, job ID, checked commit, job name, runner image, Python version, and PASS lines",
    "scripts/run_all_governance_full_checks_v0_1.py",
    "Workflow run ID: `25974130236`",
    "Workflow job ID: `76351200926`",
    "Checked commit: `9147dc5a00e3ffd74b85336e8a26e33091fec9f1`",
    "Job name: `Validate all governance checks`",
    "PASS: KuuOS emptiness two truths runtime audit release bundle manifest v0.1 validates",
    "PASS: MGAP4D external audit readiness bundle manifest checked",
    "PASS: KuuOS all governance full checks completed",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    "PASS: MGAP4D external audit readiness finality packet checked",
    "scripts/build_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py",
    "specs/mgap4d_external_audit_readiness_bundle_manifest_v0_1.generated.json",
    "Observed pre-finality all-governance bundle root hash: `25958353266318c4b0e2a49ae12794c3d6f8abfa03f8fa26361269b5b295c185`",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    "Workflow run ID: `25974409859`",
    "Workflow job ID: `76351949971`",
    "Checked commit: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Branch: `main`",
    "Post-merge bundle root hash: `94c379c61e1a405b54dee326a5faad545e0e2c711afbd16f56b9d66e26ea0dff`",
    "PASS: MGAP4D external audit readiness post-merge green receipt checked",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    "Pull request: `#7`",
    "Pull request title: `Add MGAP4D post-merge green receipt v0.1`",
    "PR head commit: `dec5e66ee46c2649cddb6273b55136cf844d4bbc`",
    "Base before merge: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Squash merge commit: `7f53a0adff847b59f7356875e1102fb7e3faf9fe`",
    "Merged at: `2026-05-17T00:35:13Z`",
    "PASS: MGAP4D external audit readiness post-merge receipt closure checked",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
    "Pull request: `#8`",
    "Pull request title: `Add MGAP4D post-merge receipt closure v0.1`",
    "PR head commit: `98792d7e7ebd426f16c4b74eb868162d3cce09a2`",
    "Base before merge: `7f53a0adff847b59f7356875e1102fb7e3faf9fe`",
    "Squash merge commit: `d29468a831baff2c1cda847124f43a05d5574fb1`",
    "Merged at: `2026-05-17T02:02:06Z`",
    "PASS: MGAP4D external audit readiness PR8 merge closure checked",
    "archived manifest verification",
    "Lean forbidden-token audit across `457` Lean files",
    "zero observed `sorry` / `admit` / `axiom` / `constant`",
    "major theorem non-placeholder audit across `12` theorem specs",
    "analytic bridge coherence audit across `8` bridge files",
    "MGAP4D.MathlibAnalytic.ExternalAuditReadinessGate",
    "`8368 / 8368` build jobs completed",
    "final `lake build` success",
    "all-governance runner integration success",
    "finality packet closure surface",
    "post-merge all-governance green receipt surface",
    "post-merge bundle root hash evidence",
    "post-merge receipt closure surface",
    "PR #7 merge integration evidence",
    "PR8 merge closure surface",
    "PR #8 merge integration evidence",
    "traceability surface only",
    "proof authority by itself",
    "truth authority by itself",
    "clinical authority",
    "execution authority",
    "governance-bypass authority",
    "external-auditor acceptance",
    "journal acceptance",
    "community acceptance",
    "same-root, append-only tightening",
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
    "post-merge green proves theorem truth",
    "post-merge green grants proof authority",
    "PR merge proves theorem truth",
    "PR merge grants proof authority",
]


def main() -> int:
    errors: list[str] = []
    for path in [
        INDEX,
        LEDGER,
        FINALITY,
        POST_MERGE_RECEIPT,
        POST_MERGE_CLOSURE,
        PR8_MERGE_CLOSURE,
        CHECKER,
        FINALITY_CHECKER,
        POST_MERGE_CHECKER,
        POST_MERGE_CLOSURE_CHECKER,
        PR8_MERGE_CLOSURE_CHECKER,
        BUNDLE_CHECKER,
        WORKFLOW,
    ]:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")

    text = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else ""
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

    print("PASS: MGAP4D external audit readiness chain index checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
