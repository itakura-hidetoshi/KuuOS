from __future__ import annotations
from pathlib import Path
import unittest

from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import query_cases, route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT / "memoryos/external/github/2026/11"
ROUND4_SOURCE="5c99d0ab97747576d3c2bdd2ee6286b56b0a30c5"
ROUND4_TREE="ed6d8a31fcab9fd07259474e465b84b7838de228"
PRIOR="d6a8a8e2136c1a5601fa01c02f5f478fdd827520"

class MemoryOSAdditiveObservationsV02(unittest.TestCase):
    def test_curated_base_and_later_run_are_both_retained(self):
        cases=read_observation_directory(DATA)
        self.assertEqual(len(cases),12)
        self.assertEqual(len(set(x["id"] for x in cases)),12)
        self.assertEqual(
          len([x for x in cases if x["producer_run"]==43691506747]),3)
        self.assertTrue(all(x["causal_status"]=="UNVERIFIED_HYPOTHESIS" for x in cases))

    def test_new_success_is_direct_only_not_independent_certified(self):
        cases=read_observation_directory(DATA)
        green=[c for c in cases if c["candidate_blob"]=="27cf21597fed1650c26cb64e31d63d469e01f4b5"]
        self.assertEqual(len(green),1)
        self.assertEqual(green[0]["outcome"],"DIRECT_LEAN_SUCCESS")
        self.assertIsNone(green[0]["independent_run"])
        self.assertIsNone(green[0]["mcp_receipt"])

    def test_cross_head_analogy_no_automatic_proof_or_rejection(self):
        cases=read_observation_directory(DATA)
        q=query_cases(cases,source_head=ROUND4_SOURCE,source_tree=ROUND4_TREE,
                      imported_blob=PRIOR)
        self.assertEqual(len(q["exact_cases"]),3)
        analog=query_cases(cases,source_head="0"*40,source_tree=ROUND4_TREE,
                           imported_blob=PRIOR)
        self.assertEqual(len(analog["exact_cases"]),0)
        self.assertFalse(analog["history_is_proof"])
        self.assertFalse(analog["memory_grants_execution"])

if __name__=="__main__":
    unittest.main()
