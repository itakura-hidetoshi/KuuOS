#!/usr/bin/env python3
from __future__ import annotations

import importlib
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CHECK_MODULES = [
    "scripts.validate_kuuos_runtime_manifest_v0_1",
    "scripts.validate_kuuos_validator_tiering_policy_v0_1",
    "scripts.check_adaptive_agent_reference_architecture_v1_0",
    "scripts.validate_cbf_membrane_gap_kernel_contract_v1_0",
    "scripts.check_cbf_membrane_gap_validation_cases_v1_0",
    "scripts.validate_cbf_membrane_gap_kernel_established_packet_v1_0",
    "scripts.validate_daemon_core_boundary_policy_v0_1",
    "scripts.validate_qi_bounded_tick_manual_runner_manifest_addendum_v0_1",
    "scripts.check_qi_bounded_tick_executor_receipt_contract_cases_v0_1",
    "scripts.check_kuuos_example_runner_import_v0_1",
    "scripts.check_kuuos_state_io_example_v0_1",
    "scripts.check_kuuos_qi_process_tensor_example_v0_1",
    "scripts.check_qi_bounded_tick_manual_runner_example_v0_1",
    "scripts.check_kuuos_runtime_daemon_example_v0_1",
    "scripts.check_qi_routed_cycle_projection_plan_example_v0_1",
    "scripts.check_qi_daemon_once_operator_cli_v0_1",
    "scripts.check_qi_daemon_once_operator_docs_v0_1",
    "scripts.check_qi_supervised_loop_operator_cli_v0_1",
    "scripts.check_qi_controlled_loop_operator_cli_v0_1",
    "scripts.check_qi_persistent_supervisor_operator_cli_v0_1",
    "scripts.check_qi_persistent_supervisor_status_view_cli_v0_1",
    "scripts.check_qi_supervisor_control_writer_v0_1",
    "scripts.check_qi_persistent_supervisor_runbook_v0_1",
    "scripts.check_qi_persistent_supervisor_operator_e2e_v0_1",
    "scripts.check_qi_persistent_supervisor_profile_runner_v0_1",
    "scripts.check_qi_persistent_supervisor_profile_validator_v0_1",
    "scripts.check_qi_supervisorctl_v0_1",
    "scripts.check_decision_os_wa_relational_harmony_v0_3",
    "scripts.check_plan_os_replan_bound_synthesis_v0_1",
    "scripts.check_plan_os_qi_conditioned_nonmarkov_replan_v0_2",
    "scripts.check_plan_os_next_cycle_basis_compiler_adapter_v0_3",
    "scripts.check_plan_os_closed_loop_replan_intake_adapter_v0_4",
    "scripts.check_plan_os_generational_replan_cycle_driver_v0_5",
    "scripts.check_act_os_authority_bound_invocation_v0_1",
    "scripts.check_act_os_replan_lineage_authority_envelope_v0_2",
    "scripts.check_observe_os_effect_grounded_observation_v0_1",
    "scripts.check_observe_os_replan_lineage_observation_envelope_v0_2",
    "scripts.check_verify_os_evidence_bound_verification_v0_1",
    "scripts.check_verify_os_replan_lineage_verification_envelope_v0_2",
    "scripts.check_learn_os_future_only_evidence_learning_v0_1",
    "scripts.check_learn_os_replan_lineage_future_only_learning_envelope_v0_2",
    "scripts.check_qi_world_self_adjoint_lean_receipt_bridge_v0_28",
    "scripts.check_world_noncommutative_operator_algebra_module_v0_29",
    "scripts.check_world_cstar_local_net_bridge_v0_30",
    "scripts.check_world_von_neumann_bicommutant_bridge_v0_31",
    "scripts.check_world_standard_form_modular_flow_bridge_v0_32",
    "scripts.check_world_modular_state_kms_relative_flow_bridge_v0_33",
    "scripts.check_world_araki_relative_entropy_bridge_v0_34",
    "scripts.check_world_petz_recovery_sufficiency_bridge_v0_35",
    "scripts.check_world_conditional_expectation_takesaki_bridge_v0_36",
    "scripts.check_world_jones_basic_construction_index_bridge_v0_37",
    "scripts.check_world_jones_tower_standard_invariant_bridge_v0_38",
    "scripts.check_world_canonical_endomorphism_qsystem_frobenius_bridge_v0_39",
]

