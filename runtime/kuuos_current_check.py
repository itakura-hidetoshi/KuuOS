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
CURRENT_MEMORYOS_FRONTIER = "MemoryOS v0.49"
CURRENT_WORLD_DEPENDENCY = "KuuOS v14.0 causal WORLD state"
CURRENT_BASELINE_DATE = "2026-07-14 JST"

CURRENT_MAIN_FRONTIER = CURRENT_REPOSITORY_FRONTIER
CURRENT_DRAFT_FRONTIER = "none"
CURRENT_DRAFT_PR = "none"
CURRENT_DRAFT_BRANCH = "none"
CURRENT_FRONTIER_ARTIFACT = (
    "runtime/kuuos_memoryos_candidate_nullspace_dephasing_rank_"
    "stratification_certificate_kernel_v0_1.py"
)
CURRENT_FRONTIER_MODE = "integrated_active_frontiers"
CURRENT_FRONTIER_BOUNDARY = "validation_only"


def _script_step(step_id: str, target: str, description: str) -> CurrentRootStep:
    return CurrentRootStep(step_id, "script", target, True, description)


PLANOS_ACTIVE_FRONTIER_SPECS: tuple[tuple[str, str, str], ...] = (
    (
        "planos-v0-91-information-geometric-qi-objective",
        "scripts/check_planos_information_geometric_qi_objective_kernel_v0_1.py",
        "Validate the executable information-geometric Qi objective kernel.",
    ),
    (
        "planos-v0-92-kl-regularized-objective-update",
        "scripts/check_planos_kl_regularized_objective_update_kernel_v0_92.py",
        "Validate support-preserving KL-regularized objective updating.",
    ),
    (
        "planos-v0-93-zero-temperature-limit",
        "scripts/check_planos_zero_temperature_minimal_action_limit_kernel_v0_1.py",
        "Validate complete minimal-action support in the zero-temperature limit.",
    ),
    (
        "planos-v0-94-finite-temperature-concentration",
        "scripts/check_planos_finite_temperature_concentration_certificate_kernel_v0_1.py",
        "Validate finite-temperature concentration evidence.",
    ),
    (
        "planos-v0-95-adaptive-qi-temperature",
        "scripts/check_planos_adaptive_qi_temperature_calibration_kernel_v0_1.py",
        "Validate bounded Qi-conditioned temperature calibration.",
    ),
    (
        "planos-v0-96-temperature-hysteresis-rate-limit",
        "scripts/check_planos_temperature_hysteresis_rate_limit_kernel_v0_1.py",
        "Validate hysteresis, rate limits, and oscillation protection.",
    ),
    (
        "planos-v0-97-temperature-trajectory-receipt",
        "scripts/check_planos_temperature_trajectory_receipt_kernel_v0_1.py",
        "Validate the future-only temperature trajectory receipt.",
    ),
    (
        "planos-v0-98-temperature-trajectory-stability",
        "scripts/check_planos_temperature_trajectory_stability_certificate_kernel_v0_1.py",
        "Validate finite-window non-Markov temperature stability.",
    ),
    (
        "planos-v0-99-qi-conditioned-information-metric",
        "scripts/check_planos_qi_conditioned_information_metric_certificate_kernel_v0_1.py",
        "Validate the Qi- and history-conditioned information metric.",
    ),
    (
        "planos-v1-00-world-conditioned-pullback-metric",
        "scripts/check_planos_world_conditioned_path_projection_pullback_metric_kernel_v0_1.py",
        "Validate read-only WORLD projection and pullback geometry.",
    ),
    (
        "planos-v1-01-world-conditioned-distribution-update",
        "scripts/check_planos_world_conditioned_objective_distribution_update_kernel_v0_1.py",
        "Validate the WORLD-conditioned future candidate distribution.",
    ),
    (
        "planos-v1-02-decision-handoff-certificate",
        "scripts/check_planos_world_conditioned_distribution_decision_handoff_certificate_kernel_v0_1.py",
        "Validate the advisory distribution handoff to DecisionOS.",
    ),
    (
        "planos-v1-05-native-coupled-information-metric",
        "scripts/check_planos_native_coupled_information_metric_certificate_kernel_v0_1.py",
        "Validate the bounded non-diagonal Gram-coupled PlanOS metric.",
    ),
    (
        "planos-v1-06-state-dependent-metric-jet-levi-civita",
        "scripts/check_planos_state_dependent_metric_jet_levi_civita_certificate_kernel_v0_1.py",
        "Validate the bounded state-dependent metric jet and Levi-Civita connection.",
    ),
    (
        "planos-v1-07-second-order-metric-jet-curvature",
        "scripts/check_planos_second_order_metric_jet_curvature_certificate_kernel_v0_1.py",
        "Validate the bounded second-order metric jet, curvature, and holonomy.",
    ),
    (
        "planos-v1-08-multi-chart-atlas-curvature",
        "scripts/check_planos_multi_chart_atlas_curvature_certificate_kernel_v0_1.py",
        "Validate multi-chart atlas compatibility, cocycles, boundaries, and curvature invariance.",
    ),
    (
        "planos-v1-09-jacobi-geodesic-deviation",
        "scripts/check_planos_jacobi_geodesic_deviation_certificate_kernel_v0_1.py",
        "Validate bounded geodesic deviation, Jacobi fields, tidal acceleration, and local conjugate-point candidates.",
    ),
    (
        "planos-v1-10-second-variation-morse-index",
        "scripts/check_planos_second_variation_morse_index_certificate_kernel_v0_1.py",
        "Validate endpoint-fixed second variation, the index form, finite-basis Morse index, and nullity.",
    ),
    (
        "planos-v1-11-conjugate-events-injectivity-radius",
        "scripts/check_planos_conjugate_event_sequence_injectivity_radius_certificate_kernel_v0_1.py",
        "Validate piecewise geodesic continuity, conjugate-event index jumps, cut candidates, and a local injectivity-radius lower bound.",
    ),
    (
        "planos-v1-12-exponential-normal-coordinate-ball",
        "scripts/check_planos_exponential_map_normal_coordinate_ball_certificate_kernel_v0_1.py",
        "Validate the bounded second-order exponential model, normal-coordinate ball, finite-sample injectivity, and chart-safe radial covering.",
    ),
    (
        "planos-v1-13-finite-normal-ball-cover-hopf-rinow-witness",
        "scripts/check_planos_finite_normal_ball_cover_hopf_rinow_witness_certificate_kernel_v0_1.py",
        "Validate finite normal-ball coverage, overlap-connected local geodesic extension, and the bounded finite-window Hopf-Rinow witness.",
    ),
    (
        "planos-v1-14-finite-cover-nerve-cech-path-homotopy",
        "scripts/check_planos_finite_cover_nerve_cech_path_homotopy_certificate_kernel_v0_1.py",
        "Validate finite nerve edges, Cech two-simplices, connectedness, and elementary endpoint-preserving path homotopy.",
    ),
    (
        "planos-v1-15-finite-simplicial-chain-homology",
        "scripts/check_planos_finite_simplicial_chain_homology_certificate_kernel_v0_1.py",
        "Validate finite simplicial boundary maps, cycle and filling witnesses, rational Betti numbers, and a bounded first-homology obstruction.",
    ),
    (
        "planos-v1-16-smith-normal-form-integer-homology",
        "scripts/check_planos_smith_normal_form_integer_homology_certificate_kernel_v0_1.py",
        "Validate the finite integer H1 presentation, Smith invariant factors, free rank, and torsion decomposition.",
    ),
    (
        "planos-v1-17-finite-filtration-persistent-homology",
        "scripts/check_planos_finite_filtration_persistent_homology_certificate_kernel_v0_1.py",
        "Validate finite filtration closure, stagewise Smith data, F2 barcode intervals, and persistent Betti numbers.",
    ),
    (
        "planos-v1-18-finite-bottleneck-persistence-stability",
        "scripts/check_planos_finite_bottleneck_persistence_stability_certificate_kernel_v0_1.py",
        "Validate finite diagram matching, exact bottleneck distance, diagonal costs, and the bounded perturbation stability witness.",
    ),
    (
        "planos-v1-19-finite-p-wasserstein-persistence-transport",
        "scripts/check_planos_finite_p_wasserstein_persistence_transport_certificate_kernel_v0_1.py",
        "Validate finite p-Wasserstein transport, exact power sums, integer root brackets, moment profiles, and tail bounds.",
    ),
    (
        "planos-v1-20-finite-wasserstein-frechet-barycenter-dispersion",
        "scripts/check_planos_finite_wasserstein_frechet_barycenter_dispersion_certificate_kernel_v0_1.py",
        "Validate finite weighted Wasserstein Frechet functionals, barycenter tie sets, consensus transports, and dispersion bounds.",
    ),
    (
        "planos-v1-21-finite-physical-quantum-qi-path-history-noncollapse",
        "scripts/check_planos_finite_physical_quantum_qi_path_history_noncollapse_certificate_kernel_v0_1.py",
        "Validate finite Physical Quantum Qi path histories, exact phase interference, reconvergence, marginals, loops, and non-collapse.",
    ),
    (
        "planos-v1-22-finite-gaussian-physical-quantum-qi-homotopy-decoherence",
        "scripts/check_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate_kernel_v0_1.py",
        "Validate exact Z4 Gaussian path amplitudes, homotopy-class blocks, decoherence decomposition, and history non-collapse.",
    ),
    (
        "planos-v1-23-finite-physical-quantum-qi-coherence-kernel-partial-dephasing",
        "scripts/check_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate_kernel_v0_1.py",
        "Validate the exact finite Gaussian coherence kernel, rational partial dephasing, purity, mixedness, and history non-collapse.",
    ),
)

