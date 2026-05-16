#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md"

REQUIRED_TOKENS = [
    "MGAP4D External Audit Readiness CI Ledger v0.1",
    "Status: CI green from provided GitHub Actions log excerpt",
    "Date: 2026-05-16",
    "Repository: itakura-hidetoshi/KuuOS",
    "Command surface: `bash scripts/check.sh`",
    "Archived manifest verification: passed",
    "Lean files scanned: `457`",
    "`sorry`: `0`",
    "`admit`: `0`",
    "`axiom`: `0`",
    "`constant`: `0`",
    "Major theorem specs audited: `12`",
    "Bridge files audited: `8`",
    "`exact_value_eq_3320`",
    "`exactGapValueReal`",
    "infinite-dimensional Yang-Mills target layer",
    "infinite-dimensional residual filling bridge",
    "hard physical residual hardening map",
    "Hilbert construction lane hardening",
    "self-adjoint HPhys lane hardening",
    "continuum Yang-Mills lane hardening",
    "plaquette spectral weight lane hardening",
    "four-lane residual closure",
    "internal review residual closure gate",
    "external audit readiness gate",
    "Lean files: `457`",
    "Imports: `1191`",
    "Declaration-like lines: `2602`",
    "Namespace lines: `938`",
    "Total lines: `27203`",
    "Built target: `MGAP4D.MathlibAnalytic.ExternalAuditReadinessGate`",
    "Build jobs: `8368 / 8368`",
    "Result: `Build completed successfully (8368 jobs)`",
    "Result: `Build completed successfully (0 jobs)`",
    "manifest integrity evidence",
    "Lean forbidden-token absence evidence",
    "major theorem non-placeholder surface evidence",
    "analytic bridge coherence evidence",
    "hardening lane audit evidence",
    "external audit readiness gate build evidence",
    "lake build success evidence",
    "Dedicated ledger CI green record",
    "Status: dedicated ledger CI green recorded",
    "Workflow run ID: `25973305278`",
    "Workflow job ID: `76349030859`",
    "Checked commit: `a9f53bad85037169a04aabf13f0296a96bff4530`",
    "Job name: `validate-mgap4d-external-audit-readiness-ledger`",
    "Runner image: `ubuntu-24.04`",
    "Python version: `3.12.13`",
    "Started: `2026-05-16T21:23:53Z`",
    "Completed: `2026-05-16T21:23:55Z`",
    "`PASS: MGAP4D external audit readiness CI ledger checked`",
    "`PASS: MGAP4D external audit readiness chain index checked`",
    "GitHub Actions checked surfaces",
    "This CI green record does not expand authority",
    "proof authority by itself",
    "truth authority by itself",
    "clinical authority",
    "execution authority",
    "governance-bypass authority",
    "external-auditor acceptance",
    "journal or community acceptance",
    "append-only",
    "boundary-preserving",
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
]


def main() -> int:
    errors: list[str] = []
    if not LEDGER.is_file():
        errors.append(f"missing ledger: {LEDGER.relative_to(ROOT)}")
        text = ""
    else:
        text = LEDGER.read_text(encoding="utf-8")

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

    print("PASS: MGAP4D external audit readiness CI ledger checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())