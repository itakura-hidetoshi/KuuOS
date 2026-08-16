from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5 import (
    build_yinyang_wuxing_fibonacci_history_receipt,
)
from runtime.kuuos_qi_wuxing_generation_control_coherence_v2_6 import (
    NON_AUTHORITY,
    RELATIONS,
    apply_relation,
    apply_shift,
    build_wuxing_generation_control_coherence_receipt,
    classify_strength,
    compose_shifts,
    is_overacting_control,
    relation_shift,
    validate_wuxing_generation_control_coherence_receipt,
)


def v2_4_dependency_receipt() -> dict:
    return {
        "version": "kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4",
        "local_real_yinyang_receipt_digest": "v2-6-test-source-digest",
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


def v2_5_receipt() -> dict:
    return build_yinyang_wuxing_fibonacci_history_receipt(
        v2_4_dependency_receipt(),
        initial_phase_index=0,
        steps=5,
        resolved_channels=1,
        active_channels=0,
    )


class WuxingGenerationControlCoherenceV26Tests(unittest.TestCase):
    def test_relation_directions(self) -> None:
        self.assertEqual(RELATIONS["generation"], {"phase_delta": 1, "history_events": 1})
        self.assertEqual(RELATIONS["control"], {"phase_delta": 2, "history_events": 1})
        self.assertEqual(RELATIONS["insult"], {"phase_delta": -2, "history_events": 1})
        self.assertEqual(RELATIONS["mother"], {"phase_delta": -1, "history_events": 1})
        self.assertEqual(RELATIONS["child"], {"phase_delta": 1, "history_events": 1})

    def test_control_and_two_generations_share_phase_not_history(self) -> None:
        initial = {
            "phase_index": 0,
            "resolved_channels": 1,
            "active_channels": 0,
        }
        control = apply_relation("control", **initial)
        generation_once = apply_relation("generation", **initial)
        generation_twice = apply_relation("generation", **generation_once)
        self.assertEqual(control["phase_index"], generation_twice["phase_index"])
        self.assertEqual(
            (control["resolved_channels"], control["active_channels"]),
            (0, 1),
        )
        self.assertEqual(
            (generation_twice["resolved_channels"], generation_twice["active_channels"]),
            (1, 1),
        )
        self.assertNotEqual(
            (control["resolved_channels"], control["active_channels"]),
            (generation_twice["resolved_channels"], generation_twice["active_channels"]),
        )

    def test_control_insult_phase_inverse_preserves_history(self) -> None:
        initial = {
            "phase_index": 3,
            "resolved_channels": 1,
            "active_channels": 0,
        }
        after_control = apply_relation("control", **initial)
        after_insult = apply_relation("insult", **after_control)
        self.assertEqual(after_insult["phase_index"], initial["phase_index"])
        self.assertEqual(
            (after_insult["resolved_channels"], after_insult["active_channels"]),
            (1, 1),
        )

    def test_shift_composition_coherence(self) -> None:
        initial = {
            "phase_index": 4,
            "resolved_channels": 1,
            "active_channels": 0,
        }
        first = relation_shift("mother")
        second = relation_shift("control")
        direct = apply_shift(**initial, shift=compose_shifts(first, second))
        after_first = apply_shift(**initial, shift=first)
        sequential = apply_shift(**after_first, shift=second)
        self.assertEqual(direct, sequential)

    def test_strength_trichotomy(self) -> None:
        self.assertEqual(classify_strength(1.0, 0.5), "under")
        self.assertEqual(classify_strength(1.0, 1.0), "balanced")
        self.assertEqual(classify_strength(1.0, 1.5), "over")

    def test_overacting_is_excess_control_not_insult(self) -> None:
        self.assertTrue(is_overacting_control("control", nominal=1.0, actual=1.5))
        self.assertFalse(is_overacting_control("control", nominal=1.0, actual=1.0))
        self.assertFalse(is_overacting_control("insult", nominal=1.0, actual=1.5))

    def test_canonical_receipt(self) -> None:
        predecessor = v2_5_receipt()
        receipt = build_wuxing_generation_control_coherence_receipt(
            predecessor,
            nominal_control_strength=1.0,
            actual_control_strength=1.5,
        )
        self.assertEqual(receipt["disposition"], "WUXING_GENERATION_CONTROL_COHERENCE_VISIBLE")
        self.assertTrue(receipt["projection_admissible"])
        self.assertEqual(receipt["strength_surface"]["classification"], "over")
        self.assertTrue(receipt["strength_surface"]["overacting_control"])
        self.assertTrue(receipt["phase_history_separation_surface"]["phase_endpoint_agrees"])
        self.assertTrue(receipt["phase_history_separation_surface"]["history_endpoint_differs"])
        self.assertTrue(receipt["inverse_direction_surface"]["phase_returns"])
        self.assertTrue(receipt["inverse_direction_surface"]["history_advances_twice"])
        self.assertTrue(receipt["coherence_surface"]["composition_verified"])
        self.assertTrue(receipt["coherence_surface"]["center_is_coherence_not_earth_substance"])
        self.assertEqual(
            validate_wuxing_generation_control_coherence_receipt(predecessor, receipt),
            [],
        )

    def test_dependency_and_boundary_holds(self) -> None:
        predecessor = v2_5_receipt()
        broken = deepcopy(predecessor)
        broken["five_phase_base_surface"]["phase_is_relational_coordinate_not_substance"] = False
        receipt = build_wuxing_generation_control_coherence_receipt(broken)
        self.assertFalse(receipt["projection_admissible"])
        self.assertEqual(receipt["disposition"], "YIN_HOLDS_ON_V2_5_DEPENDENCY_GAP")

        held = build_wuxing_generation_control_coherence_receipt(
            predecessor,
            preserve_two_truths_gap=False,
        )
        self.assertFalse(held["projection_admissible"])
        self.assertEqual(
            held["disposition"],
            "YIN_HOLDS_ON_TWO_TRUTHS_OR_PROTECTED_HISTORY_GAP",
        )

    def test_non_authority_boundaries(self) -> None:
        receipt = build_wuxing_generation_control_coherence_receipt(v2_5_receipt())
        self.assertEqual(receipt["non_authority"], NON_AUTHORITY)
        self.assertTrue(all(value is False for value in NON_AUTHORITY.values()))
        self.assertTrue(receipt["strength_surface"]["nominal_is_not_clinical_threshold"])
        self.assertTrue(receipt["operational_surface"]["validation_is_not_truth"])
        self.assertTrue(receipt["operational_surface"]["selection_is_not_execution"])

    def test_tamper_detection(self) -> None:
        predecessor = v2_5_receipt()
        receipt = build_wuxing_generation_control_coherence_receipt(predecessor)
        tampered = deepcopy(receipt)
        tampered["coherence_surface"]["composition_verified"] = False
        errors = validate_wuxing_generation_control_coherence_receipt(predecessor, tampered)
        self.assertIn("receipt_digest_invalid", errors)
        self.assertIn("coherence_surface_invalid", errors)


if __name__ == "__main__":
    unittest.main()
