#!/usr/bin/env python3
"""Top-level KuuOS governance check runner."""

from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/run_ai_yogacara_full_checks_v0_1.py"],
    [sys.executable, "scripts/run_core_governance_full_checks_v0_1.py"],
    [sys.executable, "scripts/validate_gpt_github_integration_v0_1.py"],
    [sys.executable, "scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py"],
    [sys.executable, "scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_do_two_truths_runtime_release_packet_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_do_two_truths_runtime_release_bundle_manifest_v0_1.py"],
    [sys.executable, "scripts/validate_mass_gap_two_truths_engine_bridge_v0_1.py"],
    [sys.executable, "scripts/validate_mass_gap_memory_reflection_record_bridge_v0_1.py"],
    [sys.executable, "scripts/validate_memoryos_github_external_memory_v0_1.py"],
    [sys.executable, "scripts/run_qi_motion_chain_checks_v0_1.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_runtime_release_packet_v0_1.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_equations_v0_2.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_equation_packet_v0_2.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_non_markov_memory_v0_2E.py"],
    [sys.executable, "tests/test_physical_quantum_qi_non_markov_memory_v0_2E.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_process_tensor_v0_2F.py"],
    [sys.executable, "tests/test_physical_quantum_qi_process_tensor_v0_2F.py"],
    [sys.executable, "scripts/validate_kuuos_qi_process_tensor_conventional_autonomy_v0_2G.py"],
    [sys.executable, "tests/test_kuuos_qi_process_tensor_conventional_autonomy_v0_2G.py"],
    [sys.executable, "scripts/validate_qi_process_tensor_release_chain_docs_v0_2FG.py"],
    [sys.executable, "scripts/validate_qi_process_tensor_v0_2FG_docs_closure_addendum_packet.py"],
    [sys.executable, "scripts/validate_qi_bensho_treatment_route_candidate_v0_2J.py"],
    [sys.executable, "scripts/validate_qi_bensho_decisionos_clinician_handoff_v0_2K.py"],
    [sys.executable, "scripts/validate_qi_clinical_red_flag_handover_governor_v0_2L.py"],
    [sys.executable, "scripts/check_qi_clinical_red_flag_consultation_governor_finality_v0_2L.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_observation_kernel_v0_2M.py"],
    [sys.executable, "tests/test_physical_quantum_qi_observation_kernel_v0_2M.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_state_transition_kernel_v0_2N.py"],
    [sys.executable, "tests/test_physical_quantum_qi_state_transition_kernel_v0_2N.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_transition_trajectory_ledger_v0_2O.py"],
    [sys.executable, "tests/test_physical_quantum_qi_transition_trajectory_ledger_v0_2O.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py"],
    [sys.executable, "tests/test_physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_phase_transition_response_governor_v0_2Q.py"],
    [sys.executable, "tests/test_physical_quantum_qi_phase_transition_response_governor_v0_2Q.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_response_feedback_loop_v0_2R.py"],
    [sys.executable, "tests/test_physical_quantum_qi_response_feedback_loop_v0_2R.py"],
    [sys.executable, "scripts/check_physical_quantum_qi_runtime_evolution_ci_receipt_v0_2JR.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.py"],
    [sys.executable, "scripts/check_physical_quantum_qi_runtime_evolution_finality_packet_v0_2JR.py"],
    [sys.executable, "scripts/check_physical_quantum_qi_runtime_evolution_finality_post_merge_receipt_v0_2JR.py"],
    [sys.executable, "scripts/check_physical_quantum_qi_runtime_evolution_baseline_lock_v0_2S.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_dpi_recoverability_v0_2C.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_indranet_gauge_transport_v0_2D.py"],
    [sys.executable, "tests/test_physical_quantum_qi_indranet_gauge_transport_v0_2D.py"],
    [sys.executable, "tests/test_physical_quantum_qi_indranet_transport_runtime_v0_2D.py"],
    [sys.executable, "tests/test_physical_quantum_qi_indranet_planos_handoff_v0_2D.py"],
    [sys.executable, "examples/run_physical_quantum_qi_indranet_planos_handoff_demo_v0_2D.py"],
    [sys.executable, "tests/test_physical_quantum_qi_phase_runtime_v0_2.py"],
    [sys.executable, "tests/test_physical_quantum_qi_os_bridge_v0_2.py"],
    [sys.executable, "tests/test_physical_quantum_qi_memory_record_v0_2.py"],
    [sys.executable, "tests/test_physical_quantum_qi_ward_leak_v0_2B_deepening.py"],
    [sys.executable, "examples/run_physical_quantum_qi_phase_demo_v0_2.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_deepening_v0_2.py"],
    [sys.executable, "scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py"],
    [sys.executable, "scripts/validate_qi_process_tensor_release_chain_v0_2FG.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_pr9_merge_closure_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py"],
    [sys.executable, "scripts/check_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py"],
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    completed = subprocess.run(list(cmd), cwd=ROOT)
    return completed.returncode


def main() -> int:
    failures: list[tuple[list[str], int]] = []
    for cmd in COMMANDS:
        code = run_command(cmd)
        if code != 0:
            failures.append((cmd, code))
            break

    if failures:
        for cmd, code in failures:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
        return 1

    print("\nPASS: KuuOS all governance full checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())