#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_PR11_MERGE_CLOSURE_v0_1.md"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness PR11 Merge Closure v0.1",
    "Status: PR11_MERGE_CLOSURE_RECORDED",
    "Pull request: `#11`",
    "Pull request title: `Add MGAP4D PR10 merge closure v0.1`",
    "PR head commit: `d633a7c60fff5da9cd86c7a85e51aae60bed3fa8`",
    "Base before merge: `fb082f7caa0b5d009cd0dbca34412047ffe6599e`",
    "Squash merge commit: `d76fc29c09a3c87b27878bb5ec3969512e288cfd`",
    "Merged at: `2026-05-17T03:32:18Z`",
    "All Governance Validation` — success — workflow run ID `25980273642`",
    "Emptiness Two Truths Runtime Audit Validation` — success — workflow run ID `25980273615`",
    "Core Governance Validation` — success — workflow run ID `25980273619`",
    "MGAP4D External Audit Readiness CI Ledger v0.1` — success — workflow run ID `25980273620`",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py",
    "repository-side traceability evidence only",
    "A successful PR merge is integration evidence, not theorem truth.",
    "same-root, append-only, boundary-preserving, and non-destructive",
]

FORBIDDEN_TOKENS = [
    "proof_authority_granted: true",
    "truth_authority_granted: true",
    "clinical_authority_granted: true",
    "execution_authority_granted: true",
    "external_auditor_acceptance: true",
    "PR merge proves theorem truth",
]


def main() -> int:
    errors: list[str] = []
    text = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""
    if not text:
        errors.append(f"missing file: {DOC.relative_to(ROOT)}")
    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"missing token: {token}")
    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"forbidden token: {token}")
    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1
    print("PASS: MGAP4D external audit readiness PR11 merge closure checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
