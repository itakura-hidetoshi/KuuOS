"""v0.54: independent recomputation of detached LOCAL replay observations."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_detached_replay_witness_v0_54 as subject,
    kuuos_lean_python_local_replay_reservation_v0_53 as replay,
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
    KEYS, CONTEXT, SEQ, fixtures_mac_claims,
)
from scripts import check_kuuos_lean_python_detached_replay_sources_v0_54 as audit


class DetachedReplayV054Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def _record(self, path, route="retain"):
        v, p = deepcopy(self.native[route])
        claims = two_claims(v, p)
        receipts = fixtures_mac_claims(claims)
        result = replay.reserve_verified_mac_pair_locally(
            v, p, claims, receipts, verification_keys=KEYS,
            expected_context=CONTEXT, expected_sequences=SEQ,
            ledger_path=path,
        )
        self.assertTrue(result.local_reservation_committed, result)
        return v, p, claims, receipts

    def _export(self, route="retain"):
        return TemporaryDirectory()

    def _fixture(self):
        temp = TemporaryDirectory()
        path = Path(temp.name) / "ledger.sqlite3"
        self._record(path)
        result = subject.export_detached_local_replay_witness(path)
        self.assertEqual(result.status, subject.DETACHED_EXPORTED)
        self.assertIsNotNone(result.manifest)
        return temp, path, result

    def test_six_native_routes_export_and_offline_replay(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route), TemporaryDirectory() as d:
                path = Path(d) / "ledger.sqlite3"
                self._record(path, route)
                result = subject.export_detached_local_replay_witness(path)
                self.assertEqual(result.status, subject.DETACHED_EXPORTED)
                self.assertEqual(result.entry_count, 2)
                detached = json.loads(json.dumps(result.manifest))
                path.unlink()
                check = subject.verify_detached_replay_witness(detached)
                self.assertEqual(check.status, subject.DETACHED_UNANCHORED)
                self.assertEqual(check.manifest_sha256, result.manifest_sha256)
                self.assertEqual(check.chain_head, result.chain_head)
                self.assertTrue(check.local_chain_recomputed)
                self.assertEqual(check.original_plan_result_state, NO_DATA)

    def test_export_does_not_write_database_bytes(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "ledger.db"
            self._record(path)
            before = path.read_bytes()
            witness = subject.export_detached_local_replay_witness(path)
            self.assertEqual(witness.status, subject.DETACHED_EXPORTED)
            self.assertEqual(path.read_bytes(), before)

    def test_caller_supplied_matching_checkpoint_is_only_value_equality(self):
        temp, _, exported = self._fixture()
        try:
            result = subject.verify_detached_replay_witness(
                exported.manifest,
                separately_supplied_checkpoint_sha256=exported.manifest_sha256,
            )
            self.assertEqual(result.status, subject.CHECKPOINT_MATCH)
            self.assertTrue(result.caller_checkpoint_value_matches)
            self.assertFalse(result.independent_checkpoint_custody_authenticated)
            self.assertFalse(result.external_issuers_authenticated)
            self.assertFalse(result.cross_host_replay_protected)
            self.assertFalse(result.global_descent_certified)
            self.assertFalse(result.host_execution_authorized)
        finally:
            temp.cleanup()

    def test_caller_supplied_conflicting_checkpoint_is_obstruction(self):
        temp, _, exported = self._fixture()
        try:
            result = subject.verify_detached_replay_witness(
                exported.manifest,
                separately_supplied_checkpoint_sha256="f" * 64,
            )
            self.assertEqual(result.status, subject.CHECKPOINT_MISMATCH)
            self.assertTrue(result.local_chain_recomputed)
            self.assertFalse(result.caller_checkpoint_value_matches)
        finally:
            temp.cleanup()

    def test_missing_checkpoint_remains_unanchored(self):
        temp, _, exported = self._fixture()
        try:
            result = subject.verify_detached_replay_witness(exported.manifest)
            self.assertEqual(result.status, subject.DETACHED_UNANCHORED)
            self.assertFalse(result.caller_checkpoint_value_matches)
        finally:
            temp.cleanup()

    def test_malformed_external_checkpoint_is_blocked(self):
        temp, _, exported = self._fixture()
        try:
            for bad in (True, 99, "", "G" * 64, "0" * 63, "A" * 64):
                with self.subTest(bad=bad):
                    result = subject.verify_detached_replay_witness(
                        exported.manifest,
                        separately_supplied_checkpoint_sha256=bad,
                    )
                    self.assertEqual(result.status, BLOCKED)
        finally:
            temp.cleanup()

    def test_chain_row_mutation_fails_closed(self):
        temp, _, exported = self._fixture()
        try:
            for key, val in (
                ("message_sha256", "a" * 64),
                ("previous_row_sha256", "b" * 64),
                ("row_sha256", "c" * 64),
            ):
                with self.subTest(key=key):
                    changed = deepcopy(exported.manifest)
                    changed["entries"][0][key] = val
                    self.assertEqual(
                        subject.verify_detached_replay_witness(changed).status,
                        BLOCKED,
                    )
        finally:
            temp.cleanup()

    def test_head_mutation_fails_closed(self):
        temp, _, exported = self._fixture()
        try:
            changed = deepcopy(exported.manifest)
            changed["declared_chain_head"] = "e" * 64
            self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                             BLOCKED)
        finally:
            temp.cleanup()

    def test_duplicate_key_and_nonce_fail_even_with_recomputed_chain(self):
        temp, _, exported = self._fixture()
        try:
            changed = deepcopy(exported.manifest)
            changed["entries"][1]["key_id"] = changed["entries"][0]["key_id"]
            changed["entries"][1]["context_id"] = changed["entries"][0]["context_id"]
            changed["entries"][1]["sequence"] = changed["entries"][0]["sequence"]
            changed["entries"][1]["nonce_hex"] = changed["entries"][0]["nonce_hex"]
            first = changed["entries"][0]["row_sha256"]
            changed["entries"][1]["previous_row_sha256"] = first
            changed["entries"][1]["row_sha256"] = replay._hash_row(
                first, changed["entries"][1]["key_id"],
                changed["entries"][1]["context_id"],
                changed["entries"][1]["sequence"],
                changed["entries"][1]["nonce_hex"],
                changed["entries"][1]["message_sha256"],
            )
            changed["declared_chain_head"] = changed["entries"][1]["row_sha256"]
            self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                             BLOCKED)
        finally:
            temp.cleanup()

    def test_discontinuous_entry_ids_and_partial_pair_are_blocked(self):
        temp, _, exported = self._fixture()
        try:
            changed = deepcopy(exported.manifest)
            changed["entries"][1]["entry_id"] = 7
            self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                             BLOCKED)
            changed = deepcopy(exported.manifest)
            changed["entries"].pop()
            self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                             BLOCKED)
        finally:
            temp.cleanup()

    def test_noninteger_and_nonpositive_sequences_are_blocked(self):
        temp, _, exported = self._fixture()
        try:
            for val in (False, 0, -1, 1.0, "1"):
                changed = deepcopy(exported.manifest)
                changed["entries"][0]["sequence"] = val
                self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                                 BLOCKED)
        finally:
            temp.cleanup()

    def test_modified_schema_or_extra_field_rejected(self):
        temp, _, exported = self._fixture()
        try:
            for key in ("schema", "source_boundary", "chain_domain", "genesis"):
                changed = deepcopy(exported.manifest)
                changed[key] = "forged"
                self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                                 BLOCKED)
            changed = deepcopy(exported.manifest)
            changed["authority"] = True
            self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                             BLOCKED)
            changed = deepcopy(exported.manifest)
            changed["entries"][0]["mac_secret"] = "pretend"
            self.assertEqual(subject.verify_detached_replay_witness(changed).status,
                             BLOCKED)
        finally:
            temp.cleanup()

    def test_rewritten_complete_chain_detected_only_with_old_checkpoint(self):
        temp, _, exported = self._fixture()
        try:
            forged = deepcopy(exported.manifest)
            forged["entries"][0]["message_sha256"] = "a" * 64
            previous = replay.GENESIS
            for entry in forged["entries"]:
                entry["previous_row_sha256"] = previous
                entry["row_sha256"] = replay._hash_row(
                    previous, entry["key_id"], entry["context_id"],
                    entry["sequence"], entry["nonce_hex"],
                    entry["message_sha256"],
                )
                previous = entry["row_sha256"]
            forged["declared_chain_head"] = previous
            self.assertEqual(
                subject.verify_detached_replay_witness(forged).status,
                subject.DETACHED_UNANCHORED,
            )
            with_checkpoint = subject.verify_detached_replay_witness(
                forged, separately_supplied_checkpoint_sha256=exported.manifest_sha256,
            )
            self.assertEqual(with_checkpoint.status, subject.CHECKPOINT_MISMATCH)
            self.assertFalse(with_checkpoint.independent_checkpoint_custody_authenticated)
        finally:
            temp.cleanup()

    def test_missing_evidence_and_ledger_path_are_no_data(self):
        self.assertEqual(subject.verify_detached_replay_witness(None).status, NO_DATA)
        self.assertEqual(subject.export_detached_local_replay_witness(None).status,
                         NO_DATA)

    def test_relative_missing_and_symlink_paths_blocked(self):
        self.assertEqual(
            subject.export_detached_local_replay_witness(Path("relative.sqlite")).status,
            BLOCKED,
        )
        with TemporaryDirectory() as d:
            path = Path(d) / "missing.db"
            self.assertEqual(
                subject.export_detached_local_replay_witness(path).status, BLOCKED,
            )
            self._record(path)
            link = Path(d) / "symlink.sqlite"
            link.symlink_to(path)
            self.assertEqual(
                subject.export_detached_local_replay_witness(link).status, BLOCKED,
            )

    def test_tampered_db_schema_blocks_export(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "ledger.db"
            with sqlite3.connect(path) as db:
                db.execute("CREATE TABLE kuuos_plan_mac_seen_v053 (fake TEXT)")
            self.assertEqual(
                subject.export_detached_local_replay_witness(path).status, BLOCKED,
            )

    def test_no_raw_hmac_key_in_detached_manifest(self):
        temp, _, exported = self._fixture()
        try:
            raw = json.dumps(exported.manifest).encode("ascii")
            for key in KEYS.values():
                self.assertNotIn(key, raw)
            self.assertNotIn(b"mac_sha256", raw)
        finally:
            temp.cleanup()

    def test_no_native_kernel_reexecution_on_export_or_check(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "ledger.db"
            self._record(path)
            with patch.object(
                verify, "build_verifyos_middle_way_conditional_continuity_certificate",
                side_effect=AssertionError("VerifyOS rerun"),
            ), patch.object(
                plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
                side_effect=AssertionError("PlanOS rerun"),
            ):
                exported = subject.export_detached_local_replay_witness(path)
                verified = subject.verify_detached_replay_witness(
                    exported.manifest,
                    separately_supplied_checkpoint_sha256=exported.manifest_sha256,
                )
            self.assertEqual(verified.status, subject.CHECKPOINT_MATCH)
            self.assertEqual(verified.native_kernel_invocations, 0)

    def test_source_static_integrity_checker(self):
        self.assertEqual(audit.check(), ())

    def test_pinned_v053_source_mutation_is_detected(self):
        target = audit.ROOT / (
            "formal/KUOS/Architecture/LeanPythonLocalReplayLedgerBoundaryV0_53.lean"
        )
        read = Path.read_bytes

        def tampered(path):
            raw = read(path)
            return raw + b"\n" if path == target else raw

        with patch.object(Path, "read_bytes", tampered):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/Architecture/"
                "LeanPythonLocalReplayLedgerBoundaryV0_53.lean",
                audit.check(),
            )


if __name__ == "__main__":
    unittest.main()
