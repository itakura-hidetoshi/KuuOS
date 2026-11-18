"""v0.23 native final Wa score vs exact rational normalized comparison tests.

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

from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as bridge
from runtime import kuuos_lean_python_wa_normalization_v0_22 as prior
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime import kuuos_lean_python_belief_receipt_native_cycle_v0_18 as native
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


def q(value):
    return Fraction(*value)


class WaNormalizedScoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v023-native-wa-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.native_fixture = native.build_belief_receipt_native_fixture(cls.root)
        cls.final_wa = WaDecisionStore(cls.root / "wa").recover(require_snapshot_match=True)
        cls.plural = PluralDecisionStore(cls.root / "plural").recover(require_snapshot_match=True)
        cls.decision = DecisionStore(cls.root / "decision").recover(require_snapshot_match=True)
        cls.belief = BeliefGerbeStore(cls.root / "belief").recover(require_snapshot_match=True)
        cls.genesis = json.loads((cls.root / "wa/wa-v03-genesis.json").read_text())
        cls.events = [json.loads(line)["event"] for line in
                      (cls.root / "wa/wa-v03-ledger.jsonl").read_text().splitlines()]

    def certify_first(self):
        return bridge.certify_normalized_final_trace(
            self.final_wa["profiles"][0], self.final_wa["weights"],
            self.final_wa["thresholds"]["bottleneck_weight"])

    def test_real_native_all_local_final_scores_bound_exactly(self):
        audit = bridge.audit_wa_normalized_final_state(self.final_wa)
        self.assertEqual(audit["version"], bridge.VERSION)
        self.assertEqual(audit["state_digest"], _fingerprint(self.final_wa))
        self.assertTrue(audit["all_local_final_score_checks_passed"])
        self.assertEqual(len(audit["certificates"]), len(self.final_wa["wa_records"]))
        for certificate in audit["certificates"]:
            self.assertEqual(len(certificate["endpoints"]), 2)
            self.assertTrue(certificate["normalized_final_score_ideal_only"])
            for bound in certificate["endpoints"]:
                self.assertTrue(bound["conditional_score_bound_checked"])
                self.assertLessEqual(q(bound["observed_final_score_error"]),
                                     q(bound["composed_score_error_upper_bound"]))
                self.assertLessEqual(q(bound["observed_final_score_error"]),
                                     q(bound["two_stage_composed_upper_bound"]))
                self.assertFalse(bound["python_builtin_sum_semantics_proved"])

    def test_exact_relational_contraction_for_original_weight(self):
        certificate = self.certify_first()
        for bound in certificate["endpoints"]:
            self.assertLessEqual(q(bound["weighted_ideal_contraction_error"]),
                                 abs(q(bound["observed_native_weighted"]) -
                                     q(bound["exact_normalized_weighted"])))

    def test_two_stage_relational_and_alert_error_adds(self):
        certificate = self.certify_first()
        for bound in certificate["endpoints"]:
            self.assertLessEqual(q(bound["measured_raw_wa_error"]),
                                 q(bound["measured_wa_relational_stage_error"]) +
                                 q(bound["measured_wa_alert_stage_error"]))
            self.assertEqual(q(bound["two_stage_composed_upper_bound"]),
                             q(bound["measured_wa_relational_stage_error"]) +
                             q(bound["measured_wa_alert_stage_error"]) +
                             q(bound["normalized_weighted_budget"]))

    def test_normalized_final_budget_is_explicit_sum(self):
        for bound in self.certify_first()["endpoints"]:
            self.assertEqual(q(bound["composed_score_error_upper_bound"]),
                             q(bound["measured_raw_wa_error"]) +
                             q(bound["normalized_weighted_budget"]))
            self.assertEqual(q(bound["observed_final_score_error"]),
                             abs(q(bound["observed_native_wa_score"]) -
                                 q(bound["normalized_ideal_score"])))

    def test_original_native_lower_and_upper_stored_scores_unchanged(self):
        audit = bridge.audit_wa_normalized_final_state(self.final_wa)
        for item, record in zip(audit["certificates"], self.final_wa["wa_records"]):
            for endpoint in item["endpoints"]:
                bound = endpoint["endpoint"]
                native_score = record["wa_interval"][bound]
                self.assertEqual(q(endpoint["observed_native_wa_score"]),
                                 Fraction(*native_score.as_integer_ratio()))
        self.assertFalse(audit["original_state_modified"])

    def test_v022_normalized_weighted_values_are_byte_equivalent(self):
        newer = bridge.audit_wa_normalized_final_state(self.final_wa)
        older = prior.audit_wa_normalization_state(self.final_wa)
        for new, old in zip(newer["certificates"], older["certificates"]):
            self.assertEqual(new["option_id"], old["option_id"])
            for v23, v22 in zip(new["endpoints"], old["endpoint_certificates"]):
                self.assertEqual(v23["exact_normalized_weighted"],
                                 v22["exact_normalized_weighted"])
                self.assertEqual(v23["normalized_weighted_budget"],
                                 v22["combined_error_bound"])

    def test_original_lower_upper_alert_cross_selection_is_preserved(self):
        fields = v20.trace_native_wa_score(
            self.final_wa["profiles"][0], self.final_wa["weights"],
            self.final_wa["thresholds"]["bottleneck_weight"])["fields"]
        beta = Fraction(*self.final_wa["thresholds"]["bottleneck_weight"].as_integer_ratio())
        for bound, alert_bound, certificate in zip(
                ("lower", "upper"), ("upper", "lower"), self.certify_first()["endpoints"]):
            with self.subTest(bound=bound):
                self.assertEqual(certificate["endpoint"], bound)
                weakest = Fraction(*fields["weakest_interval." + bound].as_integer_ratio())
                alert = Fraction(*fields["alert_interval." + alert_bound].as_integer_ratio())
                normalized = q(certificate["exact_normalized_weighted"])
                self.assertEqual(q(certificate["normalized_ideal_score"]),
                                 bridge._rational_ideal(beta, normalized, weakest, alert))

    def test_simple_rational_wa_ideal_is_original_formula(self):
        self.assertEqual(bridge._rational_ideal(
            Fraction(1, 2), Fraction(1, 2),
            Fraction(1, 4), Fraction(1, 4)), Fraction(9, 32))
        self.assertEqual(bridge._rational_ideal(
            Fraction(0), Fraction(1, 2), Fraction(1), Fraction(0)), Fraction(1, 2))

    def test_real_native_ledger_replay_exactly_preserves_original_adapter(self):
        state = deepcopy(self.genesis)
        for event in self.events:
            expected = prior.checked_apply_wa_normalization_event(
                state, event, self.plural, self.decision, self.belief)
            observed = bridge.checked_apply_wa_normalized_final_event(
                state, event, self.plural, self.decision, self.belief)
            with self.subTest(target_phase=event["target_phase"]):
                self.assertEqual(observed, expected)
                self.assertEqual(observed["status"], "APPLIED")
            state = observed["state"]
        self.assertEqual(state, self.final_wa)

    def test_mutation_or_reseal_of_existing_wa_score_is_blocked(self):
        forged = deepcopy(self.final_wa)
        score = forged["wa_records"][0]["wa_interval"]["lower"]
        forged["wa_records"][0]["wa_interval"]["lower"] = math.nextafter(score, math.inf)
        with self.assertRaises(bridge.WaNormalizedScoreError):
            bridge.audit_wa_normalized_final_state(forged)

    def test_missing_and_wrong_type_inputs_fail_closed(self):
        with self.assertRaises(bridge.WaNormalizedScoreError) as error:
            bridge.audit_wa_normalized_final_state(None)
        self.assertEqual(error.exception.status, "NO_DATA")
        with self.assertRaises(bridge.WaNormalizedScoreError):
            bridge.certify_normalized_final_trace(None, self.final_wa["weights"], 0.2)
        with self.assertRaises(bridge.WaNormalizedScoreError):
            bridge.certify_normalized_final_trace(
                self.final_wa["profiles"][0], None, 0.2)

    def test_nonfinite_beta_and_wrong_positive_sample_block(self):
        for bad in (float("nan"), float("inf"), -0.1, 1.1):
            with self.subTest(beta=bad):
                with self.assertRaises(bridge.WaNormalizedScoreError):
                    bridge.certify_normalized_final_trace(
                        self.final_wa["profiles"][0], self.final_wa["weights"], bad)
        forged = deepcopy(self.final_wa)
        name = v20.native._POSITIVE[0]
        forged["profiles"][0]["positive_intervals"][name]["lower"] = -0.1
        with self.assertRaises(bridge.WaNormalizedScoreError):
            bridge.audit_wa_normalized_final_state(forged)

    def test_forged_native_original_wa_record_is_not_a_trusted_profile(self):
        forged = deepcopy(self.final_wa)
        forged["profiles"][0]["option_id"] = "forged-option-id"
        with self.assertRaises(bridge.WaNormalizedScoreError):
            bridge.audit_wa_normalized_final_state(forged)

    def test_preevaluation_phase_does_not_claim_global_score_proof(self):
        audit = bridge.audit_wa_normalized_final_state(self.genesis)
        self.assertEqual(audit["certificates"], [])
        self.assertFalse(audit["all_local_final_score_checks_passed"])

    def test_original_state_and_caller_inputs_are_not_mutated(self):
        before = _fingerprint(self.final_wa)
        bridge.audit_wa_normalized_final_state(self.final_wa)
        self.assertEqual(before, _fingerprint(self.final_wa))
        before_args = _fingerprint([self.genesis, self.events[0],
                                    self.plural, self.decision, self.belief])
        bridge.checked_apply_wa_normalized_final_event(
            self.genesis, self.events[0], self.plural, self.decision, self.belief)
        self.assertEqual(before_args, _fingerprint([
            self.genesis, self.events[0], self.plural, self.decision, self.belief]))

    def test_global_semantics_and_authority_flags_remain_false(self):
        audit = bridge.audit_wa_normalized_final_state(self.final_wa)
        self.assertFalse(audit["global_ieee754_semantics_proved"])
        self.assertFalse(audit["python_lean_full_refinement_proved"])
        self.assertFalse(audit["external_issuer_authenticated"])
        self.assertFalse(audit["host_authority_granted"])
        for record in audit["certificates"]:
            self.assertFalse(record["original_score_modified"])
            self.assertFalse(record["all_input_python_lean_refinement_proved"])

    def test_unknown_phase_cannot_skip_final_score_check(self):
        forged = deepcopy(self.final_wa)
        forged["current_phase"] = "invalid"
        with self.assertRaises(bridge.WaNormalizedScoreError):
            bridge.audit_wa_normalized_final_state(forged)


if __name__ == "__main__":
    unittest.main()
