"""Conditional Wa score sensitivity to finite source extrema v0.26 tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime import kuuos_lean_python_wa_extrema_stability_v0_26 as bridge
from runtime import kuuos_lean_python_wa_finite_extrema_v0_25 as previous
from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as v23
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


def q(pair):
    return Fraction(*pair)


def params():
    # Original ideal: F_1/2(1/2, 1/4, 1/4) = 9/32.
    return dict(beta=[1, 2], observed_weighted=[1, 2],
                normalized_weighted=[1, 2],
                observed_weakest=[1, 4], reference_weakest=[1, 2],
                observed_alert=[1, 4], reference_alert=[1, 2],
                observed_score=[9, 32], wa_error_budget=[0, 1],
                normalized_weight_budget=[0, 1],
                weakest_error_budget=[1, 4], alert_error_budget=[1, 4])


class WaExtremaStabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v026-wa-extrema-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.native_fixture = native.build_belief_receipt_native_fixture(cls.root)
        cls.state = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)

    def first(self):
        return bridge.certify_original_wa_extrema_stability_trace(
            self.state["profiles"][0], self.state["weights"],
            self.state["thresholds"]["bottleneck_weight"])

    def test_pure_rational_two_extrema_error_gluing(self):
        cert = bridge.certify_exact_extrema_score_reference(**params())
        self.assertTrue(cert["conditional_rational_inequality_checked"])
        self.assertLessEqual(q(cert["observed_reference_score_error"]),
                             q(cert["conditional_composed_upper_bound"]))
        self.assertEqual(q(cert["conditional_composed_upper_bound"]), Fraction(1, 2))
        self.assertTrue(cert["counterfactual_reference_only"])

    def test_weakest_only_changes_by_at_most_observed_distance(self):
        args = params()
        args["reference_alert"] = args["observed_alert"]
        args["alert_error_budget"] = [0, 1]
        cert = bridge.certify_exact_extrema_score_reference(**args)
        self.assertLessEqual(q(cert["weakest_ideal_shift"]),
                             q(cert["measured_weakest_error"]))
        self.assertEqual(q(cert["alert_ideal_shift"]), Fraction(0))

    def test_alert_only_changes_by_at_most_observed_distance(self):
        args = params()
        args["reference_weakest"] = args["observed_weakest"]
        args["weakest_error_budget"] = [0, 1]
        cert = bridge.certify_exact_extrema_score_reference(**args)
        self.assertLessEqual(q(cert["alert_ideal_shift"]),
                             q(cert["measured_alert_error"]))
        self.assertEqual(q(cert["weakest_ideal_shift"]), Fraction(0))

    def test_reference_identical_to_source_has_zero_extra_error(self):
        args = params()
        args["reference_weakest"] = args["observed_weakest"]
        args["reference_alert"] = args["observed_alert"]
        args["weakest_error_budget"] = [0, 1]
        args["alert_error_budget"] = [0, 1]
        cert = bridge.certify_exact_extrema_score_reference(**args)
        self.assertEqual(q(cert["observed_reference_score_error"]), Fraction(0))
        self.assertEqual(q(cert["conditional_composed_upper_bound"]), Fraction(0))

    def test_weighted_reference_difference_requires_budget(self):
        args = params()
        args["observed_weighted"] = [3, 4]
        args["observed_score"] = [3, 8]
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.certify_exact_extrema_score_reference(**args)
        args["normalized_weight_budget"] = [1, 4]
        cert = bridge.certify_exact_extrema_score_reference(**args)
        self.assertEqual(q(cert["measured_weight_error"]), Fraction(1, 4))

    def test_forged_original_native_score_is_blocked(self):
        args = params()
        args["observed_score"] = [1, 2]
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.certify_exact_extrema_score_reference(**args)

    def test_undersized_weakest_budget_fails_closed(self):
        args = params()
        args["weakest_error_budget"] = [1, 8]
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.certify_exact_extrema_score_reference(**args)

    def test_undersized_alert_budget_fails_closed(self):
        args = params()
        args["alert_error_budget"] = [1, 8]
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.certify_exact_extrema_score_reference(**args)

    def test_negative_budget_and_wrong_types_are_blocked(self):
        for val in ([-1, 10], [True, 1], [1, 0], [1], "0.1", None):
            args = params()
            args["wa_error_budget"] = val
            with self.subTest(value=val):
                with self.assertRaises(bridge.WaExtremaStabilityError):
                    bridge.certify_exact_extrema_score_reference(**args)

    def test_beta_normalized_and_reference_out_of_unit_are_blocked(self):
        for field in ("beta", "normalized_weighted", "reference_weakest",
                      "observed_alert", "reference_alert"):
            args = params()
            args[field] = [5, 4]
            with self.subTest(field=field):
                with self.assertRaises(bridge.WaExtremaStabilityError):
                    bridge.certify_exact_extrema_score_reference(**args)

    def test_actual_native_profile_bound_uses_source_endpoints(self):
        cert = self.first()
        self.assertEqual(cert["version"], bridge.VERSION)
        self.assertEqual(len(cert["endpoints"]), 2)
        self.assertEqual(cert["endpoints"][0]["endpoint"], "lower")
        self.assertEqual(cert["endpoints"][0]["reference_endpoint"], "upper")
        self.assertEqual(cert["endpoints"][1]["endpoint"], "upper")
        self.assertEqual(cert["endpoints"][1]["reference_endpoint"], "lower")
        self.assertFalse(cert["host_authority_granted"])

    def test_original_observed_weakest_and_alert_reference_source_identity(self):
        p, w = self.state["profiles"][0], self.state["weights"]
        beta = self.state["thresholds"]["bottleneck_weight"]
        old = previous.certify_original_wa_extrema_trace(p, w, beta)
        now = self.first()
        for i, cur in enumerate(now["endpoints"]):
            original = old["endpoint_certificates"][i]
            alternate = old["endpoint_certificates"][1 - i]
            self.assertEqual(cur["observed_weakest_positive"],
                             original["observed_weakest_positive"])
            self.assertEqual(cur["reference_weakest_positive"],
                             alternate["observed_weakest_positive"])
            self.assertEqual(cur["observed_strongest_alert"],
                             original["observed_strongest_alert"])
            self.assertEqual(cur["reference_strongest_alert"],
                             alternate["observed_strongest_alert"])
            self.assertTrue(cur["reference_comes_from_same_source_option"])

    def test_original_v023_raw_score_and_normalized_ideal_preserved(self):
        p, w = self.state["profiles"][0], self.state["weights"]
        beta = self.state["thresholds"]["bottleneck_weight"]
        old = v23.certify_normalized_final_trace(p, w, beta)
        now = self.first()
        for original, selected in zip(old["endpoints"], now["endpoints"]):
            c = selected["comparison"]
            self.assertEqual(c["original_raw_ideal"],
                             original["original_raw_ideal_score"])
            self.assertEqual(c["normalized_original_extrema_ideal"],
                             original["normalized_ideal_score"])
            self.assertEqual(c["observed_native_score"],
                             original["observed_native_wa_score"])

    def test_actual_reference_score_budget_is_explicit_addition(self):
        for entry in self.first()["endpoints"]:
            c = entry["comparison"]
            bound = (q(c["measured_wa_error"]) +
                     q(c["measured_weight_error"]) +
                     q(c["measured_weakest_error"]) +
                     q(c["measured_alert_error"]))
            self.assertLessEqual(q(c["observed_reference_score_error"]),
                                 q(c["conditional_composed_upper_bound"]))
            self.assertLessEqual(bound, q(c["conditional_composed_upper_bound"]))
            self.assertTrue(c["conditional_rational_inequality_checked"])

    def test_original_native_state_and_saved_wa_scores_unchanged(self):
        state = deepcopy(self.state)
        old_digest = _fingerprint(state)
        new = bridge.audit_wa_extrema_stability_state(self.state)
        self.assertEqual(state, self.state)
        self.assertEqual(new["state_digest"], old_digest)
        self.assertFalse(new["original_state_modified"])

    def test_all_source_option_ids_preserved_in_full_audit(self):
        old = previous.audit_wa_finite_extrema_state(self.state)
        new = bridge.audit_wa_extrema_stability_state(self.state)
        self.assertTrue(new["all_conditional_extrema_reference_checks_passed"])
        self.assertEqual([c["option_id"] for c in new["certificates"]],
                         [c["option_id"] for c in old["certificates"]])

    def test_source_profile_tampering_fails_before_score_comparison(self):
        bad = deepcopy(self.state)
        bad["profiles"][0]["option_id"] = "forged"
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.audit_wa_extrema_stability_state(bad)

    def test_missing_weight_and_boolean_beta_block(self):
        profile = self.state["profiles"][0]
        weights = deepcopy(self.state["weights"])
        beta = self.state["thresholds"]["bottleneck_weight"]
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.certify_original_wa_extrema_stability_trace(
                profile, weights, True)
        weights.pop(next(iter(weights)))
        with self.assertRaises(bridge.WaExtremaStabilityError):
            bridge.certify_original_wa_extrema_stability_trace(
                profile, weights, beta)

    def test_before_evaluation_does_not_claim_reference_score_proof(self):
        early = deepcopy(self.state)
        early["current_phase"] = "bind"
        try:
            audit = bridge.audit_wa_extrema_stability_state(early)
        except bridge.WaExtremaStabilityError:
            return
        self.assertFalse(audit["all_conditional_extrema_reference_checks_passed"])

    def test_local_success_cannot_claim_generic_float_or_host_authority(self):
        result = bridge.audit_wa_extrema_stability_state(self.state)
        self.assertFalse(result["global_python_lean_refinement_proved"])
        self.assertFalse(result["python_min_max_sum_semantics_proved"])
        self.assertFalse(result["external_issuer_authenticated"])
        self.assertFalse(result["host_authority_granted"])
        self.assertTrue(all(
            x["comparison"]["counterfactual_reference_only"]
            for item in result["certificates"] for x in item["endpoints"]))


if __name__ == "__main__":
    unittest.main()
