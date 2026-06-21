from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from runtime import kuuos_verifyos_world_adoption_v0_33 as core_v033
from runtime.kuuos_verifyos_world_adoption_entry_v0_33 import (
    build_verifyos_request,
    build_world_disposition_candidate,
    commit_verification_receipt,
    commit_verifyos_request,
    commit_world_disposition_candidate,
    make_verification_protocol_receipt,
    make_verification_receipt,
    validate_verification_protocol_receipt,
    validate_verification_receipt,
    validate_verifyos_request,
    validate_world_disposition_candidate,
)
from runtime.kuuos_authorized_observation_world_feedback_entry_v0_32 import (
    build_authorized_observe_request,
    build_world_feedback_candidate,
    make_observation_authorization_receipt,
    make_observation_evidence_receipt,
)
from runtime.kuuos_endogenous_mission_observation_v0_31 import (
    build_mission_observation_report,
    make_world_evidence_packet,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import make_initial_state


class VerifyOSWorldAdoptionV033Test(unittest.TestCase):
    def source_chain(self, *, relation="SUPPORTS", item_suffix="1"):
        state = make_initial_state(
            agency_id=f"agency-v033-{item_suffix}",
            root_lineage_digest="a" * 64,
            created_at_ms=100,
        )
        item_id = f"q-{item_suffix}"
        packet = make_world_evidence_packet(
            packet_id=f"packet-v033-{item_suffix}",
            source_state_digest=state["body_digest"],
            world_fragment_digest="b" * 64,
            observed_at_ms=110,
            unresolved_items=[
                {
                    "item_id": item_id,
                    "question": "Which WORLD interpretation is best supported?",
                    "severity": 3,
                    "uncertainty": 4,
                    "evidence_refs": ["observation:prior-support"],
                    "counterevidence_refs": ["observation:prior-counter"],
                }
            ],
            observation_channels=[
                {
                    "channel_id": "structured-observer",
                    "modality": "structured-observation",
                    "supports_items": [item_id],
                    "cost_class": "LOW",
                    "risk_class": "LOW",
                    "latency_class": "SHORT",
                }
            ],
        )
        report = build_mission_observation_report(state, packet, generated_at_ms=120)
        observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
        authorization = make_observation_authorization_receipt(
            authorization_id=f"observation-auth-{item_suffix}",
            source_report_envelope=report,
            observation_candidate_id=observation_id,
            tool_id="tool.structured-observer.v1",
            scope_digest="c" * 64,
            host_license_digest="d" * 64,
            issued_by="external-observation-governance",
            issued_at_ms=130,
            not_before_ms=140,
            expires_at_ms=250,
        )
        observe_request = build_authorized_observe_request(
            report,
            authorization,
            requested_at_ms=150,
        )
        evidence = make_observation_evidence_receipt(
            observe_request,
            evidence_id=f"evidence-{item_suffix}",
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
            relation=relation,
        )
        feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
        return report, evidence, feedback

    def protocol(self, feedback, evidence, *, protocol_id="protocol-1", expires_at_ms=300):
        return make_verification_protocol_receipt(
            protocol_id=protocol_id,
            source_feedback_envelope=feedback,
            evidence_receipt_envelope=evidence,
            criterion_digest="8" * 64,
            evaluation_method_digest="9" * 64,
            success_condition_digest="a" * 64,
            failure_condition_digest="b" * 64,
            falsification_condition_digest="c" * 64,
            evidence_requirements_digest="d" * 64,
            assessor_policy_digest="e" * 64,
            host_license_digest="f" * 64,
            issued_by="external-verification-governance",
            issued_at_ms=180,
            not_before_ms=190,
            expires_at_ms=expires_at_ms,
        )

    def request(self, feedback, evidence, *, protocol_id="protocol-1", requested_at_ms=200, expires_at_ms=300):
        protocol = self.protocol(
            feedback,
            evidence,
            protocol_id=protocol_id,
            expires_at_ms=expires_at_ms,
        )
        return build_verifyos_request(
            feedback,
            evidence,
            protocol,
            requested_at_ms=requested_at_ms,
        )

    def passed_receipt(self, request, *, verification_id="verification-pass", completed_at_ms=210):
        return make_verification_receipt(
            request,
            verification_id=verification_id,
            completed_at_ms=completed_at_ms,
            assessor_identity="assessor-primary",
            independent_assessor_identity="assessor-independent",
            assessment_artifact_digest="1" * 64,
            assessor_receipt_digest="2" * 64,
            challenge_record_digest="3" * 64,
            corroboration_record_digest="4" * 64,
            verdict="PASSED",
            source_matched=True,
            source_divergent=False,
            corroboration_admissible=True,
            criterion_satisfied=True,
            falsifier_triggered=False,
            assessor_independent=True,
            provenance_intact=True,
            method_reproducible=True,
            unresolved_conflict=False,
            reobservation_required=False,
        )

    def failed_receipt(self, request, *, verification_id="verification-fail", completed_at_ms=210):
        return make_verification_receipt(
            request,
            verification_id=verification_id,
            completed_at_ms=completed_at_ms,
            assessor_identity="assessor-primary",
            independent_assessor_identity="assessor-independent",
            assessment_artifact_digest="1" * 64,
            assessor_receipt_digest="2" * 64,
            challenge_record_digest="3" * 64,
            corroboration_record_digest="4" * 64,
            verdict="FAILED",
            source_matched=False,
            source_divergent=True,
            corroboration_admissible=True,
            criterion_satisfied=False,
            falsifier_triggered=True,
            assessor_independent=True,
            provenance_intact=True,
            method_reproducible=True,
            unresolved_conflict=False,
            reobservation_required=False,
        )

    def indeterminate_receipt(
        self,
        request,
        *,
        route="DEFER",
        verification_id="verification-indeterminate",
        completed_at_ms=210,
    ):
        return make_verification_receipt(
            request,
            verification_id=verification_id,
            completed_at_ms=completed_at_ms,
            assessor_identity="assessor-primary",
            independent_assessor_identity="assessor-independent",
            assessment_artifact_digest="1" * 64,
            assessor_receipt_digest="2" * 64,
            challenge_record_digest="3" * 64,
            corroboration_record_digest="4" * 64,
            verdict="INDETERMINATE",
            source_matched=False,
            source_divergent=False,
            corroboration_admissible=False,
            criterion_satisfied=False,
            falsifier_triggered=False,
            assessor_independent=False,
            provenance_intact=True,
            method_reproducible=True,
            unresolved_conflict=True,
            reobservation_required=(route == "REOBSERVE"),
            indeterminate_route=route,
        )

    def test_protocol_binds_feedback_evidence_criteria_and_no_authority(self):
        _, evidence, feedback = self.source_chain()
        protocol = self.protocol(feedback, evidence)
        body = validate_verification_protocol_receipt(protocol)
        self.assertEqual(feedback["body_digest"], body["source_feedback_digest"])
        self.assertEqual(evidence["body_digest"], body["source_evidence_receipt_digest"])
        self.assertTrue(body["criterion_defined_before_adjudication"])
        self.assertTrue(body["falsification_required"])
        self.assertTrue(body["independent_assessment_required"])
        self.assertTrue(body["single_use"])
        self.assertFalse(body["grants_truth_authority"])
        self.assertFalse(body["grants_world_adoption_authority"])
        self.assertFalse(body["grants_world_commit_authority"])

    def test_protocol_time_window_is_enforced(self):
        _, evidence, feedback = self.source_chain()
        protocol = self.protocol(feedback, evidence, expires_at_ms=220)
        with self.assertRaisesRegex(ValueError, "verification_protocol_not_current"):
            build_verifyos_request(feedback, evidence, protocol, requested_at_ms=189)
        with self.assertRaisesRegex(ValueError, "verification_protocol_not_current"):
            build_verifyos_request(feedback, evidence, protocol, requested_at_ms=220)

    def test_protocol_cannot_be_rebound_to_another_feedback(self):
        _, evidence, feedback = self.source_chain(item_suffix="one")
        _, other_evidence, other_feedback = self.source_chain(item_suffix="two")
        protocol = self.protocol(feedback, evidence)
        with self.assertRaisesRegex(ValueError, "verification_protocol_binding_mismatch"):
            build_verifyos_request(other_feedback, other_evidence, protocol, requested_at_ms=200)

    def test_verify_request_is_single_use_and_exactly_bound(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        body = validate_verifyos_request(request)
        self.assertEqual(1, body["verification_index"])
        self.assertTrue(body["single_use"])
        self.assertEqual(feedback["body_digest"], body["source_feedback_digest"])
        self.assertEqual(evidence["body_digest"], body["source_evidence_receipt_digest"])
        self.assertFalse(body["grants_truth_authority"])
        self.assertFalse(body["grants_world_adoption_authority"])

    def test_protocol_is_consumed_at_most_once(self):
        _, evidence, feedback = self.source_chain()
        protocol = self.protocol(feedback, evidence)
        first_request = build_verifyos_request(feedback, evidence, protocol, requested_at_ms=200)
        second_request = build_verifyos_request(feedback, evidence, protocol, requested_at_ms=201)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "verify-requests.jsonl"
            first = commit_verifyos_request(ledger_path=ledger, request_envelope=first_request)
            replay = commit_verifyos_request(ledger_path=ledger, request_envelope=first_request)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            with self.assertRaisesRegex(ValueError, "verification_protocol_already_consumed"):
                commit_verifyos_request(ledger_path=ledger, request_envelope=second_request)

    def test_passed_receipt_has_strict_admissibility_and_non_authority(self):
        _, evidence, feedback = self.source_chain()
        receipt = self.passed_receipt(self.request(feedback, evidence))
        body = validate_verification_receipt(receipt)
        self.assertEqual("PASSED", body["verdict"])
        self.assertTrue(body["verification_debt_discharged"])
        self.assertFalse(body["verification_required"])
        self.assertTrue(body["verification_not_truth"])
        self.assertTrue(body["verification_not_world_adoption"])
        self.assertTrue(body["independent_assessor_identity_distinct"])
        self.assertTrue(body["verification_window_preserved"])
        self.assertFalse(body["grants_world_adoption_authority"])

    def test_invalid_passed_conditions_are_rejected(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        with self.assertRaisesRegex(ValueError, "passed_verification_conditions_invalid"):
            make_verification_receipt(
                request,
                verification_id="invalid-pass",
                completed_at_ms=210,
                assessor_identity="assessor-primary",
                independent_assessor_identity="assessor-independent",
                assessment_artifact_digest="1" * 64,
                assessor_receipt_digest="2" * 64,
                challenge_record_digest="3" * 64,
                corroboration_record_digest="4" * 64,
                verdict="PASSED",
                source_matched=True,
                source_divergent=False,
                corroboration_admissible=True,
                criterion_satisfied=True,
                falsifier_triggered=True,
                assessor_independent=True,
                provenance_intact=True,
                method_reproducible=True,
                unresolved_conflict=False,
                reobservation_required=False,
            )

    def test_failed_receipt_requires_conclusive_failure_basis(self):
        _, evidence, feedback = self.source_chain()
        receipt = self.failed_receipt(self.request(feedback, evidence))
        body = validate_verification_receipt(receipt)
        self.assertEqual("FAILED", body["verdict"])
        self.assertTrue(body["corrective_action_required"])
        self.assertTrue(body["verification_debt_discharged"])
        self.assertFalse(body["verification_required"])

    def test_invalid_failed_conditions_are_rejected(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        with self.assertRaisesRegex(ValueError, "failed_verification_conditions_invalid"):
            make_verification_receipt(
                request,
                verification_id="invalid-fail",
                completed_at_ms=210,
                assessor_identity="assessor-primary",
                independent_assessor_identity="assessor-independent",
                assessment_artifact_digest="1" * 64,
                assessor_receipt_digest="2" * 64,
                challenge_record_digest="3" * 64,
                corroboration_record_digest="4" * 64,
                verdict="FAILED",
                source_matched=True,
                source_divergent=False,
                corroboration_admissible=True,
                criterion_satisfied=True,
                falsifier_triggered=False,
                assessor_independent=True,
                provenance_intact=True,
                method_reproducible=True,
                unresolved_conflict=False,
                reobservation_required=False,
            )

    def test_indeterminate_preserves_debt_and_selects_defer_or_reobserve(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        deferred = validate_verification_receipt(
            self.indeterminate_receipt(request, route="DEFER", verification_id="indeterminate-defer")
        )
        reobserve = validate_verification_receipt(
            self.indeterminate_receipt(request, route="REOBSERVE", verification_id="indeterminate-reobserve")
        )
        self.assertFalse(deferred["verification_debt_discharged"])
        self.assertTrue(deferred["verification_required"])
        self.assertFalse(deferred["reobservation_required"])
        self.assertTrue(reobserve["reobservation_required"])

    def test_completion_must_finish_inside_protocol_window(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence, expires_at_ms=211)
        with self.assertRaisesRegex(ValueError, "verification_completion_outside_protocol_window"):
            self.passed_receipt(request, completed_at_ms=211)

    def test_independent_assessor_must_be_a_distinct_identity(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        with self.assertRaisesRegex(ValueError, "independent_assessor_identity_must_be_distinct"):
            make_verification_receipt(
                request,
                verification_id="same-assessor",
                completed_at_ms=210,
                assessor_identity="same",
                independent_assessor_identity="same",
                assessment_artifact_digest="1" * 64,
                assessor_receipt_digest="2" * 64,
                challenge_record_digest="3" * 64,
                corroboration_record_digest="4" * 64,
                verdict="PASSED",
                source_matched=True,
                source_divergent=False,
                corroboration_admissible=True,
                criterion_satisfied=True,
                falsifier_triggered=False,
                assessor_independent=True,
                provenance_intact=True,
                method_reproducible=True,
                unresolved_conflict=False,
                reobservation_required=False,
            )

    def test_source_cannot_be_matched_and_divergent_simultaneously(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        with self.assertRaisesRegex(ValueError, "source_match_divergence_conflict"):
            make_verification_receipt(
                request,
                verification_id="source-conflict",
                completed_at_ms=210,
                assessor_identity="assessor-primary",
                independent_assessor_identity="assessor-independent",
                assessment_artifact_digest="1" * 64,
                assessor_receipt_digest="2" * 64,
                challenge_record_digest="3" * 64,
                corroboration_record_digest="4" * 64,
                verdict="FAILED",
                source_matched=True,
                source_divergent=True,
                corroboration_admissible=True,
                criterion_satisfied=False,
                falsifier_triggered=True,
                assessor_independent=True,
                provenance_intact=True,
                method_reproducible=True,
                unresolved_conflict=False,
                reobservation_required=False,
            )

    def test_non_indeterminate_receipt_cannot_carry_reobserve_hint(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        with self.assertRaisesRegex(ValueError, "non_indeterminate_route_must_be_defer"):
            make_verification_receipt(
                request,
                verification_id="invalid-route",
                completed_at_ms=210,
                assessor_identity="assessor-primary",
                independent_assessor_identity="assessor-independent",
                assessment_artifact_digest="1" * 64,
                assessor_receipt_digest="2" * 64,
                challenge_record_digest="3" * 64,
                corroboration_record_digest="4" * 64,
                verdict="PASSED",
                source_matched=True,
                source_divergent=False,
                corroboration_admissible=True,
                criterion_satisfied=True,
                falsifier_triggered=False,
                assessor_independent=True,
                provenance_intact=True,
                method_reproducible=True,
                unresolved_conflict=False,
                reobservation_required=False,
                indeterminate_route="REOBSERVE",
            )

    def test_one_request_has_at_most_one_verification_receipt(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        passed = self.passed_receipt(request, verification_id="receipt-one")
        failed = self.failed_receipt(request, verification_id="receipt-two")
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "verification-receipts.jsonl"
            first = commit_verification_receipt(ledger_path=ledger, receipt_envelope=passed)
            replay = commit_verification_receipt(ledger_path=ledger, receipt_envelope=passed)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            with self.assertRaisesRegex(ValueError, "verifyos_request_already_has_receipt"):
                commit_verification_receipt(ledger_path=ledger, receipt_envelope=failed)

    def test_passed_world_update_feedback_maps_to_adopt_candidate(self):
        _, evidence, feedback = self.source_chain(relation="SUPPORTS")
        receipt = self.passed_receipt(self.request(feedback, evidence))
        candidate = build_world_disposition_candidate(feedback, receipt, generated_at_ms=220)
        body = validate_world_disposition_candidate(candidate)
        self.assertEqual("ADOPT_CANDIDATE", body["route"])
        self.assertEqual(body["proposed_world_fragment_digest"], body["candidate_world_fragment_digest"])
        self.assertTrue(body["disposition_is_candidate"])
        self.assertTrue(body["governance_review_required"])
        self.assertFalse(body["automatic_world_adoption"])
        self.assertFalse(body["automatic_world_commit"])

    def test_passed_reobserve_feedback_stays_reobserve_candidate(self):
        _, evidence, feedback = self.source_chain(relation="INCONCLUSIVE")
        self.assertEqual("REOBSERVE", feedback["body"]["route"])
        receipt = self.passed_receipt(self.request(feedback, evidence), verification_id="pass-reobserve")
        candidate = build_world_disposition_candidate(feedback, receipt, generated_at_ms=220)
        body = validate_world_disposition_candidate(candidate)
        self.assertEqual("REOBSERVE_CANDIDATE", body["route"])
        self.assertEqual(body["prior_world_fragment_digest"], body["candidate_world_fragment_digest"])
        self.assertFalse(body["automatic_world_adoption"])

    def test_failed_verification_maps_to_reject_candidate(self):
        _, evidence, feedback = self.source_chain()
        receipt = self.failed_receipt(self.request(feedback, evidence))
        candidate = build_world_disposition_candidate(feedback, receipt, generated_at_ms=220)
        body = validate_world_disposition_candidate(candidate)
        self.assertEqual("REJECT_CANDIDATE", body["route"])
        self.assertEqual(body["prior_world_fragment_digest"], body["candidate_world_fragment_digest"])
        self.assertFalse(body["automatic_world_rejection"])

    def test_indeterminate_maps_to_defer_or_reobserve_candidate(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        deferred = build_world_disposition_candidate(
            feedback,
            self.indeterminate_receipt(request, route="DEFER", verification_id="defer-receipt"),
            generated_at_ms=220,
        )
        reobserve = build_world_disposition_candidate(
            feedback,
            self.indeterminate_receipt(request, route="REOBSERVE", verification_id="reobserve-receipt"),
            generated_at_ms=220,
        )
        self.assertEqual("DEFER_CANDIDATE", deferred["body"]["route"])
        self.assertEqual("REOBSERVE_CANDIDATE", reobserve["body"]["route"])

    def test_disposition_rejects_mismatched_feedback_and_tampering(self):
        _, evidence, feedback = self.source_chain(item_suffix="one")
        receipt = self.passed_receipt(self.request(feedback, evidence))
        _, _, other_feedback = self.source_chain(item_suffix="two")
        with self.assertRaisesRegex(ValueError, "verification_receipt_feedback"):
            build_world_disposition_candidate(other_feedback, receipt, generated_at_ms=220)
        candidate = build_world_disposition_candidate(feedback, receipt, generated_at_ms=220)
        tampered = json.loads(json.dumps(candidate))
        tampered["body"]["automatic_world_adoption"] = True
        with self.assertRaisesRegex(ValueError, "digest_mismatch"):
            validate_world_disposition_candidate(tampered)

    def test_one_verification_receipt_has_at_most_one_disposition(self):
        _, evidence, feedback = self.source_chain()
        receipt = self.passed_receipt(self.request(feedback, evidence))
        first_candidate = build_world_disposition_candidate(feedback, receipt, generated_at_ms=220)
        second_candidate = build_world_disposition_candidate(feedback, receipt, generated_at_ms=221)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "world-dispositions.jsonl"
            first = commit_world_disposition_candidate(
                ledger_path=ledger,
                candidate_envelope=first_candidate,
            )
            replay = commit_world_disposition_candidate(
                ledger_path=ledger,
                candidate_envelope=first_candidate,
            )
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            with self.assertRaisesRegex(ValueError, "verification_receipt_already_has_world_disposition"):
                commit_world_disposition_candidate(
                    ledger_path=ledger,
                    candidate_envelope=second_candidate,
                )

    def test_official_ledgers_reject_core_only_receipt_and_candidate(self):
        _, evidence, feedback = self.source_chain()
        request = self.request(feedback, evidence)
        official_receipt = self.passed_receipt(request)
        core_receipt = core_v033.make_verification_receipt(
            request,
            verification_id="core-only",
            completed_at_ms=210,
            assessor_identity="assessor-primary",
            independent_assessor_identity="assessor-independent",
            assessment_artifact_digest="1" * 64,
            assessor_receipt_digest="2" * 64,
            challenge_record_digest="3" * 64,
            corroboration_record_digest="4" * 64,
            verdict="PASSED",
            source_matched=True,
            source_divergent=False,
            corroboration_admissible=True,
            criterion_satisfied=True,
            falsifier_triggered=False,
            assessor_independent=True,
            provenance_intact=True,
            method_reproducible=True,
            unresolved_conflict=False,
            reobservation_required=False,
        )
        official_candidate = build_world_disposition_candidate(feedback, official_receipt, generated_at_ms=220)
        core_candidate_body = dict(official_candidate["body"])
        core_candidate_body.pop("disposition_is_candidate")
        core_candidate_body.pop("route_derived_from_verification")
        core_candidate = core_v033.make_envelope(core_candidate_body)
        with tempfile.TemporaryDirectory() as tmp:
            receipt_ledger = Path(tmp) / "receipts.jsonl"
            receipt_ledger.write_text(core_v033.canonical_json(core_receipt) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requested_at_ms_invalid"):
                commit_verification_receipt(
                    ledger_path=receipt_ledger,
                    receipt_envelope=official_receipt,
                )
            disposition_ledger = Path(tmp) / "dispositions.jsonl"
            disposition_ledger.write_text(core_v033.canonical_json(core_candidate) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "official_world_disposition_boundary_invalid"):
                commit_world_disposition_candidate(
                    ledger_path=disposition_ledger,
                    candidate_envelope=official_candidate,
                )


if __name__ == "__main__":
    unittest.main()
