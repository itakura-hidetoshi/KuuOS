from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from runtime import kuuos_authorized_observation_world_feedback_v0_32 as core_v032
from runtime.kuuos_authorized_observation_world_feedback_entry_v0_32 import (
    build_authorized_observe_request,
    build_world_feedback_candidate,
    commit_evidence_receipt,
    commit_observe_request,
    commit_world_feedback,
    make_observation_authorization_receipt,
    make_observation_evidence_receipt,
)
from runtime.kuuos_endogenous_mission_observation_v0_31 import (
    build_mission_observation_report,
    make_world_evidence_packet,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import make_initial_state


class AuthorizedObservationWorldFeedbackEntryV032Test(unittest.TestCase):
    def report(self):
        state = make_initial_state(
            agency_id="agency-v032-entry",
            root_lineage_digest="a" * 64,
            created_at_ms=100,
        )
        packet = make_world_evidence_packet(
            packet_id="packet-v032-entry",
            source_state_digest=state["body_digest"],
            world_fragment_digest="b" * 64,
            observed_at_ms=110,
            unresolved_items=[
                {
                    "item_id": "q1",
                    "question": "Which observation resolves this WORLD ambiguity?",
                    "severity": 3,
                    "uncertainty": 4,
                    "evidence_refs": ["obs:old"],
                    "counterevidence_refs": ["obs:counter"],
                }
            ],
            observation_channels=[
                {
                    "channel_id": "sensor-a",
                    "modality": "structured-observation",
                    "supports_items": ["q1"],
                    "cost_class": "LOW",
                    "risk_class": "LOW",
                    "latency_class": "SHORT",
                }
            ],
        )
        return build_mission_observation_report(state, packet, generated_at_ms=120)

    def authorization(self, report):
        observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
        return make_observation_authorization_receipt(
            authorization_id="auth-entry-1",
            source_report_envelope=report,
            observation_candidate_id=observation_id,
            tool_id="tool.sensor-a.v1",
            scope_digest="c" * 64,
            host_license_digest="d" * 64,
            issued_by="external-governance",
            issued_at_ms=130,
            not_before_ms=140,
            expires_at_ms=300,
        )

    def official_request(self, report, authorization):
        return build_authorized_observe_request(
            report,
            authorization,
            requested_at_ms=150,
        )

    def official_evidence(self, request):
        return make_observation_evidence_receipt(
            request,
            evidence_id="evidence-entry-1",
            collected_at_ms=160,
            raw_artifact_digest="1" * 64,
            value_digest="2" * 64,
            collector_identity="collector-a",
            independent_source_identity="source-a",
            uncertainty_digest="3" * 64,
            calibration_digest="4" * 64,
            context_digest="5" * 64,
            tamper_evidence_digest="6" * 64,
            provenance_chain_digest="7" * 64,
            relation="SUPPORTS",
        )

    def test_request_ledger_rejects_core_only_existing_entry(self):
        report = self.report()
        authorization = self.authorization(report)
        core_only_request = core_v032.build_authorized_observe_request(
            report,
            authorization,
            requested_at_ms=150,
        )
        official_request = self.official_request(report, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "requests.jsonl"
            ledger.write_text(core_v032.canonical_json(core_only_request) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "authorization_issued_at_ms_invalid"):
                commit_observe_request(ledger_path=ledger, request_envelope=official_request)

    def test_evidence_ledger_rejects_core_only_existing_entry(self):
        report = self.report()
        request = self.official_request(report, self.authorization(report))
        core_only_evidence = core_v032.make_observation_evidence_receipt(
            request,
            evidence_id="core-evidence",
            collected_at_ms=160,
            raw_artifact_digest="1" * 64,
            value_digest="2" * 64,
            collector_identity="collector-a",
            independent_source_identity="source-a",
            uncertainty_digest="3" * 64,
            calibration_digest="4" * 64,
            context_digest="5" * 64,
            tamper_evidence_digest="6" * 64,
            provenance_chain_digest="7" * 64,
            relation="SUPPORTS",
        )
        official_evidence = self.official_evidence(request)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "evidence.jsonl"
            ledger.write_text(core_v032.canonical_json(core_only_evidence) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "authorization_expires_at_ms_invalid"):
                commit_evidence_receipt(ledger_path=ledger, receipt_envelope=official_evidence)

    def test_feedback_ledger_rejects_core_only_existing_entry(self):
        report = self.report()
        request = self.official_request(report, self.authorization(report))
        evidence = self.official_evidence(request)
        core_only_feedback = core_v032.build_world_feedback_candidate(
            report,
            evidence,
            generated_at_ms=170,
        )
        official_feedback = build_world_feedback_candidate(
            report,
            evidence,
            generated_at_ms=170,
        )
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "feedback.jsonl"
            ledger.write_text(core_v032.canonical_json(core_only_feedback) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "authorized_observation_window_not_preserved"):
                commit_world_feedback(ledger_path=ledger, feedback_envelope=official_feedback)


if __name__ == "__main__":
    unittest.main()
