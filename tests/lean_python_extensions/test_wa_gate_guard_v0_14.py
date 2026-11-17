"""Native Wa classification, plurality, and gate consistency regressions.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import math
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_wa_gate_guard_v0_14 as guard
from runtime import kuuos_lean_python_wa_numeric_guard_v0_13 as prior
from runtime import kuuos_decision_os_wa_kernel_v0_3 as kernel
from runtime import kuuos_decision_os_wa_types_v0_3 as types
from runtime import v03_decision_os_wa_relational_harmony as fixture
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from tests.lean_python_extensions.test_mediator_transition_v0_12 import _native_traces, _MemoryStore


_BASIS_FIELDS = (
    "wa_id", "source_plural_state_digest", "source_committed_plural_digest",
    "source_plural_decision_basis_digest", "source_decision_basis_digest", "source_route",
    "source_selected_option_id", "source_stakeholder_registry_digest", "source_utility_records_digest",
    "source_veto_records_digest", "source_aggregate_records_digest", "source_appeal_history_digest",
    "wa_records", "false_harmony_records", "plurality", "route", "endorsed_option_ids", "review_option_ids",
)


class WaGateGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        traces = _native_traces()
        cls.source = traces["DecisionOSPlural"][3].state
        cls.normal = traces["DecisionOSWa"][3]

    def trace(self, label, route, *, source_route=None, thresholds=None, weight_delta=0.0,
              only_nonselected=False, **profile_arguments):
        initial = kernel.build_initial_wa_state(
            wa_id="wa-v014-" + label, source_plural_state=self.source,
            weights=fixture.WA_WEIGHTS, thresholds=thresholds or fixture.WA_THRESHOLDS, now_ms=30_000,
        )
        if source_route is not None:
            # Route-map inputs are local native-schema-valid snapshots; this
            # test does not authenticate their external Plural source history.
            initial["source_route"] = source_route
            initial["source_selected_option_id"] = ""
            initial["source_retained_alternative_ids"] = list(reversed(initial["source_option_ids"]))
        initial["weights"]["inclusion"] += weight_delta
        self.seal_state(initial)
        profiles = []
        for option_id in initial["source_option_ids"]:
            arguments = dict(positive_lower=.8, positive_upper=.9)
            if not only_nonselected or option_id != self.source["selected_option_id"]:
                arguments.update(profile_arguments)
            profiles.append(fixture._profile(self.source, option_id, **arguments))
        store = _MemoryStore(initial, kernel.apply_wa_event)
        fixture._complete_wa_cycle(store, initial, profiles=profiles, requested_route=route, tick_base=10)
        return store

    def case(self, index=0, store=None):
        return deepcopy((store or self.normal).pairs[index])

    def seal_state(self, state):
        state["wa_state_digest"] = types.wa_state_digest(state)
        return state

    def seal_result(self, result):
        self.seal_state(result["state"])
        result["result_wa_state_digest"] = result["state"]["wa_state_digest"]
        result["wa_apply_result_digest"] = types.wa_apply_result_digest(result)
        return result

    def seal_basis(self, state):
        state["wa_basis_digest"] = types.sha({field: state[field] for field in _BASIS_FIELDS})
        return self.seal_state(state)

    def event(self, state, target, payload):
        return kernel.build_wa_event(
            state=state, target_phase=target, artifact_digest=types.sha("v014-" + target),
            payload=payload, now_ms=state["updated_at_ms"] + 1,
        )

    def assert_pre_blocked(self, state, event, *, status="BLOCKED"):
        fingerprint = _fingerprint([state, event]) if state is not None and event is not None else None
        with patch.object(guard, "checked_apply_wa_numeric_event", wraps=prior.checked_apply_wa_numeric_event) as numeric:
            with patch.object(kernel, "apply_wa_event", wraps=kernel.apply_wa_event) as native:
                with self.assertRaises(guard.WaGateBoundaryError) as caught:
                    guard.checked_apply_wa_gate_event(state, event)
        numeric.assert_not_called()
        native.assert_not_called()
        self.assertEqual(caught.exception.status, status)
        self.assertIs(type(caught.exception.issues), tuple)
        self.assertTrue(caught.exception.issues)
        if fingerprint is not None:
            self.assertEqual(_fingerprint([state, event]), fingerprint)
        return caught.exception

    def assert_post_blocked(self, state, event, result, *, status="BLOCKED"):
        with patch.object(kernel, "apply_wa_event", return_value=result) as native:
            with patch.object(guard, "checked_apply_wa_numeric_event", wraps=prior.checked_apply_wa_numeric_event) as numeric:
                with self.assertRaises(guard.WaGateBoundaryError) as caught:
                    guard.checked_apply_wa_gate_event(state, event)
        self.assertEqual(numeric.call_count, 1)
        self.assertEqual(native.call_count, 1)
        self.assertEqual(caught.exception.status, status)
        return caught.exception

    def test_resealed_false_classification_can_reach_native_endorse_but_new_pre_gate_blocks(self):
        for label, expected, arguments in (
            ("minority", "ESCALATE", {"minority_preserved": False}),
            ("dissent", "REOBSERVE", {"dissent_considered": False}),
        ):
            store = self.trace(label, expected, **arguments)
            state, _ = self.case(3, store)
            for record in state["false_harmony_records"]:
                record.update(confirmed_false_harmony=False, suspected_false_harmony=False, reason_codes=[])
            self.seal_state(state)
            event = self.event(state, "plurality_check", {"plurality_receipt_digest": types.sha(label)})
            self.assertEqual(kernel.validate_wa_state(state), [])
            advanced = prior.checked_apply_wa_numeric_event(state, event)["state"]
            gate = self.event(advanced, "gate", {"wa_gate_rule_digest": types.sha(label + "-gate")})
            self.assertEqual(prior.checked_apply_wa_numeric_event(advanced, gate)["state"]["route"], "ENDORSE")
            with self.subTest(label=label):
                self.assert_pre_blocked(state, event)
                self.assert_pre_blocked(state, store.pairs[2][1])

    def test_native_low_floor_resealed_endorse_replay_and_commit_are_blocked_before_prior(self):
        store = self.trace("low-floor", "REPAIR", positive_lower=.2, positive_upper=.3)
        state, _ = self.case(5, store)
        state.update(route="ENDORSE", endorsed_option_ids=[state["source_selected_option_id"]],
                     review_option_ids=[], pending_replan_activation=True)
        self.seal_basis(state)
        replay = store.pairs[4][1]
        commit = self.event(state, "commit", store.pairs[5][1]["payload"])
        self.assertEqual(kernel.validate_wa_state(state), [])
        self.assertEqual(prior.checked_apply_wa_numeric_event(state, replay)["status"], "REPLAYED")
        self.assertEqual(prior.checked_apply_wa_numeric_event(state, commit)["state"]["route"], "ENDORSE")
        self.assert_pre_blocked(state, replay)
        self.assert_pre_blocked(state, commit)

    def test_all_six_normal_phases_and_replays_preserve_native_results(self):
        self.assertEqual(len(self.normal.pairs), 6)
        for before, event in self.normal.pairs:
            expected = prior.checked_apply_wa_numeric_event(before, event)
            with self.subTest(phase=event["target_phase"]):
                with patch.object(guard, "checked_apply_wa_numeric_event", wraps=prior.checked_apply_wa_numeric_event) as numeric:
                    with patch.object(kernel, "apply_wa_event", wraps=kernel.apply_wa_event) as native:
                        result = guard.checked_apply_wa_gate_event(before, event)
                self.assertEqual(_fingerprint(result), _fingerprint(expected))
                self.assertEqual(numeric.call_count, 1)
                self.assertEqual(native.call_count, 1)
                replay = guard.checked_apply_wa_gate_event(self.normal.state, event)
                self.assertEqual(replay, prior.checked_apply_wa_numeric_event(self.normal.state, event))
                self.assertEqual(replay["status"], "REPLAYED")

    def test_real_classification_priority_threshold_equality_and_reason_order(self):
        cases = (
            ("confirmed", "ESCALATE", dict(alert_lower=.6, alert_upper=.7, minority_preserved=False, dissent_considered=False),
             True, False, ["confirmed_alert_floor_reached", "minority_not_preserved"]),
            ("suspected", "REOBSERVE", dict(alert_lower=.1, alert_upper=.4, dissent_considered=False),
             False, True, ["alert_upper_reaches_suspicion", "dissent_not_considered"]),
            ("minority-priority", "ESCALATE", dict(minority_preserved=False, dissent_considered=False),
             True, False, ["minority_not_preserved"]),
        )
        for label, route, arguments, confirmed, suspected, reasons in cases:
            store = self.trace(label, route, **arguments)
            row = store.state["false_harmony_records"][0]
            self.assertIs(row["confirmed_false_harmony"], confirmed)
            self.assertIs(row["suspected_false_harmony"], suspected)
            self.assertEqual(row["reason_codes"], reasons)
            for before, event in store.pairs:
                with self.subTest(label=label, phase=event["target_phase"]):
                    self.assertEqual(guard.checked_apply_wa_gate_event(before, event),
                                     prior.checked_apply_wa_numeric_event(before, event))

    def test_all_direct_source_routes_precede_selected_alerts_and_preserve_review_order(self):
        mapping = {"NEGOTIATE": "REOBSERVE", "APPEAL": "REOBSERVE", "HANDOVER": "ESCALATE",
                   "HOLD": "HOLD", "REJECT": "REJECT", "QUARANTINE": "QUARANTINE"}
        for source_route, route in mapping.items():
            store = self.trace(source_route, route, source_route=source_route,
                               positive_lower=.2, positive_upper=.3, alert_lower=.8, alert_upper=.9,
                               minority_preserved=False, dissent_considered=False)
            self.assertEqual(store.state["review_option_ids"], list(reversed(store.state["source_option_ids"])))
            self.assertIs(store.state["pending_replan_activation"], route not in {"REJECT", "QUARANTINE"})
            for before, event in store.pairs:
                with self.subTest(source=source_route, phase=event["target_phase"]):
                    self.assertEqual(guard.checked_apply_wa_gate_event(before, event),
                                     prior.checked_apply_wa_numeric_event(before, event))

    def test_floor_equality_passes_and_one_float_above_requires_repair(self):
        record = self.normal.state["wa_records"][0]
        floors = dict(fixture.WA_THRESHOLDS,
                      minimum_wa_floor=record["wa_interval"]["lower"],
                      minimum_dimension_floor=record["weakest_interval"]["lower"])
        for change, route in ((None, "ENDORSE"), ("minimum_wa_floor", "REPAIR"),
                              ("minimum_dimension_floor", "REPAIR")):
            thresholds = dict(floors)
            if change:
                thresholds[change] = math.nextafter(thresholds[change], math.inf)
            store = self.trace("floor-" + str(change), route, thresholds=thresholds)
            before, event = self.case(4, store)
            with self.subTest(change=change):
                self.assertEqual(guard.checked_apply_wa_gate_event(before, event), prior.checked_apply_wa_numeric_event(before, event))

    def test_nonselected_false_harmony_is_checked_without_vetoing_selected_endorsement(self):
        store = self.trace("nonselected", "ENDORSE", only_nonselected=True, minority_preserved=False)
        for before, event in store.pairs:
            self.assertEqual(guard.checked_apply_wa_gate_event(before, event), prior.checked_apply_wa_numeric_event(before, event))
        before, event = self.case(2, store)
        result = kernel.apply_wa_event(before, event)
        last = result["state"]["false_harmony_records"][-1]
        self.assertNotEqual(last["option_id"], before["source_selected_option_id"])
        last.update(confirmed_false_harmony=False, suspected_false_harmony=False, reason_codes=[])
        self.seal_result(result)
        self.assert_post_blocked(before, event, result)

    def test_forged_classification_output_and_reason_lists_are_blocked(self):
        store = self.trace("classification-tamper", "ESCALATE", alert_lower=.6, alert_upper=.7,
                           minority_preserved=False, dissent_considered=False)
        before, event = self.case(2, store)
        real = kernel.apply_wa_event(before, event)
        for change in ("clear", "both", "reverse_reasons", "drop_reason", "extra_reason", "row_order", "numeric_alias"):
            result = deepcopy(real)
            rows = result["state"]["false_harmony_records"]
            if change == "clear":
                rows[0].update(confirmed_false_harmony=False, suspected_false_harmony=False, reason_codes=[])
            elif change == "both":
                rows[0]["suspected_false_harmony"] = True
            elif change == "reverse_reasons":
                rows[0]["reason_codes"].reverse()
            elif change == "drop_reason":
                rows[0]["reason_codes"].pop()
            elif change == "extra_reason":
                rows[0]["reason_codes"].append("not-a-native-reason")
            elif change == "row_order":
                rows.reverse()
            else:
                rows[0]["confirmed_false_harmony"] = 1
            self.seal_result(result)
            with self.subTest(change=change):
                self.assert_post_blocked(before, event, result)

    def test_plurality_matches_actual_sets_and_digest_presence(self):
        before, event = self.case(3)
        real = kernel.apply_wa_event(before, event)
        for field in real["state"]["plurality"]:
            result = deepcopy(real)
            result["state"]["plurality"][field] = not result["state"]["plurality"][field]
            self.seal_result(result)
            with self.subTest(field=field):
                self.assert_post_blocked(before, event, result)
                self.assert_pre_blocked(result["state"], event)

    def test_actual_profile_and_source_id_mismatches_block_before_prior(self):
        before, event = self.case(4)
        changes = (
            ("profile_missing", lambda s: s["profiles"].pop()),
            ("duplicate_profile", lambda s: s["profiles"].append(deepcopy(s["profiles"][0]))),
            ("source_option", lambda s: s["source_option_ids"].append("unknown")),
            ("retained_option", lambda s: s["source_retained_alternative_ids"].append("unknown")),
            ("selected_option", lambda s: s.update(source_selected_option_id="unknown")),
            ("record_option", lambda s: s["wa_records"][0].update(option_id="unknown")),
            ("profile_digest_binding", lambda s: s["profiles"][0].update(option_digest="other")),
        )
        for label, mutate in changes:
            state = deepcopy(before)
            mutate(state)
            self.seal_state(state)
            with self.subTest(change=label):
                self.assert_pre_blocked(state, event)

    def test_source_presence_and_boolean_aliases_do_not_count_as_evidence(self):
        before, event = self.case(4)
        for field in ("source_stakeholder_registry_digest", "source_utility_records_digest",
                      "source_aggregate_records_digest", "source_veto_records_digest", "source_appeal_history_digest"):
            for value in (None, "", True, 1):
                state = deepcopy(before)
                state[field] = value
                self.seal_state(state)
                with self.subTest(field=field, value=value):
                    self.assert_pre_blocked(state, event)
        for field in before["plurality"]:
            state = deepcopy(before)
            state["plurality"][field] = int(state["plurality"][field])
            self.seal_state(state)
            self.assert_pre_blocked(state, event)

    def test_premature_classification_plurality_route_and_basis_are_blocked(self):
        before, event = self.case(0)
        false_records = deepcopy(self.normal.state["false_harmony_records"])
        for field, value in (
            ("false_harmony_records", false_records),
            ("plurality", deepcopy(self.normal.state["plurality"])),
            ("route", "ENDORSE"), ("endorsed_option_ids", [before["source_selected_option_id"]]),
            ("review_option_ids", list(before["source_option_ids"])),
            ("pending_replan_activation", True), ("wa_basis_digest", "premature"),
        ):
            state = deepcopy(before)
            state[field] = value
            self.seal_state(state)
            with self.subTest(field=field):
                self.assert_pre_blocked(state, event)

    def test_route_lists_pending_and_basis_cannot_be_coherently_resealed(self):
        before, event = self.case(4)
        real = kernel.apply_wa_event(before, event)
        for change in ("route", "review", "pending", "basis", "extra_basis_source"):
            result = deepcopy(real)
            state = result["state"]
            if change == "route":
                state.update(route="REPAIR", endorsed_option_ids=[], review_option_ids=[state["source_selected_option_id"]])
                self.seal_basis(state)
            elif change == "review":
                state["review_option_ids"] = list(state["source_option_ids"])
                self.seal_basis(state)
            elif change == "pending":
                state["pending_replan_activation"] = False
            elif change == "basis":
                state["wa_basis_digest"] = "different-basis"
            else:
                state["wa_basis_digest"] = types.sha({**{field: state[field] for field in _BASIS_FIELDS}, "extra": True})
            self.seal_result(result)
            with self.subTest(change=change):
                self.assert_post_blocked(before, event, result)

    def test_successful_gate_requested_route_is_bound_but_native_rejection_is_preserved(self):
        before, event = self.case(4)
        real = kernel.apply_wa_event(before, event)
        for value in ("REPAIR", True, 1):
            malformed = deepcopy(event)
            malformed["payload"]["requested_route"] = value
            malformed["wa_event_digest"] = types.wa_event_digest(malformed)
            rejected = prior.checked_apply_wa_numeric_event(before, malformed)
            self.assertEqual(rejected["status"], "REJECTED")
            self.assertEqual(guard.checked_apply_wa_gate_event(before, malformed), rejected)
            result = deepcopy(real)
            result["wa_event_digest"] = malformed["wa_event_digest"]
            result["state"]["processed_event_digests"][-1] = malformed["wa_event_digest"]
            result["state"]["event_history"][-1]["wa_event_digest"] = malformed["wa_event_digest"]
            self.seal_result(result)
            with self.subTest(value=value):
                self.assert_post_blocked(before, malformed, result)
        for value in (None, "", "ENDORSE"):
            valid = deepcopy(event)
            valid["payload"]["requested_route"] = value
            valid["wa_event_digest"] = types.wa_event_digest(valid)
            self.assertEqual(guard.checked_apply_wa_gate_event(before, valid), prior.checked_apply_wa_numeric_event(before, valid))

    def test_unchanged_rejected_result_and_missing_event_digest_stay_native(self):
        before, event = self.case()
        for change in ("digest", "phase", "payload"):
            malformed = deepcopy(event)
            if change == "digest":
                malformed.pop("wa_event_digest")
            elif change == "phase":
                malformed["target_phase"] = "commit"
                malformed["wa_event_digest"] = types.wa_event_digest(malformed)
            else:
                malformed["payload"] = {}
                malformed["wa_event_digest"] = types.wa_event_digest(malformed)
            expected = prior.checked_apply_wa_numeric_event(before, malformed)
            self.assertEqual(expected["status"], "REJECTED")
            self.assertEqual(guard.checked_apply_wa_gate_event(before, malformed), expected)

    def test_previous_rounding_boundary_stays_blocked(self):
        store = self.trace("rounding", "ENDORSE", positive_lower=1.0, positive_upper=1.0,
                           alert_lower=0.0, alert_upper=0.0, weight_delta=5e-13)
        before, event = self.case(1, store)
        with patch.object(guard, "checked_apply_wa_numeric_event", wraps=prior.checked_apply_wa_numeric_event) as numeric:
            with self.assertRaises(guard.WaGateBoundaryError) as caught:
                guard.checked_apply_wa_gate_event(before, event)
        self.assertEqual(caught.exception.status, "BLOCKED")
        self.assertEqual(numeric.call_count, 1)
        bad, replay = deepcopy(store.pairs[2][0]), store.pairs[1][1]
        self.assert_pre_blocked(bad, replay)

    def test_in_range_scoring_derivation_remains_an_explicit_unchecked_boundary(self):
        before, event = self.case(1)
        result = kernel.apply_wa_event(before, event)
        result["state"]["wa_records"][0]["weighted_interval"] = {"lower": .25, "upper": .5}
        self.seal_result(result)
        with patch.object(kernel, "apply_wa_event", return_value=result):
            accepted = guard.checked_apply_wa_gate_event(before, event)
        self.assertEqual(accepted, result)
        self.assertEqual(accepted["status"], "APPLIED")

    def test_caller_inputs_and_return_value_do_not_alias(self):
        before, event = self.case()
        fingerprint = _fingerprint([before, event])
        result = guard.checked_apply_wa_gate_event(before, event)
        result["state"]["profiles"].clear()
        self.assertEqual(_fingerprint([before, event]), fingerprint)

    def test_missing_semantic_data_is_no_data_before_prior(self):
        before, event = self.case(4)
        for field in ("current_phase", "source_route", "source_option_ids", "source_selected_option_id",
                      "source_retained_alternative_ids", "source_option_digest_by_id", "plurality", "wa_basis_digest"):
            state = deepcopy(before)
            state.pop(field)
            with self.subTest(field=field):
                self.assert_pre_blocked(state, event, status="NO_DATA")
        for field in before["false_harmony_records"][0]:
            state = deepcopy(before)
            state["false_harmony_records"][0].pop(field)
            with self.subTest(false_harmony_field=field):
                self.assert_pre_blocked(state, event, status="NO_DATA")
        self.assert_pre_blocked(None, event, status="NO_DATA")
        self.assert_pre_blocked(before, None, status="NO_DATA")

    def test_nonfinite_and_nonbuiltin_inputs_never_reach_prior(self):
        class CustomDict(dict):
            def __deepcopy__(self, memo):
                raise AssertionError("no user hook")
        before, event = self.case()
        for bad in (float("nan"), float("inf"), CustomDict(), (1,), {1: "key"}):
            malformed = deepcopy(event)
            malformed["extra"] = bad
            with patch.object(guard, "checked_apply_wa_numeric_event") as numeric:
                with self.assertRaises(guard.WaGateBoundaryError):
                    guard.checked_apply_wa_gate_event(before, malformed)
                numeric.assert_not_called()

    def test_missing_prerequisites_and_prior_errors_are_fail_closed(self):
        before, event = self.case()
        for name in ("_finite_json", "_fingerprint", "_state_numbers", "checked_apply_wa_numeric_event"):
            with self.subTest(name=name), patch.object(guard, name, None):
                with self.assertRaises(guard.WaGateBoundaryError) as caught:
                    guard.checked_apply_wa_gate_event(before, event)
                self.assertEqual(caught.exception.status, "NO_DATA")
        for status in ("BLOCKED", "NO_DATA"):
            with patch.object(guard, "checked_apply_wa_numeric_event",
                              side_effect=prior.WaNumericBoundaryError(status, ("known-prior-issue",))) as numeric:
                with self.assertRaises(guard.WaGateBoundaryError) as caught:
                    guard.checked_apply_wa_gate_event(before, event)
                self.assertEqual(caught.exception.status, status)
                self.assertIn("known-prior-issue", str(caught.exception))
                self.assertEqual(numeric.call_count, 1)

    def test_prior_and_numeric_validator_argument_mutation_are_blocked(self):
        before, event = self.case()
        real = prior.checked_apply_wa_numeric_event(before, event)
        def mutating_prior(state, supplied_event):
            supplied_event["event_index"] = float(supplied_event["event_index"])
            return deepcopy(real)
        with patch.object(guard, "checked_apply_wa_numeric_event", side_effect=mutating_prior):
            with self.assertRaises(guard.WaGateBoundaryError) as caught:
                guard.checked_apply_wa_gate_event(before, event)
            self.assertIn("argument_mutated", str(caught.exception))
        def mutating_validator(state, label):
            state["event_index"] = float(state["event_index"])
        with patch.object(guard, "_state_numbers", mutating_validator):
            self.assert_pre_blocked(before, event)

    def test_unknown_result_status_cannot_skip_post_gate(self):
        before, event = self.case()
        real = prior.checked_apply_wa_numeric_event(before, event)
        for status in (None, "PASS", True, 1):
            result = deepcopy(real)
            result["status"] = status
            with self.subTest(status=status), patch.object(guard, "checked_apply_wa_numeric_event", return_value=result):
                with self.assertRaises(guard.WaGateBoundaryError):
                    guard.checked_apply_wa_gate_event(before, event)


if __name__ == "__main__":
    unittest.main()
