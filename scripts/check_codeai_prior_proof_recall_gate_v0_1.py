#!/usr/bin/env python3
"""Negative and actual C60 regression: no proof/novelty inference from recall."""
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import scan, assess, TOOLCHAIN, MATHLIB

HEAD = "a" * 40
QI = "formal/KUOS/Architecture/QiWuxingPentagonUnifiedV3_5.lean"
F112 = "formal/Kuu/F112/PolygonNativeF55P94DK5FiveStageTypedShell.lean"

class RecallGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "formal").mkdir()
        (self.root / "lean").mkdir()
        (self.root / "lean-toolchain").write_text(TOOLCHAIN)
        (self.root / "lake-manifest.json").write_text(json.dumps(
            {"packages":[{"name":"mathlib","rev":MATHLIB}]}))
        (self.root / "formal/old.lean").write_text("theorem oldFivefoldSlot : True := by trivial\n")
        (self.root / "lean/other.lean").write_text("def otherSector : Nat := 5\n")
        self.receipt = scan(self.root, HEAD, ["FivefoldSlot", "Sector"])
        self.review = {
            "receipt_digest": self.receipt["receipt_digest"],
            "target": "renamed oldFivefoldSlot", "assumptions": "same hypotheses",
            "reviewer": "synthetic regression", "request": "new", "delta": "rename",
            "comparisons": [{"path": h["path"], "blob": h["blob"],
                "line": h["matches"][0]["line"], "declaration": "oldFivefoldSlot" if "old" in h["path"] else "otherSector",
                "relation": "equivalent" if "old" in h["path"] else "irrelevant",
                "reason": "synthetic regression only"} for h in self.receipt["hits"]]
        }

    def check(self):
        return assess(self.root, HEAD, self.receipt, self.review)

    def test_duplicate_blocks_new(self):
        self.assertEqual(self.check()["status"], "HOLD_DUPLICATE_REUSE_REQUIRED")
        self.assertFalse(self.check()["candidate_generation_hint"])
        self.review["request"] = "reuse"
        self.assertEqual(self.check()["status"], "REUSE_EXISTING")

    def test_incomplete_and_stale_hold(self):
        self.review["comparisons"].pop()
        self.assertEqual(self.check()["status"], "HOLD_UNREVIEWED")
        (self.root / "formal/new.lean").write_text("def silentChange := 7\n")
        self.assertIn("stale_or_unbound_recall_receipt", self.check()["issues"])

    def test_new_head_holds_even_if_contents_same(self):
        self.assertEqual(assess(self.root, "b"*40, self.receipt, self.review)["status"], "HOLD_UNREVIEWED")

    def test_no_hits_does_not_certify_novelty(self):
        r = scan(self.root, HEAD, ["missing1", "missing2"])
        self.assertEqual(r["status"], "HOLD_NO_DATA")
        self.assertFalse(r["novelty_certified"])

    def test_bridge_requires_consumer_and_delta(self):
        self.review["request"] = "bridge"
        self.assertEqual(self.check()["status"], "HOLD_UNREVIEWED")
        self.review["consumer"] = "typed consumer"
        self.assertEqual(self.check()["status"], "BRIDGE_PROPOSAL_ONLY_NOT_NOVELTY")
        self.assertFalse(self.check()["novelty_certified"])

    def test_review_delta_only_never_proof(self):
        for c in self.review["comparisons"]:
            c["relation"] = "prerequisite"
        self.review["delta"] = "unproved noncommutative pasting obligation"
        r = self.check()
        self.assertEqual(r["status"], "REVIEWED_DELTA_PROPOSAL_ONLY")
        for key in ("novelty_certified", "proof_authority", "execution_authority", "merge_authority"):
            self.assertFalse(r[key])
        self.review["comparisons"][0]["relation"] = "unresolved"
        self.assertEqual(self.check()["status"], "HOLD_UNREVIEWED")

    def test_actual_c60_cross_family_recall(self):
        r = scan(ROOT, os.environ.get("GITHUB_SHA", HEAD),
                 ["fivefoldSlotEquiv", "fivefoldSide_endpoints", "northK5TypedVertex_physical_five_sectors",
                  "fivefoldGK5AGNorthRotationCount_noPhysicalP92Descent"])
        hits = {h["path"]: h for h in r["hits"]}
        self.assertIn(QI, hits)
        self.assertIn(F112, hits)
        self.assertTrue(all(r["term_counts"].values()))
        self.assertTrue(any("def fivefoldSlotEquiv" in m["text"] for m in hits[QI]["matches"]))
        self.assertTrue(any("theorem northK5TypedVertex_physical_five_sectors" in m["text"] for m in hits[F112]["matches"]))
        self.assertEqual(r["status"], "REVIEW_REQUIRED")
        self.assertFalse(r["novelty_certified"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
