#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_transition_trajectory_ledger_v0_2O import (  # noqa: E402
    build_qi_transition_trajectory_ledger_candidate,
    validate_qi_transition_trajectory_ledger_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_transition_trajectory_ledger_packet_v0_2O.json"


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


class QiTransitionTrajectoryLedgerV02OTests(unittest.TestCase):
    def test_default_packet_validates_and_builds_trajectory(self) -> None:
        packet = load_packet()
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertEqual(errors, [])

        result = build_qi_transition_trajectory_ledger_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["version"], "v0.2O")
        candidate = result["trajectory_candidate"]
        receipt = result["trajectory_receipt"]

        self.assertEqual(candidate["surface_type"], "QiTransitionTrajectoryCandidate")
        self.assertEqual(candidate["record_count"], 3)
        self.assertEqual(candidate["continue_count"], 1)
        self.assertEqual(candidate["watch_count"], 1)
        self.assertEqual(candidate["hold_count"], 1)
        self.assertEqual(candidate["trajectory_decision"], "trajectory_hold_visible")
        self.assertTrue(candidate["candidate_only"])
        self.assertTrue(candidate["lineage_preserved"])
        self.assertFalse(candidate["source_history_replaced"])
        self.assertFalse(candidate["authority_granted"])
        self.assertFalse(candidate["clinical_authority_granted"])
        self.assertFalse(candidate["execution_authority_granted"])
        self.assertFalse(candidate["handover_forced"])
        self.assertFalse(candidate["doctor_ai_consultation_blocked"])
        self.assertTrue(receipt["hold_visible"])
        self.assertTrue(receipt["watch_visible"])
        self.assertFalse(receipt["authority_accumulated"])
        self.assertTrue(receipt["non_authority_boundary_preserved"])

    def test_requires_two_records_for_trajectory(self) -> None:
        packet = load_packet()
        packet["transition_records"] = packet["transition_records"][:1]
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("transition_records must contain at least two records", errors)

    def test_sequence_index_must_strictly_increase(self) -> None:
        packet = load_packet()
        packet["transition_records"][1]["sequence_index"] = 0
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("transition_records[1].sequence_index must strictly increase", errors)

    def test_hold_visibility_is_required(self) -> None:
        packet = load_packet()
        for record in packet["transition_records"]:
            if record["transition_decision"] == "candidate_hold":
                record["transition_decision"] = "candidate_watch"
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("transition_records must include at least one candidate_hold record for hold visibility", errors)

    def test_watch_visibility_is_required(self) -> None:
        packet = load_packet()
        for record in packet["transition_records"]:
            if record["transition_decision"] == "candidate_watch":
                record["transition_decision"] = "candidate_continue"
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("transition_records must include at least one candidate_watch record for watch visibility", errors)

    def test_authority_cannot_accumulate_across_records(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["authority_accumulates_across_records"] = True
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("forbidden_reductions.authority_accumulates_across_records must be false", errors)

    def test_record_cannot_grant_clinical_authority(self) -> None:
        packet = load_packet()
        packet["transition_records"][0]["clinical_authority_granted"] = True
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("transition_records[0].clinical_authority_granted must be false", errors)

    def test_next_state_metric_must_be_bounded(self) -> None:
        packet = load_packet()
        packet["transition_records"][0]["next_state_candidate"]["qi_backflow"] = 1.2
        errors = validate_qi_transition_trajectory_ledger_packet(packet)
        self.assertIn("transition_records[0].next_state_candidate.qi_backflow must be a number in [0, 1]", errors)

    def test_metric_trajectory_does_not_force_handover(self) -> None:
        packet = load_packet()
        result = build_qi_transition_trajectory_ledger_candidate(packet)
        candidate = result["trajectory_candidate"]
        receipt = result["trajectory_receipt"]
        self.assertEqual(candidate["trajectory_decision"], "trajectory_hold_visible")
        self.assertFalse(candidate["handover_forced"])
        self.assertFalse(receipt["handover_forced"])
        self.assertFalse(receipt["doctor_ai_consultation_blocked"])


if __name__ == "__main__":
    unittest.main()
