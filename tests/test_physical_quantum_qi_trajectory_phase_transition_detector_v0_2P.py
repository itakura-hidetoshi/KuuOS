#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_trajectory_phase_transition_detector_v0_2P import (  # noqa: E402
    build_qi_trajectory_phase_transition_candidate,
    validate_qi_trajectory_phase_transition_detector_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_trajectory_phase_transition_detector_packet_v0_2P.json"


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


class QiTrajectoryPhaseTransitionDetectorV02PTests(unittest.TestCase):
    def test_default_packet_validates_and_detects_hold_visible_transition(self) -> None:
        packet = load_packet()
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertEqual(errors, [])

        result = build_qi_trajectory_phase_transition_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["version"], "v0.2P")
        candidate = result["phase_transition_candidate"]
        receipt = result["phase_transition_receipt"]

        self.assertEqual(candidate["surface_type"], "QiTrajectoryPhaseTransitionCandidate")
        self.assertEqual(candidate["transition_alert_level"], "phase_transition_hold_visible")
        self.assertEqual(candidate["recommended_route"], "deepen_consultation_and_reobserve")
        self.assertTrue(candidate["hold_visible"])
        self.assertTrue(candidate["watch_visible"])
        self.assertTrue(candidate["consultation_deepening_allowed"])
        self.assertTrue(candidate["physician_ai_consultation_preserved"])
        self.assertFalse(candidate["handover_forced"])
        self.assertTrue(candidate["candidate_only"])
        self.assertFalse(candidate["authority_granted"])
        self.assertFalse(candidate["clinical_authority_granted"])
        self.assertFalse(candidate["diagnosis_authority_granted"])
        self.assertFalse(candidate["prescription_authority_granted"])
        self.assertFalse(candidate["formula_selection_authority_granted"])
        self.assertFalse(candidate["execution_authority_granted"])
        self.assertFalse(receipt["authority_created_by_alert"])
        self.assertFalse(receipt["handover_forced"])
        self.assertTrue(receipt["non_authority_boundary_preserved"])

    def test_requires_trajectory_candidate_object(self) -> None:
        packet = load_packet()
        packet["trajectory_candidate"] = None
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertIn("trajectory_candidate must be an object", errors)

    def test_requires_candidate_only_trajectory(self) -> None:
        packet = load_packet()
        packet["trajectory_candidate"]["candidate_only"] = False
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertIn("trajectory_candidate.candidate_only must be true", errors)

    def test_trajectory_cannot_force_handover(self) -> None:
        packet = load_packet()
        packet["trajectory_candidate"]["handover_forced"] = True
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertIn("trajectory_candidate.handover_forced must be false", errors)

    def test_phase_transition_cannot_close_physician_ai_consultation(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["phase_transition_closes_physician_ai_consultation"] = True
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertIn("forbidden_reductions.phase_transition_closes_physician_ai_consultation must be false", errors)

    def test_alert_cannot_create_authority(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["authority_created_by_alert"] = True
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertIn("forbidden_reductions.authority_created_by_alert must be false", errors)

    def test_threshold_order_is_checked(self) -> None:
        packet = load_packet()
        packet["thresholds"]["watch_threshold"] = 0.8
        packet["thresholds"]["hold_threshold"] = 0.6
        errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
        self.assertIn("thresholds.watch_threshold must be <= thresholds.hold_threshold", errors)

    def test_low_pressure_routes_to_continue_monitoring(self) -> None:
        packet = load_packet()
        trajectory = packet["trajectory_candidate"]
        trajectory["continue_count"] = 3
        trajectory["watch_count"] = 0
        trajectory["hold_count"] = 0
        trajectory["average_risk_score"] = 0.1
        trajectory["latest_risk_score"] = 0.1
        trajectory["stability_index"] = 0.9
        trajectory["risk_trend"] = "stable"
        trajectory["backflow_trend"] = "stable"
        trajectory["tail_residue_trend"] = "stable"
        trajectory["recoverability_trend"] = "stable"
        trajectory["transport_distortion_trend"] = "stable"
        trajectory["trajectory_decision"] = "trajectory_continue_candidate"
        result = build_qi_trajectory_phase_transition_candidate(packet)
        candidate = result["phase_transition_candidate"]
        self.assertEqual(candidate["transition_alert_level"], "phase_transition_not_indicated")
        self.assertEqual(candidate["recommended_route"], "continue_candidate_monitoring")
        self.assertFalse(candidate["handover_forced"])

    def test_detection_preserves_consultation_not_default_handover(self) -> None:
        packet = load_packet()
        result = build_qi_trajectory_phase_transition_candidate(packet)
        candidate = result["phase_transition_candidate"]
        receipt = result["phase_transition_receipt"]
        self.assertTrue(candidate["physician_ai_consultation_preserved"])
        self.assertTrue(receipt["physician_ai_consultation_preserved"])
        self.assertFalse(candidate["handover_forced"])
        self.assertFalse(receipt["handover_forced"])


if __name__ == "__main__":
    unittest.main()
