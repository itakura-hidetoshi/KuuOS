"""Local Belief gerbe ledger and exact native receipt v0.18 regressions.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_belief_receipt_guard_v0_18 as guard
from runtime import kuuos_lean_python_decision_evidence_guard_v0_17 as prior
from runtime import kuuos_qi_world_native_full_cycle_v1_3 as native
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_belief_os_gerbe_types_v0_3 import state_digest
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_KEYS, VERSION, SOURCE_MAIN, MODE, evidence_digest, root_binding,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class BeliefReceiptGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v018-pure-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.receipt = native.build_native_full_cycle_receipt(cls.root)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.belief = BeliefGerbeStore(cls.root / "belief").recover(require_snapshot_match=True)
        cls.genesis = json.loads((cls.root / "belief/belief-gerbe-genesis.json").read_text())
        cls.commits = [json.loads(row) for row in
                       (cls.root / "belief/belief-gerbe-ledger.jsonl").read_text().splitlines()]
        cls.wa_genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.wa_event = json.loads((cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()[0])["event"]
        cls.record = {
            "version": VERSION, "source_main": SOURCE_MAIN, "mode": MODE,
            "root_binding_sha256": root_binding(cls.root),
            "native_cycle_receipt": cls.receipt, "return_capture": {},
            "native_cycle_digest": cls.receipt["native_full_cycle_receipt_digest"],
            "return_capture_sha256": "test-only-opaque", "record_sha256": "",
        }
        cls.record["record_sha256"] = evidence_digest(cls.record)
        assert set(cls.record) == EVIDENCE_KEYS

    def checked(self, *, genesis=None, commits=None, belief=None, record=None):
        return guard.checked_local_belief_receipt_chain(
            self.decision, self.plural,
            self.genesis if genesis is None else genesis,
            self.commits if commits is None else commits,
            self.belief if belief is None else belief,
            self.record if record is None else record,
        )

    def test_real_original_gerbe_ledger_replays_full_native_receipt(self):
        identity = self.checked()
        self.assertEqual(identity["belief_state_witness_digest"], _fingerprint(self.belief))
        self.assertEqual(identity["belief_ledger_commit_count"], len(self.commits))
        self.assertEqual(identity["belief_last_commit_digest"],
                         self.commits[-1]["belief_gerbe_store_commit_digest"])
        self.assertEqual(identity["belief_receipt_digest"],
                         self.decision["source_belief_receipt_digest"])
        original, last = guard._replay_belief_ledger(self.genesis, self.commits, self.belief)
        self.assertEqual(original, self.receipt["native_artifacts"]["BeliefOSReceipt"])
        self.assertEqual(last, identity["belief_last_commit_digest"])

    def test_selected_original_wa_native_apply_is_byte_identical(self):
        expected = prior.checked_apply_wa_decision_evidence_event(
            self.wa_genesis, self.wa_event, self.plural, self.decision)
        actual = guard.checked_apply_wa_belief_receipt_event(
            self.wa_genesis, self.wa_event, self.plural, self.decision, self.belief)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["status"], "APPLIED")
        replay = guard.checked_apply_wa_belief_receipt_event(
            actual["state"], self.wa_event, self.plural, self.decision, self.belief)
        self.assertEqual(replay["status"], "REPLAYED")
        self.assertEqual(replay, prior.checked_apply_wa_decision_evidence_event(
            actual["state"], self.wa_event, self.plural, self.decision))

    def test_stale_belief_receipt_blocks_before_prior_wa_apply(self):
        changed = deepcopy(self.belief)
        changed["latest_receipt_digest"] = "self-consistent-but-wrong"
        changed["belief_gerbe_state_digest"] = state_digest(changed)
        with patch.object(prior, "checked_apply_wa_decision_evidence_event") as old:
            with self.assertRaises(guard.BeliefReceiptBoundaryError):
                guard.checked_apply_wa_belief_receipt_event(
                    self.wa_genesis, self.wa_event, self.plural, self.decision, changed)
            old.assert_not_called()

    def test_wrong_belief_lineage_blocks_upstream(self):
        changed = deepcopy(self.belief)
        changed["lineage_id"] = "different-local-lineage"
        changed["belief_gerbe_state_digest"] = state_digest(changed)
        with patch.object(prior, "checked_apply_wa_decision_evidence_event") as old:
            with self.assertRaisesRegex(guard.BeliefReceiptBoundaryError,
                                        "decision_lineage_mismatch"):
                guard.checked_apply_wa_belief_receipt_event(
                    self.wa_genesis, self.wa_event, self.plural, self.decision, changed)
            old.assert_not_called()

    def test_missing_local_belief_or_ledger_is_no_data(self):
        with self.assertRaises(guard.BeliefReceiptBoundaryError) as caught:
            guard.checked_apply_wa_belief_receipt_event(
                self.wa_genesis, self.wa_event, self.plural, self.decision, None)
        self.assertEqual(caught.exception.status, "NO_DATA")
        with self.assertRaises(guard.BeliefReceiptBoundaryError) as caught:
            self.checked(commits=[])
        self.assertEqual(caught.exception.status, "NO_DATA")

    def test_rewritten_ledger_commit_digest_rejected_before_receipt_link(self):
        changed = deepcopy(self.commits)
        changed[0]["belief_gerbe_store_commit_digest"] = "x" * 64
        with self.assertRaisesRegex(guard.BeliefReceiptBoundaryError,
                                    "store_commit_digest_invalid"):
            self.checked(commits=changed)

    def test_altered_belief_ledger_packet_rejected_even_if_store_digest_resealed(self):
        from runtime.kuuos_belief_os_gerbe_types_v0_3 import store_commit_digest
        changed = deepcopy(self.commits)
        changed[0]["packet"]["target_context_id"] = "forged-target"
        changed[0]["belief_gerbe_store_commit_digest"] = store_commit_digest(changed[0])
        with self.assertRaises(guard.BeliefReceiptBoundaryError):
            self.checked(commits=changed)

    def test_replayed_belief_source_content_requires_exact_native_receipt(self):
        changed = deepcopy(self.record)
        changed["native_cycle_receipt"]["native_artifacts"]["BeliefOSReceipt"]["target_context_id"] = "forged"
        changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"] = native.full_cycle_receipt_digest(
            changed["native_cycle_receipt"])
        changed["native_cycle_digest"] = changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"]
        changed["record_sha256"] = evidence_digest(changed)
        with self.assertRaises(guard.BeliefReceiptBoundaryError):
            self.checked(record=changed)

    def test_copied_native_belief_state_must_match_recovered_real_ledger(self):
        changed = deepcopy(self.record)
        changed["native_cycle_receipt"]["native_artifacts"]["BeliefOSState"]["lineage_id"] = "changed"
        changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"] = native.full_cycle_receipt_digest(
            changed["native_cycle_receipt"])
        changed["native_cycle_digest"] = changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"]
        changed["record_sha256"] = evidence_digest(changed)
        with self.assertRaises(guard.BeliefReceiptBoundaryError):
            self.checked(record=changed)

    def test_altered_recovered_belief_state_cannot_match_actual_ledger(self):
        changed = deepcopy(self.belief)
        changed["updated_at_ms"] += 1
        changed["belief_gerbe_state_digest"] = state_digest(changed)
        with self.assertRaisesRegex(guard.BeliefReceiptBoundaryError,
                                    "replayed_final_state_differs"):
            self.checked(belief=changed)

    def test_original_commit_dense_index_and_predecessors_are_enforced(self):
        for field, value in (("commit_index", 2),
                             ("predecessor_commit_digest", "nonempty"),
                             ("predecessor_gerbe_state_digest", "foreign")):
            changed = deepcopy(self.commits)
            changed[0][field] = value
            with self.subTest(field=field), self.assertRaises(guard.BeliefReceiptBoundaryError):
                self.checked(commits=changed)

    def test_prior_boundary_no_data_is_not_upgraded(self):
        with patch.object(prior, "checked_apply_wa_decision_evidence_event",
                          side_effect=prior.DecisionEvidenceBoundaryError("NO_DATA", ("missing",))):
            with self.assertRaises(guard.BeliefReceiptBoundaryError) as caught:
                guard.checked_apply_wa_belief_receipt_event(
                    self.wa_genesis, self.wa_event, self.plural, self.decision, self.belief)
        self.assertEqual(caught.exception.status, "NO_DATA")

    def test_all_inputs_unchanged_and_nonfinite_or_nonbuiltin_refused(self):
        before = _fingerprint([self.decision, self.plural, self.genesis, self.commits,
                               self.belief, self.record, self.wa_genesis, self.wa_event])
        self.checked()
        guard.checked_apply_wa_belief_receipt_event(
            self.wa_genesis, self.wa_event, self.plural, self.decision, self.belief)
        self.assertEqual(before, _fingerprint([self.decision, self.plural, self.genesis,
                                               self.commits, self.belief, self.record,
                                               self.wa_genesis, self.wa_event]))
        with self.assertRaises(guard.BeliefReceiptBoundaryError):
            guard.checked_local_belief_receipt_chain(
                self.decision, self.plural, self.genesis,
                {"bad": True}, self.belief, self.record)
        with self.assertRaises(guard.BeliefReceiptBoundaryError):
            guard.checked_local_belief_receipt_chain(
                self.decision, self.plural, self.genesis,
                self.commits, self.belief, {"nan": float("nan")})


if __name__ == "__main__":
    unittest.main()
