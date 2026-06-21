from __future__ import annotations

import unittest

from runtime.kuuos_qi_window_trajectory_scenarios_v0_29 import run_qi_window_trajectory_scenarios


class QiWindowV029Tests(unittest.TestCase):
    def test_scenarios(self) -> None:
        result = run_qi_window_trajectory_scenarios()
        self.assertEqual("KUUOS_QI_WINDOW_TRAJECTORY_V0_29_OK", result["status"])
        self.assertEqual("WINDOW_OPENING", result["opening"])
        self.assertEqual("WINDOW_STABLE_VISIBLE", result["stable"])
        self.assertEqual("WINDOW_OSCILLATING", result["oscillating"])
        self.assertEqual("WINDOW_DORMANT_REOPENABLE", result["dormant"])
        self.assertEqual("WINDOW_CONSTRICTING", result["constricting"])
        self.assertEqual("REVIEW_HANDOFF", result["review"])
        self.assertEqual("INSUFFICIENT_HISTORY", result["insufficient"])
        self.assertGreater(result["reopening_memory"], 0.0)
        self.assertFalse(result["single_decline_closure"])
        self.assertFalse(result["irreversibility_claimed"])
        self.assertFalse(result["prognosis_claimed"])
        self.assertEqual("REPLAYED", result["ledger_replay"])
        self.assertTrue(result["tamper_rejected"])


if __name__ == "__main__":
    unittest.main()
