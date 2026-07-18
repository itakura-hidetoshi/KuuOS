from copy import deepcopy
import unittest

import runtime.kuuos_codeai_independent_verification_envelope_v0_1 as m
from scripts.check_codeai_independent_verification_envelope_v0_1 import (
    failed_evidence,
    inconclusive_evidence,
    load_example,
    main as run_route_checker,
    reseal_evidence,
)


class CodeAIIndependentVerificationEnvelopeV01Test(unittest.TestCase):
    def setUp(self):
        self.example = load_example()

    def build(self, **overrides):
        values = {
            "source_candidate_receipt": self.example["source_candidate_receipt"],
            "verification_evidence": self.example["verification_evidence"],
            "verification_policy": self.example["verification_policy"],
        }
        values.update(overrides)
        return m.build_codeai_independent_verification_envelope(**values)

    def test_passed_example_records_bounded_verification(self):
        result = self.build()
        self.assertEqual(m.STATUS_READY, result.status)
        self.assertEqual((), result.issues)
        self.assertIsNotNone(result.receipt)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_PASSED, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_VERIFIED_PASS, receipt["operating_mode"])
        self.assertEqual(m.OUTCOME_PASSED, receipt["verification_outcome"])
        self.assertTrue(receipt["verification_completed"])
        self.assertFalse(receipt["verification_debt_open"])
        self.assertTrue(receipt["candidate_verification_passed"])

    def test_failed_is_first_class_and_not_rejection_authority(self):
        evidence = failed_evidence(self.example["verification_evidence"])
        result = self.build(verification_evidence=evidence)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_FAILED, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_VERIFIED_FAIL, receipt["operating_mode"])
        self.assertEqual(m.OUTCOME_FAILED, receipt["verification_outcome"])
        self.assertTrue(receipt["candidate_verification_failed"])
        self.assertFalse(receipt["failed_treated_as_rejection_authority"])
        self.assertFalse(receipt["candidate_applied"])

    def test_inconclusive_preserves_debt_and_reverification(self):
        evidence = inconclusive_evidence(self.example["verification_evidence"])
        result = self.build(verification_evidence=evidence)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_INCONCLUSIVE_DEGRADED,
            receipt["codeai_disposition"],
        )
        self.assertEqual(m.OUTCOME_INCONCLUSIVE, receipt["verification_outcome"])
        self.assertTrue(receipt["verification_completed"])
        self.assertTrue(receipt["verification_debt_open"])
        self.assertTrue(receipt["reverification_required"])

    def test_receipt_binds_candidate_and_preserves_source_commit(self):
        result = self.build()
        receipt = result.receipt
        assert receipt is not None
        source = self.example["source_candidate_receipt"]
        self.assertEqual(
            source[m.SOURCE_RECEIPT_DIGEST_FIELD],
            receipt["source_candidate_receipt_digest"],
        )
        self.assertEqual(source["candidate_patch_digest"], receipt["candidate_patch_digest"])
        self.assertEqual(source["patch_artifact_digest"], receipt["patch_artifact_digest"])
        self.assertEqual(receipt["source_commit_sha"], receipt["resulting_commit_sha"])
        self.assertEqual(
            receipt[m.RECEIPT_DIGEST_FIELD],
            m.digest_without(receipt, m.RECEIPT_DIGEST_FIELD),
        )

    def test_verifier_and_reviewer_are_independent(self):
        evidence = deepcopy(self.example["verification_evidence"])
        evidence["reviewer_id"] = evidence["verifier_id"]
        evidence = reseal_evidence(evidence)
        result = self.build(verification_evidence=evidence)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_INDEPENDENCE_REPAIR,
            receipt["codeai_disposition"],
        )

    def test_mutation_rejection_precedes_inconclusive_degradation(self):
        evidence = deepcopy(
            inconclusive_evidence(self.example["verification_evidence"])
        )
        evidence["live_repository_mutated_by_verifier"] = True
        evidence = reseal_evidence(evidence)
        result = self.build(verification_evidence=evidence)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
            receipt["codeai_disposition"],
        )
        self.assertEqual(m.MODE_REJECTED, receipt["operating_mode"])

    def test_receipt_grants_no_effect_or_successor_authority(self):
        result = self.build()
        receipt = result.receipt
        assert receipt is not None
        for field in (
            "verification_execution_performed_by_kernel",
            "candidate_selected",
            "candidate_applied",
            "execution_lease_issued",
            "repository_mutation_performed",
            "git_ref_changed",
            "branch_created",
            "commit_created",
            "push_performed",
            "pull_request_created",
            "merge_performed",
            "deployment_performed",
            "secret_access_performed",
            "selection_authority_granted",
            "verification_authority_granted",
            "execution_authority_granted",
            "merge_authority_granted",
            "deployment_authority_granted",
            "secret_access_authority_granted",
            "source_receipt_treated_as_verification_authority",
            "verification_treated_as_truth",
            "passed_treated_as_correctness_proof",
            "failed_treated_as_rejection_authority",
        ):
            self.assertFalse(receipt[field], field)

    def test_tampered_evidence_fails_closed(self):
        evidence = deepcopy(self.example["verification_evidence"])
        evidence["outcome_reason_ids"].append("unsealed-reason")
        result = self.build(verification_evidence=evidence)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("verification_evidence_digest_mismatch", result.issues)

    def test_all_disposition_routes(self):
        run_route_checker()


if __name__ == "__main__":
    unittest.main()
