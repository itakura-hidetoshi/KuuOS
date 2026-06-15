#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_licensed_canary_observation_trial_plan_v0_25"
LICENSE_VERSION = "indra_qi_licensed_canary_observation_trial_license_v0_25"
REPORT_VERSION = "indra_qi_licensed_canary_observation_trial_report_v0_25"
STATE_VERSION = "indra_qi_licensed_canary_observation_trial_state_v0_25"
LEDGER_VERSION = "indra_qi_licensed_canary_observation_trial_ledger_record_v0_25"
WORLD_VERSION = "indra_qi_world_model_v0_1"
PROPOSAL_VERSION = "indra_qi_bounded_canary_observation_proposal_v0_24"
SOURCE_STATE_VERSION = "indra_qi_bounded_canary_observation_state_v0_24"
SOURCE_RECOMMENDATION_VERSION = "indra_qi_bounded_canary_observation_recommendation_v0_24"
VERSION = "indra_qi_licensed_canary_observation_trial_v0_25"
READY = "INDRA_QI_LICENSED_CANARY_OBSERVATION_TRIAL_V0_25_READY"
BLOCKED = "INDRA_QI_LICENSED_CANARY_OBSERVATION_TRIAL_V0_25_BLOCKED"

SOURCE_DECISIONS = {
    "hold_for_observation",
    "bounded_canary_observation_proposal_ready",
    "redesign_bounded_canary_observation_proposal_recommended",
    "extend_mirror_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "licensed_canary_observation_trial_ready",
    "redesign_canary_observation_trial_recommended",
    "extend_mirror_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_24_proposal_required": True,
    "source_v0_24_digest_chain_exact": True,
    "world_source_read_only": True,
    "canary_proposal_source_read_only": True,
    "licensed_observation_copy_trial_only": True,
    "source_lane_binding_exact": True,
    "trial_fraction_bounded": True,
    "trial_duration_bounded": True,
    "trial_event_budget_bounded": True,
    "expiry_respected": True,
    "automatic_revocation_required": True,
    "rollback_receipt_required": True,
    "redaction_receipt_required": True,
    "deterministic_replay_required": True,
    "replica_restore_required": True,
    "digest_only_input_required": True,
    "raw_payload_storage_forbidden": True,
    "live_response_influence_forbidden": True,
    "feedback_to_live_path_forbidden": True,
    "live_canary_activation_forbidden": True,
    "external_actuation_disabled": True,
    "world_update_disabled": True,
    "winner_selection_forbidden": True,
    "recovery_lane_preserved": True,
    "minority_lane_preserved": True,
    "fairness_preservation_required": True,
    "candidate_weighting_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_lineage_selection_authority": True,
    "not_live_lineage_execution_authority": True,
    "not_live_canary_activation_authority": True,
    "not_external_world_actuation_authority": True,
    "not_unlicensed_execution_authority": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "canary_trial_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "canary_trial_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "canary_trial_state_digest"))


def read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        output.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return output


def write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _positive_int(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str]) -> None:
    for field in fields:
        value = policy.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            blockers.append(f"canary_trial_policy_{field}_invalid")


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str]) -> None:
    for field in fields:
        value = policy.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            blockers.append(f"canary_trial_policy_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("canary_trial_plan_version_invalid")
    if plan.get("canary_trial_plan_digest") != plan_digest(plan):
        blockers.append("canary_trial_plan_digest_invalid")
    for field in (
        "trial_program_id",
        "trial_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_canary_proposal_digest",
        "expected_source_canary_state_digest",
        "expected_source_canary_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"canary_trial_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"canary_trial_boundary_{field}_mismatch")
    policy = mapping(plan.get("trial_policy"))
    _positive_int(
        policy,
        (
            "minimum_trial_lanes",
            "maximum_trial_lanes",
            "minimum_recovery_lanes",
            "minimum_minority_lanes",
            "maximum_duration_seconds",
            "maximum_event_budget",
            "maximum_event_budget_per_lane",
        ),
        blockers,
    )
    low = policy.get("minimum_trial_lanes")
    high = policy.get("maximum_trial_lanes")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 8):
        blockers.append("canary_trial_lane_count_bounds_invalid")
    _bounded(
        policy,
        (
            "maximum_total_trial_fraction",
            "maximum_single_lane_fraction",
            "maximum_latency_delta_ratio",
            "maximum_output_divergence_score",
            "maximum_allocation_error",
            "minimum_jain_fairness_index",
            "minimum_lane_service_ratio",
            "maximum_redaction_failure_ratio",
            "maximum_live_response_influence_ratio",
            "maximum_copy_delivery_failure_ratio",
            "minimum_rollback_receipt_ratio",
            "minimum_revocation_ratio",
            "minimum_replica_restore_ratio",
            "minimum_deterministic_replay_ratio",
        ),
        blockers,
    )
    for field in (
        "require_exact_source_lane_binding",
        "require_digest_only_copy",
        "require_raw_payload_absent",
        "require_redaction_receipt",
        "require_deterministic_replay",
        "require_rollback_receipt",
        "require_automatic_revocation",
        "require_replica_restore",
        "require_live_response_unchanged",
        "require_feedback_to_live_path_disabled",
        "require_live_canary_activation_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"canary_trial_policy_{field}_not_true")
