#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_93 as current_root
from runtime import kuuos_self_organization_selected_next_action_v0_93 as selected_action

VERSION = "kuuos_self_organization_bounded_change_plan_v0_94"
DEPENDS_ON = selected_action.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
BOUNDED_CHANGE_PLAN_PATH = "status/self_organization_bounded_change_plan_v0_94.json"
BOUNDED_CHANGE_PLAN_SCHEMA_VERSION = "v0.94"

REQUIRED_BOUNDED_CHANGE_PLAN_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "bounded_change_plan_frontier",
    "bounded_change_plan_schema_version",
    "current_root_check",
    "current_root_sequence",
    "plan_enabled",
    "plan_mode",
    "planned_artifact",
    "planned_change_items",
    "planned_next_stage",
    "planned_runtime",
    "preconditions",
    "scope_boundary",
    "selected_next_action",
    "selected_next_action_frontier",
    "selected_next_action_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_bounded_change_plan() -> dict[str, Any]:
    return json.loads((_repo_root() / BOUNDED_CHANGE_PLAN_PATH).read_text(encoding="utf-8"))


def expected_bounded_change_plan() -> dict[str, Any]:
    return {
        "authority_boundary": "bounded_change_plan_not_grant",
        "bounded_change_plan_frontier": VERSION,
        "bounded_change_plan_schema_version": BOUNDED_CHANGE_PLAN_SCHEMA_VERSION,
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "plan_enabled": False,
        "plan_mode": "bounded_change_plan_only",
        "planned_artifact": "status/self_organization_completion_receipt_v0_95.json",
        "planned_change_items": [
            "bounded_change_plan_artifact_v0_94",
            "bounded_change_plan_runtime_v0_94",
            "bounded_change_plan_tests_v0_94",
            "current_root_sequence_v0_94",
        ],
        "planned_next_stage": "v0.95",
        "planned_runtime": "runtime/kuuos_self_organization_completion_receipt_v0_95.py",
        "preconditions": [
            "selected_candidate_id_is_bounded_change_plan_v0_94",
            "selected_candidate_scope_is_bounded_change_plan_only",
            "selected_next_action_verifies",
            "governance_gate_required_for_next_stage",
        ],
        "scope_boundary": "bounded_change_plan_record_only",
        "selected_next_action": selected_action.SELECTED_NEXT_ACTION_PATH,
        "selected_next_action_frontier": selected_action.VERSION,
        "selected_next_action_runtime": "runtime/kuuos_self_organization_selected_next_action_v0_93.py",
    }


def bounded_change_plan_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        plan = load_bounded_change_plan()
    except FileNotFoundError:
        return ("bounded_change_plan_missing",)
    except json.JSONDecodeError:
        return ("bounded_change_plan_invalid_json",)
    missing = set(REQUIRED_BOUNDED_CHANGE_PLAN_KEYS).difference(plan)
    if missing:
        issues.append("missing_bounded_change_plan_keys:" + ",".join(sorted(missing)))
    extra = set(plan).difference(REQUIRED_BOUNDED_CHANGE_PLAN_KEYS)
    if extra:
        issues.append("extra_bounded_change_plan_keys:" + ",".join(sorted(extra)))
    if plan != expected_bounded_change_plan():
        issues.append("bounded_change_plan_mismatch")
    if plan.get("authority_boundary") != "bounded_change_plan_not_grant":
        issues.append("authority_boundary")
    if plan.get("plan_mode") != "bounded_change_plan_only":
        issues.append("plan_mode")
    if plan.get("plan_enabled") is not False:
        issues.append("plan_enabled")
    if plan.get("scope_boundary") != "bounded_change_plan_record_only":
        issues.append("scope_boundary")
    if plan.get("planned_artifact") != "status/self_organization_completion_receipt_v0_95.json":
        issues.append("planned_artifact")
    if plan.get("planned_next_stage") != "v0.95":
        issues.append("planned_next_stage")
    selected = selected_action.load_selected_next_action()
    if selected.get("selected_candidate_id") != "bounded-change-plan-v0-94":
        issues.append("selected_candidate_id")
    if selected.get("selected_candidate_scope") != "bounded_change_plan_only":
        issues.append("selected_candidate_scope")
    if selected.get("selected_next_stage") != "v0.94":
        issues.append("selected_next_stage")
    if selected.get("next_artifact") != BOUNDED_CHANGE_PLAN_PATH:
        issues.append("selected_next_artifact")
    if selected.get("next_stage") != "v0.94":
        issues.append("selected_next_stage_pointer")
    if selected.get("effect_enabled") is not False:
        issues.append("selected_effect_enabled")
    if not selected_action.verify_selected_next_action():
        issues.append("selected_next_action_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_bounded_change_plan() -> bool:
    return bounded_change_plan_issues() == ()


def bounded_change_plan_json() -> str:
    return json.dumps(load_bounded_change_plan(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = bounded_change_plan_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(bounded_change_plan_json())
