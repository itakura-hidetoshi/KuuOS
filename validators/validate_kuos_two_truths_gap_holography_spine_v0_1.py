#!/usr/bin/env python3
"""
validate_kuos_two_truths_gap_holography_spine_v0_1.py

Standalone validator for the KuuOS Two-Truth Gap-Holography Spine v0.1.

This validator checks repository-surface consistency only. A PASS is a
consistency receipt, not theorem authority, truth authority, execution authority,
medical authority, or ultimate-exhaustion authority.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/KUOS_TWO_TRUTHS_GAP_HOLOGRAPHY_SPINE_v0_1.md",
    "specs/kuos_two_truths_gap_holography_spine_v0_1.yaml",
    "lean/KSTHolo/TwoTruthGapHolographySpine_v0_1.lean",
    "manifests/kuos_two_truths_gap_holography_spine_manifest_v0_1.json",
    "validation_cases/kuos_two_truths_gap_holography_spine_validation_cases_v0_1.yaml",
    "chain_indexes/kuos_two_truths_gap_holography_spine_chain_index_v0_1.yaml",
    "docs/KUOS_TWO_TRUTHS_GAP_HOLOGRAPHY_SPINE_RUNBOOK_v0_1.md",
    "validators/validate_kuos_two_truths_gap_holography_spine_v0_1.py",
    "scripts/run_kuos_two_truths_gap_holography_spine_checks_v0_1.py",
    ".github/workflows/two_truths_gap_holography_spine_validation.yml",
    "packets/kuos_two_truths_gap_holography_spine_release_packet_v0_1.json",
    "packets/kuos_two_truths_gap_holography_spine_baseline_lock_packet_v0_1.json",
]

REQUIRED_DOC_SNIPPETS = [
    "KuuOS uses gap-stabilized conventional records for scoped prediction",
    "preserving the unrecorded emptiness",
    "stable conventional prediction != ultimate exhaustion",
    "image non-vacuity != kernel collapse",
    "record null != ultimate null",
    "gap-stable != fully flat",
    "PredictionSufficient_Delta",
    "KernelZeroWitness",
    "UltimateIdentityWitness",
    "append-only",
]

REQUIRED_SPEC_SNIPPETS = [
    "positive_gap",
    "positive_visible_spectral_weight",
    "unique_non_vacuous_gap_record",
    "conventional_image_membership",
    "gap_holonomy_zero",
    "gap_visible_stability",
    "scoped_prediction_sufficiency",
    "no_ultimate_exhaustion",
    "kernel_zero",
    "ultimate_identity",
    "residue_erasure",
]

REQUIRED_LEAN_SNIPPETS = [
    "namespace KuuOS",
    "namespace KSTHolo",
    "structure SpectralGapData",
    "structure GapRecordImageWitness",
    "theorem gap_path_independent_of_gap_holonomy_zero",
    "structure StableConventionalRecord",
    "structure PredictionSufficientConcrete",
    "theorem fullAnalyticGap_theorem_local",
]

FORBIDDEN_LEAN_SNIPPETS = [
    " sorry",
    "\nsorry",
    "admit",
    "False.elim",
]

REQUIRED_MANIFEST_KEYS = [
    "id",
    "status",
    "mode",
    "overwrite_forbidden",
    "artifacts",
    "core_chain",
    "authorized_claims",
    "forbidden_claims",
    "fixed_invariants",
    "update_policy",
]

REQUIRED_CHAIN_SNIPPETS = [
    "baseline_documentation",
    "machine_readable_specification",
    "lean_facing_theorem_spine",
    "baseline_manifest",
    "validation_case_bundle",
    "standalone_validator",
    "reviewer_runbook",
    "ci_workflow",
    "make_target",
]

REQUIRED_WORKFLOW_SNIPPETS = [
    "Two-Truth Gap-Holography Spine Validation",
    "scripts/run_kuos_two_truths_gap_holography_spine_checks_v0_1.py",
    "PASS is a consistency receipt only",
]

RELEASE_PACKET = "packets/kuos_two_truths_gap_holography_spine_release_packet_v0_1.json"
BASELINE_LOCK_PACKET = "packets/kuos_two_truths_gap_holography_spine_baseline_lock_packet_v0_1.json"


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def require_file(rel: str) -> None:
    path = ROOT / rel
    if not path.exists():
        fail(f"missing required file: {rel}")
    if not path.is_file():
        fail(f"required path is not a file: {rel}")


def require_snippets(label: str, text: str, snippets: Iterable[str]) -> None:
    missing = [s for s in snippets if s not in text]
    if missing:
        fail(f"{label} missing snippets: {missing}")


def forbid_snippets(label: str, text: str, snippets: Iterable[str]) -> None:
    present = [s for s in snippets if s in text]
    if present:
        fail(f"{label} contains forbidden snippets: {present}")


def validate_manifest() -> None:
    rel = "manifests/kuos_two_truths_gap_holography_spine_manifest_v0_1.json"
    data = json.loads(read_text(rel))
    missing_keys = [k for k in REQUIRED_MANIFEST_KEYS if k not in data]
    if missing_keys:
        fail(f"manifest missing keys: {missing_keys}")

    if data.get("status") != "confirmed_baseline":
        fail("manifest status must be confirmed_baseline")
    if data.get("mode") != "append_only":
        fail("manifest mode must be append_only")
    if data.get("overwrite_forbidden") is not True:
        fail("manifest overwrite_forbidden must be true")

    artifacts = data.get("artifacts", {})
    flattened = []
    for value in artifacts.values():
        if isinstance(value, list):
            flattened.extend(value)
    for rel_path in [
        "docs/KUOS_TWO_TRUTHS_GAP_HOLOGRAPHY_SPINE_v0_1.md",
        "specs/kuos_two_truths_gap_holography_spine_v0_1.yaml",
        "lean/KSTHolo/TwoTruthGapHolographySpine_v0_1.lean",
        "validators/validate_kuos_two_truths_gap_holography_spine_v0_1.py",
        "scripts/run_kuos_two_truths_gap_holography_spine_checks_v0_1.py",
        ".github/workflows/two_truths_gap_holography_spine_validation.yml",
        RELEASE_PACKET,
        BASELINE_LOCK_PACKET,
    ]:
        if rel_path not in flattened:
            fail(f"manifest artifacts missing {rel_path}")

    forbidden = set(data.get("forbidden_claims", []))
    for claim in ["kernel_zero", "ultimate_identity", "ultimate_exhaustion", "residue_erasure"]:
        if claim not in forbidden:
            fail(f"manifest forbidden_claims missing {claim}")

    update_policy = data.get("update_policy", {})
    for key in ["append_only", "overwrite_forbidden", "destructive_replacement_forbidden"]:
        if update_policy.get(key) is not True:
            fail(f"manifest update_policy.{key} must be true")


def validate_release_packet() -> None:
    data = json.loads(read_text(RELEASE_PACKET))
    if data.get("status") != "released_baseline":
        fail("release packet status must be released_baseline")
    if data.get("update_policy", {}).get("overwrite_forbidden") is not True:
        fail("release packet must be overwrite_forbidden")
    for claim in ["kernel_zero", "ultimate_identity", "ultimate_exhaustion", "residue_erasure"]:
        if claim not in set(data.get("forbidden_claims", [])):
            fail(f"release packet forbidden_claims missing {claim}")
    boundary = data.get("validation_boundary", {})
    if boundary.get("pass_means") != "repository-surface consistency receipt only":
        fail("release packet pass_means must be repository-surface consistency receipt only")


def validate_baseline_lock_packet() -> None:
    data = json.loads(read_text(BASELINE_LOCK_PACKET))
    if data.get("status") != "baseline_locked":
        fail("baseline lock packet status must be baseline_locked")
    lock_policy = data.get("lock_policy", {})
    for key in ["overwrite_forbidden", "destructive_replacement_forbidden", "append_only", "same_root_required"]:
        if lock_policy.get(key) is not True:
            fail(f"baseline lock lock_policy.{key} must be true")
    locked_forbidden = set(data.get("locked_forbidden_transitions", []))
    for transition in [
        "image_non_vacuity_to_kernel_zero",
        "prediction_sufficiency_to_ultimate_identity",
        "prediction_sufficiency_to_ultimate_exhaustion",
        "gap_stability_to_full_flatness",
        "record_extraction_to_residue_erasure",
        "validation_pass_to_theorem_authority",
    ]:
        if transition not in locked_forbidden:
            fail(f"baseline lock missing forbidden transition {transition}")


def main() -> int:
    for rel in REQUIRED_FILES:
        require_file(rel)

    doc = read_text("docs/KUOS_TWO_TRUTHS_GAP_HOLOGRAPHY_SPINE_v0_1.md")
    spec = read_text("specs/kuos_two_truths_gap_holography_spine_v0_1.yaml")
    lean = read_text("lean/KSTHolo/TwoTruthGapHolographySpine_v0_1.lean")
    cases = read_text("validation_cases/kuos_two_truths_gap_holography_spine_validation_cases_v0_1.yaml")
    chain = read_text("chain_indexes/kuos_two_truths_gap_holography_spine_chain_index_v0_1.yaml")
    runbook = read_text("docs/KUOS_TWO_TRUTHS_GAP_HOLOGRAPHY_SPINE_RUNBOOK_v0_1.md")
    workflow = read_text(".github/workflows/two_truths_gap_holography_spine_validation.yml")
    makefile = read_text("Makefile")

    require_snippets("doc", doc, REQUIRED_DOC_SNIPPETS)
    require_snippets("spec", spec, REQUIRED_SPEC_SNIPPETS)
    require_snippets("lean", lean, REQUIRED_LEAN_SNIPPETS)
    forbid_snippets("lean", lean, FORBIDDEN_LEAN_SNIPPETS)
    require_snippets("chain index", chain, REQUIRED_CHAIN_SNIPPETS)
    require_snippets("validation cases", cases, ["fail_lean_contains_sorry", "pass_complete_baseline_bundle"])
    require_snippets("runbook", runbook, ["validator", "PASS is a consistency receipt", "not theorem authority"])
    require_snippets("workflow", workflow, REQUIRED_WORKFLOW_SNIPPETS)
    require_snippets("Makefile", makefile, ["two-truths-gap-holography-spine-checks"])

    validate_manifest()
    validate_release_packet()
    validate_baseline_lock_packet()

    print("PASS: KuuOS Two-Truth Gap-Holography Spine v0.1 validation succeeded")
    print("NOTE: PASS is a consistency receipt, not truth/theorem/execution/ultimate-exhaustion authority.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
