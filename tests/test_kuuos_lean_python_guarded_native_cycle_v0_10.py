"""Real native child and store-commit tests for the additive v0.10 gate.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import replace
from importlib import import_module
import json
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_checked_transition_v0_10 as checked
from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as guarded
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_FILE, GOOD, audit_isolated_evidence,
)


class GuardedNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v010-guarded-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.originals = {
            module: getattr(import_module(module), function)
            for _, module, function in guarded.STORE_BINDINGS
        }
        cls.observed_run = guarded.build_guarded_native_fixture(cls.root)

    @contextmanager
    def clone(self):
        with TemporaryDirectory(prefix="kuuos-v010-clone-") as folder:
            copied = Path(folder) / "fixture"
            shutil.copytree(self.root, copied)
            yield copied

    def test_real_child_checks_all_six_native_store_routes(self):
        self.assertEqual(self.observed_run.status, guarded.SUCCESS)
        self.assertEqual(self.observed_run.native_audit.status, GOOD)
        counts = dict(self.observed_run.guard_calls)
        self.assertEqual(tuple(counts), guarded.GUARDED_OS)
        self.assertTrue(all(type(n) is int and n > 0 for n in counts.values()))
        self.assertTrue(self.observed_run.counts_include_recovery_replays)
        self.assertGreater(counts["ActOS"],
                           self.observed_run.native_audit.local_audit.native_replay.ledger_commit_count)
        self.assertEqual(audit_isolated_evidence(self.root), self.observed_run.native_audit)

    def test_parent_keeps_all_original_store_bindings(self):
        for _, module, function in guarded.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), function), self.originals[module])

    def test_success_does_not_grant_authority_or_pre_host_effect_guard(self):
        for field in ("pre_host_effect_guarded", "external_issuer_authenticated",
                      "historical_guard_execution_proved", "lean_python_refinement_proved",
                      "execution_authority_granted", "truth_authority_granted",
                      "git_merge_authority_granted"):
            self.assertIs(getattr(self.observed_run, field), False, field)
        self.assertEqual(self.observed_run.guard_observation_mode, "local_child_stdout_unattested")

    def test_local_audit_is_read_only_and_does_not_launch_child(self):
        paths = [p for p in self.root.rglob("*") if p.is_file()]
        before = {str(p): p.read_bytes() for p in paths}
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("audit spawned")):
            result = guarded.audit_local_evidence(self.root)
        self.assertEqual(result.status, GOOD)
        self.assertEqual(before, {str(p): p.read_bytes() for p in paths})

    def test_missing_evidence_stays_no_data(self):
        with TemporaryDirectory() as folder:
            result = guarded.audit_local_evidence(Path(folder))
        self.assertEqual(result.status, "NO_DATA")
        self.assertFalse(result.local_record_checked)

    def test_nonempty_root_rejected_before_process_and_without_overwrite(self):
        before = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("must not spawn")):
            with self.assertRaises(ValueError):
                guarded.build_guarded_native_fixture(self.root)
        self.assertEqual(before, (self.root / EVIDENCE_FILE).read_bytes())

    def test_source_drift_rejected_before_child_or_fixture_effect(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch("scripts.check_kuuos_lean_python_checked_transition_sources_v0_10.check_sources",
                       return_value=("source_byte_drift:original-kernel",)):
                with patch.object(guarded.subprocess, "run", side_effect=AssertionError("must not spawn")):
                    with self.assertRaisesRegex(ValueError, "source_preflight"):
                        guarded.build_guarded_native_fixture(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_context_restores_all_bindings_after_failure(self):
        counts = {name: 0 for name in guarded.GUARDED_OS}
        with self.assertRaisesRegex(RuntimeError, "test interruption"):
            with guarded._guard_native_stores(counts):
                for _, module, function in guarded.STORE_BINDINGS:
                    self.assertIsNot(getattr(import_module(module), function), self.originals[module])
                raise RuntimeError("test interruption")
        for _, module, function in guarded.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), function), self.originals[module])

    def test_failed_added_check_stops_real_store_journal_and_snapshot(self):
        from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
        genesis = json.loads((self.root / "decision/decision-genesis.json").read_text())
        first = json.loads((self.root / "decision/decision-ledger.jsonl").read_text().splitlines()[0])["event"]
        with TemporaryDirectory() as folder:
            store = DecisionStore(Path(folder))
            store.initialize(genesis)
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            original_check = checked.audit_core_transition
            observations = []

            def fail_after_real_kernel(*args):
                actual = original_check(*args)
                observations.append((args[3]["status"], actual.status))
                return replace(actual, status="BLOCKED", issues=("injected_checked_failure",))

            with guarded._guard_native_stores({name: 0 for name in guarded.GUARDED_OS}):
                with patch.object(checked, "audit_core_transition", side_effect=fail_after_real_kernel):
                    with self.assertRaises(checked.CheckedTransitionError):
                        store.apply(first)
            self.assertEqual(observations, [("APPLIED", "RUNTIME_CHECK_PASSED")])
            self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_original_replay_and_rejection_do_not_append_extra_commit(self):
        from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
        genesis = json.loads((self.root / "decision/decision-genesis.json").read_text())
        first = json.loads((self.root / "decision/decision-ledger.jsonl").read_text().splitlines()[0])["event"]
        with TemporaryDirectory() as folder:
            store = DecisionStore(Path(folder))
            store.initialize(genesis)
            with guarded._guard_native_stores({name: 0 for name in guarded.GUARDED_OS}):
                applied = store.apply(first)
                before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
                replayed = store.apply(first)
                invalid = deepcopy(first)
                invalid["decision_event_digest"] = "not-an-event-digest"
                rejected = store.apply(invalid)
            self.assertEqual(applied["status"], "APPLIED")
            self.assertEqual(replayed["status"], "REPLAYED")
            self.assertEqual(rejected["status"], "REJECTED")
            self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_nested_act_symlink_is_refused_before_inherited_ledger_read(self):
        with self.clone() as root:
            shutil.rmtree(root / "act")
            (root / "act").symlink_to(self.root / "act", target_is_directory=True)
            result = guarded.audit_local_evidence(root)
        self.assertEqual(result.status, "BLOCKED")
        self.assertTrue(any("symlink" in issue for issue in result.violations))

    def test_symlinked_record_or_root_is_refused(self):
        with TemporaryDirectory() as folder:
            root = Path(folder) / "link"
            root.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(guarded.audit_local_evidence(root).status, "BLOCKED")
        with self.clone() as root:
            (root / EVIDENCE_FILE).unlink()
            (root / EVIDENCE_FILE).symlink_to(self.root / EVIDENCE_FILE)
            self.assertEqual(guarded.audit_local_evidence(root).status, "BLOCKED")

    def test_special_file_is_refused_without_opening_it(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            os.mkfifo(root / "unreadable-stream")
            result = guarded.audit_local_evidence(root)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("fixture:not_regular_file_or_directory", result.violations)

    def test_child_report_cannot_omit_or_fake_an_os_count(self):
        report = guarded._make_child_report(dict(self.observed_run.guard_calls), self.observed_run.native_audit)
        for value in (0, -1, True, 1.0, "1", None):
            changed = deepcopy(report)
            changed["guard_calls"]["ActOS"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                guarded._checked_report_counts(changed, self.observed_run.native_audit)
        changed = deepcopy(report)
        del changed["guard_calls"]["PlanOS"]
        with self.assertRaises(ValueError):
            guarded._checked_report_counts(changed, self.observed_run.native_audit)

    def test_child_report_binds_scope_source_and_exact_record(self):
        report = guarded._make_child_report(dict(self.observed_run.guard_calls), self.observed_run.native_audit)
        for key, value in (("source_main", "other"), ("native_record_sha256", "other"),
                           ("pre_host_effect_guarded", True), ("counts_include_recovery_replays", False),
                           ("status", "APPLIED"), ("external_signature", "invented")):
            changed = deepcopy(report)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                guarded._checked_report_counts(changed, self.observed_run.native_audit)

    def test_unsupported_schemas_are_not_reported_as_guarded(self):
        self.assertEqual(guarded.GUARDED_OS,
                         ("DecisionOS", "PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS"))
        self.assertTrue(set(guarded.GUARDED_OS).isdisjoint(
            {"BeliefOS", "DecisionOSPlural", "DecisionOSWa", "WORLD", "MemoryOS", "CodeAI"}))

    def test_child_entry_requires_explicit_mode(self):
        self.assertEqual(guarded.main([]), 2)
        self.assertEqual(guarded.main(["--audit", str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
