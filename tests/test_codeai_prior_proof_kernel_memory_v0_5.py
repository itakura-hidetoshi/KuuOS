"""Read-only immutable packet and whole-library union tests."""
import copy
import os
from pathlib import Path
import unittest

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import (
    load_packets, verify_packets, join_kernel_memory, PACKET_DIGESTS, COMBINED_DIGEST)
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import ENVIRONMENT_BLOBS
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest

ROOT = Path(__file__).resolve().parents[1]


class CombinedPacketTests(unittest.TestCase):
    def setUp(self):
        self.parent, self.frontier = load_packets(ROOT)
        self.obs = {"source_head": "a"*40, "source_tree": "b"*40, "scope": "research_head",
                    "root_entries": [{"path": k, "sha": v} for k,v in ENVIRONMENT_BLOBS.items()]}
        self.cat = {"source_head_as_observed_by_caller": self.obs["source_head"],
                    "source_tree": self.obs["source_tree"], "catalog_digest": "c"*64,
                    "source_subtrees": self.parent["source_subtrees"], "pins": self.parent["pins"]}
        self.lex = {"source_head_as_observed_by_caller": self.obs["source_head"],
                    "source_tree": self.obs["source_tree"], "catalog_digest": self.cat["catalog_digest"],
                    "status": "REVIEW_REQUIRED", "hits": [
                        {"id": r["lexical_id"], "path": r["path"], "name_lexical": r["name"].rsplit(".",1)[-1],
                         "kind":"theorem", "source_blob": r["blob"], "line":r["line"],
                         "signature_digest":r["signature_preview_digest"]}
                        for r in self.parent["observations"] + self.frontier["observations"]]}
    def join(self):
        self.lex.pop("receipt_digest", None)
        self.lex["receipt_digest"] = digest(self.lex)
        return join_kernel_memory(ROOT, self.obs, self.cat, self.lex, self.parent, self.frontier)
    def test_union_keeps_both_historical_heads_and_no_authority(self):
        x = self.join()
        self.assertEqual(x["status"], "REVIEW_REQUIRED")
        self.assertEqual(len(x["matched_observations"]),13)
        self.assertEqual(x["historical_packet_digests"], PACKET_DIGESTS)
        self.assertEqual(x["historical_packet_digest"], COMBINED_DIGEST)
        for version, p in (("v0.4", self.parent), ("v0.5", self.frontier)):
            rows = [r for r in x["matched_observations"] if r["historical_packet_version"] == version]
            self.assertEqual(len(rows),len(p["observations"]))
            self.assertTrue(all(r["historical_source_head"] == p["source_head"] and
                                r["historical_run_id"] == p["provenance"]["run_id"] for r in rows))
        self.assertFalse(x["proof_authority"] or x["novelty_certified"] or
                         x["full_transitive_proof_dependencies_verified"])
    def test_scope_drift_holds_even_without_matched_hits(self):
        self.cat["source_subtrees"] = dict(self.cat["source_subtrees"], formal="f"*40)
        self.assertEqual(len(self.join()["stale_observations"]),13)
        self.lex["hits"] = []
        self.assertEqual(self.join()["status"],"HOLD_REOBSERVE_KERNEL")
    def test_tampered_frontier_and_legacy_packet_hold(self):
        for packet in (self.parent,self.frontier):
            bad = copy.deepcopy(packet)
            bad["observations"][0]["axioms"] = ["invented"]
            with self.assertRaisesRegex(ValueError,"packet digest drift"):
                verify_packets(bad if packet is self.parent else self.parent,
                               bad if packet is self.frontier else self.frontier)
    def test_unknown_and_stale_remain_separate(self):
        self.lex["hits"][0]["name_lexical"] = "not_observed"
        self.lex["hits"][1]["signature_digest"] = "f"*64
        x = self.join()
        self.assertEqual(len(x["matched_observations"]),11)
        self.assertEqual(len(x["without_kernel_observation"]),1)
        self.assertEqual(len(x["stale_observations"]),1)
        self.assertEqual(x["status"],"HOLD_REOBSERVE_KERNEL")
    def test_lexical_truncation_and_duplicate_hold(self):
        self.lex["status"] = "HOLD_TRUNCATED"
        self.assertEqual(self.join()["status"],"HOLD_LEXICAL_RECALL")
        self.lex["hits"].append(self.lex["hits"][0])
        with self.assertRaisesRegex(ValueError,"duplicate lexical hit"):
            self.join()


@unittest.skipUnless(os.environ.get("KUUOS_KERNEL_FIRST"),"actual replay context absent")
class ActualCombinedRecallTests(unittest.TestCase):
    def test_actual_catalog_retrieves_all_thirteen_with_distinct_provenance(self):
        from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog
        from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
        parent, frontier = load_packets(ROOT)
        obs = github_observation(os.environ["GITHUB_SHA"],"research_head")
        cat = build_catalog(ROOT,obs)
        matched = {}
        for row in parent["observations"] + frontier["observations"]:
            short = row["name"].rsplit(".",1)[-1]
            lex = search_catalog(cat,short,terms=[short],limit=500)
            result = join_kernel_memory(ROOT,obs,cat,lex,parent,frontier)
            self.assertEqual(result["status"],"REVIEW_REQUIRED")
            found = [x for x in result["matched_observations"] if x["lexical_id"] == row["lexical_id"]]
            self.assertEqual(len(found),1)
            matched[row["name"]] = found[0]["historical_packet_version"]
        self.assertEqual(len(matched),13)
        self.assertEqual(list(matched.values()).count("v0.4"),3)
        self.assertEqual(list(matched.values()).count("v0.5"),10)
        print("KUUOS_V05_ACTUAL_COMBINED_RECALL 13/13 v04=3 v05=10",flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
