import unittest

from runtime.kuuos_runtime_daemon_efe_landscape_v0_1 import compile_efe_landscape, POLICY_COORDINATES

ACTIVE = {
    "selected_policy": "CONTINUE_HARMONIZED",
    "policy_free_energy_table": {
        "CONTINUE_HARMONIZED": {"expected_free_energy": 0.20},
        "CONTINUE_WITH_COMPACT_MONITOR": {"expected_free_energy": 0.30},
        "CONTINUE_AFTER_COMPACT": {"expected_free_energy": 0.35},
        "SLOW_DOWN_AND_REOBSERVE": {"expected_free_energy": 0.45},
        "BRANCH_EXPLORE_LIGHTLY": {"expected_free_energy": 0.40},
        "HOLD_WITH_RECOVERY": {"expected_free_energy": 0.60},
        "QUARANTINE_WITH_RETURN_PATH": {"expected_free_energy": 0.90},
    },
}

PRECISION = {
    "precision_weights": {
        "g_boundary": 0.9,
        "g_density": 0.7,
        "g_recovery": 0.6,
        "g_nonmarkov": 0.8,
    }
}


class EFELandscapeTests(unittest.TestCase):
    def test_compile_policy_manifold_landscape(self):
        result = compile_efe_landscape(ACTIVE, PRECISION, previous_policy="CONTINUE_HARMONIZED")
        self.assertEqual(result.landscape_status, "EFE_LANDSCAPE_COMPILED")
        self.assertEqual(result.selected_policy, "CONTINUE_HARMONIZED")
        self.assertIn("CONTINUE_HARMONIZED", result.landscape_table)
        self.assertIn("QUARANTINE_WITH_RETURN_PATH", result.landscape_table)
        self.assertIn("actioniveness", result.policy_coordinates["CONTINUE_HARMONIZED"])
        self.assertFalse(result.grants_execution_authority)

    def test_transition_distance_penalizes_far_policy_jump(self):
        result = compile_efe_landscape(ACTIVE, PRECISION, previous_policy="CONTINUE_HARMONIZED")
        near = result.landscape_table["CONTINUE_WITH_COMPACT_MONITOR"]["transition_distance"]
        far = result.landscape_table["QUARANTINE_WITH_RETURN_PATH"]["transition_distance"]
        self.assertGreater(far, near)

    def test_curvature_barrier_rises_with_boundary_policy(self):
        result = compile_efe_landscape(ACTIVE, PRECISION, previous_policy="CONTINUE_HARMONIZED")
        continue_barrier = result.landscape_table["CONTINUE_HARMONIZED"]["curvature_barrier"]
        quarantine_barrier = result.landscape_table["QUARANTINE_WITH_RETURN_PATH"]["curvature_barrier"]
        self.assertGreater(quarantine_barrier, continue_barrier)

    def test_smoothing_can_preserve_near_policy(self):
        active = {
            "selected_policy": "QUARANTINE_WITH_RETURN_PATH",
            "policy_free_energy_table": {
                policy: {"expected_free_energy": 0.2 if policy == "QUARANTINE_WITH_RETURN_PATH" else 0.25}
                for policy in POLICY_COORDINATES
            },
        }
        result = compile_efe_landscape(active, PRECISION, previous_policy="CONTINUE_HARMONIZED")
        self.assertIn(result.smoothed_selected_policy, POLICY_COORDINATES)
        self.assertGreaterEqual(result.landscape_table["QUARANTINE_WITH_RETURN_PATH"]["transition_distance"], result.transition_distance)


if __name__ == '__main__':
    unittest.main()
