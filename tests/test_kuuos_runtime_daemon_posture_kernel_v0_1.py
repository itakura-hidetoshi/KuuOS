import unittest

from runtime.kuuos_runtime_daemon_posture_kernel_v0_1 import compile_daemon_posture_kernel


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


class DaemonPostureKernelTests(unittest.TestCase):
    def test_balanced_inputs_continue_harmonized(self):
        result = compile_daemon_posture_kernel(inputs())
        self.assertEqual(result.final_runtime_posture, "CONTINUE_HARMONIZED")
        self.assertEqual(result.kernel_status, "POSTURE_KERNEL_HARMONIZED")
        self.assertGreater(result.posture_confidence, 0.6)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_boundary_pressure_dominates(self):
        result = compile_daemon_posture_kernel(inputs(
            yinyang_polarity_state="BOUNDARY_YIN_REQUIRED",
            qi_policy_mode="QUARANTINE_REVIEW",
            emptiness_action="HOLD_OR_QUARANTINE_NONFINAL",
            wa_posture="QUARANTINE_WITH_RETURN_PATH",
        ))
        self.assertEqual(result.final_runtime_posture, "QUARANTINE_WITH_RETURN_PATH")
        self.assertEqual(result.posture_reason, "boundary_pressure_dominates")
        self.assertEqual(result.boundary_pressure, 1.0)

    def test_recovery_need_dominates_after_boundary(self):
        result = compile_daemon_posture_kernel(inputs(
            four_image_phase="GREATER_YIN",
            wa_posture="HOLD_WITH_RECOVERY",
        ))
        self.assertEqual(result.final_runtime_posture, "HOLD_WITH_RECOVERY")
        self.assertEqual(result.kernel_status, "POSTURE_KERNEL_RECOVERY_HOLD")
        self.assertGreaterEqual(result.recovery_need, 0.8)

    def test_uncertainty_reobserves(self):
        result = compile_daemon_posture_kernel(inputs(
            yinyang_polarity_state="FALSE_YANG",
            qi_policy_mode="REOBSERVE_QI_PROCESS",
            qique_regime="OBSERVATION_GAP",
            missing_source_count=2,
        ))
        self.assertEqual(result.final_runtime_posture, "SLOW_DOWN_AND_REOBSERVE")
        self.assertEqual(result.kernel_status, "POSTURE_KERNEL_REOBSERVE")
        self.assertGreaterEqual(result.uncertainty_score, 0.6)

    def test_density_compacts(self):
        result = compile_daemon_posture_kernel(inputs(
            four_image_phase="GREATER_YANG",
            qique_regime="OVERDIFFUSION",
            tick_density=8,
            wa_posture="CONTINUE_HARMONIZED",
        ))
        self.assertEqual(result.final_runtime_posture, "CONTINUE_AFTER_COMPACT")
        self.assertEqual(result.posture_reason, "density_requires_compact_continue")
        self.assertGreaterEqual(result.density_pressure, 0.65)

    def test_stagnation_light_branch(self):
        result = compile_daemon_posture_kernel(inputs(
            yinyang_polarity_state="YIN_STAGNATION",
            four_image_phase="GREATER_YIN",
            wa_posture="BRANCH_EXPLORE_LIGHTLY",
        ))
        self.assertEqual(result.final_runtime_posture, "BRANCH_EXPLORE_LIGHTLY")
        self.assertEqual(result.kernel_status, "POSTURE_KERNEL_LIGHT_BRANCH")

    def test_wa_compact_is_preserved(self):
        result = compile_daemon_posture_kernel(inputs(
            wa_posture="CONTINUE_WITH_COMPACT_MONITOR",
            tick_density=2,
        ))
        self.assertEqual(result.final_runtime_posture, "CONTINUE_WITH_COMPACT_MONITOR")
        self.assertEqual(result.posture_reason, "wa_posture_preserved_compact")


if __name__ == "__main__":
    unittest.main()
