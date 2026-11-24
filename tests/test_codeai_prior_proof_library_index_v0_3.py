"""Source-bound catalog, lexical search, review boundary and exact routing regressions."""
from __future__ import annotations

import copy
import gzip
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import (
    REPOSITORY, tree_hash, build_catalog, search_catalog, assess_library,
    build_library_research_synthesis,
)
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob, TOOLCHAIN, MATHLIB

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = "ci/check_registry.d/codeai_prior_proof_library_v0_3.json"
CHECK = "codeai-prior-proof-library-v03"
SCOPE = [
    ".github/workflows/codeai-prior-proof-library-v0-3.yml",
    "AGENTS.md", FRAGMENT,
    "docs/KUUOS_CODEAI_PRIOR_PROOF_LIBRARY_INDEX_v0_3.md",
    "runtime/kuuos_codeai_prior_proof_library_index_v0_3.py",
    "scripts/codeai_prior_proof_library_index_v0_3.py",
    "tests/test_codeai_prior_proof_library_index_v0_3.py",
]


class LibraryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/"formal").mkdir()
        (self.root/"lean").mkdir()
        (self.root/"memoryos").mkdir()
        (self.root/"memoryos/research_prior_proof_subject_index_v0_2.json").write_text(
            json.dumps({"topics":[{"aliases":["C60"]}]}))
        self.files = {
            "formal/Alpha.lean": ("import Beta\n/- theorem ghost : True := by trivial -/\n"
                                  "theorem sourceOverlapDescent (x : Nat) : x = x := by rfl\n"),
            "lean/Beta.lean": "theorem priorSupport : True := by trivial\n",
            "lean-toolchain": TOOLCHAIN+"\n",
            "lake-manifest.json": json.dumps({"packages":[{"name":"mathlib","rev":MATHLIB}]}),
            "lakefile.toml": 'name = "fixture"\n',
        }
        for path, source in self.files.items():
            (self.root/path).write_text(source)
        roots = []
        for name, path in (("formal", "formal/Alpha.lean"), ("lean", "lean/Beta.lean")):
            roots.append({"path":name,"mode":"040000","sha":tree_hash([
                {"path":Path(path).name,"mode":"100644","sha":git_blob(self.files[path].encode())}])})
        for name in ("lean-toolchain", "lake-manifest.json", "lakefile.toml"):
            roots.append({"path":name,"mode":"100644","sha":git_blob(self.files[name].encode())})
        self.obs = {"repository":REPOSITORY,"source_head":"a"*40,"source_tree":tree_hash(roots),
                    "scope":"canonical_main","truncated":False,"root_entries":roots}

    def receipt(self, query="source overlap descent", **kwargs):
        return search_catalog(build_catalog(self.root,self.obs),query,**kwargs)

    def review(self, receipt):
        return {"request":"new","library_receipt_digest":receipt["receipt_digest"],
                "library_comparisons":[{"id":d["id"],"source_blob":d["source_blob"],
                     "signature_digest":d["signature_digest"],"relation":"prerequisite",
                     "reason":"synthetic only","assumptions_comparison":"fixture",
                     "conclusion_comparison":"fixture"} for d in receipt["hits"]],
                "parse_gap_reviews":[]}

    def test_exact_tree_and_automatic_discovery(self):
        catalog = build_catalog(self.root,self.obs)
        self.assertEqual(catalog["lean_source_file_count"],2)
        self.assertEqual(catalog["named_declaration_preview_count"],2)
        result = self.receipt()
        self.assertEqual(result["status"],"REVIEW_REQUIRED")
        self.assertEqual(result["hits"][0]["name_lexical"],"sourceOverlapDescent")
        self.assertIn("(x : Nat)",result["hits"][0]["signature_preview"])
        self.assertEqual(result["source_import_candidates"][0]["imports"],
                         [{"module":"Beta","local_source_candidates":["lean/Beta.lean"]}])
        self.assertFalse(result["novelty_certified"])

    def test_extra_or_changed_source_cannot_reuse_tree(self):
        extra=self.root/"formal/Extra.lean"
        extra.write_text("theorem extra : True := by trivial\n")
        with self.assertRaisesRegex(ValueError,"materialized source tree differs"):
            build_catalog(self.root,self.obs)
        extra.unlink()
        (self.root/"formal/Alpha.lean").write_text(self.files["formal/Alpha.lean"]+"-- drift\n")
        with self.assertRaisesRegex(ValueError,"materialized source tree differs"):
            build_catalog(self.root,self.obs)

    def test_root_observation_and_pin_binding(self):
        wrong=copy.deepcopy(self.obs)
        wrong["source_tree"]="b"*40
        with self.assertRaisesRegex(ValueError,"root tree observation mismatch"):
            build_catalog(self.root,wrong)
        (self.root/"lakefile.toml").write_text('name = "other"\n')
        with self.assertRaisesRegex(ValueError,"pinned source file mismatch"):
            build_catalog(self.root,self.obs)

    def test_no_hits_and_truncation_hold(self):
        missing=self.receipt("missing xyz")
        self.assertEqual(missing["status"],"HOLD_NO_DATA")
        broad=self.receipt("theorem",limit=1)
        self.assertEqual(broad["status"],"HOLD_TRUNCATED")
        self.assertEqual(broad["omitted_hits"],1)
        for r in (missing,broad):
            result=assess_library(self.root,self.obs,r,self.review(r))
            self.assertFalse(result["candidate_generation_hint"])

    def test_declaration_level_duplicate_and_stale_receipt_hold(self):
        r=self.receipt()
        review=self.review(r)
        review["library_comparisons"][0]["relation"]="equivalent"
        result=assess_library(self.root,self.obs,r,review)
        self.assertEqual(result["status"],"HOLD_DUPLICATE_REUSE_REQUIRED")
        review["library_comparisons"][0]["relation"]="prerequisite"
        new=copy.deepcopy(self.obs)
        new["source_head"]="b"*40
        self.assertIn("stale_or_unbound_library_recall",
                      assess_library(self.root,new,r,review)["issues"])
        review["library_comparisons"].clear()
        self.assertIn("unreviewed_library_declarations",
                      assess_library(self.root,self.obs,r,review)["issues"])

    def test_comment_decoy_is_not_a_declaration(self):
        r=self.receipt("ghost")
        self.assertEqual(r["total_hits"],0)

    def test_provider_never_receives_unreviewed_or_missing_context(self):
        r=self.receipt()
        review=self.review(r)
        kernel="runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1.build_research_structured_edit_synthesis"
        with patch(kernel) as downstream:
            result=build_library_research_synthesis(
                root=self.root,observation=self.obs,library_receipt=r,mathematical_review=review,
                recall_receipt={},repository_files={})
            self.assertEqual(result["status"],"HOLD_RESEARCH_RECALL")
            self.assertIn("missing_library_source_context",result["issues"])
            downstream.assert_not_called()

    def test_known_subject_cannot_bypass_subject_gate(self):
        r=self.receipt()
        review=self.review(r)
        review["target"]="C60"
        kernel="runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1.build_research_structured_edit_synthesis"
        with patch(kernel) as downstream:
            result=build_library_research_synthesis(
                root=self.root,observation=self.obs,library_receipt=r,mathematical_review=review,
                recall_receipt={},repository_files={"formal/Alpha.lean":self.files["formal/Alpha.lean"]})
            self.assertEqual(result["status"],"HOLD_RESEARCH_RECALL")
            self.assertIn("missing_existing_subject_review",result["issues"])
            downstream.assert_not_called()


