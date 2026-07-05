#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_next_candidate_v0_57 as previous

VERSION = "kuuos_receipt_v0_58"
DEPENDS_ON = previous.VERSION
READ_ONLY = True
METADATA_ONLY = True
DIRECT_EXECUTION = previous.DIRECT_EXECUTION
ACTOR = previous.ACTOR
RECEIPT = previous.CANDIDATE
PR_PATH_REQUIRED = True
GATE_REQUIRED = True


def failed_steps() -> tuple[str, ...]:
    failed: list[str] = []
    if not previous.verify_next_candidate():
        failed.append("previous")
    if not READ_ONLY:
        failed.append("read_only")
    if not METADATA_ONLY:
        failed.append("metadata_only")
    if not DIRECT_EXECUTION:
        failed.append("direct_execution")
    if ACTOR != "KuuOSAgent":
        failed.append("actor")
    if RECEIPT != "self_organization_receipt":
        failed.append("receipt")
    if not PR_PATH_REQUIRED:
        failed.append("pr_path")
    if not GATE_REQUIRED:
        failed.append("gate_path")
    return tuple(failed)


def verify_receipt() -> bool:
    return failed_steps() == ()


if __name__ == "__main__":
    if not verify_receipt():
        print("\n".join(failed_steps()))
        raise SystemExit(1)
    print(VERSION)
