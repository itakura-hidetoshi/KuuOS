from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_native_evidence_loop_v1_2 import (
    build_native_evidence_loop_receipt,
    validate_native_evidence_loop_receipt,
)
from runtime.kuuos_qi_world_native_evidence_loop_scenarios_v1_2 import (
    run_native_evidence_loop_scenarios,
)


class QiWorldNativeEvidenceLoopV12Tests(unittest.TestCase):
    def test_native_receipt_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-native-loop-test-") as temporary:
            receipt = build_native_evidence_loop_receipt(Path(temporary))
            self.assertEqual(validate_native_evidence_loop_receipt(receipt), [])
            states = receipt["native_states"]
            self.assertEqual(
                states["ObserveOS"]["source_act_state_digest"],
                states["ActOS"]["act_state_digest"],
            )
            self.assertEqual(
                states["VerifyOS"]["source_observe_state_digest"],
                states["ObserveOS"]["observe_state_digest"],
            )
            self.assertEqual(
                states["LearnOS"]["source_verify_state_digest"],
                states["VerifyOS"]["verify_state_digest"],
            )

    def test_negative_scenarios(self) -> None:
        result = run_native_evidence_loop_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_NATIVE_EVIDENCE_LOOP_V1_2_OK",
        )


if __name__ == "__main__":
    unittest.main()
