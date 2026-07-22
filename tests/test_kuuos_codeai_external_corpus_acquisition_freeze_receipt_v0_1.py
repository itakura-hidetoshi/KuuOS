from __future__ import annotations

import unittest

from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_schema_v0_1 import (
    OBSERVATION_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    seal,
)
from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_v0_1 import (
    build_codeai_external_corpus_acquisition_freeze_receipt,
)
from scripts.build_codeai_external_corpus_acquisition_freeze_receipt_fixture_v0_1 import (
    acquisition_observation,
    build_fixture,
    policy,
    predecessor_manifest,
    request,
)


class ExternalCorpusFreezeTests(unittest.TestCase):
    def run_stage(self, *, req=None, pol=None, pred=None, obs=None):
        return build_codeai_external_corpus_acquisition_freeze_receipt(
            request=request() if req is None else req,
            policy=policy() if pol is None else pol,
            predecessor_manifest=predecessor_manifest() if pred is None else pred,
            acquisition_observation=acquisition_observation() if obs is None else obs,
        )

    def test_reference_admitted(self):
        result = self.run_stage()
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.freeze_pack["freeze_decision"], "external_corpus_freeze_admitted")
        self.assertTrue(result.freeze_pack["corpus_frozen"])
        self.assertEqual(result.freeze_pack["row_count"], 500)

    def test_reference_deterministic(self):
        self.assertEqual(build_fixture(), build_fixture())

    def test_non_mapping_blocked(self):
        result = build_codeai_external_corpus_acquisition_freeze_receipt(
            request=[], policy={}, predecessor_manifest={}, acquisition_observation={}
        )
        self.assertEqual(result.status, "blocked")

    def test_request_digest_tamper_blocked(self):
        req = request(); req["request_revision"] = "r2"
        self.assertEqual(self.run_stage(req=req).status, "blocked")

    def test_policy_digest_tamper_blocked(self):
        pol = policy(); pol["maximum_request_age"] = 999
        self.assertEqual(self.run_stage(pol=pol).status, "blocked")

    def test_observation_digest_tamper_blocked(self):
        obs = acquisition_observation(); obs["observer_id"] = "other"
        self.assertEqual(self.run_stage(obs=obs).status, "blocked")

    def test_predecessor_digest_mismatch_blocked(self):
        pred = predecessor_manifest(); pred["sample_count"] = 4
        self.assertEqual(self.run_stage(pred=pred).status, "blocked")

    def test_predecessor_not_admitted_blocked(self):
        pred = predecessor_manifest(); pred["adapter_decision"] = "external_benchmark_protocol_held"
        self.assertEqual(self.run_stage(pred=pred).status, "blocked")

    def test_request_claims_gold_access_blocked(self):
        req = request(); req["claims_gold_patch_access"] = True; req = seal(req, REQUEST_DIGEST_FIELD)
        self.assertEqual(self.run_stage(req=req).status, "blocked")

    def test_policy_allows_harness_blocked(self):
        pol = policy(); pol["allow_harness_execution"] = True; pol = seal(pol, POLICY_DIGEST_FIELD)
        self.assertEqual(self.run_stage(pol=pol).status, "blocked")

    def test_stale_request_blocked(self):
        req = request(); req["request_created_epoch"] = 1; req = seal(req, REQUEST_DIGEST_FIELD)
        self.assertEqual(self.run_stage(req=req).status, "blocked")

    def test_stale_observation_blocked(self):
        obs = acquisition_observation(); obs["observation_created_epoch"] = 1; obs = seal(obs, OBSERVATION_DIGEST_FIELD)
        self.assertEqual(self.run_stage(obs=obs).status, "blocked")

    def assert_hold(self, field, value, reason_prefix):
        obs = acquisition_observation(); obs[field] = value; obs = seal(obs, OBSERVATION_DIGEST_FIELD)
        result = self.run_stage(obs=obs)
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.freeze_pack["freeze_decision"], "external_corpus_freeze_held")
        self.assertTrue(any(reason.startswith(reason_prefix) for reason in result.freeze_pack["hold_reasons"]))
        self.assertFalse(result.freeze_pack["corpus_frozen"])

    def test_fetch_incomplete_held(self):
        self.assert_hold("fetch_completed", False, "acquisition_requirement_missing")

    def test_sha_unverified_held(self):
        self.assert_hold("artifact_sha256_verified", False, "acquisition_requirement_missing")

    def test_size_unverified_held(self):
        self.assert_hold("artifact_size_verified", False, "acquisition_requirement_missing")

    def test_row_count_unverified_held(self):
        self.assert_hold("row_count_verified", False, "acquisition_requirement_missing")

    def test_schema_unverified_held(self):
        self.assert_hold("schema_verified", False, "acquisition_requirement_missing")

    def test_mutable_freeze_held(self):
        self.assert_hold("immutable_freeze", False, "acquisition_requirement_missing")

    def test_kernel_fetch_held(self):
        self.assert_hold("fetch_performed_by_kernel", True, "acquisition_boundary_violated")

    def test_gold_exposure_held(self):
        self.assert_hold("gold_patch_exposed_to_solver", True, "acquisition_boundary_violated")

    def test_test_patch_exposure_held(self):
        self.assert_hold("test_patch_exposed_to_solver", True, "acquisition_boundary_violated")

    def test_label_exposure_held(self):
        self.assert_hold("evaluation_labels_exposed_to_solver", True, "acquisition_boundary_violated")

    def test_harness_execution_held(self):
        self.assert_hold("harness_execution_performed", True, "acquisition_boundary_violated")

    def test_repository_mutation_held(self):
        self.assert_hold("repository_mutation_performed", True, "acquisition_boundary_violated")

    def test_wrong_row_count_held(self):
        obs = acquisition_observation(); obs["observed_row_count"] = 499; obs = seal(obs, OBSERVATION_DIGEST_FIELD)
        result = self.run_stage(obs=obs)
        self.assertIn("observed_row_count_mismatch", result.freeze_pack["hold_reasons"])

    def test_wrong_schema_order_held(self):
        obs = acquisition_observation(); obs["observed_schema_columns"] = list(reversed(obs["observed_schema_columns"])); obs = seal(obs, OBSERVATION_DIGEST_FIELD)
        result = self.run_stage(obs=obs)
        self.assertIn("observed_schema_columns_mismatch", result.freeze_pack["hold_reasons"])

    def test_solver_restricted_overlap_held(self):
        obs = acquisition_observation(); obs["solver_visible_fields"] = obs["solver_visible_fields"] + ["patch"]; obs = seal(obs, OBSERVATION_DIGEST_FIELD)
        result = self.run_stage(obs=obs)
        self.assertIn("solver_restricted_field_overlap", result.freeze_pack["hold_reasons"])

    def test_receipt_preserves_no_authority(self):
        receipt = self.run_stage().receipt
        self.assertFalse(receipt["solver_label_access_granted"])
        self.assertFalse(receipt["gold_patch_access_granted"])
        self.assertFalse(receipt["harness_execution_authority_granted"])
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["git_authority_granted"])
        self.assertFalse(receipt["correctness_claimed"])


if __name__ == "__main__":
    unittest.main()
