#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

VERSION = "kuuos_repository_self_organization_v0_37"
CURRENT_FRONTIER = "lifecycle_completion_v0_36"
CURRENT_RUNTIME_ROOT = "runtime/kuuos_current_check.py"
CURRENT_LEAN_ROOT = "formal/KuuOSFormal.lean"
CLOSED_MUTATION_ROOT = "runtime/kuuos_v124_check.py"
LEGACY_RUNTIME_ROOT = "scripts/run_kuuos_runtime_full_check_v0_55.py"
SELF_ORGANIZATION_TEST = "tests.test_kuuos_repo_index_v0_37"
LIFECYCLE_COMPLETION_TEST = "tests.test_kuuos_lifecycle_completion_v0_36"


@dataclass(frozen=True)
class KuuOSLine:
    name: str
    stage_range: str
    status: str
    root: str
    successor_policy: str
    notes: str


@dataclass(frozen=True)
class KuuOSRoot:
    path: str
    role: str
    includes: tuple[str, ...]
    excludes: tuple[str, ...]


@dataclass(frozen=True)
class KuuOSBoundary:
    name: str
    rule: str


INTEGRATED_LINES: tuple[KuuOSLine, ...] = (
    KuuOSLine(
        "core-governance",
        "v0.1",
        "frozen-boundary",
        "core governance workflows and registry entries",
        "tighten-only",
        "Base governance surface; not a moving feature line.",
    ),
    KuuOSLine(
        "world-math-sidecar",
        "v0.27-v0.59",
        "integrated-continuing-verification",
        CURRENT_LEAN_ROOT,
        "additive-or-tighten-only",
        "Lean-facing mathematical sidecar; CI success does not imply external theorem acceptance.",
    ),
    KuuOSLine(
        "gauge-and-module-application",
        "v0.60-v0.76",
        "integrated-continuing-verification",
        "runtime and tests for gauge/module/memory application layers",
        "additive-or-tighten-only",
        "Connection, module, MemoryOS application, review, and rollback surfaces.",
    ),
    KuuOSLine(
        "self-organizing-improvement",
        "v0.78",
        "integrated-continuing-verification",
        "runtime self-improvement checks",
        "additive-only",
        "v0.77 proposal material is not promoted by this line.",
    ),
    KuuOSLine(
        "repository-self-evolution",
        "v0.79-v1.24",
        "closed-series",
        CLOSED_MUTATION_ROOT,
        "no-automatic-successor",
        "Repository mutation research line is closed at v1.24.",
    ),
    KuuOSLine(
        "apoptosis-lifecycle-governance",
        "v0.1-v0.36",
        "terminal-completion-integrated",
        LIFECYCLE_COMPLETION_TEST,
        "no-following-lifecycle-route",
        "Independent lifecycle line; not repository mutation roadmap v1.25.",
    ),
    KuuOSLine(
        "repository-self-organization",
        "v0.37",
        "organization-index-frontier",
        SELF_ORGANIZATION_TEST,
        "index-only-unless-explicitly-extended",
        "Machine-readable repository map and current-root organization check.",
    ),
)

RUNTIME_ROOTS: tuple[KuuOSRoot, ...] = (
    KuuOSRoot(
        CURRENT_RUNTIME_ROOT,
        "current-root",
        (CLOSED_MUTATION_ROOT, LIFECYCLE_COMPLETION_TEST, SELF_ORGANIZATION_TEST),
        ("unmerged proposals", "closed branches", "v0.77 proposal material"),
    ),
    KuuOSRoot(
        CLOSED_MUTATION_ROOT,
        "closed-mutation-root",
        ("repository mutation v1.03-v1.24 cumulative runtime surface",),
        ("lifecycle governance", "new mutation successor authority"),
    ),
    KuuOSRoot(
        LEGACY_RUNTIME_ROOT,
        "legacy-compatibility-root",
        ("v1.02 compatibility surface",),
        ("current frontier", "closed mutation root", "lifecycle completion"),
    ),
    KuuOSRoot(
        CURRENT_LEAN_ROOT,
        "lean-aggregate-root",
        ("formal/KUOS/WORLD aggregate imports",),
        ("runtime-only proposals", "unmerged branches"),
    ),
)

