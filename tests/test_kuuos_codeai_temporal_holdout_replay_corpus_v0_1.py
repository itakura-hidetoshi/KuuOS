#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import unittest

from scripts.build_codeai_temporal_holdout_replay_corpus_fixture_v0_1 import build_fixture, project_fixture
from runtime.kuuos_codeai_temporal_holdout_replay_corpus_v0_1 import (
    CORPUS_DIGEST_FIELD,
    DISPOSITION_SEALED,
    ENTRY_DIGEST_FIELD,
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SPLIT_DEVELOPMENT,
    SPLIT_HOLDOUT,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_temporal_holdout_replay_corpus,
    seal,
)


def _reseal_corpus(fixture: dict, index: int | None = None) -> None:
    corpus = fixture["corpus"]
    if index is not None:
        corpus["entries"][index] = seal(corpus["entries"][index], ENTRY_DIGEST_FIELD)
    corpus["entry_digests"] = [entry[ENTRY_DIGEST_FIELD] for entry in corpus["entries"]]
    corpus["development_entry_digests"] = [
        entry[ENTRY_DIGEST_FIELD]
        for entry in corpus["entries"]
        if entry["split"] == SPLIT_DEVELOPMENT
    ]
    corpus["holdout_entry_digests"] = [
        entry[ENTRY_DIGEST_FIELD]
        for entry in corpus["entries"]
        if entry["split"] == SPLIT_HOLDOUT
    ]
    corpus["development_case_count"] = len(corpus["development_entry_digests"])
    corpus["holdout_case_count"] = len(corpus["holdout_entry_digests"])
    corpus["scenario_classes"] = sorted({entry["scenario_class"] for entry in corpus["entries"]})
    fixture["corpus"] = seal(corpus, CORPUS_DIGEST_FIELD)
    fixture["request"]["corpus_digest"] = fixture["corpus"][CORPUS_DIGEST_FIELD]
    fixture["request"] = seal(fixture["request"], REQUEST_DIGEST_FIELD)
    fixture["policy"]["expected_corpus_digest"] = fixture["corpus"][CORPUS_DIGEST_FIELD]
    fixture["policy"] = seal(fixture["policy"], POLICY_DIGEST_FIELD)


def _build(fixture: dict):
    return build_codeai_temporal_holdout_replay_corpus(
        corpus=fixture["corpus"],
        request=fixture["request"],
        policy=fixture["policy"],
    )


class TemporalHoldoutReplayCorpusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = build_fixture()

    def test_reference_fixture_is_ready(self) -> None:
        result = _build(self.fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.evidence)
        self.assertIsNotNone(result.receipt)

    def test_reference_disposition_is_sealed(self) -> None:
        result = _build(self.fixture)
        assert result.receipt is not None
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_SEALED)

    def test_reference_counts_are_three_and_three(self) -> None:
        result = _build(self.fixture)
        assert result.evidence is not None
        self.assertEqual(result.evidence["development_case_count"], 3)
        self.assertEqual(result.evidence["holdout_case_count"], 3)

    def test_reference_split_overlap_is_zero(self) -> None:
        result = _build(self.fixture)
        assert result.evidence is not None
        self.assertEqual(result.evidence["cross_split_case_id_overlap_count"], 0)
        self.assertEqual(result.evidence["cross_split_issue_digest_overlap_count"], 0)
        self.assertEqual(result.evidence["cross_split_replay_case_digest_overlap_count"], 0)

    def test_reference_holdout_protections_are_true(self) -> None:
        result = _build(self.fixture)
        assert result.evidence is not None
        for field in (
            "holdout_hidden_from_candidate_generation",
            "holdout_excluded_from_threshold_tuning",
            "holdout_excluded_from_memory_training",
            "holdout_excluded_from_prompt_selection",
            "holdout_excluded_from_model_selection",
        ):
            self.assertIs(result.evidence[field], True)

    def test_reference_overclaims_are_false(self) -> None:
        result = _build(self.fixture)
        assert result.evidence is not None
        for field in (
            "representativeness_claimed", "randomness_claimed",
            "unbiasedness_claimed", "correctness_proof_claimed",
        ):
            self.assertIs(result.evidence[field], False)

    def test_evidence_and_receipt_seals_are_deterministic(self) -> None:
        result = _build(self.fixture)
        assert result.evidence is not None and result.receipt is not None
        self.assertEqual(
            result.evidence[EVIDENCE_DIGEST_FIELD],
            seal(result.evidence, EVIDENCE_DIGEST_FIELD)[EVIDENCE_DIGEST_FIELD],
        )
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            seal(result.receipt, RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD],
        )

    def test_projection_is_deterministic(self) -> None:
        self.assertEqual(project_fixture(build_fixture()), project_fixture(build_fixture()))

    def test_entry_digest_tamper_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][0]["case_id"] = "tampered-case"
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("entry:0_digest_mismatch" in issue for issue in result.issues))

    def test_corpus_digest_tamper_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["cutoff_epoch"] = 101
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("corpus_digest_mismatch", result.issues)

    def test_request_digest_tamper_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["request"]["request_created_epoch"] = 141
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_digest_mismatch", result.issues)

    def test_policy_digest_tamper_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["policy"]["minimum_holdout_cases"] = 4
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_digest_mismatch", result.issues)

    def test_development_entry_after_cutoff_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][0]["observed_epoch"] = 110
        _reseal_corpus(fixture, 0)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("development_entry_outside_window" in issue for issue in result.issues))

    def test_holdout_entry_before_cutoff_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][3]["observed_epoch"] = 95
        _reseal_corpus(fixture, 3)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("holdout_entry_outside_window" in issue for issue in result.issues))

    def test_case_id_overlap_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][3]["case_id"] = fixture["corpus"]["entries"][0]["case_id"]
        _reseal_corpus(fixture, 3)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("cross_split_case_id_overlap" in issue for issue in result.issues))

    def test_issue_digest_overlap_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][3]["issue_digest"] = fixture["corpus"]["entries"][0]["issue_digest"]
        _reseal_corpus(fixture, 3)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("cross_split_issue_digest_overlap", result.issues)

    def test_replay_digest_overlap_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][3]["replay_case_digest"] = fixture["corpus"]["entries"][0]["replay_case_digest"]
        _reseal_corpus(fixture, 3)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("cross_split_replay_case_digest_overlap", result.issues)

    def test_holdout_label_exposure_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][3]["labels_available_to_candidate_generation"] = True
        _reseal_corpus(fixture, 3)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("holdout_label_exposed" in issue for issue in result.issues))

    def test_holdout_threshold_tuning_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][3]["used_for_threshold_tuning"] = True
        _reseal_corpus(fixture, 3)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("holdout_used_for_threshold_tuning" in issue for issue in result.issues))

    def test_holdout_memory_training_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][4]["used_for_memory_training"] = True
        _reseal_corpus(fixture, 4)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("holdout_used_for_memory_training" in issue for issue in result.issues))

    def test_holdout_prompt_selection_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][4]["used_for_prompt_selection"] = True
        _reseal_corpus(fixture, 4)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("holdout_used_for_prompt_selection" in issue for issue in result.issues))

    def test_holdout_model_selection_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][5]["used_for_model_selection"] = True
        _reseal_corpus(fixture, 5)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("holdout_used_for_model_selection" in issue for issue in result.issues))

    def test_environment_binding_mismatch_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][5]["environment_digest"] = "f" * 64
        _reseal_corpus(fixture, 5)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("uniform_binding" in issue for issue in result.issues))

    def test_missing_scenario_class_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][5]["scenario_class"] = "abstention"
        _reseal_corpus(fixture, 5)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("required_scenario_classes_missing" in issue for issue in result.issues))

    def test_unauthorized_evaluator_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["request"]["evaluator_id"] = "unauthorized-evaluator"
        fixture["request"] = seal(fixture["request"], REQUEST_DIGEST_FIELD)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("evaluator_not_authorized", result.issues)

    def test_effect_authority_policy_blocks(self) -> None:
        fixture = deepcopy(self.fixture)
        fixture["policy"]["allow_git_effect"] = True
        fixture["policy"] = seal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = _build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_required_false:allow_git_effect", result.issues)


if __name__ == "__main__":
    unittest.main()
