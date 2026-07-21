from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_independent_verifier_ensemble_checks_v0_2 import seal
from runtime.kuuos_codeai_independent_verifier_ensemble_schema_v0_2 import (
    DISPOSITION_ACCEPTED,
    DISPOSITION_DISAGREEMENT,
    DISPOSITION_FAILED,
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
)
from runtime.kuuos_codeai_independent_verifier_ensemble_v0_2 import evaluate_independent_verifier_ensemble
from scripts.build_codeai_independent_verifier_ensemble_fixture_v0_2 import build_fixture


class IndependentVerifierEnsembleV02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = build_fixture()

    def evaluate(self, fixture=None):
        return evaluate_independent_verifier_ensemble(**(fixture or self.fixture))

    def reseal_evidence(self, fixture, index):
        fixture["evidence_packets"][index] = seal(fixture["evidence_packets"][index], EVIDENCE_DIGEST_FIELD)

    def test_reference_passes(self):
        result = self.evaluate()
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_ACCEPTED)
        self.assertEqual(result.ensemble["pass_count"], 4)

    def test_reference_has_four_families(self):
        result = self.evaluate()
        self.assertEqual(len(result.ensemble["covered_check_families"]), 4)

    def test_receipt_never_accepts_candidate(self):
        result = self.evaluate()
        self.assertFalse(result.receipt["candidate_accepted"])
        self.assertFalse(result.receipt["candidate_rejected"])

    def test_request_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["request_revision"] = "tampered"
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_policy_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["minimum_pass_quorum"] = 2
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_evidence_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["nonce"] = "tampered"
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_candidate_binding_mismatch_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["candidate_digest"] = "0" * 64
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_context_binding_mismatch_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["context_pack_digest"] = "1" * 64
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_source_commit_mismatch_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["source_commit_sha"] = "2" * 40
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_duplicate_verifier_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][1]["verifier_id"] = fixture["evidence_packets"][0]["verifier_id"]
        self.reseal_evidence(fixture, 1)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_duplicate_organization_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][1]["organization_id"] = fixture["evidence_packets"][0]["organization_id"]
        self.reseal_evidence(fixture, 1)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_duplicate_session_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][1]["verification_session_id"] = fixture["evidence_packets"][0]["verification_session_id"]
        self.reseal_evidence(fixture, 1)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_shared_method_below_minimum_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][1]["verification_method_digest"] = fixture["evidence_packets"][0]["verification_method_digest"]
        self.reseal_evidence(fixture, 1)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_missing_family_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][3]["check_family"] = "behavioral_and_regression"
        self.reseal_evidence(fixture, 3)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_producer_independence_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["independent_from_candidate_producer"] = False
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_peer_independence_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["independent_from_other_verifiers"] = False
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_prompt_independence_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["prompt_lineage_independent"] = False
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_memory_independence_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["repair_memory_independent"] = False
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_test_generation_independence_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["test_generation_independent"] = False
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_kernel_execution_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["kernel_executed_verification"] = True
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_repository_mutation_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["repository_mutation_performed"] = True
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_selection_authority_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["candidate_selection_performed"] = True
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_conflict_holds(self):
        fixture = deepcopy(self.fixture)
        packet = fixture["evidence_packets"][0]
        packet["declared_outcome"] = "failed"
        packet["passed_check_ids"] = [packet["check_ids"][0]]
        packet["failed_check_ids"] = [packet["check_ids"][1]]
        packet["acceptance_criteria_satisfied"] = False
        packet["highest_severity"] = "high"
        self.reseal_evidence(fixture, 0)
        result = self.evaluate(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_DISAGREEMENT)

    def test_critical_failure_overrides_pass_quorum(self):
        fixture = deepcopy(self.fixture)
        packet = fixture["evidence_packets"][0]
        packet["declared_outcome"] = "failed"
        packet["passed_check_ids"] = [packet["check_ids"][0]]
        packet["failed_check_ids"] = [packet["check_ids"][1]]
        packet["acceptance_criteria_satisfied"] = False
        packet["highest_severity"] = "critical"
        self.reseal_evidence(fixture, 0)
        result = self.evaluate(fixture)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)

    def test_stale_evidence_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["evidence_packets"][0]["verification_completed_epoch"] = 100
        fixture["evidence_packets"][0]["verification_started_epoch"] = 99
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)

    def test_skipped_check_over_limit_blocks(self):
        fixture = deepcopy(self.fixture)
        packet = fixture["evidence_packets"][0]
        packet["declared_outcome"] = "inconclusive"
        packet["passed_check_ids"] = [packet["check_ids"][0]]
        packet["failed_check_ids"] = []
        packet["skipped_check_ids"] = [packet["check_ids"][1]]
        self.reseal_evidence(fixture, 0)
        self.assertEqual(self.evaluate(fixture).status, STATUS_BLOCKED)


if __name__ == "__main__":
    unittest.main()
