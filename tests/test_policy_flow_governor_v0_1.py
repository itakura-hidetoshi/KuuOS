import unittest

from runtime.kuuos_runtime_daemon_policy_flow_governor_v0_1 import compile_policy_flow_governor


def flow(current, target, distance, velocity, damping):
    return {
        "from_policy": current,
        "to_policy": target,
        "flow_distance": distance,
        "flow_velocity": velocity,
        "oscillation_damping": damping,
    }


class PolicyFlowGovernorTests(unittest.TestCase):
    def test_stable_no_ramp(self):
        result = compile_policy_flow_governor(flow("CONTINUE_HARMONIZED", "CONTINUE_HARMONIZED", 0.0, 1.0, 1.0))
        self.assertEqual(result.governor_status, "POLICY_FLOW_GOVERNOR_STABLE")
        self.assertEqual(result.transition_mode, "STABLE_NO_RAMP")
        self.assertEqual(result.governed_policy_advisory, "CONTINUE_HARMONIZED")
        self.assertFalse(result.grants_execution_authority)

    def test_near_transition_adopts_target(self):
        result = compile_policy_flow_governor(flow("CONTINUE_HARMONIZED", "CONTINUE_WITH_COMPACT_MONITOR", 0.25, 0.7, 0.8))
        self.assertEqual(result.governor_status, "POLICY_FLOW_GOVERNOR_LOCAL_ADVISORY")
        self.assertEqual(result.transition_mode, "LOCAL_SMOOTH_ADOPT")
        self.assertEqual(result.governed_policy_advisory, "CONTINUE_WITH_COMPACT_MONITOR")
        self.assertGreater(result.ramp_fraction, 0.0)

    def test_far_transition_ramps_without_adopting_target(self):
        result = compile_policy_flow_governor(flow("CONTINUE_HARMONIZED", "HOLD_WITH_RECOVERY", 0.75, 0.5, 0.45))
        self.assertEqual(result.governor_status, "POLICY_FLOW_GOVERNOR_RAMP")
        self.assertEqual(result.transition_mode, "RAMP_TOWARD_TARGET")
        self.assertEqual(result.governed_policy_advisory, "CONTINUE_HARMONIZED")
        self.assertLessEqual(result.max_step_fraction, 0.5)

    def test_low_damping_holds_transition(self):
        result = compile_policy_flow_governor(flow("CONTINUE_HARMONIZED", "QUARANTINE_WITH_RETURN_PATH", 1.1, 0.2, 0.2))
        self.assertEqual(result.governor_status, "POLICY_FLOW_GOVERNOR_HOLD_TRANSITION")
        self.assertEqual(result.transition_mode, "HOLD_TRANSITION_REOBSERVE")
        self.assertEqual(result.ramp_fraction, 0.0)
        self.assertEqual(result.governed_policy_advisory, "CONTINUE_HARMONIZED")


if __name__ == "__main__":
    unittest.main()
