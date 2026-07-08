#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_112 as current_root
from runtime import kuuos_self_organization_candidate_receipt_v0_112 as receipt

VERSION = "kuuos_self_organization_selection_policy_v0_113"
DEPENDS_ON = receipt.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SELECTION_POLICY_PATH = "status/self_organization_selection_policy_v0_113.json"
SELECTION_POLICY_SCHEMA_VERSION = "v0.113"

REQUIRED_SELECTION_POLICY_KEYS: tuple[str, ...] = (
    "candidate_receipt",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_stage",
    "policy_frontier",
    "policy_mode",
    "policy_schema_version",
    "policy_scope",
    "selected_candidate_id",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_selection_policy() -> dict[str, Any]:
    return json.loads((_repo_root() / SELECTION_POLICY_PATH).read_text(encoding="utf-8"))


def expected_selection_policy() -> dict[str, Any]:
    return {
        "candidate_receipt": receipt.CANDIDATE_RECEIPT_PATH,
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_selected_next_action_v0_114.json",
        "next_stage": "v0.114",
        "policy_frontier": VERSION,
        "policy_mode": "selection_policy_only",
        "policy_schema_version": SELECTION_POLICY_SCHEMA_VERSION,
        "policy_scope": "self_organization_next_cycle",
        "selected_candidate_id": "selection-policy-v0-113",
    }


def selection_policy_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        policy = load_selection_policy()
    except FileNotFoundError:
        return ("selection_policy_missing",)
    except json.JSONDecodeError:
        return ("selection_policy_invalid_json",)
    missing = set(REQUIRED_SELECTION_POLICY_KEYS).difference(policy)
    if missing:
        issues.append("missing_selection_policy_keys:" + ",".join(sorted(missing)))
    extra = set(policy).difference(REQUIRED_SELECTION_POLICY_KEYS)
    if extra:
        issues.append("extra_selection_policy_keys:" + ",".join(sorted(extra)))
    if policy != expected_selection_policy():
        issues.append("selection_policy_mismatch")
    if policy.get("policy_mode") != "selection_policy_only":
        issues.append("policy_mode")
    if policy.get("policy_scope") != "self_organization_next_cycle":
        issues.append("policy_scope")
    if policy.get("selected_candidate_id") not in receipt.expected_received_candidate_ids():
        issues.append("selected_candidate_id")
    if policy.get("next_artifact") != "status/self_organization_selected_next_action_v0_114.json":
        issues.append("next_artifact")
    if policy.get("next_stage") != "v0.114":
        issues.append("next_stage")
    source = receipt.load_candidate_receipt()
    if source.get("next_artifact") != SELECTION_POLICY_PATH:
        issues.append("receipt_next_artifact")
    if source.get("next_stage") != "v0.113":
        issues.append("receipt_next_stage")
    if not receipt.verify_candidate_receipt():
        issues.append("candidate_receipt_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_selection_policy() -> bool:
    return selection_policy_issues() == ()


def selection_policy_json() -> str:
    return json.dumps(load_selection_policy(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = selection_policy_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(selection_policy_json())
