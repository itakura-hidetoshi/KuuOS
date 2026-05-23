import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class QiProcessTensorClosedLoopReceiptDaemonResultFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_closed_loop_receipt_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_closed_loop_receipt_path", fields)
        self.assertIn("closed_loop_receipt_status", fields)
        self.assertIn("closed_loop_next_state", fields)
        self.assertIn("closed_loop_observation_required", fields)
        self.assertIn("closed_loop_compact_required", fields)

    def test_daemon_result_contains_reentry_plan_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_reentry_plan_path", fields)
        self.assertIn("reentry_plan_status", fields)
        self.assertIn("reentry_next_invocation_mode", fields)
        self.assertIn("reentry_compact_before_reentry", fields)
        self.assertIn("reentry_reobserve_before_reentry", fields)
        self.assertIn("reentry_hold_until_observation", fields)

    def test_daemon_result_contains_reentry_license_gate_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_reentry_license_gate_path", fields)
        self.assertIn("reentry_license_decision", fields)
        self.assertIn("reentry_may_invoke_next_tick", fields)
        self.assertIn("reentry_bounded_tick_license", fields)
        self.assertIn("reentry_license_denied_reason", fields)

    def test_daemon_result_contains_invocation_boundary_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_bounded_tick_invocation_boundary_path", fields)
        self.assertIn("invocation_boundary_decision", fields)
        self.assertIn("single_tick_invocation_token", fields)
        self.assertIn("recursive_invocation_denied", fields)
        self.assertIn("invocation_boundary_denied_reason", fields)

    def test_daemon_result_contains_qi_projection_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_recoverability_projection_path", fields)
        self.assertIn("recoverability_status", fields)
        self.assertIn("dominant_recovery_path", fields)
        self.assertIn("recommended_recovery_action", fields)
        self.assertIn("recoverability_score", fields)
        self.assertIn("recovery_unsafe", fields)
        self.assertIn("local_recovery_allowed", fields)
        self.assertIn("qi_process_tensor_health_projection_path", fields)
        self.assertIn("qi_process_tensor_phase", fields)
        self.assertIn("daemon_health_status", fields)
        self.assertIn("next_operator_action", fields)
        self.assertIn("health_reason", fields)


if __name__ == "__main__":
    unittest.main()
