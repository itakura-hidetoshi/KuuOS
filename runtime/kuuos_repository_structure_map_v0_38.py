#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_repository_structure_map_v0_38"
PREVIOUS_INDEX = "kuuos_repository_self_organization_v0_37"
CURRENT_ROOT = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class DirectoryZone:
    path: str
    role: str
    accepts: tuple[str, ...]
    rejects: tuple[str, ...]


@dataclass(frozen=True)
class CleanupRule:
    name: str
    rule: str


DIRECTORY_ZONES: tuple[DirectoryZone, ...] = (
    DirectoryZone(
        "runtime/",
        "executable runtime and deterministic check surfaces",
        ("pure Python runtime modules", "current-root callable checks", "bounded verification helpers"),
        ("long-form design prose", "unmerged proposal claims", "manual-only notes"),
    ),
    DirectoryZone(
        "tests/",
        "unit and integration test modules",
        ("unittest modules", "focused regression tests", "source recomputation checks"),
        ("runtime implementation", "governance prose", "large generated artifacts"),
    ),
    DirectoryZone(
        "formal/",
        "Lean proof-facing surface",
        ("Lean declarations", "aggregate imports", "witness layers"),
        ("Python runtime code", "untyped governance prose", "unmerged proposal assumptions"),
    ),
    DirectoryZone(
        "docs/",
        "human-readable design and status documents",
        ("status notes", "roadmaps", "operator-facing structure maps"),
        ("runtime-only enforcement", "test-only fixtures"),
    ),
    DirectoryZone(
        "manifests/",
        "small machine-readable stage metadata",
        ("short JSON metadata", "stage dependencies", "read-only status flags"),
        ("long prose", "runtime logic", "branch-only plans"),
    ),
    DirectoryZone(
        "ci/check_registry.d/",
        "CI registry and check notes",
        ("registry snippets", "check notes", "focused command references"),
        ("runtime implementations", "large documentation"),
    ),
    DirectoryZone(
        "scripts/",
        "operator compatibility scripts",
        ("legacy entrypoints", "workflow compatibility wrappers"),
        ("new current-root logic unless explicitly bridged",),
    ),
)

CLEANUP_RULES: tuple[CleanupRule, ...] = (
    CleanupRule("no-delete-first", "Prefer index and alias before deletion or movement."),
    CleanupRule("root-first", "Every active line must be reachable from a declared root or explicitly marked legacy."),
    CleanupRule("proposal-separation", "Unmerged proposal material must not be promoted into current roots."),
    CleanupRule("series-separation", "Closed repository mutation and lifecycle completion remain separate lines."),
    CleanupRule("manifest-small", "Manifest files should remain small metadata, not long design documents."),
    CleanupRule("docs-human", "Human explanations belong in docs, while runtime checks belong in runtime and tests."),
)


def zone_paths() -> tuple[str, ...]:
    return tuple(zone.path for zone in DIRECTORY_ZONES)


def rule_names() -> tuple[str, ...]:
    return tuple(rule.name for rule in CLEANUP_RULES)


def structure_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(zone_paths()) != len(set(zone_paths())):
        issues.append("duplicate_zone_path")
    if len(rule_names()) != len(set(rule_names())):
        issues.append("duplicate_cleanup_rule")
    required = {"runtime/", "tests/", "formal/", "docs/", "manifests/", "ci/check_registry.d/"}
    missing = required.difference(zone_paths())
    if missing:
        issues.append("required_zone_missing:" + ",".join(sorted(missing)))
    runtime_zone = next((zone for zone in DIRECTORY_ZONES if zone.path == "runtime/"), None)
    if runtime_zone is None or "long-form design prose" not in runtime_zone.rejects:
        issues.append("runtime_boundary_missing")
    docs_zone = next((zone for zone in DIRECTORY_ZONES if zone.path == "docs/"), None)
    if docs_zone is None or "status notes" not in docs_zone.accepts:
        issues.append("docs_boundary_missing")
    if not any(rule.name == "no-delete-first" for rule in CLEANUP_RULES):
        issues.append("safe_cleanup_rule_missing")
    if not any(rule.name == "root-first" for rule in CLEANUP_RULES):
        issues.append("root_first_rule_missing")
    return tuple(issues)


def verify_repository_structure_map() -> bool:
    return not structure_issues()


def as_markdown() -> str:
    rows = ["| Path | Role |", "|---|---|"]
    for zone in DIRECTORY_ZONES:
        rows.append(f"| `{zone.path}` | {zone.role} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = structure_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
