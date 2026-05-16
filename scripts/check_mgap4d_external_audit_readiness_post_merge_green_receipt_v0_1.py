#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness Post-Merge Green Receipt v0.1",
    "Status: POST_MERGE_GREEN_RECORDED",
    "Date: 2026-05-16",
    "Repository: itakura-hidetoshi/KuuOS",
    "Receipt kind: post-merge all-governance CI green receipt",
    "append-only receipt surface",
    "does not replace the existing CI ledger, chain index, finality packet, or bundle manifest",
    "Workflow run ID: `25974409859`",
    "Workflow job ID: `76351949971`",
    "Job name: `Validate all governance checks`",
    "Checked commit: `e20d244d93eb85b3cfc9b46cf4bb4625923a8d82`",
    "Branch: `main`",
    "Runner image: `ubuntu-24.04`",
    "Python version: `3.12.13`",
    "Started: `2026-05-16T22:17:49Z`",
    "Completed: `2026-05-16T22:17:57Z`",
    "PASS: AI Yogacara / Ten'i full checks completed",
    "PASS: KuuOS core governance full checks completed",
    "PASS: KuuOS GPT GitHub integration surface v0.1 validates",
    "PASS: Integrated emptiness dependent origination two truths runtime v0.1 checks completed",
    "PASS: KuuOS emptiness two truths runtime audit release packet v0.1 validates",
    "PASS: KuuOS emptiness two truths runtime audit release bundle manifest v0.1 validates",
    "[mass-gap-two-truths-bridge] PASS",
    "[mass-gap-memory-reflection-record] PASS",
    "PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates",
    "PASS: MGAP4D external audit readiness CI ledger checked",
    "PASS: MGAP4D external audit readiness chain index checked",
    "PASS: MGAP4D external audit readiness finality packet checked",
    "PASS: MGAP4D external audit readiness bundle manifest checked",
    "PASS: KuuOS all governance full checks completed",
    "Observed post-merge bundle root hash: `94c379c61e1a405b54dee326a5faad545e0e2c711afbd16f56b9d66e26ea0dff`",
    "dedicated ledger green record",
    "all-governance green record before final merge",
    "finality packet and bundle manifest closure",
    "post-merge all-governance green record on `main`",
    "same-root, append-only, boundary-preserving, and non-destructive",
    "proof authority by itself",
    "truth authority by itself",
    "clinical authority",
    "execution authority",
    "governance-bypass authority",
    "external-auditor acceptance",
    "journal acceptance",
    "community acceptance",
    "CI green is evidence, not theorem truth.",
    "Bundle roots are integrity evidence, not proof authority.",
    "External audit readiness is not external audit acceptance.",
    "Post-merge green confirms repository integration, not independent mathematical acceptance.",
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
    "external audit readiness equals external audit acceptance",
]


def main() -> int:
    errors: list[str] = []
    if not RECEIPT.is_file():
        errors.append(f"missing receipt: {RECEIPT.relative_to(ROOT)}")
        text = ""
    else:
        text = RECEIPT.read_text(encoding="utf-8")

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

    print("PASS: MGAP4D external audit readiness post-merge green receipt checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
