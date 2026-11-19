"""Native original CodeAI → Lean Scorecard/Receipt condition regressions v0.30.

Use the existing five-source CodeAI fixture builder and original selector.
No mock CI successes, fake eligibility, host effects or Git mutations.
Source digests are local integrity, never external issuer authentication.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import unittest

from runtime import kuuos_lean_python_codeai_native_selection_v0_30 as audit
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from tests.test_kuuos_codeai_evidence_weighted_selection_abstention_v0_1 import (
    fixture, run, reseal_policy, reseal_record,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_ABSTAINED, DECISION_SELECTED, OUTCOME_FAILED,
)


def bound(data):
    result = run(data)
    return audit.audit_native_codeai_selection(
        data, result.decision, result.receipt
    )


class NativeCodeAISelectionBindingsTests(unittest.TestCase):
    def test_original_five_source_reference_selection_is_checked(self):
        data = fixture()
        result = bound(data)
        self.assertEqual(result.status, audit.PASS, result.issues)
        self.assertEqual(result.selection_case, DECISION_SELECTED)
        self.assertEqual(result.source_scorecards_checked, 4)
        self.assertTrue(result.selected_lean_condition_checked)
        self.assertTrue(result.original_selection_replayed)
        self.assertTrue(result.original_output_digest_checked)

    def test_high_evidence_score_never_overrides_source_admissibility(self):
        data = fixture()
        source = run(data)
        selected = next(x for x in source.decision["candidate_scorecards"]
                        if x["candidate_selected"])
        repairable = next(x for x in source.decision["candidate_scorecards"]
                          if x["candidate_id"] == "candidate-repairable")
        self.assertGreater(repairable["evidence_score"], selected["evidence_score"])
        self.assertFalse(repairable["eligible"])
        self.assertEqual(bound(data).status, audit.PASS)

    def test_no_selected_candidate_abstains_without_claiming_rejection(self):
        data = fixture()
        data["evidence_packet"]["candidate_results"][0]["obligation_results"][0][
            "outcome"
        ] = OUTCOME_FAILED
        reseal_record(data)
        status = bound(data)
        self.assertEqual(status.status, audit.PASS, status.issues)
        self.assertEqual(status.selection_case, DECISION_ABSTAINED)
        self.assertFalse(status.selected_lean_condition_checked)

    def test_high_threshold_records_abstention_not_failure(self):
        data = fixture()
        data["selection_policy"]["minimum_evidence_score"] = 100
        reseal_policy(data)
        status = bound(data)
        self.assertEqual(status.status, audit.PASS, status.issues)
        self.assertEqual(status.selection_case, DECISION_ABSTAINED)

    def test_original_decision_and_receipt_not_mutated(self):
        data = fixture()
        native = run(data)
        original = _fingerprint([data, native.decision, native.receipt])
        status = audit.audit_native_codeai_selection(
            data, native.decision, native.receipt
        )
        self.assertEqual(status.status, audit.PASS)
        self.assertEqual(original, _fingerprint(
            [data, native.decision, native.receipt]))
        self.assertFalse(status.original_source_modified)

    def test_no_source_or_original_receipt_is_no_data(self):
        data = fixture()
        native = run(data)
        self.assertEqual(audit.audit_native_codeai_selection(
            None, native.decision, native.receipt).status, audit.NO_DATA)
        self.assertEqual(audit.audit_native_codeai_selection(
            data, native.decision, None).status, audit.NO_DATA)

    def test_modified_recorded_decision_without_new_seal_is_blocked(self):
        data = fixture()
        native = run(data)
        changed = deepcopy(native.decision)
        changed["selected_candidate_id"] = "forged"
        self.assertEqual(audit.audit_native_codeai_selection(
            data, changed, native.receipt).status, audit.BLOCKED)

    def test_modified_recorded_receipt_does_not_infer_git_authority(self):
        data = fixture()
        native = run(data)
        changed = deepcopy(native.receipt)
        changed["git_authority_granted"] = True
        self.assertEqual(audit.audit_native_codeai_selection(
            data, native.decision, changed).status, audit.BLOCKED)

    def test_unsealed_evidence_modification_is_blocked(self):
        data = fixture()
        data["evidence_packet"]["candidate_results"][0]["obligation_results"][0][
            "outcome"
        ] = OUTCOME_FAILED
        # Do not reseal record, packet, request and policy: authentic hash
        # correspondence cannot be reconstructed by silent normalization.
        original = run(fixture())
        self.assertEqual(audit.audit_native_codeai_selection(
            data, original.decision, original.receipt).status, audit.BLOCKED)

    def test_selected_lean_obligation_cannot_grant_authority(self):
        result = bound(fixture())
        self.assertEqual(result.status, audit.PASS)
        for field in (
            "source_issuer_authenticated",
            "original_independent_runner_attested_by_model",
            "formal_lean_python_refinement_proved",
            "lean_proof_term_constructed",
            "truth_authority_granted",
            "execution_authority_granted",
            "repair_authority_granted",
            "git_authority_granted",
        ):
            with self.subTest(field=field):
                self.assertFalse(getattr(result, field))

    def test_bad_mapping_type_or_unknown_input_is_blocked(self):
        data = fixture()
        native = run(data)
        self.assertEqual(audit.audit_native_codeai_selection(
            [data], native.decision, native.receipt).status, audit.BLOCKED)
        changed = deepcopy(data)
        changed["sidecar"] = {"authority": "unverified"}
        self.assertEqual(audit.audit_native_codeai_selection(
            changed, native.decision, native.receipt).status, audit.BLOCKED)


if __name__ == "__main__":
    unittest.main()
