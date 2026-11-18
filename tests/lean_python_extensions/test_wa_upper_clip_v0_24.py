"""v0.24 native original upper clipping and rational Lean-bound regressions.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime import kuuos_lean_python_wa_upper_clip_v0_24 as bridge
from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as prior
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


def q(value):
    return Fraction(*value)


class WaUpperClipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v024-native-upper-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.fixture = native.build_belief_receipt_native_fixture(cls.root)
        cls.state = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)

    def first(self):
        return bridge.certify_original_upper_clip_trace(
            self.state["profiles"][0], self.state["weights"],
            self.state["thresholds"]["bottleneck_weight"])

    def test_mathematical_clamp_does_not_change_already_below_one(self):
        witness = bridge.certify_exact_upper_clip([3, 4], [3, 4], [2, 3])
        self.assertEqual(q(witness["unclipped_upper"]), Fraction(3, 4))
        self.assertEqual(q(witness["clipped_upper"]), Fraction(3, 4))
        self.assertTrue(witness["clipping_nonexpansive_checked"])

    def test_mathematical_clamp_reduces_overshoot_error(self):
        witness = bridge.certify_exact_upper_clip([11, 10], [1, 1], [9, 10])
        self.assertEqual(q(witness["raw_ideal_error"]), Fraction(1, 5))
        self.assertEqual(q(witness["clipped_ideal_error"]), Fraction(1, 10))
        self.assertFalse(witness["python_builtin_min_semantics_proved"])

    def test_bad_upper_clip_identity_fails_closed(self):
        with self.assertRaises(bridge.WaUpperClipError):
            bridge.certify_exact_upper_clip([11, 10], [11, 10], [9, 10])
        with self.assertRaises(bridge.WaUpperClipError):
            bridge.certify_exact_upper_clip([3, 4], [1, 1], [2, 3])

    def test_ideal_outside_unit_is_not_silently_promoted(self):
        for ideal in ([11, 10], [-1, 10]):
            with self.subTest(ideal=ideal):
                with self.assertRaises(bridge.WaUpperClipError):
                    bridge.certify_exact_upper_clip([11, 10], [1, 1], ideal)

    def test_missing_malformed_and_nonrational_inputs_block(self):
        for bad in (None, [1], [1, 0], [1, "2"], [True, 1], [1, 2, 3]):
            with self.subTest(value=bad):
                with self.assertRaises(bridge.WaUpperClipError):
                    bridge.certify_exact_upper_clip(bad, [1, 1], [1, 2])

    def test_actual_native_upper_arithmetic_certificate_is_bound(self):
        entry = self.first()
        self.assertEqual(entry["version"], bridge.VERSION)
        self.assertTrue(entry["native_raw_upper_midpoint_checked"])
        self.assertTrue(entry["original_native_upper_clipping_identity_checked"])
        self.assertTrue(entry["conditional_lean_inequality_checked"])
        self.assertFalse(entry["python_min_max_sum_semantics_proved"])
        self.assertFalse(entry["host_authority_granted"])

    def test_actual_native_upper_contraction_is_quantitatively_checked(self):
        entry = self.first()
        clip = entry["upper"]
        self.assertLessEqual(q(clip["clipped_ideal_error"]),
                             q(clip["raw_ideal_error"]))
        self.assertLessEqual(q(entry["preclip_normalized_error"]),
                             q(entry["composed_upper_bound"]))
        self.assertLessEqual(q(entry["clipped_normalized_error"]),
                             q(entry["composed_upper_bound"]))
        self.assertEqual(q(entry["composed_upper_bound"]),
                         q(entry["observed_preclip_raw_wa_error"]) +
                         q(entry["normalized_weighted_budget"]))

    def test_native_trace_raw_upper_identity_and_original_min(self):
        profile = self.state["profiles"][0]
        weights = self.state["weights"]
        beta = self.state["thresholds"]["bottleneck_weight"]
        trace = v20.trace_native_wa_score(profile, weights, beta)
        raw_steps = [s for s in trace["steps"] if s["label"] == "wa:upper"]
        self.assertEqual(len(raw_steps), 1)
        raw = q(raw_steps[0]["observed"])
        clipped = Fraction(*trace["fields"]["wa_interval.upper"].as_integer_ratio())
        self.assertEqual(clipped, min(Fraction(1), raw))
        self.assertEqual(q(self.first()["upper"]["clipped_upper"]), clipped)

    def test_previous_v023_exact_normalized_upper_is_unchanged(self):
        profile = self.state["profiles"][0]
        weights = self.state["weights"]
        beta = self.state["thresholds"]["bottleneck_weight"]
        old = prior.certify_normalized_final_trace(profile, weights, beta)
        new = self.first()
        self.assertEqual(new["option_id"], old["option_id"])
        self.assertEqual(new["upper"]["normalized_ideal"],
                         old["endpoints"][1]["normalized_ideal_score"])
        self.assertEqual(new["upper"]["clipped_upper"],
                         old["endpoints"][1]["observed_native_wa_score"])

    def test_full_wa_state_audit_contains_all_original_options(self):
        prior_result = prior.audit_wa_normalized_final_state(self.state)
        result = bridge.audit_wa_upper_clip_state(self.state)
        self.assertTrue(result["all_local_upper_clips_checked"])
        self.assertEqual(len(result["certificates"]), len(prior_result["certificates"]))
        self.assertEqual([x["option_id"] for x in result["certificates"]],
                         [x["option_id"] for x in prior_result["certificates"]])
        self.assertEqual(result["state_digest"], _fingerprint(self.state))

    def test_original_store_scores_and_state_are_never_mutated(self):
        snapshot = deepcopy(self.state)
        audit = bridge.audit_wa_upper_clip_state(self.state)
        self.assertEqual(self.state, snapshot)
        self.assertFalse(audit["original_state_modified"])
        for profile, cert in zip(self.state["wa_records"], audit["certificates"]):
            self.assertEqual(q(cert["upper"]["clipped_upper"]),
                             Fraction(*profile["wa_interval"]["upper"].as_integer_ratio()))

    def test_forged_profile_cannot_replace_valid_native_state(self):
        bad = deepcopy(self.state)
        bad["profiles"][0]["option_id"] = "forged"
        with self.assertRaises(bridge.WaUpperClipError):
            bridge.audit_wa_upper_clip_state(bad)

    def test_wrong_beta_and_absent_weight_fail_closed(self):
        profile = self.state["profiles"][0]
        weights = deepcopy(self.state["weights"])
        beta = self.state["thresholds"]["bottleneck_weight"]
        with self.assertRaises(bridge.WaUpperClipError):
            bridge.certify_original_upper_clip_trace(profile, weights, True)
        weights.pop(next(iter(weights)))
        with self.assertRaises(bridge.WaUpperClipError):
            bridge.certify_original_upper_clip_trace(profile, weights, beta)

    def test_unobserved_phase_does_not_claim_a_checked_clipping(self):
        early = deepcopy(self.state)
        early["current_phase"] = "observe"
        # A prior-state guard may reject this inconsistent forged phase;
        # neither possible outcome is a certified v0.24 upper-clipping pass.
        try:
            result = bridge.audit_wa_upper_clip_state(early)
        except bridge.WaUpperClipError:
            return
        self.assertFalse(result["all_local_upper_clips_checked"])

    def test_local_success_is_not_python_or_issuer_authority(self):
        audit = bridge.audit_wa_upper_clip_state(self.state)
        self.assertFalse(audit["global_ieee754_semantics_proved"])
        self.assertFalse(audit["python_min_max_sum_semantics_proved"])
        self.assertFalse(audit["external_issuer_authenticated"])
        self.assertFalse(audit["host_authority_granted"])


if __name__ == "__main__":
    unittest.main()
