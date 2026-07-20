from __future__ import annotations

import json
import unittest
from pathlib import Path

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1 import *
from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    POLICY_DIGEST_FIELD,
    PREFLIGHT_RECEIPT_DIGEST_FIELD,
    PREFLIGHT_REPORT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    PORTFOLIO_DIGEST_FIELD,
)

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"


def fixture() -> dict:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data.pop("expected_portfolio", None)
    data.pop("expected_receipt", None)
    data.pop("profile_version", None)
    data.pop("schema_version", None)
    return data


def run(data: dict):
    return build_codeai_evidence_bearing_candidate_portfolio(
        portfolio_request=data["portfolio_request"],
        portfolio_policy=data["portfolio_policy"],
        candidate_preflight_bundles=data["candidate_preflight_bundles"],
    )


def reseal_request(data: dict) -> None:
    data["portfolio_request"] = seal(data["portfolio_request"], REQUEST_DIGEST_FIELD)


def reseal_policy(data: dict) -> None:
    data["portfolio_policy"] = seal(data["portfolio_policy"], POLICY_DIGEST_FIELD)


def reseal_report_and_receipt(data: dict, index: int) -> None:
    bundle = data["candidate_preflight_bundles"][index]
    report = seal(bundle["preflight_report"], PREFLIGHT_REPORT_DIGEST_FIELD)
    receipt = bundle["preflight_receipt"]
    receipt["static_admissibility_report_digest"] = report[PREFLIGHT_REPORT_DIGEST_FIELD]
    receipt = seal(receipt, PREFLIGHT_RECEIPT_DIGEST_FIELD)
    bundle["preflight_report"] = report
    bundle["preflight_receipt"] = receipt
    candidate_id = bundle["candidate_id"]
    request_item = next(
        item for item in data["portfolio_request"]["candidate_requests"]
        if item["candidate_id"] == candidate_id
    )
    request_item["expected_typed_edit_ir_digest"] = report["typed_edit_ir_digest"]
    request_item["expected_static_admissibility_report_digest"] = report[PREFLIGHT_REPORT_DIGEST_FIELD]
    request_item["expected_preflight_receipt_digest"] = receipt[PREFLIGHT_RECEIPT_DIGEST_FIELD]
    reseal_request(data)


