#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_direct_execution_actor_v0_55 as direct

VERSION = "kuuos_bounded_steering_v0_55"
DEPENDS_ON = direct.VERSION
READ_ONLY = direct.READ_ONLY
METADATA_ONLY = direct.METADATA_ONLY
DIRECT_EXECUTION = direct.DIRECT_EXECUTION
ACTOR = direct.ACTOR
PR_PATH_REQUIRED = direct.PR_PATH_REQUIRED
GATE_REQUIRED = direct.GATE_REQUIRED

REQUIRED_STEPS: tuple[str, ...] = (
    "direct_execution",
    "actor",
    "pr_path",
    "gate_path",
)


def step_ids() -> tuple[str, ...]:
    return REQUIRED_STEPS


def failed_steps() -> tuple[str, ...]:
    return () if direct.verify_direct_execution_actor() else ("direct_actor_path",)


def steering_issues() -> tuple[str, ...]:
    return failed_steps()


def verify_bounded_steering() -> bool:
    return direct.verify_direct_execution_actor()


def as_markdown() -> str:
    return "| Step | Passed |\n|---|---|\n| direct_execution_actor | True |"


if __name__ == "__main__":
    if not verify_bounded_steering():
        raise SystemExit(1)
    print(as_markdown())
