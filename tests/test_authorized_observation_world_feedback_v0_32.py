from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from runtime.kuuos_authorized_observation_world_feedback_entry_v0_32 import (
    build_authorized_observe_request,
    build_world_feedback_candidate,
    commit_evidence_receipt,
    commit_observe_request,
    commit_world_feedback,
    make_observation_authorization_receipt,
    make_observation_evidence_receipt,
    validate_evidence_receipt,
    validate_observe_request,
    validate_world_feedback_candidate,
)
from runtime.kuuos_endogenous_mission_observation_v0_31 import (
    build_mission_observation_report,
    make_world_evidence_packet,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import make_initial_state


class AuthorizedObservationWorldFeedbackV032Test(unittest.TestCase):
    def state(self):
        return make_initial_state(
            agency_id="agency-v032",
            root_lineage_digest="a" * 64,
            created_at_ms=100,
        )

    def report(self, *, channels=True, counterevidence=True):
        state = self.state()
        packet = make_world_evidence_packet(
            packet_id="packet-v032",
            source_state_digest=state["body_digest"],
            world_fragment_digest="b" * 64,
            observed_at_ms=110,
            unresolved_items=[
                {
                    "item_id": "q1",
                    "question": "Which WORLD interpretation best explains the anomaly?",
                    "severity": 3,
                    "uncertainty": 4,
                    "evidence_refs": ["obs:old-support"],
                    "counterevidence_refs": ["obs:old-counter"] if counterevidence else [],
                }
            ],
            observation_channels=(
                [
                    {
                        "channel_id": "sensor-a",
                        "modality": "structured-observation",
                        "supports_items": ["q1"],
                        "cost_class": "LOW",
                        "risk_class": "LOW",
                        "latency_class": "SHORT",
                    }
                ]
                if channels
                else []
            ),
        )
        return build_mission_observation_report(state, packet, generated_at_ms=120)

    def authorization(self, report, *, authorization_id="auth-1", expires_at_ms=300):
        observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
        return make_observation_authorization_receipt(
            authorization_id=authorization_id,
            source_report_envelope=report,
            observation_candidate_id=observation_id,
            tool_id="tool.sensor-a.v1",
            scope_digest="c" * 64,
            host_license_digest="d" * 64,
            issued_by="external-governance",
            issued_at_ms=130,
            not_before_ms=140,
            expires_at_ms=expires_at_ms,
        )

    def request(self, report, *, authorization_id="auth-1", requested_at_ms=150, expires_at_ms=300):
        auth = self.authorization(
            report,
            authorization_id=authorization_id,
            expires_at_ms=expires_at_ms,
        )
        return build_authorized_observe_request(report, auth, requested_at_ms=requested_at_ms)

    def evidence(self, request, *, relation="SUPPORTS", evidence_id="evidence-1", collected_at_ms=160):
        return make_observation_evidence_receipt(
            request,
            evidence_id=evidence_id,
            collected_at_ms=collected_at_ms,
            raw_artifact_digest="1" * 64,
            value_digest="2" * 64,
            collector_identity="collector-a",
            independent_source_identity="source-a",
            uncertainty_digest="3" * 64,
            calibration_digest="4" * 64,
            context_digest="5" * 64,
            tamper_evidence_digest="6" * 64,
            provenance_chain_digest="7" * 64,
            relation=relation,
        )

    def test_exact_authorization_materializes_single_use_observe_request(self):
        report = self.report()
        request = self.request(report)
        body = validate_observe_request(request)
        self.assertEqual(1, body["invocation_index"])
        self.assertTrue(body["single_use"])
        self.assertTrue(body["authorization_window_bound"])
        self.assertTrue(body["grants_observe_invocation"])
        self.assertFalse(body["grants_actos_effect_authority"])
        self.assertFalse(body["grants_truth_authority"])

    def test_expired_or_not_yet_valid_authorization_is_rejected(self):
        report = self.report()
        auth = self.authorization(report, expires_at_ms=200)
        with self.assertRaisesRegex(ValueError, "authorization_not_current"):
            build_authorized_observe_request(report, auth, requested_at_ms=139)
        with self.assertRaisesRegex(ValueError, "authorization_not_current"):
            build_authorized_observe_request(report, auth, requested_at_ms=200)

    def test_capability_discovery_candidate_cannot_be_authorized(self):
        report = self.report(channels=False)
        observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
        with self.assertRaisesRegex(ValueError, "report_not_ready_for_observation_authorization"):
            make_observation_authorization_receipt(
                authorization_id="auth-gap",
                source_report_envelope=report,
                observation_candidate_id=observation_id,
                tool_id="missing-tool",
                scope_digest="c" * 64,
                host_license_digest="d" * 64,
                issued_by="external-governance",
                issued_at_ms=130,
                not_before_ms=140,
                expires_at_ms=300,
            )

    def test_authorization_is_exactly_bound_to_report_and_candidate(self):
        report = self.report()
        auth = self.authorization(report)
        other = self.report(counterevidence=False)
        with self.assertRaisesRegex(ValueError, "authorization_report_mismatch"):
            build_authorized_observe_request(other, auth, requested_at_ms=150)
        tampered = json.loads(json.dumps(auth))
        tampered["body"]["tool_id"] = "tampered-tool"
        with self.assertRaisesRegex(ValueError, "digest_mismatch"):
            build_authorized_observe_request(report, tampered, requested_at_ms=150)

    def test_authorization_is_consumed_at_most_once(self):
        report = self.report()
        auth = self.authorization(report)
        first_request = build_authorized_observe_request(report, auth, requested_at_ms=150)
        second_request = build_authorized_observe_request(report, auth, requested_at_ms=151)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "requests.jsonl"
            first = commit_observe_request(ledger_path=ledger, request_envelope=first_request)
            replay = commit_observe_request(ledger_path=ledger, request_envelope=first_request)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            with self.assertRaisesRegex(ValueError, "authorization_already_consumed"):
                commit_observe_request(ledger_path=ledger, request_envelope=second_request)
            self.assertEqual(1, len(ledger.read_text(encoding="utf-8").splitlines()))

    def test_evidence_receipt_requires_collection_inside_authorization_window(self):
        report = self.report()
        request = self.request(report, expires_at_ms=170)
        inside = self.evidence(request, collected_at_ms=169)
        self.assertTrue(validate_evidence_receipt(inside)["authorization_window_observed"])
        with self.assertRaisesRegex(ValueError, "outside_authorization_window"):
            self.evidence(request, evidence_id="late", collected_at_ms=170)

    def test_evidence_receipt_preserves_provenance_and_verification_debt(self):
        evidence = self.evidence(self.request(self.report()), relation="CONTRADICTS")
        body = validate_evidence_receipt(evidence)
        self.assertEqual("CONTRADICTS", body["relation"])
        self.assertTrue(body["observation_recorded"])
        self.assertFalse(body["observation_is_verification"])
        self.assertTrue(body["verification_required"])
        self.assertFalse(body["grants_truth_authority"])
        self.assertFalse(body["grants_causal_attribution"])

    def test_one_request_has_at_most_one_evidence_receipt(self):
        request = self.request(self.report())
        first_evidence = self.evidence(request, evidence_id="e1")
        second_evidence = self.evidence(request, evidence_id="e2", relation="INCONCLUSIVE")
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "evidence.jsonl"
            first = commit_evidence_receipt(ledger_path=ledger, receipt_envelope=first_evidence)
            replay = commit_evidence_receipt(ledger_path=ledger, receipt_envelope=first_evidence)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            with self.assertRaisesRegex(ValueError, "request_already_has_evidence_receipt"):
                commit_evidence_receipt(ledger_path=ledger, receipt_envelope=second_evidence)

    def test_supporting_evidence_creates_world_update_candidate_not_truth(self):
        report = self.report()
        evidence = self.evidence(self.request(report), relation="SUPPORTS")
        feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
        body = validate_world_feedback_candidate(feedback)
        self.assertEqual("WORLD_UPDATE_CANDIDATE", body["route"])
        self.assertEqual("SUPPORTED_UPDATE_CANDIDATE", body["candidate_state"])
        self.assertTrue(body["world_update_is_candidate"])
        self.assertFalse(body["automatic_truth_promotion"])
        self.assertFalse(body["automatic_mission_completion"])

    def test_contradicting_evidence_preserves_prior_counterevidence_and_uncertainty(self):
        report = self.report(counterevidence=True)
        evidence = self.evidence(self.request(report), relation="CONTRADICTS")
        feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
        body = feedback["body"]
        self.assertEqual("CONTRADICTED_UPDATE_CANDIDATE", body["candidate_state"])
        self.assertEqual(["obs:old-counter"], body["unresolved_item"]["counterevidence_refs"])
        self.assertTrue(body["counterevidence_preserved"])
        self.assertTrue(body["uncertainty_preserved"])

    def test_inconclusive_and_conflicted_evidence_require_reobservation(self):
        for relation, expected in (
            ("INCONCLUSIVE", "UNRESOLVED_REOBSERVE"),
            ("CONFLICTED", "CONFLICTED_REOBSERVE"),
        ):
            report = self.report()
            evidence = self.evidence(
                self.request(report, authorization_id=f"auth-{relation}"),
                relation=relation,
                evidence_id=f"evidence-{relation}",
            )
            feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
            self.assertEqual("REOBSERVE", feedback["body"]["route"])
            self.assertEqual(expected, feedback["body"]["candidate_state"])
            self.assertTrue(feedback["body"]["verification_required"])

    def test_feedback_rejects_mismatched_report_and_tampering(self):
        report = self.report()
        evidence = self.evidence(self.request(report))
        other = self.report(counterevidence=False)
        with self.assertRaisesRegex(ValueError, "evidence_report_mismatch"):
            build_world_feedback_candidate(other, evidence, generated_at_ms=170)
        feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
        tampered = json.loads(json.dumps(feedback))
        tampered["body"]["automatic_truth_promotion"] = True
        with self.assertRaisesRegex(ValueError, "digest_mismatch"):
            validate_world_feedback_candidate(tampered)

    def test_one_evidence_receipt_has_at_most_one_world_feedback_candidate(self):
        report = self.report()
        evidence = self.evidence(self.request(report))
        first_feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
        second_feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=171)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "feedback.jsonl"
            first = commit_world_feedback(ledger_path=ledger, feedback_envelope=first_feedback)
            replay = commit_world_feedback(ledger_path=ledger, feedback_envelope=first_feedback)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            with self.assertRaisesRegex(ValueError, "evidence_receipt_already_has_world_feedback"):
                commit_world_feedback(ledger_path=ledger, feedback_envelope=second_feedback)


if __name__ == "__main__":
    unittest.main()
