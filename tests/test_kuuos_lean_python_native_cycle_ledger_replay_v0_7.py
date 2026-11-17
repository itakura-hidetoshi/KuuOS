"""Genuine, single-origin v1.3 native fixture ledger-replay integration tests.

Only the checker/mismatch tests use mocks. The positive suite executes the
existing bounded local native fixture builder once in an isolated temp dir,
and then audits that same persisted evidence without invoking a host.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime.kuuos_lean_python_native_cycle_ledger_replay_v0_7 import (
    SUCCESS, BLOCKED, NO_DATA, MODE, audit_native_cycle_ledger,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, full_cycle_receipt_digest,
    validate_native_full_cycle_receipt,
)
from scripts.check_kuuos_lean_python_native_cycle_sources_v0_7 import (
    ROOT, SOURCE_GIT_BLOBS, check_sources,
)


class SourcePinTests(unittest.TestCase):
    def test_exact_original_native_builder_bytes_unchanged(self):
        self.assertEqual(len(SOURCE_GIT_BLOBS), 8)
        self.assertEqual(check_sources(ROOT), ())

    def test_fake_source_modification_does_not_pass(self):
        with TemporaryDirectory(prefix="kuuos-v07-source-drift-") as folder:
            root = Path(folder)
            first = next(iter(SOURCE_GIT_BLOBS))
            path = root / first
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("edited original builder\n", encoding="utf-8")
            errors = check_sources(root)
            self.assertIn("source_byte_drift:" + first, errors)
            self.assertTrue(any("source_missing:" in item for item in errors))

    def test_no_missing_source_is_treated_as_success(self):
        with TemporaryDirectory() as folder:
            self.assertTrue(check_sources(Path(folder)))


class NativeCycleLedgerReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-lean-python-native-v07-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.receipt = build_native_full_cycle_receipt(cls.root)
        errors = validate_native_full_cycle_receipt(cls.receipt)
        if errors:
            raise AssertionError(("original_native_full_cycle_fixture_invalid", errors))

    def test_real_eight_os_source_and_actual_act_ledger_are_joined(self):
        result = audit_native_cycle_ledger(self.root, self.receipt)
        self.assertEqual(result.status, SUCCESS, (result.issues, result.missing))
        self.assertTrue(result.scoped_native_fixture_replay_completed)
        self.assertGreater(result.ledger_commit_count, 0)
        self.assertEqual(len(result.segments), 3)
        self.assertEqual(
            [name for name, _ in result.segments],
            ["DecisionOS->PlanOS", "PlanOS->ActOS(initial)", "ActOS(final)->LearnOS"],
        )
        for label, audit in result.segments:
            with self.subTest(segment=label):
                self.assertEqual(audit.status, "SCOPED_PATH_CHECKED",
                                 (audit.status, audit.violations, audit.missing))
                self.assertTrue(audit.local_python_checks_completed)
        self.assertEqual(
            result.act_final_digest,
            self.receipt["native_artifacts"]["ActOS"]["act_state_digest"],
        )
        self.assertEqual(
            result.wa_activation_digest,
            self.receipt["native_artifacts"]["PlanOS"]["replan_activation_receipt_digest"],
        )
        self.assertEqual(
            result.plan_activation_digest,
            self.receipt["native_artifacts"]["ActOS"]["plan_activation_receipt_digest"],
        )

    def test_original_receipt_and_stored_act_files_are_not_mutated(self):
        before = deepcopy(self.receipt)
        act_root = self.root / "act"
        names = ("act-genesis.json", "act-ledger.jsonl", "act-snapshot.json")
        file_before = {name: (act_root / name).read_bytes() for name in names}
        result = audit_native_cycle_ledger(self.root, self.receipt)
        self.assertEqual(result.status, SUCCESS, result)
        self.assertEqual(self.receipt, before)
        self.assertEqual(
            {name: (act_root / name).read_bytes() for name in names},
            file_before,
        )

    def test_no_external_or_proof_authority_claim_from_success(self):
        audit = audit_native_cycle_ledger(self.root, self.receipt)
        self.assertEqual(audit.status, SUCCESS, audit)
        self.assertFalse(audit.formal_descent_certified)
        self.assertFalse(audit.lean_python_refinement_proved)
        self.assertFalse(audit.external_receipt_authenticated)
        self.assertFalse(audit.execution_authority_granted)
        self.assertFalse(audit.truth_authority_granted)
        self.assertFalse(audit.merge_authority_granted)
        self.assertEqual(audit.receipt_evidence_mode, MODE)

    def test_no_packet_remains_no_data(self):
        result = audit_native_cycle_ledger(self.root, None)
        self.assertEqual(result.status, NO_DATA)
        self.assertEqual(result.segments, ())

    def test_absent_persisted_act_store_remains_no_data(self):
        with TemporaryDirectory(prefix="kuuos-v07-absent-") as directory:
            result = audit_native_cycle_ledger(Path(directory), self.receipt)
        self.assertEqual(result.status, NO_DATA)
        self.assertIn("actual_act_store:genesis_ledger_snapshot_missing", result.missing)

    def test_untrusted_non_path_root_cannot_be_used(self):
        result = audit_native_cycle_ledger(str(self.root), self.receipt)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("root:trusted_path_required", result.issues)

    def test_receipt_substitution_preserves_blocker_even_with_outer_reseal(self):
        for os_name, field in (
            ("PlanOS", "source_wa_state_digest"),
            ("ActOS", "source_plan_state_digest"),
            ("ObserveOS", "source_act_state_digest"),
            ("VerifyOS", "source_observe_state_digest"),
            ("LearnOS", "source_verify_state_digest"),
        ):
            with self.subTest(os=os_name):
                packet = deepcopy(self.receipt)
                packet["native_artifacts"][os_name][field] = "f" * 64
                packet["native_full_cycle_receipt_digest"] = full_cycle_receipt_digest(packet)
                result = audit_native_cycle_ledger(self.root, packet)
                self.assertEqual(result.status, BLOCKED, result)

    def test_source_reconstruction_constants_cannot_be_silently_changed(self):
        from runtime import kuuos_lean_python_native_cycle_ledger_replay_v0_7 as mod
        from runtime.kuuos_belief_os_types_v0_1 import sha as original_sha

        def altered_sha(value):
            if value == "native-full-cycle-next-plan-basis":
                return original_sha("tampered-next-plan-basis")
            return original_sha(value)

        with patch.object(mod, "sha", side_effect=altered_sha):
            result = audit_native_cycle_ledger(self.root, self.receipt)
        self.assertEqual(result.status, BLOCKED, result)
        self.assertIn("plan:wa_receipt_digest_not_reproducible", result.issues)

    def test_bad_outer_receipt_digest_fails_closed(self):
        packet = deepcopy(self.receipt)
        packet["native_full_cycle_receipt_digest"] = "0" * 64
        result = audit_native_cycle_ledger(self.root, packet)
        self.assertEqual(result.status, BLOCKED)

    def test_copied_native_store_with_invalid_event_is_rejected(self):
        with TemporaryDirectory(prefix="kuuos-v07-corrupt-event-") as folder:
            root = Path(folder)
            copied = root / "act"
            shutil.copytree(self.root / "act", copied)
            path = copied / "act-ledger.jsonl"
            rows = path.read_text(encoding="utf-8").splitlines()
            entry = json.loads(rows[0])
            entry["event"]["target_phase"] = "commit"
            rows[0] = json.dumps(entry, sort_keys=True)
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            result = audit_native_cycle_ledger(root, self.receipt)
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(any("act_store:original_replay_exception" in issue
                            for issue in result.issues))

    def test_copied_native_store_with_wrong_snapshot_is_rejected(self):
        with TemporaryDirectory(prefix="kuuos-v07-corrupt-snapshot-") as folder:
            root = Path(folder)
            copied = root / "act"
            shutil.copytree(self.root / "act", copied)
            path = copied / "act-snapshot.json"
            snapshot = json.loads(path.read_text(encoding="utf-8"))
            snapshot["act_id"] = "substituted-act-id"
            path.write_text(json.dumps(snapshot) + "\n", encoding="utf-8")
            result = audit_native_cycle_ledger(root, self.receipt)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("act_store:snapshot_not_equal_to_replay", result.issues)

    def test_copied_native_store_with_wrong_genesis_is_rejected(self):
        with TemporaryDirectory(prefix="kuuos-v07-corrupt-genesis-") as folder:
            root = Path(folder)
            copied = root / "act"
            shutil.copytree(self.root / "act", copied)
            path = copied / "act-genesis.json"
            genesis = json.loads(path.read_text(encoding="utf-8"))
            genesis["act_id"] = "substituted-act-id"
            path.write_text(json.dumps(genesis) + "\n", encoding="utf-8")
            result = audit_native_cycle_ledger(root, self.receipt)
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(any("act_store:original_replay_exception" in issue
                            for issue in result.issues))

    def test_bad_json_or_wrong_receipt_type_fails_closed(self):
        for bad in ([], object(), {"no_data": float("nan")}, {"cycle": object()}):
            with self.subTest(kind=type(bad).__name__):
                result = audit_native_cycle_ledger(self.root, bad)
                self.assertEqual(result.status, BLOCKED)

    def test_missing_or_changed_native_inventory_is_not_promoted(self):
        packet = deepcopy(self.receipt)
        del packet["native_artifacts"]["DecisionOSPlural"]
        packet["native_full_cycle_receipt_digest"] = full_cycle_receipt_digest(packet)
        result = audit_native_cycle_ledger(self.root, packet)
        self.assertEqual(result.status, BLOCKED)

    def test_deterministic_result_is_tied_to_exact_native_cycle_receipt(self):
        a = audit_native_cycle_ledger(self.root, self.receipt)
        b = audit_native_cycle_ledger(self.root, self.receipt)
        self.assertEqual(a, b)
        self.assertEqual(a.status, SUCCESS)
        self.assertIsInstance(a.receipt_digest, str)
        self.assertEqual(len(a.receipt_digest), 64)


if __name__ == "__main__":
    unittest.main()
