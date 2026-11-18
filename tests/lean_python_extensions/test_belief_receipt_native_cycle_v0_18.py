"""Real child and original Belief store native receipt v0.18 regressions.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_belief_receipt_guard_v0_18 as guard
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime import kuuos_lean_python_decision_evidence_native_cycle_v0_17 as prior
from runtime import kuuos_lean_python_decision_evidence_guard_v0_17 as prior_guard
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import EVIDENCE_FILE, GOOD
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class BeliefReceiptNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v018-native-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.result = native.build_belief_receipt_native_fixture(cls.root)

    def test_real_child_replays_original_native_eight_os_routes(self):
        r = self.result
        self.assertEqual(r.status, native.SUCCESS)
        self.assertEqual(r.native_audit.status, GOOD)
        self.assertEqual(len(r.state_guard_calls), 8)
        self.assertEqual(r.belief_guard_calls, r.decision_guard_calls)
        self.assertEqual(r.belief_guard_calls, r.wa_profile_source_guard_calls)
        self.assertEqual(r.belief_guard_calls, r.wa_evaluation_guard_calls)
        self.assertEqual(r.belief_guard_calls, r.wa_gate_guard_calls)
        self.assertEqual(r.belief_guard_calls, r.wa_numeric_guard_calls)
        self.assertEqual(r.pre_host_guard_calls, 1)

    def test_parent_original_belief_store_and_receipt_exact(self):
        r = self.result
        identity = native._postflight(self.root, r.native_audit)
        self.assertEqual(identity["belief_state_witness_digest"], r.belief_state_witness_digest)
        self.assertEqual(identity["belief_last_commit_digest"], r.belief_last_commit_digest)
        self.assertEqual(identity["belief_ledger_commit_count"], r.belief_ledger_commit_count)
        self.assertEqual(identity["belief_receipt_digest"], r.belief_receipt_digest)
        belief = BeliefGerbeStore(self.root / "belief").recover(require_snapshot_match=True)
        self.assertEqual(_fingerprint(belief), r.belief_state_witness_digest)
        self.assertEqual(r.belief_ledger_commit_count, 1)

    def test_readonly_postflight_preserves_original_write_once_record(self):
        path = self.root / EVIDENCE_FILE
        original = path.read_bytes()
        with patch.object(native.subprocess, "run", side_effect=AssertionError("spawn")):
            audit = native.audit_local_evidence(self.root)
            identity = native._postflight(self.root, audit)
        self.assertEqual(audit.status, GOOD)
        self.assertEqual(identity["belief_state_witness_digest"], self.result.belief_state_witness_digest)
        self.assertEqual(path.read_bytes(), original)

    def test_parent_cannot_reexecute_nonempty_root(self):
        content = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(native.subprocess, "run", side_effect=AssertionError("spawn")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                native.build_belief_receipt_native_fixture(self.root)
        self.assertEqual((self.root / EVIDENCE_FILE).read_bytes(), content)

    def test_missing_belief_store_fails_before_previous_wa_call(self):
        with TemporaryDirectory(prefix="kuuos-v018-missing-belief-") as directory:
            root = Path(directory)
            counters, witness = {"DecisionOSWa": 0}, [""]
            with native._guard_belief_source_boundary(root, counters, witness):
                with self.assertRaises(guard.BeliefReceiptBoundaryError) as caught:
                    prior.checked_apply_wa_decision_evidence_event({}, {}, {}, {})
            self.assertEqual(caught.exception.status, "NO_DATA")
            self.assertEqual(counters["DecisionOSWa"], 0)
            self.assertEqual(witness, [""])

    def test_child_process_does_not_inherit_parent_patch(self):
        with TemporaryDirectory(prefix="kuuos-v018-parent-patch-") as directory:
            with patch.object(prior, "checked_apply_wa_decision_evidence_event",
                              side_effect=AssertionError("parent")) as patched:
                candidate = native.build_belief_receipt_native_fixture(Path(directory))
                patched.assert_not_called()
        self.assertEqual(candidate.status, native.SUCCESS)

    def test_original_boundary_restored_after_guard_exception(self):
        original = prior.checked_apply_wa_decision_evidence_event
        self.assertIs(original, prior_guard.checked_apply_wa_decision_evidence_event)
        with self.assertRaisesRegex(RuntimeError, "interrupted"):
            with native._guard_belief_source_boundary(self.root, {"DecisionOSWa": 0}, [""]):
                self.assertIsNot(prior.checked_apply_wa_decision_evidence_event, original)
                raise RuntimeError("interrupted")
        self.assertIs(prior.checked_apply_wa_decision_evidence_event, original)

    def test_foreign_prior_adapter_and_invalid_counters_refused(self):
        for count in (None, {}, {"DecisionOSWa": True}, {"DecisionOSWa": 1},
                      {"DecisionOSWa": 0, "DecisionOSPlural": 0}):
            with self.subTest(count=count), self.assertRaises(ValueError):
                with native._guard_belief_source_boundary(self.root, count, [""]):
                    self.fail("bad counter")
        with patch.object(prior, "checked_apply_wa_decision_evidence_event", lambda *args: {}):
            with self.assertRaisesRegex(ValueError, "original_decision_evidence_boundary"):
                with native._guard_belief_source_boundary(self.root, {"DecisionOSWa": 0}, [""]):
                    self.fail("foreign source")

    def test_actual_belief_ledger_tampering_is_detected_by_original_recovery(self):
        source = self.root / "belief"
        with TemporaryDirectory(prefix="kuuos-v018-copy-tamper-") as directory:
            root = Path(directory)
            for name in ("belief-gerbe-genesis.json", "belief-gerbe-ledger.jsonl",
                         "belief-gerbe-snapshot.json"):
                (root / name).write_bytes((source / name).read_bytes())
            ledger = root / "belief-gerbe-ledger.jsonl"
            contents = [json.loads(x) for x in ledger.read_text().splitlines()]
            contents[0]["belief_gerbe_receipt_digest"] = "forged"
            ledger.write_text("\n".join(json.dumps(x, sort_keys=True) for x in contents) + "\n")
            with self.assertRaises(Exception):
                BeliefGerbeStore(root).recover(require_snapshot_match=True)

    def test_unsigned_report_count_and_digest_must_be_exact(self):
        r = self.result
        from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as mediated
        from runtime import kuuos_lean_python_wa_numeric_native_cycle_v0_13 as numeric
        from runtime import kuuos_lean_python_wa_gate_native_cycle_v0_14 as gate
        from runtime import kuuos_lean_python_wa_evaluation_native_cycle_v0_15 as evalv
        from runtime import kuuos_lean_python_wa_profile_source_native_cycle_v0_16 as prof
        base = mediated._make_child_report(dict(r.state_guard_calls), r.pre_host_guard_calls, r.native_audit)
        n = numeric._make_child_report(base, r.wa_numeric_guard_calls)
        g = gate._make_child_report(n, r.wa_gate_guard_calls)
        e = evalv._make_child_report(g, r.wa_evaluation_guard_calls)
        p = prof._make_child_report(e, r.wa_profile_source_guard_calls, r.plural_witness_digest)
        dec = prior._make_child_report(p, r.decision_guard_calls, {
            "decision_witness_digest": r.decision_witness_digest,
            "native_receipt_digest": r.native_receipt_digest,
            "belief_receipt_digest": r.belief_receipt_digest,
        })
        report = native._make_child_report(dec, r.belief_guard_calls, {
            "belief_state_witness_digest": r.belief_state_witness_digest,
            "belief_last_commit_digest": r.belief_last_commit_digest,
            "belief_ledger_commit_count": r.belief_ledger_commit_count,
        })
        self.assertEqual(set(report), native.REPORT_KEYS)
        self.assertEqual(native._checked_report(report, r.native_audit)[-1],
                         r.belief_ledger_commit_count)
        for field, candidates in (
            ("belief_guard_calls", (None, True, 0, r.belief_guard_calls + 1)),
            ("belief_ledger_commit_count", (None, True, 0, -1)),
            ("belief_last_commit_digest", (None, "zz" * 32, "x" * 63)),
        ):
            for candidate in candidates:
                changed = deepcopy(report)
                changed[field] = candidate
                with self.subTest(field=field, value=candidate), self.assertRaises(ValueError):
                    native._checked_report(changed, r.native_audit)

    def test_scope_retains_non_authority_and_immutable_receipt(self):
        for name in ("historical_guard_execution_proved", "external_issuer_authenticated",
                     "lean_python_refinement_proved", "all_store_writes_guarded",
                     "host_rollback_guaranteed", "state_commit_atomic_with_host",
                     "execution_authority_granted", "truth_authority_granted",
                     "git_merge_authority_granted"):
            self.assertIs(getattr(self.result, name), False, name)
        with self.assertRaises(FrozenInstanceError):
            self.result.execution_authority_granted = True


if __name__ == "__main__":
    unittest.main()
