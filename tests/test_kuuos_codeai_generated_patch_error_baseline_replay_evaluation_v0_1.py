#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    CASE_DIGEST_FIELD,
    CASE_PROFILE_VERSION,
    DATASET_DIGEST_FIELD,
    DATASET_PROFILE_VERSION,
    EVIDENCE_DIGEST_FIELD,
    METRICS_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SCHEMA_VERSION,
    STAGE_ABORTED,
    STAGE_FAILED,
    STAGE_NOT_RUN,
    STAGE_PASSED,
    STATUS_BLOCKED,
    STATUS_READY,
    VERIFICATION_NOT_RUN,
    VERIFICATION_PASSED,
    build_codeai_generated_patch_error_baseline_replay_evaluation,
    digest_without,
    seal,
)


def digest(char: str) -> str:
    return char * 64


def git_sha(char: str) -> str:
    return char * 40


def make_case(
    *,
    case_id: str,
    candidate_char: str,
    stage_statuses: tuple[str, str, str, str, str, str],
    verification_status: str,
    repair_cycle_count: int = 0,
    repair_reached_green: bool = False,
    provider_call_count: int = 1,
    generated_output_bytes: int = 100,
    error_fingerprints: list[str] | None = None,
    observed_epoch: int = 100,
) -> dict:
    application_required = stage_statuses[1] != STAGE_NOT_RUN
    verification_execution_required = any(
        status != STAGE_NOT_RUN for status in stage_statuses[4:6]
    )
    independent_required = verification_status != VERIFICATION_NOT_RUN
    case = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": CASE_PROFILE_VERSION,
        "case_id": case_id,
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": git_sha(candidate_char),
        "candidate_digest": digest(candidate_char),
        "patch_artifact_digest": digest(chr(ord(candidate_char) + 1)),
        "generation_receipt_digest": digest(chr(ord(candidate_char) + 2)),
        "application_receipt_digest": digest(chr(ord(candidate_char) + 3))
        if application_required
        else None,
        "verification_execution_receipt_digest": digest(
            chr(ord(candidate_char) + 4)
        )
        if verification_execution_required
        else None,
        "independent_verification_receipt_digest": digest(
            chr(ord(candidate_char) + 5)
        )
        if independent_required
        else None,
        "provider_id": "gpt",
        "model_id": "model-v1",
        "structured_output_status": stage_statuses[0],
        "patch_application_status": stage_statuses[1],
        "parse_status": stage_statuses[2],
        "typecheck_status": stage_statuses[3],
        "targeted_test_status": stage_statuses[4],
        "full_regression_status": stage_statuses[5],
        "independent_verification_status": verification_status,
        "repair_cycle_count": repair_cycle_count,
        "repair_reached_green": repair_reached_green,
        "provider_call_count": provider_call_count,
        "generated_output_bytes": generated_output_bytes,
        "error_fingerprints": list(error_fingerprints or []),
        "observed_epoch": observed_epoch,
    }
    return seal(case, CASE_DIGEST_FIELD)


