#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiDryRunProbeSimulation:
    simulation_version: str
    simulation_status: str
    simulated_probe_type: str | None
    simulated_target_time_slice: str | None
    expected_recoverability_effect: str
    expected_observation_debt_effect: str
    expected_risk_profile: str
    source_license_status: str | None
    source_summary_status: str | None
    simulation_blockers: list[str]
    simulation_warnings: list[str]
    simulation_only: bool
    dry_run_only: bool
    state_mutation_performed: bool
    control_packet_mutation_performed: bool
    memory_write_performed: bool
    authority: str = "none"
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_dry_run_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_world_update_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _no_authority(prefix: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if payload.get("authority") != "none":
        blockers.append(f"{prefix}_authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_dry_run_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
    ]:
        if payload.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _effect_for_probe(probe_type: str | None) -> tuple[str, str, str]:
    if probe_type == "observation_debt_probe":
        return ("may improve recoverability visibility", "may reduce observation debt uncertainty", "low_to_medium_review_risk")
    if probe_type == "recoverability_branch_probe":
        return ("may clarify recovery branch options", "neutral_to_low_debt_effect", "low_review_risk")
    if probe_type == "memory_kernel_probe":
        return ("may clarify memory-kernel continuity", "neutral_debt_effect", "medium_review_risk")
    if probe_type == "safe_reentry_window_probe":
        return ("may clarify safe reentry timing", "neutral_to_low_debt_effect", "medium_review_risk")
    if probe_type == "nonmarkov_memory_link_probe":
        return ("may improve non-Markov linkage visibility", "neutral_debt_effect", "medium_review_risk")
    if probe_type == "multi_time_correlation_probe":
        return ("may improve multi-time correlation visibility", "neutral_debt_effect", "low_to_medium_review_risk")
    if probe_type == "continue_process_tensor_supervision_probe":
        return ("maintains observation continuity", "may prevent new observation debt", "low_review_risk")
    return ("undetermined recoverability effect", "undetermined debt effect", "unknown_review_risk")


def build_qi_dry_run_probe_simulation(
    *,
    license_candidate: Mapping[str, Any],
    trend_summary: Mapping[str, Any],
    probe_plan: Mapping[str, Any] | None = None,
) -> QiDryRunProbeSimulation:
    license_value = _mapping(license_candidate)
    summary = _mapping(trend_summary)
    plan = _mapping(probe_plan or summary.get("latest_process_tensor_probe_plan"))
    blockers: list[str] = []
    warnings: list[str] = []

    if license_value.get("gate_status") != "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY":
        blockers.append("license_candidate_not_ready")
    if license_value.get("candidate_license_kind") != "dry_run_probe_simulation_candidate":
        blockers.append("license_candidate_kind_not_dry_run_probe_simulation")
    if license_value.get("license_candidate_only") is not True or license_value.get("dry_run_candidate_only") is not True:
        blockers.append("license_candidate_boundary_flags_invalid")
    _no_authority("license_candidate", license_value, blockers)

    if summary.get("summary_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY":
        blockers.append("trend_summary_not_ready")
    if summary.get("summary_only") is not True or summary.get("read_only") is not True:
        blockers.append("trend_summary_boundary_flags_invalid")
    _no_authority("trend_summary", summary, blockers)

    probe_type = plan.get("recommended_probe_type") or summary.get("latest_recommended_probe_type") or summary.get("dominant_probe_type")
    target = plan.get("probe_target_time_slice") or summary.get("latest_probe_target_time_slice")
    if not probe_type:
        warnings.append("probe_type_missing")
    if not target:
        warnings.append("probe_target_time_slice_missing")

    recoverability_effect, debt_effect, risk_profile = _effect_for_probe(str(probe_type) if probe_type else None)
    ready = not blockers
    return QiDryRunProbeSimulation(
        simulation_version="kuuos_runtime_daemon_qi_dry_run_probe_simulator_v0_1",
        simulation_status="QI_DRY_RUN_PROBE_SIMULATION_READY" if ready else "QI_DRY_RUN_PROBE_SIMULATION_BLOCKED",
        simulated_probe_type=str(probe_type) if probe_type else None,
        simulated_target_time_slice=str(target) if target else None,
        expected_recoverability_effect=recoverability_effect,
        expected_observation_debt_effect=debt_effect,
        expected_risk_profile=risk_profile,
        source_license_status=str(license_value.get("gate_status")) if license_value.get("gate_status") else None,
        source_summary_status=str(summary.get("summary_status")) if summary.get("summary_status") else None,
        simulation_blockers=blockers,
        simulation_warnings=warnings,
        simulation_only=True,
        dry_run_only=True,
        state_mutation_performed=False,
        control_packet_mutation_performed=False,
        memory_write_performed=False,
    )
