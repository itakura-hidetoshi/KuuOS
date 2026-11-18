"""v0.22 exact native weight-tolerance and rational normalization tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime import kuuos_lean_python_wa_normalization_v0_22 as bridge
from runtime import kuuos_lean_python_wa_weighted_sum_certificate_v0_21 as prior
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


def q(value):
    return Fraction(*value)


class WaNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v022-native-wa-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.native_result = native.build_belief_receipt_native_fixture(cls.root)
        cls.final_wa = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.belief = BeliefGerbeStore(cls.root / "belief").recover(require_snapshot_match=True)
        cls.genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.events = [json.loads(row)["event"] for row in
                      (cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]

    def predecessor_certificate(self):
        return prior.audit_wa_weighted_state(self.final_wa)["certificates"][0]

    def test_actual_weight_tolerance_is_not_silently_exact_one(self):
        weight = bridge.certify_native_weight_tolerance(self.final_wa["weights"])
        self.assertEqual(len(weight["axes"]), 7)
        self.assertEqual(len(weight["native_floats_rational"]), 7)
        self.assertEqual(sum(map(q, weight["normalized_rational_weights"]),
                             Fraction(0)), 1)
        self.assertTrue(weight["sum_of_normalized_rational_weights_is_one"])
        self.assertLessEqual(q(weight["observed_exact_weight_defect"]),
                             q(weight["exact_weight_defect_upper_bound"]))
        self.assertEqual(q(weight["exact_weight_defect_upper_bound"]),
                         q(weight["native_float_tolerance"]) +
                         q(weight["observed_builtin_sum_error"]))
        self.assertFalse(weight["native_sum_semantics_formally_proved"])

    def test_actual_original_native_Wa_records_have_rational_normalization_witnesses(self):
        audit = bridge.audit_wa_normalization_state(self.final_wa)
        self.assertEqual(audit["version"], bridge.VERSION)
        self.assertEqual(audit["state_digest"], _fingerprint(self.final_wa))
        self.assertTrue(audit["all_input_observations_certified"])
        self.assertEqual(len(audit["certificates"]), len(self.final_wa["wa_records"]))
        for row in audit["certificates"]:
            self.assertEqual(len(row["endpoint_certificates"]), 2)
            self.assertTrue(row["exact_rational_normalized_interval_only"])
            for endpoint in row["endpoint_certificates"]:
                normalized = q(endpoint["exact_normalized_weighted"])
                self.assertGreaterEqual(normalized, 0)
                self.assertLessEqual(normalized, 1)
                self.assertLessEqual(
                    q(endpoint["actual_native_vs_normalized_error"]),
                    q(endpoint["combined_error_bound"]))
                self.assertEqual(
                    q(endpoint["combined_error_bound"]),
                    q(endpoint["input_weighted_error_budget"]) +
                    q(endpoint["weight_tolerance_budget"]) +
                    q(endpoint["observed_builtin_weight_sum_error"]))
        self.assertFalse(audit["python_lean_full_refinement_proved"])
        self.assertFalse(audit["external_issuer_authenticated"])
        self.assertFalse(audit["authority_granted"])

    def test_near_one_native_tolerance_is_distinct_from_exact_normalization(self):
        axes = bridge.POSITIVE_DIMENSIONS
        vals = (0.25, 0.25, 0.25, 0.25, 1e-10, 0.0, 0.0)
        weights = dict(zip(axes, vals))
        cert = bridge.certify_native_weight_tolerance(weights)
        self.assertGreater(q(cert["exact_rational_weight_total"]), 1)
        self.assertGreater(q(cert["observed_exact_weight_defect"]), 0)
        self.assertLessEqual(q(cert["observed_exact_weight_defect"]),
                             q(cert["exact_weight_defect_upper_bound"]))
        self.assertEqual(sum(map(q, cert["normalized_rational_weights"]), Fraction(0)), 1)
        self.assertNotEqual(cert["exact_rational_weight_total"], [1, 1])

    def test_original_native_sum_is_not_proclaimed_real_or_ieee_theorem(self):
        audit = bridge.audit_wa_normalization_state(self.final_wa)
        self.assertFalse(audit["ieee754_global_semantics_proved"])
        self.assertFalse(audit["original_weights_normalized_or_modified"])
        self.assertFalse(audit["weight_tolerance"]["native_sum_semantics_formally_proved"])

    def test_cannot_forge_precomputed_weight_certificate(self):
        w = deepcopy(self.final_wa["weights"])
        cert = bridge.certify_native_weight_tolerance(w)
        cert["exact_rational_weight_total"] = [999, 1]
        with self.assertRaisesRegex(bridge.WaNormalizationError,
                                    "reconstructed_evidence_mismatch"):
            bridge.certify_normalized_profile(
                self.final_wa["profiles"][0], w, self.predecessor_certificate(), cert)

    def test_cannot_forge_weighted_certificate_or_bound(self):
        w = self.final_wa["weights"]
        row = self.predecessor_certificate()
        row["endpoints"][0]["exact_weighted"] = [999, 1]
        with self.assertRaisesRegex(bridge.WaNormalizationError, "source_weighted_mismatch"):
            bridge.certify_normalized_profile(self.final_wa["profiles"][0], w, row)
        row = self.predecessor_certificate()
        row["endpoints"][0]["composed_upper_bound"] = [0, 1]
        if q(row["endpoints"][0]["native_weighted"]) != q(row["endpoints"][0]["exact_weighted"]):
            with self.assertRaisesRegex(bridge.WaNormalizationError, "v021_weighted_bound_failed"):
                bridge.certify_normalized_profile(self.final_wa["profiles"][0], w, row)

    def test_negative_out_of_range_nonfinite_bool_and_wrong_axis_rejected(self):
        original = self.final_wa["weights"]
        for bad in (float("inf"), float("nan"), True, -0.1, 1.1, "0.1", None):
            with self.subTest(value=repr(bad)):
                weights = deepcopy(original)
                weights[bridge.POSITIVE_DIMENSIONS[0]] = bad
                with self.assertRaises(bridge.WaNormalizationError):
                    bridge.certify_native_weight_tolerance(weights)
        weights = deepcopy(original)
        weights["invented_axis"] = 0.0
        with self.assertRaisesRegex(bridge.WaNormalizationError, "seven_axis_keys_required"):
            bridge.certify_native_weight_tolerance(weights)

    def test_perturbation_beyond_native_tolerance_rejected(self):
        axes = bridge.POSITIVE_DIMENSIONS
        weights = dict(zip(axes, (0.25, 0.25, 0.25, 0.25, 1e-7, 0.0, 0.0)))
        with self.assertRaisesRegex(bridge.WaNormalizationError,
                                    "original_native_tolerance_failed"):
            bridge.certify_native_weight_tolerance(weights)

    def test_tampered_original_native_score_still_blocked(self):
        modified = deepcopy(self.final_wa)
        lower = modified["wa_records"][0]["weighted_interval"]["lower"]
        modified["wa_records"][0]["weighted_interval"]["lower"] = math.nextafter(lower, math.inf)
        with self.assertRaises(bridge.WaNormalizationError):
            bridge.audit_wa_normalization_state(modified)

    def test_missing_inputs_are_no_data(self):
        with self.assertRaises(bridge.WaNormalizationError) as context:
            bridge.audit_wa_normalization_state(None)
        self.assertEqual(context.exception.status, "NO_DATA")
        with self.assertRaises(bridge.WaNormalizationError):
            bridge.certify_native_weight_tolerance(None)

    def test_preevaluation_preserves_empty_certificates_without_promotion(self):
        result = bridge.audit_wa_normalization_state(self.genesis)
        self.assertEqual(result["certificates"], [])
        self.assertIsNone(result["weight_tolerance"])
        self.assertFalse(result["all_input_observations_certified"])

    def test_read_only_native_event_ledger_matches_v021_exactly(self):
        state = deepcopy(self.genesis)
        for event in self.events:
            expected = prior.checked_apply_wa_weighted_event(
                state, event, self.plural, self.decision, self.belief)
            actual = bridge.checked_apply_wa_normalization_event(
                state, event, self.plural, self.decision, self.belief)
            with self.subTest(phase=event["target_phase"]):
                self.assertEqual(actual, expected)
                self.assertEqual(actual["status"], "APPLIED")
            state = actual["state"]
        self.assertEqual(state, self.final_wa)

    def test_native_weighted_observation_remains_the_original_stored_number(self):
        result = bridge.audit_wa_normalization_state(self.final_wa)
        for cert, record in zip(result["certificates"], self.final_wa["wa_records"]):
            for endpoint in cert["endpoint_certificates"]:
                bound = endpoint["endpoint"]
                self.assertEqual(
                    q(endpoint["native_observed_weighted"]),
                    Fraction(*record["weighted_interval"][bound].as_integer_ratio()))

    def test_weight_and_score_checks_leave_every_input_unchanged(self):
        original = _fingerprint(self.final_wa)
        bridge.audit_wa_normalization_state(self.final_wa)
        self.assertEqual(original, _fingerprint(self.final_wa))

    def test_unknown_phase_cannot_skip_certification(self):
        mutated = deepcopy(self.final_wa)
        mutated["current_phase"] = "invalid_phase"
        with self.assertRaises(bridge.WaNormalizationError):
            bridge.audit_wa_normalization_state(mutated)


if __name__ == "__main__":
    unittest.main()
