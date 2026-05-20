#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_phase_transition_response_governor_v0_2Q import (  # noqa: E402
    build_qi_phase_transition_response_candidate,
    validate_qi_phase_transition_response_governor_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_phase_transition_response_governor_packet_v0_2Q.json"


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


class QiPhaseTransitionResponseGovernorV02QTests(unittest.TestCase):
    def test_default_packet_validates_and_routes_hold_with_consultation_open(self) -> None:
        packet = load_packet()
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertEqual(errors, [])

        result = build_qi_phase_transition_response_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["version"], "v0.2Q")
        response = result["governed_response_candidate"]
        receipt = result["response_receipt"]

        self.assertEqual(response["surface_type"], "QiPhaseTransitionGovernedResponseCandidate")
        self.assertEqual(response["response_route"], "hold_with_physician_ai_consultation_open")
        self.assertEqual(response["response_status"], "hold_visible_consultation_open")
        self.assertEqual(response["monitoring_intensity"], "high")
        self.assertTrue(response["hold_visible"])
        self.assertTrue(response["watch_visible"])
        self.assertTrue(response["consultation_open"])
        self.assertTrue(response["doctor_ai_consultation_accepted"])
        self.assertTrue(response["consultation_deepening_allowed"])
        self.assertTrue(response["reobserve_required_before_commit"])
        self.assertFalse(response["handover_forced"])
        self.assertFalse(response["handover_default"])
        self.assertTrue(response["candidate_only"])
        self.assertFalse(response["authority_granted"])
        self.assertFalse(response["clinical_authority_granted"])
        self.assertFalse(response["diagnosis_authority_granted"])
        self.assertFalse(response["prescription_authority_granted"])
        self.assertFalse(response["formula_selection_authority_granted"])
        self.assertFalse(response["triage_authority_granted"])
        self.assertFalse(response["execution_authority_granted"])

        self.assertEqual(receipt["response_route"], "hold_with_physician_ai_consultation_open")
        self.assertTrue(receipt["consultation_open"])
        self.assertTrue(receipt["doctor_ai_consultation_accepted"])
        self.assertFalse(receipt["handover_forced"])
        self.assertFalse(receipt["handover_default"])
        self.assertFalse(receipt["authority_created_by_response"])
        self.assertTrue(receipt["append_only_receipt"])
        self.assertTrue(receipt["non_authority_boundary_preserved"])

    def test_requires_response_governor_contract(self) -> None:
        packet = load_packet()
        packet["response_governor"]["doctor_ai_consultation_accepted"] = False
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertIn("response_governor.doctor_ai_consultation_accepted must be true", errors)

    def test_phase_candidate_cannot_force_handover(self) -> None:
        packet = load_packet()
        packet["phase_transition_candidate"]["handover_forced"] = True
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertIn("phase_transition_candidate.handover_forced must be false", errors)

    def test_consultation_cannot_be_closed_by_governor(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["consultation_closed_by_governor"] = True
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertIn("forbidden_reductions.consultation_closed_by_governor must be false", errors)

    def test_doctor_ai_consultation_cannot_be_blocked(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["doctor_ai_consultation_blocked"] = True
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertIn("forbidden_reductions.doctor_ai_consultation_blocked must be false", errors)

    def test_metric_cannot_force_handover(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["metric_forces_handover"] = True
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertIn("forbidden_reductions.metric_forces_handover must be false", errors)

    def test_response_cannot_create_authority(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["authority_created_by_response"] = True
        errors = validate_qi_phase_transition_response_governor_packet(packet)
        self.assertIn("forbidden_reductions.authority_created_by_response must be false", errors)

    def test_low_alert_routes_to_candidate_monitoring(self) -> None:
        packet = load_packet()
        phase = packet["phase_transition_candidate"]
        phase["phase_pressure_score"] = 0.1
        phase["critical_slowing_down_score"] = 0.1
        phase["hysteresis_score"] = 0.1
        phase["increasing_pressure_channels"] = 0
        phase["hold_visible"] = False
        phase["watch_visible"] = False
        phase["transition_alert_level"] = "phase_transition_not_indicated"
        phase["recommended_route"] = "continue_candidate_monitoring"

        result = build_qi_phase_transition_response_candidate(packet)
        response = result["governed_response_candidate"]
        self.assertEqual(response["response_route"], "continue_candidate_monitoring")
        self.assertEqual(response["response_status"], "continue_candidate_monitoring")
        self.assertEqual(response["monitoring_intensity"], "baseline")
        self.assertTrue(response["consultation_open"])
        self.assertTrue(response["doctor_ai_consultation_accepted"])
        self.assertFalse(response["handover_forced"])
        self.assertFalse(response["reobserve_required_before_commit"])

    def test_watch_alert_routes_to_consultation_monitoring(self) -> None:
        packet = load_packet()
        phase = packet["phase_transition_candidate"]
        phase["phase_pressure_score"] = 0.52
        phase["critical_slowing_down_score"] = 0.4
        phase["hysteresis_score"] = 0.5
        phase["hold_visible"] = False
        phase["watch_visible"] = True
        phase["transition_alert_level"] = "phase_transition_watch_visible"
        phase["recommended_route"] = "continue_consultation_with_monitoring"

        result = build_qi_phase_transition_response_candidate(packet)
        response = result["governed_response_candidate"]
        self.assertEqual(response["response_route"], "consultation_monitoring_route")
        self.assertEqual(response["response_status"], "watch_visible_consultation_open")
        self.assertEqual(response["monitoring_intensity"], "moderate")
        self.assertTrue(response["consultation_open"])
        self.assertFalse(response["handover_forced"])


if __name__ == "__main__":
    unittest.main()
