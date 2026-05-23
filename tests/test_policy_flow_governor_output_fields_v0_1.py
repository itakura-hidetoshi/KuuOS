import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class PolicyFlowGovernorOutputFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_policy_flow_governor_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("policy_flow_governor_path", fields)
        self.assertIn("governed_policy_advisory", fields)
        self.assertIn("policy_flow_transition_mode", fields)
        self.assertIn("policy_flow_ramp_fraction", fields)
        self.assertIn("policy_flow_max_step_fraction", fields)


if __name__ == "__main__":
    unittest.main()
