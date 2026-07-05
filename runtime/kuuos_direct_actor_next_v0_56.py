#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_direct_execution_actor_v0_55 as previous

VERSION = "kuuos_direct_actor_next_v0_56"
DEPENDS_ON = previous.VERSION
READ_ONLY = True
METADATA_ONLY = True
DIRECT_EXECUTION = previous.DIRECT_EXECUTION
ACTOR = previous.ACTOR
NEXT_LAYER = "self_organization_step"
PR_PATH_REQUIRED = True
GATE_REQUIRED = True

STEPS: tuple[str, ...] = (
    "actor_verified",
    "frontier_observed",
    "next_layer_selected",
    "pr_path_required",
    "gate_required",
)


def failed_steps() -> tuple[str, ...]:
    failed: list[str] = []
    if not previous.verify_direct_execution_actor():
        failed.append("actor_verified")
    if not READ_ONLY:
        failed.append("read_only")
    if not METADATA_ONLY:
        failed.append("metadata_only")
    if not DIRECT_EXECUTION:
        failed.append("direct_execution")
    if ACTOR != "KuuOSAgent":
        failed.append("actor")
    if not PR_PATH_REQUIRED:
        failed.append("pr_path")
    if not GATE_REQUIRED:
        failed.append("gate_path")
    return tuple(failed)


def verify_next_step() -> bool:
    return failed_steps() == ()


if __name__ == "__main__":
    if not verify_next_step():
        print("\n".join(failed_steps()))
        raise SystemExit(1)
    print(VERSION)