class EvidenceBearingCandidatePortfolioTests(unittest.TestCase):
    def test_01_example_ready(self):
        self.assertEqual(run(fixture()).status, STATUS_READY)

    def test_02_four_classifications_preserved(self):
        portfolio = run(fixture()).portfolio
        self.assertEqual(
            portfolio["classification_counts"],
            {"admissible": 1, "repairable": 1, "hold": 1, "rejected": 1},
        )

    def test_03_deterministic_request_order(self):
        portfolio = run(fixture()).portfolio
        self.assertEqual(
            portfolio["candidate_ids"],
            [
                "candidate-admissible",
                "candidate-repairable",
                "candidate-hold",
                "candidate-rejected",
            ],
        )

    def test_04_finding_evidence_preserved(self):
        data = fixture()
        portfolio = run(data).portfolio
        for source, normalized in zip(data["candidate_preflight_bundles"], portfolio["candidates"]):
            self.assertEqual(source["preflight_report"]["findings"], normalized["findings"])

    def test_05_route_receipts_preserved(self):
        portfolio = run(fixture()).portfolio
        self.assertTrue(all(candidate["preflight_route_receipt_preserved"] for candidate in portfolio["candidates"]))

    def test_06_no_ranking_or_selection(self):
        portfolio = run(fixture()).portfolio
        self.assertFalse(portfolio["ranking_performed"])
        self.assertFalse(portfolio["candidate_selected"])
        self.assertTrue(all(not candidate["rank_assigned"] for candidate in portfolio["candidates"]))
        self.assertTrue(all(not candidate["candidate_selected"] for candidate in portfolio["candidates"]))

    def test_07_no_verification_repair_execution_or_git(self):
        portfolio = run(fixture()).portfolio
        for field in (
            "verification_runner_invoked",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            self.assertFalse(portfolio[field])

    def test_08_portfolio_digest(self):
        portfolio = run(fixture()).portfolio
        self.assertEqual(portfolio[PORTFOLIO_DIGEST_FIELD], digest_without(portfolio, PORTFOLIO_DIGEST_FIELD))

    def test_09_receipt_digest(self):
        receipt = run(fixture()).receipt
        self.assertEqual(receipt[RECEIPT_DIGEST_FIELD], digest_without(receipt, RECEIPT_DIGEST_FIELD))

    def test_10_total_finding_count(self):
        self.assertEqual(run(fixture()).portfolio["total_finding_count"], 3)

    def test_11_changed_path_union_count(self):
        self.assertEqual(run(fixture()).portfolio["total_changed_path_count"], 4)

    def test_12_bundle_input_not_list_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"] = {}
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_13_bundle_count_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"].pop()
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_14_bundle_id_set_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["candidate_id"] = "other"
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_15_duplicate_bundle_id_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][1]["candidate_id"] = data["candidate_preflight_bundles"][0]["candidate_id"]
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_16_report_digest_tamper_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_report"][PREFLIGHT_REPORT_DIGEST_FIELD] = "0" * 64
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_17_receipt_digest_tamper_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_receipt"][PREFLIGHT_RECEIPT_DIGEST_FIELD] = "0" * 64
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_18_report_receipt_classification_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_receipt"]["codeai_disposition"] = DISPOSITION_HOLD
        data["candidate_preflight_bundles"][0]["preflight_receipt"] = seal(
            data["candidate_preflight_bundles"][0]["preflight_receipt"],
            PREFLIGHT_RECEIPT_DIGEST_FIELD,
        )
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_19_typed_ir_lineage_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_report"]["typed_edit_ir_digest"] = "f" * 64
        reseal_report_and_receipt(data, 0)
        data["portfolio_request"]["candidate_requests"][0]["expected_typed_edit_ir_digest"] = "1" * 64
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_20_source_commit_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_report"]["source_commit_sha"] = "8" * 40
        data["candidate_preflight_bundles"][0]["preflight_receipt"]["source_commit_sha"] = "8" * 40
        reseal_report_and_receipt(data, 0)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_21_source_snapshot_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_report"]["source_repository_snapshot_digest"] = "f" * 64
        data["candidate_preflight_bundles"][0]["preflight_receipt"]["source_repository_snapshot_digest"] = "f" * 64
        reseal_report_and_receipt(data, 0)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_22_classification_flags_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][1]["preflight_report"]["admissible"] = True
        reseal_report_and_receipt(data, 1)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_23_finding_counts_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][1]["preflight_report"]["finding_counts"]["repairable"] = 0
        data["candidate_preflight_bundles"][1]["preflight_receipt"]["finding_counts"]["repairable"] = 0
        reseal_report_and_receipt(data, 1)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_24_candidate_budget_blocks(self):
        data = fixture()
        data["portfolio_policy"]["maximum_candidates"] = 3
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_25_finding_budget_blocks(self):
        data = fixture()
        data["portfolio_policy"]["maximum_total_findings"] = 2
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_26_changed_path_budget_blocks(self):
        data = fixture()
        data["portfolio_policy"]["maximum_total_changed_paths"] = 3
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_27_stale_request_blocks(self):
        data = fixture()
        data["portfolio_request"]["request_created_epoch"] = 1
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_28_unresolved_question_blocks(self):
        data = fixture()
        data["portfolio_request"]["unresolved_portfolio_questions"] = ["need authority"]
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_29_claimed_authority_blocks(self):
        data = fixture()
        data["portfolio_request"]["claims_authority"] = True
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_30_noncontiguous_sequence_blocks(self):
        data = fixture()
        data["portfolio_request"]["candidate_requests"][0]["candidate_sequence"] = 9
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)


def authority_test(field: str):
    def test(self):
        data = fixture()
        data["portfolio_policy"][field] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)
    return test


for number, field in enumerate(
    (
        "allow_ranking",
        "allow_candidate_selection",
        "allow_verification_runner_invocation",
        "allow_repair_execution",
        "allow_execution_authority",
        "allow_git_authority",
    ),
    31,
):
    setattr(
        EvidenceBearingCandidatePortfolioTests,
        f"test_{number:02d}_{field}_blocks",
        authority_test(field),
    )


if __name__ == "__main__":
    unittest.main()
