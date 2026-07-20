from __future__ import annotations

import json
import unittest
from pathlib import Path

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1 import *
from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    POLICY_DIGEST_FIELD,
    PORTFOLIO_DIGEST_FIELD,
    PREFLIGHT_RECEIPT_DIGEST_FIELD,
    PREFLIGHT_REPORT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
)
from scripts.build_codeai_evidence_bearing_candidate_portfolio_fixture_v0_1 import build_fixture

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"


def fixture() -> dict:
    return build_fixture(json.loads(EXAMPLE.read_text(encoding="utf-8")))


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


def reseal_evidence(data: dict, index: int) -> None:
    bundle = data["candidate_preflight_bundles"][index]
    report = seal(bundle["preflight_report"], PREFLIGHT_REPORT_DIGEST_FIELD)
    receipt = bundle["preflight_receipt"]
    receipt["static_admissibility_report_digest"] = report[PREFLIGHT_REPORT_DIGEST_FIELD]
    receipt = seal(receipt, PREFLIGHT_RECEIPT_DIGEST_FIELD)
    bundle["preflight_report"] = report
    bundle["preflight_receipt"] = receipt
    request_item = next(
        item for item in data["portfolio_request"]["candidate_requests"]
        if item["candidate_id"] == bundle["candidate_id"]
    )
    request_item["expected_typed_edit_ir_digest"] = report["typed_edit_ir_digest"]
    request_item["expected_static_admissibility_report_digest"] = report[PREFLIGHT_REPORT_DIGEST_FIELD]
    request_item["expected_preflight_receipt_digest"] = receipt[PREFLIGHT_RECEIPT_DIGEST_FIELD]
    reseal_request(data)


