"""Original child, actual Decision/Plural ledgers and write-once evidence v0.17.
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

from runtime import kuuos_lean_python_decision_evidence_native_cycle_v0_17 as native
from runtime import kuuos_lean_python_decision_evidence_guard_v0_17 as guard
from runtime import kuuos_lean_python_wa_profile_source_native_cycle_v0_16 as previous
from runtime import kuuos_lean_python_wa_profile_source_guard_v0_16 as profile
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import EVIDENCE_FILE, GOOD
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class DecisionEvidenceNativeCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v017-real-child-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.observed_run = native.build_decision_evidence_native_fixture(cls.root)

    def test_child_has_every_eight_os_path_and_upstream_guard_call(self):
        run = self.observed_run
        self.assertEqual(run.status, native.SUCCESS)
        self.assertEqual(run.native_audit.status, GOOD)
        self.assertEqual(run.decision_guard_calls, run.wa_profile_source_guard_calls)
        self.assertEqual(run.decision_guard_calls, run.wa_evaluation_guard_calls)
        self.assertEqual(run.decision_guard_calls, run.wa_gate_guard_calls)
        self.assertEqual(run.decision_guard_calls, run.wa_numeric_guard_calls)
        self.assertEqual(run.decision_guard_calls, dict(run.state_guard_calls)["DecisionOSWa"])
        self.assertEqual(len(run.state_guard_calls), 8)
        self.assertEqual(run.pre_host_guard_calls, 1)

    def test_parent_recovered_real_stores_and_local_receipt_match_child(self):
        root = self.root
        dec = DecisionStore(root / "decision").recover(require_snapshot_match=True)
        plur = PluralDecisionStore(root / "plural").recover(require_snapshot_match=True)
        evidence = native._evidence_record(root)
        identity = guard.checked_local_decision_receipt_chain(dec, plur, evidence)
        self.assertEqual(identity["decision_witness_digest"], self.observed_run.decision_witness_digest)
        self.assertEqual(identity["plural_witness_digest"], self.observed_run.plural_witness_digest)
        self.assertEqual(identity["native_receipt_digest"], self.observed_run.native_receipt_digest)
        self.assertEqual(identity["belief_receipt_digest"], self.observed_run.belief_receipt_digest)
        self.assertEqual(plur["source_decision_state_digest"], dec["decision_state_digest"])

    def test_existing_write_once_record_is_preserved_under_read_only_postflight(self):
        path = self.root / EVIDENCE_FILE
        original = path.read_bytes()
        with patch.object(native.subprocess, "run", side_effect=AssertionError("spawned")):
            audit = native.audit_local_evidence(self.root)
            after = native._postflight(self.root, audit)
        self.assertEqual(audit.status, GOOD)
        self.assertEqual(after["decision_witness_digest"], self.observed_run.decision_witness_digest)
        self.assertEqual(path.read_bytes(), original)

    def test_existing_fixture_root_is_not_overwritten_or_reexecuted(self):
        previous_record = (self.root / EVIDENCE_FILE).read_bytes()
        with patch.object(native.subprocess, "run", side_effect=AssertionError("spawned")):
            with self.assertRaisesRegex(ValueError, "no_overwrite"):
                native.build_decision_evidence_native_fixture(self.root)
        self.assertEqual((self.root / EVIDENCE_FILE).read_bytes(), previous_record)

    def test_missing_decision_ledger_blocks_prior_to_wa_store_guard(self):
        with TemporaryDirectory(prefix="kuuos-v017-no-decision-") as directory:
            root = Path(directory)
            count, witness = {"DecisionOSWa": 0}, [""]
            with native._guard_decision_source_boundary(root, count, witness):
                with self.assertRaises(guard.DecisionEvidenceBoundaryError) as caught:
                    previous.checked_apply_wa_profile_source_event({}, {}, {})
            self.assertEqual(caught.exception.status, "NO_DATA")
            self.assertEqual(count["DecisionOSWa"], 0)
            self.assertEqual(witness, [""])

    def test_parent_patch_does_not_cross_child_boundary(self):
        with TemporaryDirectory(prefix="kuuos-v017-parent-patch-") as directory:
            with patch.object(previous, "checked_apply_wa_profile_source_event",
                              side_effect=AssertionError("parent-patch")) as patched:
                result = native.build_decision_evidence_native_fixture(Path(directory))
                patched.assert_not_called()
        self.assertEqual(result.status, native.SUCCESS)

    def test_guard_context_restores_original_binding_on_failure(self):
        original = previous.checked_apply_wa_profile_source_event
        self.assertIs(original, profile.checked_apply_wa_profile_source_event)
        with self.assertRaisesRegex(RuntimeError, "interrupted"):
            with native._guard_decision_source_boundary(self.root, {"DecisionOSWa": 0}, [""]):
                self.assertIsNot(previous.checked_apply_wa_profile_source_event, original)
                raise RuntimeError("interrupted")
        self.assertIs(previous.checked_apply_wa_profile_source_event, original)

    def test_invalid_counters_and_untrusted_prior_adapter_rejected(self):
        for counts in (None, {}, {"DecisionOSWa": True}, {"DecisionOSWa": 1},
                       {"DecisionOSWa": 0, "DecisionOSPlural": 0}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                with native._guard_decision_source_boundary(self.root, counts, [""]):
                    self.fail("bad counter accepted")
        with patch.object(previous, "checked_apply_wa_profile_source_event", lambda *a: {}):
            with self.assertRaisesRegex(ValueError, "original_profile_source_boundary"):
                with native._guard_decision_source_boundary(self.root, {"DecisionOSWa": 0}, [""]):
                    self.fail("foreign adapter accepted")

    def test_original_real_decision_ledger_tampering_blocks_recovery(self):
        with TemporaryDirectory(prefix="kuuos-v017-ledger-tamper-") as directory:
            dest = Path(directory)
            source = self.root / "decision"
            store = DecisionStore(dest)
            dest.mkdir(exist_ok=True)
            for name in ("decision-genesis.json", "decision-ledger.jsonl", "decision-snapshot.json"):
                (dest / name).write_bytes((source / name).read_bytes())
            lines = store.ledger_path.read_text().splitlines()
            tampered = json.loads(lines[-1])
            tampered["result_decision_state_digest"] = "forged"
            lines[-1] = json.dumps(tampered, sort_keys=True)
            store.ledger_path.write_text("\n".join(lines) + "\n")
            with self.assertRaises(Exception):
                store.recover(require_snapshot_match=True)

    def test_child_report_scope_and_digests_fail_closed(self):
        r = self.observed_run
        for attr in ("external_issuer_authenticated", "historical_guard_execution_proved",
                     "lean_python_refinement_proved", "all_store_writes_guarded",
                     "state_commit_atomic_with_host", "host_rollback_guaranteed",
                     "execution_authority_granted", "truth_authority_granted",
                     "git_merge_authority_granted"):
            self.assertIs(getattr(r, attr), False)
        with self.assertRaises(FrozenInstanceError):
            r.truth_authority_granted = True
        # Reconstruct exactly the unchanged nested v0.12-v0.16 report format.
        from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as mediated
        from runtime import kuuos_lean_python_wa_numeric_native_cycle_v0_13 as numeric
        from runtime import kuuos_lean_python_wa_gate_native_cycle_v0_14 as gate
        from runtime import kuuos_lean_python_wa_evaluation_native_cycle_v0_15 as evaluation
        base = mediated._make_child_report(dict(r.state_guard_calls), r.pre_host_guard_calls, r.native_audit)
        n = numeric._make_child_report(base, r.wa_numeric_guard_calls)
        g = gate._make_child_report(n, r.wa_gate_guard_calls)
        e = evaluation._make_child_report(g, r.wa_evaluation_guard_calls)
        p = previous._make_child_report(e, r.wa_profile_source_guard_calls, r.plural_witness_digest)
        report = native._make_child_report(p, r.decision_guard_calls, {
            "decision_witness_digest": r.decision_witness_digest,
            "native_receipt_digest": r.native_receipt_digest,
            "belief_receipt_digest": r.belief_receipt_digest,
        })
        self.assertEqual(set(report), native.REPORT_KEYS)
        self.assertEqual(native._checked_report(report, r.native_audit)[-3], r.decision_witness_digest)
        for bad in (None, 0, True, r.decision_guard_calls + 1):
            broken = deepcopy(report)
            broken["decision_guard_calls"] = bad
            with self.subTest(count=bad), self.assertRaises(ValueError):
                native._checked_report(broken, r.native_audit)
        for bad in (None, "invalid", "z" * 64):
            broken = deepcopy(report)
            broken["decision_witness_digest"] = bad
            with self.subTest(digest=bad), self.assertRaises(ValueError):
                native._checked_report(broken, r.native_audit)


if __name__ == "__main__":
    unittest.main()
