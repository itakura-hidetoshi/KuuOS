#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_85 as current_root
from runtime import kuuos_self_organization_review_packet_v0_85 as packet

VERSION = "kuuos_self_organization_review_decision_v0_86"
DEPENDS_ON = packet.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
REVIEW_DECISION_PATH = "status/self_organization_review_decision_v0_86.json"
DECISION_SCHEMA_VERSION = "v0.86"

REQUIRED_DECISION_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "decision_frontier",
    "decision_mode",
    "decision_schema_version",
    "decision_status",
    "liveness_invariant",
    "next_artifact",
    "next_stage",
    "next_stage_kind",
    "packet_checks",
    "review_loop_closed",
    "source_packet",
    "source_packet_frontier",
    "source_packet_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_review_decision() -> dict[str, Any]:
    return json.loads((_repo_root() / REVIEW_DECISION_PATH).read_text(encoding="utf-8"))


def expected_review_decision() -> dict[str, Any]:
    return {
        "authority_boundary": "bounded_action_transition_not_blanket_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "decision_frontier": VERSION,
        "decision_mode": "bounded_action_transition",
        "decision_schema_version": DECISION_SCHEMA_VERSION,
        "decision_status": "review_closed_next_stage_must_prepare_bounded_change",
        "liveness_invariant": "review_must_end_in_bounded_change_or_explicit_rejection",
        "next_artifact": "status/self_organization_bounded_change_v0_87.json",
        "next_stage": "v0.87",
        "next_stage_kind": "bounded_repository_change",
        "packet_checks": [
            "packet_is_review_only",
            "packet_sources_are_recorded",
            "packet_requested_v0_86",
            "no_grant_boundary_is_preserved",
            "review_loop_is_closed",
        ],
        "review_loop_closed": True,
        "source_packet": packet.REVIEW_PACKET_PATH,
        "source_packet_frontier": packet.VERSION,
        "source_packet_runtime": "runtime/kuuos_self_organization_review_packet_v0_85.py",
    }


def review_decision_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        decision = load_review_decision()
    except FileNotFoundError:
        return ("review_decision_missing",)
    except json.JSONDecodeError:
        return ("review_decision_invalid_json",)
    missing = set(REQUIRED_DECISION_KEYS).difference(decision)
    if missing:
        issues.append("missing_review_decision_keys:" + ",".join(sorted(missing)))
    extra = set(decision).difference(REQUIRED_DECISION_KEYS)
    if extra:
        issues.append("extra_review_decision_keys:" + ",".join(sorted(extra)))
    if decision != expected_review_decision():
        issues.append("review_decision_mismatch")
    if decision.get("authority_boundary") != "bounded_action_transition_not_blanket_grant":
        issues.append("authority_boundary")
    if decision.get("decision_mode") != "bounded_action_transition":
        issues.append("decision_mode")
    if decision.get("decision_status") != "review_closed_next_stage_must_prepare_bounded_change":
        issues.append("decision_status")
    if decision.get("review_loop_closed") is not True:
        issues.append("review_loop_closed")
    if decision.get("next_stage_kind") != "bounded_repository_change":
        issues.append("next_stage_kind")
    if "review" in str(decision.get("next_stage_kind")):
        issues.append("next_stage_kind_must_not_be_review")
    if decision.get("liveness_invariant") != "review_must_end_in_bounded_change_or_explicit_rejection":
        issues.append("liveness_invariant")
    source = packet.load_review_packet()
    if source.get("requested_next_stage") != "v0.86":
        issues.append("source_packet_requested_stage")
    if source.get("requested_next_stage_artifact") != REVIEW_DECISION_PATH:
        issues.append("source_packet_requested_artifact")
    if source.get("packet_mode") != "review_only":
        issues.append("source_packet_mode")
    if not packet.verify_review_packet():
        issues.append("review_packet_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_review_decision() -> bool:
    return review_decision_issues() == ()


def review_decision_json() -> str:
    return json.dumps(load_review_decision(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = review_decision_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(review_decision_json())
