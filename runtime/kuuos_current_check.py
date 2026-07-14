#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from runtime.kuuos_current_root_sequence_v0_113 import (
    CURRENT_ROOT_STEPS as REPOSITORY_LINEAGE_STEPS,
)
from runtime.kuuos_current_root_sequence_v0_41 import CurrentRootStep

ROOT = Path(__file__).resolve().parents[1]

CURRENT_RUNTIME_ROOT = "runtime/kuuos_current_check.py"
CURRENT_ROOT_PROFILE = "integrated-current-root-v1"
CURRENT_ROOT_SEQUENCE_FRONTIER = "kuuos_current_root_sequence_v0_113"
CURRENT_REPOSITORY_FRONTIER = "self-organization v0.113"
CURRENT_PLANOS_FRONTIER = "PlanOS v1.23"
CURRENT_DECISIONOS_FRONTIER = "DecisionOS v0.6"
CURRENT_MEMORYOS_FRONTIER = "MemoryOS v0.63"
CURRENT_WORLD_DEPENDENCY = "KuuOS v14.0 causal WORLD state"
CURRENT_BASELINE_DATE = "2026-07-14 JST"

CURRENT_MAIN_FRONTIER = CURRENT_REPOSITORY_FRONTIER
CURRENT_DRAFT_FRONTIER = "none"
CURRENT_DRAFT_PR = "none"
CURRENT_DRAFT_BRANCH = "none"
CURRENT_FRONTIER_ARTIFACT = (
    "runtime/kuuos_memoryos_kantorovich_lipschitz_mgf_"
    "certificate_kernel_v0_1.py"
)
CURRENT_FRONTIER_MODE = "integrated_active_frontiers"
CURRENT_FRONTIER_BOUNDARY = "validation_only"


def _script_step(step_id: str, target: str, description: str) -> CurrentRootStep:
    return CurrentRootStep(step_id, "script", target, True, description)


