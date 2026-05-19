#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import unittest
from copy import deepcopy

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_observation_kernel_v0_2M import (  # noqa: E402
    build_qi_observation_kernel_candidate,
    validate_qi_observation_kernel_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_observation_kernel_packet_v0_2M.json"


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


class QiObservationKernelV02MTests(unittest.TestCase):
    def test_default_packet_validates_and_projects_candidate(self) -> None:
        packet = load_packet()
        errors = validate_qi_observation_kernel_packet(packet)
        self.assertEqual(errors, [])

        result = build_qi_observation_kernel_candidate(packet)
        self.assertTrue(result["valid"])
        self.assertEqual(result["version"], "v0.2M")
        candidate = result["qi_state_candidate"]
        self.assertEqual(candidate["surface_type"], "QiStateCandidate")
        self.assertEqual(candidate["event_count"], 3)
        self.assertTrue(candidate["candidate_only"])
        self.assertFalse(candidate["authority_granted"])
        self.assertFalse(candidate["clinical_authority_granted"])
        self.assertFalse(candidate["execution_authority_granted"])
        self.assertFalse(candidate["source_history_replaced"])
        self.assertTrue(candidate["backaction_visible"])

    def test_backaction_erasure_is_rejected(self) -> None:
        packet = load_packet()
        packet["observation_events"][1]["backaction_visible"] = False
        errors = validate_qi_observation_kernel_packet(packet)
        self.assertIn("observation_events[1].backaction_visible must be true", errors)

    def test_current_snapshot_replacement_is_rejected(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["current_snapshot_replaces_process_history"] = True
        errors = validate_qi_observation_kernel_packet(packet)
        self.assertIn(
            "forbidden_reductions.current_snapshot_replaces_process_history must be false",
            errors,
        )

    def test_clinical_authority_expansion_is_rejected(self) -> None:
        packet = load_packet()
        packet["authority_boundary"]["clinical_authority"] = True
        errors = validate_qi_observation_kernel_packet(packet)
        self.assertIn("authority_boundary.clinical_authority must be false", errors)

    def test_handover_forced_by_red_flag_alone_is_rejected(self) -> None:
        packet = load_packet()
        packet["forbidden_reductions"]["handover_forced_by_red_flag_alone"] = True
        errors = validate_qi_observation_kernel_packet(packet)
        self.assertIn(
            "forbidden_reductions.handover_forced_by_red_flag_alone must be false",
            errors,
        )

    def test_event_time_must_strictly_increase(self) -> None:
        packet = load_packet()
        packet["observation_events"][2]["time_index"] = 1
        errors = validate_qi_observation_kernel_packet(packet)
        self.assertIn("observation_events[2].time_index must strictly increase", errors)

    def test_projection_modes_are_diagnostic_not_authority(self) -> None:
        packet = load_packet()
        altered = deepcopy(packet)
        for event in altered["observation_events"]:
            event["backflow_weight"] = 0.8
        result = build_qi_observation_kernel_candidate(altered)
        candidate = result["qi_state_candidate"]
        self.assertEqual(candidate["qi_runtime_mode"], "counterflow_watch")
        self.assertTrue(candidate["candidate_only"])
        self.assertFalse(candidate["authority_granted"])
        self.assertFalse(candidate["clinical_authority_granted"])
        self.assertFalse(candidate["execution_authority_granted"])


if __name__ == "__main__":
    unittest.main()
