#!/usr/bin/env python3
"""Validate the KuuOS Emptiness / Dependent Origination / Two Truths runtime audit release packet v0.1.

Stdlib-only validator.
It checks that the public release packet, CI workflow, Makefile target, and
archive metadata preserve the non-authority boundary.

Boundary notes:
- Boundary documents are allowed to mention forbidden examples as forbidden examples.
- This validator therefore rejects positive authority-escalation assertions, not every
  occurrence of a phrase that appears inside a forbidden-wording list.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RELEASE_PACKET = "specs/kuos_core_release_packet_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml"

REQUIRED_FILES = [
    RELEASE_PACKET,
    "docs/EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_PUBLIC_RELEASE_v0_1.md",
    "docs/RELEASE_NOTES_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/PUBLICATION_CHECKLIST_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md",
    "docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md",
    ".github/workflows/emptiness_two_truths_runtime_audit_validation.yml",
    "Makefile",
]

REQUIRED_TOKENS = {
    RELEASE_PACKET: [
        "implementation_level_runtime_audit_chain",
        "theorem_authority: false",
        "execution_authority: false",
        "clinical_authority: false",
        "public_visibility_changes_rights: false",
        "make emptiness-two-truths-runtime-audit-checks",
        "make all-governance-checks",
        "audit_chain_structural_consistency_not_theorem_authority",
        "hash_chain_continuity_not_truth",
        "runtime_audit_not_execution_authority",
        "claim_direct_K_observation",
        "claim_K_as_object",
        "claim_execution_authority",
        "zenodo_metadata_present",
        ".github/workflows/emptiness_two_truths_runtime_audit_validation.yml",
        "docs/ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    ],
    "docs/EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_PUBLIC_RELEASE_v0_1.md": [
        "implementation-level governance chain",
        "audit event JSONL",
        "hash-chain JSONL",
        "does **not** claim",
        "final mathematical proof authority",
        "direct observation of `K`",
        "Public visibility is not license permission",
    ],
    "docs/RELEASE_NOTES_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md": [
        "implementation-level audit chain",
        "K",
        "two_truths_non_collapse_barrier",
        "audit hash-chain",
        "does not claim final theorem authority",
    ],
    "docs/PUBLICATION_CHECKLIST_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md": [
        "make all-governance-checks",
        "final theorem proof",
        "direct observation of K",
        "clinical decision authority",
        "execution authority",
        "Hash Chain",
    ],
    "docs/ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md": [
        "Recommended title",
        "Recommended upload type",
        "Recommended description",
        "Required boundary statement",
        "Runtime auditability and hash-chain continuity are structural consistency signals",
    ],
    "docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md": [
        "make emptiness-two-truths-runtime-audit-checks",
        "scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py",
        "scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py",
        "audit_chain_structural_consistency_not_theorem_authority",
    ],
    "docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md": [
        "Emptiness / Dependent Origination / Two Truths Runtime Audit Chain",
        "docs/EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_PUBLIC_RELEASE_v0_1.md",
        "scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py",
        "runtime_audit_not_execution_authority",
    ],
    ".github/workflows/emptiness_two_truths_runtime_audit_validation.yml": [
        "Emptiness Two Truths Runtime Audit Validation",
        "make emptiness-two-truths-runtime-audit-checks",
        "python-version: '3.12'",
    ],
    "Makefile": [
        "emptiness-two-truths-runtime-audit-checks:",
        "python3 scripts/export_emptiness_do_two_truths_runtime_audit_v0_1.py",
        "python3 scripts/build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py",
        "python3 scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py",
        "python3 scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py",
    ],
}

FORBIDDEN_POSITIVE_ASSERTIONS = [
    "audit_chain_proves_theorem: true",
    "hash_chain_proves_truth: true",
    "runtime_audit_grants_execution_authority: true",
    "theorem_authority: true",
    "execution_authority: true",
    "clinical_authority: true",
    "public_visibility_changes_rights: true",
    "K_direct_observation_allowed: true",
    "K_is_object_allowed: true",
    "string_or_brane_identified_with_K_allowed: true",
    "gap_reifies_ultimate_truth_allowed: true",
    "observable_directly_measures_K_allowed: true",
    "paramartha_samvrti_collapse_allowed: true",
    "final_archive_ready: true",
    "ci_green_recorded: true",
]


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        raise AssertionError(f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def main() -> int:
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

        for token in FORBIDDEN_POSITIVE_ASSERTIONS:
            if token in text:
                errors.append(f"forbidden positive authority assertion in {file_path}: {token}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("PASS: KuuOS emptiness two truths runtime audit release packet v0.1 validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
