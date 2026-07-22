from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_codeai_bounded_official_harness_execution_fixture_v0_1 import (
    MODEL_PATCH,
    build_fixture,
)
from runtime.kuuos_codeai_bounded_official_harness_execution_checks_v0_1 import (
    build_external_observation,
    project_manifest,
    validate_official_prediction_jsonl,
)
from runtime.kuuos_codeai_bounded_official_harness_execution_schema_v0_1 import *
from runtime.kuuos_codeai_bounded_official_harness_execution_v0_1 import (
    build_codeai_bounded_official_harness_execution,
)

DIGEST_BY_KEY = {
    "request": REQUEST_DIGEST_FIELD,
    "policy": POLICY_DIGEST_FIELD,
    "execution_plan": PLAN_DIGEST_FIELD,
    "prediction": PREDICTION_DIGEST_FIELD,
    "observation": OBSERVATION_DIGEST_FIELD,
}

class BoundedOfficialHarnessExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = build_fixture()

    def run_fixture(self, fx=None):
        fx = fx or self.fx
        return build_codeai_bounded_official_harness_execution(
            request=fx["request"],
            policy=fx["policy"],
            predecessor_manifest=fx["predecessor_manifest"],
            execution_plan=fx["execution_plan"],
            prediction=fx["prediction"],
            observation=fx["observation"],
        )

    def reseal(self, fx, key):
        field = DIGEST_BY_KEY[key]
        value = {k: v for k, v in fx[key].items() if k != field}
        fx[key] = seal(value, field)

    def mutate(self, key, field, value, reseal=True):
        fx = copy.deepcopy(self.fx)
        fx[key][field] = value
        if reseal:
            self.reseal(fx, key)
        return fx

    def test_reference_admitted(self):
        self.assertEqual(self.run_fixture().status, STATUS_ADMITTED)

    def test_reference_is_unresolved_but_admitted(self):
        result = self.run_fixture()
        self.assertFalse(result.receipt["resolved"])
        self.assertEqual(result.receipt["decision"], DECISION_ADMITTED)

    def test_receipt_never_claims_correctness(self):
        self.assertFalse(self.run_fixture().receipt["correctness_claimed"])

    def test_official_prediction_fields(self):
        self.assertEqual(set(official_prediction(self.fx["prediction"])), set(OFFICIAL_PREDICTION_FIELDS))

    def test_changed_paths_derived(self):
        self.assertEqual(derive_changed_paths(MODEL_PATCH), ["sympy/core/_print_helpers.py"])

    def test_extra_request_field_blocks(self):
        fx = copy.deepcopy(self.fx)
        fx["request"]["extra"] = 1
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_request_digest_tamper_blocks(self):
        fx = self.mutate("request", "request_id", "tampered", reseal=False)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_policy_digest_tamper_blocks(self):
        fx = self.mutate("policy", "maximum_workers", 2, reseal=False)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_prediction_digest_tamper_blocks(self):
        fx = self.mutate("prediction", "model_name_or_path", "tampered", reseal=False)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_observation_digest_tamper_blocks(self):
        fx = self.mutate("observation", "observer_id", "tampered", reseal=False)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_predecessor_manifest_tamper_blocks(self):
        fx = copy.deepcopy(self.fx)
        fx["predecessor_manifest"]["resolved"] = False
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_request_policy_binding_mismatch_blocks(self):
        fx = self.mutate("policy", "expected_instance_id", "other")
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_plan_binding_mismatch_blocks(self):
        fx = self.mutate("execution_plan", "base_commit_sha", "1" * 40)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_observation_run_id_mismatch_blocks(self):
        fx = self.mutate("observation", "run_id", "other")
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_prediction_source_digest_mismatch_blocks(self):
        fx = self.mutate("prediction", "source_digest", "0" * 64)
        fx["request"]["prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        self.reseal(fx, "request")
        fx["policy"]["expected_prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        self.reseal(fx, "policy")
        fx["execution_plan"]["prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        fx["execution_plan"]["prediction_file_digest"] = canonical_digest(official_prediction(fx["prediction"]))
        self.reseal(fx, "execution_plan")
        fx["observation"]["prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        self.reseal(fx, "observation")
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_prediction_binding_mismatch_blocks(self):
        fx = self.mutate("prediction", "base_commit_sha", "1" * 40)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_changed_path_mismatch_blocks(self):
        fx = self.mutate("prediction", "changed_paths", ["other.py"])
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_stale_request_blocks(self):
        fx = self.mutate("request", "request_created_epoch", 0)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_stale_observation_blocks(self):
        fx = self.mutate("observation", "observation_created_epoch", 0)
        self.assertEqual(self.run_fixture(fx).status, STATUS_BLOCKED)

    def test_predecessor_not_admitted_holds(self):
        fx = copy.deepcopy(self.fx)
        fx["predecessor_manifest"]["decision"] = "held"
        fx["request"]["predecessor_manifest_digest"] = canonical_digest(fx["predecessor_manifest"])
        self.reseal(fx, "request")
        fx["policy"]["expected_predecessor_manifest_digest"] = fx["request"]["predecessor_manifest_digest"]
        self.reseal(fx, "policy")
        fx["execution_plan"]["predecessor_manifest_digest"] = fx["request"]["predecessor_manifest_digest"]
        self.reseal(fx, "execution_plan")
        fx["observation"]["predecessor_manifest_digest"] = fx["request"]["predecessor_manifest_digest"]
        self.reseal(fx, "observation")
        self.assertEqual(self.run_fixture(fx).status, STATUS_HELD)

    def test_sample_not_frozen_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("execution_plan", "sample_frozen", False)).status, STATUS_HELD)

    def test_prediction_not_frozen_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("execution_plan", "prediction_frozen", False)).status, STATUS_HELD)

    def test_gold_derived_holds(self):
        fx = self.mutate("prediction", "gold_derived", True)
        fx["request"]["prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        self.reseal(fx, "request")
        fx["policy"]["expected_prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        self.reseal(fx, "policy")
        fx["execution_plan"]["prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        fx["execution_plan"]["prediction_file_digest"] = canonical_digest(official_prediction(fx["prediction"]))
        self.reseal(fx, "execution_plan")
        fx["observation"]["prediction_digest"] = fx["prediction"][PREDICTION_DIGEST_FIELD]
        self.reseal(fx, "observation")
        self.assertEqual(self.run_fixture(fx).status, STATUS_HELD)

    def test_patch_not_applied_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "patch_applied", False)).status, STATUS_HELD)

    def test_evaluation_incomplete_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "evaluation_completed", False)).status, STATUS_HELD)

    def test_report_missing_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "report_observed", False)).status, STATUS_HELD)

    def test_logs_missing_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "logs_observed", False)).status, STATUS_HELD)

    def test_kernel_execution_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "harness_execution_performed_by_kernel", True)).status, STATUS_HELD)

    def test_gold_exposure_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "gold_exposed_to_solver", True)).status, STATUS_HELD)

    def test_repository_mutation_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "repository_mutated", True)).status, STATUS_HELD)

    def test_git_authority_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "git_authority", True)).status, STATUS_HELD)

    def test_correctness_claim_holds(self):
        self.assertEqual(self.run_fixture(self.mutate("observation", "correctness_claimed", True)).status, STATUS_HELD)

    def test_manifest_projection(self):
        manifest = project_manifest(self.fx["receipt"])
        self.assertEqual(manifest["decision"], DECISION_ADMITTED)
        self.assertFalse(manifest["resolved"])

    def test_prediction_jsonl_validation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "predictions.jsonl"
            path.write_text(json.dumps(official_prediction(self.fx["prediction"]), sort_keys=True) + "\n")
            validate_official_prediction_jsonl(path, self.fx["prediction"])

    def test_external_observation_accepts_unresolved_report(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            report = td / "report.json"
            output = td / "test_output.txt"
            log = td / "run_instance.log"
            report.write_text(json.dumps({self.fx["request"]["instance_id"]: {
                "resolved": False, "patch_successfully_applied": True
            }}))
            output.write_text("tests completed")
            log.write_text("APPLY_PATCH_PASS")
            observed = build_external_observation(
                template=self.fx["observation"],
                report_path=report,
                test_output_path=output,
                instance_log_path=log,
                instance_id=self.fx["request"]["instance_id"],
            )
            self.assertFalse(observed["resolved"])
            self.assertTrue(observed["patch_applied"])

if __name__ == "__main__":
    unittest.main()
