from __future__ import annotations

import unittest

from runtime.kuuos_qi_healing_potential_diagnostic_scenarios_v0_28 import (
    run_qi_healing_potential_diagnostic_scenarios,
)


class QiProcessDiagnosticV028Tests(unittest.TestCase):
    def test_scenarios(self) -> None:
        result = run_qi_healing_potential_diagnostic_scenarios()
        self.assertEqual(
            "KUUOS_QI_HEALING_POTENTIAL_DIAGNOSTIC_V0_28_OK",
            result["status"],
        )
        self.assertEqual("REPLAYED", result["ledger_replay_status"])
        self.assertTrue(result["tamper_rejected"])
        self.assertTrue(result["plural_hypotheses_preserved"])
        self.assertTrue(result["severity_separate_from_healing_score"])


if __name__ == "__main__":
    unittest.main()