BOUNDARIES: tuple[KuuOSBoundary, ...] = (
    KuuOSBoundary("candidate-authority", "candidate != authority"),
    KuuOSBoundary("validation-truth", "validation != truth"),
    KuuOSBoundary("ci-acceptance", "CI pass != external theorem acceptance"),
    KuuOSBoundary("memory-sovereignty", "memory != belief sovereignty"),
    KuuOSBoundary("selection-execution", "selection != execution"),
    KuuOSBoundary("receipt-authority", "receipt != successor authority"),
    KuuOSBoundary("roadmap-successor", "roadmap completion != successor mutation authority"),
    KuuOSBoundary("lifecycle-mutation", "apoptosis lifecycle governance != repository mutation roadmap v1.25"),
    KuuOSBoundary("completion-successor", "lifecycle completion != successor route"),
    KuuOSBoundary("terminal-inheritance", "terminal completion != future authority inheritance"),
)


def _duplicates(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return tuple(sorted(duplicates))


def line_names() -> tuple[str, ...]:
    return tuple(line.name for line in INTEGRATED_LINES)


def root_paths() -> tuple[str, ...]:
    return tuple(root.path for root in RUNTIME_ROOTS)


def boundary_names() -> tuple[str, ...]:
    return tuple(boundary.name for boundary in BOUNDARIES)


def current_root() -> KuuOSRoot:
    candidates = [root for root in RUNTIME_ROOTS if root.role == "current-root"]
    if len(candidates) != 1:
        raise ValueError("current_root_not_unique")
    return candidates[0]


def organization_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if _duplicates(line_names()):
        issues.append("duplicate_line_names")
    if _duplicates(root_paths()):
        issues.append("duplicate_root_paths")
    if _duplicates(boundary_names()):
        issues.append("duplicate_boundary_names")
    if CURRENT_FRONTIER not in " ".join(line.stage_range + " " + line.name + " " + line.root for line in INTEGRATED_LINES):
        issues.append("current_frontier_not_indexed")
    root = current_root()
    if CLOSED_MUTATION_ROOT not in root.includes:
        issues.append("current_root_missing_closed_mutation_root")
    if LIFECYCLE_COMPLETION_TEST not in root.includes:
        issues.append("current_root_missing_lifecycle_completion")
    if SELF_ORGANIZATION_TEST not in root.includes:
        issues.append("current_root_missing_self_organization")
    lifecycle = [line for line in INTEGRATED_LINES if line.name == "apoptosis-lifecycle-governance"]
    if len(lifecycle) != 1 or lifecycle[0].successor_policy != "no-following-lifecycle-route":
        issues.append("lifecycle_successor_policy_invalid")
    mutation = [line for line in INTEGRATED_LINES if line.name == "repository-self-evolution"]
    if len(mutation) != 1 or mutation[0].status != "closed-series":
        issues.append("mutation_series_not_closed")
    if not any(boundary.rule == "apoptosis lifecycle governance != repository mutation roadmap v1.25" for boundary in BOUNDARIES):
        issues.append("lifecycle_mutation_boundary_missing")
    return tuple(issues)


def as_markdown() -> str:
    rows = ["| Line | Stage range | Status | Root | Successor policy |", "|---|---|---|---|---|"]
    for line in INTEGRATED_LINES:
        rows.append(f"| {line.name} | {line.stage_range} | {line.status} | `{line.root}` | {line.successor_policy} |")
    return "\n".join(rows)


def verify_repository_self_organization() -> bool:
    return not organization_issues()


if __name__ == "__main__":
    problems = organization_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
