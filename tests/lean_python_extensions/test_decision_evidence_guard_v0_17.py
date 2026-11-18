"""Actual native-state Decision->Plural projection and receipt regressions v0.17.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_decision_evidence_guard_v0_17 as guard
from runtime import kuuos_lean_python_wa_profile_source_guard_v0_16 as prior
from runtime import kuuos_qi_world_native_full_cycle_v1_3 as native
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_KEYS, VERSION, SOURCE_MAIN, MODE, evidence_digest, root_binding,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class DecisionEvidenceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v017-pure-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.receipt = native.build_native_full_cycle_receipt(cls.root)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.first_event = json.loads((cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()[0])["event"]
        record = {
            "version": VERSION, "source_main": SOURCE_MAIN, "mode": MODE,
            "root_binding_sha256": root_binding(cls.root),
            "native_cycle_receipt": cls.receipt,
            "return_capture": {}, "native_cycle_digest": cls.receipt["native_full_cycle_receipt_digest"],
            "return_capture_sha256": "opaque-test-only", "record_sha256": "",
        }
        cls.record = record
        record["record_sha256"] = evidence_digest(record)
        assert set(record) == EVIDENCE_KEYS

    def test_original_native_wa_result_is_exact(self):
        original = prior.checked_apply_wa_profile_source_event(self.genesis, self.first_event, self.plural)
        actual = guard.checked_apply_wa_decision_evidence_event(
            self.genesis, self.first_event, self.plural, self.decision)
        self.assertEqual(actual, original)
        self.assertEqual(actual["status"], "APPLIED")

    def test_real_local_decision_projection_exact(self):
        guard._check_decision_plural(self.decision, self.plural)
        self.assertEqual(self.plural["source_decision_state_digest"], self.decision["decision_state_digest"])
        self.assertEqual(self.plural["source_committed_decision_digest"],
                         self.decision["latest_committed_decision_digest"])
        self.assertEqual(self.plural["source_options_digest"], _fingerprint(self.plural["source_options"]))

    def test_local_evidence_receipt_and_belief_reference_exact(self):
        result = guard.checked_local_decision_receipt_chain(self.decision, self.plural, self.record)
        self.assertEqual(result["decision_witness_digest"], _fingerprint(self.decision))
        self.assertEqual(result["plural_witness_digest"], _fingerprint(self.plural))
        self.assertEqual(result["native_receipt_digest"], self.receipt["native_full_cycle_receipt_digest"])
        self.assertEqual(result["belief_receipt_digest"], self.decision["source_belief_receipt_digest"])

    def test_decision_projection_mutations_block_before_prior_wa_adapter(self):
        for source in guard._DECISION_PLURAL_FIELDS:
            changed = deepcopy(self.plural)
            changed[source] = "forged-upstream-decision"
            with self.subTest(source=source), patch.object(prior, "checked_apply_wa_profile_source_event") as old:
                with self.assertRaises(guard.DecisionEvidenceBoundaryError):
                    guard.checked_apply_wa_decision_evidence_event(
                        self.genesis, self.first_event, changed, self.decision)
                old.assert_not_called()

    def test_resealed_decision_cannot_replace_recovered_upstream_witness(self):
        changed = deepcopy(self.decision)
        changed["source_belief_receipt_digest"] = "false-source-reference"
        changed["decision_state_digest"] = _fingerprint(
            {k: v for k, v in changed.items() if k != "decision_state_digest"})
        with patch.object(prior, "checked_apply_wa_profile_source_event") as old:
            with self.assertRaises(guard.DecisionEvidenceBoundaryError):
                guard.checked_apply_wa_decision_evidence_event(
                    self.genesis, self.first_event, self.plural, changed)
            old.assert_not_called()

    def test_selected_source_option_contents_and_order_bound_to_decision(self):
        changed = deepcopy(self.plural)
        changed["source_options"] = list(reversed(changed["source_options"]))
        changed["source_options_digest"] = _fingerprint(changed["source_options"])
        with self.assertRaisesRegex(guard.DecisionEvidenceBoundaryError,
                                    "source_options:decision_ledger_projection_mismatch"):
            guard._check_decision_plural(self.decision, changed)

    def test_missing_decision_or_receipt_not_promoted_to_success(self):
        for field, item in (("decision", None), ("plural", None)):
            with self.subTest(field=field):
                with self.assertRaises(guard.DecisionEvidenceBoundaryError) as caught:
                    guard.checked_apply_wa_decision_evidence_event(
                        self.genesis, self.first_event,
                        None if field == "plural" else self.plural,
                        None if field == "decision" else self.decision)
                self.assertEqual(caught.exception.status, "NO_DATA")
        with self.assertRaises(guard.DecisionEvidenceBoundaryError) as caught:
            guard.checked_local_decision_receipt_chain(self.decision, self.plural, None)
        self.assertEqual(caught.exception.status, "NO_DATA")

    def test_missing_source_decision_projection_is_no_data(self):
        changed = deepcopy(self.plural)
        changed.pop("source_committed_decision_digest")
        with self.assertRaises(guard.DecisionEvidenceBoundaryError) as caught:
            guard._check_decision_plural(self.decision, changed)
        self.assertEqual(caught.exception.status, "NO_DATA")

    def test_native_receipt_artifact_must_equal_actual_recovered_decision_and_plural(self):
        for name in ("DecisionOS", "DecisionOSPlural"):
            changed = deepcopy(self.record)
            changed["native_cycle_receipt"]["native_artifacts"][name]["lineage_id"] = "replaced"
            changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"] = native.full_cycle_receipt_digest(
                changed["native_cycle_receipt"])
            changed["native_cycle_digest"] = changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"]
            changed["record_sha256"] = evidence_digest(changed)
            with self.subTest(name=name), self.assertRaises(guard.DecisionEvidenceBoundaryError):
                guard.checked_local_decision_receipt_chain(self.decision, self.plural, changed)

    def test_locally_changed_belief_receipt_not_external_certificate(self):
        changed = deepcopy(self.record)
        changed["native_cycle_receipt"]["native_artifacts"]["BeliefOSReceipt"]["route"] = "HOLD"
        changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"] = native.full_cycle_receipt_digest(
            changed["native_cycle_receipt"])
        changed["native_cycle_digest"] = changed["native_cycle_receipt"]["native_full_cycle_receipt_digest"]
        changed["record_sha256"] = evidence_digest(changed)
        with self.assertRaises(guard.DecisionEvidenceBoundaryError):
            guard.checked_local_decision_receipt_chain(self.decision, self.plural, changed)

    def test_local_evidence_digest_mismatch_blocks(self):
        changed = deepcopy(self.record)
        changed["native_cycle_digest"] = "not-original"
        with self.assertRaisesRegex(guard.DecisionEvidenceBoundaryError, "local_record_digest_mismatch"):
            guard.checked_local_decision_receipt_chain(self.decision, self.plural, changed)

    def test_prior_adapter_failure_keeps_blocked_and_no_data(self):
        with patch.object(prior, "checked_apply_wa_profile_source_event",
                          side_effect=prior.WaProfileSourceBoundaryError("NO_DATA", ("fixture_missing",))):
            with self.assertRaises(guard.DecisionEvidenceBoundaryError) as caught:
                guard.checked_apply_wa_decision_evidence_event(
                    self.genesis, self.first_event, self.plural, self.decision)
        self.assertEqual(caught.exception.status, "NO_DATA")

    def test_inputs_unchanged_and_nonfinite_or_nonbuiltin_rejected(self):
        before = _fingerprint([self.genesis, self.first_event, self.plural, self.decision, self.record])
        guard.checked_apply_wa_decision_evidence_event(self.genesis, self.first_event, self.plural, self.decision)
        guard.checked_local_decision_receipt_chain(self.decision, self.plural, self.record)
        self.assertEqual(_fingerprint([self.genesis, self.first_event, self.plural, self.decision, self.record]), before)
        with self.assertRaises(guard.DecisionEvidenceBoundaryError):
            guard.checked_local_decision_receipt_chain(self.decision, self.plural, {"nan": float("nan")})
        with self.assertRaises(guard.DecisionEvidenceBoundaryError):
            guard.checked_apply_wa_decision_evidence_event(self.genesis, self.first_event, (), self.decision)


if __name__ == "__main__":
    unittest.main()
