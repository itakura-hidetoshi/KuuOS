"""Real child and real Wa-store tests for the additive numeric boundary.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import redirect_stderr
from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_decision_os_wa_kernel_v0_3 as wa
from runtime import kuuos_decision_os_wa_types_v0_3 as wa_types
from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_mediator_transition_v0_12 as structural
from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as prior
from runtime import kuuos_lean_python_wa_numeric_native_cycle_v0_13 as guarded
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_FILE, EVIDENCE_KEYS, GOOD, VERSION as EVIDENCE_VERSION,
)
from runtime.kuuos_lean_python_wa_numeric_guard_v0_13 import WaNumericBoundaryError


class WaNumericNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = TemporaryDirectory(prefix="kuuos-v013-native-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.original_boundary = staticmethod(prior.checked_apply_mediator_event)
        cls.store_originals = {
            module: getattr(import_module(module), name)
            for _, module, name in core.STORE_BINDINGS + prior.STORE_BINDINGS
        }
        cls.observed_run = guarded.build_wa_numeric_native_fixture(cls.root)

    def report(self):
        run = self.observed_run
        inherited = prior._make_child_report(
            dict(run.state_guard_calls), run.pre_host_guard_calls, run.native_audit,
        )
        return guarded._make_child_report(inherited, run.wa_numeric_guard_calls)

    def store_inputs(self):
        genesis = json.loads((self.root / "wa/wa-v03-genesis.json").read_text())
        commits = [json.loads(row) for row in
                   (self.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]
        return genesis, commits[0]["event"]

    def tolerance_counterexample(self):
        genesis, original_profile = self.store_inputs()
        genesis["weights"]["inclusion"] += 5e-13
        genesis["wa_state_digest"] = wa_types.wa_state_digest(genesis)
        payload = deepcopy(original_profile["payload"])
        for profile in payload["profiles"]:
            profile.pop("wa_profile_digest", None)
            for name in wa_types.POSITIVE_DIMENSIONS:
                profile["positive_intervals"][name] = {"lower": 1.0, "upper": 1.0}
            for name in wa_types.ALERT_DIMENSIONS:
                profile["alert_intervals"][name] = {"lower": 0.0, "upper": 0.0}
        profile_event = wa.build_wa_event(
            state=genesis, target_phase="profile", artifact_digest="v013-profile",
            payload=payload, now_ms=genesis["updated_at_ms"] + 1,
        )
        profiled = wa.apply_wa_event(genesis, profile_event)["state"]
        evaluate = wa.build_wa_event(
            state=profiled, target_phase="evaluate", artifact_digest="v013-evaluate",
            payload={"evaluation_receipt_digest": "v013-evaluation-receipt"},
            now_ms=profiled["updated_at_ms"] + 1,
        )
        return genesis, profile_event, profiled, evaluate

    def test_actual_child_checks_every_wa_call_and_preserves_eight_routes(self):
        run = self.observed_run
        self.assertEqual(run.status, guarded.SUCCESS)
        self.assertEqual(run.native_audit.status, GOOD)
        self.assertEqual(tuple(dict(run.state_guard_calls)), prior.GUARDED_OS)
        self.assertTrue(all(type(n) is int and n > 0 for _, n in run.state_guard_calls))
        self.assertIs(type(run.wa_numeric_guard_calls), int)
        self.assertEqual(run.wa_numeric_guard_calls, dict(run.state_guard_calls)["DecisionOSWa"])
        self.assertEqual(run.pre_host_guard_calls, 1)
        self.assertIs(run.wa_numeric_interval_bounds_checked, True)
        self.assertIs(run.numeric_values_modified, False)

    def test_parent_keeps_original_boundary_kernel_and_store_bindings(self):
        self.assertIs(prior.checked_apply_mediator_event, self.original_boundary)
        self.assertIs(self.original_boundary, structural.checked_apply_mediator_event)
        for _, module, name in core.STORE_BINDINGS + prior.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), name), self.store_originals[module])
        store_module = import_module("runtime.kuuos_decision_os_wa_store_v0_3")
        self.assertIs(store_module.apply_wa_event, wa.apply_wa_event)

    def test_actual_child_does_not_inherit_parent_boundary_replacement(self):
        with TemporaryDirectory(prefix="kuuos-v013-isolation-") as folder:
            with patch.object(prior, "checked_apply_mediator_event",
                              side_effect=AssertionError("parent boundary reached")) as replacement:
                run = guarded.build_wa_numeric_native_fixture(Path(folder))
                replacement.assert_not_called()
                self.assertIs(prior.checked_apply_mediator_event, replacement)
        self.assertEqual(run.status, guarded.SUCCESS)
        self.assertEqual(run.wa_numeric_guard_calls, dict(run.state_guard_calls)["DecisionOSWa"])
        self.assertIs(prior.checked_apply_mediator_event, self.original_boundary)

    def test_scope_does_not_promote_schema_checks_to_refinement_or_authority(self):
        run = self.observed_run
        for name in ("numeric_values_modified", "all_store_writes_guarded",
                     "wa_real_number_refinement_proved", "wa_evaluation_equivalence_proved",
                     "all_effects_prevented_on_any_failure", "host_rollback_guaranteed",
                     "state_commit_atomic_with_host", "external_issuer_authenticated",
                     "historical_guard_execution_proved", "lean_python_refinement_proved",
                     "execution_authority_granted", "truth_authority_granted",
                     "git_merge_authority_granted"):
            self.assertIs(getattr(run, name), False, name)
        self.assertIs(run.counts_include_recovery_replays, True)
        self.assertEqual(run.guard_observation_mode, "local_child_stdout_unattested")
        with self.assertRaises(FrozenInstanceError):
            run.execution_authority_granted = True

    def test_original_v09_record_inventory_is_unchanged(self):
        record = json.loads((self.root / EVIDENCE_FILE).read_text())
        self.assertEqual(set(record), EVIDENCE_KEYS)
        self.assertEqual(record["version"], EVIDENCE_VERSION)
        self.assertEqual(record["record_sha256"], self.observed_run.native_audit.record_sha256)

    def test_later_audit_is_read_only_and_does_not_reexecute_numeric_gate(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with patch.object(guarded, "checked_apply_wa_numeric_event",
                              side_effect=AssertionError("numeric gate")):
                audit = guarded.audit_local_evidence(self.root)
        self.assertEqual(audit.status, GOOD)
        self.assertFalse(audit.historical_issuance_proved)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_missing_evidence_stays_no_data(self):
        with TemporaryDirectory() as folder:
            audit = guarded.audit_local_evidence(Path(folder))
        self.assertEqual(audit.status, "NO_DATA")
        self.assertFalse(audit.local_record_checked)

    def test_existing_root_is_not_reexecuted_or_overwritten(self):
        before = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                guarded.build_wa_numeric_native_fixture(self.root)
        self.assertEqual(before, (self.root / EVIDENCE_FILE).read_bytes())

    def test_source_failure_stops_before_child_and_new_files(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch("scripts.check_kuuos_lean_python_wa_numeric_sources_v0_13.check_sources",
                       return_value=("source_byte_drift:wa_kernel",)):
                with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
                    with self.assertRaisesRegex(ValueError, "wa_numeric_source_preflight"):
                        guarded.build_wa_numeric_native_fixture(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_boundary_binding_restores_after_failure(self):
        with self.assertRaisesRegex(RuntimeError, "test interruption"):
            with guarded._guard_numeric_boundary({"DecisionOSWa": 0}):
                self.assertIsNot(prior.checked_apply_mediator_event, self.original_boundary)
                self.assertIs(structural.checked_apply_mediator_event, self.original_boundary)
                raise RuntimeError("test interruption")
        self.assertIs(prior.checked_apply_mediator_event, self.original_boundary)

    def test_nonoriginal_boundary_is_refused_without_overwriting_it(self):
        replacement = lambda name, state, event: None
        with patch.object(prior, "checked_apply_mediator_event", replacement):
            with self.assertRaisesRegex(ValueError, "original_mediator_boundary"):
                with guarded._guard_numeric_boundary({"DecisionOSWa": 0}):
                    self.fail("untrusted boundary entered")
            self.assertIs(prior.checked_apply_mediator_event, replacement)

    def test_only_fresh_exact_integer_numeric_counter_is_accepted(self):
        for counts in (None, [], {}, {"DecisionOSWa": True}, {"DecisionOSWa": 0.0},
                       {"DecisionOSWa": 1}, {"DecisionOSWa": 0, "DecisionOSPlural": 0}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                with guarded._guard_numeric_boundary(counts):
                    self.fail("bad counter accepted")

    def test_known_native_interval_inversion_is_blocked_before_real_store_append(self):
        genesis, profile_event, profiled, evaluate = self.tolerance_counterexample()
        original = wa.apply_wa_event(profiled, evaluate)
        self.assertEqual(original["status"], "APPLIED")
        self.assertEqual(wa.validate_wa_state(original["state"]), [])
        interval = original["state"]["wa_records"][0]["wa_interval"]
        self.assertGreater(interval["lower"], interval["upper"])
        self.assertLess(interval["width"], 0)
        with TemporaryDirectory() as folder:
            store = WaDecisionStore(Path(folder))
            store.initialize(genesis)
            self.assertEqual(store.apply(profile_event)["status"], "APPLIED")
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            counts = {"DecisionOSWa": 0}
            old_counts = {name: 0 for name in prior.MEDIATOR_OS}
            with guarded._guard_numeric_boundary(counts):
                with prior._guard_mediator_stores(old_counts):
                    with self.assertRaises(WaNumericBoundaryError) as caught:
                        store.apply(evaluate)
            self.assertEqual(caught.exception.status, "BLOCKED")
            self.assertTrue(caught.exception.issues)
            self.assertEqual(counts["DecisionOSWa"], 1)  # prior profile recovery only
            self.assertEqual(old_counts["DecisionOSWa"], 1)
            self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_invalid_existing_numeric_state_cannot_pass_as_a_replay(self):
        _, _, profiled, evaluate = self.tolerance_counterexample()
        invalid = wa.apply_wa_event(profiled, evaluate)["state"]
        self.assertEqual(structural.checked_apply_mediator_event(
            "DecisionOSWa", invalid, evaluate,
        )["status"], "REPLAYED")
        with TemporaryDirectory() as folder:
            store = WaDecisionStore(Path(folder))
            store.initialize(invalid)
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            counts = {"DecisionOSWa": 0}
            with guarded._guard_numeric_boundary(counts):
                with prior._guard_mediator_stores({name: 0 for name in prior.MEDIATOR_OS}):
                    with self.assertRaises(WaNumericBoundaryError):
                        store.apply(evaluate)
            self.assertEqual(counts["DecisionOSWa"], 0)
            self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_genuine_native_replay_and_rejection_keep_store_unchanged(self):
        genesis, first = self.store_inputs()
        with TemporaryDirectory() as folder:
            store = WaDecisionStore(Path(folder))
            store.initialize(genesis)
            with guarded._guard_numeric_boundary({"DecisionOSWa": 0}):
                with prior._guard_mediator_stores({name: 0 for name in prior.MEDIATOR_OS}):
                    applied = store.apply(first)
                    before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
                    replay = store.apply(first)
                    stale = deepcopy(first)
                    stale["created_at_ms"] += 1
                    stale["wa_event_digest"] = wa_types.wa_event_digest(stale)
                    rejected = store.apply(stale)
            self.assertEqual(applied["status"], "APPLIED")
            self.assertEqual(replay["status"], "REPLAYED")
            self.assertEqual(rejected["status"], "REJECTED")
            self.assertEqual(before, (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()))

    def test_report_numeric_count_is_exact_and_equals_every_wa_state_check(self):
        actual = self.observed_run.wa_numeric_guard_calls
        for count in (None, False, True, 0, -1, float(actual), str(actual), actual + 1):
            report = self.report()
            report["wa_numeric_guard_calls"] = count
            with self.subTest(count=count), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_retains_prior_source_record_scope_and_all_eight_counts(self):
        for key, value in (("source_main", "other"), ("native_record_sha256", "other"),
                           ("all_store_writes_guarded", True), ("pre_host_guard_calls", 0)):
            report = self.report()
            report["mediated_report"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)
        for name in prior.GUARDED_OS:
            report = self.report()
            del report["mediated_report"]["state_guard_calls"][name]
            with self.subTest(missing=name), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_binds_new_identity_inventory_and_non_refinement_flags(self):
        for key, value in (("source_main", "other"), ("version", "other"),
                           ("status", "APPLIED"), ("numeric_values_modified", True),
                           ("wa_numeric_interval_bounds_checked", 1),
                           ("wa_real_number_refinement_proved", True),
                           ("external_signature", "invented")):
            report = self.report()
            report[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_child_failure_retains_partial_output_and_is_not_retried(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)

            def fail(*args, **kwargs):
                (root / "partial-evidence").write_text("retain")
                return guarded.subprocess.CompletedProcess(args[0], 1, "", "failure")

            with patch.object(guarded.subprocess, "run", side_effect=fail) as child:
                with self.assertRaisesRegex(RuntimeError, "wa_numeric_native_child_failed"):
                    guarded.build_wa_numeric_native_fixture(root)
                self.assertEqual(child.call_count, 1)
            self.assertEqual((root / "partial-evidence").read_text(), "retain")

    def test_child_report_size_and_parse_failure_precede_audit(self):
        for output, error in (("x" * (core.MAX_CHILD_OUTPUT_BYTES + 1), "too_large"),
                              ("not json", "invalid_json")):
            with self.subTest(error=error), TemporaryDirectory() as folder:
                result = guarded.subprocess.CompletedProcess([], 0, output, "")
                with patch.object(guarded.subprocess, "run", return_value=result):
                    with patch.object(guarded, "audit_local_evidence",
                                      side_effect=AssertionError("audit")):
                        with self.assertRaisesRegex(ValueError, error):
                            guarded.build_wa_numeric_native_fixture(Path(folder))

    def test_cli_requires_explicit_fixture_child(self):
        with redirect_stderr(StringIO()):
            self.assertEqual(guarded.main([]), 2)
            self.assertEqual(guarded.main(["--audit", str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
