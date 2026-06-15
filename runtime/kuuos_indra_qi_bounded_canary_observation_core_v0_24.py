#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_bounded_canary_observation_plan_v0_24"
LICENSE_VERSION = "indra_qi_bounded_canary_observation_license_v0_24"
REPORT_VERSION = "indra_qi_bounded_canary_observation_report_v0_24"
STATE_VERSION = "indra_qi_bounded_canary_observation_state_v0_24"
LEDGER_VERSION = "indra_qi_bounded_canary_observation_ledger_record_v0_24"
WORLD_VERSION = "indra_qi_world_model_v0_1"
SUMMARY_VERSION = "indra_qi_longitudinal_mirror_noninterference_summary_v0_23"
SOURCE_STATE_VERSION = "indra_qi_longitudinal_mirror_noninterference_state_v0_23"
SOURCE_RECOMMENDATION_VERSION = "indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23"
VERSION = "indra_qi_bounded_canary_observation_v0_24"
READY = "INDRA_QI_BOUNDED_CANARY_OBSERVATION_V0_24_READY"
BLOCKED = "INDRA_QI_BOUNDED_CANARY_OBSERVATION_V0_24_BLOCKED"

SOURCE_DECISIONS = {
    "hold_for_observation",
    "longitudinal_mirror_noninterference_ready",
    "extend_mirror_observation_recommended",
    "redesign_longitudinal_mirror_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "bounded_canary_observation_proposal_ready",
    "redesign_bounded_canary_observation_proposal_recommended",
    "extend_mirror_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_23_summary_required": True,
    "source_v0_23_digest_chain_exact": True,
    "world_source_read_only": True,
    "longitudinal_source_read_only": True,
    "proposal_only": True,
    "canary_activation_forbidden": True,
    "canary_fraction_bounded": True,
    "canary_duration_bounded": True,
    "canary_event_budget_bounded": True,
    "automatic_revocation_required": True,
    "expiry_epoch_required": True,
    "shadow_return_material_required": True,
    "rollback_receipt_template_required": True,
    "latency_guardrail_required": True,
    "output_divergence_guardrail_required": True,
    "fairness_guardrail_required": True,
    "recovery_lane_preserved": True,
    "minority_lane_preserved": True,
    "live_response_influence_forbidden": True,
    "feedback_to_live_path_forbidden": True,
    "external_actuation_disabled": True,
    "world_update_disabled": True,
    "winner_selection_forbidden": True,
    "candidate_weighting_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_lineage_selection_authority": True,
    "not_lineage_execution_authority": True,
    "not_canary_activation_authority": True,
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


def sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    output = dict(value)
    output.pop(field, None)
    return output


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "bounded_canary_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "bounded_canary_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "bounded_canary_state_digest"))


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
            blockers.append(f"bounded_canary_policy_{field}_invalid")


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str]) -> None:
    for field in fields:
        value = policy.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            blockers.append(f"bounded_canary_policy_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("bounded_canary_plan_version_invalid")
    if plan.get("bounded_canary_plan_digest") != plan_digest(plan):
        blockers.append("bounded_canary_plan_digest_invalid")
    for field in (
        "proposal_program_id",
        "proposal_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_longitudinal_summary_digest",
        "expected_source_longitudinal_state_digest",
        "expected_source_longitudinal_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"bounded_canary_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"bounded_canary_boundary_{field}_mismatch")
    policy = mapping(plan.get("canary_policy"))
    _positive_int(
        policy,
        (
            "minimum_canary_lanes",
            "maximum_canary_lanes",
            "minimum_recovery_lanes",
            "minimum_minority_lanes",
            "maximum_duration_seconds",
            "maximum_event_budget",
            "maximum_event_budget_per_lane",
        ),
        blockers,
    )
    low = policy.get("minimum_canary_lanes")
    high = policy.get("maximum_canary_lanes")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 8):
        blockers.append("bounded_canary_lane_count_bounds_invalid")
    _bounded(
        policy,
        (
            "maximum_total_canary_fraction",
            "maximum_single_lane_fraction",
            "maximum_latency_guardrail_ratio",
            "maximum_output_divergence_guardrail",
            "minimum_fairness_guardrail_ratio",
        ),
        blockers,
    )
    for field in (
        "require_expiry_epoch",
        "require_automatic_revocation",
        "require_shadow_return_token",
        "require_rollback_receipt",
        "require_proposal_only",
        "require_canary_activation_disabled",
        "require_live_response_influence_disabled",
        "require_feedback_to_live_path_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"bounded_canary_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    summary: Mapping[str, Any],
    source_state: Mapping[str, Any],
    source_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    specs = (
        (world, WORLD_VERSION, "indra_qi_world_state_digest", "world"),
        (summary, SUMMARY_VERSION, "longitudinal_mirror_summary_digest", "summary"),
        (source_state, SOURCE_STATE_VERSION, "longitudinal_mirror_state_digest", "state"),
        (
            source_recommendation,
            SOURCE_RECOMMENDATION_VERSION,
            "longitudinal_mirror_recommendation_digest",
            "recommendation",
        ),
    )
    for value, version, digest_field, name in specs:
        if value.get("version") != version or not valid_digest(value, digest_field):
            blockers.append(f"bounded_canary_source_{name}_invalid")
    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    summary_digest = str(summary.get("longitudinal_mirror_summary_digest", ""))
    state_digest_value = str(source_state.get("longitudinal_mirror_state_digest", ""))
    recommendation_digest = str(source_recommendation.get("longitudinal_mirror_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_digest,
        "expected_longitudinal_summary_digest": summary_digest,
        "expected_source_longitudinal_state_digest": state_digest_value,
        "expected_source_longitudinal_recommendation_digest": recommendation_digest,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"bounded_canary_{field}_mismatch")
    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id or any(
        value.get("world_model_id") != world_model_id
        for value in (summary, source_state, source_recommendation)
    ):
        blockers.append("bounded_canary_source_world_model_chain_invalid")
    decision = str(source_recommendation.get("decision", ""))
    if (
        summary.get("source_world_state_digest") != world_digest
        or source_state.get("latest_longitudinal_mirror_summary_digest") != summary_digest
        or source_recommendation.get("longitudinal_mirror_summary_digest") != summary_digest
        or source_state.get("latest_longitudinal_mirror_decision") != decision
        or source_state.get("last_evidence_run_id") != source_recommendation.get("evidence_run_id")
        or decision not in SOURCE_DECISIONS
    ):
        blockers.append("bounded_canary_source_digest_or_decision_chain_invalid")
    if not (
        summary.get("raw_payload_stored") is False
        and summary.get("live_response_influenced") is False
        and summary.get("feedback_to_live_path_enabled") is False
        and summary.get("routing_activated") is False
        and summary.get("winner_selected") is False
        and source_recommendation.get("recommendation_only") is True
        and source_recommendation.get("live_response_influenced") is False
        and source_recommendation.get("routing_activated") is False
        and source_recommendation.get("winner_selected") is False
    ):
        blockers.append("bounded_canary_source_boundary_invalid")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("bounded_canary_multi_world_noncollapse_missing")
    return {
        "world_digest": world_digest,
        "summary_digest": summary_digest,
        "state_digest": state_digest_value,
        "recommendation_digest": recommendation_digest,
        "source_decision": decision,
        "source_evidence_run_id": str(source_recommendation.get("evidence_run_id", "")),
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
        "bound_bounded_canary_plan_digest": str(plan.get("bounded_canary_plan_digest", "")),
        "bound_bounded_canary_report_digest": str(report.get("bounded_canary_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_longitudinal_summary_digest": str(source.get("summary_digest", "")),
        "bound_source_longitudinal_state_digest": str(source.get("state_digest", "")),
        "bound_source_longitudinal_recommendation_digest": str(source.get("recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"bounded_canary_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("bounded_canary_license_id_missing")
    for field in (
        "state_write_allowed",
        "proposal_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"bounded_canary_license_{field}_not_true")
    for field in (
        "canary_activation_authority_granted",
        "live_response_influence_authority_granted",
        "feedback_to_live_path_authority_granted",
        "winner_selection_authority_granted",
        "external_actuation_authority_granted",
        "world_update_authority_granted",
        "lineage_selection_authority_granted",
        "lineage_execution_authority_granted",
        "truth_authority_granted",
        "direct_promotion_authority_granted",
        "direct_rollback_authority_granted",
        "direct_quarantine_authority_granted",
    ):
        if license_value.get(field) is not False:
            blockers.append(f"bounded_canary_license_{field}_not_false")


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("bounded_canary_report_version_invalid")
    if report.get("proposal_run_id") != plan.get("proposal_run_id"):
        blockers.append("bounded_canary_report_run_id_mismatch")
    if report.get("source_longitudinal_summary_digest") != source.get("summary_digest"):
        blockers.append("bounded_canary_report_summary_digest_mismatch")
    if report.get("bounded_canary_report_digest") != report_digest(report):
        blockers.append("bounded_canary_report_digest_invalid")
    if report.get("proposal_only") is not True:
        blockers.append("bounded_canary_report_not_proposal_only")
    if report.get("canary_activation_requested") is not False:
        blockers.append("bounded_canary_report_activation_requested")
    duration = report.get("duration_seconds")
    proposal_epoch = report.get("proposal_epoch")
    if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
        blockers.append("bounded_canary_report_duration_invalid")
    if isinstance(proposal_epoch, bool) or not isinstance(proposal_epoch, int) or proposal_epoch < 0:
        blockers.append("bounded_canary_report_proposal_epoch_invalid")
    lanes = [dict(mapping(value)) for value in items(report.get("canary_lanes"))]
    if not lanes:
        blockers.append("bounded_canary_lanes_missing")
        return lanes
    seen_lane_ids: set[str] = set()
    seen_lineage_ids: set[str] = set()
    for index, lane in enumerate(lanes):
        lane_id = str(lane.get("lane_id", ""))
        lineage_id = str(lane.get("lineage_id", ""))
        if not lane_id or lane_id in seen_lane_ids:
            blockers.append(f"bounded_canary_lane_{index}_lane_id_invalid")
        if not lineage_id or lineage_id in seen_lineage_ids:
            blockers.append(f"bounded_canary_lane_{index}_lineage_id_invalid")
        seen_lane_ids.add(lane_id)
        seen_lineage_ids.add(lineage_id)
        if not str(lane.get("lineage_kind", "")):
            blockers.append(f"bounded_canary_lane_{index}_lineage_kind_missing")
        fraction = lane.get("canary_fraction")
        budget = lane.get("event_budget")
        expiry = lane.get("expiry_epoch")
        if isinstance(fraction, bool) or not isinstance(fraction, (int, float)) or not 0 < float(fraction) <= 1:
            blockers.append(f"bounded_canary_lane_{index}_fraction_invalid")
        if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
            blockers.append(f"bounded_canary_lane_{index}_budget_invalid")
        if isinstance(expiry, bool) or not isinstance(expiry, int):
            blockers.append(f"bounded_canary_lane_{index}_expiry_invalid")
        for field in ("shadow_return_token_digest", "rollback_receipt_template_digest"):
            if not str(lane.get(field, "")):
                blockers.append(f"bounded_canary_lane_{index}_{field}_missing")
        for field in (
            "latency_guardrail_ratio",
            "output_divergence_guardrail",
            "fairness_guardrail_ratio",
        ):
            value = lane.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
                blockers.append(f"bounded_canary_lane_{index}_{field}_invalid")
        for field in (
            "automatic_revocation_enabled",
            "canary_activation_enabled",
            "live_response_influence_enabled",
            "feedback_to_live_path_enabled",
            "external_actuation_enabled",
            "world_update_enabled",
            "winner_selected",
            "policy_boundary_preserved",
        ):
            if not isinstance(lane.get(field), bool):
                blockers.append(f"bounded_canary_lane_{index}_{field}_invalid")
    return lanes


def analyze_proposal(
    lanes: Sequence[Mapping[str, Any]],
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("canary_policy"))
    proposal_epoch = int(report.get("proposal_epoch", 0) or 0)
    lane_count = len(lanes)
    total_fraction = sum(max(number(lane.get("canary_fraction")), 0.0) for lane in lanes)
    max_fraction = max((number(lane.get("canary_fraction")) for lane in lanes), default=1.0)
    total_budget = sum(int(lane.get("event_budget", 0) or 0) for lane in lanes)
    recovery_count = sum(str(lane.get("lineage_kind", "")) == "recovery" for lane in lanes)
    minority_count = sum(str(lane.get("lineage_kind", "")) == "minority_preservation" for lane in lanes)
    durations: list[int] = []
    boundary_breaches = 0
    auto_revoke = True
    return_material = True
    rollback_material = True
    per_lane_budget = True
    latency_guardrails = True
    divergence_guardrails = True
    fairness_guardrails = True
    enriched: list[dict[str, Any]] = []
    for raw in lanes:
        lane = dict(raw)
        expiry = int(lane.get("expiry_epoch", proposal_epoch) or proposal_epoch)
        duration = expiry - proposal_epoch
        durations.append(duration)
        auto_revoke = auto_revoke and lane.get("automatic_revocation_enabled") is True
        return_material = return_material and bool(lane.get("shadow_return_token_digest"))
        rollback_material = rollback_material and bool(lane.get("rollback_receipt_template_digest"))
        per_lane_budget = per_lane_budget and int(lane.get("event_budget", 0) or 0) <= int(
            policy.get("maximum_event_budget_per_lane", 0)
        )
        latency_guardrails = latency_guardrails and number(lane.get("latency_guardrail_ratio"), 1.0) <= number(
            policy.get("maximum_latency_guardrail_ratio")
        )
        divergence_guardrails = divergence_guardrails and number(
            lane.get("output_divergence_guardrail"), 1.0
        ) <= number(policy.get("maximum_output_divergence_guardrail"))
        fairness_guardrails = fairness_guardrails and number(lane.get("fairness_guardrail_ratio")) >= number(
            policy.get("minimum_fairness_guardrail_ratio")
        )
        boundary_ok = (
            lane.get("canary_activation_enabled") is False
            and lane.get("live_response_influence_enabled") is False
            and lane.get("feedback_to_live_path_enabled") is False
            and lane.get("external_actuation_enabled") is False
            and lane.get("world_update_enabled") is False
            and lane.get("winner_selected") is False
            and lane.get("policy_boundary_preserved") is True
        )
        boundary_breaches += not boundary_ok
        lane["duration_seconds"] = duration
        lane["proposal_boundary_preserved"] = boundary_ok
        enriched.append(lane)
    diversity_gates = {
        "minimum_plural_lanes_present": lane_count >= int(policy.get("minimum_canary_lanes", 0)),
        "recovery_lane_preserved": recovery_count >= int(policy.get("minimum_recovery_lanes", 0)),
        "minority_lane_preserved": minority_count >= int(policy.get("minimum_minority_lanes", 0)),
    }
    proposal_gates = {
        "maximum_lane_count_bounded": lane_count <= int(policy.get("maximum_canary_lanes", 0)),
        "total_canary_fraction_bounded": total_fraction <= number(policy.get("maximum_total_canary_fraction")),
        "single_lane_fraction_bounded": max_fraction <= number(policy.get("maximum_single_lane_fraction")),
        "reported_duration_bounded": int(report.get("duration_seconds", 0) or 0)
        <= int(policy.get("maximum_duration_seconds", 0)),
        "lane_expiry_duration_bounded": bool(durations)
        and all(0 < value <= int(policy.get("maximum_duration_seconds", 0)) for value in durations),
        "total_event_budget_bounded": total_budget <= int(policy.get("maximum_event_budget", 0)),
        "per_lane_event_budget_bounded": per_lane_budget,
        "automatic_revocation_complete": auto_revoke,
        "shadow_return_material_complete": return_material,
        "rollback_receipt_templates_complete": rollback_material,
        "latency_guardrails_bounded": latency_guardrails,
        "output_divergence_guardrails_bounded": divergence_guardrails,
        "fairness_guardrails_sufficient": fairness_guardrails,
        "proposal_only": report.get("proposal_only") is True,
        "canary_activation_not_requested": report.get("canary_activation_requested") is False,
        "proposal_boundary_preserved": boundary_breaches == 0,
    }
    return {
        "lane_count": lane_count,
        "canary_lanes": enriched,
        "total_canary_fraction": round(total_fraction, 8),
        "maximum_single_lane_fraction": round(max_fraction, 8),
        "total_event_budget": total_budget,
        "maximum_lane_duration_seconds": max(durations, default=0),
        "recovery_lane_count": recovery_count,
        "minority_lane_count": minority_count,
        "boundary_breach_count": boundary_breaches,
        "diversity_gates": diversity_gates,
        "proposal_gates": proposal_gates,
        "all_gates": {**diversity_gates, **proposal_gates},
    }


def evaluate_proposal(analysis: Mapping[str, Any], source_decision: str) -> tuple[str, str]:
    diversity = mapping(analysis.get("diversity_gates"))
    proposal = mapping(analysis.get("proposal_gates"))
    if source_decision in {"quarantine_recommended", "rollback_recommended", "hold_for_observation"}:
        return source_decision, f"source_v0_23_{source_decision}"
    if int(analysis.get("boundary_breach_count", 0)) > 0:
        return "quarantine_recommended", "canary_activation_or_live_intervention_boundary_breach"
    if source_decision == "extend_mirror_observation_recommended":
        return source_decision, "source_v0_23_more_mirror_evidence_required"
    if source_decision == "restore_shadow_diversity_recommended":
        return source_decision, "source_v0_23_shadow_diversity_restoration_required"
    if source_decision == "redesign_longitudinal_mirror_observation_recommended":
        return (
            "redesign_bounded_canary_observation_proposal_recommended",
            "source_v0_23_longitudinal_mirror_redesign_required",
        )
    if source_decision == "longitudinal_mirror_noninterference_ready" and not all(
        value is True for value in diversity.values()
    ):
        return "restore_shadow_diversity_recommended", "canary_lane_diversity_gates_failed"
    if source_decision == "longitudinal_mirror_noninterference_ready" and all(
        value is True for value in proposal.values()
    ):
        return "bounded_canary_observation_proposal_ready", "bounded_disabled_revocable_canary_proposal_ready"
    if source_decision == "longitudinal_mirror_noninterference_ready":
        return (
            "redesign_bounded_canary_observation_proposal_recommended",
            "canary_fraction_duration_budget_or_guardrail_gate_failed",
        )
    return "quarantine_recommended", "unknown_source_v0_23_decision"


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    proposal_program_id: str
    proposal_run_id: str
    world_model_id: str
    source_longitudinal_decision: str
    decision: str
    recommendation_only: bool
    canary_activated: bool
    source_world_state_digest: str
    source_longitudinal_summary_digest: str
    source_longitudinal_state_digest: str
    source_longitudinal_recommendation_digest: str
    bounded_canary_report_digest: str
    bounded_canary_state_digest: str
    ledger_record_digest: str
    blockers: list[str]


def validate_ledger(
    records: list[dict[str, Any]],
    program_id: str,
    world_model_id: str,
    blockers: list[str],
) -> list[dict[str, Any]]:
    previous = "GENESIS"
    runs: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    reports: set[str] = set()
    for index, record in enumerate(records):
        run_id = str(record.get("proposal_run_id", ""))
        pair = (
            str(record.get("source_longitudinal_summary_digest", "")),
            str(record.get("source_longitudinal_recommendation_digest", "")),
        )
        report_sha = str(record.get("bounded_canary_report_digest", ""))
        valid = (
            record.get("version") == LEDGER_VERSION
            and valid_digest(record, "record_digest")
            and record.get("prev_record_digest") == previous
            and record.get("proposal_program_id") == program_id
            and record.get("world_model_id") == world_model_id
            and bool(run_id)
            and run_id not in runs
            and all(pair)
            and pair not in pairs
            and bool(report_sha)
            and report_sha not in reports
        )
        if record.get("_invalid") or not valid:
            blockers.append(f"bounded_canary_ledger_record_{index}_invalid")
        runs.add(run_id)
        pairs.add(pair)
        reports.add(report_sha)
        previous = str(record.get("record_digest", ""))
    return records


def build_bounded_canary_observation(
    *,
    runtime_context: Mapping[str, Any],
    bounded_canary_plan: Mapping[str, Any],
    bounded_canary_license: Mapping[str, Any],
    bounded_canary_report: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(bounded_canary_plan))
    license_value = mapping(bounded_canary_license)
    report = dict(mapping(bounded_canary_report))
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_bounded_canary_observation_v0_24_enabled") is not True:
        blockers.append("bounded_canary_enabled_not_true")
    if context.get("apply_indra_qi_bounded_canary_observation_v0_24") is not True:
        blockers.append("bounded_canary_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    summary = read_json(root / "indra_qi_longitudinal_mirror_noninterference_summary_v0_23.json")
    source_state = read_json(root / "indra_qi_longitudinal_mirror_noninterference_state_v0_23.json")
    source_recommendation = read_json(
        root / "indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23.json"
    )
    source = validate_sources(world, summary, source_state, source_recommendation, plan, blockers)
    lanes = validate_report(report, plan, source, blockers)
    validate_license(license_value, plan, report, source, blockers)

    program_id = str(plan.get("proposal_program_id", ""))
    run_id = str(plan.get("proposal_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_bounded_canary_observation_ledger_v0_24.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), program_id, world_model_id, blockers)
    pair = (str(source.get("summary_digest", "")), str(source.get("recommendation_digest", "")))
    report_sha = str(report.get("bounded_canary_report_digest", ""))
    if any(
        record.get("proposal_run_id") == run_id
        or (
            record.get("source_longitudinal_summary_digest"),
            record.get("source_longitudinal_recommendation_digest"),
        )
        == pair
        or record.get("bounded_canary_report_digest") == report_sha
        for record in prior
    ):
        blockers.append("bounded_canary_replay_detected")

    prior_state = read_json(root / "indra_qi_bounded_canary_observation_state_v0_24.json")
    if prior_state and not valid_digest(prior_state, "bounded_canary_state_digest"):
        blockers.append("bounded_canary_prior_state_digest_invalid")
    if prior_state and prior_state.get("last_source_longitudinal_state_digest") == source.get("state_digest"):
        blockers.append("bounded_canary_source_longitudinal_state_not_advanced")

    analysis = analyze_proposal(lanes, report, plan)
    decision, reason = evaluate_proposal(analysis, str(source.get("source_decision", "")))
    if decision not in DECISIONS:
        blockers.append("bounded_canary_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        reason = "fail_closed_on_validation_or_integrity_loss"

    now = int(time.time())
    source_fields = {
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_longitudinal_summary_digest": str(source.get("summary_digest", "")),
        "source_longitudinal_state_digest": str(source.get("state_digest", "")),
        "source_longitudinal_recommendation_digest": str(source.get("recommendation_digest", "")),
        "bounded_canary_report_digest": report_sha,
    }
    proposal = {
        "version": "indra_qi_bounded_canary_observation_proposal_v0_24",
        "proposal_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        **source_fields,
        "proposal_epoch": report.get("proposal_epoch"),
        "duration_seconds": report.get("duration_seconds"),
        "canary_lanes": analysis.get("canary_lanes", []),
        "proposal_analysis": {key: value for key, value in analysis.items() if key != "canary_lanes"},
        "proposal_only": True,
        "canary_activated": False,
        "live_response_influenced": False,
        "feedback_to_live_path_enabled": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": now,
    }
    proposal["bounded_canary_proposal_digest"] = sha(proposal)
    authority = {
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
    }
    recommendation = {
        "version": "indra_qi_bounded_canary_observation_recommendation_v0_24",
        "proposal_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "decision_reasons": [reason],
        "proposal_ready": decision == "bounded_canary_observation_proposal_ready",
        "canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "bounded_canary_proposal_digest": proposal["bounded_canary_proposal_digest"],
        "proposal_analysis": {key: value for key, value in analysis.items() if key != "canary_lanes"},
        **source_fields,
        "recommendation_only": True,
        "proposal_not_canary_activation": True,
        **authority,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["bounded_canary_recommendation_digest"] = sha(recommendation)
    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "bounded_canary_observation_proposal",
        "proposal_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "source_evidence_run_id": str(source.get("source_evidence_run_id", "")),
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        "bounded_canary_proposal_digest": proposal["bounded_canary_proposal_digest"],
        "proposal_analysis": {key: value for key, value in analysis.items() if key != "canary_lanes"},
        "decision": decision,
        "canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_files_unchanged": True,
            "no_canary_activated": True,
            "no_live_response_influence": True,
            "no_feedback_to_live_path": True,
            "no_winner_selected": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)
    state = {
        "version": STATE_VERSION,
        "proposal_program_id": program_id,
        "world_model_id": world_model_id,
        "last_proposal_run_id": run_id,
        "last_source_world_state_digest": source_fields["source_world_state_digest"],
        "last_source_longitudinal_summary_digest": source_fields["source_longitudinal_summary_digest"],
        "last_source_longitudinal_state_digest": source_fields["source_longitudinal_state_digest"],
        "last_source_longitudinal_recommendation_digest": source_fields[
            "source_longitudinal_recommendation_digest"
        ],
        "last_bounded_canary_report_digest": report_sha,
        "latest_source_longitudinal_decision": str(source.get("source_decision", "")),
        "latest_bounded_canary_decision": decision,
        "latest_bounded_canary_proposal_digest": proposal["bounded_canary_proposal_digest"],
        "latest_proposal_analysis": {key: value for key, value in analysis.items() if key != "canary_lanes"},
        "latest_bounded_canary_record_digest": ledger["record_digest"],
        "prev_bounded_canary_state_digest": str(prior_state.get("bounded_canary_state_digest", "GENESIS"))
        if prior_state
        else "GENESIS",
        "boundary": {
            "bounded_canary_state_only": True,
            "proposal_not_canary_activation": True,
            "canary_activated": False,
            "live_response_influenced": False,
            "feedback_to_live_path_enabled": False,
            "winner_selected": False,
            "recommendation_only": True,
            "multi_world_noncollapse_preserved": True,
        },
        "epoch": now,
    }
    state["bounded_canary_state_digest"] = state_digest(state)
    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "proposal_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "recommendation_only": True,
        **source_fields,
        "bounded_canary_proposal_digest": proposal["bounded_canary_proposal_digest"] if not blockers else "",
        "bounded_canary_state_digest": state["bounded_canary_state_digest"]
        if not blockers
        else str(prior_state.get("bounded_canary_state_digest", "")),
        "ledger_record_digest": ledger["record_digest"] if not blockers else "",
        "blockers": blockers,
        "boundary": {**REQUIRED_BOUNDARY, "bounded_canary_proposal_committed": not blockers},
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-bounded-canary-observation-" + sha(receipt)[:16]
    if not blockers:
        write_json(root / "indra_qi_bounded_canary_observation_proposal_v0_24.json", proposal)
        write_json(root / "indra_qi_bounded_canary_observation_recommendation_v0_24.json", recommendation)
        write_json(root / "indra_qi_bounded_canary_observation_state_v0_24.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_bounded_canary_observation_receipt_v0_24.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_bounded_canary_observation_audit_v0_24.jsonl",
            {**receipt, "audit_record_digest": sha(receipt)},
        )
    return Result(
        VERSION,
        status,
        str(receipt["packet_id"]),
        str(root),
        program_id,
        run_id,
        world_model_id,
        str(source.get("source_decision", "")),
        decision,
        True,
        False,
        source_fields["source_world_state_digest"],
        source_fields["source_longitudinal_summary_digest"],
        source_fields["source_longitudinal_state_digest"],
        source_fields["source_longitudinal_recommendation_digest"],
        report_sha,
        state["bounded_canary_state_digest"]
        if not blockers
        else str(prior_state.get("bounded_canary_state_digest", "")),
        ledger["record_digest"] if not blockers else "",
        blockers,
    )
