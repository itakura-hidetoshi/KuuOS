#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_81 as current_root
from runtime import kuuos_self_organization_candidate_receipt_v0_80 as receipt
from runtime import kuuos_self_organization_candidate_queue_v0_79 as queue
from runtime import kuuos_self_organization_selection_policy_v0_81 as policy

VERSION = "kuuos_self_organization_selected_next_action_v0_82"
DEPENDS_ON = policy.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SELECTED_NEXT_ACTION_PATH = "status/self_organization_selected_next_action_v0_82.json"
SELECTION_SCHEMA_VERSION = "v0.82"

REQUIRED_SELECTION_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "candidate_receipt",
    "candidate_receipt_frontier",
    "current_root_check",
    "current_root_sequence",
    "effect_enabled",
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


def queue_candidate(candidate_id: str) -> dict[str, Any]:
    for candidate in queue.load_candidate_queue()["candidates"]:
        if candidate["candidate_id"] == candidate_id:
            return candidate
    raise KeyError(candidate_id)


def expected_selected_candidate_id() -> str:
    completed = {"candidate-receipt-v0-80", "selection-policy-v0-81", "selected-next-action-v0-82"}
    candidates = []
    for candidate_id in receipt.load_candidate_receipt()["candidate_ids"]:
        if candidate_id in completed:
            continue
        candidate = queue_candidate(candidate_id)
        candidates.append((candidate["expected_next_stage"], candidate_id))
    return sorted(candidates)[0][1]


def expected_selected_next_action() -> dict[str, Any]:
    selected_id = expected_selected_candidate_id()
    selected = queue_candidate(selected_id)
    return {
        "authority_boundary": "selected_next_action_not_grant",
        "candidate_receipt": receipt.CANDIDATE_RECEIPT_PATH,
        "candidate_receipt_frontier": receipt.VERSION,
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "effect_enabled": False,
        "selected_candidate_id": selected_id,
        "selected_candidate_scope": selected["scope"],
        "selected_next_stage": selected["expected_next_stage"],
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
