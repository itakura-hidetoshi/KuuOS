#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_generational_governance_plan_v0_13"
LICENSE_VERSION = "indra_qi_generational_governance_license_v0_13"
REPLAY_VERSION = "indra_qi_generational_replay_report_v0_13"
STATE_VERSION = "indra_qi_generational_governance_state_v0_13"
LEDGER_VERSION = "indra_qi_generational_governance_ledger_record_v0_13"
DECISIONS = {"hold_for_observation", "promote_bounded", "rollback_recommended", "quarantine_recommended"}
METRICS = ("maximum_observation_debt", "minimum_recoverability_reserve", "maximum_intervention_residue")
REQUIRED_BOUNDARY = {
    "source_v0_12_artifacts_required": True,
    "source_v0_12_digest_chain_exact": True,
    "multi_generation_window_bounded": True,
    "generation_index_monotone": True,
    "replay_required_for_promotion": True,
    "drift_bounded_for_promotion": True,
    "collapse_pressure_bounded_for_promotion": True,
    "quarantine_on_integrity_failure": True,
    "rollback_is_recommendation_only": True,
    "promotion_is_recommendation_only": True,
    "quarantine_is_recommendation_only": True,
    "candidate_weighting_not_truth": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "not_truth_authority": True,
    "not_external_world_actuation_authority": True,
    "not_unlicensed_execution_authority": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def number(value: Any, default: float = 0.0) -> float:
    return default if isinstance(value, bool) or not isinstance(value, (int, float)) else float(value)


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    return bool(value.get(field)) and str(value[field]) == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "governance_plan_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "governance_state_digest"))


def replay_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "replay_report_digest"))


def metrics(value: Mapping[str, Any]) -> dict[str, Any]:
    count = value.get("state_count")
    return {
        "state_count": count if isinstance(count, int) and not isinstance(count, bool) and count >= 0 else 0,
        "maximum_observation_debt": clamp(number(value.get("maximum_observation_debt"), 1.0)),
        "minimum_recoverability_reserve": clamp(number(value.get("minimum_recoverability_reserve"), 0.0)),
        "maximum_intervention_residue": clamp(number(value.get("maximum_intervention_residue"), 1.0)),
    }


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("generational_governance_plan_version_invalid")
    if str(plan.get("governance_plan_digest", "")) != plan_digest(plan):
        blockers.append("generational_governance_plan_digest_invalid")
    for field in ("monitor_id", "review_run_id", "runner_id", "expected_source_v0_12_runner_state_digest"):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"generational_governance_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"generational_governance_boundary_{field}_mismatch")
    policy = mapping(plan.get("governance_policy"))
    for field in ("minimum_window_generations", "maximum_window_generations", "minimum_replay_cases", "quarantine_consecutive_regressions"):
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw <= 0:
            blockers.append(f"generational_governance_policy_{field}_invalid")
    raw = policy.get("maximum_regression_steps")
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
        blockers.append("generational_governance_policy_maximum_regression_steps_invalid")
    _bounded(policy, ("minimum_replay_pass_ratio", "maximum_observation_debt_drift", "maximum_intervention_residue_drift", "maximum_recoverability_loss", "regression_epsilon", "maximum_collapse_pressure", "quarantine_collapse_pressure"), blockers, "generational_governance_policy")
    low, high = policy.get("minimum_window_generations"), policy.get("maximum_window_generations")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 32):
        blockers.append("generational_governance_window_bounds_invalid")
    if number(policy.get("maximum_collapse_pressure"), 1) >= number(policy.get("quarantine_collapse_pressure")):
        blockers.append("generational_governance_collapse_threshold_order_invalid")
    weights = mapping(policy.get("collapse_weights"))
    _bounded(weights, ("observation_debt", "recoverability_loss", "intervention_residue"), blockers, "generational_governance_collapse_weights")
    if abs(sum(number(weights.get(k)) for k in ("observation_debt", "recoverability_loss", "intervention_residue")) - 1) > 1e-8:
        blockers.append("generational_governance_collapse_weights_sum_invalid")


