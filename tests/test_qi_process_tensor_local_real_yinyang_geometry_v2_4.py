from __future__ import annotations

import unittest
from copy import deepcopy

from runtime.kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4 import (
    build_local_real_yinyang_geometry_receipt,
    compose_conversion_parity,
    validate_local_real_yinyang_geometry_receipt,
)


class QiProcessTensorLocalRealYinYangGeometryV24Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.qi = {
            "cycle_id": "local-real-test-cycle",
            "process_tensor_visible": True,
            "transition_continuity_visible": True,
            "memory_continuity_visible": True,
            "nonmarkov_memory_visible": True,
            "qi_process_tensor_receipt_digest": "qi-process-test-digest",
        }
        self.frames = [
            {
                "context_id": "source-context",
                "conjugation_involutive": True,
                "gauge_local": True,
                "absolute_global_polarity_claim": False,
            },
            {
                "context_id": "target-context",
                "conjugation_involutive": True,
                "gauge_local": True,
                "absolute_global_polarity_claim": False,
            },
        ]
        self.transports = [
            {
                "source_context": "source-context",
                "target_context": "memory-context",
                "real_structure_compatible": False,
                "conversion_visible": True,
                "memory_link_visible": True,
                "holonomy_residue_visible": True,
            },
            {
                "source_context": "memory-context",
                "target_context": "target-context",
                "real_structure_compatible": False,
                "conversion_visible": True,
                "memory_link_visible": True,
                "holonomy_residue_visible": True,
            },
        ]

    def build(self, **kwargs: object) -> dict[str, object]:
        options: dict[str, object] = {
            "qi_intensity": 3,
            "qi_capacity": 5,
            "recoverability_gap_candidate": 0.25,
            "protected_history_visible": True,
            "two_truths_gap": True,
            "context_allows_candidate_flow": True,
        }
        options.update(kwargs)
        return build_local_real_yinyang_geometry_receipt(
            self.qi,
            self.frames,
            self.transports,
            **options,
        )

    def test_double_conversion_restores_readout_parity_without_erasing_history(self) -> None:
        receipt = self.build()
        history = receipt["history_transport_surface"]
        self.assertEqual(history["conversion_count"], 2)
        self.assertEqual(history["conversion_parity"], "even")
        self.assertEqual(history["composed_polarity_action"], "preserve")
        self.assertTrue(history["history_residue_is_not_erased_by_even_parity"])
        self.assertEqual(compose_conversion_parity("convert", "convert"), "preserve")

    def test_odd_conversion_requires_polarity_aware_readout(self) -> None:
        receipt = build_local_real_yinyang_geometry_receipt(
            self.qi,
            self.frames,
            self.transports[:1],
            qi_intensity=2,
            qi_capacity=4,
            recoverability_gap_candidate=0.1,
        )
        self.assertEqual(
            receipt["disposition"],
            "ODD_LOCAL_REAL_CONVERSION_REQUIRES_POLARITY_AWARE_READOUT",
        )
        self.assertEqual(receipt["history_transport_surface"]["conversion_parity"], "odd")

    def test_saturation_splits_admitted_and_held_qi_without_erasure(self) -> None:
        receipt = self.build(qi_intensity=8, qi_capacity=5)
        split = receipt["qi_split_surface"]
        self.assertEqual(split["admitted_qi_intensity"], 5)
        self.assertEqual(split["held_qi_residue"], 3)
        self.assertEqual(
            split["admitted_qi_intensity"] + split["held_qi_residue"],
            split["qi_intensity"],
        )
        self.assertEqual(
            receipt["disposition"],
            "YANG_SATURATION_SPLITS_ADMITTED_AND_HELD_QI",
        )

    def test_boundary_loss_holds_all_qi(self) -> None:
        receipt = self.build(two_truths_gap=False)
        self.assertFalse(receipt["candidate_flow_admissible"])
        self.assertEqual(receipt["admitted_qi_intensity"], 0)
        self.assertEqual(receipt["held_qi_residue"], 3)
        self.assertEqual(receipt["disposition"], "FAIL_CLOSED_ON_TWO_TRUTHS_GAP_LOSS")

    def test_global_absolute_polarity_claim_fails_closed(self) -> None:
        frames = deepcopy(self.frames)
        frames[0]["absolute_global_polarity_claim"] = True
        receipt = build_local_real_yinyang_geometry_receipt(
            self.qi,
            frames,
            self.transports,
            qi_intensity=2,
            qi_capacity=5,
        )
        self.assertFalse(receipt["candidate_flow_admissible"])
        self.assertEqual(
            receipt["disposition"],
            "FAIL_CLOSED_ON_GLOBAL_ABSOLUTE_POLARITY_CLAIM",
        )

    def test_recoverability_gap_is_candidate_not_mass_theorem(self) -> None:
        receipt = self.build()
        recovery = receipt["recoverability_surface"]
        self.assertTrue(recovery["recoverability_gap_candidate_visible"])
        self.assertTrue(recovery["recoverability_gap_is_not_physical_mass_theorem"])
        self.assertTrue(recovery["protected_history_not_targeted_for_decay"])

    def test_receipt_validates_and_grants_no_authority(self) -> None:
        receipt = self.build()
        self.assertEqual(validate_local_real_yinyang_geometry_receipt(self.qi, receipt), [])
        self.assertTrue(all(value is False for value in receipt["non_authority"].values()))

    def test_digest_tamper_is_detected(self) -> None:
        receipt = self.build()
        receipt["held_qi_residue"] = 999
        errors = validate_local_real_yinyang_geometry_receipt(self.qi, receipt)
        self.assertIn("receipt_digest_invalid", errors)
        self.assertIn("held_qi_residue_invalid", errors)


if __name__ == "__main__":
    unittest.main()
