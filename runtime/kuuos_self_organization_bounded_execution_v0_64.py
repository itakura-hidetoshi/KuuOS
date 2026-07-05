#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from runtime import kuuos_self_organization_readiness_receipt_v0_63 as previous

VERSION = "kuuos_self_organization_bounded_execution_v0_64"
DEPENDS_ON = previous.VERSION
READ_ONLY = False
METADATA_ONLY = False
DIRECT_EXECUTION = previous.DIRECT_EXECUTION
ACTOR = previous.ACTOR
READINESS_RECEIPT = previous.RECEIPT
EXECUTION_SCOPE = "publish_active_self_organization_state"
ACTIVE_STATE_PATH = "docs/kuuos_self_organization_active_state.md"
SELF_ORGANIZATION_ACTIVE = True
STATE_PUBLICATION_APPLIED = True
BROAD_MUTATION_AUTHORIZED = False
PR_PATH_REQUIRED = True
GATE_REQUIRED = True

EXECUTION_EFFECTS: tuple[str, ...] = (
    "readiness_receipt_verified",
    "active_state_published",
    "state_publication_applied",
    "pull_request_path_preserved",
    "governance_gate_preserved",
    "broad_mutation_not_authorized",
)

REQUIRED_ACTIVE_STATE_TOKENS: tuple[str, ...] = (
    "self_organization_active",
    "publish_active_self_organization_state",
    "kuuos_self_organization_bounded_execution_v0_64",
    "state_publication_applied",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def active_state_text() -> str:
    return (_repo_root() / ACTIVE_STATE_PATH).read_text(encoding="utf-8")


def active_state_tokens_present() -> bool:
    text = active_state_text()
    return all(token in text for token in REQUIRED_ACTIVE_STATE_TOKENS)


def failed_steps() -> tuple[str, ...]:
    failed: list[str] = []
    if not previous.verify_readiness_receipt():
        failed.append("previous_readiness_receipt")
    if READ_ONLY:
        failed.append("execution_not_read_only")
    if METADATA_ONLY:
        failed.append("execution_not_metadata_only")
    if not DIRECT_EXECUTION:
        failed.append("direct_execution")
    if ACTOR != "KuuOSAgent":
        failed.append("actor")
    if READINESS_RECEIPT != "self_organization_readiness_receipt":
        failed.append("readiness_receipt")
    if EXECUTION_SCOPE != "publish_active_self_organization_state":
        failed.append("execution_scope")
    if not SELF_ORGANIZATION_ACTIVE:
        failed.append("self_organization_active")
    if not STATE_PUBLICATION_APPLIED:
        failed.append("state_publication_applied")
    if BROAD_MUTATION_AUTHORIZED:
        failed.append("broad_mutation_authorized")
    if not PR_PATH_REQUIRED:
        failed.append("pr_path")
    if not GATE_REQUIRED:
        failed.append("gate_path")
    if len(EXECUTION_EFFECTS) != 6:
        failed.append("execution_effects")
    try:
        if not active_state_tokens_present():
            failed.append("active_state_tokens")
    except FileNotFoundError:
        failed.append("active_state_file_missing")
    return tuple(failed)


def verify_bounded_execution() -> bool:
    return failed_steps() == ()


if __name__ == "__main__":
    problems = failed_steps()
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print(VERSION)