PLANOS_ACTIVE_FRONTIER_STEPS: tuple[CurrentRootStep, ...] = tuple(
    _script_step(*spec) for spec in PLANOS_ACTIVE_FRONTIER_SPECS
)

DECISIONOS_ACTIVE_FRONTIER_STEPS: tuple[CurrentRootStep, ...] = (
    _script_step(
        "decisionos-v0-1-v0-6-cumulative",
        "scripts/run_decision_os_full_checks.py",
        "Validate DecisionOS through WORLD-conditioned relational deliberation v0.6.",
    ),
)

MEMORYOS_ACTIVE_FRONTIER_STEPS: tuple[CurrentRootStep, ...] = (
    _script_step(
        "memoryos-v0-40-observer-relative-non-markov-temporal-record",
        "scripts/check_memoryos_observer_relative_non_markov_temporal_record_certificate_kernel_v0_1.py",
        "Validate observer-relative append-only records, visible translation residue, and finite non-Markov history dependence across PlanOS, DecisionOS, ObserveOS, and MemoryOS.",
    ),
    _script_step(
        "memoryos-v0-41-observer-relative-finite-window-qi-influence-planos-handoff",
        "scripts/check_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_certificate_kernel_v0_1.py",
        "Validate source-bound finite-window Qi influence, exact visible tail residue, and complete PlanOS v1.23 history-support preservation.",
    ),
    _script_step(
        "memoryos-v0-42-observer-relative-non-markov-influence-conditioned-planos-coherence-kernel",
        "scripts/check_planos_memoryos_observer_relative_non_markov_influence_conditioned_coherence_kernel_certificate_kernel_v0_1.py",
        "Validate exact memory-conditioned diagonal phase congruence, visible tail-sensitive coherence, Hermitian symmetry, diagonal normalization, PSD witness preservation, and full PlanOS support.",
    ),
    _script_step(
        "memoryos-v0-43-observer-relative-temporal-window-coherence-cocycle-composition",
        "scripts/check_planos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1.py",
        "Validate source-bound temporal segment composition, observer translation compatibility, window refinement/coarsening consistency, and exact equality with the MemoryOS v0.42 conditioned PlanOS coherence kernel.",
    ),
    _script_step(
        "memoryos-v0-44-observer-relative-coherence-quadratic-evidence-decisionos-handoff",
        "scripts/check_planos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1.py",
        "Validate exact PSD quadratic coherence evidence for every retained DecisionOS candidate while preserving relational frontier, required review, dissent, minority protection, and non-selection boundaries.",
    ),
    _script_step(
        "memoryos-v0-45-candidate-gram-lift-decisionos-relational-coherence-kernel",
        "scripts/check_planos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1.py",
        "Validate the complete candidate Gram lift, exact v0.44 diagonal recovery, PSD and Hermitian preservation, full candidate-pair support, and DecisionOS relational review boundaries.",
    ),
    _script_step(
        "memoryos-v0-46-candidate-pair-cauchy-schwarz-relational-coherence-envelope",
        "scripts/check_planos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1.py",
        "Validate exact candidate-pair Cauchy-Schwarz margins, normalized coherence-square bounds, zero-diagonal coherence extinction, complete ordered-pair support, and DecisionOS relational review boundaries.",
    ),
    _script_step(
        "memoryos-v0-47-candidate-triple-gram-determinant-joint-coherence-compatibility",
        "scripts/check_planos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1.py",
        "Validate complete ordered candidate-triple support, exact 3x3 Gram principal minors, rank-two determinant saturation, cyclic-coherence signs, joint pair-envelope compatibility, and DecisionOS relational review boundaries.",
    ),
    _script_step(
        "memoryos-v0-48-two-history-candidate-gram-factorization-reconstruction",
        "scripts/check_planos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1.py",
        "Validate exact two-history factor rows, complete 4x4 candidate-kernel reconstruction, row and column relations, full determinant zero, v0.47 triple binding, and DecisionOS relational review boundaries.",
    ),
    _script_step(
        "memoryos-v0-49-candidate-nullspace-dephasing-rank-stratification",
        "scripts/check_planos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1.py",
        "Validate exact structural null relations, null-translation invariance, coherence-dependent null release, rank and nullity trajectories, and DecisionOS relational review boundaries.",
    ),
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
    outcome = getattr(module, function_name)()
    return int(outcome)


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
        [sys.executable, str(script)],
        cwd=ROOT,
        env=env,
        check=False,
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
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print the machine-readable current root summary and exit.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the selected root steps and exit.",
    )
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
