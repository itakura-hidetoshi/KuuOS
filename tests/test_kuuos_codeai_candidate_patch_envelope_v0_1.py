from copy import deepcopy
import unittest

import runtime.kuuos_codeai_candidate_patch_envelope_v0_1 as m
from scripts.check_codeai_candidate_patch_envelope_v0_1 import (
    load_example,
    main as run_route_checker,
    reseal_candidate,
)


class CodeAICandidatePatchEnvelopeV01Test(unittest.TestCase):
    def setUp(self):
        self.example = load_example()

    def build(self, **overrides):
        values = {
            "source_observation_receipt": self.example[
                "source_observation_receipt"
            ],
            "patch_candidate": self.example["patch_candidate"],
            "patch_artifact": self.example["patch_artifact"],
            "candidate_policy": self.example["candidate_policy"],
        }
        values.update(overrides)
        return m.build_codeai_candidate_patch_envelope(**values)

    def test_supported_example_is_proposal_only(self):
        result = self.build()
        self.assertEqual(m.STATUS_READY, result.status)
        self.assertEqual((), result.issues)
        self.assertIsNotNone(result.receipt)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_SUPPORTED, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_PROPOSAL_ONLY, receipt["operating_mode"])
        self.assertTrue(receipt["candidate_patch_ready"])
        self.assertTrue(receipt["candidate_patch_recorded"])
        self.assertTrue(receipt["candidate_patch_artifact_parsed"])
        self.assertFalse(receipt["candidate_selected"])

    def test_receipt_binds_source_and_preserves_commit(self):
        result = self.build()
        receipt = result.receipt
        assert receipt is not None
        source = self.example["source_observation_receipt"]
        candidate = self.example["patch_candidate"]
        self.assertEqual(
            source[m.SOURCE_RECEIPT_DIGEST_FIELD],
            receipt["source_observation_receipt_digest"],
        )
        self.assertEqual(source["source_commit_sha"], receipt["source_commit_sha"])
        self.assertEqual(receipt["source_commit_sha"], receipt["resulting_commit_sha"])
        self.assertEqual(candidate["patch_artifact_digest"], receipt["patch_artifact_digest"])
        self.assertEqual(
            receipt[m.RECEIPT_DIGEST_FIELD],
            m.digest_without(receipt, m.RECEIPT_DIGEST_FIELD),
        )

    def test_parser_and_declared_paths_are_exact(self):
        shape, issues = m.parse_unified_diff(self.example["patch_artifact"])
        self.assertEqual((), issues)
        self.assertIsNotNone(shape)
        assert shape is not None
        candidate = self.example["patch_candidate"]
        self.assertEqual(tuple(candidate["changed_paths"]), shape.changed_paths)
        self.assertEqual(tuple(candidate["added_paths"]), shape.added_paths)
        self.assertFalse(shape.binary_patch_present)
        self.assertFalse(shape.submodule_patch_present)
        self.assertFalse(shape.mode_change_present)

    def test_receipt_grants_no_effect_or_successor_authority(self):
        result = self.build()
        receipt = result.receipt
        assert receipt is not None
        for field in (
            "candidate_generated_by_kernel",
            "candidate_selected",
            "verification_lease_issued",
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
            "source_receipt_treated_as_successor_authority",
            "candidate_treated_as_correct",
            "validation_treated_as_correctness_proof",
        ):
            self.assertFalse(receipt[field], field)

    def test_mutation_rejection_precedes_clarification(self):
        candidate = deepcopy(self.example["patch_candidate"])
        candidate["patch_applied_by_kernel"] = True
        candidate["unresolved_candidate_questions"] = ["still unresolved"]
        candidate = reseal_candidate(candidate)
        result = self.build(patch_candidate=candidate)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
            receipt["codeai_disposition"],
        )
        self.assertEqual(m.MODE_REJECTED, receipt["operating_mode"])

    def test_empty_evidence_identifier_does_not_satisfy_policy(self):
        candidate = deepcopy(self.example["patch_candidate"])
        candidate["test_plan_ids"] = [""]
        candidate = reseal_candidate(candidate)
        result = self.build(patch_candidate=candidate)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_CANDIDATE_PROVENANCE_REPAIR,
            receipt["codeai_disposition"],
        )

    def test_tampered_candidate_fails_closed(self):
        candidate = deepcopy(self.example["patch_candidate"])
        candidate["requirement_trace_ids"].append("unsealed-trace")
        result = self.build(patch_candidate=candidate)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("patch_candidate_digest_mismatch", result.issues)

    def test_all_disposition_routes(self):
        run_route_checker()


if __name__ == "__main__":
    unittest.main()
