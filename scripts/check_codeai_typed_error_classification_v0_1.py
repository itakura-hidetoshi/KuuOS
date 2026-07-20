#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    DISPOSITION_COMPLETED,
    STATUS_READY,
)
from runtime.kuuos_codeai_typed_error_classification_v0_1 import (
    build_codeai_typed_error_classification,
)
from scripts.build_codeai_typed_error_classification_fixture_v0_1 import build_fixture

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/codeai_typed_error_classification_v0_1.json"
PORTFOLIO_EXAMPLE = ROOT / "examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"
BASELINE_EXAMPLE = ROOT / "examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"
MANIFEST = ROOT / "manifests/kuuos_codeai_typed_error_classification_v0_1.json"
REQUIRED_PATHS = {
    ".github/workflows/codeai-typed-error-classification-v0-1.yml",
    "docs/KUUOS_CODEAI_TYPED_ERROR_CLASSIFICATION_v0_1.md",
    "examples/codeai_typed_error_classification_v0_1.json",
    "formal/KUOS/CodeAI/TypedErrorClassificationV0_1.lean",
    "formal/KuuOSCodeAITypedErrorClassificationV0_1.lean",
    "manifests/kuuos_codeai_typed_error_classification_v0_1.json",
    "runtime/kuuos_codeai_typed_error_classification_checks_v0_1.py",
    "runtime/kuuos_codeai_typed_error_classification_schema_v0_1.py",
    "runtime/kuuos_codeai_typed_error_classification_v0_1.py",
    "scripts/build_codeai_typed_error_classification_fixture_v0_1.py",
    "scripts/check_codeai_typed_error_classification_v0_1.py",
    "tests/test_kuuos_codeai_typed_error_classification_v0_1.py",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    specification = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    portfolio_spec = json.loads(PORTFOLIO_EXAMPLE.read_text(encoding="utf-8"))
    baseline_spec = json.loads(BASELINE_EXAMPLE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fixture = build_fixture(specification, portfolio_spec, baseline_spec)
    result = build_codeai_typed_error_classification(**fixture)
    repeated = build_codeai_typed_error_classification(**fixture)
    if result.status != STATUS_READY:
        fail("example blocked: " + ",".join(result.issues))
    if result.classification != repeated.classification or result.receipt != repeated.receipt:
        fail("typed error classification is not deterministic")
    classification = result.classification
    receipt = result.receipt
    if classification["codeai_disposition"] != DISPOSITION_COMPLETED:
        fail("classification disposition mismatch")
    if classification["candidate_count"] != specification["expected_candidate_count"]:
        fail("candidate count mismatch")
    if classification["typed_error_count"] != specification["expected_typed_error_count"]:
        fail("typed error count mismatch")
    if classification["family_counts"] != specification["expected_family_counts"]:
        fail("error family accounting mismatch")
    if classification["repair_route_counts"] != specification["expected_repair_route_counts"]:
        fail("repair route accounting mismatch")
    if classification["novelty_counts"]["known_in_replay_baseline"] != specification[
        "expected_baseline_known_error_count"
    ]:
        fail("baseline known count mismatch")
    if classification["novelty_counts"]["novel_to_replay_baseline"] != specification[
        "expected_baseline_novel_error_count"
    ]:
        fail("baseline novel count mismatch")
    if not all(item["source_finding_evidence_preserved"] for item in classification["typed_candidates"]):
        fail("source finding evidence not preserved")
    for field in (
        "ranking_performed",
        "candidate_selected",
        "verification_runner_invoked",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "repair_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
    ):
        if classification[field] is not False or receipt[field] is not False:
            fail("classification boundary violated: " + field)
    if set(manifest.get("paths", [])) != REQUIRED_PATHS:
        fail("manifest paths mismatch")
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).is_file():
            fail("missing required path: " + relative)
    boundaries = set(manifest.get("fixed_boundaries", []))
    required_boundaries = {
        "preflight finding != proven root cause",
        "historical frequency != probability",
        "repair route != repair authority",
        "typed error classification != ranking",
        "typed error classification != candidate selection",
        "classification receipt != Git authority",
    }
    if not required_boundaries.issubset(boundaries):
        fail("manifest boundary mismatch")
    print("CodeAI Typed Error Classification v0.1: passed")


if __name__ == "__main__":
    main()
