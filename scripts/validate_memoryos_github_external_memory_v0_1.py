#!/usr/bin/env python3
"""Validate KuuOS MemoryOS GitHub external memory v0.1 surfaces.

Stdlib-only validator. It checks that the documentation, manifest, and example
preserve MemoryOS non-authority, append-only, lineage, and conflict visibility
boundaries.
"""

from __future__ import annotations

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "MEMORYOS_GITHUB_EXTERNAL_MEMORY_v0_1.md"
MANIFEST = ROOT / "specs" / "memoryos_github_external_memory_manifest_v0_1.yaml"
EXAMPLE = ROOT / "examples" / "memoryos_github_external_memory_minimal.py"
MAKEFILE = ROOT / "Makefile"
WORKFLOW = ROOT / ".github" / "workflows" / "memoryos_github_external_memory_validation.yml"
INDEX = ROOT / "docs" / "KUOS_CORE_GOVERNANCE_INDEX_v0_1.md"
RUNBOOK = ROOT / "docs" / "ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md"

REQUIRED_FILES = [DOC, MANIFEST, EXAMPLE, MAKEFILE, WORKFLOW, INDEX, RUNBOOK]

REQUIRED_TOKENS = {
    DOC: [
        "GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority",
        "MemoryOS_no_silent_overwrite",
        "MemoryOS_lineage_preserved",
        "MemoryOS_conflict_visible",
        "GitHub_branch_HEAD_is_not_stable_memory",
        "semantic_digest_is_not_source_evidence",
        "no_execution_authority",
        "no_clinical_authority",
        "no_teni_authority",
        "no_world_update_authority",
        "make memoryos-github-external-memory-checks",
    ],
    MANIFEST: [
        "memoryos_github_external_memory_manifest_v0_1",
        "pointer_memory",
        "evidence_memory",
        "semantic_digest_memory",
        "repair_lineage_memory",
        "conflict_visibility_memory",
        "external_pointer_only",
        "no_truth_authority: true",
        "no_proof_authority: true",
        "GitHub_commit_is_evidence_not_truth",
        "PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates",
    ],
    EXAMPLE: [
        "GitHubExternalMemoryRecord",
        "external_pointer_only",
        "validate_record",
        "compile_context_candidate",
        "may_execute",
        "may_claim_truth",
        "may_update_world_directly",
    ],
    MAKEFILE: [
        "memoryos-github-external-memory-checks",
        "python3 scripts/validate_memoryos_github_external_memory_v0_1.py",
    ],
    WORKFLOW: [
        "MemoryOS GitHub External Memory Validation",
        "make memoryos-github-external-memory-checks",
    ],
    INDEX: [
        "MemoryOS GitHub external memory",
        "docs/MEMORYOS_GITHUB_EXTERNAL_MEMORY_v0_1.md",
        "scripts/validate_memoryos_github_external_memory_v0_1.py",
        "GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority",
    ],
    RUNBOOK: [
        "MemoryOS GitHub External Memory Command",
        "make memoryos-github-external-memory-checks",
        "PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates",
    ],
}

FORBIDDEN_AUTHORITY_PATTERNS = [
    "GitHub is memory authority",
    "GitHub is truth authority",
    "CI pass grants truth",
    "branch HEAD is stable memory",
    "semantic digest is source evidence",
    "release grants proof completion",
    "MemoryOS overwrite authority",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    for path, tokens in REQUIRED_TOKENS.items():
        text = read(path)
        for token in tokens:
            if token not in text:
                errors.append(f"missing token in {path.relative_to(ROOT)}: {token}")
        for pattern in FORBIDDEN_AUTHORITY_PATTERNS:
            if pattern in text:
                errors.append(f"forbidden authority pattern in {path.relative_to(ROOT)}: {pattern}")

    # Execute the example in-process to ensure the public minimal model is live.
    try:
        runpy.run_path(str(EXAMPLE), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (0, None):
            errors.append(f"example exited with failure: {exc.code}")
    except Exception as exc:  # pragma: no cover - intentional CLI guard
        errors.append(f"example raised exception: {exc!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
