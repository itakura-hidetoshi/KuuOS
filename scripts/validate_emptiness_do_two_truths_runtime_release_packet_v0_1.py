#!/usr/bin/env python3
"""Validate the KuuOS Emptiness / Dependent Origination / Two Truths runtime audit release packet v0.1.

Stdlib-only validator.
It checks that the public release packet, consolidated CI workflow, Makefile target,
and archive metadata preserve the non-authority boundary.

Boundary notes:
- Boundary documents are allowed to mention forbidden examples as forbidden examples.
- This validator therefore rejects positive authority-escalation assertions, not every
  occurrence of a phrase that appears inside a forbidden-wording list.
- The governance workflow may use either the legacy direct runner or the bounded
  sharded delegation chain. Sharding changes scheduling, not the command inventory
  or authority boundary.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RELEASE_PACKET = "specs/kuos_core_release_packet_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml"
GOVERNANCE_WORKFLOW = ".github/workflows/all_governance_validation.yml"
SHARDED_GOVERNANCE_WORKFLOW = ".github/workflows/all_governance_sharded_v0_2.yml"
SHARD_CI_RUNNER = "scripts/run_full_governance_shard_ci_v0_2.py"
SHARD_RUNNER = "scripts/run_all_governance_shard_v0_2.py"
FULL_RUNNER = "scripts/run_all_governance_full_checks_v0_1.py"

REQUIRED_FILES = [
    RELEASE_PACKET,
    "docs/EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_PUBLIC_RELEASE_v0_1.md",
    "docs/RELEASE_NOTES_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/PUBLICATION_CHECKLIST_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    "docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md",
    "docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md",
    GOVERNANCE_WORKFLOW,
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
        GOVERNANCE_WORKFLOW,
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
    GOVERNANCE_WORKFLOW: [
        "All Governance Validation",
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


def check_forbidden_assertions(
    file_path: str,
    text: str,
    errors: list[str],
) -> None:
    for token in FORBIDDEN_POSITIVE_ASSERTIONS:
        if token in text:
            errors.append(
                f"forbidden positive authority assertion in {file_path}: {token}"
            )


def validate_governance_workflow(errors: list[str]) -> None:
    """Accept the legacy direct runner or the bounded sharded delegation chain."""

    try:
        wrapper = read(GOVERNANCE_WORKFLOW)
    except AssertionError as exc:
        errors.append(str(exc))
        return

    legacy_tokens = [
        FULL_RUNNER,
        "python-version: '3.12'",
    ]
    if all(token in wrapper for token in legacy_tokens):
        return

    delegated_token = (
        "uses: ./.github/workflows/"
        + Path(SHARDED_GOVERNANCE_WORKFLOW).name
    )
    if delegated_token not in wrapper:
        errors.append(
            f"{GOVERNANCE_WORKFLOW} contains neither the legacy full runner "
            "nor the governed sharded workflow delegation"
        )
        return

    delegated_requirements = {
        SHARDED_GOVERNANCE_WORKFLOW: [
            "workflow_call:",
            "python-version: '3.12'",
            "max-parallel: 4",
            "scripts/run_full_governance_shard_ci_v0_2.py",
            "scripts/build_audit_summary.py",
        ],
        SHARD_CI_RUNNER: [
            "scripts/run_ci_check.py",
            "scripts/run_all_governance_shard_v0_2.py",
            "--check-id",
        ],
        SHARD_RUNNER: [
            "from run_all_governance_full_checks_v0_1 import COMMANDS",
            "sharding != authority expansion",
        ],
        FULL_RUNNER: [
            "COMMANDS: list[list[str]]",
            "PASS: KuuOS all governance full checks completed",
        ],
    }

    for file_path, tokens in delegated_requirements.items():
        try:
            text = read(file_path)
        except AssertionError as exc:
            errors.append(str(exc))
            continue

        for token in tokens:
            if token not in text:
                errors.append(
                    f"missing delegated-governance token in {file_path}: {token}"
                )

        check_forbidden_assertions(file_path, text, errors)


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

        check_forbidden_assertions(file_path, text, errors)

    validate_governance_workflow(errors)

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("PASS: KuuOS emptiness two truths runtime audit release packet v0.1 validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
