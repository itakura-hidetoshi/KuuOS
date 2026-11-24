#!/usr/bin/env python3
"""Exact-source subject retrieval and negative admission regression."""
from pathlib import Path
import os
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.kuuos_codeai_prior_proof_subject_gate_v0_2 import (
    recall_subject, assess_subject, build_subject_research_synthesis,
)

HEAD = os.environ.get("GITHUB_SHA", "a" * 40)


class SubjectRecallTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.phase = recall_subject(ROOT, HEAD, "五行とC60の物理辺をつなげたい")
        cls.high = recall_subject(ROOT, HEAD, "14-cell以上の非可換な貼合と降下")

    def test_japanese_phase_without_declaration_names(self):
        self.assertEqual(self.phase["status"], "REVIEW_REQUIRED", self.phase["issues"])
        names = {a["declaration"] for a in self.phase["anchors"]}
        self.assertTrue({"fivefoldSlotEquiv", "fivefoldSide_endpoints",
                         "northK5TypedVertex_physical_five_sectors"}.issubset(names))
        self.assertTrue(all(a["anchor_blob_matches"] for a in self.phase["anchors"]))

    def test_higher_pasting_remembers_proven_obstruction(self):
        self.assertEqual(self.high["status"], "REVIEW_REQUIRED", self.high["issues"])
        names = {a["declaration"] for a in self.high["anchors"]}
        self.assertTrue({"nativeK5FourteenSquareExchange_pastingRaw_ne",
                         "nativeK5Fourteen_noFiniteCoreFiller",
                         "nativeK5PentagonatorFifteen_raw_ne",
                         "fivefoldGK5AGNorthRotationCount_noPhysicalP92Descent",
                         "nativeC60NorthWuxingK5_actualFiveStage_obstruction"}.issubset(names))
        self.assertFalse(self.high["novelty_certified"])

    def test_contextual_descent_and_latest_old18d_source_recalled(self):
        r = recall_subject(ROOT, HEAD, "Peiffer核の普遍降下と18次元の原証明")
        self.assertEqual(r["status"], "REVIEW_REQUIRED", r["issues"])
        names = {a["declaration"] for a in r["anchors"]}
        self.assertTrue({"nativeK5AQ_factors_iff",
                         "nativeK5ARHistoryKernel_eq_base",
                         "nativeK5ASGroupHistoryDescent_iff",
                         "nativeK5ATGroupReceiver_allContexts_iff",
                         "nativeK5AUTypeReceiver_descent_iff",
                         "selectedV599C60OriginalJointObservation_eq_iff",
                         "selectedV599C60PhysicalShadow_notRawFaithful"}.issubset(names))
        self.assertFalse(r["novelty_certified"])

    def test_unknown_subject_never_becomes_new_result(self):
        r = recall_subject(ROOT, HEAD, "unindexed_xyz_785")
        self.assertEqual(r["status"], "HOLD_REOBSERVATION")
        self.assertFalse(r["proof_authority"])

    def fixture_review(self, r):
        lexical = r["lexical_receipt"]
        return {"subject_receipt_digest": r["receipt_digest"],
                "receipt_digest": lexical["receipt_digest"],
                "target": "test only", "assumptions": "test only",
                "reviewer": "synthetic regression", "request": "new", "delta": "test only",
                "comparisons": [{"path": h["path"], "blob": h["blob"],
                                 "line": h["matches"][0]["line"], "declaration": "test-only",
                                 "relation": "prerequisite", "reason": "synthetic regression"}
                                for h in lexical["hits"]],
                "anchor_comparisons": [{"path": a["path"], "blob": a["blob"], "line": a["line"],
                                        "declaration": a["declaration"], "relation": "prerequisite",
                                        "reason": "synthetic regression",
                                        "assumptions_comparison": "test only",
                                        "conclusion_comparison": "test only"} for a in r["anchors"]]}

    def test_per_declaration_duplicate_blocks_even_if_file_review_disagrees(self):
        r = self.phase
        review = self.fixture_review(r)
        for a in review["anchor_comparisons"]:
            if a["declaration"] == "fivefoldSlotEquiv":
                a["relation"] = "equivalent"
        result = assess_subject(ROOT, HEAD, r, review)
        self.assertEqual(result["status"], "HOLD_DUPLICATE_REUSE_REQUIRED", result)
        self.assertFalse(result["candidate_generation_hint"])

    def test_missing_anchor_never_reaches_downstream(self):
        r = self.high
        review = self.fixture_review(r)
        review["anchor_comparisons"].pop()
        with patch("runtime.kuuos_codeai_prior_proof_subject_gate_v0_2.build_research_structured_edit_synthesis") as downstream:
            result = build_subject_research_synthesis(
                root=ROOT, source_head=HEAD, subject_receipt=r, mathematical_review=review)
            self.assertEqual(result["status"], "HOLD_RESEARCH_RECALL")
            downstream.assert_not_called()

    def test_stale_head_and_unresolved_anchor_hold(self):
        r = self.high
        review = self.fixture_review(r)
        review["anchor_comparisons"][0]["relation"] = "unresolved"
        changed = "b" * 40 if HEAD != "b" * 40 else "c" * 40
        result = assess_subject(ROOT, changed, r, review)
        self.assertEqual(result["status"], "HOLD_RESEARCH_RECALL")
        self.assertIn("stale_or_unbound_subject_receipt", result["issues"])
        self.assertTrue(any(s.startswith("unresolved_anchor:") for s in result["issues"]))

    def test_source_context_required_before_provider(self):
        r = self.high
        review = self.fixture_review(r)
        with patch("runtime.kuuos_codeai_prior_proof_subject_gate_v0_2.build_research_structured_edit_synthesis") as downstream:
            result = build_subject_research_synthesis(
                root=ROOT, source_head=HEAD, subject_receipt=r, mathematical_review=review,
                repository_files={})
            self.assertEqual(result["status"], "HOLD_RESEARCH_RECALL")
            self.assertIn("missing_anchored_source_context", result["issues"])
            downstream.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
