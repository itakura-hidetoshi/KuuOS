from __future__ import annotations

import unittest

from runtime.kuuos_qi_world_adaptive_trace_adapter_v1_1 import (
    build_adaptive_trace_adapter_receipt,
    validate_adaptive_trace_adapter_receipt,
)
from runtime.kuuos_qi_world_adaptive_trace_scenarios_v1_1 import (
    run_adaptive_trace_adapter_scenarios,
)


class QiWorldAdaptiveTraceAdapterV11Tests(unittest.TestCase):
    def test_nominal_adapter_receipt_validates(self) -> None:
        receipt = build_adaptive_trace_adapter_receipt(label="unittest")
        self.assertEqual(validate_adaptive_trace_adapter_receipt(receipt), [])
        self.assertEqual(len(receipt["adaptive_trace"]["events"]), 10)
        self.assertEqual(len(receipt["adaptive_trace"]["states"]), 11)
        self.assertEqual(
            set(receipt["qi_world_os_interface_receipt"]["os_packets"]),
            {
                "BeliefOS",
                "DecisionOS",
                "PlanOS",
                "ActOS",
                "ObserveOS",
                "VerifyOS",
                "LearnOS",
                "Governance",
            },
        )

    def test_negative_scenarios(self) -> None:
        result = run_adaptive_trace_adapter_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_ADAPTIVE_TRACE_ADAPTER_V1_1_OK",
        )


if __name__ == "__main__":
    unittest.main()