PLANOS_ACTIVE_FRONTIER_TARGETS: tuple[tuple[str, str], ...] = (
    ("planos-v0-91-information-geometric-qi-objective", "scripts/check_planos_information_geometric_qi_objective_kernel_v0_1.py"),
    ("planos-v0-92-kl-regularized-objective-update", "scripts/check_planos_kl_regularized_objective_update_kernel_v0_92.py"),
    ("planos-v0-93-zero-temperature-limit", "scripts/check_planos_zero_temperature_minimal_action_limit_kernel_v0_1.py"),
    ("planos-v0-94-finite-temperature-concentration", "scripts/check_planos_finite_temperature_concentration_certificate_kernel_v0_1.py"),
    ("planos-v0-95-adaptive-qi-temperature", "scripts/check_planos_adaptive_qi_temperature_calibration_kernel_v0_1.py"),
    ("planos-v0-96-temperature-hysteresis-rate-limit", "scripts/check_planos_temperature_hysteresis_rate_limit_kernel_v0_1.py"),
    ("planos-v0-97-temperature-trajectory-receipt", "scripts/check_planos_temperature_trajectory_receipt_kernel_v0_1.py"),
    ("planos-v0-98-temperature-trajectory-stability", "scripts/check_planos_temperature_trajectory_stability_certificate_kernel_v0_1.py"),
    ("planos-v0-99-qi-conditioned-information-metric", "scripts/check_planos_qi_conditioned_information_metric_certificate_kernel_v0_1.py"),
    ("planos-v1-00-world-conditioned-pullback-metric", "scripts/check_planos_world_conditioned_path_projection_pullback_metric_kernel_v0_1.py"),
    ("planos-v1-01-world-conditioned-distribution-update", "scripts/check_planos_world_conditioned_objective_distribution_update_kernel_v0_1.py"),
    ("planos-v1-02-decision-handoff-certificate", "scripts/check_planos_world_conditioned_distribution_decision_handoff_certificate_kernel_v0_1.py"),
    ("planos-v1-05-native-coupled-information-metric", "scripts/check_planos_native_coupled_information_metric_certificate_kernel_v0_1.py"),
    ("planos-v1-06-state-dependent-metric-jet-levi-civita", "scripts/check_planos_state_dependent_metric_jet_levi_civita_certificate_kernel_v0_1.py"),
    ("planos-v1-07-second-order-metric-jet-curvature", "scripts/check_planos_second_order_metric_jet_curvature_certificate_kernel_v0_1.py"),
    ("planos-v1-08-multi-chart-atlas-curvature", "scripts/check_planos_multi_chart_atlas_curvature_certificate_kernel_v0_1.py"),
    ("planos-v1-09-jacobi-geodesic-deviation", "scripts/check_planos_jacobi_geodesic_deviation_certificate_kernel_v0_1.py"),
    ("planos-v1-10-second-variation-morse-index", "scripts/check_planos_second_variation_morse_index_certificate_kernel_v0_1.py"),
    ("planos-v1-11-conjugate-events-injectivity-radius", "scripts/check_planos_conjugate_event_sequence_injectivity_radius_certificate_kernel_v0_1.py"),
    ("planos-v1-12-exponential-normal-coordinate-ball", "scripts/check_planos_exponential_map_normal_coordinate_ball_certificate_kernel_v0_1.py"),
    ("planos-v1-13-finite-normal-ball-cover-hopf-rinow-witness", "scripts/check_planos_finite_normal_ball_cover_hopf_rinow_witness_certificate_kernel_v0_1.py"),
    ("planos-v1-14-finite-cover-nerve-cech-path-homotopy", "scripts/check_planos_finite_cover_nerve_cech_path_homotopy_certificate_kernel_v0_1.py"),
    ("planos-v1-15-finite-simplicial-chain-homology", "scripts/check_planos_finite_simplicial_chain_homology_certificate_kernel_v0_1.py"),
    ("planos-v1-16-smith-normal-form-integer-homology", "scripts/check_planos_smith_normal_form_integer_homology_certificate_kernel_v0_1.py"),
    ("planos-v1-17-finite-filtration-persistent-homology", "scripts/check_planos_finite_filtration_persistent_homology_certificate_kernel_v0_1.py"),
    ("planos-v1-18-finite-bottleneck-persistence-stability", "scripts/check_planos_finite_bottleneck_persistence_stability_certificate_kernel_v0_1.py"),
    ("planos-v1-19-finite-p-wasserstein-persistence-transport", "scripts/check_planos_finite_p_wasserstein_persistence_transport_certificate_kernel_v0_1.py"),
    ("planos-v1-20-finite-wasserstein-frechet-barycenter-dispersion", "scripts/check_planos_finite_wasserstein_frechet_barycenter_dispersion_certificate_kernel_v0_1.py"),
    ("planos-v1-21-finite-physical-quantum-qi-path-history-noncollapse", "scripts/check_planos_finite_physical_quantum_qi_path_history_noncollapse_certificate_kernel_v0_1.py"),
    ("planos-v1-22-finite-gaussian-physical-quantum-qi-homotopy-decoherence", "scripts/check_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate_kernel_v0_1.py"),
    ("planos-v1-23-finite-physical-quantum-qi-coherence-kernel-partial-dephasing", "scripts/check_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate_kernel_v0_1.py"),
)
PLANOS_ACTIVE_FRONTIER_STEPS: tuple[CurrentRootStep, ...] = tuple(
    _script_step(step_id, target, f"Validate {step_id}.")
    for step_id, target in PLANOS_ACTIVE_FRONTIER_TARGETS
)

DECISIONOS_ACTIVE_FRONTIER_STEPS: tuple[CurrentRootStep, ...] = (
    _script_step(
        "decisionos-v0-1-v0-6-cumulative",
        "scripts/run_decision_os_full_checks.py",
        "Validate DecisionOS through WORLD-conditioned relational deliberation v0.6.",
    ),
)

