#!/usr/bin/env python3
"""Validate KuuOS MemoryOS GitHub external memory v0.1 surfaces."""

from __future__ import annotations

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "doc": ROOT / "docs" / "MEMORYOS_GITHUB_EXTERNAL_MEMORY_v0_1.md",
    "manifest": ROOT / "specs" / "memoryos_github_external_memory_manifest_v0_1.yaml",
    "example": ROOT / "examples" / "memoryos_github_external_memory_minimal.py",
    "makefile": ROOT / "Makefile",
    "index": ROOT / "docs" / "KUOS_CORE_GOVERNANCE_INDEX_v0_1.md",
    "runbook": ROOT / "docs" / "ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md",
    "runner": ROOT / "scripts" / "run_all_governance_full_checks_v0_1.py",
}

REQUIRED = {
    "doc": [
        "GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority",
        "MemoryOS_no_silent_overwrite",
        "MemoryOS_lineage_preserved",
        "MemoryOS_conflict_visible",
        "GitHub_branch_HEAD_is_not_stable_memory",
        "semantic_digest_is_not_source_evidence",
        "make memoryos-github-external-memory-checks",
    ],
    "manifest": [
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
    ],
    "example": [
        "GitHubExternalMemoryRecord",
        "external_pointer_only",
        "validate_record",
        "compile_context_candidate",
        "may_execute",
        "may_claim_truth",
        "may_update_world_directly",
    ],
    "makefile": [
        "memoryos-github-external-memory-checks",
        "python3 scripts/validate_memoryos_github_external_memory_v0_1.py",
    ],
    "index": [
        "MemoryOS GitHub external memory",
        "docs/MEMORYOS_GITHUB_EXTERNAL_MEMORY_v0_1.md",
        "scripts/validate_memoryos_github_external_memory_v0_1.py",
    ],
    "runbook": [
        "MemoryOS GitHub External Memory Command",
        "make memoryos-github-external-memory-checks",
    ],
    "runner": [
        "scripts/validate_memoryos_github_external_memory_v0_1.py",
        "scripts/validate_mass_gap_two_truths_engine_bridge_v0_1.py",
    ],
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for label, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        content = text(path)
        for token in REQUIRED[label]:
            if token not in content:
                errors.append(f"missing token in {path.relative_to(ROOT)}: {token}")

    try:
        runpy.run_path(str(FILES["example"]), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (0, None):
            errors.append(f"example exited with failure: {exc.code}")
    except Exception as exc:
        errors.append(f"example raised exception: {exc!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
