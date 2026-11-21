"""v0.56 common-ancestor successors: detect local incomparable branches."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_common_ancestor_fork_v0_56 as subject,
    kuuos_lean_python_prior_checkpoint_prefix_v0_55 as prior,
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
from scripts import check_kuuos_lean_python_common_ancestor_sources_v0_56 as audit


class CommonAncestorForkV056Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def _commit(self, path, route="retain", seq=None, nonce=None):
        v, p = deepcopy(self.native[route])
        claims = two_claims(v, p)
        receipts = (fixtures_mac_claims(claims) if seq is None else
                    fixtures_mac_claims(claims, seq=seq, nonce=nonce))
        result = replay.reserve_verified_mac_pair_locally(
            v, p, claims, receipts,
            verification_keys=KEYS, expected_context=CONTEXT,
            expected_sequences=seq if seq is not None else SEQ,
            ledger_path=path,
        )
        self.assertTrue(result.local_reservation_committed, result)
        return result

    def _manifest(self, path):
        result = detached.export_detached_local_replay_witness(path)
        self.assertEqual(result.status, detached.DETACHED_EXPORTED)
        return result.manifest

    def _fork(self, route="retain"):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            ancestor_db = root / "ancestor.sqlite"
            left_db = root / "left.sqlite"
            right_db = root / "right.sqlite"
            self._commit(ancestor_db, route)
            old = self._manifest(ancestor_db)
            shutil.copyfile(ancestor_db, left_db)
            shutil.copyfile(ancestor_db, right_db)
            self._commit(left_db, route,
                         seq={"first": 9, "second": 10},
                         nonce={"first": "00000000000000000000000000000111",
                                "second": "00000000000000000000000000000222"})
            self._commit(right_db, route,
                         seq={"first": 11, "second": 12},
                         nonce={"first": "00000000000000000000000000000333",
                                "second": "00000000000000000000000000000444"})
            left, right = self._manifest(left_db), self._manifest(right_db)
            return old, left, right

    def test_six_native_routes_yield_local_fork_only(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                old, left, right = self._fork(route)
                z = subject.audit_two_local_successors(old, left, right)
                self.assertEqual(z.status, subject.LOCAL_FORK)
                self.assertTrue(z.both_strictly_extend_ancestor)
                self.assertTrue(z.local_fork_observed)
                self.assertFalse(z.successor_histories_comparable)
                self.assertFalse(z.independent_checkpoint_custody_authenticated)
                self.assertFalse(z.historical_source_authenticated)
                self.assertFalse(z.host_execution_authorized)
                self.assertIsNone(z.selected_successor)
                self.assertEqual((z.ancestor_entry_count,
                                  z.left_entry_count,z.right_entry_count),(2,4,4))
                self.assertEqual(z.first_divergent_entry_id, 3)

    def test_same_successor_twice_is_not_fork(self):
        old, left, _ = self._fork()
        z = subject.audit_two_local_successors(old, left, deepcopy(left))
        self.assertEqual(z.status, subject.LOCAL_SAME)
        self.assertTrue(z.successor_histories_identical)
        self.assertTrue(z.successor_histories_comparable)
        self.assertFalse(z.local_fork_observed)

    def test_strictly_comparable_descendants_are_not_fork(self):
        old, left, _ = self._fork()
        with TemporaryDirectory() as temp:
            db = Path(temp) / "linear.sqlite"
            # v0.56 does not have access to the original detached data's DB.
            # Add a valid two-row continuation by copying the full left
            # verified row sequence into an isolated non-secret manifest.
            later = deepcopy(left)
            old_tail = deepcopy(left["entries"][-2:])
            prev = later["declared_chain_head"]
            for idx, entry in enumerate(old_tail, start=5):
                row = deepcopy(entry)
                row["entry_id"] = idx
                row["sequence"] += 20
                row["nonce_hex"] = f"{800 + idx:032x}"
                row["previous_row_sha256"] = prev
                row["row_sha256"] = replay._hash_row(
                    prev, row["key_id"], row["context_id"], row["sequence"],
                    row["nonce_hex"], row["message_sha256"],
                )
                later["entries"].append(row)
                prev = row["row_sha256"]
            later["declared_chain_head"] = prev
            self.assertEqual(
                detached.verify_detached_replay_witness(later).status,
                detached.DETACHED_UNANCHORED,
            )
            z = subject.audit_two_local_successors(old, left, later)
            self.assertEqual(z.status, subject.LOCAL_CHAIN)
            self.assertTrue(z.successor_histories_comparable)
            self.assertFalse(z.successor_histories_identical)
            self.assertFalse(z.local_fork_observed)

    def test_matching_caller_checkpoint_preserves_fork_obstruction(self):
        old, left, right = self._fork()
        digest = detached.verify_detached_replay_witness(old).manifest_sha256
        z = subject.audit_two_local_successors(
            old,left,right,separately_supplied_ancestor_checkpoint_sha256=digest,
        )
        self.assertEqual(z.status, subject.LOCAL_FORK)
        self.assertTrue(z.caller_prior_checkpoint_value_matches)
        self.assertTrue(z.local_fork_observed)
        self.assertFalse(z.independent_checkpoint_custody_authenticated)

    def test_wrong_caller_checkpoint_preserves_two_obstructions(self):
        old, left, right = self._fork()
        z = subject.audit_two_local_successors(
            old,left,right,
            separately_supplied_ancestor_checkpoint_sha256="f"*64,
        )
        self.assertEqual(z.status, subject.LOCAL_FORK_AND_CHECKPOINT)
        self.assertTrue(z.local_fork_observed)
        self.assertIn("caller_prior_checkpoint_value_disagrees",z.issues)
        self.assertIn("incompatible_declared_successor_histories",z.issues)

    def test_wrong_checkpoint_even_with_comparable_descendants(self):
        old,left,_=self._fork()
        z=subject.audit_two_local_successors(
            old,left,deepcopy(left),
            separately_supplied_ancestor_checkpoint_sha256="f"*64,
        )
        self.assertEqual(z.status,subject.LOCAL_CHECKPOINT)
        self.assertFalse(z.local_fork_observed)

    def test_incorrect_checkpoint_shape_blocks(self):
        old,left,right=self._fork()
        for bad in (True,42,0.0,"","g"*64,"0"*63,"F"*64):
            with self.subTest(value=bad):
                z=subject.audit_two_local_successors(
                    old,left,right,separately_supplied_ancestor_checkpoint_sha256=bad)
                self.assertEqual(z.status,BLOCKED)

    def test_missing_input_preserves_no_data(self):
        old,left,right=self._fork()
        for x,y,z in ((None,left,right),(old,None,right),(old,left,None)):
            self.assertEqual(subject.audit_two_local_successors(x,y,z).status,NO_DATA)

    def test_nonmapping_and_invalid_snapshot_blocked(self):
        old,left,right=self._fork()
        for invalid in ([],42,"{}",tuple()):
            self.assertEqual(
                subject.audit_two_local_successors(invalid,left,right).status,
                BLOCKED)
        bad=deepcopy(right)
        bad["entries"][0]["row_sha256"]="a"*64
        self.assertEqual(subject.audit_two_local_successors(old,left,bad).status,
                         BLOCKED)

    def test_noncommon_ancestor_is_obstruction_not_fork(self):
        old,left,right=self._fork()
        z=subject.audit_two_local_successors(left,old,right)
        self.assertEqual(z.status,subject.LOCAL_ANCESTOR)
        self.assertFalse(z.both_strictly_extend_ancestor)
        self.assertFalse(z.local_fork_observed)

    def test_rewriting_only_right_common_rows_blocks_shared_ancestor(self):
        old,left,right=self._fork()
        fake=deepcopy(right)
        fake["entries"][0]["message_sha256"]="a"*64
        prev=replay.GENESIS
        for row in fake["entries"]:
            row["previous_row_sha256"]=prev
            row["row_sha256"]=replay._hash_row(
                prev,row["key_id"],row["context_id"],row["sequence"],
                row["nonce_hex"],row["message_sha256"])
            prev=row["row_sha256"]
        fake["declared_chain_head"]=prev
        self.assertEqual(detached.verify_detached_replay_witness(fake).status,
                         detached.DETACHED_UNANCHORED)
        z=subject.audit_two_local_successors(old,left,fake)
        self.assertEqual(z.status,subject.LOCAL_ANCESTOR)
        self.assertFalse(z.local_fork_observed)

    def test_call_does_not_change_manifest_objects(self):
        old,left,right=self._fork()
        originals=deepcopy((old,left,right))
        subject.audit_two_local_successors(old,left,right)
        self.assertEqual((old,left,right),originals)

    def test_no_sqlite_or_original_kernel_reexecution(self):
        old,left,right=self._fork()
        with patch.object(
            sqlite3,"connect",side_effect=AssertionError("no DB"),
        ),patch.object(
            verify,"build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("no VerifyOS"),
        ),patch.object(
            plan,"build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("no PlanOS"),
        ):
            result=subject.audit_two_local_successors(old,left,right)
        self.assertEqual(result.status,subject.LOCAL_FORK)
        self.assertEqual(result.native_kernel_invocations,0)

    def test_no_raw_hmac_keys_or_claims_in_detached_snapshots(self):
        old,left,right=self._fork()
        raw=json.dumps([old,left,right]).encode("ascii")
        self.assertNotIn(b"mac_sha256",raw)
        for secret in KEYS.values():
            self.assertNotIn(secret,raw)

    def test_fork_stays_proposal_and_cannot_select_any_successor(self):
        old,left,right=self._fork()
        result=subject.audit_two_local_successors(old,left,right)
        self.assertFalse(result.independent_issuers_authenticated)
        self.assertFalse(result.cross_host_replay_protected)
        self.assertFalse(result.original_lean_match_proved)
        self.assertFalse(result.global_descent_certified)
        self.assertFalse(result.host_execution_authorized)
        self.assertIsNone(result.selected_successor)
        self.assertEqual(result.original_plan_result_state,NO_DATA)

    def test_source_checker_passes(self):
        self.assertEqual(audit.check(),())

    def test_mutated_v055_original_source_is_rejected(self):
        path=audit.ROOT/"formal/KUOS/Architecture/LeanPythonPriorCheckpointPrefixBoundaryV0_55.lean"
        read=Path.read_bytes
        def altered(p):
            raw=read(p)
            return raw+b"\n" if p==path else raw
        with patch.object(Path,"read_bytes",altered):
            self.assertIn("changed_pinned_source:formal/KUOS/Architecture/LeanPythonPriorCheckpointPrefixBoundaryV0_55.lean",audit.check())


if __name__=="__main__":
    unittest.main()
