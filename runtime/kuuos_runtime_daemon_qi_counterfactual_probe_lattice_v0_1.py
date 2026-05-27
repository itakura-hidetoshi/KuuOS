#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


PROBE_TYPES = [
    "observation_debt_probe",
    "recoverability_branch_probe",
    "memory_kernel_probe",
    "safe_reentry_window_probe",
    "nonmarkov_memory_link_probe",
    "multi_time_correlation_probe",
    "continue_process_tensor_supervision_probe",
]

SCORES = {
    "observation_debt_probe": (0.72, 0.82, 0.35),
    "recoverability_branch_probe": (0.86, 0.38, 0.20),
    "memory_kernel_probe": (0.68, 0.30, 0.55),
    "safe_reentry_window_probe": (0.74, 0.42, 0.50),
    "nonmarkov_memory_link_probe": (0.66, 0.32, 0.52),
    "multi_time_correlation_probe": (0.62, 0.34, 0.40),
    "continue_process_tensor_supervision_probe": (0.45, 0.50, 0.10),
}


@dataclass(frozen=True)
class QiCounterfactualProbeCandidate:
    probe_type: str
    target_time_slice: str | None
    expected_recoverability_delta: float
    expected_observation_debt_delta: float
    risk_score: float
    lattice_score: float
    candidate_role: str
    explanation: str


@dataclass(frozen=True)
class QiCounterfactualProbeLattice:
    lattice_version: str
    lattice_status: str
    chosen_probe_type: str | None
    recommended_probe_type: str | None
    candidate_count: int
    ranked_candidates: list[dict[str, Any]]
    unchosen_probe_explanations: list[str]
    lattice_blockers: list[str]
    lattice_warnings: list[str]
    counterfactual_only: bool
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


def _rank_probe(probe_type: str, target: str | None, chosen: str | None) -> QiCounterfactualProbeCandidate:
    rec, debt, risk = SCORES.get(probe_type, (0.30, 0.20, 0.70))
    score = round((rec * 0.50) + (debt * 0.35) - (risk * 0.15), 4)
    role = "chosen_probe" if probe_type == chosen else "unchosen_counterfactual_probe"
    explanation = f"{probe_type} trades recoverability_delta={rec}, observation_debt_delta={debt}, risk={risk}."
    return QiCounterfactualProbeCandidate(
        probe_type=probe_type,
        target_time_slice=target,
        expected_recoverability_delta=rec,
        expected_observation_debt_delta=debt,
        risk_score=risk,
        lattice_score=score,
        candidate_role=role,
        explanation=explanation,
    )


def build_qi_counterfactual_probe_lattice(
    *,
    dry_run_simulation: Mapping[str, Any],
    trend_summary: Mapping[str, Any],
    candidate_probe_types: list[str] | None = None,
) -> QiCounterfactualProbeLattice:
    sim = _mapping(dry_run_simulation)
    summary = _mapping(trend_summary)
    blockers: list[str] = []
    warnings: list[str] = []

    if sim.get("simulation_status") != "QI_DRY_RUN_PROBE_SIMULATION_READY":
        blockers.append("dry_run_simulation_not_ready")
    if sim.get("simulation_only") is not True or sim.get("dry_run_only") is not True:
        blockers.append("dry_run_simulation_boundary_flags_invalid")
    for key in ["state_mutation_performed", "control_packet_mutation_performed", "memory_write_performed"]:
        if sim.get(key) is not False:
            blockers.append(f"dry_run_simulation_{key}_not_false")
    _no_authority("dry_run_simulation", sim, blockers)

    if summary.get("summary_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY":
        blockers.append("trend_summary_not_ready")
    _no_authority("trend_summary", summary, blockers)

    chosen = sim.get("simulated_probe_type") or summary.get("latest_recommended_probe_type")
    target = sim.get("simulated_target_time_slice") or summary.get("latest_probe_target_time_slice")
    probes = candidate_probe_types or PROBE_TYPES
    valid_probes = [p for p in probes if isinstance(p, str) and p]
    if not valid_probes:
        blockers.append("candidate_probe_types_missing")
    if chosen and chosen not in valid_probes:
        valid_probes = [str(chosen)] + valid_probes

    candidates = sorted(
        [_rank_probe(p, str(target) if target else None, str(chosen) if chosen else None) for p in dict.fromkeys(valid_probes)],
        key=lambda item: item.lattice_score,
        reverse=True,
    )
    recommended = candidates[0].probe_type if candidates else None
    unchosen = [c.explanation for c in candidates if c.probe_type != chosen]
    ready = not blockers
    return QiCounterfactualProbeLattice(
        lattice_version="kuuos_runtime_daemon_qi_counterfactual_probe_lattice_v0_1",
        lattice_status="QI_COUNTERFACTUAL_PROBE_LATTICE_READY" if ready else "QI_COUNTERFACTUAL_PROBE_LATTICE_BLOCKED",
        chosen_probe_type=str(chosen) if chosen else None,
        recommended_probe_type=recommended,
        candidate_count=len(candidates),
        ranked_candidates=[asdict(candidate) for candidate in candidates],
        unchosen_probe_explanations=unchosen,
        lattice_blockers=blockers,
        lattice_warnings=warnings,
        counterfactual_only=True,
        simulation_only=True,
        dry_run_only=True,
        state_mutation_performed=False,
        control_packet_mutation_performed=False,
        memory_write_performed=False,
    )
