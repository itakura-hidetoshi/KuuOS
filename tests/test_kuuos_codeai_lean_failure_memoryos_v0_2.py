from __future__ import annotations
from pathlib import Path
import unittest

from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import query_cases, route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed, checked_independent_pointers
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT / "memoryos/external/github/2026/11"
ROUND4_SOURCE="5c99d0ab97747576d3c2bdd2ee6286b56b0a30c5"
ROUND4_TREE="ed6d8a31fcab9fd07259474e465b84b7838de228"
PRIOR="d6a8a8e2136c1a5601fa01c02f5f478fdd827520"

class MemoryOSAdditiveObservationsV02(unittest.TestCase):
    def test_curated_base_and_later_run_are_both_retained(self):
        cases=read_observation_directory(DATA)
        prior_base=read_observation_seed(DATA/"kuuos_codeai_lean_observations_v1.json")
        prior_round4=read_observation_seed(DATA/"kuuos_codeai_lean_observations_round4_v1.json")
        added_v1107=read_observation_seed(DATA/"kuuos_codeai_lean_observations_v1107_v1.json")
        # Preserve the exact historical 12 cases; certify 5 new cases without
        # assuming the observation store cannot grow append-only.
        self.assertEqual(len(prior_base)+len(prior_round4),12)
        self.assertEqual(len(added_v1107),5)
        self.assertEqual(
          len([x for x in cases if x["producer_run"]==43693040574]),5)
        self.assertEqual(
          len(cases),sum(len(read_observation_seed(p)) for p in
             DATA.glob("kuuos_codeai_lean_observations*_v1.json")))
        self.assertEqual(len(set(x["id"] for x in cases)),len(cases))
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

    def test_v1107_actual_face_observations_never_grant_proof_authority(self):
        filename=DATA/"kuuos_codeai_lean_observations_v1107_v1.json"
        cases=read_observation_seed(filename)
        self.assertEqual(len(cases),5)
        self.assertEqual(sum(x["outcome"]=="DIRECT_LEAN_SUCCESS" for x in cases),4)
        self.assertEqual(sum(x["outcome"]=="DIRECT_LEAN_FAILURE" for x in cases),1)
        self.assertTrue(all(x["independent_run"] is None for x in cases))
        self.assertTrue(all(x["causal_status"]=="UNVERIFIED_HYPOTHESIS" for x in cases))
        ptrs=checked_independent_pointers(filename)
        self.assertEqual(len(ptrs),1)
        self.assertEqual(ptrs[0]["run_id"],43693479426)
        self.assertEqual(ptrs[0]["exact_source_blob"],
                         "37c3e75c5d74c74b8d125983c9cd257f9757995a")
        self.assertFalse(ptrs[0]["grant_proof_authority"])
        self.assertTrue(ptrs[0]["requires_external_completed_CI_reobservation"])

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
