from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from runtime.kuuos_codeai_evidence_grounded_candidate_ranking_v0_1 import (
    POLICY_DIGEST_FIELD,
    RANKING_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SOURCE_PORTFOLIO_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_evidence_grounded_candidate_ranking,
    seal,
)
from scripts.build_codeai_evidence_grounded_candidate_ranking_fixture_v0_1 import build_fixture

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads(
    (ROOT / "examples/codeai_evidence_grounded_candidate_ranking_v0_1.json").read_text(
        encoding="utf-8"
    )
)


def reseal_in_place(value: dict, field: str) -> None:
    value.pop(field, None)
    sealed = seal(value, field)
    value.clear()
    value.update(sealed)


def run(data: dict):
    return build_codeai_evidence_grounded_candidate_ranking(
        source_portfolio=data["source_portfolio"],
        source_portfolio_receipt=data["source_portfolio_receipt"],
        ranking_request=data["ranking_request"],
        ranking_policy=data["ranking_policy"],
    )


class EvidenceGroundedCandidateRankingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = build_fixture(SPEC)

    def fixture(self) -> dict:
        return copy.deepcopy(self.base)

    def assert_blocked(self, data: dict) -> None:
        result = run(data)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.ranking)
        self.assertIsNone(result.receipt)
        self.assertTrue(result.issues)

    def test_01_example_ready(self) -> None:
        result = run(self.fixture())
        self.assertEqual(result.status, STATUS_READY)
        self.assertIsNotNone(result.ranking)
        self.assertIsNotNone(result.receipt)

    def test_02_deterministic(self) -> None:
        data = self.fixture()
        left = run(data)
        right = run(data)
        self.assertEqual(left.ranking, right.ranking)
        self.assertEqual(left.receipt, right.receipt)

    def test_03_expected_order(self) -> None:
        result = run(self.fixture())
        self.assertEqual(result.ranking["ordered_candidate_ids"], SPEC["expected_ordered_candidate_ids"])

    def test_04_positions_contiguous(self) -> None:
        result = run(self.fixture())
        self.assertEqual(
            [item["ranking_position"] for item in result.ranking["ranked_candidates"]],
            [1, 2, 3, 4],
        )

    def test_05_source_evidence_preserved(self) -> None:
        data = self.fixture()
        result = run(data)
        by_id = {item["candidate_id"]: item for item in data["source_portfolio"]["candidates"]}
        for ranked in result.ranking["ranked_candidates"]:
            self.assertEqual(ranked["source_candidate_evidence"], by_id[ranked["candidate_id"]])

    def test_06_no_selection_or_effect_authority(self) -> None:
        result = run(self.fixture())
        for surface in (result.ranking, result.receipt):
            for field in (
                "candidate_selected",
                "selection_authority_granted",
                "verification_runner_invoked",
                "repair_executed",
                "repository_mutation_performed",
                "git_effect_performed",
                "execution_authority_granted",
                "git_authority_granted",
            ):
                self.assertIs(surface[field], False)

    def test_07_request_digest_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_request"][REQUEST_DIGEST_FIELD] = "0" * 64
        self.assert_blocked(data)

    def test_08_policy_digest_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_policy"][POLICY_DIGEST_FIELD] = "0" * 64
        self.assert_blocked(data)

    def test_09_source_portfolio_digest_mismatch(self) -> None:
        data = self.fixture()
        data["source_portfolio"][SOURCE_PORTFOLIO_DIGEST_FIELD] = "0" * 64
        self.assert_blocked(data)

    def test_10_source_receipt_digest_mismatch(self) -> None:
        data = self.fixture()
        data["source_portfolio_receipt"][SOURCE_RECEIPT_DIGEST_FIELD] = "0" * 64
        self.assert_blocked(data)

    def test_11_request_portfolio_digest_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_request"]["source_portfolio_digest"] = "1" * 64
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_12_request_receipt_digest_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_request"]["source_portfolio_receipt_digest"] = "1" * 64
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_13_policy_portfolio_digest_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["expected_source_portfolio_digest"] = "1" * 64
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_14_policy_receipt_digest_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["expected_source_portfolio_receipt_digest"] = "1" * 64
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_15_request_repository_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_request"]["repository_full_name"] = "other/repository"
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_16_policy_repository_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["expected_repository_full_name"] = "other/repository"
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_17_request_source_commit_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_request"]["source_commit_sha"] = "1" * 40
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_18_policy_source_commit_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["expected_source_commit_sha"] = "1" * 40
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_19_request_snapshot_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_request"]["source_repository_snapshot_digest"] = "1" * 64
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_20_policy_snapshot_mismatch(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["expected_source_repository_snapshot_digest"] = "1" * 64
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_21_stale_request(self) -> None:
        data = self.fixture()
        data["ranking_request"]["request_created_epoch"] = 1
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_22_future_request(self) -> None:
        data = self.fixture()
        data["ranking_request"]["request_created_epoch"] = data["ranking_policy"]["evaluation_epoch"] + 1
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_23_unresolved_questions(self) -> None:
        data = self.fixture()
        data["ranking_request"]["unresolved_ranking_questions"] = ["question"]
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_24_request_claims_selection_authority(self) -> None:
        data = self.fixture()
        data["ranking_request"]["claims_selection_authority"] = True
        reseal_in_place(data["ranking_request"], REQUEST_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_25_authority_flags_fail_closed(self) -> None:
        for field in (
            "allow_candidate_selection",
            "allow_verification_runner_invocation",
            "allow_repair_execution",
            "allow_repository_mutation",
            "allow_execution_authority",
            "allow_git_authority",
        ):
            with self.subTest(field=field):
                data = self.fixture()
                data["ranking_policy"][field] = True
                reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
                self.assert_blocked(data)

    def test_26_required_preservation_flags_fail_closed(self) -> None:
        for field in (
            "require_exact_lineage",
            "require_classification_preservation",
            "require_finding_evidence_preservation",
            "require_stable_tie_break",
        ):
            with self.subTest(field=field):
                data = self.fixture()
                data["ranking_policy"][field] = False
                reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
                self.assert_blocked(data)

    def test_27_candidate_budget(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["maximum_candidates"] = 3
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_28_finding_budget(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["maximum_total_findings"] = 2
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_29_classification_priority_invalid(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["classification_priority"] = list(
            reversed(data["ranking_policy"]["classification_priority"])
        )
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_30_strategy_invalid(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["ranking_strategy"] = "score_then_select"
        reseal_in_place(data["ranking_policy"], POLICY_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_31_source_portfolio_already_ranked(self) -> None:
        data = self.fixture()
        data["source_portfolio"]["ranking_performed"] = True
        reseal_in_place(data["source_portfolio"], SOURCE_PORTFOLIO_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_32_source_portfolio_already_selected(self) -> None:
        data = self.fixture()
        data["source_portfolio"]["candidate_selected"] = True
        reseal_in_place(data["source_portfolio"], SOURCE_PORTFOLIO_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_33_source_candidate_already_ranked(self) -> None:
        data = self.fixture()
        data["source_portfolio"]["candidates"][0]["rank_assigned"] = True
        reseal_in_place(data["source_portfolio"], SOURCE_PORTFOLIO_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_34_source_candidate_evidence_not_preserved(self) -> None:
        data = self.fixture()
        data["source_portfolio"]["candidates"][0]["finding_evidence_preserved"] = False
        reseal_in_place(data["source_portfolio"], SOURCE_PORTFOLIO_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_35_source_receipt_already_ranked(self) -> None:
        data = self.fixture()
        data["source_portfolio_receipt"]["ranking_performed"] = True
        reseal_in_place(data["source_portfolio_receipt"], SOURCE_RECEIPT_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_36_source_receipt_portfolio_pointer_mismatch(self) -> None:
        data = self.fixture()
        data["source_portfolio_receipt"]["evidence_bearing_candidate_portfolio_digest"] = "1" * 64
        reseal_in_place(data["source_portfolio_receipt"], SOURCE_RECEIPT_DIGEST_FIELD)
        self.assert_blocked(data)

    def test_37_request_extra_field(self) -> None:
        data = self.fixture()
        data["ranking_request"]["unexpected"] = True
        self.assert_blocked(data)

    def test_38_policy_extra_field(self) -> None:
        data = self.fixture()
        data["ranking_policy"]["unexpected"] = True
        self.assert_blocked(data)

    def test_39_request_missing_field(self) -> None:
        data = self.fixture()
        del data["ranking_request"]["ranking_purpose"]
        self.assert_blocked(data)

    def test_40_policy_missing_field(self) -> None:
        data = self.fixture()
        del data["ranking_policy"]["ranking_strategy"]
        self.assert_blocked(data)

    def test_41_ranking_digest_is_sealed(self) -> None:
        result = run(self.fixture())
        self.assertEqual(
            result.ranking[RANKING_DIGEST_FIELD],
            seal(
                {key: value for key, value in result.ranking.items() if key != RANKING_DIGEST_FIELD},
                RANKING_DIGEST_FIELD,
            )[RANKING_DIGEST_FIELD],
        )

    def test_42_receipt_digest_is_sealed(self) -> None:
        result = run(self.fixture())
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            seal(
                {key: value for key, value in result.receipt.items() if key != RECEIPT_DIGEST_FIELD},
                RECEIPT_DIGEST_FIELD,
            )[RECEIPT_DIGEST_FIELD],
        )


if __name__ == "__main__":
    unittest.main()
