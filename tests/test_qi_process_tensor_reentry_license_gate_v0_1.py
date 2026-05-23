import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_reentry_license_gate_v0_1 import (
    compile_qi_process_tensor_reentry_license_gate,
)


class QiProcessTensorReentryLicenseGateTests(unittest.TestCase):
    def test_hold_plan_denies_bounded_tick_license(self):
        gate = compile_qi_process_tensor_reentry_license_gate(
            {
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_HELD",
                "next_invocation_mode": "NO_REENTRY_UNTIL_OBSERVATION",
                "hold_until_observation": True,
            }
        )
        self.assertEqual(gate.gate_status, "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_HOLD")
        self.assertEqual(gate.license_decision, "NO_BOUNDED_TICK_LICENSE")
        self.assertFalse(gate.may_invoke_next_tick)
        self.assertFalse(gate.bounded_tick_license)
        self.assertIn("observation_or_quarantine_exit_required", gate.required_preconditions)
        self.assertFalse(gate.grants_execution_authority)

    def test_reobserve_plan_denies_bounded_tick_license(self):
        gate = compile_qi_process_tensor_reentry_license_gate(
            {
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_REOBSERVE_FIRST",
                "next_invocation_mode": "REOBSERVE_THEN_BOUNDED_REENTRY",
                "reobserve_before_reentry": True,
            }
        )
        self.assertEqual(gate.gate_status, "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_REOBSERVE")
        self.assertEqual(gate.denied_reason, "reobserve_required_before_reentry")
        self.assertFalse(gate.may_invoke_next_tick)
        self.assertIn("fresh_observation_required_before_reentry", gate.required_preconditions)

    def test_compact_plan_denies_bounded_tick_license(self):
        gate = compile_qi_process_tensor_reentry_license_gate(
            {
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST",
                "next_invocation_mode": "COMPACT_THEN_BOUNDED_REENTRY",
                "compact_before_reentry": True,
            }
        )
        self.assertEqual(gate.gate_status, "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_COMPACT")
        self.assertEqual(gate.denied_reason, "compaction_required_before_reentry")
        self.assertFalse(gate.may_invoke_next_tick)
        self.assertIn("trace_compaction_required_before_reentry", gate.required_preconditions)

    def test_ready_plan_grants_bounded_tick_license_without_execution_authority(self):
        gate = compile_qi_process_tensor_reentry_license_gate(
            {
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_READY",
                "next_invocation_mode": "BOUNDED_REENTRY_READY",
                "recommended_sleep_seconds": 0.25,
                "recommended_max_ticks": 4,
                "recommended_max_steps_per_tick": 3,
                "compact_before_reentry": False,
                "reobserve_before_reentry": False,
                "hold_until_observation": False,
            }
        )
        self.assertEqual(gate.gate_status, "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED")
        self.assertEqual(gate.license_decision, "BOUNDED_TICK_LICENSE_GRANTED")
        self.assertTrue(gate.may_invoke_next_tick)
        self.assertTrue(gate.bounded_tick_license)
        self.assertEqual(gate.licensed_sleep_seconds, 0.25)
        self.assertEqual(gate.licensed_max_ticks, 4)
        self.assertEqual(gate.licensed_max_steps_per_tick, 3)
        self.assertFalse(gate.grants_execution_authority)
        self.assertIn("executor_precondition_token", gate.allowed_projection)

    def test_unknown_plan_denies_license(self):
        gate = compile_qi_process_tensor_reentry_license_gate(
            {
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_UNKNOWN",
                "next_invocation_mode": "UNKNOWN_REENTRY_MODE",
            }
        )
        self.assertEqual(gate.gate_status, "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_UNKNOWN")
        self.assertFalse(gate.may_invoke_next_tick)
        self.assertEqual(gate.denied_reason, "unrecognized_or_incomplete_reentry_plan")
        self.assertIn("recognized_ready_plan_required", gate.required_preconditions)


if __name__ == "__main__":
    unittest.main()