def make_bundle() -> tuple[dict, dict, dict]:
    cases = [
        make_case(
            case_id="case-pass",
            candidate_char="1",
            stage_statuses=(STAGE_PASSED,) * 6,
            verification_status=VERIFICATION_PASSED,
            provider_call_count=2,
            generated_output_bytes=1000,
        ),
        make_case(
            case_id="case-type-fail",
            candidate_char="2",
            stage_statuses=(
                STAGE_PASSED,
                STAGE_PASSED,
                STAGE_PASSED,
                STAGE_FAILED,
                STAGE_NOT_RUN,
                STAGE_NOT_RUN,
            ),
            verification_status=VERIFICATION_NOT_RUN,
            provider_call_count=1,
            generated_output_bytes=500,
            error_fingerprints=["TYPE_MISMATCH"],
        ),
        make_case(
            case_id="case-repaired",
            candidate_char="3",
            stage_statuses=(STAGE_PASSED,) * 6,
            verification_status=VERIFICATION_PASSED,
            repair_cycle_count=1,
            repair_reached_green=True,
            provider_call_count=3,
            generated_output_bytes=1500,
            error_fingerprints=["TYPE_MISMATCH"],
        ),
    ]
    dataset = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": DATASET_PROFILE_VERSION,
            "dataset_id": "baseline-dataset-001",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "window_start_epoch": 90,
            "window_end_epoch": 110,
            "case_digests": [case[CASE_DIGEST_FIELD] for case in cases],
            "cases": cases,
        },
        DATASET_DIGEST_FIELD,
    )
    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "evaluation_id": "baseline-evaluation-001",
            "dataset_digest": dataset[DATASET_DIGEST_FIELD],
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "evaluator_id": "codeai-baseline-evaluator",
            "request_created_epoch": 120,
            "compute_stage_baseline": True,
            "compute_error_fingerprint_baseline": True,
            "compute_repair_efficiency": True,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "expected_repository_full_name": "itakura-hidetoshi/KuuOS",
            "expected_dataset_digest": dataset[DATASET_DIGEST_FIELD],
            "authorized_evaluator_ids": ["codeai-baseline-evaluator"],
            "maximum_request_age": 20,
            "maximum_cases": 16,
            "maximum_error_fingerprints_per_case": 8,
            "maximum_repair_cycles_per_case": 4,
            "maximum_provider_calls_per_case": 8,
            "maximum_generated_output_bytes_per_case": 10000,
            "evaluation_epoch": 125,
            "require_exact_case_digests": True,
            "require_sequential_stage_evidence": True,
            "allow_read_only_replay_evaluation": True,
            "allow_execution": False,
            "allow_repository_mutation": False,
            "allow_git_effect": False,
            "allow_network_access": False,
            "allow_secret_read": False,
            "allow_selection_authority": False,
            "allow_successor_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    return dataset, request, policy


def reseal_case(dataset: dict, index: int) -> None:
    dataset["cases"][index][CASE_DIGEST_FIELD] = digest_without(
        dataset["cases"][index], CASE_DIGEST_FIELD
    )
    dataset["case_digests"][index] = dataset["cases"][index][CASE_DIGEST_FIELD]
    dataset[DATASET_DIGEST_FIELD] = digest_without(dataset, DATASET_DIGEST_FIELD)


def reseal_request(request: dict) -> None:
    request[REQUEST_DIGEST_FIELD] = digest_without(request, REQUEST_DIGEST_FIELD)


def reseal_policy(policy: dict) -> None:
    policy[POLICY_DIGEST_FIELD] = digest_without(policy, POLICY_DIGEST_FIELD)


