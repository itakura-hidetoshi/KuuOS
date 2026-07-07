#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_91 as current_root
from runtime import kuuos_self_organization_candidate_receipt_v0_91 as receipt

VERSION = "kuuos_self_organization_selection_policy_v0_92"
DEPENDS_ON = receipt.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SELECTION_POLICY_PATH = "status/self_organization_selection_policy_v0_92.json"
POLICY_SCHEMA_VERSION = "v0.92"

REQUIRED_POLICY_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "candidate_receipt",
    "candidate_receipt_frontier",
    "candidate_receipt_runtime",
    "current_root_check",
    "current_root_sequence",
    "effect_authorized",
    "next_artifact",
    "next_stage",
    "policy_frontier",
    "policy_mode",
    "policy_schema_version",
    "ranking_rules",
    "selection_authorized",
    "selection_output",
    "tie_breaker",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_selection_policy() -> dict[str, Any]:
    return json.loads((_repo_root() / SELECTION_POLICY_PATH).read_text(encoding="utf-8"))


def expected_selection_policy() -> dict[str, Any]:
    return {
        "authority_boundary": "selection_policy_not_authority_grant",
        "candidate_receipt": receipt.CANDIDATE_RECEIPT_PATH,
        "candidate_receipt_frontier": receipt.VERSION,
        "candidate_receipt_runtime": "runtime/kuuos_self_organization_candidate_receipt_v0_91.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "effect_authorized": False,
        "next_artifact": "status/self_organization_selected_next_action_v0_93.json",
        "next_stage": "v0.93",
        "policy_frontier": VERSION,
        "policy_mode": "policy_only",
        "policy_schema_version": POLICY_SCHEMA_VERSION,
        "ranking_rules": [
            "candidate_must_exist_in_v0_91_receipt",
            "candidate_must_preserve_pr_path",
            "candidate_must_require_governance_gate",
            "candidate_must_have_single_next_stage_scope",
        ],
        "selection_authorized": False,
        "selection_output": None,
        "tie_breaker": "lowest_expected_next_stage",
    }


def selection_policy_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        policy = load_selection_policy()
    except FileNotFoundError:
        return ("selection_policy_missing",)
    except json.JSONDecodeError:
        return ("selection_policy_invalid_json",)
    missing = set(REQUIRED_POLICY_KEYS).difference(policy)
    if missing:
        issues.append("missing_selection_policy_keys:" + ",".join(sorted(missing)))
    extra = set(policy).difference(REQUIRED_POLICY_KEYS)
    if extra:
        issues.append("extra_selection_policy_keys:" + ",".join(sorted(extra)))
    if policy != expected_selection_policy():
        issues.append("selection_policy_mismatch")
    if policy.get("authority_boundary") != "selection_policy_not_authority_grant":
        issues.append("authority_boundary")
    if policy.get("policy_mode") != "policy_only":
        issues.append("policy_mode")
    if policy.get("effect_authorized") is not False:
        issues.append("effect_authorized")
    if policy.get("selection_authorized") is not False:
        issues.append("selection_authorized")
    if policy.get("selection_output") is not None:
        issues.append("selection_output")
    if policy.get("tie_breaker") != "lowest_expected_next_stage":
        issues.append("tie_breaker")
    if policy.get("next_artifact") != "status/self_organization_selected_next_action_v0_93.json":
        issues.append("next_artifact")
    if policy.get("next_stage") != "v0.93":
        issues.append("next_stage")
    receipt_payload = receipt.load_candidate_receipt()
    if policy.get("candidate_receipt") != receipt.CANDIDATE_RECEIPT_PATH:
        issues.append("candidate_receipt_path")
    if receipt_payload.get("next_artifact") != SELECTION_POLICY_PATH:
        issues.append("receipt_next_artifact")
    if receipt_payload.get("next_stage") != "v0.92":
        issues.append("receipt_next_stage")
    if receipt_payload.get("selection_authorized") is not False:
        issues.append("receipt_selection_flag")
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
