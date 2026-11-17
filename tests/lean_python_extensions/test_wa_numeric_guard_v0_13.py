"""Exact represented-value checks around genuine Wa event transitions.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import math
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_wa_numeric_guard_v0_13 as guard
from runtime import kuuos_lean_python_mediator_transition_v0_12 as mediator
from runtime import kuuos_decision_os_wa_kernel_v0_3 as kernel
from runtime import kuuos_decision_os_wa_types_v0_3 as types
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from tests.lean_python_extensions.test_mediator_transition_v0_12 import _native_traces


class WaNumericGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = _native_traces()["DecisionOSWa"][3]

    def case(self, index=0):
        return deepcopy(self.trace.pairs[index])

    def prior(self, state, event):
        return mediator.checked_apply_mediator_event("DecisionOSWa", state, event)

    def reseal_state(self, state):
        state["wa_state_digest"] = types.wa_state_digest(state)
        return state

    def reseal_event(self, event):
        event["wa_event_digest"] = types.wa_event_digest(event)
        return event

    def reseal_result(self, result):
        self.reseal_state(result["state"])
        result["result_wa_state_digest"] = result["state"]["wa_state_digest"]
        result["wa_apply_result_digest"] = types.wa_apply_result_digest(result)
        return result

    def customized_profile(self, *, lower=.1, upper=.9, alert_lower=0.0,
                           alert_upper=0.0, weight_delta=0.0, beta=None):
        before, event = self.case()
        before["weights"]["inclusion"] += weight_delta
        if beta is not None:
            before["thresholds"]["bottleneck_weight"] = beta
        self.reseal_state(before)
        event["expected_wa_state_digest"] = before["wa_state_digest"]
        for profile in event["payload"]["profiles"]:
            for interval in profile["positive_intervals"].values():
                interval.update(lower=lower, upper=upper)
            for interval in profile["alert_intervals"].values():
                interval.update(lower=alert_lower, upper=alert_upper)
        self.reseal_event(event)
        return before, event

    def evaluation_event(self, state):
        return kernel.build_wa_event(
            state=state, target_phase="evaluate", artifact_digest=types.sha("numeric-v013-evaluate"),
            payload={"evaluation_receipt_digest": types.sha("numeric-v013-receipt")},
            now_ms=state["updated_at_ms"] + 1,
        )

    def assert_pre_blocked(self, before, event, *, status="BLOCKED"):
        with patch.object(guard, "checked_apply_mediator_event") as prior:
            with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                guard.checked_apply_wa_numeric_event(before, event)
        prior.assert_not_called()
        self.assertEqual(caught.exception.status, status)
        self.assertIs(type(caught.exception.issues), tuple)
        self.assertTrue(caught.exception.issues)
        return caught.exception

    def assert_post_blocked(self, before, event, result, *, status="BLOCKED"):
        # The actual v0.12 checks still run around the coherently resealed result.
        with patch.object(kernel, "apply_wa_event", return_value=result) as native:
            with patch.object(guard, "checked_apply_mediator_event",
                              wraps=mediator.checked_apply_mediator_event) as prior:
                with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                    guard.checked_apply_wa_numeric_event(before, event)
        self.assertEqual(prior.call_count, 1)
        self.assertEqual(native.call_count, 1)
        self.assertEqual(caught.exception.status, status)
        return caught.exception

    def test_known_native_rounding_counterexample_is_blocked_without_correction(self):
        before, profile_event = self.customized_profile(lower=1.0, upper=1.0, weight_delta=5e-13)
        profiled = guard.checked_apply_wa_numeric_event(before, profile_event)["state"]
        event = self.evaluation_event(profiled)
        original = self.prior(profiled, event)
        self.assertEqual(original["status"], "APPLIED")
        self.assertEqual(kernel.validate_wa_state(original["state"]), [])
        interval = original["state"]["wa_records"][0]["wa_interval"]
        self.assertGreater(interval["lower"], interval["upper"])
        self.assertLess(interval["width"], 0.0)
        saved = _fingerprint([profiled, event, original])
        with patch.object(kernel, "apply_wa_event", wraps=kernel.apply_wa_event) as native:
            with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                guard.checked_apply_wa_numeric_event(profiled, event)
        self.assertEqual(caught.exception.status, "BLOCKED")
        self.assertIn("post_state", str(caught.exception))
        self.assertEqual(native.call_count, 1)
        self.assertEqual(_fingerprint([profiled, event, original]), saved)

    def test_all_six_genuine_phases_match_and_call_prior_and_kernel_once(self):
        self.assertEqual(len(self.trace.pairs), 6)
        for before, event in self.trace.pairs:
            expected = self.prior(before, event)
            with self.subTest(phase=event["target_phase"]):
                with patch.object(guard, "checked_apply_mediator_event",
                                  wraps=mediator.checked_apply_mediator_event) as prior:
                    with patch.object(kernel, "apply_wa_event", wraps=kernel.apply_wa_event) as native:
                        result = guard.checked_apply_wa_numeric_event(before, event)
                self.assertEqual(result["status"], "APPLIED")
                self.assertEqual(_fingerprint(result), _fingerprint(expected))
                self.assertEqual(prior.call_count, 1)
                self.assertEqual(native.call_count, 1)
                self.assertEqual(prior.call_args.args[0], "DecisionOSWa")

    def test_genuine_old_event_replays_remain_unchanged(self):
        for _, event in self.trace.pairs:
            with self.subTest(phase=event["target_phase"]):
                expected = self.prior(self.trace.state, event)
                self.assertEqual(expected["status"], "REPLAYED")
                self.assertEqual(guard.checked_apply_wa_numeric_event(self.trace.state, event), expected)

    def test_native_rejected_profile_numeric_diagnostics_are_preserved(self):
        before, event = self.case()
        for bad in (-.1, 1.1, True, "not-a-number"):
            malformed = deepcopy(event)
            malformed["payload"]["profiles"][0]["positive_intervals"]["inclusion"]["lower"] = bad
            self.reseal_event(malformed)
            expected = self.prior(before, malformed)
            with self.subTest(value=bad):
                self.assertEqual(expected["status"], "REJECTED")
                self.assertEqual(guard.checked_apply_wa_numeric_event(before, malformed), expected)

    def test_exact_weight_sum_one_is_not_required(self):
        before, event = self.case()
        self.assertEqual(sum(before["weights"].values()), 1.0)
        self.assertNotEqual(sum(Fraction(value) for value in before["weights"].values()), Fraction(1))
        self.assertEqual(guard.checked_apply_wa_numeric_event(before, event), self.prior(before, event))

    def test_width_uses_native_subtraction_not_rational_endpoint_difference(self):
        before, event = self.customized_profile(lower=.1, upper=.9)
        profiled = guard.checked_apply_wa_numeric_event(before, event)["state"]
        event = self.evaluation_event(profiled)
        expected = self.prior(profiled, event)
        interval = expected["state"]["wa_records"][0]["wa_interval"]
        self.assertNotEqual(Fraction(interval["width"]), Fraction(interval["upper"]) - Fraction(interval["lower"]))
        self.assertEqual(interval["width"], interval["upper"] - interval["lower"])
        self.assertEqual(guard.checked_apply_wa_numeric_event(profiled, event), expected)

    def test_zero_one_integer_endpoints_and_beta_boundaries_preserve_native_results(self):
        for lower, upper, beta in ((0, 0, 0), (1, 1, 1), (0, 1, 0), (-0.0, 1.0, 1)):
            with self.subTest(lower=lower, upper=upper, beta=beta):
                before, event = self.customized_profile(lower=lower, upper=upper, beta=beta)
                expected = self.prior(before, event)
                self.assertEqual(guard.checked_apply_wa_numeric_event(before, event), expected)
                profiled = expected["state"]
                evaluate = self.evaluation_event(profiled)
                self.assertEqual(guard.checked_apply_wa_numeric_event(profiled, evaluate), self.prior(profiled, evaluate))

    def test_caller_data_and_result_do_not_alias(self):
        before, event = self.case()
        fingerprint = _fingerprint([before, event])
        result = guard.checked_apply_wa_numeric_event(before, event)
        result["state"]["profiles"].clear()
        result["errors"].append("local-only")
        self.assertEqual(_fingerprint([before, event]), fingerprint)

    def test_missing_scalar_and_record_containers_remain_no_data(self):
        before, event = self.case()
        for field in ("weights", "thresholds", "profiles", "wa_records", "false_harmony_records"):
            malformed = deepcopy(before)
            malformed.pop(field)
            with self.subTest(field=field):
                self.assert_pre_blocked(malformed, event, status="NO_DATA")
        self.assert_pre_blocked(None, event, status="NO_DATA")
        self.assert_pre_blocked(before, None, status="NO_DATA")

    def test_pre_weights_and_thresholds_require_exact_bounded_numbers(self):
        before, event = self.case()
        for container, field in (("weights", "inclusion"), ("thresholds", "bottleneck_weight")):
            for bad in (True, False, "0.5", None, [], math.nextafter(0.0, -math.inf), math.nextafter(1.0, math.inf)):
                malformed = deepcopy(before)
                malformed[container][field] = bad
                with self.subTest(container=container, value=bad):
                    self.assert_pre_blocked(malformed, event)

    def test_all_numeric_axis_and_scalar_inventories_are_required(self):
        before, event = self.case(1)
        for container in ("weights", "thresholds"):
            malformed = deepcopy(before)
            malformed[container].pop(next(iter(malformed[container])))
            self.assert_pre_blocked(malformed, event, status="NO_DATA")
            malformed = deepcopy(before)
            malformed[container]["unknown"] = .5
            self.assert_pre_blocked(malformed, event)
        for field in ("positive_intervals", "alert_intervals"):
            malformed = deepcopy(before)
            malformed["profiles"][0][field].pop(next(iter(malformed["profiles"][0][field])))
            self.assert_pre_blocked(malformed, event, status="NO_DATA")
            malformed = deepcopy(before)
            malformed["profiles"][0][field]["unknown"] = {"lower": 0.0, "upper": 1.0}
            self.assert_pre_blocked(malformed, event)

    def test_profile_state_intervals_are_checked_before_original(self):
        before, event = self.case(1)
        for field in ("positive_intervals", "alert_intervals"):
            for bad in (True, "0.2", None, math.nextafter(0.0, -math.inf), math.nextafter(1.0, math.inf)):
                malformed = deepcopy(before)
                axis = next(iter(malformed["profiles"][0][field]))
                malformed["profiles"][0][field][axis]["lower"] = bad
                with self.subTest(field=field, value=bad):
                    self.assert_pre_blocked(malformed, event)

    def test_preexisting_bad_numeric_record_blocks_replay_before_original(self):
        before, event = self.customized_profile(lower=1.0, upper=1.0, weight_delta=5e-13)
        profiled = self.prior(before, event)["state"]
        evaluate = self.evaluation_event(profiled)
        bad = self.prior(profiled, evaluate)["state"]
        self.assertEqual(self.prior(bad, evaluate)["status"], "REPLAYED")
        self.assert_pre_blocked(bad, evaluate)

    def test_each_derived_interval_rejects_bounds_and_next_float_inversion(self):
        before, event = self.case(1)
        real = self.prior(before, event)
        for field in ("weighted_interval", "weakest_interval", "relational_interval", "alert_interval", "wa_interval"):
            for change in ("negative", "above_one", "inverted"):
                result = deepcopy(real)
                interval = result["state"]["wa_records"][0][field]
                if change == "negative":
                    interval["lower"] = math.nextafter(0.0, -math.inf)
                elif change == "above_one":
                    interval["upper"] = math.nextafter(1.0, math.inf)
                else:
                    interval["upper"] = .5
                    interval["lower"] = math.nextafter(.5, math.inf)
                self.reseal_result(result)
                with self.subTest(field=field, change=change):
                    self.assertEqual(kernel.validate_wa_state(result["state"]), [])
                    self.assert_post_blocked(before, event, result)

    def test_each_derived_interval_rejects_numeric_alias_types(self):
        before, event = self.case(1)
        real = self.prior(before, event)
        for field in ("weighted_interval", "weakest_interval", "relational_interval", "alert_interval", "wa_interval"):
            for value in (False, "0.0", None):
                result = deepcopy(real)
                result["state"]["wa_records"][0][field]["lower"] = value
                self.reseal_result(result)
                with self.subTest(field=field, value=value):
                    self.assert_post_blocked(before, event, result)

    def test_missing_or_extra_interval_fields_cannot_silently_skip_checks(self):
        before, event = self.case(1)
        real = self.prior(before, event)
        for field in ("weighted_interval", "weakest_interval", "relational_interval", "alert_interval", "wa_interval"):
            result = deepcopy(real)
            result["state"]["wa_records"][0].pop(field)
            self.reseal_result(result)
            with self.subTest(field=field, change="missing_interval"):
                self.assert_post_blocked(before, event, result, status="NO_DATA")
            result = deepcopy(real)
            result["state"]["wa_records"][0][field].pop("lower")
            self.reseal_result(result)
            with self.subTest(field=field, change="missing_lower"):
                self.assert_post_blocked(before, event, result, status="NO_DATA")
            result = deepcopy(real)
            result["state"]["wa_records"][0][field]["extra"] = 0.0
            self.reseal_result(result)
            with self.subTest(field=field, change="extra_field"):
                self.assert_post_blocked(before, event, result)

    def test_width_negative_wrong_or_nonnumeric_is_blocked(self):
        before, event = self.case(1)
        real = self.prior(before, event)
        for width in (math.nextafter(0.0, -math.inf), .123, True, "0.135", None):
            result = deepcopy(real)
            result["state"]["wa_records"][0]["wa_interval"]["width"] = width
            self.reseal_result(result)
            with self.subTest(width=width):
                self.assert_post_blocked(before, event, result)

    def test_false_harmony_alert_must_be_numeric_and_copy_the_wa_record(self):
        before, event = self.case(2)
        real = self.prior(before, event)
        for interval in ({"lower": .1, "upper": .2}, {"lower": False, "upper": .1},
                         {"lower": -.1, "upper": .1}, {"lower": .2, "upper": .1}):
            result = deepcopy(real)
            result["state"]["false_harmony_records"][0]["alert_interval"] = interval
            self.reseal_result(result)
            with self.subTest(interval=interval):
                self.assert_post_blocked(before, event, result)

    def test_successful_raw_profile_numeric_string_is_blocked_after_native_normalizes(self):
        before, event = self.case()
        event["payload"]["profiles"][0]["positive_intervals"]["inclusion"]["lower"] = "0.8"
        self.reseal_event(event)
        original = self.prior(before, event)
        self.assertEqual(original["status"], "APPLIED")
        self.assertIs(type(original["state"]["profiles"][0]["positive_intervals"]["inclusion"]["lower"]), float)
        for state in (before, original["state"]):
            with self.subTest(phase=state["current_phase"]):
                with patch.object(kernel, "apply_wa_event", wraps=kernel.apply_wa_event) as native:
                    with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                        guard.checked_apply_wa_numeric_event(state, event)
                self.assertEqual(caught.exception.status, "BLOCKED")
                self.assertIn("event", str(caught.exception))
                self.assertEqual(native.call_count, 1)

    def test_replay_numeric_bool_cannot_hide_in_a_resealed_history(self):
        before, event = self.case()
        result = self.prior(before, event)
        event["payload"]["profiles"][0]["alert_intervals"]["coercive_conformity"]["lower"] = False
        self.reseal_event(event)
        replay_state = result["state"]
        replay_state["processed_event_digests"][-1] = event["wa_event_digest"]
        replay_state["event_history"][-1]["wa_event_digest"] = event["wa_event_digest"]
        self.reseal_state(replay_state)
        self.assertEqual(self.prior(replay_state, event)["status"], "REPLAYED")
        with self.assertRaises(guard.WaNumericBoundaryError):
            guard.checked_apply_wa_numeric_event(replay_state, event)

    def test_nonfinite_and_nonbuiltin_json_inputs_fail_before_prior(self):
        class CustomDict(dict):
            def __deepcopy__(self, memo):
                raise AssertionError("no user hook")
        class CustomFloat(float):
            pass
        before, event = self.case()
        cycle = []
        cycle.append(cycle)
        for bad in (float("nan"), float("inf"), float("-inf"), CustomDict(), CustomFloat(.5), (1,), cycle):
            malformed = deepcopy(event)
            malformed["extra"] = bad
            with self.subTest(kind=type(bad).__name__):
                self.assert_pre_blocked(before, malformed)

    def test_missing_prerequisites_report_no_data(self):
        before, event = self.case()
        for name in ("_finite_json", "_fingerprint", "checked_apply_mediator_event"):
            with self.subTest(name=name), patch.object(guard, name, None):
                with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                    guard.checked_apply_wa_numeric_event(before, event)
                self.assertEqual(caught.exception.status, "NO_DATA")

    def test_prior_failure_preserves_status_and_diagnostics_without_retry(self):
        before, event = self.case()
        for status in ("BLOCKED", "NO_DATA"):
            error = mediator.MediatorTransitionError(status, ("known-prior-issue",))
            with self.subTest(status=status), patch.object(guard, "checked_apply_mediator_event", side_effect=error) as prior:
                with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                    guard.checked_apply_wa_numeric_event(before, event)
                self.assertEqual(caught.exception.status, status)
                self.assertIn("known-prior-issue", str(caught.exception))
                self.assertEqual(prior.call_count, 1)
        with patch.object(guard, "checked_apply_mediator_event", side_effect=RuntimeError("unexpected")) as prior:
            with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                guard.checked_apply_wa_numeric_event(before, event)
            self.assertEqual(caught.exception.status, "BLOCKED")
            self.assertEqual(prior.call_count, 1)

    def test_prior_argument_mutation_cannot_hide_behind_numeric_equality(self):
        before, event = self.case()
        real = self.prior(before, event)
        fingerprint = _fingerprint([before, event])
        def mutating(name, state_copy, event_copy):
            event_copy["event_index"] = float(event_copy["event_index"])
            return deepcopy(real)
        with patch.object(guard, "checked_apply_mediator_event", side_effect=mutating) as prior:
            with self.assertRaises(guard.WaNumericBoundaryError) as caught:
                guard.checked_apply_wa_numeric_event(before, event)
            self.assertIn("argument_mutated", str(caught.exception))
            self.assertEqual(prior.call_count, 1)
        self.assertEqual(_fingerprint([before, event]), fingerprint)

    def test_result_status_or_state_cannot_skip_the_numeric_gate(self):
        before, event = self.case()
        real = self.prior(before, event)
        for status in (None, "PASS", True, 1, []):
            result = deepcopy(real)
            result["status"] = status
            with self.subTest(status=status), patch.object(guard, "checked_apply_mediator_event", return_value=result):
                with self.assertRaises(guard.WaNumericBoundaryError):
                    guard.checked_apply_wa_numeric_event(before, event)
        result = deepcopy(real)
        result["state"]["weights"]["inclusion"] = float("nan")
        with patch.object(guard, "checked_apply_mediator_event", return_value=result):
            with self.assertRaises(guard.WaNumericBoundaryError):
                guard.checked_apply_wa_numeric_event(before, event)


if __name__ == "__main__":
    unittest.main()
