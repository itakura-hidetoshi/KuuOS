#!/usr/bin/env python3
"""Check that rejected research never reaches the original CodeAI provider."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_codeai_prior_proof_recall_gate_v0_1 import RecallGateTests, HEAD
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1 import build_research_structured_edit_synthesis

KERNEL = "runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1.build_codeai_autonomous_structured_edit_synthesis"

class ResearchSynthesisTests(RecallGateTests):
    def setUp(self):
        super().setUp()
        self.request = {"intent_text": "renamed oldFivefoldSlot; same hypotheses; rename"}
        self.review["synthesis_request_binding"] = digest(self.request)
        self.context = {"formal/old.lean": (self.root/"formal/old.lean").read_text()}
        self.observation = {"source_commit_sha": HEAD, "source_branch": "main",
                            "repository_full_name": "itakura-hidetoshi/KuuOS"}

    def run_wrapper(self):
        return build_research_structured_edit_synthesis(
            root=self.root, source_head=HEAD, recall_receipt=self.receipt,
            mathematical_review=self.review, source_observation_receipt=self.observation,
            repository_files=self.context, synthesis_request=self.request,
            provider_adapters=[], synthesis_policy={}, candidate_policy={})

    def admit_delta(self):
        self.review["comparisons"][0]["relation"] = "prerequisite"
        self.review["delta"] = "actual unproved residual"
        self.request["intent_text"] = "renamed oldFivefoldSlot; same hypotheses; actual unproved residual"
        self.review["synthesis_request_binding"] = digest(self.request)

    def test_duplicate_never_calls_original_kernel(self):
        with patch(KERNEL) as provider:
            self.assertEqual(self.run_wrapper()["status"], "HOLD_RESEARCH_RECALL")
            provider.assert_not_called()

    def test_exact_delta_forwards_original_kernel_only_after_review(self):
        self.admit_delta()
        with patch(KERNEL, return_value="synthetic kernel receipt") as provider:
            r = self.run_wrapper()
            self.assertEqual(r["status"], "FORWARDED_TO_ORIGINAL_CODEAI")
            self.assertEqual(r["synthesis"], "synthetic kernel receipt")
            provider.assert_called_once()

    def test_missing_prior_source_and_changed_request_hold(self):
        self.admit_delta()
        self.context.clear()
        with patch(KERNEL) as provider:
            self.assertIn("reviewed_prior_source_not_in_provider_context", self.run_wrapper()["issues"])
            self.request["intent_text"] += " unexpected mutation"
            self.assertIn("research_synthesis_request_unbound", self.run_wrapper()["issues"])
            provider.assert_not_called()

    def test_stale_head_and_stale_context_hold(self):
        self.admit_delta()
        self.observation["source_commit_sha"] = "b"*40
        self.context["formal/old.lean"] += "-- invented source\n"
        with patch(KERNEL) as provider:
            r = self.run_wrapper()
            self.assertIn("research_source_observation_mismatch", r["issues"])
            self.assertIn("provider_context_source_mismatch:formal/old.lean", r["issues"])
            provider.assert_not_called()

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ResearchSynthesisTests)
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        raise SystemExit(1)
