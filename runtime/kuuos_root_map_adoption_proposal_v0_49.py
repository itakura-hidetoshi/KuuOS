#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_next_review_v0_48 as review

VERSION = "kuuos_root_map_adoption_proposal_v0_49"
DEPENDS_ON = review.VERSION
READ_ONLY = True
METADATA_ONLY = True
SELECTED_REVIEW_ID = "status-to-next-review"
SELECTED_NEXT_STEP = "derive_next_read_only_metadata_candidate"

PROPOSAL_BOUNDARIES: tuple[str, ...] = review.REQUIRED_BOUNDARIES + (
    "proposal_only",
    "no_automatic_adoption",
    "new_stage_required_for_adoption",
)


@dataclass(frozen=True)
class AdoptionProposal:
    proposal_id: str
    selected_review_id: str
    selected_next_step: str
    proposal_state: str
    boundaries: tuple[str, ...]


PROPOSAL = AdoptionProposal(
    "root-map-adoption-proposal-v0-49",
    SELECTED_REVIEW_ID,
    SELECTED_NEXT_STEP,
    "proposed_for_future_review",
    PROPOSAL_BOUNDARIES,
)


def selected_review_exists() -> bool:
    return PROPOSAL.selected_review_id in review.review_ids()


def selected_next_step_matches() -> bool:
    return PROPOSAL.selected_next_step in review.next_steps()


def proposal_boundaries() -> tuple[str, ...]:
    return PROPOSAL.boundaries


def proposal_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not review.verify_next_review():
        issues.append("upstream_next_review_invalid")
    if not selected_review_exists():
        issues.append("selected_review_missing")
    if not selected_next_step_matches():
        issues.append("selected_next_step_missing")
    if PROPOSAL.proposal_state != "proposed_for_future_review":
        issues.append("unexpected_proposal_state")
    required = set(review.REQUIRED_BOUNDARIES).union(
        {"proposal_only", "no_automatic_adoption", "new_stage_required_for_adoption"}
    )
    missing = required.difference(PROPOSAL.boundaries)
    if missing:
        issues.append("missing_boundary:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_adoption_proposal() -> bool:
    return not proposal_issues()


def as_markdown() -> str:
    return "\n".join(
        (
            "| Proposal | Selected review | Selected next step | State | Boundaries |",
            "|---|---|---|---|---|",
            f"| {PROPOSAL.proposal_id} | {PROPOSAL.selected_review_id} | "
            f"`{PROPOSAL.selected_next_step}` | {PROPOSAL.proposal_state} | "
            f"{', '.join(PROPOSAL.boundaries)} |",
        )
    )


if __name__ == "__main__":
    problems = proposal_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
