from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_native_full_cycle_scenarios_v1_3 import (
    run_native_full_cycle_scenarios,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt,
    validate_native_full_cycle_receipt,
)


class QiWorldNativeFullCycleV13Tests(unittest.TestCase):
    def test_native_full_cycle_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-native-full-cycle-test-") as temporary:
            receipt = build_native_full_cycle_receipt(Path(temporary))
            self.assertEqual(validate_native_full_cycle_receipt(receipt), [])
            self.assertEqual(len(receipt["native_artifacts"]), 9)
            self.assertEqual(
                set(receipt["qi_world_os_interface_receipt"]["os_packets"]),
                {
                    "BeliefOS",
                    "DecisionOS",
                    "PlanOS",
                    "Governance",
                    "ActOS",
                    "ObserveOS",
                    "VerifyOS",
                    "LearnOS",
                },
            )

    def test_negative_scenarios(self) -> None:
        result = run_native_full_cycle_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_NATIVE_FULL_CYCLE_V1_3_OK",
        )


if __name__ == "__main__":
    unittest.main()
