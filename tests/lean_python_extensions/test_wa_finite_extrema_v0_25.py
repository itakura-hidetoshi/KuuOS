"""Original Wa finite positive min / alert max observation tests v0.25.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime import kuuos_lean_python_wa_finite_extrema_v0_25 as bridge
from runtime import kuuos_lean_python_wa_upper_clip_v0_24 as prior
from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as v23
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


def q(value):
    return Fraction(*value)


class WaFiniteExtremaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v025-wa-extrema-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.original_fixture = native.build_belief_receipt_native_fixture(cls.root)
        cls.state = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)

    def first(self):
        return bridge.certify_original_wa_extrema_trace(
            self.state["profiles"][0], self.state["weights"],
            self.state["thresholds"]["bottleneck_weight"])

    def test_pure_finite_rational_extrema(self):
        cert = bridge.certify_finite_extrema(
            [[1, 4], [3, 4], [1, 2]], [1, 4], [3, 4])
        self.assertEqual(cert["count"], 3)
        self.assertEqual(q(cert["observed_min"]), Fraction(1, 4))
        self.assertEqual(q(cert["observed_max"]), Fraction(3, 4))
        self.assertTrue(cert["rational_finite_extrema_checked"])
        self.assertFalse(cert["python_min_max_semantics_proved"])

    def test_tied_minimum_and_maximum_have_explicit_member_indices(self):
        cert = bridge.certify_finite_extrema(
            [[1, 4], [1, 4], [3, 4], [3, 4]],
            [1, 4], [3, 4])
        self.assertEqual(cert["min_member_indices"], [0, 1])
        self.assertEqual(cert["max_member_indices"], [2, 3])

    def test_singleton_finite_min_and_max_are_same(self):
        cert = bridge.certify_finite_extrema([[2, 3]], [2, 3], [2, 3])
        self.assertEqual(cert["min_member_indices"], [0])
        self.assertEqual(cert["max_member_indices"], [0])

    def test_exact_rational_extrema_are_order_invariant(self):
        samples = [[2, 3], [1, 3], [3, 4], [1, 2]]
        left = bridge.certify_finite_extrema(samples, [1, 3], [3, 4])
        right = bridge.certify_finite_extrema(list(reversed(samples)), [1, 3], [3, 4])
        self.assertEqual(left["observed_min"], right["observed_min"])
        self.assertEqual(left["observed_max"], right["observed_max"])

    def test_empty_and_invalid_samples_fail_closed(self):
        for bad in (None, [], (), "[]", [None], [[1]], [[1, 0]],
                    [[True, 1]], [[1, 2, 3]]):
            with self.subTest(value=bad):
                with self.assertRaises(bridge.WaFiniteExtremaError):
                    bridge.certify_finite_extrema(bad, [0, 1], [1, 1])

    def test_out_of_unit_samples_fail_closed(self):
        for sample in ([-1, 3], [4, 3]):
            with self.subTest(value=sample):
                with self.assertRaises(bridge.WaFiniteExtremaError):
                    bridge.certify_finite_extrema([sample], sample, sample)

    def test_wrong_observed_min_is_blocked(self):
        with self.assertRaises(bridge.WaFiniteExtremaError):
            bridge.certify_finite_extrema([[1, 4], [3, 4]], [1, 2], [3, 4])

    def test_wrong_observed_max_is_blocked(self):
        with self.assertRaises(bridge.WaFiniteExtremaError):
            bridge.certify_finite_extrema([[1, 4], [3, 4]], [1, 4], [1, 2])

    def test_observed_native_positive_and_alert_axes_are_bound(self):
        cert = self.first()
        self.assertEqual(cert["version"], bridge.VERSION)
        self.assertEqual(len(cert["endpoint_certificates"]), 2)
        for entry in cert["endpoint_certificates"]:
            self.assertEqual(entry["positive_axis_names"], list(v20.native._POSITIVE))
            self.assertEqual(entry["alert_axis_names"], list(v20.native._ALERT))
            self.assertEqual(len(entry["positive_sample_rationals"]), 7)
            self.assertTrue(entry["original_extremum_identities_checked"])
            self.assertTrue(entry["observed_min_max_gluing_checked"])

    def test_original_lower_upper_cross_alert_selection_preserved(self):
        cert = self.first()
        for endpoint, opposite, entry in zip(
                ("lower", "upper"), ("upper", "lower"),
                cert["endpoint_certificates"]):
            self.assertEqual(entry["endpoint"], endpoint)
            self.assertEqual(entry["alert_source_endpoint"], opposite)
            self.assertEqual(q(entry["observed_weakest_positive"]),
                             min(q(x) for x in entry["positive_sample_rationals"]))
            self.assertEqual(q(entry["observed_strongest_alert"]),
                             max(q(x) for x in entry["alert_sample_rationals"]))

    def test_finite_selected_extrema_keep_original_wa_ideal(self):
        p = self.state["profiles"][0]
        w = self.state["weights"]
        beta = self.state["thresholds"]["bottleneck_weight"]
        old = v23.certify_normalized_final_trace(p, w, beta)
        new = self.first()
        b = Fraction(*beta.as_integer_ratio())
        for current, baseline in zip(new["endpoint_certificates"], old["endpoints"]):
            self.assertEqual(current["normalized_ideal_score"],
                             baseline["normalized_ideal_score"])
            self.assertEqual(q(current["normalized_ideal_score"]),
                             v23._rational_ideal(
                                b, q(baseline["exact_normalized_weighted"]),
                                q(current["observed_weakest_positive"]),
                                q(current["observed_strongest_alert"])))

    def test_new_upper_identity_preserves_previous_clipping_result(self):
        p = self.state["profiles"][0]
        w = self.state["weights"]
        beta = self.state["thresholds"]["bottleneck_weight"]
        old = prior.certify_original_upper_clip_trace(p, w, beta)
        now = self.first()["endpoint_certificates"][1]
        self.assertEqual(now["normalized_ideal_score"],
                         old["upper"]["normalized_ideal"])

    def test_full_state_audit_preserves_order_and_source_digest(self):
        old = prior.audit_wa_upper_clip_state(self.state)
        new = bridge.audit_wa_finite_extrema_state(self.state)
        self.assertTrue(new["all_original_finite_extrema_checked"])
        self.assertEqual(new["state_digest"], _fingerprint(self.state))
        self.assertEqual([z["option_id"] for z in new["certificates"]],
                         [z["option_id"] for z in old["certificates"]])

    def test_original_native_store_and_scores_not_modified(self):
        prior_state = deepcopy(self.state)
        audit = bridge.audit_wa_finite_extrema_state(self.state)
        self.assertEqual(self.state, prior_state)
        self.assertFalse(audit["original_state_modified"])
        self.assertTrue(all(not c["original_wa_source_modified"]
                            for c in audit["certificates"]))

    def test_source_tampering_cannot_gain_certificate(self):
        changed = deepcopy(self.state)
        changed["profiles"][0]["option_id"] = "forged"
        with self.assertRaises(bridge.WaFiniteExtremaError):
            bridge.audit_wa_finite_extrema_state(changed)

    def test_missing_weight_and_invalid_beta_block(self):
        p = self.state["profiles"][0]
        w = deepcopy(self.state["weights"])
        beta = self.state["thresholds"]["bottleneck_weight"]
        with self.assertRaises(bridge.WaFiniteExtremaError):
            bridge.certify_original_wa_extrema_trace(p, w, True)
        w.pop(next(iter(w)))
        with self.assertRaises(bridge.WaFiniteExtremaError):
            bridge.certify_original_wa_extrema_trace(p, w, beta)

    def test_before_evaluation_cannot_claim_global_extrema(self):
        changed = deepcopy(self.state)
        changed["current_phase"] = "bind"
        try:
            audit = bridge.audit_wa_finite_extrema_state(changed)
        except bridge.WaFiniteExtremaError:
            return
        self.assertFalse(audit["all_original_finite_extrema_checked"])

    def test_local_success_cannot_grant_python_or_issuer_authority(self):
        audit = bridge.audit_wa_finite_extrema_state(self.state)
        self.assertFalse(audit["global_ieee754_semantics_proved"])
        self.assertFalse(audit["python_min_max_semantics_proved"])
        self.assertFalse(audit["external_issuer_authenticated"])
        self.assertFalse(audit["host_authority_granted"])


if __name__ == "__main__":
    unittest.main()
