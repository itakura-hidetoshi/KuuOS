#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_repository_structure_map_v0_38 import DIRECTORY_ZONES, zone_paths

VERSION = "kuuos_repository_cleanup_proposals_v0_39"
DEPENDS_ON = "kuuos_repository_structure_map_v0_38"
CURRENT_ROOT = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class CleanupProposal:
    proposal_id: str
    title: str
    target_zone: str
    action_kind: str
    safety_level: str
    preconditions: tuple[str, ...]
    forbidden_effects: tuple[str, ...]


PROPOSALS: tuple[CleanupProposal, ...] = (
    CleanupProposal(
        "docs-status-frontier-summary",
        "Create a concise docs status frontier summary",
        "docs/",
        "add-index-document",
        "read-only-additive",
        ("source frontier is known", "no existing document is deleted", "links are descriptive not authoritative"),
        ("delete documentation", "rewrite history", "promote unmerged proposal"),
    ),
    CleanupProposal(
        "runtime-current-root-commentary",
        "Keep current root small and delegate detail to focused tests",
        "runtime/",
        "tighten-entrypoint",
        "read-only-runtime-check",
        ("focused tests already exist", "root order is explicit", "failure remains fail-closed"),
        ("perform repository mutation", "import proposal-only code", "skip existing root"),
    ),
    CleanupProposal(
        "manifest-small-metadata-rule",
        "Keep manifests short and metadata-only",
        "manifests/",
        "tighten-metadata-boundary",
        "metadata-only",
        ("manifest describes a merged or draft stage", "long prose has a docs target"),
        ("move runtime logic into manifest", "store large prose", "encode authority inheritance"),
    ),
    CleanupProposal(
        "ci-note-to-registry-candidate",
        "Convert check notes to registry snippets only when filters allow it",
        "ci/check_registry.d/",
        "deferred-registry-normalization",
        "deferred-safe",
        ("focused command is stable", "current root already runs the check", "registry syntax can be added without filter failure"),
        ("remove current-root coverage first", "invent check names", "hide missing registry support"),
    ),
    CleanupProposal(
        "legacy-entrypoint-labeling",
        "Label legacy entrypoints without removing compatibility wrappers",
        "scripts/",
        "additive-labeling",
        "compatibility-preserving",
        ("legacy workflow still references the script", "replacement root is documented"),
        ("delete wrapper", "break workflow", "rename without alias"),
    ),
)


def proposal_ids() -> tuple[str, ...]:
    return tuple(proposal.proposal_id for proposal in PROPOSALS)


def target_zones() -> tuple[str, ...]:
    return tuple(proposal.target_zone for proposal in PROPOSALS)


def proposal_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(proposal_ids()) != len(set(proposal_ids())):
        issues.append("duplicate_proposal_id")
    known_zones = set(zone_paths())
    for proposal in PROPOSALS:
        if proposal.target_zone not in known_zones:
            issues.append("unknown_target_zone:" + proposal.proposal_id)
        if not proposal.preconditions:
            issues.append("missing_precondition:" + proposal.proposal_id)
        if not proposal.forbidden_effects:
            issues.append("missing_forbidden_effect:" + proposal.proposal_id)
        if proposal.action_kind in {"move-file", "delete-file"}:
            issues.append("unsafe_action_kind:" + proposal.proposal_id)
    if "runtime/" not in target_zones():
        issues.append("runtime_proposal_missing")
    if "docs/" not in target_zones():
        issues.append("docs_proposal_missing")
    if "manifests/" not in target_zones():
        issues.append("manifest_proposal_missing")
    return tuple(issues)


def verify_cleanup_proposals() -> bool:
    return not proposal_issues()


def as_markdown() -> str:
    rows = ["| Proposal | Target | Action | Safety |", "|---|---|---|---|"]
    for proposal in PROPOSALS:
        rows.append(f"| {proposal.proposal_id} | `{proposal.target_zone}` | {proposal.action_kind} | {proposal.safety_level} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = proposal_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
