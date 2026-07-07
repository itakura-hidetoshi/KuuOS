#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_99 as current_root
from runtime import kuuos_self_organization_candidate_queue_v0_97 as queue
from runtime import kuuos_self_organization_candidate_receipt_v0_98 as receipt
from runtime import kuuos_self_organization_selection_policy_v0_99 as policy

VERSION = "kuuos_self_organization_selected_next_action_v0_100"
DEPENDS_ON = policy.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SELECTED_NEXT_ACTION_PATH = "status/self_organization_selected_next_action_v0_100.json"
SELECTION_SCHEMA_VERSION = "v0.100"

COMPLETED_CANDIDATE_IDS: frozenset[str] = frozenset(
    {
        "candidate-receipt-v0-98",
        "selection-policy-v0-99",
        "selected-next-action-v0-100",
    }
)

CANDIDATE_NEXT_STAGES: dict[str, str] = {
    "candidate-receipt-v0-98": "v0.98",
    "selection-policy-v0-99": "v0.99",
    "selected-next-action-v0-100": "v0.100",
    "bounded-change-plan-v0-101": "v0.101",
}

CANDIDATE_SCOPES: dict[str, str] = {
    "candidate-receipt-v0-98": "candidate_receipt_only",
    "selection-policy-v0-99": "policy_only",
    "selected-next-action-v0-100": "selection_only",
    "bounded-change-plan-v0-101": "bounded_change_plan_only",
}

REQUIRED_SELECTION_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "candidate_receipt",
    "candidate_receipt_frontier",
    "current_root_check",
    "current_root_sequence",
    "effect_enabled",
    "next_artifact",
    "next_stage",
    "selected_candidate_id",
    "selected_candidate_scope",
    "selected_next_stage",
    "selection_frontier",
    "selection_mode",
    "selection_policy",
    "selection_policy_frontier",
    "selection_rule_applied",
    "selection_schema_version",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_selected_next_action() -> dict[str, Any]:
    return json.loads((_repo_root() / SELECTED_NEXT_ACTION_PATH).read_text(encoding="utf-8"))


def expected_selected_candidate_id() -> str:
    receipt_ids = receipt.load_candidate_receipt()["candidate_ids"]
    candidates = []
    for candidate_id in receipt_ids:
        if candidate_id in COMPLETED_CANDIDATE_IDS:
            continue
        candidates.append((CANDIDATE_NEXT_STAGES[candidate_id], candidate_id))
    return sorted(candidates)[0][1]


def expected_selected_next_action() -> dict[str, Any]:
    selected_id = expected_selected_candidate_id()
    return {
        "authority_boundary": "selected_next_action_not_grant",
        "candidate_receipt": receipt.CANDIDATE_RECEIPT_PATH,
        "candidate_receipt_frontier": receipt.VERSION,
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "effect_enabled": False,
        "next_artifact": "status/self_organization_bounded_change_plan_v0_101.json",
        "next_stage": "v0.101",
        "selected_candidate_id": selected_id,
        "selected_candidate_scope": CANDIDATE_SCOPES[selected_id],
        "selected_next_stage": CANDIDATE_NEXT_STAGES[selected_id],
        "selection_frontier": VERSION,
        "selection_mode": "selection_only",
        "selection_policy": policy.SELECTION_POLICY_PATH,
        "selection_policy_frontier": policy.VERSION,
        "selection_rule_applied": "lowest_expected_next_stage_after_completed_policy_and_selection_layers",
        "selection_schema_version": SELECTION_SCHEMA_VERSION,
    }


def selected_next_action_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        selected = load_selected_next_action()
    except FileNotFoundError:
        return ("selected_next_action_missing",)
    except json.JSONDecodeError:
        return ("selected_next_action_invalid_json",)
    missing = set(REQUIRED_SELECTION_KEYS).difference(selected)
    if missing:
        issues.append("missing_selected_next_action_keys:" + ",".join(sorted(missing)))
    extra = set(selected).difference(REQUIRED_SELECTION_KEYS)
    if extra:
        issues.append("extra_selected_next_action_keys:" + ",".join(sorted(extra)))
    if selected != expected_selected_next_action():
        issues.append("selected_next_action_mismatch")
    if selected.get("authority_boundary") != "selected_next_action_not_grant":
        issues.append("authority_boundary")
    if selected.get("selection_mode") != "selection_only":
        issues.append("selection_mode")
    if selected.get("effect_enabled") is not False:
        issues.append("effect_enabled")
    if selected.get("selected_candidate_id") not in receipt.load_candidate_receipt()["candidate_ids"]:
        issues.append("selected_candidate_missing_from_receipt")
    if selected.get("selected_candidate_id") != "bounded-change-plan-v0-101":
        issues.append("selected_candidate_id")
    if selected.get("selected_candidate_scope") != "bounded_change_plan_only":
        issues.append("selected_candidate_scope")
    if selected.get("selected_next_stage") != "v0.101":
        issues.append("selected_next_stage")
    if selected.get("next_artifact") != "status/self_organization_bounded_change_plan_v0_101.json":
        issues.append("next_artifact")
    if selected.get("next_stage") != "v0.101":
        issues.append("next_stage")
    policy_payload = policy.load_selection_policy()
    if policy_payload.get("next_artifact") != SELECTED_NEXT_ACTION_PATH:
        issues.append("policy_next_artifact")
    if policy_payload.get("next_stage") != "v0.100":
        issues.append("policy_next_stage")
    if policy_payload.get("selection_authorized") is not False:
        issues.append("policy_selection_flag")
    if queue.expected_candidate_ids() != receipt.load_candidate_receipt()["candidate_ids"]:
        issues.append("queue_receipt_candidate_ids")
    if not queue.verify_candidate_queue():
        issues.append("candidate_queue_not_verified")
    if not receipt.verify_candidate_receipt():
        issues.append("candidate_receipt_not_verified")
    if not policy.verify_selection_policy():
        issues.append("selection_policy_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_selected_next_action() -> bool:
    return selected_next_action_issues() == ()


def selected_next_action_json() -> str:
    return json.dumps(load_selected_next_action(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = selected_next_action_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(selected_next_action_json())