MEMORYOS_ACTIVE_FRONTIER_TARGETS: tuple[tuple[str, str], ...] = (
    ("memoryos-v0-40-observer-relative-non-markov-temporal-record", "scripts/check_memoryos_observer_relative_non_markov_temporal_record_certificate_kernel_v0_1.py"),
    ("memoryos-v0-41-observer-relative-finite-window-qi-influence-planos-handoff", "scripts/check_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_certificate_kernel_v0_1.py"),
    ("memoryos-v0-42-observer-relative-non-markov-influence-conditioned-planos-coherence-kernel", "scripts/check_planos_memoryos_observer_relative_non_markov_influence_conditioned_coherence_kernel_certificate_kernel_v0_1.py"),
    ("memoryos-v0-43-observer-relative-temporal-window-coherence-cocycle-composition", "scripts/check_planos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1.py"),
    ("memoryos-v0-44-observer-relative-coherence-quadratic-evidence-decisionos-handoff", "scripts/check_planos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1.py"),
    ("memoryos-v0-45-candidate-gram-lift-decisionos-relational-coherence-kernel", "scripts/check_planos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1.py"),
    ("memoryos-v0-46-candidate-pair-cauchy-schwarz-relational-coherence-envelope", "scripts/check_planos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1.py"),
    ("memoryos-v0-47-candidate-triple-gram-determinant-joint-coherence-compatibility", "scripts/check_planos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1.py"),
    ("memoryos-v0-48-two-history-candidate-gram-factorization-reconstruction", "scripts/check_planos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1.py"),
    ("memoryos-v0-49-candidate-nullspace-dephasing-rank-stratification", "scripts/check_planos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1.py"),
    ("memoryos-v0-50-candidate-quotient-coordinate-canonicalization", "scripts/check_planos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1.py"),
    ("memoryos-v0-51-candidate-quotient-mode-diagonalization-inverse", "scripts/check_planos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1.py"),
    ("memoryos-v0-52-quotient-metric-covector-transport", "scripts/check_planos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1.py"),
    ("memoryos-v0-53-quotient-transport-jacobian-volume-stratification", "scripts/check_planos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1.py"),
    ("memoryos-v0-54-quotient-metric-density-transport-radon-nikodym-cocycle", "scripts/check_planos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1.py"),
    ("memoryos-v0-55-relative-entropy-transport-lebesgue-decomposition", "scripts/check_planos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1.py"),
    ("memoryos-v0-56-f-divergence-transport-data-processing-contraction", "scripts/check_planos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1.py"),
    ("memoryos-v0-57-stochastic-markov-kernel-f-divergence-sufficiency", "scripts/check_planos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1.py"),
    ("memoryos-v0-58-reversible-markov-semigroup-entropy-production", "scripts/check_planos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1.py"),
    ("memoryos-v0-59-log-sobolev-hypercontractive-mixing", "scripts/check_planos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1.py"),
    ("memoryos-v0-60-modified-log-sobolev-hellinger-separation-cutoff", "scripts/check_planos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.py"),
    ("memoryos-v0-61-bakry-emery-functional-hierarchy-concentration", "scripts/check_planos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1.py"),
    ("memoryos-v0-62-wasserstein-pearson-transport-marton-coupling", "scripts/check_planos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1.py"),
    ("memoryos-v0-63-kantorovich-lipschitz-semigroup-finite-mgf", "scripts/check_planos_memoryos_kantorovich_lipschitz_mgf_certificate_kernel_v0_1.py"),
)
MEMORYOS_ACTIVE_FRONTIER_STEPS: tuple[CurrentRootStep, ...] = tuple(
    _script_step(step_id, target, f"Validate {step_id}.")
    for step_id, target in MEMORYOS_ACTIVE_FRONTIER_TARGETS
)

CURRENT_ROOT_STEPS: tuple[CurrentRootStep, ...] = (
    REPOSITORY_LINEAGE_STEPS
    + PLANOS_ACTIVE_FRONTIER_STEPS
    + DECISIONOS_ACTIVE_FRONTIER_STEPS
    + MEMORYOS_ACTIVE_FRONTIER_STEPS
)


