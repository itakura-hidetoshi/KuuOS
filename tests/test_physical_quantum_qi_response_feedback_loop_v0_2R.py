#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_response_feedback_loop_v0_2R import (  # noqa: E402
    build_qi_response_feedback_loop_candidate,
    validate_qi_response_feedback_loop_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_response_feedback_loop_packet_v0_2R.json"


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


class QiResponseFeedbackLoopV02RTests(unittest.TestCase):
    def test_default_packet_validates_and_keeps_consultation_open(self) -> None:
        packet = load_packet()
        self.assertEqual(validate_qi_response_feedback_loop_packet(packet), [])
        result = build_qi_response_feedback_loop_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["feedback_candidate"]["surface_type"], "QiResponseFeedbackLoopCandidate")
        self.assertTrue(result["feedback_candidate"]["consultation_open"])
        self.assertTrue(result["feedback_candidate"]["doctor_ai_consultation_accepted"])
        self.assertFalse(result["feedback_candidate"]["handover_forced"])
        self.assertFalse(result["feedback_receipt"]["authority_created_by_feedback"])

    def test_partial_recovery_does_not_create_truth_or_execution_authority(self) -> None:
        packet = load_packet()
        result = build_qi_response_feedback_loop_candidate(packet)
        self.assertEqual(result["feedback_status"], "partial_recovery_watch_visible")
        self.assertEqual(result["next_loop_route"], "continue_consultation_monitoring")
        self.assertGreaterEqual(result["feedback_candidate"]["recovery_signal"], 0.04)
        self.assertFalse(result["feedback_candidate"]["silent_recovery_claim_allowed"])
        self.assertFalse(result["authority_boundary"]["truth_authority"])
        self.assertFalse(result["authority_boundary"]["execution_authority"])

    def test_increasing_residue_routes_to_reobservation_loop(self) -> None:
        packet = load_packet()
        packet["response_candidate"]["hold_visible"] = False
        packet["response_candidate"]["watch_visible"] = False
        packet["response_candidate"]["response_route"] = "reobserve_and_record"
        packet["feedback_observation"]["phase_pressure_delta"] = 0.25
        packet["feedback_observation"]["critical_slowing_down_delta"] = 0.05
        packet["feedback_observation"]["hysteresis_delta"] = 0.05
        result = build_qi_response_feedback_loop_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["feedback_status"], "residue_increasing_reobserve")
        self.assertEqual(result["next_loop_route"], "continue_reobservation_loop")
        self.assertGreater(result["feedback_candidate"]["residue_signal"], 0.1)
        self.assertFalse(result["feedback_candidate"]["handover_default"])

    def test_hold_persistent_residue_keeps_hold_consultation_open_not_handover(self) -> None:
        packet = load_packet()
        packet["feedback_observation"]["phase_pressure_delta"] = 0.10
        packet["feedback_observation"]["critical_slowing_down_delta"] = 0.10
        packet["feedback_observation"]["hysteresis_delta"] = 0.10
        result = build_qi_response_feedback_loop_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["feedback_status"], "hold_visible_residue_persistent")
        self.assertEqual(result["next_loop_route"], "hold_with_consultation_open")
        self.assertTrue(result["feedback_candidate"]["hold_visible"])
        self.assertTrue(result["feedback_candidate"]["consultation_open"])
        self.assertFalse(result["feedback_candidate"]["handover_forced"])

    def test_missing_consultation_continuity_fails_closed(self) -> None:
        packet = load_packet()
        packet["feedback_observation"]["consultation_continuity"] = False
        errors = validate_qi_response_feedback_loop_packet(packet)
        self.assertIn("feedback_observation.consultation_continuity must be true", errors)

    def test_forbidden_metric_handover_flag_fails(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["metric_forces_handover"] = True
        errors = validate_qi_response_feedback_loop_packet(packet)
        self.assertIn("forbidden_reductions.metric_forces_handover must be false", errors)

    def test_response_authority_flag_fails(self) -> None:
        packet = load_packet()
        packet["response_candidate"]["clinical_authority_granted"] = True
        errors = validate_qi_response_feedback_loop_packet(packet)
        self.assertIn("response_candidate.clinical_authority_granted must be false", errors)


if __name__ == "__main__":
    unittest.main()
