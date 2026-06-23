from __future__ import annotations

import unittest
from copy import deepcopy

from runtime.kuuos_qi_world_cross_cycle_blocker_core_v1_5 import BLOCKER_ORDER
from runtime.kuuos_qi_world_yinyang_process_blocker_complementarity_v2_3 import (
    build_yinyang_process_blocker_receipt,
    relational_polarity,
    validate_yinyang_process_blocker_receipt,
)


class YinYangProcessBlockerComplementarityV23Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.qi = {
            "cycle_id": "test-cycle",
            "process_tensor_visible": True,
            "transition_continuity_visible": True,
            "memory_continuity_visible": True,
            "qi_process_tensor_receipt_digest": "qi-test-digest",
        }
        self.blockers = {
            "cycle_id": "test-cycle",
            "composed_blocker_vector": {name: True for name in BLOCKER_ORDER},
            "all_required_blockers_active": True,
            "blocker_certificate_digest": "blocker-test-digest",
        }

    def test_balanced_flow_preserves_intensity(self) -> None:
        receipt = build_yinyang_process_blocker_receipt(
            self.qi, self.blockers, qi_intensity=2, qi_capacity=3
        )
        self.assertTrue(receipt["candidate_flow_admissible"])
        self.assertEqual(receipt["effective_qi_intensity"], 2)
        self.assertEqual(
            validate_yinyang_process_blocker_receipt(self.qi, self.blockers, receipt),
            [],
        )

    def test_saturation_generates_containment(self) -> None:
        receipt = build_yinyang_process_blocker_receipt(
            self.qi, self.blockers, qi_intensity=4, qi_capacity=3
        )
        self.assertFalse(receipt["candidate_flow_admissible"])
        self.assertEqual(receipt["effective_qi_intensity"], 0)
        self.assertTrue(receipt["coupling"]["saturation_generates_yin_containment"])

    def test_boundary_loss_fails_closed(self) -> None:
        blockers = deepcopy(self.blockers)
        blockers["composed_blocker_vector"]["world_identity_blocker"] = False
        blockers["all_required_blockers_active"] = False
        receipt = build_yinyang_process_blocker_receipt(
            self.qi, blockers, qi_intensity=1, qi_capacity=3
        )
        self.assertEqual(receipt["disposition"], "YIN_FAIL_CLOSED_ON_BOUNDARY_LOSS")
        self.assertFalse(receipt["candidate_flow_admissible"])

    def test_polarity_is_relational(self) -> None:
        self.assertEqual(relational_polarity("contain"), "yin")
        self.assertEqual(relational_polarity("propagate"), "yang")
        self.assertEqual(relational_polarity("unknown"), "undetermined")

    def test_no_authority_is_created(self) -> None:
        receipt = build_yinyang_process_blocker_receipt(
            self.qi, self.blockers, qi_intensity=1, qi_capacity=3
        )
        self.assertTrue(all(value is False for value in receipt["non_authority"].values()))
        self.assertFalse(receipt["physics_boundary"]["claims_physics_theorem"])


if __name__ == "__main__":
    unittest.main()
