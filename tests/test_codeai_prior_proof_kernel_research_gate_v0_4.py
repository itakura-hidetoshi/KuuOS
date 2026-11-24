"""Kernel-memory research admission fixtures; no external model invocation."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import load_packet, PACKET_DIGEST
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from runtime.kuuos_codeai_prior_proof_kernel_research_gate_v0_4 import (
    kernel_context_text, build_kernel_memory_research_synthesis)
ROOT = Path(__file__).resolve().parents[1]
MOD = "runtime.kuuos_codeai_prior_proof_kernel_research_gate_v0_4"


class KernelResearchGateTests(unittest.TestCase):
    def setUp(self):
        packet = load_packet(ROOT)
        row = packet["observations"][0]
        self.id = row["lexical_id"]
        self.path = row["path"]
        self.obs = {"source_head":"a"*40,"source_tree":"b"*40,"scope":"canonical_main"}
        self.lex = {"query":"C60 gauge slot injective","terms":["c60","gauge","slot","injective"],
                    "mode":"all","limit":100,"receipt_digest":"c"*64,"status":"REVIEW_REQUIRED"}
        self.match = {"lexical_id":self.id,"historical_source_head":packet["source_head"],
                      "historical_run_id":packet["provenance"]["run_id"],
                      "status":"HISTORICAL_KERNEL_OBSERVATION_SOURCE_SCOPE_MATCH","observation":row}
        self.receipt = {"source_head":self.obs["source_head"],"source_tree":self.obs["source_tree"],
                        "historical_packet_digest":PACKET_DIGEST,"lexical_receipt":self.lex,
                        "matched_observations":[self.match],"without_kernel_observation":["d"*64],
                        "stale_observations":[],"scope_issues":[],"status":"REVIEW_REQUIRED"}
        self.receipt["receipt_digest"]=digest(self.receipt)
        self.review={"request":"new","kernel_receipt_digest":self.receipt["receipt_digest"],
                     "library_receipt_digest":self.lex["receipt_digest"],
                     "library_comparisons":[{"id":self.id,"relation":"prerequisite"}],
                     "kernel_comparisons":[{"id":self.id,"relation":"prerequisite",
                           "observation_digest":digest(self.match),
                           "type_expr_sha256":row["type_expr_sha256"],
                           "type_assumptions_comparison":"synthetic reviewed assumptions",
                           "type_conclusion_comparison":"synthetic reviewed conclusion",
                           "proof_reference_review":"synthetic reviewed proof references"}],
                     "unobserved_kernel_hit_ids":["d"*64]}
        self.context={self.path:(ROOT/self.path).read_text(encoding="utf-8")}
        self.req={"intent_text":"synthetic residual target\n"+kernel_context_text(self.receipt)}
        self.review["synthesis_request_binding"]=digest(self.req)

    def run_gate(self, fresh=None):
        with patch(MOD+".recall_kernel_memory",return_value=self.receipt if fresh is None else fresh), \
             patch(MOD+".build_library_research_synthesis",
                   return_value={"status":"fixture downstream","synthesis":"fixture only"}) as downstream:
            result=build_kernel_memory_research_synthesis(
                root=ROOT, observation=self.obs, kernel_receipt=self.receipt,
                mathematical_review=self.review, recall_receipt={}, synthesis_request=self.req,
                repository_files=self.context)
            return result, downstream

    def test_only_reviewed_observation_forwards_all_original_gates(self):
        result, downstream=self.run_gate()
        self.assertEqual(result["status"],"fixture downstream")
        self.assertEqual(downstream.call_count,1)
        self.assertEqual(downstream.call_args.kwargs["library_receipt"],self.lex)
        self.assertIn(kernel_context_text(self.receipt),
                      downstream.call_args.kwargs["synthesis_request"]["intent_text"])
        self.assertFalse(result["kernel_review"]["proof_authority"])

    def test_duplicate_new_result_blocks_before_any_downstream(self):
        self.review["kernel_comparisons"][0]["relation"]="equivalent"
        self.review["library_comparisons"][0]["relation"]="equivalent"
        result, downstream=self.run_gate()
        self.assertEqual(result["kernel_review"]["status"],"HOLD_DUPLICATE_REUSE_REQUIRED")
        downstream.assert_not_called()

    def test_missing_or_mismatched_observation_review_holds(self):
        self.review["kernel_comparisons"][0]["type_expr_sha256"]="e"*64
        result, downstream=self.run_gate()
        self.assertEqual(result["status"],"HOLD_RESEARCH_RECALL")
        downstream.assert_not_called()
        self.review["kernel_comparisons"]=[]
        result, downstream=self.run_gate()
        self.assertIn("unreviewed_kernel_observations",result["kernel_review"]["issues"])
        downstream.assert_not_called()

    def test_stale_fresh_receipt_and_noncanonical_scope_hold(self):
        fresh=copy.deepcopy(self.receipt)
        fresh["stale_observations"]=[{"lexical_id":self.id}]
        fresh["status"]="HOLD_REOBSERVE_KERNEL"
        result, downstream=self.run_gate(fresh)
        self.assertIn("stale_or_unbound_kernel_memory",result["kernel_review"]["issues"])
        downstream.assert_not_called()
        self.obs["scope"]="research_head"
        result, downstream=self.run_gate()
        self.assertIn("noncanonical_kernel_research_scope",result["kernel_review"]["issues"])
        downstream.assert_not_called()

    def test_original_source_and_provider_intent_required(self):
        self.context[self.path]+="\n-- invented context"
        self.req["intent_text"]="synthetic residual target"
        self.review["synthesis_request_binding"]=digest(self.req)
        result, downstream=self.run_gate()
        self.assertIn("historical_kernel_context_missing_from_provider_intent",
                      result["kernel_review"]["issues"])
        self.assertIn("kernel_source_context_mismatch:"+self.path,result["kernel_review"]["issues"])
        downstream.assert_not_called()

    def test_unobserved_hits_must_remain_explicit(self):
        self.review["unobserved_kernel_hit_ids"]=[]
        result, downstream=self.run_gate()
        self.assertIn("unobserved_kernel_scope_not_acknowledged",result["kernel_review"]["issues"])
        downstream.assert_not_called()


class KernelResearchRoutingTests(unittest.TestCase):
    def test_registered_scope_and_first_registration_preserve_guards(self):
        from scripts.select_impacted_checks import load_registry, select
        registry=load_registry(ROOT/"ci/check_registry.yaml")
        fragment="ci/check_registry.d/codeai_prior_proof_kernel_memory_v0_4.json"
        cid="codeai-prior-proof-kernel-memory-v04"
        paths=registry["checks"][cid]["paths"]
        focused=select(registry,[p for p in paths if p!=fragment],None)
        self.assertEqual(focused["unknown_paths"],[])
        self.assertEqual(focused["unmapped_paths"],[])
        self.assertFalse(focused["lean_required"])
        self.assertFalse(focused["full_audit_required"])
        selected={r["id"] for r in focused["selected_checks"]}
        self.assertTrue({cid,"codeai-prior-proof-library-v03","codeai-prior-proof-recall-v02"}.issubset(selected))
        first=select(registry,paths,None)
        self.assertTrue(first["full_audit_required"])
        self.assertTrue(first["lean_required"])
        self.assertIn(fragment,first["full_audit_trigger_paths"])
        with patch("scripts.select_impacted_checks.select_lean_targets",
                   return_value=(["KuuOSFormal"],"synthetic Lean change")):
            self.assertTrue(select(registry,paths+["formal/Kuu/Actual.lean"],None)["lean_required"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
