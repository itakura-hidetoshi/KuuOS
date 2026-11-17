"""Native child and effect-order tests for the additive v0.11 Act gate.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import redirect_stderr
from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_act_os_kernel_v0_1 as act
from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as prior
from runtime import kuuos_lean_python_pre_host_native_cycle_v0_11 as guarded
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_FILE, GOOD,
)
from runtime.kuuos_lean_python_pre_host_guard_v0_11 import PreHostCheckError


class PreHostNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = TemporaryDirectory(prefix="kuuos-v011-native-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.caller = import_module(guarded.CALLER_MODULE)
        cls.original_builder = staticmethod(getattr(cls.caller, guarded.BUILDER_BINDING))
        cls.original_host = staticmethod(act.run_host_tick)
        cls.store_originals = {
            module: getattr(import_module(module), name)
            for _, module, name in prior.STORE_BINDINGS
        }
        cls.observed_run = guarded.build_pre_host_guarded_native_fixture(cls.root)

    def report(self):
        return guarded._make_child_report(
            dict(self.observed_run.state_guard_calls),
            self.observed_run.pre_host_guard_calls,
            self.observed_run.native_audit,
        )

    def test_actual_child_checks_one_act_invocation_and_all_six_state_routes(self):
        run = self.observed_run
        self.assertEqual(run.status, guarded.SUCCESS)
        self.assertIs(type(run.pre_host_guard_calls), int)
        self.assertEqual(run.pre_host_guard_calls, 1)
        self.assertTrue(run.act_invocation_inputs_checked_before_host)
        self.assertEqual(run.native_audit.status, GOOD)
        self.assertEqual(tuple(dict(run.state_guard_calls)), prior.GUARDED_OS)
        self.assertTrue(all(type(n) is int and n > 0 for _, n in run.state_guard_calls))

    def test_parent_builder_host_and_store_bindings_remain_original(self):
        self.assertIs(getattr(self.caller, guarded.BUILDER_BINDING), self.original_builder)
        self.assertIs(self.original_builder, act.build_authorized_invoke_event)
        self.assertIs(act.run_host_tick, self.original_host)
        for _, module, name in prior.STORE_BINDINGS:
            self.assertIs(getattr(import_module(module), name), self.store_originals[module])

    def test_actual_child_does_not_inherit_parent_invocation_replacement(self):
        with TemporaryDirectory(prefix="kuuos-v011-parent-isolation-") as folder:
            with patch.object(self.caller, guarded.BUILDER_BINDING,
                              side_effect=AssertionError("parent replacement reached")) as replacement:
                observed = guarded.build_pre_host_guarded_native_fixture(Path(folder))
                replacement.assert_not_called()
                self.assertIs(getattr(self.caller, guarded.BUILDER_BINDING), replacement)
        self.assertEqual(observed.status, guarded.SUCCESS)
        self.assertEqual(observed.pre_host_guard_calls, 1)
        self.assertIs(getattr(self.caller, guarded.BUILDER_BINDING), self.original_builder)

    def test_native_record_keeps_original_v09_format(self):
        import json
        from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
            EVIDENCE_KEYS, VERSION,
        )
        record = json.loads((self.root / EVIDENCE_FILE).read_text())
        self.assertEqual(set(record), EVIDENCE_KEYS)
        self.assertEqual(record["version"], VERSION)
        self.assertEqual(record["record_sha256"], self.observed_run.native_audit.record_sha256)

    def test_scope_never_claims_atomicity_rollback_authentication_or_authority(self):
        run = self.observed_run
        for field in ("all_effects_prevented_on_any_failure", "host_rollback_guaranteed",
                      "state_commit_atomic_with_host", "external_issuer_authenticated",
                      "historical_guard_execution_proved", "lean_python_refinement_proved",
                      "execution_authority_granted", "truth_authority_granted",
                      "git_merge_authority_granted"):
            self.assertIs(getattr(run, field), False, field)
        self.assertEqual(run.guard_observation_mode, "local_child_stdout_unattested")
        self.assertTrue(run.counts_include_recovery_replays)
        with self.assertRaises(FrozenInstanceError):
            run.execution_authority_granted = True

    def test_read_only_audit_does_not_reexecute_pre_host_guard(self):
        paths = [p for p in self.root.rglob("*") if p.is_file()]
        before = {str(p): p.read_bytes() for p in paths}
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with patch.object(guarded, "checked_build_authorized_invoke_event",
                              side_effect=AssertionError("invoke")):
                observed = guarded.audit_local_evidence(self.root)
        self.assertEqual(observed.status, GOOD)
        self.assertFalse(observed.historical_issuance_proved)
        self.assertEqual(before, {str(p): p.read_bytes() for p in paths})

    def test_missing_evidence_stays_no_data(self):
        with TemporaryDirectory() as folder:
            result = guarded.audit_local_evidence(Path(folder))
        self.assertEqual(result.status, "NO_DATA")
        self.assertFalse(result.local_record_checked)

    def test_nonempty_root_is_not_reexecuted_or_overwritten(self):
        before = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                guarded.build_pre_host_guarded_native_fixture(self.root)
        self.assertEqual(before, (self.root / EVIDENCE_FILE).read_bytes())

    def test_source_failure_stops_before_child_or_new_files(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch("scripts.check_kuuos_lean_python_pre_host_sources_v0_11.check_sources",
                       return_value=("source_byte_drift:host",)):
                with patch.object(guarded.subprocess, "run", side_effect=AssertionError("spawn")):
                    with self.assertRaisesRegex(ValueError, "source_preflight"):
                        guarded.build_pre_host_guarded_native_fixture(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_binding_restored_after_scope_exception(self):
        with self.assertRaisesRegex(RuntimeError, "test interruption"):
            with guarded._guard_native_invocation({"ActOS": 0}):
                self.assertIsNot(getattr(self.caller, guarded.BUILDER_BINDING), self.original_builder)
                self.assertIs(act.build_authorized_invoke_event, self.original_builder)
                self.assertIs(act.run_host_tick, self.original_host)
                raise RuntimeError("test interruption")
        self.assertIs(getattr(self.caller, guarded.BUILDER_BINDING), self.original_builder)

    def test_nonoriginal_caller_binding_is_refused_and_preserved(self):
        replacement = lambda **kwargs: None
        with patch.object(self.caller, guarded.BUILDER_BINDING, replacement):
            with self.assertRaisesRegex(ValueError, "original_native_invocation_binding"):
                with guarded._guard_native_invocation({"ActOS": 0}):
                    self.fail("entered an untrusted binding")
            self.assertIs(getattr(self.caller, guarded.BUILDER_BINDING), replacement)

    def test_only_fresh_exact_integer_counters_are_accepted(self):
        for counts in ({}, {"ActOS": True}, {"ActOS": 0.0}, {"ActOS": 1},
                       {"ActOS": 0, "Other": 0}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                with guarded._guard_native_invocation(counts):
                    self.fail("invalid counter accepted")

    def test_real_native_finish_expired_authorization_calls_no_host_and_appends_nothing(self):
        from runtime.kuuos_act_os_fixture_v0_1 import (
            host_inputs, prepared_project_state, source_plan,
        )
        from runtime.v01_act_os_authority_bound_invocation import _finish
        with TemporaryDirectory(prefix="kuuos-v011-expired-") as folder:
            root = Path(folder)
            plan, activation = source_plan(root)
            policy, bundle, license_packet, projection = host_inputs(job_id="v011-expired")
            store, state = prepared_project_state(
                root=root / "act", act_id="v011-expired", plan_state=plan,
                plan_activation=activation, job_id="v011-expired",
                host_license=license_packet, projection=projection,
            )
            paths = [p for p in root.rglob("*") if p.is_file()]
            before = {str(p): p.read_bytes() for p in paths}
            counters = {"ActOS": 0}
            with guarded._guard_native_invocation(counters):
                with prior._guard_native_stores({name: 0 for name in prior.GUARDED_OS}):
                    with patch.object(act, "run_host_tick", wraps=act.run_host_tick) as host:
                        with self.assertRaises(PreHostCheckError) as raised:
                            _finish(store=store, state=state, bundle=bundle, policy=policy,
                                    invoke_ms=200_000)
                        self.assertFalse(raised.exception.host_call_attempted)
                        host.assert_not_called()
            self.assertEqual(counters, {"ActOS": 0})
            self.assertEqual(before, {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()})
            self.assertIs(getattr(self.caller, guarded.BUILDER_BINDING), self.original_builder)

    def test_report_requires_exactly_one_successful_pre_host_call(self):
        for value in (None, False, True, 0, -1, 1.0, "1", 2):
            report = self.report()
            report["pre_host_guard_calls"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_requires_all_six_state_counters(self):
        for value in (None, True, 0, -1, 1.0, "1"):
            report = self.report()
            report["state_guard_calls"]["ActOS"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)
        report = self.report()
        del report["state_guard_calls"]["PlanOS"]
        with self.assertRaises(ValueError):
            guarded._checked_report(report, self.observed_run.native_audit)

    def test_report_binds_source_record_and_scope(self):
        for key, value in (("source_main", "other"), ("version", "other"),
                           ("native_record_sha256", "other"), ("status", "APPLIED"),
                           ("act_invocation_inputs_checked_before_host", 1),
                           ("counts_include_recovery_replays", False),
                           ("all_effects_prevented_on_any_failure", True),
                           ("external_issuer_signature", "invented")):
            report = self.report()
            report[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                guarded._checked_report(report, self.observed_run.native_audit)

    def test_cli_requires_explicit_fixture_mode(self):
        with redirect_stderr(StringIO()):
            self.assertEqual(guarded.main([]), 2)
            self.assertEqual(guarded.main(["--audit", str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
