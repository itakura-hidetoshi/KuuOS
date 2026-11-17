"""Real isolated eight-route fixture and mediator store-boundary tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import ExitStack, redirect_stderr
from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_act_os_kernel_v0_1 as act
from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_pre_host_native_cycle_v0_11 as prior
from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as guarded
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_FILE, EVIDENCE_KEYS, GOOD, VERSION as EVIDENCE_VERSION,
)
from runtime.kuuos_lean_python_mediator_transition_v0_12 import MediatorTransitionError


class MediatedNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = TemporaryDirectory(prefix="kuuos-v012-native-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.originals = {
            module: getattr(import_module(module), name)
            for _, module, name in core.STORE_BINDINGS + guarded.STORE_BINDINGS
        }
        cls.caller = import_module(prior.CALLER_MODULE)
        cls.original_builder = staticmethod(getattr(cls.caller, prior.BUILDER_BINDING))
        cls.original_host = staticmethod(act.run_host_tick)
        cls.observed_run = guarded.build_mediated_native_fixture(cls.root)

    def report(self):
        return guarded._make_child_report(
            dict(self.observed_run.state_guard_calls),
            self.observed_run.pre_host_guard_calls,
            self.observed_run.native_audit,
        )

    def store_inputs(self, name):
        if name == "DecisionOSPlural":
            from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
            from runtime.kuuos_decision_os_plural_types_v0_2 import event_digest
            directory, stem, store_class, digest = (
                "plural", "plural", PluralDecisionStore, event_digest,
            )
        else:
            from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
            from runtime.kuuos_decision_os_wa_types_v0_3 import wa_event_digest
            directory, stem, store_class, digest = (
                "wa", "wa-v03", WaDecisionStore, wa_event_digest,
            )
        genesis = json.loads((self.root / directory / (stem + "-genesis.json")).read_text())
        lines = (self.root / directory / (stem + "-ledger.jsonl")).read_text().splitlines()
        first = json.loads(lines[0])["event"]
        return store_class, genesis, first, digest

    def test_actual_child_checks_eight_state_routes_and_one_pre_host_invocation(self):
        run = self.observed_run
        self.assertEqual(run.status, guarded.SUCCESS)
        self.assertEqual(run.native_audit.status, GOOD)
        self.assertEqual(tuple(dict(run.state_guard_calls)), guarded.GUARDED_OS)
        self.assertTrue(all(type(n) is int and n > 0 for _, n in run.state_guard_calls))
        self.assertIs(type(run.pre_host_guard_calls), int)
        self.assertEqual(run.pre_host_guard_calls, 1)
        self.assertIs(run.act_invocation_inputs_checked_before_host, True)

    def test_parent_store_builder_and_host_bindings_remain_original(self):
        for _, module, name in core.STORE_BINDINGS + guarded.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), name), self.originals[module])
        self.assertIs(getattr(self.caller, prior.BUILDER_BINDING), self.original_builder)
        self.assertIs(act.build_authorized_invoke_event, self.original_builder)
        self.assertIs(act.run_host_tick, self.original_host)

    def test_actual_child_does_not_inherit_parent_mediator_replacements(self):
        with TemporaryDirectory(prefix="kuuos-v012-parent-isolation-") as folder:
            with ExitStack() as stack:
                replacements = []
                for _, module, name in guarded.STORE_BINDINGS:
                    replacement = stack.enter_context(patch.object(
                        import_module(module), name,
                        side_effect=AssertionError("parent replacement reached"),
                    ))
                    replacements.append((module, name, replacement))
                run = guarded.build_mediated_native_fixture(Path(folder))
                for module, name, replacement in replacements:
                    replacement.assert_not_called()
                    self.assertIs(getattr(import_module(module), name), replacement)
        self.assertEqual(run.status, guarded.SUCCESS)
        for _, module, name in guarded.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), name), self.originals[module])

    def test_native_record_keeps_exact_original_v09_inventory(self):
        record = json.loads((self.root / EVIDENCE_FILE).read_text())
        self.assertEqual(set(record), EVIDENCE_KEYS)
        self.assertEqual(record["version"], EVIDENCE_VERSION)
        self.assertEqual(record["record_sha256"], self.observed_run.native_audit.record_sha256)

    def test_scope_does_not_claim_initialization_math_authentication_or_authority(self):
        run = self.observed_run
        for field in ("all_store_writes_guarded", "wa_real_number_refinement_proved",
                      "all_effects_prevented_on_any_failure", "host_rollback_guaranteed",
                      "state_commit_atomic_with_host", "external_issuer_authenticated",
                      "historical_guard_execution_proved", "lean_python_refinement_proved",
                      "execution_authority_granted", "truth_authority_granted",
                      "git_merge_authority_granted"):
            self.assertIs(getattr(run, field), False, field)
        self.assertEqual(run.guard_observation_mode, "local_child_stdout_unattested")
        self.assertIs(run.counts_include_recovery_replays, True)
        with self.assertRaises(FrozenInstanceError):
            run.execution_authority_granted = True

    def test_read_only_audit_neither_spawns_nor_reexecutes_mediator_guard(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with patch.object(guarded, "checked_apply_mediator_event",
                              side_effect=AssertionError("apply")):
                audit = guarded.audit_local_evidence(self.root)
        self.assertEqual(audit.status, GOOD)
        self.assertFalse(audit.historical_issuance_proved)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_missing_evidence_stays_no_data(self):
        with TemporaryDirectory() as folder:
            audit = guarded.audit_local_evidence(Path(folder))
        self.assertEqual(audit.status, "NO_DATA")
        self.assertFalse(audit.local_record_checked)

    def test_nonempty_root_stops_before_child_and_preserves_record(self):
        before = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                guarded.build_mediated_native_fixture(self.root)
        self.assertEqual(before, (self.root / EVIDENCE_FILE).read_bytes())

    def test_source_failure_stops_before_child_or_fixture_files(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch("scripts.check_kuuos_lean_python_mediator_sources_v0_12.check_sources",
                       return_value=("source_byte_drift:plural_kernel",)):
                with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
                    with self.assertRaisesRegex(ValueError, "mediator_source_preflight"):
                        guarded.build_mediated_native_fixture(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_bindings_restore_after_scope_exception_and_kernel_stays_original(self):
        with self.assertRaisesRegex(RuntimeError, "test interruption"):
            with guarded._guard_mediator_stores({name: 0 for name in guarded.MEDIATOR_OS}):
                for _, module, name in guarded.STORE_BINDINGS:
                    self.assertIsNot(getattr(import_module(module), name), self.originals[module])
                    kernel = import_module(module.replace("_store_", "_kernel_"))
                    self.assertIs(getattr(kernel, name), self.originals[module])
                raise RuntimeError("test interruption")
        for _, module, name in guarded.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), name), self.originals[module])

    def test_partial_entry_failure_restores_first_and_preserves_second_replacement(self):
        _, first_module, first_name = guarded.STORE_BINDINGS[0]
        _, second_module, second_name = guarded.STORE_BINDINGS[1]
        replacement = lambda state, event: None
        with patch.object(import_module(second_module), second_name, replacement):
            with self.assertRaisesRegex(ValueError, "original_mediator_store_binding"):
                with guarded._guard_mediator_stores({name: 0 for name in guarded.MEDIATOR_OS}):
                    self.fail("untrusted binding entered")
            self.assertIs(getattr(import_module(first_module), first_name), self.originals[first_module])
            self.assertIs(getattr(import_module(second_module), second_name), replacement)

    def test_counter_inputs_require_exact_fresh_dict_and_integer_zeros(self):
        for counts in (None, [], {}, {"DecisionOSPlural": 0},
                       {"DecisionOSPlural": True, "DecisionOSWa": 0},
                       {"DecisionOSPlural": 0.0, "DecisionOSWa": 0},
                       {"DecisionOSPlural": 0, "DecisionOSWa": 1},
                       {"DecisionOSPlural": 0, "DecisionOSWa": 0, "Other": 0}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                with guarded._guard_mediator_stores(counts):
                    self.fail("invalid counter accepted")

    def test_added_check_failure_after_real_kernel_preserves_both_store_ledgers(self):
        original_checked = guarded.checked_apply_mediator_event
        for name in guarded.MEDIATOR_OS:
            with self.subTest(os_name=name), TemporaryDirectory() as folder:
                store_class, genesis, first, _ = self.store_inputs(name)
                store = store_class(Path(folder))
                store.initialize(genesis)
                before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
                observations = []

                def fail_after_checked(os_name, state, event):
                    result = original_checked(os_name, state, event)
                    observations.append((os_name, result["status"]))
                    raise MediatorTransitionError("BLOCKED", ("injected_added_check_failure",))

                counts = {key: 0 for key in guarded.MEDIATOR_OS}
                with guarded._guard_mediator_stores(counts):
                    with patch.object(guarded, "checked_apply_mediator_event",
                                      side_effect=fail_after_checked):
                        with self.assertRaises(MediatorTransitionError):
                            store.apply(first)
                self.assertEqual(observations, [(name, "APPLIED")])
                self.assertEqual(counts, {key: 0 for key in guarded.MEDIATOR_OS})
                self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_native_replay_and_rejection_do_not_append_either_store(self):
        for name in guarded.MEDIATOR_OS:
            with self.subTest(os_name=name), TemporaryDirectory() as folder:
                store_class, genesis, first, digest = self.store_inputs(name)
                store = store_class(Path(folder))
                store.initialize(genesis)
                with guarded._guard_mediator_stores({key: 0 for key in guarded.MEDIATOR_OS}):
                    applied = store.apply(first)
                    before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
                    replayed = store.apply(first)
                    stale = deepcopy(first)
                    stale["created_at_ms"] += 1
                    key = "plural_event_digest" if name == "DecisionOSPlural" else "wa_event_digest"
                    stale[key] = digest(stale)
                    rejected = store.apply(stale)
                self.assertEqual(applied["status"], "APPLIED")
                self.assertEqual(replayed["status"], "REPLAYED")
                self.assertEqual(rejected["status"], "REJECTED")
                self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_report_requires_all_eight_strict_positive_counters(self):
        for name in guarded.GUARDED_OS:
            for value in (None, False, True, 0, -1, 1.0, "1"):
                report = self.report()
                report["state_guard_calls"][name] = value
                with self.subTest(os_name=name, value=value), self.assertRaises(ValueError):
                    guarded._checked_report(report, self.observed_run.native_audit)
            report = self.report()
            del report["state_guard_calls"][name]
            with self.subTest(missing=name), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_cannot_admit_a_ninth_os(self):
        report = self.report()
        report["state_guard_calls"]["WORLD"] = 1
        with self.assertRaises(ValueError):
            guarded._checked_report(report, self.observed_run.native_audit)
        self.assertEqual(guarded.GUARDED_OS, (
            "DecisionOS", "DecisionOSPlural", "DecisionOSWa", "PlanOS", "ActOS",
            "ObserveOS", "VerifyOS", "LearnOS",
        ))

    def test_report_requires_one_exact_pre_host_count(self):
        for value in (None, False, True, 0, -1, 1.0, "1", 2):
            report = self.report()
            report["pre_host_guard_calls"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_binds_source_record_inventory_and_narrow_scope(self):
        for key, value in (("source_main", "other"), ("version", "other"),
                           ("native_record_sha256", "other"), ("status", "APPLIED"),
                           ("act_invocation_inputs_checked_before_host", 1),
                           ("counts_include_recovery_replays", False),
                           ("all_store_writes_guarded", True),
                           ("wa_real_number_refinement_proved", True),
                           ("all_effects_prevented_on_any_failure", True),
                           ("external_issuer_signature", "invented")):
            report = self.report()
            report[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_child_failure_is_not_retried_and_partial_output_is_retained(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)

            def child_failure(*args, **kwargs):
                (root / "partial-evidence").write_text("keep for inspection")
                return guarded.subprocess.CompletedProcess(args[0], 1, "", "test_failure")

            with patch.object(guarded.subprocess, "run", side_effect=child_failure) as child:
                with self.assertRaisesRegex(RuntimeError, "mediated_native_child_failed"):
                    guarded.build_mediated_native_fixture(root)
                self.assertEqual(child.call_count, 1)
            self.assertEqual((root / "partial-evidence").read_text(), "keep for inspection")

    def test_child_report_size_and_json_fail_before_evidence_audit(self):
        for stdout, error in (("x" * (core.MAX_CHILD_OUTPUT_BYTES + 1), "too_large"),
                              ("not json", "invalid_json")):
            with self.subTest(error=error), TemporaryDirectory() as folder:
                completed = guarded.subprocess.CompletedProcess([], 0, stdout, "")
                with patch.object(guarded.subprocess, "run", return_value=completed):
                    with patch.object(guarded, "audit_local_evidence",
                                      side_effect=AssertionError("audit")):
                        with self.assertRaisesRegex(ValueError, error):
                            guarded.build_mediated_native_fixture(Path(folder))

    def test_cli_requires_explicit_fixture_child_mode(self):
        with redirect_stderr(StringIO()):
            self.assertEqual(guarded.main([]), 2)
            self.assertEqual(guarded.main(["--audit", str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
