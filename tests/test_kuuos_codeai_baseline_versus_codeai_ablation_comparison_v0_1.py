from __future__ import annotations

import unittest

from runtime.kuuos_codeai_baseline_versus_codeai_ablation_comparison_schema_v0_1 import *
from runtime.kuuos_codeai_baseline_versus_codeai_ablation_comparison_v0_1 import (
    build_codeai_baseline_versus_codeai_ablation_comparison,
)
from scripts.build_codeai_baseline_versus_codeai_ablation_comparison_fixture_v0_1 import (
    BASELINE_COHORT,
    CODEAI_COHORT,
    clone_fixture,
)


def reseal(value: dict, digest_field: str) -> dict:
    material = {key: item for key, item in value.items() if key != digest_field}
    return seal(material, digest_field)


class BaselineVersusCodeAIAblationComparisonTests(unittest.TestCase):
    def build(self, fixture: dict):
        return build_codeai_baseline_versus_codeai_ablation_comparison(
            request=fixture["request"],
            policy=fixture["policy"],
            predecessor_manifest=fixture["predecessor_manifest"],
            plan=fixture["plan"],
            cohort_registry=fixture["cohort_registry"],
            metric_registry=fixture["metric_registry"],
            observation_registry=fixture["observation_registry"],
        )

    def test_reference_preregistration_admitted(self):
        result = self.build(clone_fixture())
        self.assertEqual(result.status, STATUS_ADMITTED)
        self.assertTrue(result.comparison_pack["preregistration_completed"])

    def test_reference_does_not_claim_performance_comparison(self):
        result = self.build(clone_fixture())
        self.assertFalse(result.comparison_pack["performance_comparison_completed"])
        self.assertFalse(result.comparison_pack["performance_claimed"])

    def test_reference_grants_only_limited_comparison_authority(self):
        receipt = self.build(clone_fixture()).receipt
        self.assertTrue(receipt["limited_aggregate_comparison_authority_granted"])
        self.assertFalse(receipt["repository_mutation_authority_granted"])
        self.assertFalse(receipt["git_authority_granted"])

    def test_reference_codeai_observation_preserves_measured_unresolved(self):
        fixture = clone_fixture()
        observation = next(
            item for item in fixture["observation_registry"]["observations"]
            if item["cohort_id"] == CODEAI_COHORT
        )
        self.assertEqual(observation["sample_count"], 1)
        self.assertEqual(observation["resolved_count"], 0)
        self.assertEqual(observation["fail_to_pass_failure_count"], 1)

    def test_request_tamper_blocked(self):
        fixture = clone_fixture()
        fixture["request"]["request_id"] = "tampered"
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_policy_tamper_blocked(self):
        fixture = clone_fixture()
        fixture["policy"]["maximum_request_age"] += 1
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_plan_tamper_blocked(self):
        fixture = clone_fixture()
        fixture["plan"]["comparison_id"] = "tampered"
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_cohort_registry_tamper_blocked(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0]["target_sample_count"] = 99
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_metric_registry_tamper_blocked(self):
        fixture = clone_fixture()
        fixture["metric_registry"]["metrics"][0]["primary"] = False
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_observation_registry_tamper_blocked(self):
        fixture = clone_fixture()
        fixture["observation_registry"]["observations"][1]["resolved_count"] = 1
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_extra_request_field_blocked(self):
        fixture = clone_fixture()
        fixture["request"]["extra"] = 1
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_missing_cohort_field_blocked(self):
        fixture = clone_fixture()
        del fixture["cohort_registry"]["cohorts"][0]["role"]
        fixture["cohort_registry"] = reseal(fixture["cohort_registry"], COHORT_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_controller_cross_binding_blocked(self):
        fixture = clone_fixture()
        fixture["plan"]["controller_repository"] = "other/repo"
        fixture["plan"] = reseal(fixture["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_nested_sample_cross_binding_blocked(self):
        fixture = clone_fixture()
        fixture["observation_registry"]["observations"][0]["sample_binding_digest"] = "0" * 64
        fixture["observation_registry"] = reseal(
            fixture["observation_registry"], OBSERVATION_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_predecessor_manifest_digest_mismatch_blocked(self):
        fixture = clone_fixture()
        fixture["predecessor_manifest"]["resolved"] = True
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_stale_request_blocked(self):
        fixture = clone_fixture()
        fixture["request"]["request_created_epoch"] = 0
        fixture["request"] = reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_stale_cohort_registry_blocked(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["registry_created_epoch"] = 0
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_stale_observation_blocked(self):
        fixture = clone_fixture()
        fixture["observation_registry"]["observations"][0][
            "observation_created_epoch"
        ] = 0
        fixture["observation_registry"] = reseal(
            fixture["observation_registry"], OBSERVATION_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_BLOCKED)

    def test_predecessor_not_admitted_held(self):
        fixture = clone_fixture()
        fixture["predecessor_manifest"]["decision"] = (
            "external_result_process_evidence_ingestion_held"
        )
        digest = canonical_digest(fixture["predecessor_manifest"])
        fixture["request"]["predecessor_manifest_digest"] = digest
        fixture["request"] = reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        fixture["policy"]["expected_predecessor_manifest_digest"] = digest
        fixture["policy"] = reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        for key, digest_field in (
            ("plan", PLAN_DIGEST_FIELD),
            ("cohort_registry", COHORT_DIGEST_FIELD),
            ("metric_registry", METRIC_DIGEST_FIELD),
            ("observation_registry", OBSERVATION_DIGEST_FIELD),
        ):
            fixture[key]["predecessor_manifest_digest"] = digest
            fixture[key] = reseal(fixture[key], digest_field)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_missing_metric_held(self):
        fixture = clone_fixture()
        fixture["metric_registry"]["metrics"].pop()
        fixture["metric_registry"] = reseal(
            fixture["metric_registry"], METRIC_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_missing_observation_held(self):
        fixture = clone_fixture()
        fixture["observation_registry"]["observations"].pop()
        fixture["observation_registry"] = reseal(
            fixture["observation_registry"], OBSERVATION_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_cohort_target_imbalance_held(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0]["target_sample_count"] = 99
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_holdout_not_frozen_held(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0]["frozen_before_observation"] = False
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_gold_access_held(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0]["gold_access_granted"] = True
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_raw_test_name_access_held(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0][
            "raw_test_name_access_granted"
        ] = True
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_raw_log_observation_held(self):
        fixture = clone_fixture()
        fixture["observation_registry"]["observations"][0]["raw_logs_included"] = True
        fixture["observation_registry"] = reseal(
            fixture["observation_registry"], OBSERVATION_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_candidate_feedback_held(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0]["candidate_feedback_enabled"] = True
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_repair_memory_feedback_held(self):
        fixture = clone_fixture()
        fixture["cohort_registry"]["cohorts"][0][
            "repair_memory_feedback_enabled"
        ] = True
        fixture["cohort_registry"] = reseal(
            fixture["cohort_registry"], COHORT_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_repository_mutation_authority_held(self):
        fixture = clone_fixture()
        fixture["plan"]["repository_mutation_authority_granted"] = True
        fixture["plan"] = reseal(fixture["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_git_authority_held(self):
        fixture = clone_fixture()
        fixture["plan"]["git_authority_granted"] = True
        fixture["plan"] = reseal(fixture["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_correctness_claim_held(self):
        fixture = clone_fixture()
        fixture["plan"]["correctness_claimed"] = True
        fixture["plan"] = reseal(fixture["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_request_overclaim_held(self):
        fixture = clone_fixture()
        fixture["request"]["claims_correctness"] = True
        fixture["request"] = reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_policy_authority_overreach_held(self):
        fixture = clone_fixture()
        fixture["policy"]["allow_git_authority"] = True
        fixture["policy"] = reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_metric_not_predeclared_held(self):
        fixture = clone_fixture()
        fixture["metric_registry"]["metrics"][0]["predeclared"] = False
        fixture["metric_registry"] = reseal(
            fixture["metric_registry"], METRIC_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_metric_missing_evidence_policy_held(self):
        fixture = clone_fixture()
        fixture["metric_registry"]["metrics"][0][
            "missing_evidence_disposition"
        ] = "drop"
        fixture["metric_registry"] = reseal(
            fixture["metric_registry"], METRIC_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_execution_phase_with_pending_evidence_held(self):
        fixture = clone_fixture()
        fixture["request"]["comparison_phase"] = "comparison-execution"
        fixture["request"] = reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        fixture["plan"]["comparison_phase"] = "comparison-execution"
        fixture["plan"] = reseal(fixture["plan"], PLAN_DIGEST_FIELD)
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_pending_observation_with_values_held(self):
        fixture = clone_fixture()
        baseline = next(
            item for item in fixture["observation_registry"]["observations"]
            if item["cohort_id"] == BASELINE_COHORT
        )
        baseline["sample_count"] = 1
        fixture["observation_registry"] = reseal(
            fixture["observation_registry"], OBSERVATION_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)

    def test_codeai_receipt_mismatch_held(self):
        fixture = clone_fixture()
        codeai = next(
            item for item in fixture["observation_registry"]["observations"]
            if item["cohort_id"] == CODEAI_COHORT
        )
        codeai["source_receipt_digest"] = "0" * 64
        fixture["observation_registry"] = reseal(
            fixture["observation_registry"], OBSERVATION_DIGEST_FIELD
        )
        self.assertEqual(self.build(fixture).status, STATUS_HELD)


if __name__ == "__main__":
    unittest.main()
