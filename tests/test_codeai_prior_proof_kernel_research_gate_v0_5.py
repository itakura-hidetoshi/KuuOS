"""Kernel-memory research admission fixtures; no external model invocation."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import load_packet
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import COMBINED_DIGEST as PACKET_DIGEST, PACKET_DIGESTS
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from runtime.kuuos_codeai_prior_proof_kernel_research_gate_v0_5 import (
    kernel_context_text, build_kernel_memory_research_synthesis)
ROOT = Path(__file__).resolve().parents[1]
MOD = "runtime.kuuos_codeai_prior_proof_kernel_research_gate_v0_5"


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
                        "historical_packet_digest":PACKET_DIGEST,"historical_packet_digests":dict(PACKET_DIGESTS),"lexical_receipt":self.lex,
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


@unittest.skipUnless(__import__("os").environ.get("KUUOS_KERNEL_FIRST"),
                     "actual archived replay integration context not supplied")
class ActualProviderBoundaryReplayTests(unittest.TestCase):
    """Actual source retrieval and actual CodeAI stack; synthetic test-only intent.

    The current research branch is NOT canonical main. This test explicitly
    supplies a synthetic canonical-scope contract input to exercise the
    read-only call path, not an authenticated canonical observation. No
    production branch/scope rules are changed and no external model is called.
    The provider returns HOLD rather than a candidate. No novelty review is
    claimed for the synthetic fixture.
    """
    def test_real_original_kernel_receives_exact_historical_context_and_holds(self):
        import os
        from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import recall_kernel_memory
        from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import scan
        from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
            seal, SOURCE_RECEIPT_DIGEST_FIELD, POLICY_DIGEST_FIELD as CANDIDATE_POLICY_DIGEST_FIELD)
        from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
            ProviderAdapter, REQUEST_DIGEST_FIELD, BOUNDARY_HOLD)
        from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
        from tests.test_kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
            source_and_candidate_policy, request, policy, response)

        observed = github_observation(os.environ["GITHUB_SHA"], "research_head")
        self.assertEqual(observed["scope"], "research_head")
        # Synthetic canonical-contract label ONLY within this no-write,
        # no-external-provider test. The source head/tree remain actual.
        fixture_observation = dict(observed, scope="canonical_main")
        query = "sourceglobal overlapfaithful"
        receipt = recall_kernel_memory(ROOT, fixture_observation, query, limit=500)
        self.assertEqual(receipt["status"], "REVIEW_REQUIRED")
        self.assertEqual({r["historical_packet_version"] for r in receipt["matched_observations"]}, {"v0.4", "v0.5"})
        self.assertGreater(len(receipt["matched_observations"]), 2)
        self.assertFalse(receipt["proof_authority"])
        lexical = receipt["lexical_receipt"]
        legacy = scan(ROOT, observed["source_head"], [
            "sourceGlobal_iff_shadowGlobal_and_overlapFaithful",
            "no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal"])
        self.assertEqual(legacy["status"], "REVIEW_REQUIRED")
        target = "Fixture-only transport of an existing read-only context"
        assumptions = "Synthetic review contract, not a mathematical theorem"
        delta = "Exercise context propagation with no new proof"
        consumer = "Local deterministic HOLD callback"
        review = {
            "request": "bridge", "target": target, "assumptions": assumptions,
            "delta": delta, "consumer": consumer,
            "reviewer": "synthetic integration test only",
            "receipt_digest": legacy["receipt_digest"],
            "library_receipt_digest": lexical["receipt_digest"],
            "kernel_receipt_digest": receipt["receipt_digest"],
            "unobserved_kernel_hit_ids": receipt["without_kernel_observation"],
            "parse_gap_reviews": [
                {"path": g["path"], "blob": g["blob"],
                 "disposition": "reviewed_irrelevant", "reason": "fixture only"}
                for g in lexical["parse_gaps"]],
            "comparisons": [
                {"path": hit["path"], "blob": hit["blob"], "line": hit["matches"][0]["line"],
                 "declaration": "fixture context reference only", "relation": "prerequisite",
                 "reason": "synthetic test relation only, no mathematical comparison asserted"}
                for hit in legacy["hits"]],
            "library_comparisons": [
                {"id": hit["id"], "source_blob": hit["source_blob"],
                 "signature_digest": hit["signature_digest"], "relation": "prerequisite",
                 "reason": "synthetic test relation", "assumptions_comparison": "fixture only",
                 "conclusion_comparison": "fixture only"}
                for hit in lexical["hits"]],
            "kernel_comparisons": [
                {"id": match["lexical_id"], "relation": "prerequisite",
                 "observation_digest": digest(match),
                 "type_expr_sha256": match["observation"]["type_expr_sha256"],
                 "type_assumptions_comparison": "fixture only",
                 "type_conclusion_comparison": "fixture only",
                 "proof_reference_review": "fixture only"}
                for match in receipt["matched_observations"]],
        }
        paths = {h["path"] for h in lexical["hits"]} | {h["path"] for h in legacy["hits"]}
        files = {p: (ROOT / p).read_bytes().decode("utf-8") for p in sorted(paths)}
        text = "\n".join([target, assumptions, delta, consumer, kernel_context_text(receipt)])
        req = seal(dict(request(1), intent_text=text), REQUEST_DIGEST_FIELD)
        review["synthesis_request_binding"] = digest(req)
        source, candidate_policy = source_and_candidate_policy()
        source = seal(dict(source, source_commit_sha=observed["source_head"],
                           resulting_commit_sha=observed["source_head"],
                           tree_digest=observed["source_tree"],
                           observed_path_count=len(files), declared_path_count=len(files)),
                      SOURCE_RECEIPT_DIGEST_FIELD)
        candidate_policy = seal(dict(candidate_policy,
            expected_source_commit_sha=observed["source_head"],
            expected_source_observation_receipt_digest=source[SOURCE_RECEIPT_DIGEST_FIELD]),
            CANDIDATE_POLICY_DIGEST_FIELD)
        # Deliberately generous, fixture-only context limits. No operational
        # policies are relaxed. A deterministic provider must return HOLD.
        synthesis_policy = policy(
            allowed_provider_ids=["local_model"],
            allowed_repository_path_prefixes=["formal","lean"],
            maximum_provider_calls=1,
            maximum_proposals=1,
            maximum_intent_bytes=len(text.encode("utf-8"))+1024,
            maximum_repository_snapshot_bytes=len(
                __import__("json").dumps(files,ensure_ascii=False,sort_keys=True,
                    separators=(",",":")).encode("utf-8"))+1024)
        calls = []
        def local_hold(prompt):
            calls.append(prompt)
            return response(evidence_missing=True)
        kwargs = dict(root=ROOT, observation=fixture_observation,
                      kernel_receipt=receipt, mathematical_review=review,
                      recall_receipt=legacy, source_observation_receipt=source,
                      repository_files=files, synthesis_request=req,
                      provider_adapters=[ProviderAdapter("kernel-recall-fixture","local_model",
                                                        "deterministic-hold",local_hold)],
                      synthesis_policy=synthesis_policy,candidate_policy=candidate_policy)
        result = build_kernel_memory_research_synthesis(**kwargs)
        self.assertEqual(result["status"],"FORWARDED_TO_ORIGINAL_CODEAI",result)
        synthesis = result["synthesis"]
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0]["intent_text"],text)
        self.assertEqual(calls[0]["repository_files"],files)
        self.assertEqual(len(synthesis.attempts),1,synthesis.issues)
        self.assertEqual(synthesis.attempts[0].boundary_status,BOUNDARY_HOLD)
        self.assertEqual(len(synthesis.candidates),0)
        self.assertFalse(synthesis.receipt["repository_mutation_performed"])
        self.assertFalse(synthesis.receipt["execution_authority_granted"])
        # Same actual recall, but a duplicate marked NEW must not invoke
        # even this deterministic callback a second time.
        duplicate=copy.deepcopy(review)
        duplicate["request"]="new"
        i=duplicate["kernel_comparisons"][0]["id"]
        duplicate["kernel_comparisons"][0]["relation"]="equivalent"
        next(x for x in duplicate["library_comparisons"] if x["id"]==i)["relation"]="equivalent"
        blocked=build_kernel_memory_research_synthesis(**dict(kwargs,mathematical_review=duplicate))
        self.assertEqual(blocked["kernel_review"]["status"],"HOLD_DUPLICATE_REUSE_REQUIRED")
        self.assertEqual(len(calls),1)
        print("KUUOS_ACTUAL_CODEAI_V05_COMBINED_BOUNDARY_REPLAY",
              f"matched={len(receipt['matched_observations'])} provider_calls=1 candidate_count=0 duplicate_provider_calls=0",
              "synthetic_scope_contract=true external_model=false",flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