class EvidenceBearingCandidatePortfolioTests(unittest.TestCase):
    def test_01_example_ready(self):
        self.assertEqual(run(fixture()).status, STATUS_READY)

    def test_02_four_classifications_preserved(self):
        self.assertEqual(
            run(fixture()).portfolio["classification_counts"],
            {"admissible": 1, "repairable": 1, "hold": 1, "rejected": 1},
        )

    def test_03_request_sequence_preserved(self):
        self.assertEqual(
            run(fixture()).portfolio["candidate_ids"],
            ["candidate-admissible", "candidate-repairable", "candidate-hold", "candidate-rejected"],
        )

    def test_04_findings_preserved(self):
        data = fixture()
        portfolio = run(data).portfolio
        for bundle, candidate in zip(data["candidate_preflight_bundles"], portfolio["candidates"]):
            self.assertEqual(bundle["preflight_report"]["findings"], candidate["findings"])

    def test_05_preflight_receipts_preserved(self):
        self.assertTrue(all(c["preflight_route_receipt_preserved"] for c in run(fixture()).portfolio["candidates"]))

    def test_06_no_authority_or_effect(self):
        portfolio = run(fixture()).portfolio
        for field in (
            "ranking_performed", "candidate_selected", "verification_runner_invoked",
            "repair_executed", "repository_mutation_performed", "git_effect_performed",
            "execution_authority_granted", "git_authority_granted",
        ):
            self.assertFalse(portfolio[field])

    def test_07_content_addressed_outputs(self):
        result = run(fixture())
        self.assertEqual(result.portfolio[PORTFOLIO_DIGEST_FIELD], digest_without(result.portfolio, PORTFOLIO_DIGEST_FIELD))
        self.assertEqual(result.receipt[RECEIPT_DIGEST_FIELD], digest_without(result.receipt, RECEIPT_DIGEST_FIELD))

    def test_08_total_findings(self):
        self.assertEqual(run(fixture()).portfolio["total_finding_count"], 3)

    def test_09_changed_path_union(self):
        self.assertEqual(run(fixture()).portfolio["total_changed_path_count"], 1)

    def test_10_bundle_input_must_be_list(self):
        data = fixture(); data["candidate_preflight_bundles"] = {}
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_11_bundle_count_mismatch_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"].pop()
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_12_bundle_id_set_mismatch_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][0]["candidate_id"] = "other"
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_13_duplicate_bundle_id_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][1]["candidate_id"] = data["candidate_preflight_bundles"][0]["candidate_id"]
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_14_report_digest_tamper_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][0]["preflight_report"][PREFLIGHT_REPORT_DIGEST_FIELD] = "0" * 64
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_15_receipt_digest_tamper_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][0]["preflight_receipt"][PREFLIGHT_RECEIPT_DIGEST_FIELD] = "0" * 64
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_16_report_receipt_classification_mismatch_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][0]["preflight_receipt"]["codeai_disposition"] = DISPOSITION_HOLD
        data["candidate_preflight_bundles"][0]["preflight_receipt"] = seal(data["candidate_preflight_bundles"][0]["preflight_receipt"], PREFLIGHT_RECEIPT_DIGEST_FIELD)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_17_typed_ir_lineage_mismatch_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][0]["preflight_report"]["typed_edit_ir_digest"] = "f" * 64
        reseal_evidence(data, 0)
        data["portfolio_request"]["candidate_requests"][0]["expected_typed_edit_ir_digest"] = "1" * 64
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_18_source_commit_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_report"]["source_commit_sha"] = "8" * 40
        data["candidate_preflight_bundles"][0]["preflight_receipt"]["source_commit_sha"] = "8" * 40
        reseal_evidence(data, 0)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_19_source_snapshot_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][0]["preflight_report"]["source_repository_snapshot_digest"] = "f" * 64
        data["candidate_preflight_bundles"][0]["preflight_receipt"]["source_repository_snapshot_digest"] = "f" * 64
        reseal_evidence(data, 0)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_20_classification_flags_mismatch_blocks(self):
        data = fixture(); data["candidate_preflight_bundles"][1]["preflight_report"]["admissible"] = True
        reseal_evidence(data, 1)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_21_finding_counts_mismatch_blocks(self):
        data = fixture()
        data["candidate_preflight_bundles"][1]["preflight_report"]["finding_counts"]["repairable"] = 0
        data["candidate_preflight_bundles"][1]["preflight_receipt"]["finding_counts"]["repairable"] = 0
        reseal_evidence(data, 1)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_22_candidate_budget_blocks(self):
        data = fixture(); data["portfolio_policy"]["maximum_candidates"] = 3; reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_23_finding_budget_blocks(self):
        data = fixture(); data["portfolio_policy"]["maximum_total_findings"] = 2; reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_24_changed_path_budget_blocks(self):
        data = fixture(); data["portfolio_policy"]["maximum_total_changed_paths"] = 0; reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_25_stale_request_blocks(self):
        data = fixture(); data["portfolio_request"]["request_created_epoch"] = 1; reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_26_unresolved_question_blocks(self):
        data = fixture(); data["portfolio_request"]["unresolved_portfolio_questions"] = ["need authority"]; reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_27_claimed_authority_blocks(self):
        data = fixture(); data["portfolio_request"]["claims_authority"] = True; reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_28_noncontiguous_sequence_blocks(self):
        data = fixture(); data["portfolio_request"]["candidate_requests"][0]["candidate_sequence"] = 9; reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_35_request_digest_tamper_blocks(self):
        data = fixture(); data["portfolio_request"][REQUEST_DIGEST_FIELD] = "0" * 64
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_36_policy_digest_tamper_blocks(self):
        data = fixture(); data["portfolio_policy"][POLICY_DIGEST_FIELD] = "0" * 64
        self.assertEqual(run(data).status, STATUS_BLOCKED)


def authority_test(field: str):
    def test(self):
        data = fixture(); data["portfolio_policy"][field] = True; reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)
    return test


for number, field in enumerate((
    "allow_ranking", "allow_candidate_selection", "allow_verification_runner_invocation",
    "allow_repair_execution", "allow_execution_authority", "allow_git_authority",
), 29):
    setattr(EvidenceBearingCandidatePortfolioTests, f"test_{number:02d}_{field}_blocks", authority_test(field))


if __name__ == "__main__":
    unittest.main()
