from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    PORTFOLIO_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as PORTFOLIO_RECEIPT_DIGEST_FIELD,
    seal as portfolio_seal,
)
from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD as BASELINE_EVIDENCE_DIGEST_FIELD,
    METRICS_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as BASELINE_RECEIPT_DIGEST_FIELD,
    seal as baseline_seal,
)
from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    seal,
)
from runtime.kuuos_codeai_typed_error_classification_v0_1 import (
    build_codeai_typed_error_classification,
)
from scripts.build_codeai_typed_error_classification_fixture_v0_1 import build_fixture

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    classification_spec = json.loads(
        (ROOT / "examples/codeai_typed_error_classification_v0_1.json").read_text(encoding="utf-8")
    )
    portfolio_spec = json.loads(
        (ROOT / "examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json").read_text(encoding="utf-8")
    )
    baseline_spec = json.loads(
        (ROOT / "examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    return build_fixture(classification_spec, portfolio_spec, baseline_spec)


def run(data: dict):
    return build_codeai_typed_error_classification(
        source_portfolio=data["source_portfolio"],
        source_portfolio_receipt=data["source_portfolio_receipt"],
        baseline_evidence=data["baseline_evidence"],
        baseline_receipt=data["baseline_receipt"],
        classification_request=data["classification_request"],
        classification_policy=data["classification_policy"],
    )


def reseal_request(data: dict) -> None:
    data["classification_request"] = seal(data["classification_request"], REQUEST_DIGEST_FIELD)


def reseal_policy(data: dict) -> None:
    data["classification_policy"] = seal(data["classification_policy"], POLICY_DIGEST_FIELD)


def reseal_portfolio_lineage(data: dict) -> None:
    portfolio = portfolio_seal(data["source_portfolio"], PORTFOLIO_DIGEST_FIELD)
    receipt = dict(data["source_portfolio_receipt"])
    receipt["evidence_bearing_candidate_portfolio_digest"] = portfolio[PORTFOLIO_DIGEST_FIELD]
    receipt = portfolio_seal(receipt, PORTFOLIO_RECEIPT_DIGEST_FIELD)
    data["source_portfolio"] = portfolio
    data["source_portfolio_receipt"] = receipt
    data["classification_request"]["source_portfolio_digest"] = portfolio[PORTFOLIO_DIGEST_FIELD]
    data["classification_request"]["source_portfolio_receipt_digest"] = receipt[
        PORTFOLIO_RECEIPT_DIGEST_FIELD
    ]
    data["classification_policy"]["expected_source_portfolio_digest"] = portfolio[
        PORTFOLIO_DIGEST_FIELD
    ]
    data["classification_policy"]["expected_source_portfolio_receipt_digest"] = receipt[
        PORTFOLIO_RECEIPT_DIGEST_FIELD
    ]
    reseal_request(data)
    reseal_policy(data)


def reseal_baseline_lineage(data: dict) -> None:
    evidence = dict(data["baseline_evidence"])
    metrics = baseline_seal(evidence["metrics"], METRICS_DIGEST_FIELD)
    evidence["metrics"] = metrics
    evidence["metrics_digest"] = metrics[METRICS_DIGEST_FIELD]
    evidence = baseline_seal(evidence, BASELINE_EVIDENCE_DIGEST_FIELD)
    receipt = dict(data["baseline_receipt"])
    receipt["metrics_digest"] = metrics[METRICS_DIGEST_FIELD]
    receipt["evidence_digest"] = evidence[BASELINE_EVIDENCE_DIGEST_FIELD]
    receipt = baseline_seal(receipt, BASELINE_RECEIPT_DIGEST_FIELD)
    data["baseline_evidence"] = evidence
    data["baseline_receipt"] = receipt
    data["classification_request"]["baseline_evidence_digest"] = evidence[BASELINE_EVIDENCE_DIGEST_FIELD]
    data["classification_request"]["baseline_receipt_digest"] = receipt[BASELINE_RECEIPT_DIGEST_FIELD]
    data["classification_policy"]["expected_baseline_evidence_digest"] = evidence[
        BASELINE_EVIDENCE_DIGEST_FIELD
    ]
    data["classification_policy"]["expected_baseline_receipt_digest"] = receipt[
        BASELINE_RECEIPT_DIGEST_FIELD
    ]
    reseal_request(data)
    reseal_policy(data)


class TypedErrorClassificationTests(unittest.TestCase):
    def test_ready(self):
        self.assertEqual(run(fixture()).status, STATUS_READY)

    def test_deterministic(self):
        data = fixture()
        self.assertEqual(run(data).classification, run(data).classification)

    def test_receipt_digest_valid(self):
        result = run(fixture())
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            seal(result.receipt, RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD],
        )

    def test_classification_digest_present(self):
        result = run(fixture())
        self.assertIn(CLASSIFICATION_DIGEST_FIELD, result.classification)

    def test_candidate_count(self):
        self.assertEqual(run(fixture()).classification["candidate_count"], 4)

    def test_typed_error_count(self):
        self.assertEqual(run(fixture()).classification["typed_error_count"], 3)

    def test_family_counts(self):
        counts = run(fixture()).classification["family_counts"]
        self.assertEqual(counts["syntax"], 1)
        self.assertEqual(counts["dependency"], 1)
        self.assertEqual(counts["operation_conflict"], 1)

    def test_repair_route_counts(self):
        counts = run(fixture()).classification["repair_route_counts"]
        self.assertEqual(counts["local_candidate_repair"], 1)
        self.assertEqual(counts["external_evidence_required"], 1)
        self.assertEqual(counts["current_ir_unmaterializable"], 1)

    def test_error_free_candidate_preserved(self):
        candidates = run(fixture()).classification["typed_candidates"]
        self.assertTrue(candidates[0]["no_static_error_observed"])
        self.assertEqual(candidates[0]["typed_errors"], [])

    def test_source_findings_preserved(self):
        result = run(fixture())
        self.assertTrue(all(item["source_finding_evidence_preserved"] for item in result.classification["typed_candidates"]))

    def test_no_downstream_effects(self):
        result = run(fixture()).classification
        for field in (
            "ranking_performed",
            "candidate_selected",
            "verification_runner_invoked",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "selection_authority_granted",
            "verification_authority_granted",
            "repair_authority_granted",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            self.assertFalse(result[field], field)

    def test_request_not_mapping_blocks(self):
        data = fixture()
        data["classification_request"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_policy_not_mapping_blocks(self):
        data = fixture()
        data["classification_policy"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_portfolio_not_mapping_blocks(self):
        data = fixture()
        data["source_portfolio"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_baseline_not_mapping_blocks(self):
        data = fixture()
        data["baseline_evidence"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_request_digest_tamper_blocks(self):
        data = fixture()
        data["classification_request"]["classification_id"] = "tampered"
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_policy_digest_tamper_blocks(self):
        data = fixture()
        data["classification_policy"]["maximum_typed_errors"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_portfolio_digest_tamper_blocks(self):
        data = fixture()
        data["source_portfolio"]["candidate_count"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_portfolio_receipt_digest_tamper_blocks(self):
        data = fixture()
        data["source_portfolio_receipt"]["candidate_count"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_baseline_digest_tamper_blocks(self):
        data = fixture()
        data["baseline_evidence"]["evaluated_case_count"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_baseline_receipt_digest_tamper_blocks(self):
        data = fixture()
        data["baseline_receipt"]["evaluated_case_count"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_request_claims_authority_blocks(self):
        data = fixture()
        data["classification_request"]["claims_authority"] = True
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_unresolved_question_blocks(self):
        data = fixture()
        data["classification_request"]["unresolved_classification_questions"] = ["unknown"]
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_stale_request_blocks(self):
        data = fixture()
        data["classification_request"]["request_created_epoch"] = 1
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_future_request_blocks(self):
        data = fixture()
        data["classification_request"]["request_created_epoch"] = data["classification_policy"]["evaluation_epoch"] + 1
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_candidate_budget_blocks(self):
        data = fixture()
        data["classification_policy"]["maximum_candidates"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_error_budget_blocks(self):
        data = fixture()
        data["classification_policy"]["maximum_typed_errors"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_ranking_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_ranking"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_selection_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_candidate_selection"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_verification_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_verification_runner_invocation"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_repair_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_repair_execution"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_repository_mutation_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_repository_mutation"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_execution_authority_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_execution_authority"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_git_authority_blocks(self):
        data = fixture()
        data["classification_policy"]["allow_git_authority"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_exact_lineage_must_be_required(self):
        data = fixture()
        data["classification_policy"]["require_exact_lineage"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_complete_taxonomy_must_be_required(self):
        data = fixture()
        data["classification_policy"]["require_complete_taxonomy"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_finding_preservation_must_be_required(self):
        data = fixture()
        data["classification_policy"]["require_finding_evidence_preservation"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_unknown_finding_code_blocks_fail_closed(self):
        data = fixture()
        finding = data["source_portfolio"]["candidates"][1]["findings"][0]
        finding["code"] = "new_unmapped_failure"
        reseal_portfolio_lineage(data)
        result = run(data)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("taxonomy_missing_codes" in issue for issue in result.issues))

    def test_known_baseline_fingerprint_is_reference_only(self):
        data = fixture()
        data["baseline_evidence"]["metrics"]["error_fingerprint_counts"]["PYTHON_PARSE_FAILED"] = 2
        reseal_baseline_lineage(data)
        result = run(data)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.classification["novelty_counts"]["known_in_replay_baseline"], 1)
        self.assertFalse(result.classification["historical_frequency_treated_as_probability"])

    def test_repository_mismatch_blocks(self):
        data = fixture()
        data["classification_request"]["repository_full_name"] = "other/repo"
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_source_commit_mismatch_blocks(self):
        data = fixture()
        data["classification_request"]["source_commit_sha"] = "0" * 40
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_portfolio_digest_correspondence_blocks(self):
        data = fixture()
        data["classification_request"]["source_portfolio_digest"] = "0" * 64
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_baseline_digest_correspondence_blocks(self):
        data = fixture()
        data["classification_request"]["baseline_evidence_digest"] = "0" * 64
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)


if __name__ == "__main__":
    unittest.main()
