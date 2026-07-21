#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    METRICS_DIGEST_FIELD as SOURCE_METRICS_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    digest_without,
)
from runtime.kuuos_codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1 import (
    COMPARISON_METRICS_DIGEST_FIELD,
    DISPOSITION_CONFIRMED,
    DISPOSITION_NOT_CONFIRMED,
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_generated_patch_error_reduction_comparative_replay_evaluation,
)
from scripts.build_codeai_generated_patch_error_reduction_comparative_replay_fixture_v0_1 import (
    build_fixture,
)


def _run(fixture: dict):
    return build_codeai_generated_patch_error_reduction_comparative_replay_evaluation(
        baseline_evidence=fixture["baseline"]["evidence"],
        baseline_receipt=fixture["baseline"]["receipt"],
        successor_evidence=fixture["successor"]["evidence"],
        successor_receipt=fixture["successor"]["receipt"],
        request=fixture["comparison_request"],
        policy=fixture["comparison_policy"],
    )


def _reseal_request(fixture: dict) -> None:
    request = fixture["comparison_request"]
    request[REQUEST_DIGEST_FIELD] = digest_without(request, REQUEST_DIGEST_FIELD)


def _reseal_policy(fixture: dict) -> None:
    policy = fixture["comparison_policy"]
    policy[POLICY_DIGEST_FIELD] = digest_without(policy, POLICY_DIGEST_FIELD)


def _refresh_source(fixture: dict, name: str) -> None:
    evidence = fixture[name]["evidence"]
    receipt = fixture[name]["receipt"]
    metrics = evidence["metrics"]
    metrics[SOURCE_METRICS_DIGEST_FIELD] = digest_without(
        metrics, SOURCE_METRICS_DIGEST_FIELD
    )
    evidence["metrics_digest"] = metrics[SOURCE_METRICS_DIGEST_FIELD]
    evidence[SOURCE_EVIDENCE_DIGEST_FIELD] = digest_without(
        evidence, SOURCE_EVIDENCE_DIGEST_FIELD
    )
    receipt["metrics_digest"] = evidence["metrics_digest"]
    receipt["evidence_digest"] = evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
    for field in (
        "evaluation_id",
        "dataset_id",
        "repository_full_name",
        "request_digest",
        "policy_digest",
        "dataset_digest",
        "evaluated_case_count",
        "exact_source_correspondence_verified",
        "read_only_replay_evaluation_completed",
        "historical_code_reexecuted",
        "provider_invoked",
        "verification_runner_invoked",
        "repository_mutation_performed",
        "git_effect_performed",
        "network_accessed",
        "secret_material_read",
        "selection_authority_granted",
        "successor_stage_authority_granted",
    ):
        receipt[field] = evidence[field]
    receipt[SOURCE_RECEIPT_DIGEST_FIELD] = digest_without(
        receipt, SOURCE_RECEIPT_DIGEST_FIELD
    )
    request = fixture["comparison_request"]
    policy = fixture["comparison_policy"]
    request[f"{name}_evidence_digest"] = evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
    request[f"{name}_receipt_digest"] = receipt[SOURCE_RECEIPT_DIGEST_FIELD]
    policy[f"expected_{name}_evidence_digest"] = evidence[
        SOURCE_EVIDENCE_DIGEST_FIELD
    ]
    policy[f"expected_{name}_receipt_digest"] = receipt[
        SOURCE_RECEIPT_DIGEST_FIELD
    ]
    _reseal_request(fixture)
    _reseal_policy(fixture)


