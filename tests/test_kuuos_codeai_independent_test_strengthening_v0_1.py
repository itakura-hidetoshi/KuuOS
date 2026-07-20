from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CLASSIFICATION_RECEIPT_DIGEST_FIELD,
    seal as source_seal,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    CAPABILITY_CATALOG_DIGEST_FIELD,
    PLAN_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    CHECK_ERROR_FREE_MUTATION_PROBE,
    CHECK_EXTERNAL_EVIDENCE_BINDING,
    CHECK_LOCAL_REPAIR_REGRESSION,
    CHECK_NOVELTY_FALSIFICATION,
    CHECK_PARSE_NEGATIVE_CONTROL,
    CHECK_UNMATERIALIZABILITY_REPRODUCTION,
    seal,
)
from runtime.kuuos_codeai_independent_test_strengthening_v0_1 import (
    build_codeai_independent_test_strengthening,
)
from scripts.build_codeai_independent_test_strengthening_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    def load(path: str) -> dict:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    return build_fixture(
        load("examples/codeai_independent_test_strengthening_v0_1.json"),
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load("examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"),
    )


def run(data: dict):
    return build_codeai_independent_test_strengthening(**data)


def reseal_request(data: dict) -> None:
    data["strengthening_request"] = seal(data["strengthening_request"], REQUEST_DIGEST_FIELD)


def reseal_policy(data: dict) -> None:
    data["strengthening_policy"] = seal(data["strengthening_policy"], POLICY_DIGEST_FIELD)


def reseal_catalog(data: dict) -> None:
    data["capability_catalog"] = seal(
        data["capability_catalog"],
        CAPABILITY_CATALOG_DIGEST_FIELD,
    )
    digest = data["capability_catalog"][CAPABILITY_CATALOG_DIGEST_FIELD]
    data["strengthening_request"]["capability_catalog_digest"] = digest
    data["strengthening_policy"]["expected_capability_catalog_digest"] = digest
    reseal_request(data)
    reseal_policy(data)


def reseal_source(data: dict) -> None:
    classification = source_seal(data["source_classification"], CLASSIFICATION_DIGEST_FIELD)
    receipt = dict(data["source_classification_receipt"])
    receipt["typed_error_classification_digest"] = classification[CLASSIFICATION_DIGEST_FIELD]
    receipt = source_seal(receipt, CLASSIFICATION_RECEIPT_DIGEST_FIELD)
    data["source_classification"] = classification
    data["source_classification_receipt"] = receipt
    data["strengthening_request"]["source_classification_digest"] = classification[
        CLASSIFICATION_DIGEST_FIELD
    ]
    data["strengthening_request"]["source_classification_receipt_digest"] = receipt[
        CLASSIFICATION_RECEIPT_DIGEST_FIELD
    ]
    data["strengthening_policy"]["expected_source_classification_digest"] = classification[
        CLASSIFICATION_DIGEST_FIELD
    ]
    data["strengthening_policy"]["expected_source_classification_receipt_digest"] = receipt[
        CLASSIFICATION_RECEIPT_DIGEST_FIELD
    ]
    reseal_request(data)
    reseal_policy(data)


