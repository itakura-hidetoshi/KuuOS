#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_licensed_sandbox_lineage_trial_plan_v0_16"
LICENSE_VERSION = "indra_qi_licensed_sandbox_lineage_trial_license_v0_16"
REPORT_VERSION = "indra_qi_licensed_sandbox_lineage_trial_report_v0_16"
STATE_VERSION = "indra_qi_licensed_sandbox_lineage_trial_state_v0_16"
LEDGER_VERSION = "indra_qi_licensed_sandbox_lineage_trial_ledger_record_v0_16"
WORLD_VERSION = "indra_qi_world_model_v0_1"
CANDIDATE_SET_VERSION = "indra_qi_multi_lineage_candidate_set_v0_15"
EVOLUTION_STATE_VERSION = "indra_qi_multi_lineage_evolution_state_v0_15"
EVOLUTION_RECOMMENDATION_VERSION = "indra_qi_multi_lineage_evolution_recommendation_v0_15"

SOURCE_DECISIONS = {
    "hold_for_observation",
    "diverse_bounded_evolution_ready",
    "branch_reopening_candidate_set_ready",
    "focus_reobserve_candidate_set_ready",
    "redesign_candidate_set_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "sandbox_trial_set_ready",
    "redesign_sandbox_trials_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
READY_SOURCE_DECISIONS = {
    "diverse_bounded_evolution_ready",
    "branch_reopening_candidate_set_ready",
    "focus_reobserve_candidate_set_ready",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_15_candidate_set_required": True,
    "source_v0_15_digest_chain_exact": True,
    "world_source_read_only": True,
    "multi_lineage_source_read_only": True,
    "sandbox_trial_evidence_only": True,
    "sandbox_network_disabled": True,
    "sandbox_external_actuation_disabled": True,
    "sandbox_filesystem_overlay_required": True,
    "sandbox_snapshot_restore_required": True,
    "sandbox_resource_budget_bounded": True,
    "deterministic_replay_required": True,
    "trial_residual_bounded": True,
    "candidate_weighting_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_lineage_selection_authority": True,
    "not_lineage_execution_authority": True,
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
    return sha(without(value, "sandbox_trial_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "sandbox_trial_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "sandbox_trial_state_digest"))


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"{prefix}_{field}_invalid")


def _positive_int(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw <= 0:
            blockers.append(f"{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("sandbox_trial_plan_version_invalid")
    if plan.get("sandbox_trial_plan_digest") != plan_digest(plan):
        blockers.append("sandbox_trial_plan_digest_invalid")
    for field in (
        "trial_program_id",
        "trial_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_candidate_set_digest",
        "expected_source_evolution_state_digest",
        "expected_source_evolution_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"sandbox_trial_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"sandbox_trial_boundary_{field}_mismatch")
    policy = mapping(plan.get("trial_policy"))
    _positive_int(
        policy,
        (
            "minimum_trial_lineages",
            "maximum_trial_lineages",
            "maximum_attempts_per_lineage",
            "maximum_duration_ms",
            "maximum_cpu_ms",
            "maximum_peak_memory_mb",
        ),
        blockers,
        "sandbox_trial_policy",
    )
    low = policy.get("minimum_trial_lineages")
    high = policy.get("maximum_trial_lineages")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 16):
        blockers.append("sandbox_trial_lineage_count_bounds_invalid")
    _bounded(
        policy,
        (
            "minimum_lineage_coverage_ratio",
            "minimum_passing_lineage_ratio",
            "minimum_deterministic_replay_ratio",
            "maximum_trial_residual_score",
        ),
        blockers,
        "sandbox_trial_policy",
    )
    for field in (
        "require_network_disabled",
        "require_external_actuation_disabled",
        "require_filesystem_overlay",
        "require_snapshot_restore",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"sandbox_trial_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    candidate_set: Mapping[str, Any],
    evolution_state: Mapping[str, Any],
    evolution_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION or not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("sandbox_trial_source_world_invalid")
    if candidate_set.get("version") != CANDIDATE_SET_VERSION or not valid_digest(candidate_set, "candidate_set_digest"):
        blockers.append("sandbox_trial_source_candidate_set_invalid")
    if evolution_state.get("version") != EVOLUTION_STATE_VERSION or not valid_digest(evolution_state, "multi_lineage_state_digest"):
        blockers.append("sandbox_trial_source_evolution_state_invalid")
    if evolution_recommendation.get("version") != EVOLUTION_RECOMMENDATION_VERSION or not valid_digest(
        evolution_recommendation, "multi_lineage_recommendation_digest"
    ):
        blockers.append("sandbox_trial_source_evolution_recommendation_invalid")

    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    candidate_digest = str(candidate_set.get("candidate_set_digest", ""))
    state_sha = str(evolution_state.get("multi_lineage_state_digest", ""))
    recommendation_sha = str(evolution_recommendation.get("multi_lineage_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_digest,
        "expected_candidate_set_digest": candidate_digest,
        "expected_source_evolution_state_digest": state_sha,
        "expected_source_evolution_recommendation_digest": recommendation_sha,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"sandbox_trial_{field}_mismatch")
    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id:
        blockers.append("sandbox_trial_world_model_id_mismatch")
    if candidate_set.get("world_model_id") != world_model_id or evolution_state.get("world_model_id") != world_model_id or evolution_recommendation.get("world_model_id") != world_model_id:
        blockers.append("sandbox_trial_source_world_model_chain_invalid")
    if candidate_set.get("source_world_state_digest") != world_digest:
        blockers.append("sandbox_trial_candidate_world_digest_mismatch")
    if evolution_state.get("latest_candidate_set_digest") != candidate_digest:
        blockers.append("sandbox_trial_state_candidate_set_digest_mismatch")
    if evolution_recommendation.get("candidate_set_digest") != candidate_digest:
        blockers.append("sandbox_trial_recommendation_candidate_set_digest_mismatch")
    if evolution_state.get("latest_multi_lineage_decision") != evolution_recommendation.get("decision"):
        blockers.append("sandbox_trial_source_decision_mismatch")
    if evolution_state.get("last_evolution_run_id") != evolution_recommendation.get("evolution_run_id"):
        blockers.append("sandbox_trial_source_run_id_mismatch")
    decision = str(evolution_recommendation.get("decision", ""))
    if decision not in SOURCE_DECISIONS:
        blockers.append("sandbox_trial_source_decision_invalid")
    if evolution_recommendation.get("recommendation_only") is not True:
        blockers.append("sandbox_trial_source_recommendation_not_advisory")
    for field in (
        "direct_lineage_selection_authority",
        "direct_lineage_execution_authority",
        "direct_world_update_authority",
        "direct_promotion_authority",
        "direct_rollback_authority",
        "direct_quarantine_authority",
        "truth_authority",
    ):
        if evolution_recommendation.get(field) is not False:
            blockers.append(f"sandbox_trial_source_{field}_not_false")
    if candidate_set.get("candidate_weighting_not_truth") is not True or candidate_set.get("candidate_set_not_execution") is not True:
        blockers.append("sandbox_trial_candidate_set_authority_boundary_invalid")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("sandbox_trial_multi_world_noncollapse_missing")
    lineages = [dict(mapping(value)) for value in items(candidate_set.get("candidate_lineages"))]
    lineage_ids = {str(value.get("lineage_id", "")) for value in lineages if str(value.get("lineage_id", ""))}
    if len(lineage_ids) != len(lineages) or not lineage_ids:
        blockers.append("sandbox_trial_candidate_lineage_ids_invalid")
    return {
        "world_digest": world_digest,
        "candidate_set_digest": candidate_digest,
        "evolution_state_digest": state_sha,
        "evolution_recommendation_digest": recommendation_sha,
        "source_decision": decision,
        "source_evolution_run_id": str(evolution_recommendation.get("evolution_run_id", "")),
        "lineages": lineages,
        "lineage_ids": lineage_ids,
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
        "bound_sandbox_trial_plan_digest": str(plan.get("sandbox_trial_plan_digest", "")),
        "bound_sandbox_trial_report_digest": str(report.get("sandbox_trial_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "bound_source_evolution_state_digest": str(source.get("evolution_state_digest", "")),
        "bound_source_evolution_recommendation_digest": str(source.get("evolution_recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"sandbox_trial_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("sandbox_trial_license_id_missing")
    for field in (
        "state_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"sandbox_trial_license_{field}_not_true")
    for field in (
        "network_authority_granted",
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
            blockers.append(f"sandbox_trial_license_{field}_not_false")


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("sandbox_trial_report_version_invalid")
    if report.get("trial_run_id") != plan.get("trial_run_id"):
        blockers.append("sandbox_trial_report_run_id_mismatch")
    if report.get("source_candidate_set_digest") != source.get("candidate_set_digest"):
        blockers.append("sandbox_trial_report_candidate_set_digest_mismatch")
    if report.get("source_evolution_recommendation_digest") != source.get("evolution_recommendation_digest"):
        blockers.append("sandbox_trial_report_evolution_recommendation_digest_mismatch")
    if report.get("sandbox_trial_report_digest") != report_digest(report):
        blockers.append("sandbox_trial_report_digest_invalid")
    raw_trials = report.get("trials")
    trials = [dict(mapping(value)) for value in raw_trials] if isinstance(raw_trials, list) else []
    if not trials:
        blockers.append("sandbox_trial_report_trials_missing")
        return trials
    seen: set[str] = set()
    attempt_keys: set[tuple[str, int]] = set()
    lineage_ids = set(source.get("lineage_ids", set()))
    for index, trial in enumerate(trials):
        trial_id = str(trial.get("trial_id", ""))
        lineage_id = str(trial.get("lineage_id", ""))
        attempt = trial.get("attempt_index")
        if not trial_id or trial_id in seen:
            blockers.append(f"sandbox_trial_case_{index}_trial_id_invalid")
        seen.add(trial_id)
        if lineage_id not in lineage_ids:
            blockers.append(f"sandbox_trial_case_{index}_lineage_unknown")
        if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 0 or (lineage_id, attempt) in attempt_keys:
            blockers.append(f"sandbox_trial_case_{index}_attempt_invalid")
        else:
            attempt_keys.add((lineage_id, attempt))
        for field in (
            "sandbox_image_digest",
            "sandbox_snapshot_digest",
            "input_digest",
            "output_digest",
            "replay_output_digest",
            "rollback_state_digest",
            "expected_rollback_state_digest",
            "stdout_digest",
            "stderr_digest",
        ):
            if not str(trial.get(field, "")):
                blockers.append(f"sandbox_trial_case_{index}_{field}_missing")
        for field in ("duration_ms", "cpu_ms", "peak_memory_mb"):
            raw = trial.get(field)
            if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
                blockers.append(f"sandbox_trial_case_{index}_{field}_invalid")
        residual = trial.get("residual_score")
        if isinstance(residual, bool) or not isinstance(residual, (int, float)) or not 0 <= float(residual) <= 1:
            blockers.append(f"sandbox_trial_case_{index}_residual_score_invalid")
        for field in (
            "network_access_attempted",
            "external_actuation_attempted",
            "filesystem_overlay_used",
            "policy_boundary_preserved",
        ):
            if not isinstance(trial.get(field), bool):
                blockers.append(f"sandbox_trial_case_{index}_{field}_invalid")
        exit_code = trial.get("process_exit_code")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            blockers.append(f"sandbox_trial_case_{index}_process_exit_code_invalid")
    return trials


def analyze_trials(
    trials: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("trial_policy"))
    lineage_ids = set(source.get("lineage_ids", set()))
    maximum_attempts = int(policy.get("maximum_attempts_per_lineage", 1))
    attempts = Counter(str(trial.get("lineage_id", "")) for trial in trials)
    over_attempted = sorted(lineage for lineage, count in attempts.items() if count > maximum_attempts)
    isolation_breaches = 0
    passing_trials = 0
    deterministic_trials = 0
    snapshot_restored_trials = 0
    trial_results: list[dict[str, Any]] = []
    passing_lineages: set[str] = set()
    deterministic_lineages: set[str] = set()

    for trial in trials:
        lineage_id = str(trial.get("lineage_id", ""))
        network_ok = trial.get("network_access_attempted") is False
        actuation_ok = trial.get("external_actuation_attempted") is False
        overlay_ok = trial.get("filesystem_overlay_used") is True
        boundary_ok = trial.get("policy_boundary_preserved") is True
        isolation_ok = network_ok and actuation_ok and overlay_ok and boundary_ok
        if not isolation_ok:
            isolation_breaches += 1
        deterministic = str(trial.get("output_digest", "")) == str(trial.get("replay_output_digest", ""))
        restored = str(trial.get("rollback_state_digest", "")) == str(trial.get("expected_rollback_state_digest", ""))
        budget_ok = (
            int(trial.get("duration_ms", 10**18)) <= int(policy.get("maximum_duration_ms", 0))
            and int(trial.get("cpu_ms", 10**18)) <= int(policy.get("maximum_cpu_ms", 0))
            and int(trial.get("peak_memory_mb", 10**18)) <= int(policy.get("maximum_peak_memory_mb", 0))
        )
        residual_ok = number(trial.get("residual_score"), 1.0) <= number(policy.get("maximum_trial_residual_score"), 0.0)
        process_ok = trial.get("process_exit_code") == 0
        passed = isolation_ok and deterministic and restored and budget_ok and residual_ok and process_ok
        if passed:
            passing_trials += 1
            passing_lineages.add(lineage_id)
        if deterministic:
            deterministic_trials += 1
            deterministic_lineages.add(lineage_id)
        if restored:
            snapshot_restored_trials += 1
        trial_results.append(
            {
                "trial_id": str(trial.get("trial_id", "")),
                "lineage_id": lineage_id,
                "attempt_index": int(trial.get("attempt_index", -1)),
                "isolation_preserved": isolation_ok,
                "deterministic_replay": deterministic,
                "snapshot_restored": restored,
                "resource_budget_preserved": budget_ok,
                "residual_bounded": residual_ok,
                "process_succeeded": process_ok,
                "trial_passed": passed,
            }
        )

    covered_lineages = set(attempts) & lineage_ids
    denominator = max(len(lineage_ids), 1)
    trial_count = len(trials)
    coverage_ratio = clamp(len(covered_lineages) / denominator)
    passing_lineage_ratio = clamp(len(passing_lineages) / denominator)
    deterministic_ratio = clamp(deterministic_trials / trial_count) if trial_count else 0.0
    restored_ratio = clamp(snapshot_restored_trials / trial_count) if trial_count else 0.0
    gates = {
        "trial_lineage_count_bounded": int(policy.get("minimum_trial_lineages", 0)) <= len(covered_lineages) <= int(policy.get("maximum_trial_lineages", 0)),
        "attempt_count_bounded": not over_attempted,
        "lineage_coverage_sufficient": coverage_ratio >= number(policy.get("minimum_lineage_coverage_ratio")),
        "passing_lineage_ratio_sufficient": passing_lineage_ratio >= number(policy.get("minimum_passing_lineage_ratio")),
        "deterministic_replay_ratio_sufficient": deterministic_ratio >= number(policy.get("minimum_deterministic_replay_ratio")),
        "snapshot_restore_complete": restored_ratio == 1.0,
        "isolation_boundary_preserved": isolation_breaches == 0,
    }
    return {
        "candidate_lineage_count": len(lineage_ids),
        "trial_count": trial_count,
        "covered_lineage_count": len(covered_lineages),
        "passing_trial_count": passing_trials,
        "passing_lineage_count": len(passing_lineages),
        "deterministic_trial_count": deterministic_trials,
        "snapshot_restored_trial_count": snapshot_restored_trials,
        "isolation_breach_count": isolation_breaches,
        "over_attempted_lineage_ids": over_attempted,
        "lineage_coverage_ratio": coverage_ratio,
        "passing_lineage_ratio": passing_lineage_ratio,
        "deterministic_replay_ratio": deterministic_ratio,
        "snapshot_restore_ratio": restored_ratio,
        "trial_results": trial_results,
        "gates": gates,
    }


def evaluate_trials(analysis: Mapping[str, Any], source_decision: str) -> dict[str, Any]:
    gates = mapping(analysis.get("gates"))
    if source_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_15_quarantine_recommended"
    elif source_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_15_rollback_recommended"
    elif source_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_15_hold_for_observation"
    elif int(analysis.get("isolation_breach_count", 0)) > 0:
        decision, reason = "quarantine_recommended", "sandbox_isolation_or_actuation_boundary_breach"
    elif source_decision == "redesign_candidate_set_recommended":
        decision, reason = "redesign_sandbox_trials_recommended", "source_v0_15_candidate_set_redesign_required"
    elif source_decision in READY_SOURCE_DECISIONS and all(value is True for value in gates.values()):
        decision, reason = "sandbox_trial_set_ready", "bounded_isolated_deterministic_trials_passed"
    elif source_decision in READY_SOURCE_DECISIONS:
        decision, reason = "redesign_sandbox_trials_recommended", "sandbox_trial_evidence_gates_failed"
    else:
        decision, reason = "quarantine_recommended", "unknown_source_v0_15_decision"
    return {
        "source_evolution_decision": source_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "trial_set_ready": decision == "sandbox_trial_set_ready",
        "recommendation_only": True,
    }
