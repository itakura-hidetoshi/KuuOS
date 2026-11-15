from __future__ import annotations
import copy
from pathlib import Path
import tempfile
import unittest

from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import (
    append_cases, cases_from_portfolio, classify_error, git_blob,
    make_case, query_cases, read_journal, route_candidates, validate_case,
)
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import (
    read_observation_seed, checked_independent_pointers,
)

SEED=Path(__file__).resolve().parents[1] / (
    "memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v1.json")
HEAD="aafeb59d31937fc87a7e946d704962da7ae12a6c"
TREE="fe49b206e86ce03216c8bfb6b227811b08ac5866"
PRIOR="d6a8a8e2136c1a5601fa01c02f5f478fdd827520"

class TestLeanCodeAIMemoryOS(unittest.TestCase):
    def test_actual_observation_seed_is_non_authoritative(self):
        records=read_observation_seed(SEED)
        self.assertEqual(len(records),9)
        self.assertTrue(all(c["causal_status"]=="UNVERIFIED_HYPOTHESIS" for c in records))
        self.assertTrue(any(c["outcome"]=="DIRECT_LEAN_SUCCESS" for c in records))
        self.assertTrue(any(c["outcome"]=="DIRECT_LEAN_FAILURE" for c in records))
        pointers=checked_independent_pointers(SEED)
        self.assertEqual(len(pointers),2)
        self.assertTrue(all(not x["grant_proof_authority"] for x in pointers))

    def test_typed_error_taxonomy_from_real_lean_messages(self):
        expected={
            "error(lean.invalidField): Invalid field strictLabel":"API_FIELD_RESOLUTION",
            "error: Expected type must not contain free variables":"DEPENDENT_PROOF_ELABORATION",
            "error: omega could not prove the goal":"TACTIC_NONLINEAR_OR_UNAVAILABLE_HYPOTHESIS",
            "error: This simp argument is unused:":"UNUSED_SIMP_ARGUMENT",
            "error: unsolved goals":"UNRESOLVED_GOAL",
            "error: Application type mismatch: The argument":"APPLICATION_TYPE_MISMATCH",
        }
        for src,out in expected.items():
            self.assertEqual(classify_error("formal/KUOS/a.lean:22:5: "+src)["family"],out)
        d=classify_error("formal/KUOS/a.lean:22:5: error: unsolved goals")
        self.assertEqual(d["causal_status"],"UNVERIFIED_HYPOTHESIS")

    def test_exact_same_source_failed_candidate_not_replayed(self):
        s="theorem x : True := by trivial\n"
        candidate=git_blob(s)
        c=make_case(source_head=HEAD,source_tree=TREE,imported_blob=PRIOR,
                    candidate_blob=candidate,variant="previous-failed",
                    producer_run=123456,outcome="DIRECT_LEAN_FAILURE",
                    errors=["a.lean:1:1: error: unsolved goals"])
        payload={"repeat":s,"new":"theorem y : True := by trivial\n"}
        out,hints=route_candidates(payload,[c],source_head=HEAD,source_tree=TREE,imported_blob=PRIOR)
        self.assertNotIn("repeat",out)
        self.assertIn("new",out)
        self.assertEqual(len(hints["quarantined"]),1)
        self.assertFalse(hints["selects_proof"])

    def test_analog_not_auto_refused(self):
        s="theorem x : True := by trivial\n"
        case=make_case(source_head=HEAD,source_tree=TREE,imported_blob=PRIOR,
             candidate_blob=git_blob(s),variant="red",producer_run=123456,
             outcome="DIRECT_LEAN_FAILURE",errors=["a.lean:1:1: error: unsolved goals"])
        for variant in [
            {"source_head":"0"*40,"source_tree":TREE,"imported_blob":PRIOR},
            {"source_head":HEAD,"source_tree":"0"*40,"imported_blob":PRIOR},
            {"source_head":HEAD,"source_tree":TREE,"imported_blob":"0"*40},
        ]:
            result,advice=route_candidates({"candidate":s},[case],**variant)
            self.assertEqual(list(result),["candidate"])
            self.assertEqual(advice["quarantined"],[])
        report=query_cases([case],source_head=HEAD,source_tree=TREE,
                           imported_blob=PRIOR,mathlib_rev="0"*40)
        self.assertEqual(len(report["excluded"]),1)

    def test_append_only_memoryos_journal_and_tamper_detection(self):
        cases=read_observation_seed(SEED)[:3]
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"journal.jsonl"
            one=append_cases(p,cases)
            self.assertEqual(one["appended"],3)
            self.assertEqual(one["total"],3)
            self.assertEqual(append_cases(p,cases)["appended"],0)
            events=read_journal(p)
            self.assertEqual(len(events),3)
            self.assertTrue(all(x["authority"]=="external_pointer_only" for x in events))
            text=p.read_text()
            p.write_text(text.replace("external_pointer_only","execution_authority",1))
            with self.assertRaises(ValueError):
                read_journal(p)

    def test_case_id_cannot_be_relabelled(self):
        c=read_observation_seed(SEED)[0]
        wrong=copy.deepcopy(c)
        wrong["outcome"]="LOCAL_MCP_SUCCESS"
        with self.assertRaises(ValueError):
            validate_case(wrong)
        with self.assertRaises(ValueError):
            make_case(source_head=HEAD,source_tree=TREE,imported_blob=PRIOR,
              candidate_blob="not_a_sha",variant="x",producer_run=1,
              outcome="DIRECT_LEAN_SUCCESS",errors=[])

    def test_no_direct_proof_to_mcp_or_ci(self):
        portfolio={"source_head":HEAD,"source_tree":TREE,
                   "imported_v1103_blob":PRIOR,"source_restored":True,
                   "git_write_performed":False,"independent_ci_certified":False,
                   "candidate_count":1,
                   "candidates":[{"variant":"red","candidate_blob":"1"*40,
                   "status":"FAILURE","exit_code":1,"olean_exists":False,
                   "error_count":1,"errors":["a.lean:1:1: error: unsolved goals"]}]}
        mcp={"source_head":HEAD,"candidate_count":1,
             "mcp_success":False,"direct_lean_green":[]}
        cases=cases_from_portfolio(portfolio,mcp,123456)
        self.assertEqual(cases[0]["outcome"],"DIRECT_LEAN_FAILURE")
        self.assertIsNone(cases[0]["independent_run"])
        self.assertFalse(cases[0]["mcp_receipt"])
        mcp["selected"]="red"
        with self.assertRaises(ValueError):
            cases_from_portfolio(portfolio,mcp,123456)

    def test_no_secret_in_diagnostic(self):
        d=classify_error("a.lean:1:2: error: sk-123456789012345678901234")
        self.assertNotIn("sk-12345",d["message"])
        self.assertIn("[REDACTED]",d["message"])

if __name__=="__main__":
    unittest.main()
