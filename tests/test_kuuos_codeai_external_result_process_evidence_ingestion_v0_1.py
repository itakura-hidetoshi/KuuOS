from __future__ import annotations

import unittest

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import *
from runtime.kuuos_codeai_external_result_process_evidence_ingestion_v0_1 import (
    build_codeai_external_result_process_evidence_ingestion,
)
from scripts.build_codeai_external_result_process_evidence_ingestion_fixture_v0_1 import clone_fixture


def reseal(value: dict, digest_field: str) -> dict:
    material = {k: v for k, v in value.items() if k != digest_field}
    return seal(material, digest_field)

class ExternalResultProcessEvidenceIngestionTests(unittest.TestCase):
    def build(self, fixture: dict):
        return build_codeai_external_result_process_evidence_ingestion(
            request=fixture["request"], policy=fixture["policy"],
            predecessor_manifest=fixture["predecessor_manifest"], plan=fixture["plan"],
            result_evidence=fixture["result_evidence"], process_evidence=fixture["process_evidence"],
        )

    def test_reference_admitted(self):
        result = self.build(clone_fixture())
        self.assertEqual(result.status, STATUS_ADMITTED)
        self.assertEqual(result.ingestion_pack["outcome_disposition"], "measured_unresolved")

    def test_unresolved_is_not_protocol_failure(self):
        result = self.build(clone_fixture())
        self.assertFalse(result.ingestion_pack["resolved"])
        self.assertTrue(result.ingestion_pack["execution_valid"])

    def test_receipt_has_no_authority(self):
        receipt = self.build(clone_fixture()).receipt
        self.assertFalse(receipt["downstream_comparison_authority_granted"])
        self.assertFalse(receipt["repository_mutation_authority_granted"])
        self.assertFalse(receipt["git_authority_granted"])
        self.assertFalse(receipt["correctness_claimed"])

    def test_projection_excludes_raw_evidence(self):
        pack = self.build(clone_fixture()).ingestion_pack
        self.assertFalse(pack["raw_gold_ingested"])
        self.assertFalse(pack["raw_test_names_ingested"])
        self.assertFalse(pack["raw_logs_committed"])

    def test_request_tamper_blocked(self):
        f = clone_fixture(); f["request"]["request_id"] = "tampered"
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_policy_tamper_blocked(self):
        f = clone_fixture(); f["policy"]["maximum_request_age"] += 1
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_plan_tamper_blocked(self):
        f = clone_fixture(); f["plan"]["result_count"] = 2
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_result_tamper_blocked(self):
        f = clone_fixture(); f["result_evidence"]["resolved"] = True
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_process_tamper_blocked(self):
        f = clone_fixture(); f["process_evidence"]["docker_used"] = False
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_extra_request_field_blocked(self):
        f = clone_fixture(); f["request"]["extra"] = 1
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_missing_process_field_blocked(self):
        f = clone_fixture(); del f["process_evidence"]["image_removed"]
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_controller_binding_mismatch_blocked(self):
        f = clone_fixture(); f["request"]["controller_repository"] = "other/repo"; f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_artifact_binding_mismatch_blocked(self):
        f = clone_fixture(); f["process_evidence"]["predecessor_artifact_id"] += 1; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_observation_binding_mismatch_blocked(self):
        f = clone_fixture(); f["result_evidence"]["external_observation_digest"] = "0" * 64; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_predecessor_manifest_digest_mismatch_blocked(self):
        f = clone_fixture(); f["predecessor_manifest"]["resolved"] = True
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_stale_request_blocked(self):
        f = clone_fixture(); f["request"]["request_created_epoch"] = 0; f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_stale_result_blocked(self):
        f = clone_fixture(); f["result_evidence"]["result_created_epoch"] = 0; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_stale_process_blocked(self):
        f = clone_fixture(); f["process_evidence"]["process_created_epoch"] = 0; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_BLOCKED)

    def test_predecessor_not_admitted_held(self):
        f = clone_fixture(); f["predecessor_manifest"]["decision"] = "bounded_official_harness_execution_held"; digest = canonical_digest(f["predecessor_manifest"])
        for key, df in (("request",REQUEST_DIGEST_FIELD),("plan",PLAN_DIGEST_FIELD),("result_evidence",RESULT_DIGEST_FIELD),("process_evidence",PROCESS_DIGEST_FIELD)):
            f[key]["predecessor_manifest_digest"] = digest; f[key] = reseal(f[key],df)
        f["policy"]["expected_predecessor_manifest_digest"] = digest; f["policy"] = reseal(f["policy"],POLICY_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_patch_missing_held(self):
        f = clone_fixture(); f["result_evidence"]["patch_exists"] = False; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_patch_unapplied_held(self):
        f = clone_fixture(); f["result_evidence"]["patch_applied"] = False; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_evaluation_incomplete_held(self):
        f = clone_fixture(); f["result_evidence"]["evaluation_completed"] = False; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_execution_error_held(self):
        f = clone_fixture(); f["result_evidence"]["error_count"] = 1; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_raw_test_names_held(self):
        f = clone_fixture(); f["result_evidence"]["raw_test_names_included"] = True; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_gold_material_held(self):
        f = clone_fixture(); f["result_evidence"]["gold_material_included"] = True; f["result_evidence"] = reseal(f["result_evidence"], RESULT_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_artifact_expired_held(self):
        f = clone_fixture(); f["process_evidence"]["artifact_expired"] = True; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_workflow_incomplete_held(self):
        f = clone_fixture(); f["process_evidence"]["workflow_completed"] = False; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_report_missing_held(self):
        f = clone_fixture(); f["process_evidence"]["report_observed"] = False; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_logs_missing_held(self):
        f = clone_fixture(); f["process_evidence"]["logs_observed"] = False; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_kernel_execution_held(self):
        f = clone_fixture(); f["process_evidence"]["harness_executed_by_kernel"] = True; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_raw_logs_committed_held(self):
        f = clone_fixture(); f["process_evidence"]["raw_logs_committed"] = True; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_repository_mutation_held(self):
        f = clone_fixture(); f["process_evidence"]["repository_mutated"] = True; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_git_authority_held(self):
        f = clone_fixture(); f["process_evidence"]["git_authority"] = True; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_correctness_claim_held(self):
        f = clone_fixture(); f["process_evidence"]["correctness_claimed"] = True; f["process_evidence"] = reseal(f["process_evidence"], PROCESS_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_candidate_feedback_held(self):
        f = clone_fixture(); f["plan"]["candidate_generation_feedback_enabled"] = True; f["plan"] = reseal(f["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_repair_memory_feedback_held(self):
        f = clone_fixture(); f["plan"]["repair_memory_feedback_enabled"] = True; f["plan"] = reseal(f["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_comparison_authority_held(self):
        f = clone_fixture(); f["plan"]["comparison_authority_granted"] = True; f["plan"] = reseal(f["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_request_overclaim_held(self):
        f = clone_fixture(); f["request"]["claims_correctness"] = True; f["request"] = reseal(f["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

    def test_policy_authority_held(self):
        f = clone_fixture(); f["policy"]["allow_git_authority"] = True; f["policy"] = reseal(f["policy"], POLICY_DIGEST_FIELD)
        self.assertEqual(self.build(f).status, STATUS_HELD)

if __name__ == "__main__":
    unittest.main()
