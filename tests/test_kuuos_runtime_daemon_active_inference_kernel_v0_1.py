import unittest

from runtime.kuuos_runtime_daemon_active_inference_kernel_v0_1 import (
    infer_daemon_belief_state,
    posterior_precision,
    run_active_inference_kernel,
    select_policy_by_expected_free_energy,
    variational_free_energy_proxy,
)


def inputs(**overrides):
    base = {
        "yinyang_polarity_state": "RECOVERY_YANG_PRESENT",
        "four_image_phase": "LESSER_YANG",
        "qi_policy_mode": "CONTINUE_WITH_QI_MEMORY_MONITOR",
        "qique_regime": "NONMARKOV_MEMORY_ACTIVE",
        "emptiness_action": "CONTINUE_ADVISORY_ONLY",
        "wa_posture": "CONTINUE_HARMONIZED",
        "tick_density": 2,
        "missing_source_count": 0,
    }
    base.update(overrides)
    return base


class DaemonActiveInferenceKernelTests(unittest.TestCase):
    def test_belief_state_is_inferred_from_sources(self):
        belief = infer_daemon_belief_state(inputs())
        self.assertEqual(belief["boundary_pressure"], 0.0)
        self.assertEqual(belief["uncertainty"], 0.0)
        self.assertGreater(belief["density_pressure"], 0.0)
        self.assertGreater(belief["action_drive"], 0.0)

    def test_precision_and_vfe_are_bounded(self):
        belief = infer_daemon_belief_state(inputs(
            yinyang_polarity_state="FALSE_YANG",
            qi_policy_mode="REOBSERVE_QI_PROCESS",
            qique_regime="OBSERVATION_GAP",
            missing_source_count=2,
        ))
        precision = posterior_precision(belief)
        vfe = variational_free_energy_proxy(belief)
        self.assertGreaterEqual(precision, 0.0)
        self.assertLessEqual(precision, 1.0)
        self.assertGreaterEqual(vfe, 0.0)
        self.assertLessEqual(vfe, 1.0)

    def test_balanced_case_selects_continue_harmonized_by_efe(self):
        result = run_active_inference_kernel(inputs())
        self.assertEqual(result.selected_policy, "CONTINUE_HARMONIZED")
        self.assertEqual(result.policy_selection_reason, "min_expected_free_energy")
        self.assertIsNone(result.hard_constraint_active)
        self.assertIn("CONTINUE_HARMONIZED", result.policy_free_energy_table)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_boundary_hard_constraint_selects_quarantine_return_path(self):
        result = run_active_inference_kernel(inputs(
            yinyang_polarity_state="BOUNDARY_YIN_REQUIRED",
            qi_policy_mode="QUARANTINE_REVIEW",
            emptiness_action="HOLD_OR_QUARANTINE_NONFINAL",
            wa_posture="QUARANTINE_WITH_RETURN_PATH",
        ))
        self.assertEqual(result.selected_policy, "QUARANTINE_WITH_RETURN_PATH")
        self.assertEqual(result.policy_selection_reason, "hard_boundary_constraint")
        self.assertEqual(result.hard_constraint_active, "boundary_pressure")
        self.assertEqual(result.posterior_belief_state["boundary_pressure"], 1.0)

    def test_uncertainty_selects_reobserve_by_expected_free_energy(self):
        result = run_active_inference_kernel(inputs(
            yinyang_polarity_state="FALSE_YANG",
            qi_policy_mode="REOBSERVE_QI_PROCESS",
            qique_regime="OBSERVATION_GAP",
            missing_source_count=2,
        ))
        self.assertEqual(result.selected_policy, "SLOW_DOWN_AND_REOBSERVE")
        self.assertEqual(result.policy_selection_reason, "min_expected_free_energy")
        self.assertGreaterEqual(result.posterior_belief_state["uncertainty"], 0.6)

    def test_density_selects_compact_continue(self):
        result = run_active_inference_kernel(inputs(
            four_image_phase="GREATER_YANG",
            qique_regime="OVERDIFFUSION",
            tick_density=8,
            wa_posture="CONTINUE_HARMONIZED",
        ))
        self.assertEqual(result.selected_policy, "CONTINUE_AFTER_COMPACT")
        self.assertGreaterEqual(result.posterior_belief_state["density_pressure"], 0.65)

    def test_recovery_can_select_hold_with_recovery(self):
        result = run_active_inference_kernel(inputs(
            four_image_phase="GREATER_YIN",
            wa_posture="HOLD_WITH_RECOVERY",
            qi_policy_mode="CONTINUE_WITH_QI_MEMORY_MONITOR",
        ))
        self.assertEqual(result.selected_policy, "HOLD_WITH_RECOVERY")
        self.assertGreaterEqual(result.posterior_belief_state["recovery_need"], 0.8)

    def test_policy_table_minimum_matches_selected(self):
        belief = infer_daemon_belief_state(inputs(tick_density=6, qique_regime="OVERDIFFUSION"))
        selected, table, reason, hard = select_policy_by_expected_free_energy(belief)
        min_policy = min(table, key=lambda policy: table[policy]["expected_free_energy"])
        self.assertEqual(selected, min_policy)
        self.assertEqual(reason, "min_expected_free_energy")
        self.assertIsNone(hard)


if __name__ == "__main__":
    unittest.main()
