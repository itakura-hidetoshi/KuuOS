from __future__ import annotations

import unittest

from runtime.kuuos_qi_candidate_lineage_scenarios_v0_29 import (
    run_candidate_lineage_scenarios,
)


class CandidateLineageV029Test(unittest.TestCase):
    def test_scenarios(self) -> None:
        result = run_candidate_lineage_scenarios()
        self.assertEqual(result["visible_route"], "HOLD")
        self.assertEqual(result["insufficient_route"], "REOBSERVE")
        self.assertEqual(result["review_route"], "REVIEW")
        self.assertEqual(result["terminated_route"], "TERMINATE")
        self.assertEqual(result["handover_route"], "HANDOVER")
        self.assertTrue(result["substitution_rejected"])
        self.assertTrue(result["tamper_rejected"])
        self.assertTrue(result["packet_reuse_rejected"])
        self.assertEqual(result["replay_status"], "REPLAYED")


if __name__ == "__main__":
    unittest.main()
