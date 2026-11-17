"""Actual child, store, and receipt regressions for v0.15 Wa evaluation.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_decision_os_wa_kernel_v0_3 as kernel
from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as mediated
from runtime import kuuos_lean_python_wa_numeric_native_cycle_v0_13 as numeric
from runtime import kuuos_lean_python_wa_gate_native_cycle_v0_14 as prior
from runtime import kuuos_lean_python_wa_gate_guard_v0_14 as gate
from runtime import kuuos_lean_python_wa_evaluation_native_cycle_v0_15 as guarded
from runtime.kuuos_lean_python_wa_evaluation_guard_v0_15 import WaEvaluationBoundaryError
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import EVIDENCE_FILE, EVIDENCE_KEYS, GOOD


class WaEvaluationNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v015-native-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.original = prior.checked_apply_wa_gate_event
        cls.store_originals = {
            module: getattr(import_module(module), symbol)
            for _, module, symbol in core.STORE_BINDINGS + mediated.STORE_BINDINGS
        }
        cls.observed_run = guarded.build_wa_evaluation_native_fixture(cls.root)

    def _report(self):
        inherited = mediated._make_child_report(
            dict(self.observed_run.state_guard_calls), self.observed_run.pre_host_guard_calls, self.observed_run.native_audit,
        )
        numeric_report = numeric._make_child_report(inherited, self.observed_run.wa_numeric_guard_calls)
        gate_report = prior._make_child_report(numeric_report, self.observed_run.wa_gate_guard_calls)
        return guarded._make_child_report(gate_report, self.observed_run.wa_evaluation_guard_calls)

    def _store_inputs(self):
        initial = json.loads((self.root / "wa/wa-v03-genesis.json").read_text())
        commits = [json.loads(line) for line in
                   (self.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]
        return initial, [item["event"] for item in commits]

    def test_real_child_all_eight_routes_and_equal_guard_counts(self):
        run = self.observed_run
        self.assertEqual(run.status, guarded.SUCCESS)
        self.assertEqual(run.native_audit.status, GOOD)
        self.assertEqual(tuple(dict(run.state_guard_calls)), mediated.GUARDED_OS)
        self.assertTrue(all(type(n) is int and n > 0 for _, n in run.state_guard_calls))
        self.assertEqual(run.wa_evaluation_guard_calls, run.wa_gate_guard_calls)
        self.assertEqual(run.wa_evaluation_guard_calls, run.wa_numeric_guard_calls)
        self.assertEqual(run.wa_evaluation_guard_calls, dict(run.state_guard_calls)["DecisionOSWa"])
        self.assertEqual(run.pre_host_guard_calls, 1)
        self.assertTrue(run.wa_native_float_derivation_checked)
        self.assertFalse(run.numeric_values_modified)

    def test_read_only_audit_preserves_original_v09_bytes(self):
        original = (self.root / EVIDENCE_FILE).read_bytes()
        record = json.loads(original)
        self.assertEqual(set(record), EVIDENCE_KEYS)
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with patch.object(guarded, "checked_apply_wa_evaluation_event",
                              side_effect=AssertionError("evaluation")):
                audit = guarded.audit_local_evidence(self.root)
        self.assertEqual(audit.status, GOOD)
        self.assertEqual(original, (self.root / EVIDENCE_FILE).read_bytes())

    def test_original_gate_and_store_bindings_unchanged_in_parent(self):
        self.assertIs(prior.checked_apply_wa_gate_event, self.original)
        self.assertIs(self.original, gate.checked_apply_wa_gate_event)
        for _, module, name in core.STORE_BINDINGS + mediated.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), name), self.store_originals[module])

    def test_child_is_independent_of_parent_patches(self):
        with TemporaryDirectory(prefix="kuuos-v015-child-isolation-") as directory:
            with patch.object(prior, "checked_apply_wa_gate_event",
                              side_effect=AssertionError("parent patch")) as fake:
                result = guarded.build_wa_evaluation_native_fixture(Path(directory))
                fake.assert_not_called()
        self.assertEqual(result.status, guarded.SUCCESS)
        self.assertEqual(result.wa_evaluation_guard_calls, result.wa_gate_guard_calls)

    def test_existing_root_is_not_overwritten_or_replayed(self):
        before = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                guarded.build_wa_evaluation_native_fixture(self.root)
        self.assertEqual(before, (self.root / EVIDENCE_FILE).read_bytes())

    def test_preflight_source_failure_stops_before_any_child_file(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            with patch("scripts.check_kuuos_lean_python_wa_evaluation_sources_v0_15.check_sources",
                       return_value=("source_byte_drift:kernel",)):
                with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
                    with self.assertRaisesRegex(ValueError, "source_preflight_failed"):
                        guarded.build_wa_evaluation_native_fixture(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_binding_restores_after_exception_without_overwriting_old_adapter(self):
        with self.assertRaisesRegex(RuntimeError, "controlled interruption"):
            with guarded._guard_evaluation_boundary({"DecisionOSWa": 0}):
                self.assertIsNot(prior.checked_apply_wa_gate_event, self.original)
                self.assertIs(gate.checked_apply_wa_gate_event, self.original)
                raise RuntimeError("controlled interruption")
        self.assertIs(prior.checked_apply_wa_gate_event, self.original)

    def test_bad_counter_or_unexpected_rebinding_fails_closed(self):
        for counts in (None, [], {}, {"DecisionOSWa": True}, {"DecisionOSWa": 0.0},
                       {"DecisionOSWa": 1}, {"DecisionOSWa": 0, "DecisionOSPlural": 0}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                with guarded._guard_evaluation_boundary(counts):
                    self.fail("invalid counter accepted")
        replacement = lambda s, e: None
        with patch.object(prior, "checked_apply_wa_gate_event", replacement):
            with self.assertRaisesRegex(ValueError, "original_gate_adapter_binding_required"):
                with guarded._guard_evaluation_boundary({"DecisionOSWa": 0}):
                    self.fail("unexpected rebinding accepted")

    def test_forged_actual_evaluate_is_blocked_before_real_store_append(self):
        initial, events = self._store_inputs()
        profile_event, evaluate_event = events[0], events[1]
        original_evaluator = kernel._evaluate_profile
        def fake(state, profile):
            record = original_evaluator(state, profile)
            lower = record["weighted_interval"]["lower"]
            record["weighted_interval"]["lower"] = math.nextafter(lower, math.inf)
            return record
        with TemporaryDirectory() as directory:
            store = WaDecisionStore(Path(directory))
            store.initialize(initial)
            self.assertEqual(store.apply(profile_event)["status"], "APPLIED")
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            with guarded._guard_evaluation_boundary({"DecisionOSWa": 0}):
                with prior._guard_gate_boundary({"DecisionOSWa": 0}):
                    with numeric._guard_numeric_boundary({"DecisionOSWa": 0}):
                        with mediated._guard_mediator_stores(
                                {name: 0 for name in mediated.MEDIATOR_OS}):
                            with patch.object(kernel, "_evaluate_profile", side_effect=fake):
                                with self.assertRaises(WaEvaluationBoundaryError) as caught:
                                    store.apply(evaluate_event)
            self.assertIn("weighted_interval", str(caught.exception))
            self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_report_rejects_wrong_count_and_scope_forgery(self):
        actual = self.observed_run.wa_evaluation_guard_calls
        for value in (None, True, False, 0, -1, str(actual), float(actual), actual + 1):
            report = self._report()
            report["wa_evaluation_guard_calls"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)
        for field, value in (("wa_native_float_derivation_checked", False),
                             ("lean_python_refinement_proved", True),
                             ("numeric_values_modified", True)):
            report = self._report()
            report[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_exactly_preserves_prior_gate_report(self):
        report = self._report()
        self.assertEqual(set(report), guarded.REPORT_KEYS)
        self.assertEqual(guarded._checked_report(report, self.observed_run.native_audit)[-1],
                         self.observed_run.wa_evaluation_guard_calls)
        self.assertEqual(report["gate_report"]["version"], prior.VERSION)

    def test_scope_flags_remain_unverified_and_frozen(self):
        for key in ("wa_real_number_refinement_proved", "all_store_writes_guarded",
                    "external_issuer_authenticated", "historical_guard_execution_proved",
                    "lean_python_refinement_proved", "all_effects_prevented_on_any_failure",
                    "host_rollback_guaranteed", "state_commit_atomic_with_host",
                    "execution_authority_granted", "truth_authority_granted",
                    "git_merge_authority_granted"):
            self.assertIs(getattr(self.observed_run, key), False)
        with self.assertRaises(FrozenInstanceError):
            self.observed_run.truth_authority_granted = True


if __name__ == "__main__":
    unittest.main()
