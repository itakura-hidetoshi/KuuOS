#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_manifest_index_v0_42"
DEPENDS_ON = "kuuos_current_root_sequence_v0_41"
CURRENT_ROOT = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class ManifestEntry:
    stage: str
    path: str
    depends_on: str
    role: str
    max_lines: int


MANIFEST_ENTRIES: tuple[ManifestEntry, ...] = (
    ManifestEntry(
        "repo-index-v0-37",
        "manifests/kuuos_repo_index_v0_37.json",
        "lifecycle_completion_v0_36",
        "repository line and root index metadata",
        1,
    ),
    ManifestEntry(
        "repository-structure-map-v0-38",
        "manifests/kuuos_repository_structure_map_v0_38.json",
        "repository_self_organization_v0_37",
        "directory zone metadata",
        1,
    ),
    ManifestEntry(
        "repository-cleanup-proposals-v0-39",
        "manifests/kuuos_repository_cleanup_proposals_v0_39.json",
        "repository_structure_map_v0_38",
        "cleanup proposal metadata",
        1,
    ),
    ManifestEntry(
        "repository-frontier-summary-v0-40",
        "manifests/kuuos_repository_frontier_summary_v0_40.json",
        "repository_cleanup_proposals_v0_39",
        "frontier summary metadata",
        1,
    ),
    ManifestEntry(
        "current-root-sequence-v0-41",
        "manifests/kuuos_current_root_sequence_v0_41.json",
        "repository_frontier_summary_v0_40",
        "current root sequence metadata",
        1,
    ),
    ManifestEntry(
        "manifest-index-v0-42",
        "manifests/kuuos_manifest_index_v0_42.json",
        "current_root_sequence_v0_41",
        "manifest index metadata",
        1,
    ),
)


def manifest_paths() -> tuple[str, ...]:
    return tuple(entry.path for entry in MANIFEST_ENTRIES)


def manifest_stages() -> tuple[str, ...]:
    return tuple(entry.stage for entry in MANIFEST_ENTRIES)


def manifest_index_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(manifest_paths()) != len(set(manifest_paths())):
        issues.append("duplicate_manifest_path")
    if len(manifest_stages()) != len(set(manifest_stages())):
        issues.append("duplicate_manifest_stage")
    for entry in MANIFEST_ENTRIES:
        if not entry.path.startswith("manifests/"):
            issues.append("manifest_path_outside_manifest_dir:" + entry.stage)
        if not entry.path.endswith(".json"):
            issues.append("manifest_path_not_json:" + entry.stage)
        if entry.max_lines > 3:
            issues.append("manifest_too_large_for_index_rule:" + entry.stage)
        if not entry.depends_on:
            issues.append("missing_dependency:" + entry.stage)
        if not entry.role:
            issues.append("missing_manifest_role:" + entry.stage)
    required = {
        "repo-index-v0-37",
        "repository-structure-map-v0-38",
        "repository-cleanup-proposals-v0-39",
        "repository-frontier-summary-v0-40",
        "current-root-sequence-v0-41",
        "manifest-index-v0-42",
    }
    missing = required.difference(manifest_stages())
    if missing:
        issues.append("missing_manifest_stage:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_manifest_index() -> bool:
    return not manifest_index_issues()


def as_markdown() -> str:
    rows = ["| Stage | Manifest | Depends on |", "|---|---|---|"]
    for entry in MANIFEST_ENTRIES:
        rows.append(f"| {entry.stage} | `{entry.path}` | {entry.depends_on} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = manifest_index_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
