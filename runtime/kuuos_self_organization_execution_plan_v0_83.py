#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_82 as current_root
from runtime import kuuos_self_organization_selected_next_action_v0_82 as selected_action

VERSION = "kuuos_self_organization_execution_plan_v0_83"
DEPENDS_ON = selected_action.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
EXECUTION_PLAN_PATH = "status/self_organization_execution_plan_v0_83.json"
PLAN_SCHEMA_VERSION = "v0.83"

REQUIRED_PLAN_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "execution_plan_frontier",
    "execution_plan_schema_version",
    "plan_enabled",
    "plan_mode",
    "planned_artifact",
    "planned_next_stage",
    "planned_runtime",
    "preconditions",
    "selected_next_action",
    "selected_next_action_frontier",
    "selected_next_action_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_execution_plan() -> dict[str, Any]:
    return json.loads((_repo_root() / EXECUTION_PLAN_PATH).read_text(encoding="utf-8"))


def expected_execution_plan() -> dict[str, Any]:
    selected = selected_action.load_selected_next_action()
    return {
        "authority_boundary": "execution_plan_not_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "execution_plan_frontier": VERSION,
        "execution_plan_schema_version": PLAN_SCHEMA_VERSION,
        "plan_enabled": False,
        "plan_mode": "plan_only",
        "planned_artifact": "status/self_organization_next_request_v0_84.json",
        "planned_next_stage": "v0.84",
        "planned_runtime": "runtime/kuuos_self_organization_next_request_v0_84.py",
        "preconditions": [
            "selected_candidate_id_is_execution_plan_v0_83",
            "selected_candidate_scope_is_plan_only",
            "selected_next_action_verifies",
            "governance_gate_required_for_next_stage",
        ],
        "selected_next_action": selected_action.SELECTED_NEXT_ACTION_PATH,
        "selected_next_action_frontier": selected_action.VERSION,
        "selected_next_action_runtime": "runtime/kuuos_self_organization_selected_next_action_v0_82.py",
    }


def execution_plan_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        plan = load_execution_plan()
    except FileNotFoundError:
        return ("execution_plan_missing",)
    except json.JSONDecodeError:
        return ("execution_plan_invalid_json",)
    missing = set(REQUIRED_PLAN_KEYS).difference(plan)
    if missing:
        issues.append("missing_execution_plan_keys:" + ",".join(sorted(missing)))
    extra = set(plan).difference(REQUIRED_PLAN_KEYS)
    if extra:
        issues.append("extra_execution_plan_keys:" + ",".join(sorted(extra)))
    if plan != expected_execution_plan():
        issues.append("execution_plan_mismatch")
    if plan.get("authority_boundary") != "execution_plan_not_grant":
        issues.append("authority_boundary")
    if plan.get("plan_mode") != "plan_only":
        issues.append("plan_mode")
    if plan.get("plan_enabled") is not False:
        issues.append("plan_enabled")
    selected = selected_action.load_selected_next_action()
    if selected.get("selected_candidate_id") != "execution-plan-v0-83":
        issues.append("selected_candidate_id")
    if selected.get("selected_candidate_scope") != "plan_only":
        issues.append("selected_candidate_scope")
    if not selected_action.verify_selected_next_action():
        issues.append("selected_next_action_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_execution_plan() -> bool:
    return execution_plan_issues() == ()


def execution_plan_json() -> str:
    return json.dumps(load_execution_plan(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = execution_plan_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(execution_plan_json())
