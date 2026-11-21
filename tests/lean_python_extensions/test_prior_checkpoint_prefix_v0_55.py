"""v0.55: strict two-snapshot local prefix and separate prior checkpoint."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_prior_checkpoint_prefix_v0_55 as subject,
    kuuos_lean_python_detached_replay_witness_v0_54 as detached,
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
from scripts import check_kuuos_lean_python_prior_checkpoint_sources_v0_55 as audit


class PriorCheckpointPrefixV055Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def _reserve(self, path, route="retain", *, sequences=None, nonces=None):
        v, p = deepcopy(self.native[route])
        claims = two_claims(v, p)
        if sequences is None:
            sequences = SEQ
            receipts = fixtures_mac_claims(claims)
        else:
            receipts = fixtures_mac_claims(claims, seq=sequences, nonce=nonces)
        result = replay.reserve_verified_mac_pair_locally(
            v, p, claims, receipts, verification_keys=KEYS,
            expected_context=CONTEXT, expected_sequences=sequences,
            ledger_path=path,
        )
        self.assertTrue(result.local_reservation_committed, result)
        return result

    @staticmethod
    def _manifest(path):
        report = detached.export_detached_local_replay_witness(path)
        assert report.status == detached.DETACHED_EXPORTED, report
        assert report.manifest is not None
        return report.manifest

    def _snapshots(self, route="retain", total_pairs=2):
        assert total_pairs >= 2
        with TemporaryDirectory() as d:
            path = Path(d) / "ledger.sqlite3"
            self._reserve(path, route)
            old = self._manifest(path)
            for index in range(1, total_pairs):
                sequences = {
                    "first": 7 + 2 * index,
                    "second": 8 + 2 * index,
                }
                nonces = {
                    "first": f"{100 + index:032x}",
                    "second": f"{200 + index:032x}",
                }
                self._reserve(
                    path, route, sequences=sequences, nonces=nonces,
                )
            new = self._manifest(path)
            return old, new

    @staticmethod
    def _rehash(manifest):
        previous = replay.GENESIS
        for entry in manifest["entries"]:
            entry["previous_row_sha256"] = previous
            entry["row_sha256"] = replay._hash_row(
                previous, entry["key_id"], entry["context_id"],
                entry["sequence"], entry["nonce_hex"], entry["message_sha256"],
            )
            previous = entry["row_sha256"]
        manifest["declared_chain_head"] = previous

    def test_six_original_routes_have_strict_unanchored_extension(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                past, current = self._snapshots(route)
                z = subject.audit_local_prior_checkpoint_prefix(past, current)
                self.assertEqual(z.status, subject.PREFIX_UNANCHORED)
                self.assertEqual((z.old_entry_count, z.new_entry_count), (2, 4))
                self.assertEqual(z.added_complete_pairs, 1)
                self.assertTrue(z.older_snapshot_recomputed)
                self.assertTrue(z.newer_snapshot_recomputed)
                self.assertTrue(z.exact_ordered_prefix_compatible)
                self.assertTrue(z.strict_local_extension)
                self.assertFalse(z.caller_prior_checkpoint_value_matches)
                self.assertFalse(z.independent_checkpoint_custody_authenticated)
                self.assertFalse(z.historical_receipt_authenticated)
                self.assertFalse(z.host_execution_authorized)
                self.assertEqual(z.original_plan_result_state, NO_DATA)

    def test_explicit_matching_prior_manifest_checkpoint_is_value_only(self):
        past, current = self._snapshots()
        prior_digest = detached.verify_detached_replay_witness(past).manifest_sha256
        z = subject.audit_local_prior_checkpoint_prefix(
            past, current, separately_supplied_prior_checkpoint_sha256=prior_digest,
        )
        self.assertEqual(z.status, subject.PREFIX_CHECKPOINT_VALUE_MATCH)
        self.assertTrue(z.caller_prior_checkpoint_value_matches)
        self.assertTrue(z.strict_local_extension)
        self.assertEqual(z.old_manifest_sha256, prior_digest)
        self.assertFalse(z.independent_checkpoint_custody_authenticated)
        self.assertFalse(z.external_issuers_authenticated)
        self.assertFalse(z.cross_host_replay_protected)
        self.assertFalse(z.global_descent_certified)
        self.assertFalse(z.host_execution_authorized)

    def test_distinct_valid_caller_prior_checkpoint_is_obstruction(self):
        past, current = self._snapshots()
        z = subject.audit_local_prior_checkpoint_prefix(
            past, current, separately_supplied_prior_checkpoint_sha256="f" * 64,
        )
        self.assertEqual(z.status, subject.PREFIX_CHECKPOINT_MISMATCH)
        self.assertTrue(z.strict_local_extension)
        self.assertFalse(z.caller_prior_checkpoint_value_matches)
        self.assertIn("caller_prior_checkpoint_value_disagrees", z.issues)

    def test_invalid_checkpoint_types_fail_closed(self):
        past, current = self._snapshots()
        for bad in (False, 15, 1.0, "", "g" * 64, "F" * 64, "0" * 63):
            with self.subTest(bad=bad):
                z = subject.audit_local_prior_checkpoint_prefix(
                    past, current,
                    separately_supplied_prior_checkpoint_sha256=bad,
                )
                self.assertEqual(z.status, BLOCKED)
                self.assertFalse(z.caller_prior_checkpoint_value_matches)

    def test_equal_history_is_not_a_strict_extension_even_with_matching_digest(self):
        past, _ = self._snapshots()
        digest = detached.verify_detached_replay_witness(past).manifest_sha256
        z = subject.audit_local_prior_checkpoint_prefix(
            past, deepcopy(past),
            separately_supplied_prior_checkpoint_sha256=digest,
        )
        self.assertEqual(z.status, subject.PREFIX_NO_NEW_ROWS)
        self.assertTrue(z.exact_ordered_prefix_compatible)
        self.assertFalse(z.strict_local_extension)
        self.assertTrue(z.caller_prior_checkpoint_value_matches)
        self.assertEqual(z.added_complete_pairs, 0)

    def test_truncated_history_preserves_obstructions(self):
        past, current = self._snapshots()
        z = subject.audit_local_prior_checkpoint_prefix(current, past)
        self.assertEqual(z.status, subject.PREFIX_COMPOSITE_OBSTRUCTION)
        self.assertFalse(z.strict_local_extension)
        self.assertIn("no_new_complete_pair_after_prior_snapshot", z.issues)
        self.assertIn("old_rows_not_exact_ordered_prefix", z.issues)

    def test_full_history_rehash_in_new_snapshot_only_is_divergence(self):
        past, current = self._snapshots()
        altered = deepcopy(current)
        altered["entries"][0]["message_sha256"] = "a" * 64
        self._rehash(altered)
        self.assertEqual(detached.verify_detached_replay_witness(altered).status,
                         detached.DETACHED_UNANCHORED)
        z = subject.audit_local_prior_checkpoint_prefix(past, altered)
        self.assertEqual(z.status, subject.PREFIX_DIVERGENCE)
        self.assertFalse(z.exact_ordered_prefix_compatible)
        self.assertFalse(z.strict_local_extension)
        self.assertIn("old_rows_not_exact_ordered_prefix", z.issues)

    def test_prefix_rewrite_plus_wrong_prior_checkpoint_preserves_both_obstructions(self):
        past, current = self._snapshots()
        altered = deepcopy(current)
        altered["entries"][0]["message_sha256"] = "a" * 64
        self._rehash(altered)
        z = subject.audit_local_prior_checkpoint_prefix(
            past, altered, separately_supplied_prior_checkpoint_sha256="f" * 64,
        )
        self.assertEqual(z.status, subject.PREFIX_COMPOSITE_OBSTRUCTION)
        self.assertIn("old_rows_not_exact_ordered_prefix", z.issues)
        self.assertIn("caller_prior_checkpoint_value_disagrees", z.issues)

    def test_both_manifests_rewritten_with_rehashed_chains_are_unanchored(self):
        past, current = self._snapshots()
        prior_hash = detached.verify_detached_replay_witness(past).manifest_sha256
        fake_past, fake_current = deepcopy(past), deepcopy(current)
        for candidate in (fake_past, fake_current):
            candidate["entries"][0]["message_sha256"] = "a" * 64
            self._rehash(candidate)
        z = subject.audit_local_prior_checkpoint_prefix(fake_past, fake_current)
        self.assertEqual(z.status, subject.PREFIX_UNANCHORED)
        self.assertTrue(z.strict_local_extension)
        self.assertFalse(z.historical_receipt_authenticated)
        anchored = subject.audit_local_prior_checkpoint_prefix(
            fake_past, fake_current,
            separately_supplied_prior_checkpoint_sha256=prior_hash,
        )
        self.assertEqual(anchored.status, subject.PREFIX_CHECKPOINT_MISMATCH)
        self.assertFalse(anchored.independent_checkpoint_custody_authenticated)

    def test_two_additional_pairs_report_exact_count(self):
        past, current = self._snapshots(total_pairs=3)
        z = subject.audit_local_prior_checkpoint_prefix(past, current)
        self.assertEqual(z.status, subject.PREFIX_UNANCHORED)
        self.assertEqual((z.old_entry_count, z.new_entry_count), (2, 6))
        self.assertEqual(z.added_complete_pairs, 2)

    def test_changed_row_without_rehash_blocks_entire_new_snapshot(self):
        past, current = self._snapshots()
        altered = deepcopy(current)
        altered["entries"][0]["message_sha256"] = "a" * 64
        z = subject.audit_local_prior_checkpoint_prefix(past, altered)
        self.assertEqual(z.status, BLOCKED)
        self.assertFalse(z.strict_local_extension)

    def test_corrupt_older_snapshot_blocks_not_descends(self):
        past, current = self._snapshots()
        altered = deepcopy(past)
        altered["entries"][0]["row_sha256"] = "a" * 64
        z = subject.audit_local_prior_checkpoint_prefix(altered, current)
        self.assertEqual(z.status, BLOCKED)
        self.assertFalse(z.older_snapshot_recomputed)

    def test_wrong_manifest_domain_rejected(self):
        past, current = self._snapshots()
        altered = deepcopy(current)
        altered["chain_domain"] = "other-world"
        z = subject.audit_local_prior_checkpoint_prefix(past, altered)
        self.assertEqual(z.status, BLOCKED)

    def test_half_committed_pair_is_not_a_valid_detached_snapshot(self):
        past, current = self._snapshots()
        altered = deepcopy(current)
        altered["entries"].pop()
        z = subject.audit_local_prior_checkpoint_prefix(past, altered)
        self.assertEqual(z.status, BLOCKED)

    def test_old_snapshot_missing_stays_no_data(self):
        _, current = self._snapshots()
        self.assertEqual(
            subject.audit_local_prior_checkpoint_prefix(None, current).status,
            NO_DATA,
        )
        self.assertEqual(
            subject.audit_local_prior_checkpoint_prefix(current, None).status,
            NO_DATA,
        )

    def test_untrusted_non_dict_input_blocks(self):
        past, current = self._snapshots()
        for candidate in ([], (), "{}", 1):
            self.assertEqual(
                subject.audit_local_prior_checkpoint_prefix(candidate, current).status,
                BLOCKED,
            )
        self.assertEqual(
            subject.audit_local_prior_checkpoint_prefix(past, []).status,
            BLOCKED,
        )

    def test_original_certificates_and_manifest_are_not_mutated(self):
        past, current = self._snapshots()
        before = deepcopy((past, current))
        subject.audit_local_prior_checkpoint_prefix(past, current)
        self.assertEqual((past, current), before)

    def test_no_original_kernel_reexecution_or_network_or_database_access(self):
        past, current = self._snapshots()
        with patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("VerifyOS reexecution"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("PlanOS reexecution"),
        ), patch.object(
            sqlite3, "connect", side_effect=AssertionError("new sqlite access"),
        ):
            z = subject.audit_local_prior_checkpoint_prefix(past, current)
        self.assertEqual(z.status, subject.PREFIX_UNANCHORED)
        self.assertEqual(z.native_kernel_invocations, 0)

    def test_no_raw_mac_secrets_or_tags_in_detached_history(self):
        past, current = self._snapshots()
        raw = json.dumps((past, current), sort_keys=True).encode("ascii")
        self.assertNotIn(b"mac_sha256", raw)
        for secret in KEYS.values():
            self.assertNotIn(secret, raw)

    def test_source_integrity_uses_git_blobs(self):
        self.assertEqual(audit.check(), ())

    def test_mutated_original_v054_lean_source_is_detected(self):
        target = audit.ROOT / (
            "formal/KUOS/Architecture/LeanPythonDetachedReplayWitnessBoundaryV0_54.lean"
        )
        read = Path.read_bytes

        def tampered(path):
            raw = read(path)
            return raw + b"\n" if path == target else raw

        with patch.object(Path, "read_bytes", tampered):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/Architecture/"
                "LeanPythonDetachedReplayWitnessBoundaryV0_54.lean",
                audit.check(),
            )


if __name__ == "__main__":
    unittest.main()
