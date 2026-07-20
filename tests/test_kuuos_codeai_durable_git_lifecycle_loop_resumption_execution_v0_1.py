from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace
import unittest

from scripts.check_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1 import (
    build_example_bundle,
    seal,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import (
    RESUME_INPUT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1 import (
    EXECUTION_INPUT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    LIFECYCLE_RECEIPT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as INNER_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as INNER_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as INNER_REQUEST_DIGEST_FIELD,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1 import (
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_durable_git_lifecycle_loop_resumption_execution,
)


class DurableGitLifecycleLoopResumptionExecutionTests(unittest.TestCase):
    def bundle(self):
        return build_example_bundle()

    def run_bundle(self, bundle):
        return build_codeai_durable_git_lifecycle_loop_resumption_execution(**bundle)

    def assert_blocked(self, bundle):
        result = self.run_bundle(bundle)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.evidence)
        self.assertIsNone(result.next_registry)
        self.assertIsNone(result.receipt)
        return result

    def test_01_ready_path(self):
        result = self.run_bundle(self.bundle())
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())

    def test_02_consumes_input_once(self):
        bundle = self.bundle()
        result = self.run_bundle(bundle)
        self.assertIn(
            bundle["execution_input"][EXECUTION_INPUT_DIGEST_FIELD],
            result.next_registry["consumed_execution_input_digests"],
        )

    def test_03_consumes_nonce_once(self):
        bundle = self.bundle()
        result = self.run_bundle(bundle)
        self.assertIn(
            bundle["execution_request"]["invocation_nonce_digest"],
            result.next_registry["consumed_invocation_nonce_digests"],
        )

    def test_04_registry_advances_exactly_once(self):
        result = self.run_bundle(self.bundle())
        self.assertEqual(result.next_registry["registry_revision"], 1)
        self.assertEqual(result.next_registry["successful_execution_count"], 1)

    def test_05_receipt_is_sealed(self):
        result = self.run_bundle(self.bundle())
        receipt = result.receipt
        self.assertEqual(receipt[RECEIPT_DIGEST_FIELD], seal(receipt, RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD])

    def test_06_delegated_effect_count_recorded(self):
        result = self.run_bundle(self.bundle())
        self.assertEqual(result.receipt["delegated_git_effect_count"], 2)
        self.assertFalse(result.receipt["direct_git_effect_performed"])

    def test_07_orchestrator_receives_exact_inputs(self):
        bundle = self.bundle()
        seen = {}
        original = bundle["orchestrator"]

        def capture(**kwargs):
            seen.update(kwargs)
            return original(**kwargs)

        bundle["orchestrator"] = capture
        result = self.run_bundle(bundle)
        self.assertEqual(result.status, STATUS_READY)
        self.assertIs(seen["loop_request"], bundle["loop_request"])
        self.assertIs(seen["initial_lifecycle_receipt"], bundle["initial_lifecycle_receipt"])

    def test_08_source_receipt_tamper_blocks(self):
        bundle = self.bundle()
        bundle["consumption_receipt"]["loop_id"] = "wrong"
        self.assert_blocked(bundle)

    def test_09_source_evidence_tamper_blocks(self):
        bundle = self.bundle()
        bundle["consumption_evidence"]["execution_input_active"] = False
        self.assert_blocked(bundle)

    def test_10_source_registry_tamper_blocks(self):
        bundle = self.bundle()
        bundle["consumption_registry"]["registry_revision"] = 2
        self.assert_blocked(bundle)

    def test_11_source_resume_input_tamper_blocks(self):
        bundle = self.bundle()
        bundle["source_resume_input"]["loop_id"] = "wrong-loop"
        self.assert_blocked(bundle)

    def test_12_execution_input_tamper_blocks(self):
        bundle = self.bundle()
        bundle["execution_input"]["active_now"] = False
        self.assert_blocked(bundle)

    def test_13_execution_input_reusable_blocks(self):
        bundle = self.bundle()
        active = deepcopy(bundle["execution_input"])
        active["reusable"] = True
        bundle["execution_input"] = seal(active, EXECUTION_INPUT_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_14_execution_input_direct_git_authority_blocks(self):
        bundle = self.bundle()
        active = deepcopy(bundle["execution_input"])
        active["direct_git_effect_authorized"] = True
        bundle["execution_input"] = seal(active, EXECUTION_INPUT_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_15_request_extra_field_blocks(self):
        bundle = self.bundle()
        bundle["execution_request"]["unexpected"] = True
        self.assert_blocked(bundle)

    def test_16_policy_extra_field_blocks(self):
        bundle = self.bundle()
        bundle["execution_policy"]["unexpected"] = True
        self.assert_blocked(bundle)

    def test_17_registry_extra_field_blocks(self):
        bundle = self.bundle()
        bundle["execution_registry"]["unexpected"] = True
        self.assert_blocked(bundle)

    def test_18_replayed_nonce_blocks(self):
        bundle = self.bundle()
        registry = deepcopy(bundle["execution_registry"])
        registry["consumed_invocation_nonce_digests"] = [bundle["execution_request"]["invocation_nonce_digest"]]
        registry["consumed_execution_input_digests"] = ["e" * 64]
        registry["emitted_loop_receipt_digests"] = ["f" * 64]
        registry["registry_revision"] = 1
        registry["successful_execution_count"] = 1
        bundle["execution_registry"] = seal(registry, REGISTRY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_19_replayed_execution_input_blocks(self):
        bundle = self.bundle()
        registry = deepcopy(bundle["execution_registry"])
        registry["consumed_invocation_nonce_digests"] = ["e" * 64]
        registry["consumed_execution_input_digests"] = [bundle["execution_input"][EXECUTION_INPUT_DIGEST_FIELD]]
        registry["emitted_loop_receipt_digests"] = ["f" * 64]
        registry["registry_revision"] = 1
        registry["successful_execution_count"] = 1
        bundle["execution_registry"] = seal(registry, REGISTRY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_20_stale_request_blocks(self):
        bundle = self.bundle()
        policy = deepcopy(bundle["execution_policy"])
        policy["evaluation_epoch"] = 1000
        bundle["execution_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_21_unauthorized_executor_blocks(self):
        bundle = self.bundle()
        request = deepcopy(bundle["execution_request"])
        request["executor_id"] = "other-executor"
        bundle["execution_request"] = seal(request, REQUEST_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_22_loop_identity_mismatch_blocks(self):
        bundle = self.bundle()
        request = deepcopy(bundle["execution_request"])
        request["loop_id"] = "other-loop"
        bundle["execution_request"] = seal(request, REQUEST_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_23_initial_lifecycle_receipt_mismatch_blocks(self):
        bundle = self.bundle()
        lifecycle = deepcopy(bundle["initial_lifecycle_receipt"])
        lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD] = "e" * 64
        bundle["initial_lifecycle_receipt"] = lifecycle
        self.assert_blocked(bundle)

    def test_24_effect_budget_expansion_blocks(self):
        bundle = self.bundle()
        loop_request = deepcopy(bundle["loop_request"])
        loop_request["requested_max_effect_count"] = 3
        bundle["loop_request"] = seal(loop_request, INNER_REQUEST_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_25_command_budget_expansion_blocks(self):
        bundle = self.bundle()
        loop_policy = deepcopy(bundle["loop_policy"])
        loop_policy["maximum_total_execution_command_count"] = 5
        loop_policy["maximum_total_reobservation_command_count"] = 4
        bundle["loop_policy"] = seal(loop_policy, INNER_POLICY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_26_output_budget_expansion_blocks(self):
        bundle = self.bundle()
        loop_policy = deepcopy(bundle["loop_policy"])
        loop_policy["maximum_total_execution_output_bytes"] = 5000
        loop_policy["maximum_total_reobservation_output_bytes"] = 4000
        bundle["loop_policy"] = seal(loop_policy, INNER_POLICY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_27_direct_git_policy_blocks(self):
        bundle = self.bundle()
        policy = deepcopy(bundle["execution_policy"])
        policy["allow_direct_git_effect"] = True
        bundle["execution_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_28_automatic_execution_policy_blocks(self):
        bundle = self.bundle()
        policy = deepcopy(bundle["execution_policy"])
        policy["allow_automatic_execution"] = True
        bundle["execution_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assert_blocked(bundle)

    def test_29_inner_blocked_returns_no_outer_receipt(self):
        bundle = self.bundle()
        bundle["orchestrator"] = lambda **kwargs: SimpleNamespace(status=STATUS_BLOCKED, issues=("inner",), receipt=None, evidence=None)
        result = self.assert_blocked(bundle)
        self.assertIsNotNone(result.loop_result)
        self.assertIn("bounded_loop:inner", result.issues)

    def test_30_inner_missing_receipt_blocks(self):
        bundle = self.bundle()
        bundle["orchestrator"] = lambda **kwargs: SimpleNamespace(status=STATUS_READY, issues=(), receipt=None, evidence={})
        self.assert_blocked(bundle)

    def test_31_source_receipt_digest_pin_mismatch_blocks(self):
        bundle = self.bundle()
        request = deepcopy(bundle["execution_request"])
        request["source_consumption_receipt_digest"] = "f" * 64
        bundle["execution_request"] = seal(request, REQUEST_DIGEST_FIELD)
        self.assertNotEqual(
            request["source_consumption_receipt_digest"],
            bundle["consumption_receipt"][SOURCE_RECEIPT_DIGEST_FIELD],
        )
        self.assert_blocked(bundle)


if __name__ == "__main__":
    unittest.main()
