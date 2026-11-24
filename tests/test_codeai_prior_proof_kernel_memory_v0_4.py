"""Actual artifact projection and source-version-bound recall regression."""
import copy
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import (
    load_packet, verify_runner_receipts, join_kernel_memory, recall_kernel_memory,
    PACKET_DIGEST, ENVIRONMENT_BLOBS)
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation

ROOT=Path(__file__).resolve().parents[1]

class PacketTests(unittest.TestCase):
    def setUp(self):
        self.packet=load_packet(ROOT)
        row=self.packet["observations"][0]
        self.obs={"source_head":"a"*40,"source_tree":"b"*40,"scope":"research_head",
                  "root_entries":[{"path":k,"sha":v} for k,v in ENVIRONMENT_BLOBS.items()]}
        self.cat={"source_head_as_observed_by_caller":self.obs["source_head"],
                  "source_tree":self.obs["source_tree"],"source_subtrees":self.packet["source_subtrees"],
                  "pins":self.packet["pins"],"catalog_digest":"c"*64}
        self.lex={"catalog_digest":self.cat["catalog_digest"],"status":"REVIEW_REQUIRED",
                  "hits":[{"id":row["lexical_id"],"name_lexical":row["name"].rsplit(".",1)[-1],
                           "path":row["path"],"source_blob":row["blob"],"line":row["line"],
                           "signature_digest":row["signature_preview_digest"]}]}

    def join(self):
        return join_kernel_memory(ROOT,self.obs,self.cat,self.lex,self.packet)

    def test_committed_projection_digest(self):
        self.assertEqual(digest(self.packet),PACKET_DIGEST)
        self.assertEqual(len(self.packet["observations"]),3)

    def test_source_scope_unchanged_reuses_historical_observation_not_authority(self):
        x=self.join()
        self.assertEqual(x["status"],"REVIEW_REQUIRED")
        self.assertEqual(len(x["matched_observations"]),1)
        self.assertFalse(x["proof_authority"])
        self.assertFalse(x["novelty_certified"])
        self.assertFalse(x["full_transitive_proof_dependencies_verified"])

    def test_dependency_subtree_drift_even_if_target_blob_same_holds(self):
        self.cat["source_subtrees"]={**self.cat["source_subtrees"],"formal":"f"*40}
        x=self.join()
        self.assertEqual(x["status"],"HOLD_REOBSERVE_KERNEL")
        self.assertEqual(x["matched_observations"],[])
        self.assertEqual(len(x["stale_observations"]),1)

    def test_other_manifest_dependency_drift_holds(self):
        self.obs["root_entries"]=[{**r,"sha":"f"*40} if r["path"]=="lake-manifest.json" else r
                                  for r in self.obs["root_entries"]]
        self.assertEqual(self.join()["status"],"HOLD_REOBSERVE_KERNEL")

    def test_target_identity_and_unobserved_hits_not_promoted(self):
        self.lex["hits"][0]["id"]="f"*64
        self.assertEqual(self.join()["status"],"HOLD_REOBSERVE_KERNEL")
        self.lex["hits"][0]["name_lexical"]="not_observed"
        x=self.join()
        self.assertEqual(x["status"],"NO_DATA_KERNEL_LEXICAL_REVIEW_ONLY")
        self.assertEqual(len(x["without_kernel_observation"]),1)
        self.assertEqual(x["matched_observations"],[])

    def test_tampered_packet_and_truncated_recall(self):
        self.lex["status"]="HOLD_TRUNCATED"
        self.assertEqual(self.join()["status"],"HOLD_LEXICAL_RECALL")
        self.packet["observations"][0]["axioms"]=[]
        with self.assertRaisesRegex(ValueError,"packet digest drift"):
            self.join()

    def test_stale_catalog(self):
        self.obs["source_head"]="d"*40
        with self.assertRaisesRegex(ValueError,"stale catalog"):
            self.join()

@unittest.skipUnless(os.environ.get("KUUOS_KERNEL_FIRST"),"actual runner artifacts not supplied")
class ActualArtifactTests(unittest.TestCase):
    def test_exact_projection_from_actual_two_runner_receipts(self):
        p=load_packet(ROOT)
        a=Path(os.environ["KUUOS_KERNEL_FIRST"])
        b=Path(os.environ["KUUOS_KERNEL_FRESH"])
        read=lambda x:json.loads(x.read_text())
        first,fresh,mcp,ind=read(a/"direct.json"),read(b/"direct.json"),read(a/"mcp.json"),read(b/"independent.json")
        verify_runner_receipts(p,first,fresh,mcp,ind)
        bad=copy.deepcopy(first)
        bad["observations"][0]["proof_constants"]=[]
        with self.assertRaisesRegex(ValueError,"receipt digest mismatch"):
            verify_runner_receipts(p,bad,fresh,mcp,ind)
        obs=github_observation(os.environ["GITHUB_SHA"],"research_head")
        lec=recall_kernel_memory(ROOT,obs,"source aware overlap descent",limit=500)
        qi=recall_kernel_memory(ROOT,obs,"c60 gauge slot injective",limit=500)
        self.assertEqual(len(lec["matched_observations"]),2)
        self.assertEqual(len(qi["matched_observations"]),1)
        self.assertEqual(lec["stale_observations"],[])
        self.assertEqual(qi["stale_observations"],[])
        print("KUUOS_KERNEL_MEMORY_REPLAY",json.dumps({"matched_LEC":2,"matched_Qi":1,
              "source_head":obs["source_head"],"source_tree":obs["source_tree"],
              "historical_head":p["source_head"],"historical_packet_digest":PACKET_DIGEST,
              "unobserved_LEC_hits":len(lec["without_kernel_observation"]),
              "unobserved_Qi_hits":len(qi["without_kernel_observation"]),
              "proof_authority":False},sort_keys=True),flush=True)

if __name__=="__main__":
    unittest.main(verbosity=2)
