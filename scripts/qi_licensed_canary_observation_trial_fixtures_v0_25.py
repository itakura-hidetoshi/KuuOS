#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_licensed_canary_observation_trial_core_v0_25 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_licensed_canary_observation_trial_runtime_v0_25 import (
    BLOCKED,
    READY,
    build_licensed_canary_observation_trial,
)


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def source_lane(lineage_id: str, kind: str, fraction: float, proposal_epoch: int) -> dict[str, Any]:
    return {
        "lane_id": "lane-" + lineage_id,
        "lineage_id": lineage_id,
        "lineage_kind": kind,
        "canary_fraction": fraction,
        "event_budget": 8,
        "expiry_epoch": proposal_epoch + 240,
        "shadow_return_token_digest": sha({"return": lineage_id}),
        "rollback_receipt_template_digest": sha({"rollback-template": lineage_id}),
        "latency_guardrail_ratio": 0.15,
        "output_divergence_guardrail": 0.08,
        "fairness_guardrail_ratio": 0.90,
        "automatic_revocation_enabled": True,
        "canary_activation_enabled": False,
        "live_response_influence_enabled": False,
        "feedback_to_live_path_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "winner_selected": False,
        "policy_boundary_preserved": True,
        "duration_seconds": 240,
        "proposal_boundary_preserved": True,
    }


def sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "mandala_inclusion": {"multi_world_noncollapse": True, "single_ontology_forced": False},
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)
    proposal_epoch = 1000
    lanes = [
        source_lane("l0", "explore", 0.020, proposal_epoch),
        source_lane("l1", "recovery", 0.015, proposal_epoch),
        source_lane("l2", "minority_preservation", 0.015, proposal_epoch),
    ]
    proposal = {
        "version": "indra_qi_bounded_canary_observation_proposal_v0_24",
        "proposal_program_id": "canary-proposal-program-a",
        "proposal_run_id": "canary-proposal-run-a",
        "world_model_id": "world-a",
        "source_longitudinal_decision": "longitudinal_mirror_noninterference_ready",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_longitudinal_summary_digest": sha({"long-summary": 1}),
        "source_longitudinal_state_digest": sha({"long-state": 1}),
        "source_longitudinal_recommendation_digest": sha({"long-rec": 1}),
        "bounded_canary_report_digest": sha({"canary-report": 1}),
        "proposal_epoch": proposal_epoch,
        "duration_seconds": 240,
        "canary_lanes": lanes,
        "proposal_analysis": {},
        "proposal_only": True,
        "canary_activated": False,
        "live_response_influenced": False,
        "feedback_to_live_path_enabled": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": 50,
    }
    proposal["bounded_canary_proposal_digest"] = sha(proposal)
    state = {
        "version": "indra_qi_bounded_canary_observation_state_v0_24",
        "proposal_program_id": "canary-proposal-program-a",
        "world_model_id": "world-a",
        "last_proposal_run_id": "canary-proposal-run-a",
        "latest_bounded_canary_decision": decision,
        "latest_bounded_canary_proposal_digest": proposal["bounded_canary_proposal_digest"],
        "epoch": 51,
    }
    state["bounded_canary_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_bounded_canary_observation_recommendation_v0_24",
        "proposal_program_id": "canary-proposal-program-a",
        "proposal_run_id": "canary-proposal-run-a",
        "world_model_id": "world-a",
        "source_longitudinal_decision": "longitudinal_mirror_noninterference_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "proposal_ready": decision == "bounded_canary_observation_proposal_ready",
        "canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "bounded_canary_proposal_digest": proposal["bounded_canary_proposal_digest"],
        "proposal_analysis": {},
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "recommendation_only": True,
        "proposal_not_canary_activation": True,
        "direct_canary_activation_authority": False,
        "direct_live_response_influence_authority": False,
        "direct_feedback_to_live_path_authority": False,
        "direct_winner_selection_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "epoch": 51,
    }
    recommendation["bounded_canary_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_bounded_canary_observation_proposal_v0_24.json", proposal)
    write(root / "indra_qi_bounded_canary_observation_state_v0_24.json", state)
    write(root / "indra_qi_bounded_canary_observation_recommendation_v0_24.json", recommendation)
    return {"world": world, "proposal": proposal, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], run_id: str = "canary-trial-run-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "trial_program_id": "canary-trial-program-a",
        "trial_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_canary_proposal_digest": source["proposal"]["bounded_canary_proposal_digest"],
        "expected_source_canary_state_digest": source["state"]["bounded_canary_state_digest"],
        "expected_source_canary_recommendation_digest": source["recommendation"][
            "bounded_canary_recommendation_digest"
        ],
        "trial_policy": {
            "minimum_trial_lanes": 3,
            "maximum_trial_lanes": 4,
            "minimum_recovery_lanes": 1,
            "minimum_minority_lanes": 1,
            "maximum_total_trial_fraction": 0.05,
            "maximum_single_lane_fraction": 0.025,
            "maximum_duration_seconds": 300,
            "maximum_event_budget": 30,
            "maximum_event_budget_per_lane": 12,
            "maximum_latency_delta_ratio": 0.20,
            "maximum_output_divergence_score": 0.10,
            "maximum_allocation_error": 0.10,
            "minimum_jain_fairness_index": 0.80,
            "minimum_lane_service_ratio": 1.0,
            "maximum_redaction_failure_ratio": 0.0,
            "maximum_live_response_influence_ratio": 0.0,
            "maximum_copy_delivery_failure_ratio": 0.0,
            "minimum_rollback_receipt_ratio": 1.0,
            "minimum_revocation_ratio": 1.0,
            "minimum_replica_restore_ratio": 1.0,
            "minimum_deterministic_replay_ratio": 1.0,
            "require_exact_source_lane_binding": True,
            "require_digest_only_copy": True,
            "require_raw_payload_absent": True,
            "require_redaction_receipt": True,
            "require_deterministic_replay": True,
            "require_rollback_receipt": True,
            "require_automatic_revocation": True,
            "require_replica_restore": True,
            "require_live_response_unchanged": True,
            "require_feedback_to_live_path_disabled": True,
            "require_live_canary_activation_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["canary_trial_plan_digest"] = plan_digest(value)
    return value


def trial_lane(source_lane_value: Mapping[str, Any], fraction: float, trial_epoch: int, duration: int, budget: int = 4) -> dict[str, Any]:
    return {
        "lane_id": source_lane_value["lane_id"],
        "lineage_id": source_lane_value["lineage_id"],
        "lineage_kind": source_lane_value["lineage_kind"],
        "trial_fraction": fraction,
        "event_budget": budget,
        "expiry_epoch": trial_epoch + duration,
        "source_shadow_return_token_digest": source_lane_value["shadow_return_token_digest"],
        "source_rollback_template_digest": source_lane_value["rollback_receipt_template_digest"],
        "observation_copy_enabled": True,
        "automatic_revocation_enabled": True,
        "live_canary_activation_enabled": False,
        "live_response_influence_enabled": False,
        "feedback_to_live_path_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "winner_selected": False,
        "policy_boundary_preserved": True,
    }


def event(
    index: int,
    trial_lane_value: Mapping[str, Any],
    *,
    latency: float = 0.05,
    divergence: float = 0.02,
    bad_redaction: bool = False,
    nondeterministic: bool = False,
    bad_rollback: bool = False,
    bad_revocation: bool = False,
    restore: bool = True,
    live: bool = False,
    activate: bool = False,
) -> dict[str, Any]:
    lane_id = str(trial_lane_value["lane_id"])
    lineage_id = str(trial_lane_value["lineage_id"])
    source_request = sha({"source-request": index})
    redaction = sha({"redaction": index})
    copied = sha(
        {
            "source_request_digest": source_request,
            "redaction_receipt_digest": redaction,
            "lane_id": lane_id,
        }
    )
    output = sha({"trial-output": index, "lane": lane_id})
    rollback = sha({"rollback": index, "lane": lane_id})
    revocation = sha({"revocation": index, "lane": lane_id})
    live_before = sha({"live-response": index})
    return {
        "event_index": index,
        "lane_id": lane_id,
        "lineage_id": lineage_id,
        "source_request_digest": source_request,
        "copied_request_digest": copied,
        "redaction_receipt_digest": redaction,
        "expected_redaction_receipt_digest": sha({"wrong": index}) if bad_redaction else redaction,
        "copy_delivery_digest": sha({"delivery": index}),
        "trial_output_digest": output,
        "replay_output_digest": sha({"different": index}) if nondeterministic else output,
        "rollback_receipt_digest": sha({"bad-rollback": index}) if bad_rollback else rollback,
        "expected_rollback_receipt_digest": rollback,
        "revocation_receipt_digest": sha({"bad-revocation": index}) if bad_revocation else revocation,
        "expected_revocation_receipt_digest": revocation,
        "replica_snapshot_digest": sha({"snapshot": index}),
        "live_response_digest_before": live_before,
        "live_response_digest_after": sha({"changed-live": index}) if live else live_before,
        "latency_delta_ratio": latency,
        "output_divergence_score": divergence,
        "copy_delivered": True,
        "automatic_revocation_executed": not bad_revocation,
        "replica_restored": restore,
        "live_canary_activation_attempted": activate,
        "feedback_to_live_path_attempted": live,
        "external_actuation_attempted": False,
        "world_update_attempted": False,
        "policy_boundary_preserved": True,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    trial_epoch = 1050
    duration = 120
    source_lanes = source["proposal"]["canary_lanes"]
    trial_lanes = [
        trial_lane(source_lanes[0], 0.012, trial_epoch, duration),
        trial_lane(source_lanes[1], 0.009, trial_epoch, duration),
        trial_lane(source_lanes[2], 0.009, trial_epoch, duration),
    ]
    if mode == "fraction":
        trial_lanes[0]["trial_fraction"] = 0.030
    elif mode == "duration":
        duration = 400
        for lane_value in trial_lanes:
            lane_value["expiry_epoch"] = trial_epoch + duration
    elif mode == "budget":
        for lane_value in trial_lanes:
            lane_value["event_budget"] = 15
    elif mode == "missing-minority":
        trial_lanes = trial_lanes[:2]

    if mode == "unfair":
        sequence = [trial_lanes[0]] * 12
    elif mode == "fraction":
        sequence = [trial_lanes[0]] * 8 + [trial_lanes[1]] * 2 + [trial_lanes[2]] * 2
    else:
        sequence = [trial_lanes[index % len(trial_lanes)] for index in range(12)]
    trial_events = [
        event(
            index,
            lane_value,
            latency=0.35 if mode == "latency" and index == 2 else 0.05,
            divergence=0.25 if mode == "divergence" and index == 3 else 0.02,
            bad_redaction=mode == "redaction" and index == 4,
            nondeterministic=mode == "nondeterministic" and index == 5,
            bad_rollback=mode == "rollback" and index == 6,
            bad_revocation=mode == "revocation" and index == 7,
            restore=not (mode == "restore" and index == 8),
            live=mode == "live" and index == 1,
            activate=mode == "activate" and index == 1,
        )
        for index, lane_value in enumerate(sequence, start=1)
    ]
    value = {
        "version": REPORT_VERSION,
        "trial_run_id": plan_value["trial_run_id"],
        "source_canary_proposal_digest": source["proposal"]["bounded_canary_proposal_digest"],
        "observation_copy_trial_started": True,
        "observation_copy_trial_completed": True,
        "raw_payload_stored": False,
        "live_canary_activation_requested": False,
        "live_response_influence_requested": False,
        "trial_epoch": trial_epoch,
        "duration_seconds": duration,
        "total_trial_fraction": round(sum(value["trial_fraction"] for value in trial_lanes), 8),
        "trial_lanes": trial_lanes,
        "trial_events": trial_events,
    }
    value["canary_trial_report_digest"] = report_digest(value)
    return value


def license_value(
    plan_value: Mapping[str, Any],
    report_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["trial_run_id"]),
        "bound_canary_trial_plan_digest": plan_value["canary_trial_plan_digest"],
        "bound_canary_trial_report_digest": report_value["canary_trial_report_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_canary_proposal_digest": source["proposal"]["bounded_canary_proposal_digest"],
        "bound_source_canary_state_digest": source["state"]["bounded_canary_state_digest"],
        "bound_source_canary_recommendation_digest": source["recommendation"][
            "bounded_canary_recommendation_digest"
        ],
        "state_write_allowed": True,
        "summary_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "isolated_observation_copy_trial_allowed": True,
        "live_canary_activation_authority_granted": False,
        "live_response_influence_authority_granted": False,
        "feedback_to_live_path_authority_granted": False,
        "winner_selection_authority_granted": False,
        "external_actuation_authority_granted": False,
        "world_update_authority_granted": False,
        "lineage_selection_authority_granted": False,
        "live_lineage_execution_authority_granted": False,
        "truth_authority_granted": False,
        "direct_promotion_authority_granted": False,
        "direct_rollback_authority_granted": False,
        "direct_quarantine_authority_granted": False,
    }


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_licensed_canary_observation_trial_v0_25_enabled": True,
        "apply_indra_qi_licensed_canary_observation_trial_v0_25": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_bounded_canary_observation_proposal_v0_24.json",
        "indra_qi_bounded_canary_observation_state_v0_24.json",
        "indra_qi_bounded_canary_observation_recommendation_v0_24.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_licensed_canary_observation_trial(
        runtime_context=context(root),
        canary_trial_plan=plan_value,
        canary_trial_license=license_value(plan_value, report_value, source),
        canary_trial_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result