def current_runtime_root_summary() -> dict[str, object]:
    return {
        "runtime_root": CURRENT_RUNTIME_ROOT,
        "root_profile": CURRENT_ROOT_PROFILE,
        "baseline_date": CURRENT_BASELINE_DATE,
        "repository_root_sequence": CURRENT_ROOT_SEQUENCE_FRONTIER,
        "repository_frontier": CURRENT_REPOSITORY_FRONTIER,
        "planos_frontier": CURRENT_PLANOS_FRONTIER,
        "decisionos_frontier": CURRENT_DECISIONOS_FRONTIER,
        "memoryos_frontier": CURRENT_MEMORYOS_FRONTIER,
        "world_dependency": CURRENT_WORLD_DEPENDENCY,
        "repository_step_count": len(REPOSITORY_LINEAGE_STEPS),
        "planos_step_count": len(PLANOS_ACTIVE_FRONTIER_STEPS),
        "decisionos_step_count": len(DECISIONOS_ACTIVE_FRONTIER_STEPS),
        "memoryos_step_count": len(MEMORYOS_ACTIVE_FRONTIER_STEPS),
        "total_step_count": len(CURRENT_ROOT_STEPS),
        "frontier_mode": CURRENT_FRONTIER_MODE,
        "frontier_boundary": CURRENT_FRONTIER_BOUNDARY,
    }


def _run_unittest_module(module_name: str) -> int:
    suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def _run_callable(target: str) -> int:
    module_name, function_name = target.split(":", 1)
    module = importlib.import_module(module_name)
    return int(getattr(module, function_name)())


def _run_script(target: str) -> int:
    script = ROOT / target
    if not script.is_file():
        print(f"missing_current_root_script:{target}", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT), env.get("PYTHONPATH", "")) if part
    )
    return subprocess.run(
        [sys.executable, str(script)], cwd=ROOT, env=env, check=False
    ).returncode


def _run_step(runner: str, target: str) -> int:
    if runner == "unittest":
        return _run_unittest_module(target)
    if runner == "callable":
        return _run_callable(target)
    if runner == "script":
        return _run_script(target)
    raise ValueError("unknown_current_root_runner:" + runner)


def _steps_for_profile(profile: str) -> tuple[CurrentRootStep, ...]:
    if profile == "repository":
        return REPOSITORY_LINEAGE_STEPS
    if profile == "planos":
        return PLANOS_ACTIVE_FRONTIER_STEPS
    if profile == "decisionos":
        return DECISIONOS_ACTIVE_FRONTIER_STEPS
    if profile == "memoryos":
        return MEMORYOS_ACTIVE_FRONTIER_STEPS
    if profile == "all":
        return CURRENT_ROOT_STEPS
    raise ValueError("unknown_current_root_profile:" + profile)


def list_current_root_steps(profile: str = "all") -> None:
    for ordinal, step in enumerate(_steps_for_profile(profile), start=1):
        print(f"{ordinal:03d}\t{step.step_id}\t{step.runner}\t{step.target}")


def run_current(profile: str = "all") -> int:
    steps = _steps_for_profile(profile)
    failures: list[str] = []
    total = len(steps)
    for ordinal, step in enumerate(steps, start=1):
        print(f"\n[{ordinal}/{total}] {step.step_id}", flush=True)
        try:
            status = _run_step(step.runner, step.target)
        except Exception as exc:
            status = 1
            print(
                f"current_root_exception:{step.step_id}:{type(exc).__name__}:{exc}",
                file=sys.stderr,
            )
        if status == 0:
            print(f"PASS: {step.step_id}", flush=True)
        else:
            print(f"FAIL: {step.step_id} exited with {status}", flush=True)
            if step.required:
                failures.append(step.step_id)
    if failures:
        print("\nCURRENT ROOT FAILED", file=sys.stderr)
        for step_id in failures:
            print(f"- {step_id}", file=sys.stderr)
        return 1
    print(
        "\nPASS: KuuOS integrated current root "
        f"({CURRENT_REPOSITORY_FRONTIER}; {CURRENT_PLANOS_FRONTIER}; "
        f"{CURRENT_DECISIONOS_FRONTIER}; {CURRENT_MEMORYOS_FRONTIER})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the KuuOS integrated current root.")
    parser.add_argument(
        "--profile",
        choices=("all", "repository", "planos", "decisionos", "memoryos"),
        default="all",
        help="Select one bounded validation surface. The default is all.",
    )
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)
    if args.summary:
        print(json.dumps(current_runtime_root_summary(), ensure_ascii=False, indent=2))
        return 0
    if args.list:
        list_current_root_steps(args.profile)
        return 0
    return run_current(args.profile)


if __name__ == "__main__":
    raise SystemExit(main())