class GeneratedPatchErrorBaselineReplayEvaluationTests(unittest.TestCase):
    def test_ready_metrics_and_no_effects(self) -> None:
        dataset, request, policy = make_bundle()
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset,
            request=request,
            policy=policy,
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.evidence)
        self.assertIsNotNone(result.receipt)
        assert result.evidence is not None
        assert result.receipt is not None
        metrics = result.evidence["metrics"]
        self.assertEqual(metrics["total_case_count"], 3)
        self.assertEqual(metrics["stage_metrics"]["typecheck"]["passed_count"], 2)
        self.assertEqual(
            metrics["stage_metrics"]["typecheck"]["failed_count"],
            1,
        )
        self.assertEqual(metrics["verified_patch_count"], 2)
        self.assertEqual(metrics["repair_green_case_count"], 1)
        self.assertEqual(metrics["repeated_error_fingerprint_count"], 1)
        self.assertEqual(metrics["cases_with_repeated_error_fingerprint"], 2)
        self.assertFalse(result.evidence["historical_code_reexecuted"])
        self.assertFalse(result.evidence["repository_mutation_performed"])
        self.assertFalse(result.evidence["git_effect_performed"])
        self.assertFalse(result.receipt["correctness_proof_claimed"])
        self.assertEqual(
            result.evidence[EVIDENCE_DIGEST_FIELD],
            digest_without(result.evidence, EVIDENCE_DIGEST_FIELD),
        )
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            digest_without(result.receipt, RECEIPT_DIGEST_FIELD),
        )
        self.assertEqual(
            metrics[METRICS_DIGEST_FIELD],
            digest_without(metrics, METRICS_DIGEST_FIELD),
        )

    def test_deterministic_for_fixed_inputs(self) -> None:
        dataset, request, policy = make_bundle()
        first = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        second = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(first, second)

    def test_dataset_digest_mismatch_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["dataset_id"] = "tampered"
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("dataset_digest_mismatch", result.issues)

    def test_case_digest_mismatch_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"][0]["provider_call_count"] = 7
        dataset[DATASET_DIGEST_FIELD] = digest_without(dataset, DATASET_DIGEST_FIELD)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("case_digest_mismatch" in issue for issue in result.issues))

    def test_duplicate_case_id_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"][1]["case_id"] = dataset["cases"][0]["case_id"]
        reseal_case(dataset, 1)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("dataset_duplicate_case_id", result.issues)

    def test_repository_mismatch_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        request["repository_full_name"] = "itakura-hidetoshi/Other"
        reseal_request(request)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_repository_correspondence_mismatch", result.issues)

    def test_request_digest_mismatch_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        request["evaluation_id"] = "changed"
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_digest_mismatch", result.issues)

    def test_policy_digest_mismatch_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["maximum_cases"] = 99
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_digest_mismatch", result.issues)

    def test_stale_request_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["evaluation_epoch"] = 200
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_stale", result.issues)

    def test_future_request_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        request["request_created_epoch"] = 130
        reseal_request(request)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_from_future", result.issues)

    def test_unauthorized_evaluator_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        request["evaluator_id"] = "other-evaluator"
        reseal_request(request)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("evaluator_not_authorized", result.issues)

    def test_nonsequential_stage_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"][1]["patch_application_status"] = STAGE_FAILED
        dataset["cases"][1]["parse_status"] = STAGE_PASSED
        reseal_case(dataset, 1)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_nonsequential_stage_evidence" in issue for issue in result.issues)
        )

    def test_case_budget_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["maximum_cases"] = 2
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("dataset_case_budget_exceeded", result.issues)

    def test_fingerprint_budget_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["maximum_error_fingerprints_per_case"] = 0
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_error_fingerprint_budget_exceeded" in issue for issue in result.issues)
        )

    def test_repair_cycle_budget_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["maximum_repair_cycles_per_case"] = 0
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_repair_cycle_budget_exceeded" in issue for issue in result.issues)
        )

    def test_provider_call_budget_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["maximum_provider_calls_per_case"] = 2
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_provider_call_budget_exceeded" in issue for issue in result.issues)
        )

    def test_output_budget_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["maximum_generated_output_bytes_per_case"] = 1000
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_generated_output_budget_exceeded" in issue for issue in result.issues)
        )

    def test_forbidden_execution_policy_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        policy["allow_execution"] = True
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_required_false:allow_execution", result.issues)

    def test_empty_dataset_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"] = []
        dataset["case_digests"] = []
        dataset[DATASET_DIGEST_FIELD] = digest_without(dataset, DATASET_DIGEST_FIELD)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("dataset_cases_invalid", result.issues)

    def test_case_outside_window_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"][0]["observed_epoch"] = 999
        reseal_case(dataset, 0)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("observed_epoch_outside_window" in issue for issue in result.issues)
        )

    def test_invalid_error_fingerprint_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"][1]["error_fingerprints"] = ["not valid"]
        reseal_case(dataset, 1)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_error_fingerprint_invalid" in issue for issue in result.issues)
        )

    def test_missing_application_receipt_blocks(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"][0]["application_receipt_digest"] = None
        reseal_case(dataset, 0)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any("case_required_digest_invalid:application_receipt_digest" in issue for issue in result.issues)
        )

    def test_zero_verified_patch_ratios_are_undefined(self) -> None:
        dataset, request, policy = make_bundle()
        dataset["cases"] = [copy.deepcopy(dataset["cases"][1])]
        dataset["case_digests"] = [dataset["cases"][0][CASE_DIGEST_FIELD]]
        dataset[DATASET_DIGEST_FIELD] = digest_without(dataset, DATASET_DIGEST_FIELD)
        request["dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_request(request)
        policy["expected_dataset_digest"] = dataset[DATASET_DIGEST_FIELD]
        reseal_policy(policy)
        result = build_codeai_generated_patch_error_baseline_replay_evaluation(
            dataset=dataset, request=request, policy=policy
        )
        self.assertEqual(result.status, STATUS_READY)
        assert result.evidence is not None
        ratio = result.evidence["metrics"]["provider_calls_per_verified_patch"]
        self.assertFalse(ratio["defined"])
        self.assertIsNone(ratio["basis_points"])
        self.assertEqual(ratio["denominator"], 0)


if __name__ == "__main__":
    unittest.main()
