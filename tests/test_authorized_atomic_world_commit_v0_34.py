from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from runtime.kuuos_authorized_atomic_world_commit_entry_v0_34 import (
    ZERO_DIGEST,
    build_authorized_world_commit_request,
    commit_world_fragment_atomic,
    initialize_world_store,
    make_initial_world_store,
    make_world_commit_authorization_receipt,
    read_world_store,
    validate_atomic_world_commit_receipt,
    validate_authorized_world_commit_request,
    validate_world_commit_authorization_receipt,
    validate_world_store,
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
from runtime.kuuos_verifyos_world_adoption_entry_v0_33 import (
    build_verifyos_request,
    build_world_disposition_candidate,
    make_verification_protocol_receipt,
    make_verification_receipt,
)


class AuthorizedAtomicWorldCommitV034Test(unittest.TestCase):
    def disposition_chain(
        self,
        *,
        item_suffix: str = "1",
        prior_fragment: str = "b" * 64,
        verdict: str = "PASSED",
    ):
        state = make_initial_state(
            agency_id=f"agency-v034-{item_suffix}",
            root_lineage_digest="a" * 64,
            created_at_ms=100,
        )
        item_id = f"world-item-{item_suffix}"
        packet = make_world_evidence_packet(
            packet_id=f"packet-v034-{item_suffix}",
            source_state_digest=state["body_digest"],
            world_fragment_digest=prior_fragment,
            observed_at_ms=110,
            unresolved_items=[
                {
                    "item_id": item_id,
                    "question": "Should this WORLD fragment be updated?",
                    "severity": 3,
                    "uncertainty": 4,
                    "evidence_refs": ["evidence:prior"],
                    "counterevidence_refs": ["counterevidence:prior"],
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
        observation_authorization = make_observation_authorization_receipt(
            authorization_id=f"observe-auth-{item_suffix}",
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
            observation_authorization,
            requested_at_ms=150,
        )
        evidence = make_observation_evidence_receipt(
            observe_request,
            evidence_id=f"evidence-{item_suffix}",
            collected_at_ms=160,
            raw_artifact_digest="1" * 64,
            value_digest="2" * 64,
            collector_identity="collector-primary",
            independent_source_identity="independent-source",
            uncertainty_digest="3" * 64,
            calibration_digest="4" * 64,
            context_digest="5" * 64,
            tamper_evidence_digest="6" * 64,
            provenance_chain_digest="7" * 64,
            relation="SUPPORTS",
        )
        feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
        protocol = make_verification_protocol_receipt(
            protocol_id=f"verify-protocol-{item_suffix}",
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
            expires_at_ms=300,
        )
        verify_request = build_verifyos_request(
            feedback,
            evidence,
            protocol,
            requested_at_ms=200,
        )
        if verdict == "PASSED":
            verification = make_verification_receipt(
                verify_request,
                verification_id=f"verification-pass-{item_suffix}",
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
        else:
            verification = make_verification_receipt(
                verify_request,
                verification_id=f"verification-fail-{item_suffix}",
                completed_at_ms=210,
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
        disposition = build_world_disposition_candidate(
            feedback,
            verification,
            generated_at_ms=220,
        )
        return disposition

    def authorization(
        self,
        disposition,
        *,
        authorization_id: str = "world-commit-auth-1",
        store_id: str = "world-store-main",
        expected_generation: int = 0,
        expected_prior_commit_digest: str = ZERO_DIGEST,
        fencing_token: int = 1,
        lease_epoch: int = 1,
        expires_at_ms: int = 400,
    ):
        return make_world_commit_authorization_receipt(
            authorization_id=authorization_id,
            source_disposition_envelope=disposition,
            world_store_id=store_id,
            expected_generation=expected_generation,
            expected_prior_commit_digest=expected_prior_commit_digest,
            fencing_token=fencing_token,
            lease_epoch=lease_epoch,
            scope_digest="1" * 64,
            host_license_digest="2" * 64,
            issued_by="external-world-governance",
            issued_at_ms=230,
            not_before_ms=240,
            expires_at_ms=expires_at_ms,
        )

    def request(self, disposition, authorization, *, requested_at_ms: int = 250):
        return build_authorized_world_commit_request(
            disposition,
            authorization,
            requested_at_ms=requested_at_ms,
        )

    def initialize_store(self, path: Path, disposition):
        store = make_initial_world_store(
            world_store_id="world-store-main",
            root_lineage_digest=disposition["body"]["root_lineage_digest"],
            current_world_fragment_digest=disposition["body"]["prior_world_fragment_digest"],
            created_at_ms=225,
        )
        return initialize_world_store(store_path=path, store_envelope=store)

    def commit(self, path: Path, disposition, authorization, request, *, committed_at_ms=260):
        return commit_world_fragment_atomic(
            store_path=path,
            source_disposition_envelope=disposition,
            authorization_envelope=authorization,
            request_envelope=request,
            committed_at_ms=committed_at_ms,
        )

    def test_authorization_is_local_single_use_and_preserves_open_horizon(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        body = validate_world_commit_authorization_receipt(authorization)
        self.assertEqual(1, body["max_commits"])
        self.assertTrue(body["single_use"])
        self.assertTrue(body["local_commit_authorization_only"])
        self.assertTrue(body["open_horizon_preserved"])
        self.assertIsNone(body["global_cycle_limit"])
        self.assertIsNone(body["global_generation_limit"])
        self.assertIsNone(body["global_time_horizon_limit"])
        self.assertFalse(body["grants_constitutional_root_rewrite"])
        self.assertFalse(body["grants_memory_history_overwrite"])

    def test_only_adopt_candidate_can_be_authorized(self):
        rejected = self.disposition_chain(verdict="FAILED")
        self.assertEqual("REJECT_CANDIDATE", rejected["body"]["route"])
        with self.assertRaisesRegex(ValueError, "not_adopt_candidate"):
            self.authorization(rejected)

    def test_authorization_window_is_finite_but_does_not_bound_global_horizon(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition, expires_at_ms=260)
        with self.assertRaisesRegex(ValueError, "not_current"):
            self.request(disposition, authorization, requested_at_ms=260)
        body = validate_world_commit_authorization_receipt(authorization)
        self.assertLess(body["not_before_ms"], body["expires_at_ms"])
        self.assertIsNone(body["global_generation_limit"])

    def test_request_is_exactly_bound_and_single_use(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        body = validate_authorized_world_commit_request(request)
        self.assertEqual(disposition["body_digest"], body["source_disposition_digest"])
        self.assertEqual(authorization["body_digest"], body["authorization_digest"])
        self.assertEqual(1, body["commit_index"])
        self.assertTrue(body["optimistic_concurrency_required"])
        self.assertTrue(body["fencing_required"])
        self.assertTrue(body["atomic_replace_required"])
        self.assertTrue(body["append_only_history_required"])
        self.assertFalse(body["grants_constitutional_root_rewrite"])

    def test_request_cannot_rebind_authorization_to_another_disposition(self):
        first = self.disposition_chain(item_suffix="one")
        second = self.disposition_chain(item_suffix="two")
        authorization = self.authorization(first)
        with self.assertRaisesRegex(ValueError, "authorization_binding_mismatch"):
            self.request(second, authorization)

    def test_initial_store_is_genesis_and_open_horizon(self):
        disposition = self.disposition_chain()
        store = make_initial_world_store(
            world_store_id="world-store-main",
            root_lineage_digest=disposition["body"]["root_lineage_digest"],
            current_world_fragment_digest=disposition["body"]["prior_world_fragment_digest"],
            created_at_ms=225,
        )
        body = validate_world_store(store)
        self.assertEqual(0, body["generation"])
        self.assertEqual([], body["commits"])
        self.assertEqual(ZERO_DIGEST, body["last_commit_digest"])
        self.assertTrue(body["history_deletion_forbidden"])
        self.assertTrue(body["constitutional_root_immutable"])
        self.assertIsNone(body["global_cycle_limit"])

    def test_store_initialization_is_create_once(self):
        disposition = self.disposition_chain()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            with self.assertRaisesRegex(ValueError, "already_exists"):
                self.initialize_store(path, disposition)

    def test_atomic_commit_updates_pointer_and_appends_immutable_receipt(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            result = self.commit(path, disposition, authorization, request)
            self.assertEqual("COMMITTED", result.status)
            receipt = validate_atomic_world_commit_receipt(result.receipt)
            store = validate_world_store(result.store)
            self.assertEqual(1, store["generation"])
            self.assertEqual(
                disposition["body"]["candidate_world_fragment_digest"],
                store["current_world_fragment_digest"],
            )
            self.assertEqual(result.receipt["body_digest"], store["last_commit_digest"])
            self.assertEqual(1, len(store["commits"]))
            self.assertTrue(receipt["atomic_replace_committed"])
            self.assertTrue(receipt["append_only_history_preserved"])
            self.assertTrue(receipt["immutable_commit_receipt"])
            self.assertFalse(receipt["constitutional_root_rewritten"])
            self.assertFalse(receipt["memory_history_overwritten"])

    def test_exact_replay_returns_receipt_even_after_authorization_expiry(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition, expires_at_ms=270)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            first = self.commit(path, disposition, authorization, request, committed_at_ms=260)
            replay = self.commit(path, disposition, authorization, request, committed_at_ms=999)
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", replay.status)
            self.assertEqual(first.receipt["body_digest"], replay.receipt["body_digest"])
            self.assertEqual(1, replay.store["body"]["generation"])

    def test_new_commit_must_finish_inside_authorization_window(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition, expires_at_ms=260)
        request = self.request(disposition, authorization, requested_at_ms=250)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            with self.assertRaisesRegex(ValueError, "outside_authorization_window"):
                self.commit(path, disposition, authorization, request, committed_at_ms=260)

    def test_commit_revalidates_disposition_authorization_and_request_together(self):
        first = self.disposition_chain(item_suffix="one")
        second = self.disposition_chain(item_suffix="two")
        authorization = self.authorization(first)
        request = self.request(first, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, first)
            with self.assertRaisesRegex(ValueError, "authorization_binding_mismatch"):
                self.commit(path, second, authorization, request)

    def test_root_lineage_mismatch_is_rejected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            wrong_store = make_initial_world_store(
                world_store_id="world-store-main",
                root_lineage_digest="f" * 64,
                current_world_fragment_digest=disposition["body"]["prior_world_fragment_digest"],
                created_at_ms=225,
            )
            initialize_world_store(store_path=path, store_envelope=wrong_store)
            with self.assertRaisesRegex(ValueError, "root_lineage_mismatch"):
                self.commit(path, disposition, authorization, request)

    def test_store_id_mismatch_is_rejected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition, store_id="other-store")
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            with self.assertRaisesRegex(ValueError, "world_store_id_mismatch"):
                self.commit(path, disposition, authorization, request)

    def test_optimistic_generation_conflict_is_rejected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition, expected_generation=1)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            with self.assertRaisesRegex(ValueError, "generation_conflict"):
                self.commit(path, disposition, authorization, request)

    def test_prior_commit_conflict_is_rejected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(
            disposition,
            expected_prior_commit_digest="f" * 64,
        )
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            with self.assertRaisesRegex(ValueError, "prior_commit_conflict"):
                self.commit(path, disposition, authorization, request)

    def test_prior_fragment_conflict_is_rejected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            wrong_store = make_initial_world_store(
                world_store_id="world-store-main",
                root_lineage_digest=disposition["body"]["root_lineage_digest"],
                current_world_fragment_digest="e" * 64,
                created_at_ms=225,
            )
            initialize_world_store(store_path=path, store_envelope=wrong_store)
            with self.assertRaisesRegex(ValueError, "prior_fragment_conflict"):
                self.commit(path, disposition, authorization, request)

    def test_authorization_cannot_be_consumed_by_two_requests(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        first_request = self.request(disposition, authorization, requested_at_ms=250)
        second_request = self.request(disposition, authorization, requested_at_ms=251)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            self.commit(path, disposition, authorization, first_request)
            with self.assertRaisesRegex(ValueError, "authorization_already_consumed"):
                self.commit(path, disposition, authorization, second_request, committed_at_ms=261)

    def test_disposition_cannot_be_committed_twice_under_new_authorization(self):
        disposition = self.disposition_chain()
        first_authorization = self.authorization(disposition, authorization_id="auth-one")
        first_request = self.request(disposition, first_authorization)
        second_authorization = self.authorization(
            disposition,
            authorization_id="auth-two",
            fencing_token=2,
        )
        second_request = self.request(disposition, second_authorization, requested_at_ms=251)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            self.commit(path, disposition, first_authorization, first_request)
            with self.assertRaisesRegex(ValueError, "disposition_already_committed"):
                self.commit(path, disposition, second_authorization, second_request, committed_at_ms=261)

    def test_stale_fencing_token_is_rejected_across_generations(self):
        first = self.disposition_chain(item_suffix="one")
        first_auth = self.authorization(first, fencing_token=1, lease_epoch=1)
        first_request = self.request(first, first_auth)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, first)
            first_result = self.commit(path, first, first_auth, first_request)
            next_prior = first_result.store["body"]["current_world_fragment_digest"]
            second = self.disposition_chain(item_suffix="two", prior_fragment=next_prior)
            second_auth = self.authorization(
                second,
                authorization_id="auth-second",
                expected_generation=1,
                expected_prior_commit_digest=first_result.receipt["body_digest"],
                fencing_token=1,
                lease_epoch=1,
            )
            second_request = self.request(second, second_auth)
            with self.assertRaisesRegex(ValueError, "stale_fencing_token"):
                self.commit(path, second, second_auth, second_request)

    def test_stale_lease_epoch_is_rejected(self):
        first = self.disposition_chain(item_suffix="one")
        first_auth = self.authorization(first, fencing_token=1, lease_epoch=2)
        first_request = self.request(first, first_auth)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, first)
            first_result = self.commit(path, first, first_auth, first_request)
            second = self.disposition_chain(
                item_suffix="two",
                prior_fragment=first_result.store["body"]["current_world_fragment_digest"],
            )
            second_auth = self.authorization(
                second,
                authorization_id="auth-second",
                expected_generation=1,
                expected_prior_commit_digest=first_result.receipt["body_digest"],
                fencing_token=2,
                lease_epoch=1,
            )
            second_request = self.request(second, second_auth)
            with self.assertRaisesRegex(ValueError, "stale_lease_epoch"):
                self.commit(path, second, second_auth, second_request)

    def test_two_generation_commit_chain_is_valid_and_append_only(self):
        first = self.disposition_chain(item_suffix="one")
        first_auth = self.authorization(first, fencing_token=1, lease_epoch=1)
        first_request = self.request(first, first_auth)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, first)
            first_result = self.commit(path, first, first_auth, first_request)
            second = self.disposition_chain(
                item_suffix="two",
                prior_fragment=first_result.store["body"]["current_world_fragment_digest"],
            )
            second_auth = self.authorization(
                second,
                authorization_id="auth-second",
                expected_generation=1,
                expected_prior_commit_digest=first_result.receipt["body_digest"],
                fencing_token=2,
                lease_epoch=1,
            )
            second_request = self.request(second, second_auth)
            second_result = self.commit(
                path,
                second,
                second_auth,
                second_request,
                committed_at_ms=261,
            )
            store = validate_world_store(second_result.store)
            self.assertEqual(2, store["generation"])
            self.assertEqual(2, len(store["commits"]))
            self.assertEqual(
                first_result.receipt["body_digest"],
                second_result.receipt["body"]["previous_commit_digest"],
            )
            self.assertEqual(
                first_result.receipt["body"]["committed_world_fragment_digest"],
                second_result.receipt["body"]["previous_world_fragment_digest"],
            )
            self.assertTrue(store["append_only_history"])

    def test_receipt_contains_rollback_reference_but_performs_no_rollback(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            result = self.commit(path, disposition, authorization, request)
            receipt = validate_atomic_world_commit_receipt(result.receipt)
            self.assertEqual(64, len(receipt["rollback_reference_digest"]))
            self.assertTrue(receipt["rollback_requires_fresh_authorization"])
            self.assertTrue(receipt["rollback_is_not_history_deletion"])
            self.assertFalse(receipt["automatic_rollback_performed"])

    def test_store_history_tampering_is_detected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            self.commit(path, disposition, authorization, request)
            store = read_world_store(path)
            tampered_body = dict(store["body"])
            tampered_body["commits"] = []
            tampered = {"body": tampered_body, "body_digest": store["body_digest"]}
            path.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "digest_mismatch"):
                read_world_store(path)

    def test_receipt_tampering_is_detected(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            result = self.commit(path, disposition, authorization, request)
            tampered = json.loads(json.dumps(result.receipt))
            tampered["body"]["constitutional_root_rewritten"] = True
            with self.assertRaisesRegex(ValueError, "digest_mismatch"):
                validate_atomic_world_commit_receipt(tampered)

    def test_atomic_write_leaves_no_temporary_state_file(self):
        disposition = self.disposition_chain()
        authorization = self.authorization(disposition)
        request = self.request(disposition, authorization)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world-store.json"
            self.initialize_store(path, disposition)
            self.commit(path, disposition, authorization, request)
            temporary_files = [
                child.name for child in Path(tmp).iterdir() if ".tmp." in child.name
            ]
            self.assertEqual([], temporary_files)


if __name__ == "__main__":
    unittest.main()
