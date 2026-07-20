#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1 import (
    PORTFOLIO_DISPOSITION,
    STATUS_READY,
    build_codeai_evidence_bearing_candidate_portfolio,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"
MANIFEST = ROOT / "manifests/kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1.json"
REQUIRED_PATHS = {
    ".github/workflows/codeai-evidence-bearing-candidate-portfolio-v0-1.yml",
    "docs/KUUOS_CODEAI_EVIDENCE_BEARING_CANDIDATE_PORTFOLIO_v0_1.md",
    "examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json",
    "formal/KUOS/CodeAI/EvidenceBearingCandidatePortfolioV0_1.lean",
    "formal/KuuOSCodeAIEvidenceBearingCandidatePortfolioV0_1.lean",
    "manifests/kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1.json",
    "runtime/kuuos_codeai_evidence_bearing_candidate_portfolio_checks_v0_1.py",
    "runtime/kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1.py",
    "runtime/kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1.py",
    "scripts/check_codeai_evidence_bearing_candidate_portfolio_v0_1.py",
    "tests/test_kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1.py",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    result = build_codeai_evidence_bearing_candidate_portfolio(
        portfolio_request=example["portfolio_request"],
        portfolio_policy=example["portfolio_policy"],
        candidate_preflight_bundles=example["candidate_preflight_bundles"],
    )
    if result.status != STATUS_READY:
        fail("example blocked: " + ",".join(result.issues))
    if result.portfolio != example["expected_portfolio"]:
        fail("example portfolio drift")
    if result.receipt != example["expected_receipt"]:
        fail("example receipt drift")
    if result.portfolio["codeai_disposition"] != PORTFOLIO_DISPOSITION:
        fail("example portfolio disposition mismatch")
    if result.portfolio["classification_counts"] != {
        "admissible": 1,
        "repairable": 1,
        "hold": 1,
        "rejected": 1,
    }:
        fail("classification accounting mismatch")
    if result.portfolio["total_finding_count"] != 3:
        fail("finding evidence accounting mismatch")
    for field in (
        "ranking_performed",
        "candidate_selected",
        "verification_runner_invoked",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "execution_authority_granted",
        "git_authority_granted",
    ):
        if result.portfolio[field] is not False:
            fail("portfolio boundary violated: " + field)

    if manifest.get("profile_version") != "CodeAI Evidence-Bearing Candidate Portfolio v0.1":
        fail("manifest profile mismatch")
    if set(manifest.get("paths", [])) != REQUIRED_PATHS:
        fail("manifest paths mismatch")
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).is_file():
            fail("missing required path: " + relative)
    boundaries = set(manifest.get("fixed_boundaries", []))
    required_boundaries = {
        "preflight classification != ranking",
        "admissible != selected",
        "repairable != automatically repaired",
        "portfolio receipt != verification authority",
        "portfolio receipt != execution authority",
        "portfolio receipt != Git authority",
    }
    if not required_boundaries.issubset(boundaries):
        fail("manifest boundary mismatch")
    print("CodeAI Evidence-Bearing Candidate Portfolio v0.1: passed")


if __name__ == "__main__":
    main()
