"""v0.21 real native-Wa seven-product rounding/sum error certificate tests.

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
from unittest.mock import patch

from runtime import kuuos_lean_python_wa_weighted_sum_certificate_v0_21 as bridge
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as prior
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


def q(pair):
    return Fraction(*pair)


class WaWeightedSumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v021-real-wa-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.native_result = native.build_belief_receipt_native_fixture(cls.root)
        cls.final_wa = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.belief = BeliefGerbeStore(cls.root / "belief").recover(require_snapshot_match=True)
        cls.genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.events = [json.loads(line)["event"] for line in
                      (cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]

    def get_trace(self):
        return prior.trace_native_wa_score(
            self.final_wa["profiles"][0], self.final_wa["weights"],
            self.final_wa["thresholds"]["bottleneck_weight"])

    def test_genuine_native_7_axis_certificates_both_endpoints(self):
        audit = bridge.audit_wa_weighted_state(self.final_wa)
        self.assertEqual(audit["version"], bridge.VERSION)
        self.assertEqual(audit["state_digest"], _fingerprint(self.final_wa))
        self.assertEqual(audit["wa_v020_record_count"], len(self.final_wa["wa_records"]))
        self.assertEqual(len(audit["certificates"]), len(self.final_wa["wa_records"]))
        for item in audit["certificates"]:
            self.assertEqual(item["certified_endpoint_count"], 2)
            self.assertTrue(item["rational_finite_sum_inequalities_checked"])
            for endpoint in item["endpoints"]:
                self.assertEqual(endpoint["product_count"], 7)
                self.assertEqual(len(endpoint["products"]), 7)
                self.assertTrue(endpoint["bound_checked"])
                self.assertLessEqual(q(endpoint["observed_weighted_error"]),
                                     q(endpoint["composed_upper_bound"]))
                self.assertFalse(endpoint["builtin_sum_semantics_proved"])

    def test_exact_signed_error_telescoping(self):
        certificate = bridge.certify_weighted_trace(self.get_trace())
        for endpoint in certificate["endpoints"]:
            self.assertEqual(q(endpoint["rounded_product_sum"]) -
                             q(endpoint["exact_weighted"]),
                             q(endpoint["signed_product_error_sum"]))
            self.assertLessEqual(q(endpoint["sum_absolute_product_errors"]),
                                 q(endpoint["half_quantum_budget"]))
            self.assertEqual(q(endpoint["composed_upper_bound"]),
                             q(endpoint["observed_builtin_sum_error"]) +
                             q(endpoint["half_quantum_budget"]))

    def test_python_builtin_sum_has_separate_measured_error(self):
        certificate = bridge.certify_weighted_trace(self.get_trace())
        for endpoint in certificate["endpoints"]:
            self.assertEqual(
                q(endpoint["observed_builtin_sum_error"]),
                abs(q(endpoint["native_weighted"]) -
                    q(endpoint["rounded_product_sum"])))
        self.assertFalse(certificate["builtin_sum_semantics_proved"])
        self.assertFalse(certificate["ieee754_global_semantics_proved"])
        self.assertFalse(certificate["lean_python_full_refinement_proved"])

    def test_order_and_axis_names_bound_to_original_native_trace(self):
        certificate = bridge.certify_weighted_trace(self.get_trace())
        expected = tuple(prior.native._POSITIVE)
        for row in certificate["endpoints"]:
            self.assertEqual(tuple(p["label"].split(":weight:")[1] for p in row["products"]),
                             expected)

    def test_original_wa_score_and_state_are_unchanged(self):
        original = _fingerprint(self.final_wa)
        audit = bridge.audit_wa_weighted_state(self.final_wa)
        self.assertEqual(original, _fingerprint(self.final_wa))
        self.assertFalse(audit["action_authority_granted"])
        self.assertFalse(audit["full_refinement_proved"])

    def test_explicit_native_event_cycle_matches_v020_without_repair(self):
        state = deepcopy(self.genesis)
        for event in self.events:
            expected = prior.checked_apply_wa_binary64_event(
                state, event, self.plural, self.decision, self.belief)
            observed = bridge.checked_apply_wa_weighted_event(
                state, event, self.plural, self.decision, self.belief)
            with self.subTest(target_phase=event["target_phase"]):
                self.assertEqual(observed, expected)
                self.assertEqual(observed["status"], "APPLIED")
            state = observed["state"]
        self.assertEqual(state, self.final_wa)

    def test_resealed_one_ulp_original_score_change_is_still_rejected(self):
        forged = deepcopy(self.final_wa)
        item = forged["wa_records"][0]["weighted_interval"]
        item["lower"] = math.nextafter(item["lower"], math.inf)
        with self.assertRaises(bridge.WaWeightedSumError):
            bridge.audit_wa_weighted_state(forged)

    def test_forged_original_product_exact_value_is_rejected(self):
        trace = self.get_trace()
        trace["steps"][0]["exact"] = [999, 1]
        with self.assertRaisesRegex(bridge.WaWeightedSumError, "product_ideal_mismatch"):
            bridge.certify_weighted_trace(trace)

    def test_forged_signed_absolute_error_is_rejected(self):
        trace = self.get_trace()
        trace["steps"][0]["absolute_error"] = [333, 1]
        with self.assertRaisesRegex(bridge.WaWeightedSumError, "signed_product_error_mismatch"):
            bridge.certify_weighted_trace(trace)

    def test_forged_neighbor_quantum_or_midpoint_is_rejected(self):
        trace = self.get_trace()
        trace["steps"][0]["maximum_neighbor_gap"] = [0, 1]
        with self.assertRaisesRegex(bridge.WaWeightedSumError, "neighbor_gap_mismatch"):
            bridge.certify_weighted_trace(trace)
        trace = self.get_trace()
        trace["steps"][0]["previous"] = [100, 1]
        with self.assertRaisesRegex(bridge.WaWeightedSumError, "strict_neighbor_order_required"):
            bridge.certify_weighted_trace(trace)

    def test_corrupted_builtin_sum_certificate_is_rejected(self):
        for key, bad in (("exact_sum", [999, 1]),
                         ("absolute_error", [999, 1]),
                         ("terms", 6), ("bound", "upper")):
            with self.subTest(key=key):
                trace = self.get_trace()
                trace["builtin_summations"][0][key] = bad
                with self.assertRaises(bridge.WaWeightedSumError):
                    bridge.certify_weighted_trace(trace)

    def test_forged_semantics_flag_is_never_accepted(self):
        trace = self.get_trace()
        trace["builtin_summations"][0]["builtin_sum_semantics_proved"] = True
        with self.assertRaisesRegex(bridge.WaWeightedSumError, "unproved_semantics_flag_required"):
            bridge.certify_weighted_trace(trace)

    def test_noncanonical_ratios_bool_and_missing_field_block(self):
        for pair in ([2, 4], [1, 0], [True, 1], [1, False], ("1", 1), None):
            with self.subTest(pair=pair):
                with self.assertRaises(bridge.WaWeightedSumError):
                    bridge._ratio(pair, "invalid")
        trace = self.get_trace()
        del trace["steps"][0]["exact"]
        with self.assertRaises(bridge.WaWeightedSumError):
            bridge.certify_weighted_trace(trace)

    def test_missing_wa_state_keeps_no_data_and_phase_does_not_skip(self):
        with self.assertRaises(bridge.WaWeightedSumError) as caught:
            bridge.audit_wa_weighted_state(None)
        self.assertEqual(caught.exception.status, "NO_DATA")
        state = deepcopy(self.final_wa)
        state["current_phase"] = "invalid"
        with self.assertRaises(bridge.WaWeightedSumError):
            bridge.audit_wa_weighted_state(state)

    def test_pre_evaluate_state_has_no_new_certificates(self):
        audit = bridge.audit_wa_weighted_state(self.genesis)
        self.assertEqual(audit["certificates"], [])
        self.assertFalse(audit["python_builtin_sum_semantics_proved"])

    def test_checked_adapter_preserves_caller_arguments(self):
        before = _fingerprint([
            self.genesis, self.events[0], self.plural, self.decision, self.belief,
        ])
        bridge.checked_apply_wa_weighted_event(
            self.genesis, self.events[0], self.plural, self.decision, self.belief)
        self.assertEqual(before, _fingerprint([
            self.genesis, self.events[0], self.plural, self.decision, self.belief,
        ]))

    def test_garbled_trace_list_does_not_pass(self):
        trace = self.get_trace()
        trace["steps"] = trace["steps"][:-1]
        with self.assertRaisesRegex(bridge.WaWeightedSumError, "original_27_rounding_steps_required"):
            bridge.certify_weighted_trace(trace)


if __name__ == "__main__":
    unittest.main()
