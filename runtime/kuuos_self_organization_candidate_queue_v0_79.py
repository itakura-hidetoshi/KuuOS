#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_78 as current_root
from runtime import kuuos_current_surface_entrypoint_v0_77 as current_surface
from runtime import kuuos_current_status_surface_index_v0_76 as surface_index

VERSION = "kuuos_self_organization_candidate_queue_v0_79"
DEPENDS_ON = current_surface.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
CANDIDATE_QUEUE_PATH = "status/self_organization_candidate_queue_v0_79.json"
CANDIDATE_QUEUE_SCHEMA_VERSION = "v0.79"

REQUIRED_QUEUE_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "candidate_queue_frontier",
    "candidate_queue_schema_version",
    "candidates",
    "current_root_check",
    "current_root_sequence",
    "derived_from",
    "generation_mode",
    "stable_current_surface_cli",
)

REQUIRED_CANDIDATE_KEYS: tuple[str, ...] = (
    "candidate_id",
    "description",
    "expected_next_stage",
    "required_gate",
    "risk",
    "scope",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_candidate_queue() -> dict[str, Any]:
    return json.loads((_repo_root() / CANDIDATE_QUEUE_PATH).read_text(encoding="utf-8"))


def expected_candidate_queue() -> dict[str, Any]:
    return {
        "authority_boundary": "candidate_queue_not_authority_grant",
        "candidate_queue_frontier": VERSION,
        "candidate_queue_schema_version": CANDIDATE_QUEUE_SCHEMA_VERSION,
        "candidates": [
            {
                "candidate_id": "selection-policy-v0-81",
                "description": "Define a policy for selecting among generated self-organization candidates.",
                "expected_next_stage": "v0.81",
                "required_gate": "KuuOS PR Governance Gate",
                "risk": "policy_mismatch",
                "scope": "proposal_only",
            },
            {
                "candidate_id": "candidate-receipt-v0-80",
                "description": "Commit a receipt for this generated candidate queue before choosing a next action.",
                "expected_next_stage": "v0.80",
                "required_gate": "KuuOS PR Governance Gate",
                "risk": "stale_candidate_receipt",
                "scope": "proposal_receipt",
            },
            {
                "candidate_id": "selected-next-action-v0-82",
                "description": "Select one candidate under the selection policy without executing repository mutation.",
                "expected_next_stage": "v0.82",
                "required_gate": "KuuOS PR Governance Gate",
                "risk": "selection_without_policy",
                "scope": "selection_only",
            },
            {
                "candidate_id": "execution-plan-v0-83",
                "description": "Create a bounded execution plan for a selected action.",
                "expected_next_stage": "v0.83",
                "required_gate": "KuuOS PR Governance Gate",
                "risk": "plan_scope_expansion",
                "scope": "plan_only",
            },
        ],
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "derived_from": surface_index.SURFACE_INDEX_PATH,
        "generation_mode": "proposal_only",
        "stable_current_surface_cli": current_surface.STABLE_ENTRYPOINT,
    }


def candidate_queue_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        queue = load_candidate_queue()
    except FileNotFoundError:
        return ("candidate_queue_missing",)
    except json.JSONDecodeError:
        return ("candidate_queue_invalid_json",)
    missing = set(REQUIRED_QUEUE_KEYS).difference(queue)
    if missing:
        issues.append("missing_candidate_queue_keys:" + ",".join(sorted(missing)))
    extra = set(queue).difference(REQUIRED_QUEUE_KEYS)
    if extra:
        issues.append("extra_candidate_queue_keys:" + ",".join(sorted(extra)))
    expected = expected_candidate_queue()
    if queue != expected:
        issues.append("candidate_queue_mismatch")
    candidates = queue.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        issues.append("candidate_queue_empty")
    candidate_ids: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            issues.append("candidate_not_object")
            continue
        missing_candidate = set(REQUIRED_CANDIDATE_KEYS).difference(candidate)
        if missing_candidate:
            issues.append("missing_candidate_keys:" + ",".join(sorted(missing_candidate)))
        candidate_ids.append(str(candidate.get("candidate_id")))
        if candidate.get("required_gate") != "KuuOS PR Governance Gate":
            issues.append("candidate_gate:" + str(candidate.get("candidate_id")))
    if len(candidate_ids) != len(set(candidate_ids)):
        issues.append("duplicate_candidate_id")
    if queue.get("authority_boundary") != "candidate_queue_not_authority_grant":
        issues.append("authority_boundary")
    if queue.get("generation_mode") != "proposal_only":
        issues.append("generation_mode")
    if not surface_index.verify_surface_index():
        issues.append("surface_index_not_verified")
    if not current_surface.verify_entrypoint():
        issues.append("current_surface_entrypoint_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_candidate_queue() -> bool:
    return candidate_queue_issues() == ()


def candidate_queue_json() -> str:
    return json.dumps(load_candidate_queue(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = candidate_queue_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(candidate_queue_json())
