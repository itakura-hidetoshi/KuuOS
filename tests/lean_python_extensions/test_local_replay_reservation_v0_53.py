"""v0.53: transactional local replay reservations, distinct from actual PlanOS authority."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_local_replay_reservation_v0_53 as subject,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, ROUTES,
)
from tests.lean_python_extensions.test_original_verify_plan_certificate_seam_v0_48 import (
    native_certificates,
)
from tests.lean_python_extensions.test_two_declared_plan_result_claims_v0_51 import (
    two_claims,
)
from tests.lean_python_extensions.test_local_mac_bound_plan_claims_v0_52 import (
    KEYS, CONTEXT, SEQ, NONCE, fixtures_mac_claims,
)
from scripts import (
    check_kuuos_lean_python_local_replay_sources_v0_53 as audit,
)


class LocalReplayReservationV053Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def _data(self, route="retain"):
        v, p = deepcopy(self.native[route])
        claims = two_claims(v, p)
        receipts = fixtures_mac_claims(claims)
        return v, p, claims, receipts

    def _reserve(self, data, path=None, keys=KEYS, context=CONTEXT, sequences=SEQ):
        v, p, c, r = data
        return subject.reserve_verified_mac_pair_locally(
            v, p, c, r,
            verification_keys=keys, expected_context=context,
            expected_sequences=sequences, ledger_path=path,
        )

    @staticmethod
    def _rows(path):
        with sqlite3.connect(path) as conn:
            return conn.execute(
                "SELECT key_id,context_id,sequence,nonce_hex,"
                "message_sha256,previous_row_sha256,row_sha256 "
                "FROM kuuos_plan_mac_seen_v053 ORDER BY entry_id"
            ).fetchall()

    def test_six_original_routes_record_only_local_proposal(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route), TemporaryDirectory() as tmp:
                path = Path(tmp) / "replay.sqlite3"
                result = self._reserve(self._data(route), path)
                self.assertEqual(result.status, subject.LOCAL_RECORDED_PROPOSAL)
                self.assertTrue(result.local_mac_verified)
                self.assertTrue(result.local_reservation_committed)
                self.assertEqual(result.local_rows_added, 2)
                self.assertTrue(path.is_file())
                self.assertEqual(len(self._rows(path)), 2)
                self.assertEqual(result.original_plan_result_state, NO_DATA)
                self.assertFalse(result.original_results_observed)
                self.assertFalse(result.external_issuers_authenticated)
                self.assertFalse(result.cross_host_replay_protected)
                self.assertFalse(result.original_lean_match_proved)
                self.assertFalse(result.host_execution_authorized)

    def test_missing_ledger_path_preserves_no_data_and_no_write(self):
        data = self._data()
        z = self._reserve(data)
        self.assertEqual(z.status, NO_DATA)
        self.assertFalse(z.local_reservation_committed)

    def test_same_receipts_replayed_across_calls_are_rejected(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            first = self._reserve(data, path)
            again = self._reserve(data, path)
            self.assertEqual(first.status, subject.LOCAL_RECORDED_PROPOSAL)
            self.assertEqual(again.status, subject.LOCAL_REPLAY_OBSTRUCTION)
            self.assertFalse(again.local_reservation_committed)
            self.assertEqual(len(self._rows(path)), 2)

    def test_duplicate_sequence_with_new_nonce_is_rejected(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            self.assertTrue(self._reserve(data, path).local_reservation_committed)
            v, p, c, _ = data
            new_nonces = dict(NONCE)
            new_nonces["first"] = "11112222333344445555666677778888"
            second = (v, p, c, fixtures_mac_claims(c, nonce=new_nonces))
            z = self._reserve(second, path)
            self.assertEqual(z.status, subject.LOCAL_REPLAY_OBSTRUCTION)
            self.assertEqual(len(self._rows(path)), 2)

    def test_duplicate_nonce_with_new_sequence_is_rejected(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            self._reserve(data, path)
            v, p, c, _ = data
            sequences = {"first": 9, "second": 10}
            receipts = fixtures_mac_claims(c, seq=sequences)
            z = self._reserve((v, p, c, receipts), path, sequences=sequences)
            self.assertEqual(z.status, subject.LOCAL_REPLAY_OBSTRUCTION)
            self.assertEqual(len(self._rows(path)), 2)

    def test_second_slot_collision_rolls_back_fresh_first_slot(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            self._reserve(data, path)
            v, p, c, _ = data
            sequences = {"first": 9, "second": 8}
            nonces = dict(NONCE)
            nonces["first"] = "11112222333344445555666677778888"
            receipts = fixtures_mac_claims(c, seq=sequences, nonce=nonces)
            z = self._reserve((v, p, c, receipts), path, sequences=sequences)
            self.assertEqual(z.status, subject.LOCAL_REPLAY_OBSTRUCTION)
            self.assertFalse(z.local_reservation_committed)
            self.assertEqual(len(self._rows(path)), 2)
            self.assertFalse(any(row[0] == "key-a" and row[2] == 9
                                 for row in self._rows(path)))

    def test_fresh_second_pair_extends_chain_and_retains_old_rows(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            first = self._reserve(data, path)
            before = self._rows(path)
            v, p, c, _ = data
            sequences = {"first": 9, "second": 10}
            nonces = {"first": "11112222333344445555666677778888",
                      "second": "88887777666655554444333322221111"}
            receipts = fixtures_mac_claims(c, seq=sequences, nonce=nonces)
            result = self._reserve((v, p, c, receipts), path, sequences=sequences)
            after = self._rows(path)
            self.assertEqual(result.status, subject.LOCAL_RECORDED_PROPOSAL)
            self.assertEqual(after[:2], before)
            self.assertEqual(len(after), 4)
            self.assertEqual(after[2][5], first.local_chain_head)
            self.assertEqual(after[-1][-1], result.local_chain_head)

    def test_existing_chain_inconsistency_blocks_future_insert(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            self._reserve(data, path)
            with sqlite3.connect(path) as db:
                db.execute(
                    "UPDATE kuuos_plan_mac_seen_v053 "
                    "SET row_sha256=? WHERE entry_id=1",
                    ("f" * 64,),
                )
            v, p, c, _ = data
            sequences = {"first": 9, "second": 10}
            nonces = {"first": "11112222333344445555666677778888",
                      "second": "88887777666655554444333322221111"}
            z = self._reserve(
                (v, p, c, fixtures_mac_claims(c, seq=sequences, nonce=nonces)),
                path, sequences=sequences,
            )
            self.assertEqual(z.status, BLOCKED)
            self.assertFalse(z.local_reservation_committed)
            self.assertEqual(len(self._rows(path)), 2)

    def test_preexisting_noncanonical_schema_is_blocked(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            with sqlite3.connect(path) as db:
                db.execute("CREATE TABLE kuuos_plan_mac_seen_v053 (fake TEXT)")
            z = self._reserve(data, path)
            self.assertEqual(z.status, BLOCKED)
            self.assertFalse(z.local_reservation_committed)

    def test_invalid_database_bytes_are_blocked(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            path.write_bytes(b"not-a-database")
            z = self._reserve(data, path)
            self.assertEqual(z.status, BLOCKED)

    def test_symlink_ledger_location_is_blocked(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            target = Path(tmp) / "target.db"
            link = Path(tmp) / "symlink.db"
            link.symlink_to(target)
            z = self._reserve(data, link)
            self.assertEqual(z.status, BLOCKED)
            self.assertFalse(target.exists())

    def test_relative_path_fails_closed(self):
        self.assertEqual(
            self._reserve(self._data(), Path("relative.db")).status, BLOCKED,
        )

    def test_invalid_mac_does_not_create_ledger_file(self):
        v, p, c, r = self._data()
        r["first"]["mac_sha256"] = "0" * 64
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            z = self._reserve((v, p, c, r), path)
            self.assertEqual(z.status, BLOCKED)
            self.assertFalse(path.exists())

    def test_missing_verifier_keys_never_creates_ledger(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            self.assertEqual(self._reserve(data, path, keys=None).status, NO_DATA)
            self.assertFalse(path.exists())

    def test_conflicting_mac_checked_claims_can_be_recorded_as_obstruction(self):
        v, p, c, _ = self._data()
        c["second"]["supplied_result_evidence"]["resulting_lineage_digests"].append(
            "zz-extra-lineage"
        )
        receipts = fixtures_mac_claims(c)
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            z = self._reserve((v, p, c, receipts), path)
            self.assertEqual(z.status, subject.LOCAL_RECORDED_OBSTRUCTION)
            self.assertEqual(z.conflicting_fields, ("resulting_lineage_digests",))
            self.assertTrue(z.local_reservation_committed)
            self.assertFalse(z.pairwise_agreement_proposal_only)
            self.assertEqual(z.original_plan_result_state, NO_DATA)
            self.assertEqual(len(self._rows(path)), 2)

    def test_invalid_original_planos_certificate_cannot_commit(self):
        v, p, c, r = self._data()
        p["intake_disposition"] = "malicious-reinterpretation"
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            z = self._reserve((v, p, c, r), path)
            self.assertEqual(z.status, BLOCKED)
            self.assertFalse(path.exists())

    def test_two_simultaneous_connection_attempts_only_one_can_commit(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(self._reserve, data, path) for _ in range(2)]
                results = [future.result() for future in futures]
            self.assertEqual(
                sorted(r.status for r in results),
                sorted([subject.LOCAL_RECORDED_PROPOSAL,
                        subject.LOCAL_REPLAY_OBSTRUCTION]),
            )
            self.assertEqual(len(self._rows(path)), 2)

    def test_no_symmetric_secrets_appear_in_rows(self):
        data = self._data()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.db"
            self._reserve(data, path)
            raw = path.read_bytes()
            for secret in KEYS.values():
                self.assertNotIn(secret, raw)
            self.assertEqual(len(self._rows(path)), 2)

    def test_original_source_and_claims_are_not_mutated(self):
        data = self._data()
        original = deepcopy(data)
        with TemporaryDirectory() as tmp:
            self._reserve(data, Path(tmp) / "ledger.db")
        self.assertEqual(data, original)

    def test_no_original_kernel_reexecution(self):
        data = self._data()
        with TemporaryDirectory() as tmp, patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("VerifyOS rerun"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("PlanOS rerun"),
        ):
            z = self._reserve(data, Path(tmp) / "ledger.db")
        self.assertEqual(z.status, subject.LOCAL_RECORDED_PROPOSAL)

    def test_no_replay_or_issuer_authentication_is_inferred_from_local_commit(self):
        with TemporaryDirectory() as tmp:
            z = self._reserve(self._data(), Path(tmp) / "ledger.db")
        self.assertFalse(z.cross_host_replay_protected)
        self.assertFalse(z.external_issuers_authenticated)
        self.assertFalse(z.original_lean_match_proved)
        self.assertFalse(z.global_descent_certified)
        self.assertFalse(z.host_execution_authorized)

    def test_new_original_source_static_checker_is_called_in_runtime_suite(self):
        self.assertEqual(audit.check(), ())

    def test_mutated_original_planos_source_rejected_by_checker(self):
        target = audit.ROOT / "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean"
        read = Path.read_bytes
        def changed(path):
            raw = read(path)
            return raw + b"\n" if path == target else raw
        with patch.object(Path, "read_bytes", changed):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
                audit.check(),
            )


if __name__ == "__main__":
    unittest.main()
