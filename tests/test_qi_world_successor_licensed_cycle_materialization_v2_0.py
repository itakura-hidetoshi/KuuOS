from __future__ import annotations

import unittest

from runtime.kuuos_qi_world_successor_licensed_cycle_materialization_scenarios_v2_0 import (
    run_successor_licensed_cycle_materialization_scenarios,
)


class SuccessorLicensedCycleMaterializationV20Test(unittest.TestCase):
    def test_digest_linked_second_cycle(self) -> None:
        result = run_successor_licensed_cycle_materialization_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_SUCCESSOR_LICENSED_CYCLE_MATERIALIZATION_V2_0_OK",
        )
        self.assertEqual(result["cycle_count"], 2)
        self.assertTrue(result["authority_packets_distinct"])
        self.assertTrue(result["human_approvals_distinct"])
        self.assertTrue(result["host_licenses_distinct"])
        self.assertTrue(result["all_cycles_closed"])
        self.assertTrue(result["all_blockers_active"])
        self.assertFalse(result["next_act_started"])


if __name__ == "__main__":
    unittest.main()
