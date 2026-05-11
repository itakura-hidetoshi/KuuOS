#!/usr/bin/env python3
"""Validate KuuOS GPT GitHub integration surface v0.1.

Stdlib-only validator.
It checks that the integration docs, manifest, issue template, PR hook,
and formal bridge preserve the required non-authority fixed points.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md",
    "docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md",
    "specs/gpt_github_integration_manifest_v0_1.yaml",
    ".github/ISSUE_TEMPLATE/kuos_gpt_github_integration_check.md",
    ".github/pull_request_template.md",
]

REQUIRED_TOKENS = {
    "docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md": [
        "AI raw output is candidate, not authority",
        "PASS",
        "HOLD",
        "REPAIR",
        "REJECT",
        "QUARANTINE",
        "GPT_summary_not_authority",
        "ci_pass_not_execution_authority",
        "docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md",
    ],
    "docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md": [
        "itakura-hidetoshi/4d-mass-gap",
        "GPT_summary_not_proof_authority",
        "ci_pass_not_theorem_truth",
        "review_gate_required_for_public_final_claim",
        "DOCUMENTED",
        "FORMAL_STUBBED",
        "CHECKER_VALIDATED",
        "CI_REPLAYED",
        "REVIEW_GATED",
    ],
    "specs/gpt_github_integration_manifest_v0_1.yaml": [
        "docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md",
        "docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md",
        "python3 scripts/validate_gpt_github_integration_v0_1.py",
        "gpt-github-integration-checks",
        "itakura-hidetoshi/4d-mass-gap",
        "GPT_summary_not_authority",
        "ci_pass_not_execution_authority",
    ],
    ".github/ISSUE_TEMPLATE/kuos_gpt_github_integration_check.md": [
        "KuuOS GPT GitHub Integration Check",
        "GPT_reading_not_authority",
        "ci_pass_not_execution_authority",
        "PASS / HOLD / REPAIR / REJECT / QUARANTINE",
        "make gpt-github-integration-checks",
    ],
    ".github/pull_request_template.md": [
        "GPT GitHub Review Hook",
        "docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md",
        "PASS / HOLD / REPAIR / REJECT / QUARANTINE",
    ],
}

FORBIDDEN_TOKENS = [
    "CI pass proves truth",
    "validation pass grants execution authority",
    "GPT review is authority",
    "Lean stub proves theorem",
    "clinical authority exists",
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

        for token in FORBIDDEN_TOKENS:
            if token in text:
                errors.append(f"forbidden overclaim token in {file_path}: {token}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("PASS: KuuOS GPT GitHub integration surface v0.1 validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
