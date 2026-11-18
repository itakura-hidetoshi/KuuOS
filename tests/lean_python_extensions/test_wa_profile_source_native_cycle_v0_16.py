"""Native child, original stores and local committed-source tests for Wa v0.16.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_decision_os_wa_kernel_v0_3 as wa
from runtime import kuuos_decision_os_wa_store_v0_3 as wa_store
from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as mediated
from runtime import kuuos_lean_python_wa_numeric_native_cycle_v0_13 as numeric
from runtime import kuuos_lean_python_wa_gate_native_cycle_v0_14 as gate
from runtime import kuuos_lean_python_wa_evaluation_native_cycle_v0_15 as prior
from runtime import kuuos_lean_python_wa_evaluation_guard_v0_15 as previous_adapter
from runtime import kuuos_lean_python_wa_profile_source_native_cycle_v0_16 as guarded
from runtime import kuuos_lean_python_wa_profile_source_guard_v0_16 as profile_guard
from runtime.kuuos_decision_os_wa_types_v0_3 import wa_event_digest, wa_state_digest
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import EVIDENCE_FILE, EVIDENCE_KEYS, GOOD


class WaProfileSourceNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v016-native-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.original_adapter = staticmethod(prior.checked_apply_wa_evaluation_event)
        cls.store_bindings = {
            module: getattr(import_module(module), symbol)
            for _, module, symbol in core.STORE_BINDINGS + mediated.STORE_BINDINGS
        }
        cls.observed_run = guarded.build_wa_profile_source_native_fixture(cls.root)

    def report(self):
        r = self.observed_run
        structural = mediated._make_child_report(
            dict(r.state_guard_calls), r.pre_host_guard_calls, r.native_audit,
        )
        n = numeric._make_child_report(structural, r.wa_numeric_guard_calls)
        g = gate._make_child_report(n, r.wa_gate_guard_calls)
        e = prior._make_child_report(g, r.wa_evaluation_guard_calls)
        return guarded._make_child_report(e, r.wa_profile_source_guard_calls, r.source_witness_digest)

    def store_inputs(self):
        genesis = json.loads((self.root / "wa/wa-v03-genesis.json").read_text())
        lines = (self.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()
        commits = [json.loads(row) for row in lines]
        return genesis, [row["event"] for row in commits]

    def source(self):
        return PluralDecisionStore(self.root / "plural").recover(require_snapshot_match=True)

    def test_actual_child_checks_eight_native_os_and_all_wa_calls(self):
        run = self.observed_run
        self.assertEqual(run.status, guarded.SUCCESS)
        self.assertEqual(run.native_audit.status, GOOD)
        self.assertEqual(tuple(dict(run.state_guard_calls)), mediated.GUARDED_OS)
        self.assertEqual(run.wa_profile_source_guard_calls, run.wa_evaluation_guard_calls)
        self.assertEqual(run.wa_profile_source_guard_calls, run.wa_gate_guard_calls)
        self.assertEqual(run.wa_profile_source_guard_calls, run.wa_numeric_guard_calls)
        self.assertEqual(run.wa_profile_source_guard_calls, dict(run.state_guard_calls)["DecisionOSWa"])
        self.assertEqual(run.pre_host_guard_calls, 1)
        self.assertIs(run.profile_digest_binding_checked, True)
        self.assertIs(run.source_recovered_locally, True)

    def test_recovered_actual_plural_store_matches_child_witness(self):
        source = self.source()
        self.assertEqual(source["current_phase"], "commit")
        self.assertEqual(self.observed_run.source_witness_digest, _fingerprint(source))
        state, _ = self.store_inputs()
        expected = profile_guard._source_projection(source)
        self.assertEqual(len(expected), 19)
        for field, value in expected.items():
            self.assertEqual(_fingerprint(state[field]), _fingerprint(value))

    def test_original_v09_evidence_inventory_and_read_only_audit_preserved(self):
        original = (self.root / EVIDENCE_FILE).read_bytes()
        self.assertEqual(set(json.loads(original)), EVIDENCE_KEYS)
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with patch.object(guarded, "checked_apply_wa_profile_source_event",
                              side_effect=AssertionError("guard")):
                reread = guarded.audit_local_evidence(self.root)
        self.assertEqual(reread.status, GOOD)
        self.assertEqual((self.root / EVIDENCE_FILE).read_bytes(), original)

    def test_parent_keeps_unmodified_original_kernel_store_and_adapter_bindings(self):
        self.assertIs(prior.checked_apply_wa_evaluation_event, self.original_adapter)
        self.assertIs(self.original_adapter, previous_adapter.checked_apply_wa_evaluation_event)
        self.assertIs(wa_store.apply_wa_event, wa.apply_wa_event)
        for _, module, symbol in core.STORE_BINDINGS + mediated.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), symbol), self.store_bindings[module])

    def test_child_process_is_independent_of_parent_patch(self):
        with TemporaryDirectory(prefix="kuuos-v016-parent-patch-") as directory:
            with patch.object(prior, "checked_apply_wa_evaluation_event",
                              side_effect=AssertionError("parent patch")) as patched:
                result = guarded.build_wa_profile_source_native_fixture(Path(directory))
                patched.assert_not_called()
        self.assertEqual(result.status, guarded.SUCCESS)
        self.assertEqual(result.wa_profile_source_guard_calls, result.wa_evaluation_guard_calls)

    def test_existing_evidence_root_is_never_reexecuted(self):
        previous = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                guarded.build_wa_profile_source_native_fixture(self.root)
        self.assertEqual(previous, (self.root / EVIDENCE_FILE).read_bytes())

    def test_preflight_bad_source_stops_before_child_launch(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            with patch("scripts.check_kuuos_lean_python_wa_profile_source_sources_v0_16.check_sources",
                       return_value=("source_byte_drift:old",)):
                with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
                    with self.assertRaisesRegex(ValueError, "preflight_failed"):
                        guarded.build_wa_profile_source_native_fixture(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_original_binding_is_restored_on_raised_exception(self):
        with self.assertRaisesRegex(RuntimeError, "interrupted"):
            with guarded._guard_profile_source_boundary(
                    self.root, {"DecisionOSWa": 0}, [""]):
                self.assertIsNot(prior.checked_apply_wa_evaluation_event, self.original_adapter)
                self.assertIs(previous_adapter.checked_apply_wa_evaluation_event, self.original_adapter)
                raise RuntimeError("interrupted")
        self.assertIs(prior.checked_apply_wa_evaluation_event, self.original_adapter)

    def test_invalid_counters_and_foreign_adapter_are_rejected(self):
        for count in (None, {}, [], {"DecisionOSWa": True}, {"DecisionOSWa": 0.0},
                      {"DecisionOSWa": 1}, {"DecisionOSWa": 0, "DecisionOSPlural": 0}):
            with self.subTest(count=count), self.assertRaises(ValueError):
                with guarded._guard_profile_source_boundary(self.root, count, [""]):
                    self.fail("bad counter accepted")
        for witness in (None, ["wrong"], [], [0], ["", ""]):
            with self.subTest(witness=witness), self.assertRaises(ValueError):
                with guarded._guard_profile_source_boundary(
                        self.root, {"DecisionOSWa": 0}, witness):
                    self.fail("bad witness status accepted")
        foreign = lambda s, e: {}
        with patch.object(prior, "checked_apply_wa_evaluation_event", foreign):
            with self.assertRaisesRegex(ValueError, "original_evaluation_boundary"):
                with guarded._guard_profile_source_boundary(
                        self.root, {"DecisionOSWa": 0}, [""]):
                    self.fail("unexpected adapter accepted")

    def test_forged_native_profile_hash_blocks_before_real_store_append(self):
        original_normalizer = wa._normalize_profile
        def forge(state, profile):
            normalized = original_normalizer(state, profile)
            normalized["dialogue_receipt_digest"] = "forged-after-normalize"
            return normalized
        genesis, events = self.store_inputs()
        first = events[0]
        source = self.source()
        with TemporaryDirectory() as directory:
            store = WaDecisionStore(Path(directory))
            store.initialize(genesis)
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            with patch.object(wa, "_normalize_profile", side_effect=forge):
                # Existing v0.12 mediator already prevents this stale hash.
                with self.assertRaises(previous_adapter.WaEvaluationBoundaryError):
                    previous_adapter.checked_apply_wa_evaluation_event(genesis, first)
            with patch.object(wa_store, "apply_wa_event",
                              side_effect=lambda state, event:
                              profile_guard.checked_apply_wa_profile_source_event(state, event, source)):
                with patch.object(wa, "_normalize_profile", side_effect=forge):
                    with self.assertRaises(profile_guard.WaProfileSourceBoundaryError) as caught:
                        store.apply(first)
            # The earlier v0.12 mediator may reject this bad digest first;
            # both diagnostics retain a blocking profile-digest mismatch.
            self.assertIn("profile_digest", str(caught.exception))
            self.assertEqual((store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()), before)

    def test_local_source_mismatch_blocks_before_actual_store_append(self):
        genesis, events = self.store_inputs()
        source = self.source()
        genesis["source_utility_records_digest"] = "different-local-source"
        genesis["wa_state_digest"] = wa_state_digest(genesis)
        event = wa.build_wa_event(
            state=genesis, target_phase="profile",
            artifact_digest="v016-source-bad", payload=events[0]["payload"],
            now_ms=genesis["updated_at_ms"] + 1,
        )
        self.assertEqual(previous_adapter.checked_apply_wa_evaluation_event(genesis, event)["status"], "APPLIED")
        with TemporaryDirectory() as directory:
            store = WaDecisionStore(Path(directory))
            store.initialize(genesis)
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            with patch.object(wa_store, "apply_wa_event",
                              side_effect=lambda state, actual:
                              profile_guard.checked_apply_wa_profile_source_event(state, actual, source)):
                with self.assertRaises(profile_guard.WaProfileSourceBoundaryError) as caught:
                    store.apply(event)
            self.assertIn("source_utility_records_digest", str(caught.exception))
            self.assertEqual((store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()), before)

    def test_missing_local_plural_ledger_yields_no_data_before_wa_write(self):
        genesis, events = self.store_inputs()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            store = WaDecisionStore(root / "wa")
            store.initialize(genesis)
            before = (store.ledger_path.read_bytes(), store.snapshot_path.read_bytes())
            counts = {"DecisionOSWa": 0}
            with guarded._guard_profile_source_boundary(root, counts, [""]):
                with patch.object(wa_store, "apply_wa_event",
                                  side_effect=lambda state, event:
                                  prior.checked_apply_wa_evaluation_event(state, event)):
                    # The actual store must refuse the event before append.
                    with self.assertRaises(profile_guard.WaProfileSourceBoundaryError):
                        store.apply(events[0])
            self.assertEqual(counts["DecisionOSWa"], 0)
            self.assertEqual((store.ledger_path.read_bytes(), store.snapshot_path.read_bytes()), before)

    def test_report_count_and_local_witness_binding_must_be_exact(self):
        report = self.report()
        self.assertEqual(set(report), guarded.REPORT_KEYS)
        self.assertEqual(guarded._checked_report(report, self.observed_run.native_audit)[-1],
                         self.observed_run.source_witness_digest)
        for wrong in (None, True, 0, "0", float(self.observed_run.wa_profile_source_guard_calls),
                      self.observed_run.wa_profile_source_guard_calls + 1):
            trial = deepcopy(report)
            trial["wa_profile_source_guard_calls"] = wrong
            with self.subTest(wrong=wrong), self.assertRaises(ValueError):
                guarded._checked_report(trial, self.observed_run.native_audit)
        for bad in (None, True, 1, "zz"*32, "a"*63):
            trial = deepcopy(report)
            trial["source_witness_digest"] = bad
            with self.subTest(digest=bad), self.assertRaises(ValueError):
                guarded._checked_report(trial, self.observed_run.native_audit)

    def test_unsigned_report_does_not_claim_historical_or_external_authority(self):
        for attr in ("source_external_authenticity_established", "external_issuer_authenticated",
                     "historical_guard_execution_proved", "lean_python_refinement_proved",
                     "original_native_sources_modified", "all_store_writes_guarded",
                     "all_effects_prevented_on_any_failure", "host_rollback_guaranteed",
                     "state_commit_atomic_with_host", "execution_authority_granted",
                     "truth_authority_granted", "git_merge_authority_granted"):
            self.assertIs(getattr(self.observed_run, attr), False, attr)
        with self.assertRaises(FrozenInstanceError):
            self.observed_run.execution_authority_granted = True


if __name__ == "__main__":
    unittest.main()
