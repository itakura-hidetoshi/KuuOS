import unittest

from scripts.validate_qi_bounded_tick_executor_receipt_v0_1 import validate_receipt


BASE_INVOKED = {
    "executor_version": "kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1",
    "executor_status": "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED",
    "source_gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
    "source_license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
    "source_boundary_status": "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_GRANTED_SINGLE_TICK",
    "source_invocation_decision": "SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
    "bounded_tick_license": True,
    "single_tick_invocation_token": True,
    "tick_invoked": True,
    "denied_reason": None,
    "steps_run": 1,
    "licensed_max_steps_per_tick": 1,
    "run_manifest_path": "/tmp/run_manifest_v0_1.json",
    "next_raw_state_path": "/tmp/next_raw_state_v0_1.json",
    "state_bundle_path": "/tmp/state_bundle_v0_1.json",
    "step_trace_path": "/tmp/step_trace_v0_1.json",
    "grants_execution_authority": True,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

BASE_DENIED = {
    "executor_version": "kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1",
    "executor_status": "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED",
    "source_gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_HOLD",
    "source_license_decision": "NO_BOUNDED_TICK_LICENSE",
    "source_boundary_status": "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_NO_LICENSE",
    "source_invocation_decision": "NO_SINGLE_TICK_INVOCATION_TOKEN",
    "bounded_tick_license": False,
    "single_tick_invocation_token": False,
    "tick_invoked": False,
    "denied_reason": "bounded_tick_license_missing_or_not_granted",
    "steps_run": 0,
    "licensed_max_steps_per_tick": 0,
    "run_manifest_path": None,
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}


class QiBoundedTickExecutorReceiptValidatorTests(unittest.TestCase):
    def test_invoked_receipt_valid(self):
        self.assertEqual(validate_receipt(dict(BASE_INVOKED)), [])

    def test_denied_receipt_valid(self):
        self.assertEqual(validate_receipt(dict(BASE_DENIED)), [])

    def test_invoked_receipt_requires_token(self):
        receipt = dict(BASE_INVOKED)
        receipt["single_tick_invocation_token"] = False
        errors = validate_receipt(receipt)
        self.assertTrue(any("single_tick_invocation_token" in error for error in errors))

    def test_denied_receipt_cannot_grant_execution_authority(self):
        receipt = dict(BASE_DENIED)
        receipt["grants_execution_authority"] = True
        errors = validate_receipt(receipt)
        self.assertTrue(any("execution authority" in error for error in errors))

    def test_truth_authority_always_false(self):
        receipt = dict(BASE_INVOKED)
        receipt["grants_truth_authority"] = True
        errors = validate_receipt(receipt)
        self.assertTrue(any("grants_truth_authority" in error for error in errors))

    def test_invoked_max_steps_clamped(self):
        receipt = dict(BASE_INVOKED)
        receipt["licensed_max_steps_per_tick"] = 1000
        errors = validate_receipt(receipt)
        self.assertTrue(any("licensed_max_steps_per_tick" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
