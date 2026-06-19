from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_cross_cycle_reentry_scenarios_v1_4 import (
    run_cross_cycle_reentry_scenarios,
)
from runtime.kuuos_qi_world_cross_cycle_reentry_v1_4 import (
    build_cross_cycle_reentry_receipt,
    validate_cross_cycle_reentry_receipt,
)


class QiWorldCrossCycleReentryV14Tests(unittest.TestCase):
    def test_cross_cycle_receipt_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-cross-cycle-test-") as temporary:
            receipt = build_cross_cycle_reentry_receipt(Path(temporary))
            self.assertEqual(validate_cross_cycle_reentry_receipt(receipt), [])
            previous = receipt["previous_cycle_receipt"]["native_artifacts"]
            next_artifacts = receipt["next_cycle_artifacts"]
            self.assertEqual(
                next_artifacts["BeliefOS"]["source_memory_digest"],
                previous["LearnOS"]["learn_state_digest"],
            )
            self.assertEqual(
                next_artifacts["BeliefActivation"]["next_plan_basis_digest"],
                previous["LearnOS"]["learning_delta_digest"],
            )
            self.assertEqual(
                next_artifacts["PlanOS"]["next_plan_basis_digest"],
                previous["LearnOS"]["learning_delta_digest"],
            )
            self.assertTrue(receipt["previous_cycle_immutable"])
            self.assertTrue(receipt["next_act_not_started"])

    def test_negative_scenarios(self) -> None:
        result = run_cross_cycle_reentry_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_CROSS_CYCLE_REENTRY_V1_4_OK",
        )
        self.assertEqual(
            result["next_plan_basis_digest"],
            result["previous_learning_delta_digest"],
        )


if __name__ == "__main__":
    unittest.main()