class RoutingTests(unittest.TestCase):
    def test_registration_preserves_existing_full_and_focused_checks(self):
        from scripts.select_impacted_checks import load_registry, select
        registry=load_registry(ROOT/"ci/check_registry.yaml")
        regular=[p for p in SCOPE if p!=FRAGMENT]
        focused=select(registry,regular,None)
        self.assertEqual(focused["unmapped_paths"],[])
        self.assertFalse(focused["full_audit_required"])
        self.assertFalse(focused["lean_required"])
        self.assertIn(CHECK,{row["id"] for row in focused["selected_checks"]})
        self.assertIn("codeai-prior-proof-recall-v02",{row["id"] for row in focused["selected_checks"]})
        first=select(registry,SCOPE,None)
        self.assertTrue(first["full_audit_required"])
        self.assertTrue(first["lean_required"])
        self.assertIn(FRAGMENT,first["full_audit_trigger_paths"])
        unknown=select(registry,regular+["scripts/unregistered_library_probe.py"],None)
        self.assertTrue(unknown["full_audit_required"])
        self.assertTrue(unknown["lean_required"])
        with patch("scripts.select_impacted_checks.select_lean_targets",
                   return_value=(["KuuOSFormal"],"synthetic scope")):
            self.assertTrue(select(registry,regular+["formal/Kuu/Actual.lean"],None)["lean_required"])


class RealCatalogTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("KUUOS_LIBRARY_CATALOG_DIR"),"actual exact-tree artifact not supplied")
    def test_real_library_discovers_outside_curated_catalog(self):
        out=Path(os.environ["KUUOS_LIBRARY_CATALOG_DIR"])
        with gzip.open(out/"catalog.json.gz","rt",encoding="utf-8") as stream:
            catalog=json.load(stream)
        self.assertEqual(catalog["source_head_as_observed_by_caller"],os.environ["GITHUB_SHA"])
        self.assertGreater(catalog["lean_source_file_count"],100)
        self.assertGreater(catalog["named_declaration_preview_count"],1000)
        self.assertFalse(catalog["novelty_certified"])
        # Query contains no stored theorem name, and LEC is not in the v0.2
        # curated six-topic catalog.
        lec=json.loads((out/"living-engi.json").read_text())
        path="formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean"
        self.assertTrue(any(x["path"]==path and
                            x["name_lexical"]=="sourceGlobal_iff_shadowGlobal_and_overlapFaithful"
                            for x in lec["hits"]),lec["total_hits"])
        self.assertTrue(any(x["path"]==path and x["imports"] for x in lec["source_import_candidates"]))
        self.assertFalse(lec["semantic_search_complete"])
        higher=json.loads((out/"higher-cell.json").read_text())
        self.assertTrue(any(x["name_lexical"]=="nativeK5ASGroupHistoryDescent_iff"
                            for x in higher["hits"]),higher["total_hits"])
        self.assertEqual(lec["source_tree"],catalog["source_tree"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
