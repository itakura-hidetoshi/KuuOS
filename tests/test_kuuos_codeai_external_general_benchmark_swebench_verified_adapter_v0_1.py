from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_schema_v0_1 import *
from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1 import (
    build_codeai_external_general_benchmark_swebench_verified_adapter,
)
from scripts.build_codeai_external_general_benchmark_swebench_verified_adapter_fixture_v0_1 import (
    build_fixture,
)


class ExternalGeneralBenchmarkSWEBenchVerifiedAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = build_fixture()

    def run_fixture(self, fixture=None):
        item = fixture or self.fixture
        return build_codeai_external_general_benchmark_swebench_verified_adapter(
            request=item["request"],
            policy=item["policy"],
            benchmark_contract=item["benchmark_contract"],
            run_plan=item["run_plan"],
            predictions=item["predictions"],
        )

    def reseal_request(self, fixture):
        fixture["request"] = seal(fixture["request"], REQUEST_DIGEST_FIELD)

    def reseal_policy(self, fixture):
        fixture["policy"] = seal(fixture["policy"], POLICY_DIGEST_FIELD)

    def rebind_contract(self, fixture):
        fixture["benchmark_contract"] = seal(
            fixture["benchmark_contract"], CONTRACT_DIGEST_FIELD
        )
        digest = fixture["benchmark_contract"][CONTRACT_DIGEST_FIELD]
        fixture["request"]["benchmark_contract_digest"] = digest
        fixture["policy"]["expected_benchmark_contract_digest"] = digest
        self.reseal_request(fixture)
        self.reseal_policy(fixture)

    def rebind_plan(self, fixture):
        fixture["run_plan"] = seal(fixture["run_plan"], RUN_PLAN_DIGEST_FIELD)
        digest = fixture["run_plan"][RUN_PLAN_DIGEST_FIELD]
        fixture["request"]["run_plan_digest"] = digest
        fixture["policy"]["expected_run_plan_digest"] = digest
        self.reseal_request(fixture)
        self.reseal_policy(fixture)

    def test_reference_protocol_is_admitted(self):
        result = self.run_fixture()
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_ADMIT)
        self.assertEqual(result.adapter_pack["hold_reasons"], [])
        self.assertFalse(result.adapter_pack["harness_execution_performed"])
        self.assertFalse(result.adapter_pack["correctness_claimed"])

    def test_reference_is_deterministic(self):
        first = self.run_fixture()
        second = self.run_fixture(build_fixture())
        self.assertEqual(first.adapter_pack, second.adapter_pack)
        self.assertEqual(first.receipt, second.receipt)

    def test_official_projection_has_exact_three_fields(self):
        result = self.run_fixture()
        for prediction in result.adapter_pack["official_predictions"]:
            self.assertEqual(tuple(prediction), OFFICIAL_PREDICTION_FIELDS)

    def test_request_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["request_revision"] = "tampered"
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_digest_mismatch", result.issues)

    def test_unresolved_question_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["unresolved_questions"] = ["which subset"]
        self.reseal_request(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_unresolved_questions_present", result.issues)

    def test_authority_claim_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["claims_harness_execution_authority"] = True
        self.reseal_request(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_claims_authority_or_correctness", result.issues)

    def test_policy_harness_execution_enablement_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["allow_harness_execution"] = True
        self.reseal_policy(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_effect_or_authority_enabled", result.issues)

    def test_wrong_dataset_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["benchmark_contract"]["dataset_name"] = "SWE-bench/SWE-bench_Lite"
        self.rebind_contract(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("dataset_name_not_official_verified", result.adapter_pack["hold_reasons"])

    def test_wrong_expected_count_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["benchmark_contract"]["expected_instance_count"] = 499
        self.rebind_contract(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("dataset_instance_count_not_500", result.adapter_pack["hold_reasons"])

    def test_unpinned_harness_contract_is_structurally_blocked(self):
        fixture = deepcopy(self.fixture)
        fixture["benchmark_contract"]["harness_commit_sha"] = "not-a-commit"
        fixture["benchmark_contract"] = seal(
            fixture["benchmark_contract"], CONTRACT_DIGEST_FIELD
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("harness_commit_invalid" in issue for issue in result.issues))

    def test_nonfrozen_sample_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["run_plan"]["selection_frozen_before_execution"] = False
        self.rebind_plan(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("run_plan_selection_not_frozen", result.adapter_pack["hold_reasons"])

    def test_holdout_label_exposure_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["run_plan"]["holdout_labels_exposed"] = True
        self.rebind_plan(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("run_plan_holdout_labels_exposed", result.adapter_pack["hold_reasons"])

    def test_gold_patch_exposure_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["run_plan"]["gold_patches_exposed"] = True
        self.rebind_plan(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("run_plan_gold_patches_exposed", result.adapter_pack["hold_reasons"])

    def test_harness_execution_request_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["run_plan"]["harness_execution_requested"] = True
        self.rebind_plan(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn(
            "run_plan_forbidden_request:harness_execution_requested",
            result.adapter_pack["hold_reasons"],
        )

    def test_duplicate_prediction_instance_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["predictions"][1]["instance_id"] = fixture["predictions"][0]["instance_id"]
        fixture["predictions"][1] = seal(
            fixture["predictions"][1], PREDICTION_DIGEST_FIELD
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("prediction_instance_ids_not_unique", result.adapter_pack["hold_reasons"])

    def test_prediction_order_mismatch_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["predictions"][0], fixture["predictions"][1] = (
            fixture["predictions"][1],
            fixture["predictions"][0],
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn(
            "prediction_instance_order_or_set_mismatch", result.adapter_pack["hold_reasons"]
        )

    def test_changed_path_claim_mismatch_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["predictions"][0]["changed_paths"] = ["sympy/core/not_the_patch.py"]
        fixture["predictions"][0] = seal(
            fixture["predictions"][0], PREDICTION_DIGEST_FIELD
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("prediction_changed_paths_mismatch" in issue for issue in result.issues))

    def test_protected_test_path_overlap_holds(self):
        fixture = deepcopy(self.fixture)
        protected = fixture["run_plan"]["instances"][1]["protected_test_paths"][0]
        fixture["predictions"][1]["model_patch"] = (
            f"diff --git a/{protected} b/{protected}\n"
            f"--- a/{protected}\n"
            f"+++ b/{protected}\n"
            "@@ -1 +1 @@\n-old\n+new\n"
        )
        fixture["predictions"][1]["changed_paths"] = [protected]
        fixture["predictions"][1] = seal(
            fixture["predictions"][1], PREDICTION_DIGEST_FIELD
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertTrue(
            any(
                reason.startswith("prediction_protected_test_path_overlap:")
                for reason in result.adapter_pack["hold_reasons"]
            )
        )

    def test_instance_contract_digest_mismatch_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["predictions"][0]["instance_contract_digest"] = "f" * 64
        fixture["predictions"][0] = seal(
            fixture["predictions"][0], PREDICTION_DIGEST_FIELD
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertTrue(
            any(
                reason.startswith("prediction_instance_contract_digest_mismatch:")
                for reason in result.adapter_pack["hold_reasons"]
            )
        )

    def test_prediction_claims_harness_result_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["predictions"][0]["claims_harness_result"] = True
        fixture["predictions"][0] = seal(
            fixture["predictions"][0], PREDICTION_DIGEST_FIELD
        )
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertTrue(
            any("claims_unexecuted_harness_result" in reason for reason in result.adapter_pack["hold_reasons"])
        )

    def test_patch_budget_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["maximum_patch_bytes"] = 10
        self.reseal_policy(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertTrue(
            any("prediction_patch_budget_exceeded" in reason for reason in result.adapter_pack["hold_reasons"])
        )

    def test_sample_count_policy_holds(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["maximum_sample_count"] = 2
        self.reseal_policy(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.adapter_pack["adapter_decision"], DECISION_HOLD)
        self.assertIn("run_plan_sample_count_out_of_bounds", result.adapter_pack["hold_reasons"])

    def test_receipt_never_claims_benchmark_result(self):
        result = self.run_fixture()
        self.assertFalse(result.receipt["benchmark_result_ingested"])
        self.assertFalse(result.receipt["correctness_claimed"])
        self.assertFalse(result.receipt["harness_execution_performed"])


if __name__ == "__main__":
    unittest.main()
