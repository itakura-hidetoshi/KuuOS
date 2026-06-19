from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_native_generational_replan_v1_4 import (
    build_native_generational_replan_receipt,
    validate_native_generational_replan_receipt,
)
from runtime.kuuos_qi_world_native_generational_replan_scenarios_v1_4 import (
    run_native_generational_replan_scenarios,
)


class QiWorldNativeGenerationalReplanV14Tests(unittest.TestCase):
    def test_native_generational_replan_validates(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-native-generational-test-"
        ) as temporary:
            receipt = build_native_generational_replan_receipt(Path(temporary))
            self.assertEqual(
                validate_native_generational_replan_receipt(receipt), []
            )
            replan = receipt["native_replan_artifacts"]["PlanOSReplan"]
            decision = receipt["native_replan_artifacts"]["DecisionOS"]
            self.assertEqual(
                receipt["target_generation"],
                receipt["source_generation"] + 1,
            )
            self.assertEqual(
                replan["selected_candidate_id"],
                decision["selected_option_id"],
            )
            self.assertTrue(replan["next_plan_basis_committed"])
            self.assertFalse(replan["active_now"])
            self.assertFalse(replan["host_license_granted"])
            self.assertTrue(receipt["world_projection_read_only"])
            self.assertFalse(receipt["exact_world_updated"])

    def test_substitution_and_boundary_scenarios(self) -> None:
        result = run_native_generational_replan_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_NATIVE_GENERATIONAL_REPLAN_V1_4_OK",
        )
        self.assertTrue(result["future_only"])
        self.assertFalse(result["active_now"])


if __name__ == "__main__":
    unittest.main()
