#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_candidate_static_admissibility_preflight_v0_1 import (
    DISPOSITION_ADMISSIBLE,
    STATUS_READY,
    build_codeai_candidate_static_admissibility_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/codeai_candidate_static_admissibility_preflight_v0_1.json"
MANIFEST = ROOT / "manifests/kuuos_codeai_candidate_static_admissibility_preflight_v0_1.json"
REQUIRED_PATHS = {
    ".github/workflows/codeai-candidate-static-admissibility-preflight-v0-1.yml",
    "docs/KUUOS_CODEAI_CANDIDATE_STATIC_ADMISSIBILITY_PREFLIGHT_v0_1.md",
    "examples/codeai_candidate_static_admissibility_preflight_v0_1.json",
    "formal/KUOS/CodeAI/CandidateStaticAdmissibilityPreflightV0_1.lean",
    "formal/KuuOSCodeAICandidateStaticAdmissibilityPreflightV0_1.lean",
    "manifests/kuuos_codeai_candidate_static_admissibility_preflight_v0_1.json",
    "runtime/kuuos_codeai_candidate_static_admissibility_preflight_v0_1.py",
    "runtime/kuuos_codeai_candidate_static_admissibility_preflight_checks_v0_1.py",
    "runtime/kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1.py",
    "scripts/check_codeai_candidate_static_admissibility_preflight_v0_1.py",
    "tests/test_kuuos_codeai_candidate_static_admissibility_preflight_v0_1.py",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    result = build_codeai_candidate_static_admissibility_preflight(
        typed_edit_ir=example["typed_edit_ir"],
        typed_edit_ir_receipt=example["typed_edit_ir_receipt"],
        repository_files=example["repository_files"],
        preflight_request=example["preflight_request"],
        preflight_policy=example["preflight_policy"],
        dependency_inventory=example["dependency_inventory"],
        test_plan_catalog=example["test_plan_catalog"],
    )
    if result.status != STATUS_READY:
        fail("example blocked: " + ",".join(result.issues))
    if result.report != example["expected_report"]:
        fail("example report drift")
    if result.receipt != example["expected_receipt"]:
        fail("example receipt drift")
    if result.report["codeai_disposition"] != DISPOSITION_ADMISSIBLE:
        fail("example not admissible")
    if result.report["findings"]:
        fail("example contains findings")
    if result.report["repository_mutation_performed"] is not False:
        fail("example reports repository mutation")
    if result.report["candidate_selected"] is not False:
        fail("example reports candidate selection")
    if result.receipt["execution_authority_granted"] is not False:
        fail("example grants execution authority")

    if manifest.get("profile_version") != "CodeAI Candidate Static Admissibility Preflight v0.1":
        fail("manifest profile mismatch")
    manifest_paths = set(manifest.get("paths", []))
    if manifest_paths != REQUIRED_PATHS:
        fail("manifest paths mismatch")
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).is_file():
            fail("missing required path: " + relative)
    boundaries = set(manifest.get("fixed_boundaries", []))
    required_boundaries = {
        "static preflight != correctness proof",
        "parse success != type correctness",
        "materialized snapshot != repository mutation",
        "admissible != selected",
        "preflight receipt != execution authority",
    }
    if not required_boundaries.issubset(boundaries):
        fail("manifest boundary mismatch")
    print("CodeAI Candidate Static Admissibility Preflight v0.1: passed")


if __name__ == "__main__":
    main()
