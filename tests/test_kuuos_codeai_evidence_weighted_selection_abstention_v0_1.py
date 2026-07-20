from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    PLAN_DIGEST_FIELD as STRENGTHENING_PLAN_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as STRENGTHENING_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_ABSTAINED,
    DECISION_SELECTED,
    EVIDENCE_PACKET_DIGEST_FIELD,
    EVIDENCE_RECORD_DIGEST_FIELD,
    OUTCOME_FAILED,
    POLICY_DIGEST_FIELD,
    REASON_BELOW_THRESHOLD,
    REASON_INSUFFICIENT_MARGIN,
    REASON_NO_ELIGIBLE,
    REASON_TIED_TOP,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    seal,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_v0_1 import (
    build_codeai_evidence_weighted_selection_abstention,
)
from scripts.build_codeai_evidence_weighted_selection_abstention_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    def load(path: str) -> dict:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    return build_fixture(
        load("examples/codeai_evidence_weighted_selection_abstention_v0_1.json"),
        load("examples/codeai_independent_test_strengthening_v0_1.json"),
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load("examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"),
    )


def run(data: dict):
    return build_codeai_evidence_weighted_selection_abstention(
        strengthening_plan=data["strengthening_plan"],
        strengthening_receipt=data["strengthening_receipt"],
        evidence_packet=data["evidence_packet"],
        selection_request=data["selection_request"],
        selection_policy=data["selection_policy"],
    )


def reseal_request(data: dict) -> None:
    data["selection_request"] = seal(data["selection_request"], REQUEST_DIGEST_FIELD)


def reseal_policy(data: dict) -> None:
    data["selection_policy"] = seal(data["selection_policy"], POLICY_DIGEST_FIELD)


def reseal_evidence(data: dict) -> None:
    packet = seal(data["evidence_packet"], EVIDENCE_PACKET_DIGEST_FIELD)
    data["evidence_packet"] = packet
    data["selection_request"]["evidence_packet_digest"] = packet[
        EVIDENCE_PACKET_DIGEST_FIELD
    ]
    data["selection_policy"]["expected_evidence_packet_digest"] = packet[
        EVIDENCE_PACKET_DIGEST_FIELD
    ]
    reseal_request(data)
    reseal_policy(data)


def reseal_record(data: dict, candidate_index: int = 0, record_index: int = 0) -> None:
    record = data["evidence_packet"]["candidate_results"][candidate_index][
        "obligation_results"
    ][record_index]
    data["evidence_packet"]["candidate_results"][candidate_index][
        "obligation_results"
    ][record_index] = seal(record, EVIDENCE_RECORD_DIGEST_FIELD)
    reseal_evidence(data)


def reseal_source_lineage(data: dict) -> None:
    plan = seal(data["strengthening_plan"], STRENGTHENING_PLAN_DIGEST_FIELD)
    receipt = dict(data["strengthening_receipt"])
    receipt["independent_test_strengthening_plan_digest"] = plan[
        STRENGTHENING_PLAN_DIGEST_FIELD
    ]
    receipt = seal(receipt, STRENGTHENING_RECEIPT_DIGEST_FIELD)
    packet = dict(data["evidence_packet"])
    packet["strengthening_plan_digest"] = plan[STRENGTHENING_PLAN_DIGEST_FIELD]
    packet["strengthening_receipt_digest"] = receipt[
        STRENGTHENING_RECEIPT_DIGEST_FIELD
    ]
    packet = seal(packet, EVIDENCE_PACKET_DIGEST_FIELD)
    data["strengthening_plan"] = plan
    data["strengthening_receipt"] = receipt
    data["evidence_packet"] = packet
    data["selection_request"]["strengthening_plan_digest"] = plan[
        STRENGTHENING_PLAN_DIGEST_FIELD
    ]
    data["selection_request"]["strengthening_receipt_digest"] = receipt[
        STRENGTHENING_RECEIPT_DIGEST_FIELD
    ]
    data["selection_request"]["evidence_packet_digest"] = packet[
        EVIDENCE_PACKET_DIGEST_FIELD
    ]
    data["selection_policy"]["expected_strengthening_plan_digest"] = plan[
        STRENGTHENING_PLAN_DIGEST_FIELD
    ]
    data["selection_policy"]["expected_strengthening_receipt_digest"] = receipt[
        STRENGTHENING_RECEIPT_DIGEST_FIELD
    ]
    data["selection_policy"]["expected_evidence_packet_digest"] = packet[
        EVIDENCE_PACKET_DIGEST_FIELD
    ]
    reseal_request(data)
    reseal_policy(data)


