from copy import deepcopy
import unittest

import runtime.kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1 as m
from scripts.check_codeai_autonomous_trajectory_synthesis_envelope_v0_1 import (
    bind_to_source,
    failed_source,
    inconclusive_source,
    load_example,
    main as run_route_checker,
    reseal_request,
)


class CodeAIAutonomousTrajectorySynthesisEnvelopeV01Test(unittest.TestCase):
    def setUp(self):
        self.example = load_example()

    def build(self, **overrides):
        values = {
            "source_verification_receipt": self.example[
                "source_verification_receipt"
            ],
            "trajectory_request": self.example["trajectory_request"],
            "trajectory_policy": self.example["trajectory_policy"],
        }
        values.update(overrides)
        return m.build_codeai_autonomous_trajectory_synthesis_envelope(**values)

    def test_passed_synthesizes_read_only_deliberation_candidate(self):
        result = self.build()
        self.assertEqual(m.STATUS_READY, result.status)
        self.assertEqual((), result.issues)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_DELIBERATION, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_AUTONOMOUS_READ_ONLY, receipt["operating_mode"])
        self.assertEqual(m.NEXT_DELIBERATION, receipt["next_internal_step_kind"])
        self.assertTrue(receipt["trajectory_synthesized_by_kernel"])
        self.assertTrue(receipt["autonomous_deliberation_candidate_generated"])

    def test_failed_synthesizes_repair_candidate_without_patch(self):
        source = failed_source(self.example["source_verification_receipt"])
        request, policy = bind_to_source(
            self.example["trajectory_request"], self.example["trajectory_policy"], source
        )
        result = self.build(
            source_verification_receipt=source,
            trajectory_request=request,
            trajectory_policy=policy,
        )
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_REPAIR, receipt["codeai_disposition"])
        self.assertEqual(m.NEXT_REPAIR, receipt["next_internal_step_kind"])
        self.assertTrue(receipt["autonomous_repair_candidate_generated"])
        self.assertFalse(receipt["patch_generated"])
        self.assertFalse(receipt["patch_applied"])

    def test_inconclusive_synthesizes_reverification_candidate(self):
        source = inconclusive_source(self.example["source_verification_receipt"])
        request, policy = bind_to_source(
            self.example["trajectory_request"], self.example["trajectory_policy"], source
        )
        result = self.build(
            source_verification_receipt=source,
            trajectory_request=request,
            trajectory_policy=policy,
        )
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_REVERIFICATION, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_DEGRADED_AUTONOMY, receipt["operating_mode"])
        self.assertEqual(m.NEXT_REVERIFICATION, receipt["next_internal_step_kind"])
        self.assertTrue(receipt["autonomous_reverification_candidate_generated"])

    def test_trajectory_reconstructs_only_available_receipts(self):
        receipt = self.build().receipt
        assert receipt is not None
        self.assertEqual(2, receipt["trajectory_step_count"])
        self.assertEqual(
            ["candidate-lineage-anchor", "independent-verification"],
            receipt["trajectory_node_ids"],
        )
        self.assertEqual(2, len(receipt["trajectory_node_digests"]))
        self.assertTrue(receipt["trajectory_complete_for_available_receipts"])
        self.assertFalse(receipt["full_intent_lineage_reconstructed"])

    def test_external_handover_is_deferred_until_permission(self):
        request = deepcopy(self.example["trajectory_request"])
        request["external_handover_requested"] = True
        request = reseal_request(request)
        receipt = self.build(trajectory_request=request).receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_HANDOVER_DEFERRED, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_HOLD, receipt["operating_mode"])
        self.assertTrue(receipt["external_handover_deferred"])
        self.assertFalse(receipt["human_handover_performed"])
        self.assertFalse(receipt["external_authority_handover_performed"])
        self.assertFalse(receipt["trajectory_synthesized_by_kernel"])

    def test_effect_request_rejected_before_autonomous_synthesis(self):
        request = deepcopy(self.example["trajectory_request"])
        request["git_mutation_requested"] = True
        request = reseal_request(request)
        receipt = self.build(trajectory_request=request).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_EFFECT_REQUEST_REJECTED, receipt["codeai_disposition"]
        )
        self.assertFalse(receipt["trajectory_synthesized_by_kernel"])

    def test_receipt_grants_no_effect_or_successor_authority(self):
        receipt = self.build().receipt
        assert receipt is not None
        for field in (
            "human_handover_performed",
            "external_authority_handover_performed",
            "candidate_selected",
            "patch_generated",
            "patch_applied",
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
            "trajectory_treated_as_truth",
            "autonomous_candidate_treated_as_authority",
        ):
            self.assertFalse(receipt[field], field)

    def test_tampered_request_fails_closed(self):
        request = deepcopy(self.example["trajectory_request"])
        request["trajectory_revision"] = "unsealed"
        result = self.build(trajectory_request=request)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("trajectory_request_digest_mismatch", result.issues)

    def test_all_disposition_routes(self):
        run_route_checker()


if __name__ == "__main__":
    unittest.main()
