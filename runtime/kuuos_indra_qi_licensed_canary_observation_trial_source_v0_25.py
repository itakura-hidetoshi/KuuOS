#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_indra_qi_licensed_canary_observation_trial_base_v0_25 import *

def validate_sources(
    world: Mapping[str, Any],
    proposal: Mapping[str, Any],
    source_state: Mapping[str, Any],
    source_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    specs = (
        (world, WORLD_VERSION, "indra_qi_world_state_digest", "world"),
        (proposal, PROPOSAL_VERSION, "bounded_canary_proposal_digest", "proposal"),
        (source_state, SOURCE_STATE_VERSION, "bounded_canary_state_digest", "state"),
        (
            source_recommendation,
            SOURCE_RECOMMENDATION_VERSION,
            "bounded_canary_recommendation_digest",
            "recommendation",
        ),
    )
    for value, version, digest_field, name in specs:
        if value.get("version") != version or not valid_digest(value, digest_field):
            blockers.append(f"canary_trial_source_{name}_invalid")

    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    proposal_digest = str(proposal.get("bounded_canary_proposal_digest", ""))
    state_digest_value = str(source_state.get("bounded_canary_state_digest", ""))
    recommendation_digest = str(source_recommendation.get("bounded_canary_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_digest,
        "expected_canary_proposal_digest": proposal_digest,
        "expected_source_canary_state_digest": state_digest_value,
        "expected_source_canary_recommendation_digest": recommendation_digest,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"canary_trial_{field}_mismatch")

    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id or any(
        value.get("world_model_id") != world_model_id
        for value in (proposal, source_state, source_recommendation)
    ):
        blockers.append("canary_trial_source_world_model_chain_invalid")

    decision = str(source_recommendation.get("decision", ""))
    if (
        proposal.get("source_world_state_digest") != world_digest
        or source_state.get("latest_bounded_canary_proposal_digest") != proposal_digest
        or source_recommendation.get("bounded_canary_proposal_digest") != proposal_digest
        or source_state.get("latest_bounded_canary_decision") != decision
        or source_state.get("last_proposal_run_id") != source_recommendation.get("proposal_run_id")
        or decision not in SOURCE_DECISIONS
    ):
        blockers.append("canary_trial_source_digest_or_decision_chain_invalid")

    if not (
        proposal.get("proposal_only") is True
        and proposal.get("canary_activated") is False
        and proposal.get("live_response_influenced") is False
        and proposal.get("feedback_to_live_path_enabled") is False
        and proposal.get("winner_selected") is False
        and source_recommendation.get("recommendation_only") is True
        and source_recommendation.get("canary_activated") is False
        and source_recommendation.get("live_response_influenced") is False
        and source_recommendation.get("winner_selected") is False
    ):
        blockers.append("canary_trial_source_boundary_invalid")

    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("canary_trial_multi_world_noncollapse_missing")

    lanes: dict[str, dict[str, Any]] = {}
    lineage_ids: set[str] = set()
    for raw in items(proposal.get("canary_lanes")):
        lane = dict(mapping(raw))
        lane_id = str(lane.get("lane_id", ""))
        lineage_id = str(lane.get("lineage_id", ""))
        if not lane_id or lane_id in lanes or not lineage_id or lineage_id in lineage_ids:
            blockers.append("canary_trial_source_lane_ids_invalid")
            continue
        if not (
            lane.get("canary_activation_enabled") is False
            and lane.get("live_response_influence_enabled") is False
            and lane.get("feedback_to_live_path_enabled") is False
            and lane.get("external_actuation_enabled") is False
            and lane.get("world_update_enabled") is False
            and lane.get("winner_selected") is False
            and lane.get("policy_boundary_preserved") is True
            and lane.get("automatic_revocation_enabled") is True
        ):
            blockers.append(f"canary_trial_source_lane_{lane_id}_boundary_invalid")
        lanes[lane_id] = lane
        lineage_ids.add(lineage_id)
    if not lanes:
        blockers.append("canary_trial_source_lanes_missing")

    return {
        "world_digest": world_digest,
        "proposal_digest": proposal_digest,
        "state_digest": state_digest_value,
        "recommendation_digest": recommendation_digest,
        "source_decision": decision,
        "source_proposal_run_id": str(source_recommendation.get("proposal_run_id", "")),
        "proposal_epoch": int(proposal.get("proposal_epoch", 0) or 0),
        "source_duration_seconds": int(proposal.get("duration_seconds", 0) or 0),
        "lanes": lanes,
    }


def validate_license(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    report: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> None:
    expected = {
        "version": LICENSE_VERSION,
        "bound_canary_trial_plan_digest": str(plan.get("canary_trial_plan_digest", "")),
        "bound_canary_trial_report_digest": str(report.get("canary_trial_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_canary_proposal_digest": str(source.get("proposal_digest", "")),
        "bound_source_canary_state_digest": str(source.get("state_digest", "")),
        "bound_source_canary_recommendation_digest": str(source.get("recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"canary_trial_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("canary_trial_license_id_missing")
    for field in (
        "state_write_allowed",
        "summary_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "isolated_observation_copy_trial_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"canary_trial_license_{field}_not_true")
    for field in (
        "live_canary_activation_authority_granted",
        "live_response_influence_authority_granted",
        "feedback_to_live_path_authority_granted",
        "winner_selection_authority_granted",
        "external_actuation_authority_granted",
        "world_update_authority_granted",
        "lineage_selection_authority_granted",
        "live_lineage_execution_authority_granted",
        "truth_authority_granted",
        "direct_promotion_authority_granted",
        "direct_rollback_authority_granted",
        "direct_quarantine_authority_granted",
    ):
        if license_value.get(field) is not False:
            blockers.append(f"canary_trial_license_{field}_not_false")


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("canary_trial_report_version_invalid")
    if report.get("trial_run_id") != plan.get("trial_run_id"):
        blockers.append("canary_trial_report_run_id_mismatch")
    if report.get("source_canary_proposal_digest") != source.get("proposal_digest"):
        blockers.append("canary_trial_report_proposal_digest_mismatch")
    if report.get("canary_trial_report_digest") != report_digest(report):
        blockers.append("canary_trial_report_digest_invalid")
    if report.get("observation_copy_trial_started") is not True:
        blockers.append("canary_trial_not_started")
    if report.get("observation_copy_trial_completed") is not True:
        blockers.append("canary_trial_not_completed")
    if report.get("raw_payload_stored") is not False:
        blockers.append("canary_trial_raw_payload_storage_invalid")
    if report.get("live_canary_activation_requested") is not False:
        blockers.append("canary_trial_live_activation_requested")
    if report.get("live_response_influence_requested") is not False:
        blockers.append("canary_trial_live_response_influence_requested")

    trial_epoch = report.get("trial_epoch")
    duration = report.get("duration_seconds")
    total_fraction = report.get("total_trial_fraction")
    if isinstance(trial_epoch, bool) or not isinstance(trial_epoch, int) or trial_epoch < 0:
        blockers.append("canary_trial_epoch_invalid")
    if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
        blockers.append("canary_trial_duration_invalid")
    if isinstance(total_fraction, bool) or not isinstance(total_fraction, (int, float)) or not 0 < float(total_fraction) <= 1:
        blockers.append("canary_trial_total_fraction_invalid")

    source_lanes = mapping(source.get("lanes"))
    trial_lanes = [dict(mapping(value)) for value in items(report.get("trial_lanes"))]
    if not trial_lanes:
        blockers.append("canary_trial_lanes_missing")
    seen_lane_ids: set[str] = set()
    for index, lane in enumerate(trial_lanes):
        lane_id = str(lane.get("lane_id", ""))
        source_lane = mapping(source_lanes.get(lane_id))
        if not lane_id or lane_id in seen_lane_ids or not source_lane:
            blockers.append(f"canary_trial_lane_{index}_source_binding_invalid")
            continue
        seen_lane_ids.add(lane_id)
        if lane.get("lineage_id") != source_lane.get("lineage_id") or lane.get("lineage_kind") != source_lane.get("lineage_kind"):
            blockers.append(f"canary_trial_lane_{index}_lineage_binding_invalid")
        fraction = lane.get("trial_fraction")
        budget = lane.get("event_budget")
        expiry = lane.get("expiry_epoch")
        if isinstance(fraction, bool) or not isinstance(fraction, (int, float)) or not 0 < float(fraction) <= 1:
            blockers.append(f"canary_trial_lane_{index}_fraction_invalid")
        if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
            blockers.append(f"canary_trial_lane_{index}_budget_invalid")
        if isinstance(expiry, bool) or not isinstance(expiry, int):
            blockers.append(f"canary_trial_lane_{index}_expiry_invalid")
        if lane.get("source_shadow_return_token_digest") != source_lane.get("shadow_return_token_digest"):
            blockers.append(f"canary_trial_lane_{index}_return_token_mismatch")
        if lane.get("source_rollback_template_digest") != source_lane.get("rollback_receipt_template_digest"):
            blockers.append(f"canary_trial_lane_{index}_rollback_template_mismatch")
        for field in (
            "observation_copy_enabled",
            "automatic_revocation_enabled",
            "live_canary_activation_enabled",
            "live_response_influence_enabled",
            "feedback_to_live_path_enabled",
            "external_actuation_enabled",
            "world_update_enabled",
            "winner_selected",
            "policy_boundary_preserved",
        ):
            if not isinstance(lane.get(field), bool):
                blockers.append(f"canary_trial_lane_{index}_{field}_invalid")

    events = [dict(mapping(value)) for value in items(report.get("trial_events"))]
    if not events:
        blockers.append("canary_trial_events_missing")
        return trial_lanes, events
    seen_indices: set[int] = set()
    trial_lane_map = {str(lane.get("lane_id", "")): lane for lane in trial_lanes}
    for index, event in enumerate(events):
        event_index = event.get("event_index")
        lane_id = str(event.get("lane_id", ""))
        trial_lane = mapping(trial_lane_map.get(lane_id))
        if (
            isinstance(event_index, bool)
            or not isinstance(event_index, int)
            or event_index <= 0
            or event_index in seen_indices
        ):
            blockers.append(f"canary_trial_event_{index}_index_invalid")
        if isinstance(event_index, int) and not isinstance(event_index, bool):
            seen_indices.add(event_index)
        if not trial_lane or event.get("lineage_id") != trial_lane.get("lineage_id"):
            blockers.append(f"canary_trial_event_{index}_lane_binding_invalid")
        source_request = str(event.get("source_request_digest", ""))
        redaction = str(event.get("redaction_receipt_digest", ""))
        expected_copy = sha(
            {
                "source_request_digest": source_request,
                "redaction_receipt_digest": redaction,
                "lane_id": lane_id,
            }
        )
        if event.get("copied_request_digest") != expected_copy:
            blockers.append(f"canary_trial_event_{index}_copy_binding_invalid")
        for field in (
            "source_request_digest",
            "copied_request_digest",
            "redaction_receipt_digest",
            "expected_redaction_receipt_digest",
            "copy_delivery_digest",
            "trial_output_digest",
            "replay_output_digest",
            "rollback_receipt_digest",
            "expected_rollback_receipt_digest",
            "revocation_receipt_digest",
            "expected_revocation_receipt_digest",
            "replica_snapshot_digest",
            "live_response_digest_before",
            "live_response_digest_after",
        ):
            if not str(event.get(field, "")):
                blockers.append(f"canary_trial_event_{index}_{field}_missing")
        for field in ("latency_delta_ratio", "output_divergence_score"):
            value = event.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
                blockers.append(f"canary_trial_event_{index}_{field}_invalid")
        for field in (
            "copy_delivered",
            "automatic_revocation_executed",
            "replica_restored",
            "live_canary_activation_attempted",
            "feedback_to_live_path_attempted",
            "external_actuation_attempted",
            "world_update_attempted",
            "policy_boundary_preserved",
        ):
            if not isinstance(event.get(field), bool):
                blockers.append(f"canary_trial_event_{index}_{field}_invalid")
    return trial_lanes, events