class EvidenceWeightedSelectionAbstentionTests(unittest.TestCase):
    def test_reference_selection(self):
        result = run(fixture())
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.decision["decision"], DECISION_SELECTED)
        self.assertEqual(result.decision["selected_candidate_id"], "candidate-admissible")
        self.assertEqual(result.decision["selected_evidence_score"], 60)
        self.assertEqual(result.decision["candidate_count"], 4)
        self.assertEqual(result.decision["evidence_record_count"], 22)
        self.assertEqual(result.decision["eligible_candidate_count"], 1)

    def test_deterministic_and_receipt_sealed(self):
        data = fixture()
        left = run(data)
        right = run(data)
        self.assertEqual(left.decision, right.decision)
        self.assertEqual(
            left.receipt[RECEIPT_DIGEST_FIELD],
            seal(left.receipt, RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD],
        )

    def test_high_ineligible_score_cannot_override_admissibility(self):
        scorecards = run(fixture()).decision["candidate_scorecards"]
        selected = next(item for item in scorecards if item["candidate_selected"])
        repairable = next(
            item for item in scorecards if item["candidate_id"] == "candidate-repairable"
        )
        self.assertGreater(repairable["evidence_score"], selected["evidence_score"])
        self.assertFalse(repairable["eligible"])
        self.assertEqual(scorecards[0]["candidate_id"], "candidate-admissible")

    def test_selection_is_bounded_and_has_no_downstream_effect(self):
        decision = run(fixture()).decision
        self.assertTrue(decision["selection_authority_exercised"])
        self.assertTrue(decision["selection_authority_bounded_to_decision"])
        for field in (
            "test_execution_performed_by_kernel",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "verification_authority_granted",
            "repair_authority_granted",
            "execution_authority_granted",
            "git_authority_granted",
            "score_treated_as_probability",
            "score_treated_as_correctness_proof",
            "selection_treated_as_correctness_proof",
            "abstention_treated_as_rejection",
        ):
            self.assertFalse(decision[field], field)

    def test_no_eligible_candidate_abstains(self):
        data = fixture()
        data["evidence_packet"]["candidate_results"][0]["obligation_results"][0][
            "outcome"
        ] = OUTCOME_FAILED
        reseal_record(data)
        result = run(data)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.decision["decision"], DECISION_ABSTAINED)
        self.assertEqual(result.decision["decision_reason"], REASON_NO_ELIGIBLE)

    def test_below_threshold_abstains(self):
        data = fixture()
        data["selection_policy"]["minimum_evidence_score"] = 100
        reseal_policy(data)
        result = run(data)
        self.assertEqual(result.decision["decision"], DECISION_ABSTAINED)
        self.assertEqual(result.decision["decision_reason"], REASON_BELOW_THRESHOLD)

    def test_tied_top_abstains(self):
        data = fixture()
        data["strengthening_plan"]["candidate_plans"][1][
            "source_classification"
        ] = DISPOSITION_ADMISSIBLE
        reseal_source_lineage(data)
        data["selection_policy"]["category_weights"] = {
            "baseline": 10,
            "error_specific": 10,
            "novelty": 10,
            "route": 10,
            "error_free": 30,
        }
        reseal_policy(data)
        result = run(data)
        self.assertEqual(result.decision["decision"], DECISION_ABSTAINED)
        self.assertEqual(result.decision["decision_reason"], REASON_TIED_TOP)

    def test_insufficient_margin_abstains(self):
        data = fixture()
        data["strengthening_plan"]["candidate_plans"][1][
            "source_classification"
        ] = DISPOSITION_ADMISSIBLE
        reseal_source_lineage(data)
        data["selection_policy"]["category_weights"] = {
            "baseline": 1,
            "error_specific": 1,
            "novelty": 1,
            "route": 1,
            "error_free": 1,
        }
        data["selection_policy"]["minimum_evidence_score"] = 1
        data["selection_policy"]["minimum_score_margin"] = 3
        reseal_policy(data)
        result = run(data)
        self.assertEqual(result.decision["decision"], DECISION_ABSTAINED)
        self.assertEqual(result.decision["decision_reason"], REASON_INSUFFICIENT_MARGIN)

    def test_stale_and_future_windows_block(self):
        cases = (
            ("selection_request", "request_created_epoch"),
            ("evidence_packet", "evidence_created_epoch"),
        )
        for container, field in cases:
            with self.subTest(container=container, mode="stale"):
                data = fixture()
                data[container][field] = 1
                reseal_request(data) if container == "selection_request" else reseal_evidence(data)
                self.assertEqual(run(data).status, STATUS_BLOCKED)
            with self.subTest(container=container, mode="future"):
                data = fixture()
                data[container][field] = data["selection_policy"]["evaluation_epoch"] + 1
                reseal_request(data) if container == "selection_request" else reseal_evidence(data)
                self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_missing_obligation_and_reordered_candidates_block(self):
        data = fixture()
        records = data["evidence_packet"]["candidate_results"][0]["obligation_results"]
        records.pop()
        data["evidence_packet"]["candidate_results"][0]["obligation_result_count"] = len(records)
        data["evidence_packet"]["evidence_record_count"] -= 1
        reseal_evidence(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

        data = fixture()
        data["evidence_packet"]["candidate_results"][0], data["evidence_packet"][
            "candidate_results"
        ][1] = (
            data["evidence_packet"]["candidate_results"][1],
            data["evidence_packet"]["candidate_results"][0],
        )
        reseal_evidence(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_budgets_and_weights_block(self):
        data = fixture()
        data["selection_policy"]["maximum_candidates"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

        data = fixture()
        data["selection_policy"]["maximum_evidence_records"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

        data = fixture()
        data["selection_policy"]["category_weights"].pop("route")
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

        data = fixture()
        data["selection_policy"]["category_weights"]["baseline"] = 0
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_resealed_source_selection_effect_blocks(self):
        data = fixture()
        data["strengthening_plan"]["candidate_selected"] = True
        reseal_source_lineage(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)


def _install_dynamic_tests() -> None:
    mapping_inputs = (
        "strengthening_plan",
        "strengthening_receipt",
        "evidence_packet",
        "selection_request",
        "selection_policy",
    )
    for field in mapping_inputs:
        def test(self, field=field):
            data = fixture()
            data[field] = []
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_non_mapping_{field}_blocks", test)

    digest_cases = (
        ("selection_request", "selection_id", "tampered"),
        ("selection_policy", "minimum_evidence_score", 999),
        ("strengthening_plan", "candidate_count", 999),
        ("strengthening_receipt", "candidate_count", 999),
        ("evidence_packet", "candidate_count", 999),
    )
    for container, field, value in digest_cases:
        def test(self, container=container, field=field, value=value):
            data = fixture()
            data[container][field] = value
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(
            EvidenceWeightedSelectionAbstentionTests,
            f"test_tampered_{container}_{field}_blocks",
            test,
        )

    required_policy = (
        "require_exact_lineage",
        "require_complete_obligation_coverage",
        "require_independent_runner",
        "require_independent_reviewer",
        "require_isolated_execution",
        "require_source_correspondence",
        "require_admissible_source_classification",
        "require_all_obligations_passed",
        "allow_selection_decision",
    )
    for field in required_policy:
        def test(self, field=field):
            data = fixture()
            data["selection_policy"][field] = False
            reseal_policy(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_required_{field}_blocks", test)

    forbidden_policy = (
        "allow_test_execution",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    for field in forbidden_policy:
        def test(self, field=field):
            data = fixture()
            data["selection_policy"][field] = True
            reseal_policy(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_forbidden_{field}_blocks", test)

    packet_required_true = (
        "external_test_execution_reported",
        "independent_runner_verified",
        "independent_reviewer_verified",
        "isolated_execution_verified",
        "source_correspondence_verified",
    )
    for field in packet_required_true:
        def test(self, field=field):
            data = fixture()
            data["evidence_packet"][field] = False
            reseal_evidence(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_packet_{field}_false_blocks", test)

    packet_required_false = (
        "candidate_producer_involved_in_evidence",
        "repository_mutation_performed",
        "git_effect_performed",
    )
    for field in packet_required_false:
        def test(self, field=field):
            data = fixture()
            data["evidence_packet"][field] = True
            reseal_evidence(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_packet_{field}_true_blocks", test)

    record_required_true = (
        "completed",
        "external_execution",
        "independent_runner",
        "independent_reviewer",
        "isolated_execution",
        "source_correspondence",
    )
    for field in record_required_true:
        def test(self, field=field):
            data = fixture()
            data["evidence_packet"]["candidate_results"][0]["obligation_results"][0][field] = False
            reseal_record(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_record_{field}_false_blocks", test)

    record_required_false = (
        "candidate_producer_involved",
        "repository_mutation_performed",
        "git_effect_performed",
    )
    for field in record_required_false:
        def test(self, field=field):
            data = fixture()
            data["evidence_packet"]["candidate_results"][0]["obligation_results"][0][field] = True
            reseal_record(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_record_{field}_true_blocks", test)

    roles = (
        ("independent_runner_id", "candidate_producer_id"),
        ("independent_reviewer_id", "candidate_producer_id"),
        ("independent_reviewer_id", "independent_runner_id"),
    )
    for target, source in roles:
        def test(self, target=target, source=source):
            data = fixture()
            data["evidence_packet"][target] = data["evidence_packet"][source]
            reseal_evidence(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_role_collision_{target}_{source}_blocks", test)

    claims = ("claims_execution_authority", "claims_git_authority")
    for field in claims:
        def test(self, field=field):
            data = fixture()
            data["selection_request"][field] = True
            reseal_request(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(EvidenceWeightedSelectionAbstentionTests, f"test_request_{field}_blocks", test)


_install_dynamic_tests()


if __name__ == "__main__":
    unittest.main()
