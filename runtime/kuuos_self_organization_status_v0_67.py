#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_66 as current_root
from runtime import kuuos_self_organization_bounded_execution_v0_64 as active_state

VERSION = "kuuos_self_organization_status_v0_67"
DEPENDS_ON = current_root.VERSION
ACTIVE_STATE_FRONTIER = active_state.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
STATUS_COMMAND = "kuuos_self_organization_status"
STATUS_SCHEMA_VERSION = "v0.67"

REQUIRED_STATUS_KEYS: tuple[str, ...] = (
    "status_schema_version",
    "status_command",
    "active",
    "active_state_path",
    "active_state_frontier",
    "current_root_sequence",
    "bounded_execution_verified",
    "current_root_sequence_verified",
    "public_status_checked",
    "authority_boundary",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _readme_text() -> str:
    return (_repo_root() / "README.md").read_text(encoding="utf-8")


def public_status_checked() -> bool:
    text = _readme_text()
    required_tokens = (
        "KuuOS README Public Status v0.66",
        "kuuos_current_root_sequence_v0_66",
        "docs/kuuos_self_organization_active_state.md",
        "README public status != authority grant",
    )
    return all(token in text for token in required_tokens)


def build_status() -> dict[str, Any]:
    return {
        "status_schema_version": STATUS_SCHEMA_VERSION,
        "status_command": STATUS_COMMAND,
        "active": active_state.SELF_ORGANIZATION_ACTIVE,
        "active_state_path": active_state.ACTIVE_STATE_PATH,
        "active_state_frontier": ACTIVE_STATE_FRONTIER,
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "bounded_execution_verified": active_state.verify_bounded_execution(),
        "current_root_sequence_verified": current_root.verify_current_root_sequence(),
        "public_status_checked": public_status_checked(),
        "authority_boundary": "active_state_not_unbounded_authority",
    }


def status_issues() -> tuple[str, ...]:
    issues: list[str] = []
    status = build_status()
    missing = set(REQUIRED_STATUS_KEYS).difference(status)
    if missing:
        issues.append("missing_status_keys:" + ",".join(sorted(missing)))
    if status.get("status_schema_version") != "v0.67":
        issues.append("status_schema_version")
    if status.get("status_command") != "kuuos_self_organization_status":
        issues.append("status_command")
    if status.get("active") is not True:
        issues.append("active")
    if status.get("active_state_path") != "docs/kuuos_self_organization_active_state.md":
        issues.append("active_state_path")
    if status.get("active_state_frontier") != "kuuos_self_organization_bounded_execution_v0_64":
        issues.append("active_state_frontier")
    if status.get("current_root_sequence") != "kuuos_current_root_sequence_v0_66":
        issues.append("current_root_sequence")
    if status.get("bounded_execution_verified") is not True:
        issues.append("bounded_execution_verified")
    if status.get("current_root_sequence_verified") is not True:
        issues.append("current_root_sequence_verified")
    if status.get("public_status_checked") is not True:
        issues.append("public_status_checked")
    if status.get("authority_boundary") != "active_state_not_unbounded_authority":
        issues.append("authority_boundary")
    return tuple(issues)


def verify_status() -> bool:
    return status_issues() == ()


def status_json() -> str:
    return json.dumps(build_status(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = status_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(status_json())
