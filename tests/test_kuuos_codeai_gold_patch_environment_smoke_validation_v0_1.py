from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_checks_v0_1 import (
    validate_harness_outputs,
)
from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_schema_v0_1 import (
    OBSERVATION_DIGEST_FIELD, PLAN_DIGEST_FIELD, POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD, seal,
)
from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_v0_1 import (
    evaluate_gold_patch_environment_smoke,
)
from scripts.build_codeai_gold_patch_environment_smoke_validation_fixture_v0_1 import (
    build_reference_fixture,
)

def reseal(value: dict, field: str) -> dict:
    value.pop(field, None)
    return seal(value, field)

class GoldPatchEnvironmentSmokeTests(unittest.TestCase):
    def evaluate(self, fixture=None):
        f = fixture or build_reference_fixture()
        return evaluate_gold_patch_environment_smoke(
            f["request"], f["policy"], f["predecessor_manifest"],
            f["smoke_plan"], f["observation"],
        )

    def test_reference_admitted(self):
        result = self.evaluate()
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.issues, ())
        self.assertEqual(result.receipt["decision"], "gold_patch_environment_smoke_admitted")
        self.assertTrue(result.receipt["resolved"])

    def test_non_mapping_blocks(self):
        self.assertEqual(
            evaluate_gold_patch_environment_smoke([], {}, {}, {}, {}).status,
            "blocked",
        )

    def test_request_tamper_blocks(self):
        f = build_reference_fixture()
        f["request"]["instance_id"] = "tampered"
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_policy_tamper_blocks(self):
        f = build_reference_fixture()
        f["policy"]["maximum_workers"] = 2
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_plan_tamper_blocks(self):
        f = build_reference_fixture()
        f["smoke_plan"]["timeout_seconds"] = 7
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_observation_tamper_blocks(self):
        f = build_reference_fixture()
        f["observation"]["resolved"] = False
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_binding_mismatch_blocks(self):
        f = build_reference_fixture()
        f["request"]["instance_id"] = "sympy__sympy-99999"
        f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_predecessor_digest_mismatch_blocks(self):
        f = build_reference_fixture()
        f["predecessor_manifest"]["row_count"] = 499
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_predecessor_not_admitted_blocks(self):
        f = build_reference_fixture()
        f["predecessor_manifest"]["freeze_decision"] = "external_corpus_freeze_held"
        f["request"]["predecessor_manifest_digest"] = __import__("hashlib").sha256(
            json.dumps(f["predecessor_manifest"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_request_stale_blocks(self):
        f = build_reference_fixture()
        f["request"]["request_created_epoch"] = 1
        f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_observation_stale_blocks(self):
        f = build_reference_fixture()
        f["observation"]["observation_created_epoch"] = 1
        f["observation"] = reseal(f["observation"], OBSERVATION_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_request_forbidden_authority_blocks(self):
        f = build_reference_fixture()
        f["request"]["claims_solver_gold_access"] = True
        f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_policy_forbidden_authority_blocks(self):
        f = build_reference_fixture()
        f["policy"]["allow_kernel_harness_execution"] = True
        f["policy"] = reseal(f["policy"], POLICY_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def hold_for_observation(self, field, value):
        f = build_reference_fixture()
        f["observation"][field] = value
        f["observation"] = reseal(f["observation"], OBSERVATION_DIGEST_FIELD)
        result = self.evaluate(f)
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.receipt["decision"], "gold_patch_environment_smoke_held")
        self.assertTrue(result.issues)

    def test_unresolved_holds(self): self.hold_for_observation("resolved", False)
    def test_patch_not_applied_holds(self): self.hold_for_observation("gold_patch_applied", False)
    def test_evaluation_incomplete_holds(self): self.hold_for_observation("evaluation_completed", False)
    def test_missing_report_holds(self): self.hold_for_observation("report_observed", False)
    def test_missing_logs_holds(self): self.hold_for_observation("logs_observed", False)
    def test_missing_image_holds(self): self.hold_for_observation("image_available", False)
    def test_missing_container_holds(self): self.hold_for_observation("container_started", False)
    def test_kernel_execution_holds(self): self.hold_for_observation("harness_execution_performed_by_kernel", True)
    def test_solver_gold_exposure_holds(self): self.hold_for_observation("gold_patch_exposed_to_solver", True)
    def test_candidate_generation_gold_use_holds(self): self.hold_for_observation("gold_patch_used_for_candidate_generation", True)
    def test_repair_memory_gold_use_holds(self): self.hold_for_observation("gold_patch_used_for_repair_memory", True)
    def test_repository_mutation_holds(self): self.hold_for_observation("repository_mutation_performed", True)
    def test_git_authority_holds(self): self.hold_for_observation("git_authority_granted", True)
    def test_correctness_claim_holds(self): self.hold_for_observation("correctness_claimed", True)

    def test_non_gold_plan_holds_or_blocks(self):
        f = build_reference_fixture()
        f["smoke_plan"]["predictions_path"] = "predictions.json"
        f["smoke_plan"] = reseal(f["smoke_plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.evaluate(f).status, "blocked")

    def test_harness_output_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            d = Path(directory)
            instance = "sympy__sympy-20590"
            report = d / "report.json"
            output = d / "test_output.txt"
            log = d / "run_instance.log"
            report.write_text(json.dumps({instance: {"resolved": True}}))
            output.write_text("tests passed")
            log.write_text("patch applied")
            evidence = validate_harness_outputs(report, output, log, instance)
            self.assertTrue(evidence["resolved"])
            self.assertEqual(len(evidence["report_digest"]), 64)

    def test_harness_unresolved_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            d = Path(directory)
            instance = "sympy__sympy-20590"
            report = d / "report.json"
            output = d / "test_output.txt"
            log = d / "run_instance.log"
            report.write_text(json.dumps({instance: {"resolved": False}}))
            output.write_text("failed")
            log.write_text("ran")
            with self.assertRaises(ValueError):
                validate_harness_outputs(report, output, log, instance)

if __name__ == "__main__":
    unittest.main()
