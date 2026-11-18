"""v0.20 exact float-neighbor certificates on actual native Wa state.

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

from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as bridge
from runtime import kuuos_lean_python_wa_rational_shadow_v0_19 as prior
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class WaBinary64MidpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v020-native-wa-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.run = native.build_belief_receipt_native_fixture(cls.root)
        cls.final_wa = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.belief = BeliefGerbeStore(cls.root / "belief").recover(require_snapshot_match=True)
        cls.genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.events = [json.loads(line)["event"] for line in
                      (cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]

    def test_concrete_python_add_rounding_obstruction(self):
        value, cert = bridge.observed_binary64_operation(0.1, 0.2, "add", "native_add")
        self.assertEqual(value, 0.1 + 0.2)
        self.assertEqual(Fraction(*cert["absolute_error"]), Fraction(1, 36028797018963968))
        self.assertLessEqual(Fraction(*cert["absolute_error"]),
                             Fraction(*cert["maximum_neighbor_gap"]) / 2)
        self.assertTrue(cert["exact_midpoint_certificate_checked"])

    def test_concrete_multiplication_and_subtraction(self):
        for a, b, op in ((1.1, 3.0, "mul"), (0.3, 0.1, "sub"),
                         (-0.75, 0.125, "add"), (0.0, 0.0, "sub")):
            with self.subTest(a=a, b=b, op=op):
                _, cert = bridge.observed_binary64_operation(a, b, op)
                self.assertLessEqual(Fraction(*cert["absolute_error"]),
                                     Fraction(*cert["maximum_neighbor_gap"]) / 2)

    def test_subnormal_ties_even_is_not_half_up_grid_identity(self):
        smallest = math.nextafter(0.0, math.inf)
        observed, cert = bridge.observed_binary64_operation(smallest, 0.5, "mul")
        self.assertEqual(observed, 0.0)
        quantum = Fraction(*smallest.as_integer_ratio())
        self.assertEqual(Fraction(*cert["exact"]), quantum / 2)
        # A half-up uniform grid would choose +smallest, whereas Python
        # ties-to-even produces zero. The grid identity is NOT certified.
        self.assertNotEqual(Fraction(*observed.as_integer_ratio()), quantum)
        self.assertFalse(bridge.audit_wa_binary64_state(self.genesis)["ieee754_global_semantics_proved"])

    def test_overflow_and_nonfinite_neighbors_fail_closed(self):
        for args in ((1e308, 2.0, "mul"), (float("inf"), 1.0, "add"),
                     (1.0, float("nan"), "mul"), (1, 1.0, "add")):
            with self.subTest(args=args):
                with self.assertRaises(bridge.WaBinary64MidpointError):
                    bridge.observed_binary64_operation(*args)

    def test_unknown_operator_and_forged_neighbors_are_rejected(self):
        with self.assertRaisesRegex(bridge.WaBinary64MidpointError, "unknown_operation"):
            bridge.observed_binary64_operation(0.1, 0.2, "divide")
        with patch.object(bridge.math, "nextafter", lambda x, direction: x):
            with self.assertRaisesRegex(bridge.WaBinary64MidpointError,
                                        "strict_finite_neighbors_required"):
                bridge.observed_binary64_operation(0.1, 0.2, "add")

    def test_real_native_wa_score_11_fields_and_midpoint_steps(self):
        audit = bridge.audit_wa_binary64_state(self.final_wa)
        self.assertEqual(audit["version"], bridge.VERSION)
        self.assertEqual(audit["state_digest"], _fingerprint(self.final_wa))
        self.assertGreater(len(audit["local_step_certificates"]), 0)
        self.assertEqual(audit["v019_certificates"], len(self.final_wa["wa_records"]))
        for item in audit["local_step_certificates"]:
            self.assertTrue(item["stored_scores_exact"])
            self.assertEqual(item["score_field_count"], 11)
            self.assertEqual(item["step_count"], 27)
            self.assertEqual(len(item["builtin_summations"]), 2)
            self.assertTrue(all(not s["builtin_sum_semantics_proved"]
                                for s in item["builtin_summations"]))
            for step in item["step_certificates"]:
                self.assertTrue(step["exact_midpoint_certificate_checked"])
                self.assertLessEqual(Fraction(*step["absolute_error"]),
                                     Fraction(*step["maximum_neighbor_gap"]) / 2)

    def test_opaque_builtin_sum_error_not_promoted_to_ieee_theorem(self):
        trace = bridge.trace_native_wa_score(
            self.final_wa["profiles"][0], self.final_wa["weights"],
            self.final_wa["thresholds"]["bottleneck_weight"])
        self.assertEqual(len(trace["builtin_summations"]), 2)
        for row in trace["builtin_summations"]:
            self.assertGreaterEqual(Fraction(*row["absolute_error"]), 0)
            self.assertFalse(row["builtin_sum_semantics_proved"])
        result = bridge.audit_wa_binary64_state(self.final_wa)
        self.assertFalse(result["builtin_sum_semantics_proved"])
        self.assertFalse(result["python_lean_full_refinement_proved"])
        self.assertFalse(result["host_authority_granted"])

    def test_single_ulp_stored_score_change_rejected_even_if_v019_accepts(self):
        forged = deepcopy(self.final_wa)
        low = forged["wa_records"][0]["wa_interval"]["lower"]
        forged["wa_records"][0]["wa_interval"]["lower"] = math.nextafter(low, math.inf)
        self.assertEqual(len(prior.audit_wa_rational_state(forged)["certificates"]),
                         len(forged["wa_records"]))
        with self.assertRaisesRegex(bridge.WaBinary64MidpointError,
                                    "native_float_trace_mismatch"):
            bridge.audit_wa_binary64_state(forged)

    def test_native_wa_event_ledger_replay_has_exact_existing_v019_result(self):
        state = deepcopy(self.genesis)
        for event in self.events:
            expected = prior.checked_apply_wa_rational_event(
                state, event, self.plural, self.decision, self.belief)
            observed = bridge.checked_apply_wa_binary64_event(
                state, event, self.plural, self.decision, self.belief)
            with self.subTest(phase=event["target_phase"]):
                self.assertEqual(observed, expected)
                self.assertEqual(observed["status"], "APPLIED")
            state = observed["state"]
        self.assertEqual(state, self.final_wa)

    def test_audit_does_not_mutate_original_state_or_scores(self):
        before = _fingerprint(self.final_wa)
        bridge.audit_wa_binary64_state(self.final_wa)
        self.assertEqual(_fingerprint(self.final_wa), before)

    def test_pre_evaluate_phase_has_no_score_certificates(self):
        audit = bridge.audit_wa_binary64_state(self.genesis)
        self.assertEqual(audit["local_step_certificates"], [])
        self.assertFalse(audit["external_issuer_authenticated"])

    def test_no_data_and_invalid_phase_fail_closed(self):
        with self.assertRaises(bridge.WaBinary64MidpointError) as ctx:
            bridge.audit_wa_binary64_state(None)
        self.assertEqual(ctx.exception.status, "NO_DATA")
        state = deepcopy(self.final_wa)
        state["current_phase"] = "unknown"
        with self.assertRaises(bridge.WaBinary64MidpointError):
            bridge.audit_wa_binary64_state(state)


if __name__ == "__main__":
    unittest.main()