class GeneratedPatchErrorReductionComparativeReplayEvaluationTests(unittest.TestCase):
    def test_reference_comparison_confirms_error_reduction(self) -> None:
        fixture = build_fixture()
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.evidence)
        self.assertIsNotNone(result.receipt)
        assert result.evidence is not None
        assert result.receipt is not None
        self.assertEqual(
            result.receipt["codeai_disposition"], DISPOSITION_CONFIRMED
        )
        self.assertTrue(result.receipt["error_reduction_confirmed"])
        metrics = result.evidence["comparison_metrics"]
        self.assertEqual(metrics["verified_patch_count_delta"], 1)
        self.assertEqual(metrics["first_failure_count_deltas"]["typecheck"], -1)
        self.assertEqual(metrics["repeated_error_fingerprint_count_delta"], -1)
        self.assertEqual(
            metrics["cases_with_repeated_error_fingerprint_delta"], -2
        )
        self.assertEqual(metrics["target_count"], 8)
        self.assertEqual(metrics["targets_met_count"], 8)
        self.assertTrue(metrics["all_targets_met"])

    def test_fixed_inputs_are_deterministic(self) -> None:
        fixture = build_fixture()
        self.assertEqual(_run(fixture), _run(fixture))

    def test_valid_comparison_can_be_not_confirmed(self) -> None:
        fixture = build_fixture()
        fixture["comparison_policy"][
            "minimum_independent_verification_pass_rate_delta_basis_points"
        ] = 4000
        _reseal_policy(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertIsNotNone(result.receipt)
        assert result.receipt is not None
        self.assertEqual(
            result.receipt["codeai_disposition"], DISPOSITION_NOT_CONFIRMED
        )
        self.assertFalse(result.receipt["error_reduction_confirmed"])

    def test_request_digest_mismatch_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_request"]["comparison_id"] = "tampered"
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_digest_mismatch", result.issues)

    def test_policy_digest_mismatch_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_policy"]["maximum_request_age"] = 99
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_digest_mismatch", result.issues)

    def test_baseline_evidence_digest_mismatch_blocks(self) -> None:
        fixture = build_fixture()
        fixture["baseline"]["evidence"]["dataset_id"] = "tampered"
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("baseline_evidence_digest_mismatch", result.issues)

    def test_successor_receipt_digest_mismatch_blocks(self) -> None:
        fixture = build_fixture()
        fixture["successor"]["receipt"]["comparison"] = "extra"
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any(issue.startswith("successor_receipt_extra_fields") for issue in result.issues)
        )

    def test_request_repository_correspondence_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_request"][
            "repository_full_name"
        ] = "itakura-hidetoshi/Other"
        _reseal_request(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_repository_correspondence_mismatch", result.issues)

    def test_policy_repository_correspondence_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_policy"][
            "expected_repository_full_name"
        ] = "itakura-hidetoshi/Other"
        _reseal_policy(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_repository_correspondence_mismatch", result.issues)

    def test_unauthorized_evaluator_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_request"]["evaluator_id"] = "other-evaluator"
        _reseal_request(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("evaluator_not_authorized", result.issues)

    def test_stale_request_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_policy"]["evaluation_epoch"] = 400
        _reseal_policy(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_stale", result.issues)

    def test_future_request_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_request"]["request_created_epoch"] = 400
        _reseal_request(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_from_future", result.issues)

    def test_identical_dataset_digest_blocks(self) -> None:
        fixture = build_fixture()
        fixture["successor"]["evidence"]["dataset_digest"] = fixture["baseline"][
            "evidence"
        ]["dataset_digest"]
        _refresh_source(fixture, "successor")
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_dataset_digests_not_distinct", result.issues)

    def test_forbidden_execution_policy_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_policy"]["allow_provider_invocation"] = True
        _reseal_policy(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "policy_required_false:allow_provider_invocation", result.issues
        )

    def test_missing_request_field_blocks(self) -> None:
        fixture = build_fixture()
        del fixture["comparison_request"]["compare_error_recurrence"]
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any(issue.startswith("request_missing_fields") for issue in result.issues)
        )

    def test_extra_policy_field_blocks(self) -> None:
        fixture = build_fixture()
        fixture["comparison_policy"]["unexpected"] = False
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any(issue.startswith("policy_extra_fields") for issue in result.issues)
        )

    def test_undefined_source_ratio_blocks(self) -> None:
        fixture = build_fixture()
        ratio = fixture["successor"]["evidence"]["metrics"][
            "provider_calls_per_verified_patch"
        ]
        ratio["denominator"] = 0
        ratio["defined"] = False
        ratio["basis_points"] = None
        _refresh_source(fixture, "successor")
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "ratio_undefined:provider_calls_per_verified_patch_delta_basis_points",
            result.issues,
        )

    def test_source_effect_claim_blocks_even_when_resealed(self) -> None:
        fixture = build_fixture()
        fixture["successor"]["evidence"]["git_effect_performed"] = True
        _refresh_source(fixture, "successor")
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("successor_required_false:git_effect_performed", result.issues)

    def test_source_receipt_evidence_mismatch_blocks(self) -> None:
        fixture = build_fixture()
        receipt = fixture["baseline"]["receipt"]
        receipt["evidence_digest"] = "f" * 64
        receipt[SOURCE_RECEIPT_DIGEST_FIELD] = digest_without(
            receipt, SOURCE_RECEIPT_DIGEST_FIELD
        )
        fixture["comparison_request"]["baseline_receipt_digest"] = receipt[
            SOURCE_RECEIPT_DIGEST_FIELD
        ]
        fixture["comparison_policy"][
            "expected_baseline_receipt_digest"
        ] = receipt[SOURCE_RECEIPT_DIGEST_FIELD]
        _reseal_request(fixture)
        _reseal_policy(fixture)
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("baseline_receipt_evidence_digest_mismatch", result.issues)

    def test_source_profile_substitution_blocks(self) -> None:
        fixture = build_fixture()
        fixture["baseline"]["evidence"]["profile_version"] = "Other v0.1"
        _refresh_source(fixture, "baseline")
        result = _run(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("baseline_evidence_profile_unsupported", result.issues)

    def test_comparison_output_digests_are_canonical(self) -> None:
        result = _run(build_fixture())
        assert result.evidence is not None
        assert result.receipt is not None
        metrics = result.evidence["comparison_metrics"]
        self.assertEqual(
            metrics[COMPARISON_METRICS_DIGEST_FIELD],
            digest_without(metrics, COMPARISON_METRICS_DIGEST_FIELD),
        )
        self.assertEqual(
            result.evidence[EVIDENCE_DIGEST_FIELD],
            digest_without(result.evidence, EVIDENCE_DIGEST_FIELD),
        )
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            digest_without(result.receipt, RECEIPT_DIGEST_FIELD),
        )

    def test_comparison_performs_no_effects_or_epistemic_overclaim(self) -> None:
        result = _run(build_fixture())
        assert result.receipt is not None
        for field in (
            "historical_code_reexecuted",
            "provider_invoked",
            "verification_runner_invoked",
            "repository_mutation_performed",
            "git_effect_performed",
            "network_accessed",
            "secret_material_read",
            "selection_authority_granted",
            "successor_stage_authority_granted",
            "correctness_proof_claimed",
            "probability_claimed",
            "dataset_unbiasedness_claimed",
        ):
            self.assertFalse(result.receipt[field], field)

    def test_original_fixture_is_not_mutated(self) -> None:
        fixture = build_fixture()
        original = copy.deepcopy(fixture)
        _run(fixture)
        self.assertEqual(fixture, original)


if __name__ == "__main__":
    unittest.main()
