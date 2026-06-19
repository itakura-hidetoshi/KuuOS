from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt,
    validate_native_full_cycle_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_scenarios_v1_3 import (
    run_native_full_cycle_scenarios,
)


class QiWorldNativeFullCycleV13Tests(unittest.TestCase):
    def test_full_native_cycle_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-native-full-test-") as temporary:
            receipt = build_native_full_cycle_receipt(Path(temporary))
            self.assertEqual(validate_native_full_cycle_receipt(receipt), [])
            artifacts = receipt["native_artifacts"]
            self.assertEqual(
                artifacts["DecisionOS"]["source_belief_receipt_digest"],
                artifacts["BeliefOSReceipt"]["belief_gerbe_receipt_digest"],
            )
            self.assertEqual(
                artifacts["PlanOS"]["source_wa_state_digest"],
                artifacts["DecisionOSWa"]["wa_state_digest"],
            )
            self.assertEqual(
                artifacts["ActOS"]["source_plan_state_digest"],
                artifacts["PlanOS"]["plan_state_digest"],
            )
            self.assertEqual(
                artifacts["LearnOS"]["source_verify_state_digest"],
                artifacts["VerifyOS"]["verify_state_digest"],
            )

    def test_substitution_scenarios(self) -> None:
        result = run_native_full_cycle_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_NATIVE_FULL_CYCLE_V1_3_OK",
        )


if __name__ == "__main__":
    unittest.main()
