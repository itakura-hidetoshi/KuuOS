#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout

VERSION = "kuuos_agent_self_organization_v0_55"
DEPENDS_ON = closeout.VERSION
READ_ONLY = True
METADATA_ONLY = True
AGENT_MODE = "bounded_self_organization"
DIRECT_MUTATION = False
AUTONOMOUS_EXECUTION = False

REQUIRED_AGENT_STEPS: tuple[str, ...] = (
    "observe_frontier",
    "preserve_boundaries",
    "select_bounded_next_layer",
    "require_draft_pr",
    "require_gate_before_merge",
)


@dataclass(frozen=True)
class AgentStep:
    step_id: str
    passed: bool
    note: str


AGENT_STEPS: tuple[AgentStep, ...] = (
    AgentStep(
        "observe_frontier",
        closeout.verify_deferral_closeout(),
        "agent observes the verified v0.54 closeout frontier",
    ),
    AgentStep(
        "preserve_boundaries",
        closeout.READ_ONLY and closeout.METADATA_ONLY,
        "agent preserves read-only and metadata-only boundaries",
    ),
    AgentStep(
        "select_bounded_next_layer",
        True,
        "agent selects only one bounded successor layer at a time",
    ),
    AgentStep(
        "require_draft_pr",
        True,
        "agent output must be proposed through a draft pull request",
    ),
    AgentStep(
        "require_gate_before_merge",
        True,
        "agent output requires governance gate success before merge",
    ),
)


def agent_step_ids() -> tuple[str, ...]:
    return tuple(step.step_id for step in AGENT_STEPS)


def failed_agent_steps() -> tuple[str, ...]:
    return tuple(step.step_id for step in AGENT_STEPS if not step.passed)


def agent_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if DIRECT_MUTATION:
        issues.append("direct_mutation_enabled")
    if AUTONOMOUS_EXECUTION:
        issues.append("autonomous_execution_enabled")
    if AGENT_MODE != "bounded_self_organization":
        issues.append("unexpected_agent_mode")
    if len(agent_step_ids()) != len(set(agent_step_ids())):
        issues.append("duplicate_agent_step")
    missing = set(REQUIRED_AGENT_STEPS).difference(agent_step_ids())
    if missing:
        issues.append("missing_agent_step:" + ",".join(sorted(missing)))
    for step in AGENT_STEPS:
        if not step.note:
            issues.append("missing_note:" + step.step_id)
    for failed in failed_agent_steps():
        issues.append("failed_agent_step:" + failed)
    return tuple(issues)


def verify_agent_self_organization() -> bool:
    return not agent_issues()


def as_markdown() -> str:
    rows = ["| Agent step | Passed | Note |", "|---|---|---|"]
    for step in AGENT_STEPS:
        rows.append(f"| {step.step_id} | {step.passed} | {step.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = agent_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
