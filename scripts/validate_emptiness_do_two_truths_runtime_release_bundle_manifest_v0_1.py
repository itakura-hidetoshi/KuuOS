#!/usr/bin/env python3
"""Validate the KuuOS Emptiness / Dependent Origination / Two Truths runtime audit release bundle manifest v0.1.

Stdlib-only validator.
It checks that all bundle entries exist and that required non-authority fixed points are preserved.

Boundary notes:
- Boundary documents and validators are allowed to mention denied claims as denied-claim examples.
- This validator rejects positive YAML-style authority escalation assertions in public release artifacts.
- It does not scan validator source code for sentinel strings used by validators themselves.
- CI ledger status wording is intentionally matched by stable semantic anchors, not one brittle heading string.
- Green CI observations are accepted only when accompanied by explicit non-authority boundary tokens.
- Generated audit artifacts are deterministically rebuilt before validation so that each governance shard is self-contained.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANIFEST = "specs/kuos_core_release_bundle_manifest_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml"
CI_LEDGER = "docs/CI_LEDGER_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md"
AUDIT_CHAIN_BUILDER = ROOT / "scripts" / "build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py"

REQUIRED_FILES = [
    MANIFEST,
    "specs/kuos_core_release_packet_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml",
    "specs/kuos_core_manifest_addendum_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml",
    CI_LEDGER,
    "docs/EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_PUBLIC_RELEASE_v0_1.md",
    "docs/RELEASE_NOTES_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/PUBLICATION_CHECKLIST_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md",
    "docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md",
    "specs/emptiness_do_two_truths_runtime_claims_v0_1.json",
    "specs/emptiness_do_two_truths_runtime_audit_events_v0_1.generated.jsonl",
    "specs/emptiness_do_two_truths_runtime_audit_chain_v0_1.generated.jsonl",
    "scripts/export_emptiness_do_two_truths_runtime_audit_v0_1.py",
    "scripts/build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py",
    "scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py",
    "scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py",
    "scripts/validate_emptiness_do_two_truths_runtime_release_packet_v0_1.py",
    "scripts/validate_emptiness_do_two_truths_runtime_release_bundle_manifest_v0_1.py",
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml",
    "Makefile",
]

PUBLIC_ARTIFACTS_TO_SCAN = [
    MANIFEST,
    "specs/kuos_core_release_packet_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml",
    "specs/kuos_core_manifest_addendum_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml",
    CI_LEDGER,
    "docs/EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_PUBLIC_RELEASE_v0_1.md",
    "docs/RELEASE_NOTES_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/PUBLICATION_CHECKLIST_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md",
    "docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md",
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml",
    "Makefile",
]

REQUIRED_TOKENS = {
    MANIFEST: [
        "release_bundle_manifest",
        "release_packet_validator",
        "release_bundle_manifest_validator",
        "dedicated_ci",
        "all_governance_checks",
        "make emptiness-two-truths-runtime-audit-checks",
        "make all-governance-checks",
        "ci_pass_not_theorem_truth",
        "ci_pass_not_execution_authority",
        "hash_chain_continuity_not_truth",
        "audit_chain_structural_consistency_not_theorem_authority",
        "runtime_audit_not_execution_authority",
        "ci_green_recorded: false",
        "final_archive_ready: false",
    ],
    CI_LEDGER: [
        "Status:",
        "do_not_claim_ci_green",
        "CI success is not theorem truth",
        "CI success is not execution authority",
        "runtime chain passed structurally",
        "ci_pass_not_theorem_truth",
        "ci_pass_not_execution_authority",
        "audit_chain_structural_consistency_not_theorem_authority",
    ],
    "Makefile": [
        "emptiness-two-truths-runtime-audit-checks:",
        "python3 scripts/validate_emptiness_do_two_truths_runtime_release_packet_v0_1.py",
        "python3 scripts/validate_emptiness_do_two_truths_runtime_release_bundle_manifest_v0_1.py",
    ],
}

REQUIRED_ANY_TOKENS = {
    CI_LEDGER: [
        [
            "CI failure recorded; validator fix applied; green rerun not yet recorded",
            "CI failures recorded; validator fixes applied; green rerun not yet recorded",
            "CI green recorded for run",
            "CI green recorded; release archive ready for publication boundary review",
        ],
        [
            "claim_boundary: do_not_claim_ci_green_until_rerun_passes",
            "result: success",
        ],
    ],
}

GREEN_OBSERVATION_REQUIRED_TOKENS = [
    "### Observation 10: all-governance CI green",
    "run_id: 25960321365",
    "job_id: 76314405002",
    "result: success",
    "PASS: KuuOS all governance full checks completed",
    "ci_pass_not_theorem_truth",
    "ci_pass_not_execution_authority",
    "hash_chain_continuity_not_truth",
]

FORBIDDEN_POSITIVE_ASSERTIONS = [
    "ci_green_recorded: true",
    "final_archive_ready: true",
    "audit_chain_proves_theorem: true",
    "hash_chain_proves_truth: true",
    "runtime_audit_grants_execution_authority: true",
    "theorem_authority: true",
    "execution_authority: true",
    "clinical_authority: true",
    "public_visibility_changes_rights: true",
]

FORBIDDEN_POSITIVE_PROSE = [
    "CI success is theorem truth",
    "CI success grants execution authority",
    "hash chain proves truth",
    "audit chain proves theorem",
]


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        raise AssertionError(f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def rebuild_generated_audit_artifacts() -> int:
    if not AUDIT_CHAIN_BUILDER.is_file():
        print(
            "FAIL: missing audit chain builder: "
            f"{AUDIT_CHAIN_BUILDER.relative_to(ROOT)}"
        )
        return 1

    completed = subprocess.run(
        [sys.executable, str(AUDIT_CHAIN_BUILDER)],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        print(
            "FAIL: deterministic audit artifact rebuild failed: "
            f"{AUDIT_CHAIN_BUILDER.relative_to(ROOT)}"
        )
    return completed.returncode


def main() -> int:
    rebuild_code = rebuild_generated_audit_artifacts()
    if rebuild_code != 0:
        return rebuild_code

    errors: list[str] = []

    for file_path in REQUIRED_FILES:
        try:
            text = read(file_path)
        except AssertionError as exc:
            errors.append(str(exc))
            continue

        for token in REQUIRED_TOKENS.get(file_path, []):
            if token not in text:
                errors.append(f"missing token in {file_path}: {token}")

        for alternatives in REQUIRED_ANY_TOKENS.get(file_path, []):
            if not any(token in text for token in alternatives):
                errors.append(
                    f"missing one-of tokens in {file_path}: " + " OR ".join(alternatives)
                )

    ci_ledger_text = read(CI_LEDGER) if (ROOT / CI_LEDGER).exists() else ""
    if "CI green recorded for run" in ci_ledger_text or "### Observation 10: all-governance CI green" in ci_ledger_text:
        for token in GREEN_OBSERVATION_REQUIRED_TOKENS:
            if token not in ci_ledger_text:
                errors.append(f"missing green-observation token in {CI_LEDGER}: {token}")

    for file_path in PUBLIC_ARTIFACTS_TO_SCAN:
        try:
            text = read(file_path)
        except AssertionError as exc:
            errors.append(str(exc))
            continue

        for token in FORBIDDEN_POSITIVE_ASSERTIONS:
            if token in text:
                errors.append(f"forbidden positive authority assertion in {file_path}: {token}")

        for token in FORBIDDEN_POSITIVE_PROSE:
            if token in text:
                errors.append(f"forbidden positive prose claim in {file_path}: {token}")

    manifest_text = read(MANIFEST) if (ROOT / MANIFEST).exists() else ""
    for required in REQUIRED_FILES:
        if required not in manifest_text and required != MANIFEST:
            errors.append(f"manifest does not list required file: {required}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("PASS: KuuOS emptiness two truths runtime audit release bundle manifest v0.1 validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