def validate_license(value: Mapping[str, Any], plan: Mapping[str, Any], state_sha: str, handoff_sha: str, blockers: list[str]) -> None:
    checks = {
        "version": LICENSE_VERSION,
        "bound_governance_plan_digest": str(plan.get("governance_plan_digest", "")),
        "bound_source_v0_12_runner_state_digest": state_sha,
        "bound_source_generation_handoff_digest": handoff_sha,
    }
    for field, expected in checks.items():
        if value.get(field) != expected:
            blockers.append(f"generational_governance_license_{field}_mismatch")
    if not str(value.get("license_id", "")):
        blockers.append("generational_governance_license_id_missing")
    for field in ("state_write_allowed", "ledger_append_allowed", "recommendation_write_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if value.get(field) is not True:
            blockers.append(f"generational_governance_license_{field}_not_true")
    for field in ("execution_authority_granted", "truth_authority_granted", "direct_promotion_authority_granted", "direct_rollback_authority_granted", "direct_quarantine_authority_granted"):
        if value.get(field) is not False:
            blockers.append(f"generational_governance_license_{field}_not_false")


def validate_source(handoff: Mapping[str, Any], record: Mapping[str, Any], state: Mapping[str, Any], plan: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    versions = ((handoff, "indra_qi_bounded_cycle_handoff_packet_v0_12", "handoff"), (record, "indra_qi_bounded_cycle_record_v0_12", "record"), (state, "indra_qi_bounded_generational_cycle_state_v0_12", "state"))
    for value, version, name in versions:
        if value.get("version") != version:
            blockers.append(f"generational_governance_source_{name}_version_invalid")
    for value, field, name in ((handoff, "generation_handoff_digest", "handoff"), (record, "generation_record_digest", "record"), (state, "runner_state_digest", "state")):
        if not valid_digest(value, field):
            blockers.append(f"generational_governance_source_{name}_digest_invalid")
    runner = str(plan.get("runner_id", ""))
    if any(str(value.get("runner_id", "")) != runner for value in (handoff, record, state)):
        blockers.append("generational_governance_source_runner_id_mismatch")
    generation = handoff.get("generation_index")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
        blockers.append("generational_governance_source_generation_index_invalid")
        generation = -1
    run_id = str(handoff.get("generation_run_id", ""))
    if record.get("generation_index") != generation or handoff.get("completed_generations") != generation + 1 or state.get("completed_generations") != generation + 1:
        blockers.append("generational_governance_source_generation_alignment_invalid")
    if not run_id or record.get("generation_run_id") != run_id or state.get("last_generation_run_id") != run_id:
        blockers.append("generational_governance_source_generation_run_id_mismatch")
    handoff_sha, record_sha, state_sha = (str(handoff.get("generation_handoff_digest", "")), str(record.get("generation_record_digest", "")), str(state.get("runner_state_digest", "")))
    if record.get("source_generation_handoff_digest") != handoff_sha or state.get("last_generation_record_digest") != record_sha:
        blockers.append("generational_governance_source_artifact_chain_invalid")
    if plan.get("expected_source_v0_12_runner_state_digest") != state_sha:
        blockers.append("generational_governance_expected_source_state_digest_mismatch")
    target = str(handoff.get("target_v0_11_handoff_packet_digest", ""))
    if state.get("latest_v0_11_handoff_packet_digest") != target:
        blockers.append("generational_governance_source_target_v0_11_digest_mismatch")
    current_metrics = mapping(handoff.get("dynamic_metrics"))
    normalized = metrics(current_metrics)
    if normalized["state_count"] <= 0 or any(not isinstance(current_metrics.get(k), (int, float)) or isinstance(current_metrics.get(k), bool) or not 0 <= float(current_metrics[k]) <= 1 for k in METRICS):
        blockers.append("generational_governance_source_metrics_invalid")
    if metrics(mapping(state.get("dynamic_metrics"))) != normalized:
        blockers.append("generational_governance_source_state_metrics_mismatch")
    return {"runner_id": runner, "generation_index": generation, "generation_run_id": run_id, "handoff_digest": handoff_sha, "record_digest": record_sha, "state_digest": state_sha, "prev_state_digest": str(state.get("prev_runner_state_digest", "")), "source_v0_11_handoff_digest": str(handoff.get("source_v0_11_handoff_packet_digest", "")), "target_v0_11_handoff_digest": target, "metrics": normalized}


def validate_replay(report: Mapping[str, Any], plan: Mapping[str, Any], handoff_sha: str, blockers: list[str]) -> dict[str, Any]:
    if report.get("version") != REPLAY_VERSION or report.get("review_run_id") != plan.get("review_run_id") or report.get("source_generation_handoff_digest") != handoff_sha:
        blockers.append("generational_governance_replay_binding_invalid")
    if report.get("replay_report_digest") != replay_digest(report):
        blockers.append("generational_governance_replay_report_digest_invalid")
    cases = [mapping(v) for v in report.get("cases", []) if isinstance(v, Mapping)] if isinstance(report.get("cases"), list) else []
    seen: set[str] = set()
    passed = 0
    for case in cases:
        case_id = str(case.get("case_id", ""))
        if not case_id or case_id in seen or case.get("source_generation_handoff_digest") != handoff_sha:
            blockers.append("generational_governance_replay_case_invalid")
        seen.add(case_id)
        if any(not str(case.get(k, "")) for k in ("replay_input_digest", "expected_output_digest", "observed_output_digest")):
            blockers.append("generational_governance_replay_case_digest_missing")
        passed += case.get("expected_output_digest") == case.get("observed_output_digest")
    return {"case_count": len(cases), "passed_count": passed, "pass_ratio": round(passed / len(cases), 8) if cases else 0.0}


def adverse(previous: Mapping[str, Any], current: Mapping[str, Any]) -> dict[str, float]:
    return {"observation_debt_increase": round(max(0.0, number(current.get(METRICS[0])) - number(previous.get(METRICS[0]))), 8), "recoverability_loss": round(max(0.0, number(previous.get(METRICS[1])) - number(current.get(METRICS[1]))), 8), "intervention_residue_increase": round(max(0.0, number(current.get(METRICS[2])) - number(previous.get(METRICS[2]))), 8)}


def analyze(observations: Sequence[Mapping[str, Any]], replay: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    window = list(observations)[-int(policy.get("maximum_window_generations", 1) or 1):]
    values = [metrics(mapping(v.get("dynamic_metrics"))) for v in window]
    current = values[-1] if values else metrics({})
    baseline = values[0] if values else current
    drift = adverse(baseline, current)
    epsilon = number(policy.get("regression_epsilon"))
    regressions = trailing = 0
    maximum_step = {k: 0.0 for k in drift}
    for before, after in zip(values, values[1:]):
        step = adverse(before, after)
        maximum_step = {k: max(maximum_step[k], step[k]) for k in step}
        if any(v > epsilon for v in step.values()):
            regressions += 1
            trailing += 1
        else:
            trailing = 0
    weights = mapping(policy.get("collapse_weights"))
    pressure = clamp(number(current.get(METRICS[0])) * number(weights.get("observation_debt")) + (1 - number(current.get(METRICS[1]))) * number(weights.get("recoverability_loss")) + number(current.get(METRICS[2])) * number(weights.get("intervention_residue")))
    enough_history = len(window) >= int(policy.get("minimum_window_generations", 1))
    enough_replay = int(replay.get("case_count", 0)) >= int(policy.get("minimum_replay_cases", 1))
    replay_passed = number(replay.get("pass_ratio")) >= number(policy.get("minimum_replay_pass_ratio"), 1)
    drift_ok = drift["observation_debt_increase"] <= number(policy.get("maximum_observation_debt_drift")) and drift["recoverability_loss"] <= number(policy.get("maximum_recoverability_loss")) and drift["intervention_residue_increase"] <= number(policy.get("maximum_intervention_residue_drift"))
    regression_ok = regressions <= int(policy.get("maximum_regression_steps", 0))
    pressure_ok = pressure <= number(policy.get("maximum_collapse_pressure"))
    if pressure >= number(policy.get("quarantine_collapse_pressure"), 1):
        decision, reason = "quarantine_recommended", "collapse_pressure_at_or_above_quarantine_threshold"
    elif trailing >= int(policy.get("quarantine_consecutive_regressions", 1)):
        decision, reason = "quarantine_recommended", "consecutive_regressions_at_or_above_quarantine_threshold"
    elif not enough_history:
        decision, reason = "hold_for_observation", "minimum_generation_window_not_reached"
    elif not enough_replay:
        decision, reason = "hold_for_observation", "minimum_replay_case_count_not_reached"
    elif not replay_passed:
        decision, reason = "rollback_recommended", "replay_pass_ratio_below_threshold"
    elif not drift_ok:
        decision, reason = "rollback_recommended", "multi_generation_drift_exceeded"
    elif not regression_ok:
        decision, reason = "rollback_recommended", "regression_step_count_exceeded"
    elif not pressure_ok:
        decision, reason = "rollback_recommended", "collapse_pressure_exceeded"
    else:
        decision, reason = "promote_bounded", "replay_passed_and_drift_bounded"
    return {"window_generation_count": len(window), "window_start_generation_index": int(window[0].get("generation_index", -1)) if window else -1, "window_end_generation_index": int(window[-1].get("generation_index", -1)) if window else -1, "baseline_metrics": baseline, "current_metrics": current, "adverse_window_drift": drift, "maximum_adverse_step": maximum_step, "regression_steps": regressions, "consecutive_regressions": trailing, "collapse_pressure": pressure, "history_sufficient": enough_history, "replay_sufficient": enough_replay, "replay_passed": replay_passed, "drift_bounded": drift_ok, "regression_bounded": regression_ok, "collapse_pressure_bounded": pressure_ok, "decision": decision, "decision_reasons": [reason]}
