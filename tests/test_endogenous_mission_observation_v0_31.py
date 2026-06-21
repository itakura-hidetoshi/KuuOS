from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from runtime.kuuos_endogenous_mission_observation_v0_31 import (
    build_mission_observation_report,
    make_world_evidence_packet,
    persist_report,
    validate_report,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import (
    apply_request,
    make_initial_state,
    make_request,
)


class EndogenousMissionObservationV031Test(unittest.TestCase):
    def state(self):
        return make_initial_state(
            agency_id="agency-v031",
            root_lineage_digest="d" * 64,
            created_at_ms=100,
        )

    def packet(self, state, *, unresolved_items=None, channels=None, packet_id="packet-1"):
        if unresolved_items is None:
            unresolved_items = [
                {
                    "item_id": "q1",
                    "question": "Which mechanism explains the new WORLD anomaly?",
                    "severity": 3,
                    "uncertainty": 4,
                    "evidence_refs": ["obs:a"],
                    "counterevidence_refs": [],
                }
            ]
        if channels is None:
            channels = [
                {
                    "channel_id": "sensor-a",
                    "modality": "structured-observation",
                    "supports_items": ["q1"],
                    "cost_class": "LOW",
                    "risk_class": "LOW",
                    "latency_class": "SHORT",
                },
                {
                    "channel_id": "archive-b",
                    "modality": "historical-retrieval",
                    "supports_items": ["*"],
                    "cost_class": "LOW",
                    "risk_class": "LOW",
                    "latency_class": "MEDIUM",
                },
            ]
        return make_world_evidence_packet(
            packet_id=packet_id,
            source_state_digest=state["body_digest"],
            world_fragment_digest="e" * 64,
            observed_at_ms=110,
            unresolved_items=unresolved_items,
            observation_channels=channels,
        )

    def test_unresolved_world_evidence_generates_mission_and_plural_observations(self):
        state = self.state()
        report = build_mission_observation_report(state, self.packet(state), generated_at_ms=120)
        body = validate_report(report)
        self.assertEqual("MISSION_PORTFOLIO_READY", body["route"])
        self.assertEqual(1, len(body["mission_candidates"]))
        self.assertEqual(2, len(body["observation_portfolio"]))
        self.assertEqual("CANDIDATE", body["mission_candidates"][0]["status"])
        self.assertFalse(body["mission_candidates"][0]["grants_activation_authority"])
        self.assertTrue(all(not item["grants_tool_invocation"] for item in body["observation_portfolio"]))

    def test_counterevidence_creates_disambiguation_mission_and_preserves_trace(self):
        state = self.state()
        items = [
            {
                "item_id": "q1",
                "question": "Resolve conflicting WORLD interpretations",
                "severity": 2,
                "uncertainty": 4,
                "evidence_refs": ["obs:positive"],
                "counterevidence_refs": ["obs:negative"],
            }
        ]
        report = build_mission_observation_report(
            state,
            self.packet(state, unresolved_items=items),
            generated_at_ms=120,
        )
        body = report["body"]
        self.assertEqual("DISAMBIGUATE", body["mission_candidates"][0]["mission_type"])
        self.assertEqual(["obs:negative"], body["unresolved_trace"][0]["counterevidence_refs"])
        self.assertTrue(body["preserves_counterevidence"])

    def test_missing_channel_routes_to_capability_discovery_without_self_authorization(self):
        state = self.state()
        report = build_mission_observation_report(
            state,
            self.packet(state, channels=[]),
            generated_at_ms=120,
        )
        body = report["body"]
        self.assertEqual("CAPABILITY_DISCOVERY", body["route"])
        observation = body["observation_portfolio"][0]
        self.assertIsNone(observation["channel_id"])
        self.assertEqual("CAPABILITY_DISCOVERY_CANDIDATE", observation["modality"])
        self.assertFalse(observation["grants_tool_invocation"])
        self.assertFalse(body["grants_actos_invocation"])

    def test_empty_unresolved_set_creates_no_mission(self):
        state = self.state()
        report = build_mission_observation_report(
            state,
            self.packet(state, unresolved_items=[], channels=[]),
            generated_at_ms=120,
        )
        body = report["body"]
        self.assertEqual("NO_NEW_MISSION", body["route"])
        self.assertEqual([], body["mission_candidates"])
        self.assertEqual([], body["observation_portfolio"])

    def test_paused_state_holds_portfolio_without_closing_horizon(self):
        state = self.state()
        request = make_request(
            request_id="pause-1",
            source_state_digest=state["body_digest"],
            action="LOCAL_HOLD",
            payload={
                "control_id": "hold-1",
                "scope_kind": "mission_instance",
                "scope_id": "agency-v031",
                "reason": "review",
                "expires_at_ms": 500,
            },
            requested_at_ms=105,
        )
        state = apply_request(state, request, applied_at_ms=108)["body"]["result_state"]
        report = build_mission_observation_report(state, self.packet(state), generated_at_ms=120)
        self.assertEqual("HOLD", report["body"]["route"])
        self.assertEqual("OPEN", state["body"]["constitutional_horizons"]["goal_formation"])
        self.assertEqual("OPEN", state["body"]["constitutional_horizons"]["observation_seeking"])

    def test_terminated_state_routes_to_handover_but_preserves_candidates(self):
        state = self.state()
        request = make_request(
            request_id="terminate-1",
            source_state_digest=state["body_digest"],
            action="TERMINATE_INSTANCE",
            payload={},
            requested_at_ms=105,
        )
        state = apply_request(state, request, applied_at_ms=108)["body"]["result_state"]
        report = build_mission_observation_report(state, self.packet(state), generated_at_ms=120)
        body = report["body"]
        self.assertEqual("HANDOVER", body["route"])
        self.assertEqual(1, len(body["mission_candidates"]))
        self.assertFalse(body["grants_plan_activation"])

    def test_priority_is_deterministic_and_highest_first(self):
        state = self.state()
        items = [
            {
                "item_id": "low",
                "question": "Low-priority question",
                "severity": 1,
                "uncertainty": 1,
                "evidence_refs": [],
                "counterevidence_refs": [],
            },
            {
                "item_id": "high",
                "question": "High-priority question",
                "severity": 4,
                "uncertainty": 4,
                "evidence_refs": ["obs:1", "obs:2"],
                "counterevidence_refs": ["counter:1"],
            },
        ]
        channels = [
            {
                "channel_id": "all",
                "modality": "general",
                "supports_items": ["*"],
                "cost_class": "LOW",
                "risk_class": "LOW",
                "latency_class": "SHORT",
            }
        ]
        packet = self.packet(state, unresolved_items=items, channels=channels)
        first = build_mission_observation_report(state, packet, generated_at_ms=120)
        second = build_mission_observation_report(state, packet, generated_at_ms=120)
        self.assertEqual(first, second)
        self.assertEqual("high", first["body"]["mission_candidates"][0]["source_item_id"])

    def test_packet_source_mismatch_and_tampering_are_rejected(self):
        state = self.state()
        other = make_initial_state(
            agency_id="other",
            root_lineage_digest="f" * 64,
            created_at_ms=100,
        )
        packet = self.packet(other)
        with self.assertRaisesRegex(ValueError, "source_state_packet_mismatch"):
            build_mission_observation_report(state, packet, generated_at_ms=120)
        tampered = json.loads(json.dumps(self.packet(state)))
        tampered["body"]["unresolved_items"][0]["question"] = "tampered"
        with self.assertRaisesRegex(ValueError, "digest_mismatch"):
            build_mission_observation_report(state, tampered, generated_at_ms=120)

    def test_persistence_is_append_only_and_exact_replay_is_idempotent(self):
        state = self.state()
        report = build_mission_observation_report(state, self.packet(state), generated_at_ms=120)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "mission-observation-v031.jsonl"
            first = persist_report(ledger_path=ledger, report_envelope=report)
            second = persist_report(ledger_path=ledger, report_envelope=report)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", second.status)
            self.assertEqual(1, len(ledger.read_text(encoding="utf-8").splitlines()))

    def test_same_packet_id_cannot_bind_to_different_report(self):
        state = self.state()
        first = build_mission_observation_report(state, self.packet(state), generated_at_ms=120)
        different_packet = self.packet(
            state,
            packet_id="packet-1",
            unresolved_items=[
                {
                    "item_id": "q2",
                    "question": "Different unresolved question",
                    "severity": 1,
                    "uncertainty": 2,
                    "evidence_refs": [],
                    "counterevidence_refs": [],
                }
            ],
            channels=[],
        )
        second = build_mission_observation_report(state, different_packet, generated_at_ms=121)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "mission-observation-v031.jsonl"
            persist_report(ledger_path=ledger, report_envelope=first)
            with self.assertRaisesRegex(ValueError, "packet_id_reuse_with_different_report"):
                persist_report(ledger_path=ledger, report_envelope=second)


if __name__ == "__main__":
    unittest.main()
