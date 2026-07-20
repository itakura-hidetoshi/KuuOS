#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_evidence_grounded_candidate_ranking_v0_1 import (
    RANKING_DISPOSITION,
    STATUS_READY,
    build_codeai_evidence_grounded_candidate_ranking,
)
from scripts.build_codeai_evidence_grounded_candidate_ranking_fixture_v0_1 import build_fixture

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/codeai_evidence_grounded_candidate_ranking_v0_1.json"
MANIFEST = ROOT / "manifests/kuuos_codeai_evidence_grounded_candidate_ranking_v0_1.json"
REQUIRED_PATHS = {
    ".github/workflows/codeai-evidence-grounded-candidate-ranking-v0-1.yml",
    "docs/KUUOS_CODEAI_EVIDENCE_GROUNDED_CANDIDATE_RANKING_v0_1.md",
    "examples/codeai_evidence_grounded_candidate_ranking_v0_1.json",
    "formal/KUOS/CodeAI/EvidenceGroundedCandidateRankingV0_1.lean",
    "formal/KuuOSCodeAIEvidenceGroundedCandidateRankingV0_1.lean",
    "manifests/kuuos_codeai_evidence_grounded_candidate_ranking_v0_1.json",
    "runtime/kuuos_codeai_evidence_grounded_candidate_ranking_checks_v0_1.py",
    "runtime/kuuos_codeai_evidence_grounded_candidate_ranking_schema_v0_1.py",
    "runtime/kuuos_codeai_evidence_grounded_candidate_ranking_v0_1.py",
    "scripts/build_codeai_evidence_grounded_candidate_ranking_fixture_v0_1.py",
    "scripts/check_codeai_evidence_grounded_candidate_ranking_v0_1.py",
    "tests/test_kuuos_codeai_evidence_grounded_candidate_ranking_v0_1.py",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    specification = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fixture = build_fixture(specification)
    result = build_codeai_evidence_grounded_candidate_ranking(**fixture)
    repeated = build_codeai_evidence_grounded_candidate_ranking(**fixture)
    if result.status != STATUS_READY or result.ranking is None or result.receipt is None:
        fail("example blocked: " + ",".join(result.issues))
    if result.ranking != repeated.ranking or result.receipt != repeated.receipt:
        fail("evidence-grounded ranking is not deterministic")
    if result.ranking["codeai_disposition"] != RANKING_DISPOSITION:
        fail("ranking disposition mismatch")
    if result.ranking["ordered_candidate_ids"] != specification["expected_ordered_candidate_ids"]:
        fail("ranking order mismatch")
    if result.ranking["classification_counts"] != specification["expected_classification_counts"]:
        fail("classification accounting mismatch")
    if result.ranking["total_finding_count"] != specification["expected_total_finding_count"]:
        fail("finding accounting mismatch")
    if result.ranking["total_changed_path_count"] != specification["expected_total_changed_path_count"]:
        fail("changed-path accounting mismatch")
    if [item["ranking_position"] for item in result.ranking["ranked_candidates"]] != list(
        range(1, result.ranking["candidate_count"] + 1)
    ):
        fail("ranking positions are not contiguous")
    source_by_id = {
        item["candidate_id"]: item for item in fixture["source_portfolio"]["candidates"]
    }
    for ranked in result.ranking["ranked_candidates"]:
        if ranked["source_candidate_evidence"] != source_by_id[ranked["candidate_id"]]:
            fail("source candidate evidence was not preserved")
    for surface in (result.ranking, result.receipt):
        if surface["ranking_performed"] is not True:
            fail("ranking was not recorded")
        for field in (
            "candidate_selected",
            "selection_authority_granted",
            "verification_runner_invoked",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            if surface[field] is not False:
                fail("ranking boundary violated: " + field)
    if manifest.get("profile_version") != "CodeAI Evidence-Grounded Candidate Ranking v0.1":
        fail("manifest profile mismatch")
    if set(manifest.get("paths", [])) != REQUIRED_PATHS:
        fail("manifest paths mismatch")
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).is_file():
            fail("missing required path: " + relative)
    required_boundaries = {
        "evidence portfolio != ranking correctness proof",
        "ranking != candidate selection",
        "ranking position one != selected candidate",
        "ranking receipt != verification authority",
        "ranking receipt != execution authority",
        "ranking receipt != Git authority",
    }
    if not required_boundaries.issubset(set(manifest.get("fixed_boundaries", []))):
        fail("manifest boundary mismatch")
    print("CodeAI Evidence-Grounded Candidate Ranking v0.1: passed")


if __name__ == "__main__":
    main()
