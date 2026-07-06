#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_84 as current_root
from runtime import kuuos_self_organization_candidate_queue_v0_79 as queue
from runtime import kuuos_self_organization_candidate_receipt_v0_80 as receipt
from runtime import kuuos_self_organization_execution_plan_v0_83 as plan
from runtime import kuuos_self_organization_next_request_v0_84 as request
from runtime import kuuos_self_organization_selected_next_action_v0_82 as selected
from runtime import kuuos_self_organization_selection_policy_v0_81 as policy

VERSION = "kuuos_self_organization_review_packet_v0_85"
DEPENDS_ON = request.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
REVIEW_PACKET_PATH = "status/self_organization_review_packet_v0_85.json"
PACKET_SCHEMA_VERSION = "v0.85"

REQUIRED_PACKET_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "packet_frontier",
    "packet_mode",
    "packet_schema_version",
    "packet_sources",
    "requested_next_stage",
    "requested_next_stage_artifact",
    "review_focus",
    "source_request",
    "source_request_frontier",
    "source_request_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_review_packet() -> dict[str, Any]:
    return json.loads((_repo_root() / REVIEW_PACKET_PATH).read_text(encoding="utf-8"))


def expected_packet_sources() -> list[str]:
    return [
        queue.CANDIDATE_QUEUE_PATH,
        receipt.CANDIDATE_RECEIPT_PATH,
        policy.SELECTION_POLICY_PATH,
        selected.SELECTED_NEXT_ACTION_PATH,
        plan.EXECUTION_PLAN_PATH,
        request.ITEM_PATH,
    ]


def expected_review_packet() -> dict[str, Any]:
    return {
        "authority_boundary": "review_packet_not_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "packet_frontier": VERSION,
        "packet_mode": "review_only",
        "packet_schema_version": PACKET_SCHEMA_VERSION,
        "packet_sources": expected_packet_sources(),
        "requested_next_stage": "v0.86",
        "requested_next_stage_artifact": "status/self_organization_review_decision_v0_86.json",
        "review_focus": [
            "queue_was_recorded",
            "policy_was_recorded",
            "selected_action_was_recorded",
            "plan_was_recorded",
            "next_request_was_recorded",
            "no_grant_boundary_is_preserved",
        ],
        "source_request": request.ITEM_PATH,
        "source_request_frontier": request.VERSION,
        "source_request_runtime": "runtime/kuuos_self_organization_next_request_v0_84.py",
    }


def review_packet_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        packet = load_review_packet()
    except FileNotFoundError:
        return ("review_packet_missing",)
    except json.JSONDecodeError:
        return ("review_packet_invalid_json",)
    missing = set(REQUIRED_PACKET_KEYS).difference(packet)
    if missing:
        issues.append("missing_review_packet_keys:" + ",".join(sorted(missing)))
    extra = set(packet).difference(REQUIRED_PACKET_KEYS)
    if extra:
        issues.append("extra_review_packet_keys:" + ",".join(sorted(extra)))
    if packet != expected_review_packet():
        issues.append("review_packet_mismatch")
    if packet.get("authority_boundary") != "review_packet_not_grant":
        issues.append("authority_boundary")
    if packet.get("packet_mode") != "review_only":
        issues.append("packet_mode")
    if packet.get("packet_sources") != expected_packet_sources():
        issues.append("packet_sources")
    if request.load_item().get("requested_artifact") != REVIEW_PACKET_PATH:
        issues.append("request_does_not_name_review_packet")
    if request.load_item().get("requested_next_stage") != "v0.85":
        issues.append("request_stage")
    if not queue.verify_candidate_queue():
        issues.append("candidate_queue_not_verified")
    if not receipt.verify_candidate_receipt():
        issues.append("candidate_receipt_not_verified")
    if not policy.verify_selection_policy():
        issues.append("selection_policy_not_verified")
    if not selected.verify_selected_next_action():
        issues.append("selected_next_action_not_verified")
    if not plan.verify_execution_plan():
        issues.append("execution_plan_not_verified")
    if not request.verify_item():
        issues.append("next_request_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_review_packet() -> bool:
    return review_packet_issues() == ()


def review_packet_json() -> str:
    return json.dumps(load_review_packet(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = review_packet_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(review_packet_json())
