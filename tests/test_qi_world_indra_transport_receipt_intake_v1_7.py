from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_indra_transport_receipt_intake_scenarios_v1_7 import (
    run_indra_transport_receipt_intake_scenarios,
)
from runtime.kuuos_qi_world_indra_transport_receipt_intake_v1_7 import (
    build_fixture_indra_transport_receipt_intake,
    validate_indra_transport_receipt_intake,
)


class QiWorldIndraTransportReceiptIntakeV17Tests(unittest.TestCase):
    def test_fixture_receipt_set_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-indra-intake-test-") as temporary:
            intake = build_fixture_indra_transport_receipt_intake(Path(temporary))
            self.assertEqual(validate_indra_transport_receipt_intake(intake), [])
            self.assertEqual(len(intake["external_receipts"]), 7)
            self.assertTrue(intake["semantic_review_required"])
            self.assertFalse(intake["runtime_transport_realized"])

    def test_negative_scenarios(self) -> None:
        result = run_indra_transport_receipt_intake_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_INDRA_RECEIPT_INTAKE_V1_7_OK",
        )


if __name__ == "__main__":
    unittest.main()