class IndependentTestStrengtheningTests(unittest.TestCase):
    def test_ready(self):
        self.assertEqual(run(fixture()).status, STATUS_READY)

    def test_deterministic(self):
        data = fixture()
        self.assertEqual(run(data).plan, run(data).plan)

    def test_plan_digest_present(self):
        self.assertIn(PLAN_DIGEST_FIELD, run(fixture()).plan)

    def test_receipt_digest_valid(self):
        result = run(fixture())
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            seal(result.receipt, RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD],
        )

    def test_expected_counts(self):
        plan = run(fixture()).plan
        self.assertEqual(plan["candidate_count"], 4)
        self.assertEqual(plan["typed_error_count"], 3)
        self.assertEqual(plan["obligation_count"], 22)

    def test_all_candidates_preserved(self):
        plan = run(fixture()).plan
        self.assertEqual(plan["candidate_ids"], [item["candidate_id"] for item in plan["candidate_plans"]])

    def test_baseline_three_per_candidate(self):
        plan = run(fixture()).plan
        self.assertEqual(plan["category_counts"]["baseline"], 12)

    def test_error_free_candidate_gets_mutation_probe(self):
        plan = run(fixture()).plan
        kinds = {item["check_kind"] for item in plan["candidate_plans"][0]["obligations"]}
        self.assertIn(CHECK_ERROR_FREE_MUTATION_PROBE, kinds)

    def test_syntax_candidate_gets_parse_control(self):
        plan = run(fixture()).plan
        kinds = {item["check_kind"] for item in plan["candidate_plans"][1]["obligations"]}
        self.assertIn(CHECK_PARSE_NEGATIVE_CONTROL, kinds)

    def test_all_novel_errors_get_falsification(self):
        plan = run(fixture()).plan
        self.assertEqual(plan["check_kind_counts"][CHECK_NOVELTY_FALSIFICATION], 3)

    def test_routes_remain_distinct(self):
        plan = run(fixture()).plan
        counts = plan["check_kind_counts"]
        self.assertEqual(counts[CHECK_LOCAL_REPAIR_REGRESSION], 1)
        self.assertEqual(counts[CHECK_EXTERNAL_EVIDENCE_BINDING], 1)
        self.assertEqual(counts[CHECK_UNMATERIALIZABILITY_REPRODUCTION], 1)

    def test_no_downstream_effects(self):
        plan = run(fixture()).plan
        for field in (
            "test_generation_performed",
            "test_execution_performed",
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
            self.assertFalse(plan[field], field)

    def test_request_not_mapping_blocks(self):
        data = fixture()
        data["strengthening_request"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_policy_not_mapping_blocks(self):
        data = fixture()
        data["strengthening_policy"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_catalog_not_mapping_blocks(self):
        data = fixture()
        data["capability_catalog"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_classification_not_mapping_blocks(self):
        data = fixture()
        data["source_classification"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_receipt_not_mapping_blocks(self):
        data = fixture()
        data["source_classification_receipt"] = []
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_request_digest_tamper_blocks(self):
        data = fixture()
        data["strengthening_request"]["strengthening_id"] = "tampered"
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_policy_digest_tamper_blocks(self):
        data = fixture()
        data["strengthening_policy"]["maximum_obligations"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_catalog_digest_tamper_blocks(self):
        data = fixture()
        data["capability_catalog"]["catalog_id"] = "tampered"
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_classification_digest_tamper_blocks(self):
        data = fixture()
        data["source_classification"]["candidate_count"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_receipt_digest_tamper_blocks(self):
        data = fixture()
        data["source_classification_receipt"]["candidate_count"] += 1
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_request_claims_authority_blocks(self):
        data = fixture()
        data["strengthening_request"]["claims_authority"] = True
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_unresolved_question_blocks(self):
        data = fixture()
        data["strengthening_request"]["unresolved_strengthening_questions"] = ["unknown"]
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_stale_request_blocks(self):
        data = fixture()
        data["strengthening_request"]["request_created_epoch"] = 1
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_future_request_blocks(self):
        data = fixture()
        data["strengthening_request"]["request_created_epoch"] = (
            data["strengthening_policy"]["evaluation_epoch"] + 1
        )
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_candidate_budget_blocks(self):
        data = fixture()
        data["strengthening_policy"]["maximum_candidates"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_obligation_budget_blocks(self):
        data = fixture()
        data["strengthening_policy"]["maximum_obligations"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_test_generation_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_test_generation"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_test_execution_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_test_execution"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_selection_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_candidate_selection"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_verification_authority_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_verification_authority"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_repair_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_repair_execution"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_repository_mutation_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_repository_mutation"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_execution_authority_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_execution_authority"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_allow_git_authority_blocks(self):
        data = fixture()
        data["strengthening_policy"]["allow_git_authority"] = True
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_exact_lineage_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_exact_lineage"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_baseline_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_baseline_obligations"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_independence_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_independent_runner"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_isolation_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_isolated_execution"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_falsification_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_falsification_for_novel_errors"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_mutation_probe_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_error_free_mutation_probe"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_required_route_obligations_cannot_be_disabled(self):
        data = fixture()
        data["strengthening_policy"]["require_route_specific_obligations"] = False
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_missing_capability_blocks(self):
        data = fixture()
        removed = data["capability_catalog"]["check_capabilities"].pop()
        data["capability_catalog"]["supported_check_kinds"].remove(removed["check_kind"])
        data["capability_catalog"]["capability_count"] -= 1
        reseal_catalog(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_non_independent_runner_blocks(self):
        data = fixture()
        data["capability_catalog"]["check_capabilities"][0]["independent_runner"] = False
        reseal_catalog(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_non_isolated_runner_blocks(self):
        data = fixture()
        data["capability_catalog"]["check_capabilities"][0]["isolated_execution"] = False
        reseal_catalog(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_missing_falsification_capability_blocks(self):
        data = fixture()
        for item in data["capability_catalog"]["check_capabilities"]:
            if item["check_kind"] == CHECK_NOVELTY_FALSIFICATION:
                item["falsification_capable"] = False
        reseal_catalog(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_missing_mutation_capability_blocks(self):
        data = fixture()
        for item in data["capability_catalog"]["check_capabilities"]:
            if item["check_kind"] == CHECK_ERROR_FREE_MUTATION_PROBE:
                item["mutation_capable"] = False
        reseal_catalog(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_repository_mismatch_blocks(self):
        data = fixture()
        data["strengthening_request"]["repository_full_name"] = "other/repo"
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_source_commit_mismatch_blocks(self):
        data = fixture()
        data["strengthening_request"]["source_commit_sha"] = "0" * 40
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_classification_correspondence_mismatch_blocks(self):
        data = fixture()
        data["strengthening_request"]["source_classification_digest"] = "0" * 64
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_catalog_correspondence_mismatch_blocks(self):
        data = fixture()
        data["strengthening_request"]["capability_catalog_digest"] = "0" * 64
        reseal_request(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_source_effect_claim_blocks(self):
        data = fixture()
        data["source_classification"]["candidate_selected"] = True
        reseal_source(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)


if __name__ == "__main__":
    unittest.main()
