from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_indra_transport_request_v1_6 import (
    build_indra_transport_request_receipt,
    validate_indra_transport_request_receipt,
)
from runtime.kuuos_qi_world_indra_transport_request_scenarios_v1_6 import (
    run_indra_transport_request_scenarios,
)


class QiWorldIndraTransportRequestV16Tests(unittest.TestCase):
    def test_nominal_request_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-indra-v16-test-") as temporary:
            receipt = build_indra_transport_request_receipt(Path(temporary))
            self.assertEqual(validate_indra_transport_request_receipt(receipt), [])
            request = receipt["transport_request"]
            self.assertNotEqual(request["source_patch_id"], request["target_patch_id"])
            self.assertTrue(request["request_only"])
            self.assertFalse(request["transport_realized"])
            self.assertTrue(receipt["world_v042_sidecar_ready"])
            self.assertTrue(receipt["all_cross_cycle_blockers_active"])

    def test_negative_scenarios(self) -> None:
        result = run_indra_transport_request_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_INDRA_TRANSPORT_REQUEST_V1_6_OK",
        )


if __name__ == "__main__":
    unittest.main()
