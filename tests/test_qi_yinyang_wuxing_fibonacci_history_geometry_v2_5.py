from __future__ import annotations

from copy import deepcopy
import math
import unittest

from runtime.kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5 import (
    NON_AUTHORITY,
    advance_history,
    advance_phase_history,
    build_yinyang_wuxing_fibonacci_history_receipt,
    golden_ratio,
    validate_yinyang_wuxing_fibonacci_history_receipt,
)


def dependency_receipt() -> dict:
    return {
        "version": "kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4",
        "local_real_yinyang_receipt_digest": "dependency-digest",
        "process_tensor_surface": {"process_support_visible": True},
        "local_real_structure_surface": {
            "all_frames_involutive": True,
            "all_frames_gauge_local": True,
            "absolute_global_polarity_claim": False,
        },
        "recoverability_surface": {
            "protected_history_visible": True,
            "two_truths_gap": True,
        },
        "non_authority": {
            "grants_execution_authority": False,
            "grants_truth_authority": False,
        },
    }


class WuxingFibonacciHistoryGeometryV25Tests(unittest.TestCase):
    def test_fusion_step(self) -> None:
        self.assertEqual(advance_history(1, 0), (0, 1))
        self.assertEqual(advance_history(0, 1), (1, 1))
        self.assertEqual(advance_history(1, 1), (1, 2))

    def test_five_phase_return_and_fibonacci_history_advance(self) -> None:
        projection = advance_phase_history(
            initial_phase_index=2,
            resolved_channels=1,
            active_channels=0,
            steps=5,
        )
        self.assertEqual(projection["final_phase_index"], 2)
        self.assertEqual(projection["final_resolved_channels"], 3)
        self.assertEqual(projection["final_active_channels"], 5)
        self.assertEqual(len(projection["trajectory"]), 6)

    def test_ten_steps_preserve_phase_period_but_not_history(self) -> None:
        projection = advance_phase_history(
            initial_phase_index=4,
            resolved_channels=1,
            active_channels=0,
            steps=10,
        )
        self.assertEqual(projection["final_phase_index"], 4)
        self.assertEqual(
            (
                projection["final_resolved_channels"],
                projection["final_active_channels"],
            ),
            (34, 55),
        )

    def test_canonical_receipt(self) -> None:
        receipt = build_yinyang_wuxing_fibonacci_history_receipt(
            dependency_receipt(),
            initial_phase_index=0,
            steps=5,
            resolved_channels=1,
            active_channels=0,
        )
        self.assertEqual(
            receipt["disposition"],
            "FIVE_PHASE_BASE_RETURNS_WITH_FIBONACCI_HISTORY_ADVANCE",
        )
        self.assertTrue(receipt["projection_admissible"])
        self.assertTrue(
            receipt["five_phase_base_surface"]["phase_returned"]
        )
        self.assertFalse(
            receipt["fibonacci_history_fibre_surface"]["history_returned"]
        )
        self.assertTrue(
            receipt["fibonacci_history_fibre_surface"]
            ["five_step_fusion_identity_visible"]
        )
        self.assertTrue(
            receipt["golden_ratio_growth_surface"]["dimension_scaling_verified"]
        )
        self.assertAlmostEqual(
            receipt["golden_ratio_growth_surface"]["final_history_dimension"],
            golden_ratio() ** 5,
            places=12,
        )
        self.assertEqual(
            validate_yinyang_wuxing_fibonacci_history_receipt(
                dependency_receipt(), receipt
            ),
            [],
        )

    def test_dependency_gap_holds_projection(self) -> None:
        dependency = dependency_receipt()
        dependency["process_tensor_surface"]["process_support_visible"] = False
        receipt = build_yinyang_wuxing_fibonacci_history_receipt(dependency)
        self.assertFalse(receipt["projection_admissible"])
        self.assertEqual(
            receipt["disposition"],
            "YIN_HOLDS_ON_V2_4_LOCAL_REAL_DEPENDENCY_GAP",
        )

    def test_boundary_gap_holds_projection_without_erasing_history(self) -> None:
        receipt = build_yinyang_wuxing_fibonacci_history_receipt(
            dependency_receipt(),
            preserve_two_truths_gap=False,
        )
        self.assertFalse(receipt["projection_admissible"])
        projection = receipt["fibonacci_history_fibre_surface"]["projection"]
        self.assertEqual(
            (projection["final_resolved_channels"], projection["final_active_channels"]),
            (3, 5),
        )

    def test_context_hold(self) -> None:
        receipt = build_yinyang_wuxing_fibonacci_history_receipt(
            dependency_receipt(),
            context_allows_projection=False,
        )
        self.assertEqual(
            receipt["disposition"],
            "YIN_CONTEXT_HOLDS_WUXING_FIBONACCI_PROJECTION",
        )

    def test_non_authority_and_fixed_boundaries(self) -> None:
        receipt = build_yinyang_wuxing_fibonacci_history_receipt(
            dependency_receipt()
        )
        self.assertEqual(receipt["non_authority"], NON_AUTHORITY)
        self.assertTrue(all(value is False for value in NON_AUTHORITY.values()))
        self.assertTrue(
            receipt["categorical_surface"]
            ["classical_wuxing_not_identified_with_su2_3"]
        )
        self.assertTrue(
            receipt["categorical_surface"]["physical_anyon_realization_not_claimed"]
        )
        self.assertTrue(
            receipt["operational_surface"]["golden_ratio_is_not_a_clinical_threshold"]
        )
        self.assertGreater(
            receipt["golden_ratio_growth_surface"]["entropy_rate_per_step"],
            0.0,
        )
        self.assertTrue(
            math.isfinite(
                receipt["golden_ratio_growth_surface"]["entropy_rate_per_step"]
            )
        )

    def test_tamper_detection(self) -> None:
        receipt = build_yinyang_wuxing_fibonacci_history_receipt(
            dependency_receipt()
        )
        tampered = deepcopy(receipt)
        tampered["fibonacci_history_fibre_surface"]["projection"][
            "final_active_channels"
        ] = 999
        errors = validate_yinyang_wuxing_fibonacci_history_receipt(
            dependency_receipt(), tampered
        )
        self.assertIn("receipt_digest_invalid", errors)
        self.assertIn("fibonacci_history_fibre_surface_invalid", errors)


if __name__ == "__main__":
    unittest.main()
