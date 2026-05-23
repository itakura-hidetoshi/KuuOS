import unittest

from runtime.kuuos_runtime_daemon_policy_flow_v0_1 import compile_policy_flow

COORDS = {
    "CONTINUE_HARMONIZED": {"actioniveness": 0.90, "boundary_intensity": 0.10, "observation_depth": 0.15, "recovery_depth": 0.10},
    "CONTINUE_WITH_COMPACT_MONITOR": {"actioniveness": 0.70, "boundary_intensity": 0.25, "observation_depth": 0.35, "recovery_depth": 0.20},
    "QUARANTINE_WITH_RETURN_PATH": {"actioniveness": 0.05, "boundary_intensity": 0.95, "observation_depth": 0.80, "recovery_depth": 0.75},
}


def landscape(policy, distance=0.0, curvature=0.0, smoothing=0.0):
    return {
        "selected_policy": policy,
        "smoothed_selected_policy": policy,
        "transition_distance": distance,
        "curvature_barrier": curvature,
        "harmonic_smoothing_penalty": smoothing,
        "policy_coordinates": COORDS,
    }


class PolicyFlowTests(unittest.TestCase):
    def test_stable_flow(self):
        result = compile_policy_flow(landscape("CONTINUE_HARMONIZED"), previous_policy="CONTINUE_HARMONIZED")
        self.assertEqual(result.flow_status, "POLICY_FLOW_STABLE")
        self.assertEqual(result.flow_distance, 0.0)
        self.assertFalse(result.grants_execution_authority)

    def test_near_transition(self):
        result = compile_policy_flow(landscape("CONTINUE_WITH_COMPACT_MONITOR"), previous_policy="CONTINUE_HARMONIZED")
        self.assertEqual(result.flow_status, "POLICY_FLOW_SMOOTH_LOCAL")
        self.assertGreater(result.flow_distance, 0.0)
        self.assertLessEqual(result.flow_distance, 0.35)
        self.assertEqual(len(result.geodesic_waypoints), 5)

    def test_far_transition_damped(self):
        result = compile_policy_flow(
            landscape("QUARANTINE_WITH_RETURN_PATH", distance=1.0, curvature=1.2, smoothing=0.7),
            previous_policy="CONTINUE_HARMONIZED",
        )
        self.assertEqual(result.flow_status, "POLICY_FLOW_DAMPED_TRANSITION")
        self.assertGreater(result.flow_distance, 0.35)
        self.assertLess(result.oscillation_damping, 0.5)


if __name__ == "__main__":
    unittest.main()
