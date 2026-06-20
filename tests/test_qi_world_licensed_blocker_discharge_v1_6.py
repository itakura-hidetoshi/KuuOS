from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_licensed_blocker_discharge_scenarios_v1_6 import (
    run_licensed_blocker_discharge_scenarios,
)
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_6 import (
    INVARIANT_BLOCKERS,
    RELEASABLE_BLOCKERS,
    build_licensed_act_handoff_receipt,
    validate_licensed_act_handoff_receipt,
)


class QiWorldLicensedBlockerDischargeV16Tests(unittest.TestCase):
    def test_licensed_handoff_validates(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-licensed-discharge-test-"
        ) as temporary:
            receipt = build_licensed_act_handoff_receipt(Path(temporary))
            self.assertEqual(validate_licensed_act_handoff_receipt(receipt), [])
            authority = receipt["external_authority_packet"]
            discharge = receipt["blocker_discharge_certificate"]
            self.assertEqual(
                authority["released_blockers"], list(RELEASABLE_BLOCKERS)
            )
            self.assertEqual(
                authority["retained_invariant_blockers"],
                list(INVARIANT_BLOCKERS),
            )
            self.assertTrue(discharge["all_invariant_blockers_retained"])
            self.assertTrue(receipt["target_act_started"])
            self.assertTrue(receipt["effect_recorded"])
            self.assertTrue(receipt["observation_required"])
            self.assertTrue(receipt["verification_required"])
            self.assertFalse(receipt["memory_overwritten"])
            self.assertFalse(receipt["exact_world_updated"])
            self.assertFalse(receipt["truth_promoted"])

    def test_authority_is_external_scoped_and_single_use(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-licensed-authority-test-"
        ) as temporary:
            receipt = build_licensed_act_handoff_receipt(Path(temporary))
            authority = receipt["external_authority_packet"]
            self.assertTrue(authority["external_issuer"])
            self.assertFalse(authority["self_issued"])
            self.assertTrue(authority["single_use"])
            self.assertTrue(authority["authority_does_not_widen_host_license"])
            self.assertEqual(receipt["release_consumption_count"], 1)
            self.assertTrue(receipt["source_cycle_immutable"])
            self.assertTrue(receipt["source_blocker_certificate_immutable"])

    def test_substitution_and_boundary_scenarios(self) -> None:
        result = run_licensed_blocker_discharge_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_LICENSED_BLOCKER_DISCHARGE_V1_6_OK",
        )
        self.assertEqual(result["release_consumption_count"], 1)
        self.assertTrue(result["effect_recorded"])
        self.assertTrue(result["observation_required"])
        self.assertTrue(result["verification_required"])
        self.assertTrue(result["source_cycle_immutable"])
        self.assertFalse(result["exact_world_updated"])
        self.assertFalse(result["truth_promoted"])


if __name__ == "__main__":
    unittest.main()
