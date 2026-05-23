import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class PolicyFlowOutputFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_policy_flow_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("policy_flow_path", fields)
        self.assertIn("policy_flow_from_policy", fields)
        self.assertIn("policy_flow_to_policy", fields)
        self.assertIn("policy_flow_distance", fields)
        self.assertIn("policy_flow_velocity", fields)
        self.assertIn("policy_flow_oscillation_damping", fields)


if __name__ == "__main__":
    unittest.main()
