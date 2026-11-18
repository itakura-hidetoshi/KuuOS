"""v0.19 exact rational Wa score certificate on genuine v0.18 native data.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_wa_rational_shadow_v0_19 as bridge
from runtime import kuuos_lean_python_belief_receipt_guard_v0_18 as prior
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class WaRationalShadowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v019-real-native-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.native_run = native.build_belief_receipt_native_fixture(cls.root)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.belief = BeliefGerbeStore(cls.root / "belief").recover(require_snapshot_match=True)
        cls.final_wa = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)
        cls.wa_genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.events = [json.loads(row)["event"] for row in
                      (cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]

    def test_real_native_scores_have_exact_rational_error_certificates(self):
        audit = bridge.audit_wa_rational_state(self.final_wa)
        self.assertEqual(audit["version"], bridge.VERSION)
        self.assertEqual(audit["state_digest"], _fingerprint(self.final_wa))
        self.assertGreater(len(audit["certificates"]), 0)
        self.assertEqual(audit["error_budget"], [1, 2**40])
        self.assertFalse(audit["lean_python_full_refinement_proved"])
        for certificate in audit["certificates"]:
            self.assertEqual(len(certificate["exact_error_by_field"]), 11)
            largest = Fraction(*certificate["maximum_absolute_error"])
            self.assertGreaterEqual(largest, 0)
            self.assertLessEqual(largest, bridge.ERROR_BUDGET)
            for pair in certificate["exact_error_by_field"].values():
                self.assertGreaterEqual(Fraction(*pair), 0)
                self.assertLessEqual(Fraction(*pair), bridge.ERROR_BUDGET)

    def test_entire_real_wa_ledger_has_exact_original_adapter_results(self):
        state = deepcopy(self.wa_genesis)
        for event in self.events:
            expected = prior.checked_apply_wa_belief_receipt_event(
                state, event, self.plural, self.decision, self.belief)
            observed = bridge.checked_apply_wa_rational_event(
                state, event, self.plural, self.decision, self.belief)
            with self.subTest(phase=event["target_phase"]):
                self.assertEqual(observed, expected)
                self.assertEqual(observed["status"], "APPLIED")
            state = observed["state"]
        self.assertEqual(state, self.final_wa)

    def test_existing_native_child_evidence_and_authority_preserved(self):
        self.assertEqual(self.native_run.status, native.SUCCESS)
        self.assertFalse(self.native_run.external_issuer_authenticated)
        self.assertFalse(self.native_run.lean_python_refinement_proved)
        self.assertFalse(self.native_run.host_rollback_guaranteed)

    def test_python_binary64_addition_rational_obstruction_matches_lean_literals(self):
        a, b, value = (Fraction(*v.as_integer_ratio()) for v in
                       (0.1, 0.2, 0.1 + 0.2))
        self.assertEqual(a, Fraction(3602879701896397, 36028797018963968))
        self.assertEqual(b, Fraction(3602879701896397, 18014398509481984))
        self.assertEqual(value, Fraction(1351079888211149, 4503599627370496))
        self.assertEqual(value - (a + b), Fraction(1, 36028797018963968))
        self.assertNotEqual(value, a + b)

    def test_exact_input_reference_and_floating_result_differ_in_general(self):
        profile = self.final_wa["profiles"][0]
        shadow = bridge.rational_ideal_record(
            profile, self.final_wa["weights"],
            self.final_wa["thresholds"]["bottleneck_weight"])
        self.assertEqual(len(shadow), 11)
        for field in shadow:
            self.assertIsInstance(shadow[field], Fraction)

    def test_resealed_small_native_score_change_beyond_budget_is_blocked(self):
        state = deepcopy(self.final_wa)
        state["wa_records"][0]["wa_interval"]["lower"] += 1e-8
        with self.assertRaisesRegex(bridge.WaRationalShadowError, "exceeds_budget"):
            bridge.audit_wa_rational_state(state)

    def test_exact_width_certificate_is_distinct_from_native_subtraction(self):
        certificate = bridge.audit_wa_rational_state(self.final_wa)["certificates"][0]
        self.assertIn("wa_interval.width", certificate["exact_error_by_field"])
        self.assertLessEqual(
            Fraction(*certificate["exact_error_by_field"]["wa_interval.width"]),
            bridge.ERROR_BUDGET,
        )

    def test_pre_evaluate_phase_has_no_records_and_is_not_promoted_to_proof(self):
        observation = bridge.audit_wa_rational_state(self.wa_genesis)
        self.assertEqual(observation["certificates"], [])
        self.assertFalse(observation["ieee754_global_rounding_proved"])

    def test_missing_wa_state_is_no_data(self):
        with self.assertRaises(bridge.WaRationalShadowError) as e:
            bridge.audit_wa_rational_state(None)
        self.assertEqual(e.exception.status, "NO_DATA")

    def test_invalid_num_types_nonfinite_and_nonbuiltins_are_blocked(self):
        for value in (True, "0.1", float("nan"), float("inf"), (), None):
            with self.subTest(value=repr(value)):
                with self.assertRaises(bridge.WaRationalShadowError):
                    bridge._q(value, "sample")

    def test_missing_reference_field_retains_no_data(self):
        state = deepcopy(self.final_wa)
        del state["thresholds"]
        with self.assertRaises(bridge.WaRationalShadowError) as e:
            bridge.audit_wa_rational_state(state)
        self.assertEqual(e.exception.status, "NO_DATA")

    def test_unknown_phase_or_bad_option_reference_is_blocked(self):
        state = deepcopy(self.final_wa)
        state["current_phase"] = "not-a-phase"
        with self.assertRaises(bridge.WaRationalShadowError):
            bridge.audit_wa_rational_state(state)
        state = deepcopy(self.final_wa)
        state["wa_records"][0]["option_id"] = "unauthorized-option"
        with self.assertRaises(bridge.WaRationalShadowError):
            bridge.audit_wa_rational_state(state)

    def test_malformed_earlier_native_errors_keep_no_data(self):
        event = self.events[0]
        with patch.object(prior, "checked_apply_wa_belief_receipt_event",
                          side_effect=prior.BeliefReceiptBoundaryError("NO_DATA", ("missing",))) as patched:
            with self.assertRaises(bridge.WaRationalShadowError) as e:
                bridge.checked_apply_wa_rational_event(
                    self.wa_genesis, event, self.plural, self.decision, self.belief)
        patched.assert_called_once()
        self.assertEqual(e.exception.status, "NO_DATA")

    def test_pure_adapter_and_certificate_leave_all_original_inputs_unchanged(self):
        original = _fingerprint([self.wa_genesis, self.events[0], self.plural,
                                 self.decision, self.belief, self.final_wa])
        bridge.checked_apply_wa_rational_event(
            self.wa_genesis, self.events[0], self.plural, self.decision, self.belief)
        bridge.audit_wa_rational_state(self.final_wa)
        self.assertEqual(original, _fingerprint([self.wa_genesis, self.events[0],
                        self.plural, self.decision, self.belief, self.final_wa]))


if __name__ == "__main__":
    unittest.main()
