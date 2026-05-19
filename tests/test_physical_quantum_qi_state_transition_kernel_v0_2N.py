#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import unittest
from copy import deepcopy

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_state_transition_kernel_v0_2N import (  # noqa: E402
    build_qi_state_transition_candidate,
    validate_qi_state_transition_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_state_transition_kernel_packet_v0_2N.json"


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


class QiStateTransitionKernelV02NTests(unittest.TestCase):
    def test_default_packet_validates_and_projects_next_state(self) -> None:
        packet = load_packet()
        errors = validate_qi_state_transition_packet(packet)
        self.assertEqual(errors, [])

        result = build_qi_state_transition_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["version"], "v0.2N")
        next_state = result["next_state_candidate"]
        receipt = result["transition_receipt"]

        self.assertEqual(next_state["surface_type"], "QiStateCandidate")
        self.assertEqual(next_state["version"], "v0.2N")
        self.assertTrue(next_state["candidate_only"])
        self.assertTrue(next_state["lineage_preserved"])
        self.assertFalse(next_state["source_history_replaced"])
        self.assertFalse(next_state["authority_granted"])
        self.assertFalse(next_state["clinical_authority_granted"])
        self.assertFalse(next_state["execution_authority_granted"])
        self.assertTrue(receipt["lineage_preserved"])
        self.assertFalse(receipt["authority_granted"])
        self.assertFalse(receipt["handover_forced"])
        self.assertFalse(receipt["doctor_ai_consultation_blocked"])

    def test_transition_delta_out_of_bounds_is_rejected(self) -> None:
        packet = load_packet()
        packet["transition_events"][0]["backflow_delta"] = 0.5
        errors = validate_qi_state_transition_packet(packet)
        self.assertIn("transition_events[0].backflow_delta must be a number in [-0.25, 0.25]", errors)

    def test_backaction_erasure_is_rejected(self) -> None:
        packet = load_packet()
        packet["transition_events"][0]["backaction_visible"] = False
        errors = validate_qi_state_transition_packet(packet)
        self.assertIn("transition_events[0].backaction_visible must be true", errors)

    def test_lineage_replacement_is_rejected(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["lineage_replaced"] = True
        errors = validate_qi_state_transition_packet(packet)
        self.assertIn("forbidden_reductions.lineage_replaced must be false", errors)

    def test_transition_cannot_grant_clinical_authority(self) -> None:
        packet = load_packet()
        packet["authority_boundary"]["clinical_authority"] = True
        errors = validate_qi_state_transition_packet(packet)
        self.assertIn("authority_boundary.clinical_authority must be false", errors)

    def test_transition_cannot_force_handover_by_metric_alone(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["transition_forces_handover_by_metric_alone"] = True
        errors = validate_qi_state_transition_packet(packet)
        self.assertIn(
            "forbidden_reductions.transition_forces_handover_by_metric_alone must be false",
            errors,
        )

    def test_worsening_transition_routes_to_watch_or_hold_without_authority(self) -> None:
        packet = load_packet()
        altered = deepcopy(packet)
        for event in altered["transition_events"]:
            event["backflow_delta"] = 0.25
            event["tail_residue_delta"] = 0.25
            event["recoverability_delta"] = -0.25
            event["coherence_delta"] = -0.25
        result = build_qi_state_transition_candidate(altered)
        receipt = result["transition_receipt"]
        next_state = result["next_state_candidate"]
        self.assertIn(receipt["transition_decision"], {"candidate_watch", "candidate_hold"})
        self.assertIn(next_state["qi_runtime_mode"], {"counterflow_watch", "stagnation_watch", "deficiency_watch"})
        self.assertTrue(next_state["candidate_only"])
        self.assertFalse(next_state["authority_granted"])
        self.assertFalse(receipt["authority_granted"])
        self.assertFalse(receipt["handover_forced"])

    def test_hold_result_is_valid_not_silently_closed(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["hold_result_silently_closed"] = True
        errors = validate_qi_state_transition_packet(packet)
        self.assertIn("forbidden_reductions.hold_result_silently_closed must be false", errors)


if __name__ == "__main__":
    unittest.main()