TEST_MODULES = [
    "tests.test_cbf_membrane_gap_kernel_contract_v1_0",
    "tests.test_cbf_membrane_gap_validation_cases_v1_0",
    "tests.test_cbf_membrane_gap_established_packet_v1_0",
    "tests.test_validate_daemon_core_boundary_policy_v0_1",
    "tests.test_qi_process_tensor_v0_1",
    "tests.test_qi_process_tensor_downstream_v0_1",
    "tests.test_kuuos_closed_loop_v0_1",
    "tests.test_kuuos_closed_loop_driver_v0_1",
    "tests.test_kuuos_state_io_runner_v0_1",
    "tests.test_kuuos_runtime_daemon_v0_1",
    "tests.test_kuuos_runtime_daemon_wa_output_v0_1",
    "tests.test_kuuos_runtime_daemon_active_inference_output_v0_1",
    "tests.test_kuuos_runtime_daemon_status_v0_1",
    "tests.test_kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1",
    "tests.test_kuuos_runtime_daemon_four_image_phase_gauge_v0_1",
    "tests.test_kuuos_runtime_daemon_qi_policy_v0_1",
    "tests.test_kuuos_runtime_daemon_qique_gauge_v0_1",
    "tests.test_kuuos_runtime_daemon_emptiness_gate_v0_1",
    "tests.test_kuuos_runtime_daemon_wa_function_v0_1",
    "tests.test_kuuos_runtime_daemon_active_inference_feature_compiler_v0_1",
    "tests.test_kuuos_runtime_daemon_active_inference_kernel_v0_1",
    "tests.test_kuuos_runtime_daemon_belief_state_manifold_v0_1",
    "tests.test_kuuos_runtime_daemon_precision_geometry_v0_1",
    "tests.test_kuuos_runtime_daemon_efe_landscape_v0_1",
    "tests.test_policy_flow_v0_1",
    "tests.test_policy_flow_output_fields_v0_1",
    "tests.test_policy_flow_governor_v0_1",
    "tests.test_policy_flow_governor_output_fields_v0_1",
    "tests.test_qi_process_tensor_actuator_v0_1",
    "tests.test_qi_process_tensor_actuator_output_fields_v0_1",
    "tests.test_qi_process_tensor_tick_scheduler_output_fields_v0_1",
    "tests.test_qi_process_tensor_closed_loop_receipt_v0_1",
    "tests.test_qi_process_tensor_reentry_plan_v0_1",
    "tests.test_qi_process_tensor_reentry_license_gate_v0_1",
    "tests.test_qi_process_tensor_bounded_tick_invocation_boundary_v0_1",
    "tests.test_qi_process_tensor_bounded_tick_executor_v0_1",
    "tests.test_qi_process_tensor_bounded_tick_manual_runner_v0_1",
    "tests.test_qi_bounded_tick_executor_receipt_validator_v0_1",
    "tests.test_qi_process_tensor_health_projection_v0_1",
    "tests.test_qi_process_tensor_recoverability_projection_v0_1",
    "tests.test_qi_process_tensor_observation_debt_scheduler_v0_1",
    "tests.test_qi_process_tensor_trace_compaction_planner_v0_1",
    "tests.test_qi_projection_output_writer_v0_1",
    "tests.test_qi_projection_summary_bridge_runner_v0_1",
    "tests.test_qi_projection_summary_plan_bridge_runner_v0_1",
    "tests.test_qi_routed_cycle_projection_plan_runner_v0_1",
    "tests.test_qi_projection_plan_readable_summary_v0_1",
    "tests.test_qi_supervised_loop_runner_v0_1",
    "tests.test_qi_supervised_loop_control_v0_1",
    "tests.test_qi_controlled_loop_runner_v0_1",
    "tests.test_qi_persistent_supervisor_v0_1",
    "tests.test_qi_persistent_supervisor_status_view_v0_1",
    "tests.test_qi_process_tensor_advantage_metrics_v0_1",
    "tests.test_qi_runtime_output_surface_v0_1",
    "tests.test_qi_runtime_output_action_router_v0_1",
    "tests.test_qi_runtime_output_action_dispatcher_v0_1",
    "tests.test_qi_routed_daemon_cycle_runner_v0_1",
    "tests.test_qi_recovery_feedback_bridge_v0_1",
    "tests.test_qi_policy_feedback_surface_v0_1",
    "tests.test_qi_policy_feedback_candidate_adapter_v0_1",
    "tests.test_qi_policy_candidate_admission_gate_v0_1",
    "tests.test_qi_admitted_policy_candidate_handoff_v0_1",
    "tests.test_qi_policy_flow_handoff_receiver_v0_1",
    "tests.test_qi_policy_flow_candidate_inbox_v0_1",
    "tests.test_qi_policy_flow_candidate_intake_view_v0_1",
    "tests.test_qi_policy_flow_candidate_shadow_evaluator_v0_1",
    "tests.test_qi_policy_flow_candidate_shadow_admission_gate_v0_1",
    "tests.test_qi_routed_cycle_operational_summary_v0_1",
    "tests.test_qi_next_runtime_mode_plan_v0_1",
    "tests.test_qi_bounded_reentry_cycle_runner_v0_1",
    "tests.test_qi_reentry_handoff_chain_runner_v0_1",
    "tests.test_qi_reentry_chain_controller_v0_1",
    "tests.test_qi_managed_reentry_chain_runner_v0_1",
    "tests.test_qi_managed_daemon_cycle_runner_v0_1",
    "tests.test_qi_process_tensor_closed_loop_receipt_daemon_result_fields_v0_1",
    "tests.test_kuuos_runtime_daemon_geometric_chain_fields_v0_1",
]


def run_checks() -> list[str]:
    errors: list[str] = []
    for name in CHECK_MODULES:
        module = importlib.import_module(name)
        result = module.main()
        if result != 0:
            errors.append(f"{name} returned {result}")
    return errors


def run_unittests() -> list[str]:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for name in TEST_MODULES:
        suite.addTests(loader.loadTestsFromName(name))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        return []
    return [f"unittest failures={len(result.failures)} errors={len(result.errors)}"]


def main() -> int:
    errors = []
    errors.extend(run_checks())
    errors.extend(run_unittests())
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuuOS runtime full check v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
