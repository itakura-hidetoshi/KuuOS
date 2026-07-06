#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_83 as current_root
from runtime import kuuos_self_organization_execution_plan_v0_83 as plan

VERSION = "kuuos_self_organization_next_request_v0_84"
DEPENDS_ON = plan.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
ITEM_PATH = "status/self_organization_next_request_v0_84.json"
SCHEMA_VERSION = "v0.84"

REQUIRED_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "next_request_frontier",
    "next_request_schema_version",
    "plan",
    "plan_frontier",
    "request_mode",
    "requested_artifact",
    "requested_next_stage",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_item() -> dict[str, Any]:
    return json.loads((_repo_root() / ITEM_PATH).read_text(encoding="utf-8"))


def expected_item() -> dict[str, Any]:
    return {
        "authority_boundary": "next_request_not_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_request_frontier": VERSION,
        "next_request_schema_version": SCHEMA_VERSION,
        "plan": plan.EXECUTION_PLAN_PATH,
        "plan_frontier": plan.VERSION,
        "request_mode": "request_only",
        "requested_artifact": "status/self_organization_review_packet_v0_85.json",
        "requested_next_stage": "v0.85",
    }


def item_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        item = load_item()
    except FileNotFoundError:
        return ("item_missing",)
    except json.JSONDecodeError:
        return ("item_invalid_json",)
    missing = set(REQUIRED_KEYS).difference(item)
    if missing:
        issues.append("missing_item_keys:" + ",".join(sorted(missing)))
    extra = set(item).difference(REQUIRED_KEYS)
    if extra:
        issues.append("extra_item_keys:" + ",".join(sorted(extra)))
    if item != expected_item():
        issues.append("item_mismatch")
    if item.get("authority_boundary") != "next_request_not_grant":
        issues.append("authority_boundary")
    if item.get("request_mode") != "request_only":
        issues.append("mode")
    if not plan.verify_execution_plan():
        issues.append("plan_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_item() -> bool:
    return item_issues() == ()


def item_json() -> str:
    return json.dumps(load_item(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = item_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(item_json())
