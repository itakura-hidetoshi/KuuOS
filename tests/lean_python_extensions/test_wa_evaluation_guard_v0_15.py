"""Regressions for exact native Python-float Wa score derivation.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from copy import deepcopy
import math
import unittest
from unittest.mock import patch
from runtime import kuuos_lean_python_wa_evaluation_guard_v0_15 as guard
from runtime import kuuos_lean_python_wa_gate_guard_v0_14 as prior
from runtime import kuuos_decision_os_wa_kernel_v0_3 as kernel
from runtime import kuuos_decision_os_wa_types_v0_3 as types
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from tests.lean_python_extensions.test_mediator_transition_v0_12 import _native_traces


class WaEvaluationGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = _native_traces()["DecisionOSWa"][3]

    def case(self, index=0):
        return deepcopy(self.trace.pairs[index])

    def seal(self, result):
        state = result["state"]
        state["wa_state_digest"] = types.wa_state_digest(state)
        result["result_wa_state_digest"] = state["wa_state_digest"]
        result["wa_apply_result_digest"] = types.wa_apply_result_digest(result)
        return result

    def assert_pre_blocked(self, before, event, status="BLOCKED"):
        old = _fingerprint([before, event])
        with patch.object(prior, "checked_apply_wa_gate_event", wraps=prior.checked_apply_wa_gate_event) as gate:
            with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                guard.checked_apply_wa_evaluation_event(before, event)
            gate.assert_not_called()
        self.assertEqual(caught.exception.status, status)
        self.assertEqual(_fingerprint([before, event]), old)
        return caught.exception

    def assert_post_blocked(self, before, event, result, status="BLOCKED"):
        with patch.object(kernel, "apply_wa_event", return_value=result):
            with patch.object(prior, "checked_apply_wa_gate_event", wraps=prior.checked_apply_wa_gate_event) as gate:
                with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                    guard.checked_apply_wa_evaluation_event(before, event)
                self.assertEqual(gate.call_count, 1)
        self.assertEqual(caught.exception.status, status)
        return caught.exception

    def test_genuine_all_phases_match_original_gate_and_one_return(self):
        self.assertEqual(len(self.trace.pairs), 6)
        for before, event in self.trace.pairs:
            expected = prior.checked_apply_wa_gate_event(before, event)
            self.assertEqual(guard.checked_apply_wa_evaluation_event(before, event), expected)
            self.assertEqual(guard.checked_apply_wa_evaluation_event(expected["state"], event),
                             prior.checked_apply_wa_gate_event(expected["state"], event))

    def test_genuine_stored_records_match_independently_computed_all_fields(self):
        before, _ = self.case(2)
        self.assertEqual(before["current_phase"], "evaluate")
        self.assertEqual(len(before["profiles"]), len(before["wa_records"]))
        beta = float(before["thresholds"]["bottleneck_weight"])
        for index, (profile, record) in enumerate(zip(before["profiles"], before["wa_records"])):
            result = guard._calculate(profile, before["weights"], beta, str(index))
            self.assertEqual(_fingerprint(result), _fingerprint(record))
            self.assertEqual(set(result), set(record))
            for name in ("weighted_interval", "weakest_interval", "relational_interval",
                         "alert_interval", "wa_interval"):
                self.assertIs(type(result[name]["lower"]), float)
                self.assertIs(type(result[name]["upper"]), float)

    def test_original_v014_accepts_in_range_score_forgery_but_v015_rejects_post(self):
        before, event = self.case(1)
        real = kernel.apply_wa_event(before, event)
        forged = deepcopy(real)
        forged["state"]["wa_records"][0]["weighted_interval"] = {"lower": .25, "upper": .5}
        self.seal(forged)
        with patch.object(kernel, "apply_wa_event", return_value=forged):
            self.assertEqual(prior.checked_apply_wa_gate_event(before, event), forged)
        issue = self.assert_post_blocked(before, event, forged)
        self.assertIn("weighted_interval", str(issue))

    def test_each_five_intervals_differently_resealed_forgery_is_rejected(self):
        before, event = self.case(1)
        original = kernel.apply_wa_event(before, event)
        for name, replacement in (
            ("weighted_interval", {"lower": .1, "upper": .4}),
            ("weakest_interval", {"lower": .1, "upper": .4}),
            ("relational_interval", {"lower": .1, "upper": .4}),
            ("alert_interval", {"lower": .1, "upper": .4}),
            ("wa_interval", {"lower": .1, "upper": .3, "width": .3 - .1}),
        ):
            changed = deepcopy(original)
            changed["state"]["wa_records"][0][name] = replacement
            self.seal(changed)
            with self.subTest(name=name):
                with patch.object(kernel, "apply_wa_event", return_value=changed):
                    self.assertEqual(prior.checked_apply_wa_gate_event(before, event), changed)
                self.assertIn(name, str(self.assert_post_blocked(before, event, changed)))

    def test_single_ulp_change_is_not_silently_tolerated(self):
        before, event = self.case(1)
        result = kernel.apply_wa_event(before, event)
        value = result["state"]["wa_records"][0]["weighted_interval"]["lower"]
        result["state"]["wa_records"][0]["weighted_interval"]["lower"] = math.nextafter(value, math.inf)
        self.seal(result)
        with patch.object(kernel, "apply_wa_event", return_value=result):
            self.assertEqual(prior.checked_apply_wa_gate_event(before, event), result)
        self.assert_post_blocked(before, event, result)

    def test_resealed_prestate_score_forgery_stops_before_prior_and_replay(self):
        before, event = self.case(2)
        before["wa_records"][0]["weighted_interval"] = {"lower": .2, "upper": .4}
        before["wa_state_digest"] = types.wa_state_digest(before)
        self.assertEqual(kernel.validate_wa_state(before), [])
        self.assert_pre_blocked(before, event)
        self.assert_pre_blocked(before, self.case(1)[1])

    def test_preexisting_invalid_evaluation_stops_even_for_rejected_event(self):
        before, event = self.case(2)
        before["wa_records"][0]["relational_interval"] = {"lower": .2, "upper": .4}
        before["wa_state_digest"] = types.wa_state_digest(before)
        malformed = deepcopy(event)
        malformed.pop("wa_event_digest")
        self.assert_pre_blocked(before, malformed)

    def test_record_order_and_extra_fields_cannot_be_resealed(self):
        before, event = self.case(2)
        state = deepcopy(before)
        state["wa_records"][0]["hidden_score"] = .5
        state["wa_state_digest"] = types.wa_state_digest(state)
        self.assert_pre_blocked(state, event)
        if len(before["wa_records"]) > 1:
            swapped = deepcopy(before)
            swapped["wa_records"].reverse()
            swapped["wa_state_digest"] = types.wa_state_digest(swapped)
            self.assert_pre_blocked(swapped, event)

    def test_routed_gate_and_commit_preserve_existing_results(self):
        for index in (4, 5):
            before, event = self.case(index)
            with patch.object(prior, "checked_apply_wa_gate_event",
                              wraps=prior.checked_apply_wa_gate_event) as old:
                result = guard.checked_apply_wa_evaluation_event(before, event)
                self.assertEqual(old.call_count, 1)
            self.assertEqual(result, prior.checked_apply_wa_gate_event(before, event))

    def test_native_rejection_has_identical_status_errors_and_digest(self):
        before, event = self.case()
        event.pop("wa_event_digest")
        expected = prior.checked_apply_wa_gate_event(before, event)
        self.assertEqual(expected["status"], "REJECTED")
        self.assertEqual(guard.checked_apply_wa_evaluation_event(before, event), expected)

    def test_missing_numeric_input_is_no_data_before_prior(self):
        before, event = self.case(2)
        for field in ("profiles", "weights", "thresholds", "wa_records"):
            changed = deepcopy(before)
            changed.pop(field)
            with self.subTest(field=field):
                self.assert_pre_blocked(changed, event, "NO_DATA")

    def test_invalid_finite_json_rejected_before_prior_without_user_hooks(self):
        before, event = self.case()
        for invalid in (float("nan"), float("inf"), {1: "illegal"}, (1,), object()):
            changed = deepcopy(event)
            changed["invalid_extra"] = invalid
            with self.subTest(kind=type(invalid).__name__):
                with patch.object(prior, "checked_apply_wa_gate_event") as old:
                    with self.assertRaises(guard.WaEvaluationBoundaryError):
                        guard.checked_apply_wa_evaluation_event(before, changed)
                    old.assert_not_called()

    def test_missing_prerequisites_fail_closed(self):
        before, event = self.case()
        for name in ("_finite_json", "_fingerprint", "_state_numbers"):
            with self.subTest(name=name), patch.object(guard, name, None):
                with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                    guard.checked_apply_wa_evaluation_event(before, event)
                self.assertEqual(caught.exception.status, "NO_DATA")
        with patch.object(prior, "checked_apply_wa_gate_event", None):
            with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                guard.checked_apply_wa_evaluation_event(before, event)
            self.assertEqual(caught.exception.status, "NO_DATA")

    def test_prior_no_data_and_blocked_errors_are_not_upgraded(self):
        before, event = self.case()
        for status in ("BLOCKED", "NO_DATA"):
            with patch.object(prior, "checked_apply_wa_gate_event",
                              side_effect=prior.WaGateBoundaryError(status, ("local-prior",))):
                with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                    guard.checked_apply_wa_evaluation_event(before, event)
            self.assertEqual(caught.exception.status, status)
            self.assertIn("local-prior", str(caught.exception))

    def test_gate_adapter_argument_mutation_is_blocked(self):
        before, event = self.case()
        def mutated(s, e):
            e["event_index"] = .5
            return {"status": "REJECTED", "state": s}
        with patch.object(prior, "checked_apply_wa_gate_event", side_effect=mutated):
            with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                guard.checked_apply_wa_evaluation_event(before, event)
        self.assertIn("argument_mutated", str(caught.exception))

    def test_status_and_poststate_cannot_skip_score_check(self):
        before, event = self.case(1)
        true_result = prior.checked_apply_wa_gate_event(before, event)
        for status in (None, True, 1, "PASS"):
            changed = deepcopy(true_result)
            changed["status"] = status
            with self.subTest(status=status), patch.object(prior, "checked_apply_wa_gate_event", return_value=changed):
                with self.assertRaises(guard.WaEvaluationBoundaryError):
                    guard.checked_apply_wa_evaluation_event(before, event)
        changed = deepcopy(true_result)
        changed["state"]["wa_records"][0]["weighted_interval"] = {"lower": .2, "upper": .4}
        with patch.object(prior, "checked_apply_wa_gate_event", return_value=changed):
            with self.assertRaises(guard.WaEvaluationBoundaryError) as caught:
                guard.checked_apply_wa_evaluation_event(before, event)
        self.assertIn("derived_value_mismatch", str(caught.exception))

    def test_caller_inputs_and_returned_native_values_do_not_alias(self):
        before, event = self.case()
        original = _fingerprint([before, event])
        result = guard.checked_apply_wa_evaluation_event(before, event)
        result["state"]["profiles"].clear()
        self.assertEqual(_fingerprint([before, event]), original)


if __name__ == "__main__":
    unittest.main()
