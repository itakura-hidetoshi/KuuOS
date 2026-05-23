import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1 import (
    compile_qi_process_tensor_bounded_tick_invocation_boundary,
)


class QiProcessTensorBoundedTickInvocationBoundaryTests(unittest.TestCase):
    def test_missing_license_denies_single_tick_token(self):
        boundary = compile_qi_process_tensor_bounded_tick_invocation_boundary(
            {
                "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_HOLD",
                "license_decision": "NO_BOUNDED_TICK_LICENSE",
                "bounded_tick_license": False,
                "may_invoke_next_tick": False,
            }
        )
        self.assertEqual(boundary.boundary_status, "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_NO_LICENSE")
        self.assertEqual(boundary.invocation_decision, "NO_SINGLE_TICK_INVOCATION_TOKEN")
        self.assertFalse(boundary.single_tick_invocation_token)
        self.assertFalse(boundary.grants_execution_authority)
        self.assertEqual(boundary.denied_reason, "bounded_tick_license_missing_or_not_granted")

    def test_recursive_depth_denies_even_with_license(self):
        boundary = compile_qi_process_tensor_bounded_tick_invocation_boundary(
            {
                "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
                "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
                "bounded_tick_license": True,
                "may_invoke_next_tick": True,
                "licensed_max_steps_per_tick": 1,
            },
            requested_invocation_depth=1,
            max_allowed_invocation_depth=0,
        )
        self.assertEqual(boundary.boundary_status, "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_RECURSIVE")
        self.assertTrue(boundary.recursive_invocation_denied)
        self.assertFalse(boundary.single_tick_invocation_token)
        self.assertEqual(boundary.licensed_max_steps_per_tick, 0)

    def test_granted_license_emits_single_tick_token_without_execution_authority(self):
        boundary = compile_qi_process_tensor_bounded_tick_invocation_boundary(
            {
                "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
                "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
                "bounded_tick_license": True,
                "may_invoke_next_tick": True,
                "licensed_max_steps_per_tick": 3,
            }
        )
        self.assertEqual(boundary.boundary_status, "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_GRANTED_SINGLE_TICK")
        self.assertEqual(boundary.invocation_decision, "SINGLE_TICK_INVOCATION_TOKEN_GRANTED")
        self.assertTrue(boundary.single_tick_invocation_token)
        self.assertFalse(boundary.recursive_invocation_denied)
        self.assertFalse(boundary.grants_execution_authority)
        self.assertEqual(boundary.licensed_max_steps_per_tick, 3)
        self.assertIn("single_tick_invocation_token", boundary.allowed_projection)

    def test_max_steps_clamped_to_25(self):
        boundary = compile_qi_process_tensor_bounded_tick_invocation_boundary(
            {
                "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
                "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
                "bounded_tick_license": True,
                "may_invoke_next_tick": True,
                "licensed_max_steps_per_tick": 1000,
            }
        )
        self.assertEqual(boundary.licensed_max_steps_per_tick, 25)


if __name__ == "__main__":
    unittest.main()
