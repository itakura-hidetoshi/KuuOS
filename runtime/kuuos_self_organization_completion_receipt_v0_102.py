#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_101 as current_root
from runtime import kuuos_self_organization_bounded_change_plan_v0_101 as bounded_plan

VERSION = "kuuos_self_organization_completion_receipt_v0_102"
DEPENDS_ON = bounded_plan.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
COMPLETION_RECEIPT_PATH = "status/self_organization_completion_receipt_v0_102.json"
COMPLETION_RECEIPT_SCHEMA_VERSION = "v0.102"

REQUIRED_COMPLETION_RECEIPT_KEYS: tuple[str, ...] = (
    "completion_receipt_frontier",
    "completion_receipt_schema_version",
    "completed_stage",
    "completed_stage_artifact",
    "completed_stage_frontier",
    "completed_stage_runtime",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_stage",
    "receipt_items",
    "receipt_mode",
    "source_bounded_change_plan",
    "source_bounded_change_plan_frontier",
    "source_bounded_change_plan_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_completion_receipt() -> dict[str, Any]:
    return json.loads((_repo_root() / COMPLETION_RECEIPT_PATH).read_text(encoding="utf-8"))


def expected_completion_receipt() -> dict[str, Any]:
    return {
        "completion_receipt_frontier": VERSION,
        "completion_receipt_schema_version": COMPLETION_RECEIPT_SCHEMA_VERSION,
        "completed_stage": "v0.101",
        "completed_stage_artifact": bounded_plan.BOUNDED_CHANGE_PLAN_PATH,
        "completed_stage_frontier": bounded_plan.VERSION,
        "completed_stage_runtime": "runtime/kuuos_self_organization_bounded_change_plan_v0_101.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_next_cycle_seed_v0_103.json",
        "next_stage": "v0.103",
        "receipt_items": [
            "bounded_change_plan_artifact_verified",
            "bounded_change_plan_runtime_verified",
            "bounded_change_plan_tests_connected",
            "current_root_sequence_connected",
            "plan_enabled_false",
        ],
        "receipt_mode": "completion_receipt_only",
        "source_bounded_change_plan": bounded_plan.BOUNDED_CHANGE_PLAN_PATH,
        "source_bounded_change_plan_frontier": bounded_plan.VERSION,
        "source_bounded_change_plan_runtime": "runtime/kuuos_self_organization_bounded_change_plan_v0_101.py",
    }


def completion_receipt_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        receipt = load_completion_receipt()
    except FileNotFoundError:
        return ("completion_receipt_missing",)
    except json.JSONDecodeError:
        return ("completion_receipt_invalid_json",)
    missing = set(REQUIRED_COMPLETION_RECEIPT_KEYS).difference(receipt)
    if missing:
        issues.append("missing_completion_receipt_keys:" + ",".join(sorted(missing)))
    extra = set(receipt).difference(REQUIRED_COMPLETION_RECEIPT_KEYS)
    if extra:
        issues.append("extra_completion_receipt_keys:" + ",".join(sorted(extra)))
    if receipt != expected_completion_receipt():
        issues.append("completion_receipt_mismatch")
    if receipt.get("receipt_mode") != "completion_receipt_only":
        issues.append("receipt_mode")
    if receipt.get("completed_stage") != "v0.101":
        issues.append("completed_stage")
    if receipt.get("next_artifact") != "status/self_organization_next_cycle_seed_v0_103.json":
        issues.append("next_artifact")
    if receipt.get("next_stage") != "v0.103":
        issues.append("next_stage")
    source = bounded_plan.load_bounded_change_plan()
    if source.get("planned_artifact") != COMPLETION_RECEIPT_PATH:
        issues.append("source_planned_artifact")
    if source.get("planned_next_stage") != "v0.102":
        issues.append("source_planned_next_stage")
    if source.get("plan_mode") != "bounded_change_plan_only":
        issues.append("source_plan_mode")
    if source.get("plan_enabled") is not False:
        issues.append("source_plan_enabled")
    if source.get("scope_boundary") != "bounded_change_plan_record_only":
        issues.append("source_scope_boundary")
    if not bounded_plan.verify_bounded_change_plan():
        issues.append("bounded_change_plan_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_completion_receipt() -> bool:
    return completion_receipt_issues() == ()


def completion_receipt_json() -> str:
    return json.dumps(load_completion_receipt(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = completion_receipt_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(completion_receipt_json())
