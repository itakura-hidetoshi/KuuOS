"""Real Plural/Wa traces and fail-closed transition-boundary regressions.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_mediator_transition_v0_12 as guard
from runtime import kuuos_decision_os_kernel_v0_1 as decision
from runtime import kuuos_decision_os_plural_kernel_v0_2 as plural
from runtime import kuuos_decision_os_plural_types_v0_2 as plural_types
from runtime import kuuos_decision_os_wa_kernel_v0_3 as wa
from runtime import kuuos_decision_os_wa_types_v0_3 as wa_types
from runtime import v01_decision_os_relational_deliberation as decision_fixture
from runtime import v02_decision_os_plural_harmony_appeal as plural_fixture
from runtime import v03_decision_os_wa_relational_harmony as wa_fixture
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint


class _MemoryStore:
    """Use real native fixture construction without filesystem persistence."""

    def __init__(self, state, apply):
        self.state = deepcopy(state)
        self.apply_original = apply
        self.pairs = []

    def apply(self, event):
        self.pairs.append((deepcopy(self.state), deepcopy(event)))
        result = self.apply_original(self.state, event)
        if result["status"] == "APPLIED":
            self.state = deepcopy(result["state"])
        return result


def _native_traces():
    initial = decision_fixture._initial("mediator-transition-v012")
    store = _MemoryStore(initial, decision.apply_decision_event)
    source, _ = decision_fixture._complete_cycle(
        store, initial,
        options=[
            decision_fixture._option(
                option_id="option-a", action_class="exploit",
                positive=(.86, .94), negative=(.04, .10), information_gain=(.3, .45)),
            decision_fixture._option(
                option_id="option-b", action_class="observe",
                positive=(.38, .52), negative=(.28, .38), information_gain=(.45, .58)),
        ], challenge=decision_fixture._challenge(), middle_way=decision_fixture._middle(),
        tick_base=10, requested_route="SELECT_CANDIDATE",
    )
    initial_plural = plural.build_initial_plural_state(
        source_decision_state=source, plural_id="plural-v012", lineage_id=source["lineage_id"],
        thresholds=plural_fixture.PLURAL_THRESHOLDS, now_ms=10_000,
    )
    pstore = _MemoryStore(initial_plural, plural.apply_plural_event)
    committed_plural, _ = plural_fixture._complete_plural_cycle(
        store=pstore, state=initial_plural, stakeholders=plural_fixture._stakeholders(),
        tick_base=10, requested_route="CONSENSUS_CANDIDATE",
    )
    initial_wa = wa.build_initial_wa_state(
        wa_id="wa-v012", source_plural_state=committed_plural, weights=wa_fixture.WA_WEIGHTS,
        thresholds=wa_fixture.WA_THRESHOLDS, now_ms=30_000,
    )
    wstore = _MemoryStore(initial_wa, wa.apply_wa_event)
    wa_fixture._complete_wa_cycle(
        wstore, initial_wa,
        profiles=[wa_fixture._profile(committed_plural, option_id, positive_lower=.8,
                                     positive_upper=.9)
                  for option_id in committed_plural["source_option_ids"]],
        tick_base=10, requested_route="ENDORSE",
    )
    return {
        "DecisionOSPlural": ("plural", plural, plural_types, pstore),
        "DecisionOSWa": ("wa", wa, wa_types, wstore),
    }


class MediatorTransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traces = _native_traces()

    def case(self, name, index=0):
        stem, kernel, types, store = self.traces[name]
        before, event = deepcopy(store.pairs[index])
        return stem, kernel, types, before, event

    def digest(self, types, stem, kind, value):
        prefix = "wa_" if stem == "wa" else ""
        return getattr(types, prefix + kind + "_digest")(value)

    def reseal_event(self, types, stem, event):
        event[stem + "_event_digest"] = self.digest(types, stem, "event", event)
        return event

    def reseal_result(self, types, stem, result):
        state = result["state"]
        state[stem + "_state_digest"] = self.digest(types, stem, "state", state)
        result["result_" + stem + "_state_digest"] = state[stem + "_state_digest"]
        result[stem + "_apply_result_digest"] = self.digest(types, stem, "apply_result", result)
        return result

    def checked(self, name, before, event):
        return guard.checked_apply_mediator_event(name, before, event)

    def assert_blocked_result(self, name, before, event, result, *, status="BLOCKED"):
        stem, kernel, _, _ = self.traces[name]
        with patch.object(kernel, "apply_" + stem + "_event", return_value=result) as native:
            with self.assertRaises(guard.MediatorTransitionError) as caught:
                self.checked(name, before, event)
        self.assertEqual(native.call_count, 1)
        self.assertEqual(caught.exception.status, status)
        self.assertIs(type(caught.exception.issues), tuple)
        self.assertTrue(caught.exception.issues)
        return caught.exception

    def test_fixed_two_names_and_no_arbitrary_import(self):
        self.assertEqual(guard.MEDIATOR_OS_NAMES, ("DecisionOSPlural", "DecisionOSWa"))
        for name in ("DecisionOS", "Plural", "runtime.fake", "", None, True, []):
            with self.subTest(name=name), patch.object(guard, "import_module") as imported:
                with self.assertRaises(guard.MediatorTransitionError) as caught:
                    self.checked(name, {}, {})
                self.assertEqual(caught.exception.status, "BLOCKED")
                imported.assert_not_called()

    def test_all_real_phases_preserve_native_result_and_call_once(self):
        self.assertEqual([len(item[3].pairs) for item in self.traces.values()], [8, 6])
        for name, (stem, kernel, _, store) in self.traces.items():
            original = getattr(kernel, "apply_" + stem + "_event")
            for before, event in store.pairs:
                with self.subTest(name=name, phase=event["target_phase"]):
                    expected = original(before, event)
                    with patch.object(kernel, "apply_" + stem + "_event", wraps=original) as native:
                        actual = self.checked(name, before, event)
                    self.assertEqual(native.call_count, 1)
                    self.assertEqual(actual["status"], "APPLIED")
                    self.assertEqual(_fingerprint(actual), _fingerprint(expected))

    def test_real_replays_preserve_old_predecessor_event(self):
        for name, (stem, kernel, _, store) in self.traces.items():
            original = getattr(kernel, "apply_" + stem + "_event")
            for _, event in store.pairs:
                with self.subTest(name=name, index=event["event_index"]):
                    expected = original(store.state, event)
                    self.assertEqual(expected["status"], "REPLAYED")
                    self.assertEqual(self.checked(name, store.state, event), expected)

    def test_real_rejections_and_missing_event_digest_preserve_native_status(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            for change in ("phase", "payload", "digest"):
                malformed = deepcopy(event)
                if change == "phase":
                    malformed["target_phase"] = "commit"
                    self.reseal_event(types, stem, malformed)
                elif change == "payload":
                    malformed["payload"] = {}
                    self.reseal_event(types, stem, malformed)
                else:
                    malformed.pop(stem + "_event_digest")
                with self.subTest(name=name, change=change):
                    expected = getattr(kernel, "apply_" + stem + "_event")(before, malformed)
                    self.assertEqual(expected["status"], "REJECTED")
                    self.assertEqual(self.checked(name, before, malformed), expected)

    def test_genuine_appeal_and_veto_records_preserve_variable_length(self):
        _, _, _, initial, _ = self.case("DecisionOSPlural")
        store = _MemoryStore(initial, plural.apply_plural_event)
        appeals = [plural_fixture._appeal(
            appeal_id="appeal-v012", stakeholder_id="patient", target_option_id="option-a",
            materiality=.8)]
        plural_fixture._complete_plural_cycle(
            store=store, state=initial,
            stakeholders=plural_fixture._stakeholders(patient_veto=[
                plural_fixture._veto("option-b", plural_fixture.MISSION_SAFETY, "v012")]),
            appeals=appeals, requested_route="APPEAL", tick_base=30,
        )
        self.assertEqual(len(store.state["appeal_history"]), 1)
        self.assertEqual(len(store.state["validated_veto_records"]), 1)
        for before, event in store.pairs:
            self.assertEqual(self.checked("DecisionOSPlural", before, event),
                             plural.apply_plural_event(before, event))

    def test_caller_inputs_and_returned_state_do_not_alias(self):
        for name in self.traces:
            _, _, _, before, event = self.case(name)
            original = _fingerprint([before, event])
            result = self.checked(name, before, event)
            result["state"]["event_history"].clear()
            result["errors"].append("caller-local")
            self.assertEqual(_fingerprint([before, event]), original)

    def test_missing_inputs_are_no_data_before_original(self):
        for name in self.traces:
            stem, kernel, _, before, event = self.case(name)
            for left, right in ((None, event), (before, None)):
                with self.subTest(name=name), patch.object(kernel, "apply_" + stem + "_event") as native:
                    with self.assertRaises(guard.MediatorTransitionError) as caught:
                        self.checked(name, left, right)
                    self.assertEqual(caught.exception.status, "NO_DATA")
                    native.assert_not_called()

    def test_missing_runtime_prerequisites_are_no_data(self):
        _, _, _, before, event = self.case("DecisionOSPlural")
        for target in ("_finite_json", "_fingerprint"):
            with self.subTest(target=target), patch.object(guard, target, None):
                with self.assertRaises(guard.MediatorTransitionError) as caught:
                    self.checked("DecisionOSPlural", before, event)
                self.assertEqual(caught.exception.status, "NO_DATA")
        with patch.object(guard, "import_module", side_effect=ImportError("missing dependency")):
            with self.assertRaises(guard.MediatorTransitionError) as caught:
                self.checked("DecisionOSPlural", before, event)
            self.assertEqual(caught.exception.status, "NO_DATA")
        with patch.object(plural, "apply_plural_event", None):
            with self.assertRaises(guard.MediatorTransitionError) as caught:
                self.checked("DecisionOSPlural", before, event)
            self.assertEqual(caught.exception.status, "NO_DATA")

    def test_nonfinite_nonbuiltin_cycles_and_budget_are_blocked(self):
        class CustomDict(dict):
            def __deepcopy__(self, memo):
                raise AssertionError("user hook must not run")
        class CustomInt(int):
            pass
        cycle = []
        cycle.append(cycle)
        _, kernel, _, before, event = self.case("DecisionOSPlural")
        for bad in (float("nan"), float("inf"), float("-inf"), CustomDict(), CustomInt(1),
                    (1,), {1: "not-json-key"}, cycle, "x" * 4_000_001):
            malformed = deepcopy(event)
            malformed["extra"] = bad
            with self.subTest(kind=type(bad).__name__), patch.object(kernel, "apply_plural_event") as native:
                with self.assertRaises(guard.MediatorTransitionError) as caught:
                    self.checked("DecisionOSPlural", before, malformed)
                self.assertEqual(caught.exception.status, "BLOCKED")
                native.assert_not_called()

    def test_pre_state_native_validation_runs_before_original(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            before["route"] = "not-a-route"
            before[stem + "_state_digest"] = self.digest(types, stem, "state", before)
            with self.subTest(name=name), patch.object(kernel, "apply_" + stem + "_event") as native:
                with self.assertRaises(guard.MediatorTransitionError):
                    self.checked(name, before, event)
                native.assert_not_called()

    def test_strict_pre_state_counters_and_flags(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            count = "completed_plural_deliberations" if stem == "plural" else "completed_wa_reviews"
            changes = [(field, value) for field in ("event_index", "updated_at_ms", stem + "_version", count)
                       for value in (True, 0.0, "0")]
            changes += [("pending_replan_activation", 0), ("non_authority", {
                key: 0 for key in before["non_authority"]}), ("boundary", {
                key: 1 for key in before["boundary"]})]
            for field, value in changes:
                altered = deepcopy(before)
                altered[field] = value
                altered[stem + "_state_digest"] = self.digest(types, stem, "state", altered)
                with self.subTest(name=name, field=field, value=value), patch.object(
                        kernel, "apply_" + stem + "_event") as native:
                    with self.assertRaises(guard.MediatorTransitionError):
                        self.checked(name, altered, event)
                    native.assert_not_called()

    def test_native_validators_check_before_and_after_even_with_forged_apply(self):
        for name in self.traces:
            stem, kernel, _, before, event = self.case(name)
            result = getattr(kernel, "apply_" + stem + "_event")(before, event)
            with self.subTest(name=name), patch.object(
                    kernel, "validate_" + stem + "_state", side_effect=[[], ["post_state_invalid"]]) as validate:
                error = self.assert_blocked_result(name, before, event, result)
                self.assertIn("post_state", str(error))
                self.assertEqual(validate.call_count, 2)

    def test_mutating_or_malformed_native_validator_is_blocked(self):
        _, _, _, before, event = self.case("DecisionOSPlural")
        def mutating(state):
            state["event_index"] = 0.0
            return []
        for validator in (mutating, lambda state: None, lambda state: [True]):
            with self.subTest(validator=validator), patch.object(plural, "validate_plural_state", validator):
                with self.assertRaises(guard.MediatorTransitionError):
                    self.checked("DecisionOSPlural", before, event)
        self.assertIs(type(before["event_index"]), int)

    def test_original_exception_is_reported_and_caller_inputs_unchanged(self):
        for name in self.traces:
            stem, kernel, _, before, event = self.case(name)
            fingerprint = _fingerprint([before, event])
            with self.subTest(name=name), patch.object(kernel, "apply_" + stem + "_event",
                                                      side_effect=RuntimeError("original failure")) as native:
                with self.assertRaises(guard.MediatorTransitionError) as caught:
                    self.checked(name, before, event)
                self.assertIn("original_apply_raised", str(caught.exception))
                self.assertEqual(native.call_count, 1)
            self.assertEqual(_fingerprint([before, event]), fingerprint)

    def test_original_argument_mutation_cannot_hide_behind_python_equality(self):
        for name in self.traces:
            stem, kernel, _, before, event = self.case(name)
            result = getattr(kernel, "apply_" + stem + "_event")(before, event)
            for argument in ("state", "event"):
                def mutating(state_copy, event_copy):
                    (state_copy if argument == "state" else event_copy)["event_index"] = float(
                        (state_copy if argument == "state" else event_copy)["event_index"])
                    return deepcopy(result)
                fingerprint = _fingerprint([before, event])
                with self.subTest(name=name, argument=argument), patch.object(
                        kernel, "apply_" + stem + "_event", side_effect=mutating) as native:
                    with self.assertRaises(guard.MediatorTransitionError) as caught:
                        self.checked(name, before, event)
                    self.assertIn("argument_mutated", str(caught.exception))
                    self.assertEqual(native.call_count, 1)
                self.assertEqual(_fingerprint([before, event]), fingerprint)

    def test_exact_envelope_keys_and_missing_fields(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            self.assertEqual(len(real), 8)
            for field in real:
                result = deepcopy(real)
                result.pop(field)
                with self.subTest(name=name, missing=field):
                    self.assert_blocked_result(name, before, event, result, status="NO_DATA")
            result = deepcopy(real)
            result["extra"] = True
            self.reseal_result(types, stem, result)
            self.assert_blocked_result(name, before, event, result)

    def test_result_status_cannot_be_null_unknown_or_nonstring(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            for status in (None, "", "PASS", "BLOCKED", True, 1, []):
                result = deepcopy(real)
                result["status"] = status
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, status=status):
                    self.assert_blocked_result(name, before, event, result)

    def test_version_errors_and_result_digest_are_checked(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            for field, value in (("version", "other-version"), ("errors", None),
                                 ("errors", [True]), ("errors", ["error-on-success"])):
                result = deepcopy(real)
                result[field] = value
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, field=field, value=value):
                    self.assert_blocked_result(name, before, event, result)
            result = deepcopy(real)
            result[stem + "_apply_result_digest"] = "0" * 64
            self.assert_blocked_result(name, before, event, result)

    def test_coherent_packet_hash_does_not_hide_wrong_bindings(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            fields = (stem + "_event_digest", "predecessor_" + stem + "_state_digest",
                      "result_" + stem + "_state_digest")
            for field in fields:
                for value in (None, "", "0" * 64):
                    result = deepcopy(real)
                    result[field] = value
                    result[stem + "_apply_result_digest"] = self.digest(types, stem, "apply_result", result)
                    with self.subTest(name=name, field=field, value=value):
                        self.assert_blocked_result(name, before, event, result)

    def test_native_success_with_numeric_event_aliases_is_blocked(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            mutations = [("event_index", True), ("event_index", 1.0),
                         ("created_at_ms", float(event["created_at_ms"]) + .75),
                         ("created_at_ms", str(event["created_at_ms"]))]
            for field, value in mutations:
                malformed = deepcopy(event)
                malformed[field] = value
                self.reseal_event(types, stem, malformed)
                with self.subTest(name=name, field=field, value=value):
                    original = getattr(kernel, "apply_" + stem + "_event")(before, malformed)
                    self.assertEqual(original["status"], "APPLIED")
                    with self.assertRaises(guard.MediatorTransitionError):
                        self.checked(name, before, malformed)

    def test_native_success_with_numeric_authority_flags_is_blocked(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            event["non_authority"]["truth_authority_granted"] = 0
            self.reseal_event(types, stem, event)
            with self.subTest(name=name):
                self.assertEqual(getattr(kernel, "apply_" + stem + "_event")(before, event)["status"], "APPLIED")
                with self.assertRaises(guard.MediatorTransitionError):
                    self.checked(name, before, event)

    def test_native_wa_commit_numeric_booleans_and_nested_authority_are_blocked(self):
        stem, kernel, types, before, event = self.case("DecisionOSWa", -1)
        for field in ("future_only", "memory_overwrite", "wa_not_truth", "wa_not_execution", "wa_not_moral_veto", "non_authority"):
            malformed = deepcopy(event)
            malformed["payload"][field] = ({key: 0 for key in malformed["payload"][field]}
                if field == "non_authority" else int(malformed["payload"][field]))
            self.reseal_event(types, stem, malformed)
            with self.subTest(field=field):
                self.assertEqual(kernel.apply_wa_event(before, malformed)["status"], "APPLIED")
                with self.assertRaises(guard.MediatorTransitionError):
                    self.checked("DecisionOSWa", before, malformed)

    def test_replay_body_or_identity_substitution_is_blocked(self):
        for name in self.traces:
            stem, kernel, _, before, event = self.case(name)
            after = getattr(kernel, "apply_" + stem + "_event")(before, event)["state"]
            for field, value in (("payload", {"forged": True}), (stem + "_id", "another"),
                                 ("lineage_id", "another"), ("version", None), ("event_index", True)):
                forged = deepcopy(event)
                forged[field] = value
                with self.subTest(name=name, field=field):
                    self.assertEqual(getattr(kernel, "apply_" + stem + "_event")(after, forged)["status"], "REPLAYED")
                    with self.assertRaises(guard.MediatorTransitionError):
                        self.checked(name, after, forged)

    def test_replay_requires_actual_processed_membership(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            result = getattr(kernel, "apply_" + stem + "_event")(before, event)
            result["status"] = "REPLAYED"
            result["state"] = deepcopy(before)
            self.reseal_result(types, stem, result)
            self.assert_blocked_result(name, before, event, result)

    def test_rejected_and_replayed_state_must_be_canonically_unchanged(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            before["local_annotation"] = {"tag": True}
            before[stem + "_state_digest"] = self.digest(types, stem, "state", before)
            event["expected_" + stem + "_state_digest"] = before[stem + "_state_digest"]
            self.reseal_event(types, stem, event)
            after = getattr(kernel, "apply_" + stem + "_event")(before, event)["state"]
            for status in ("REPLAYED", "REJECTED"):
                base = after if status == "REPLAYED" else before
                malformed = deepcopy(event)
                if status == "REJECTED":
                    malformed["target_phase"] = "unknown"
                    self.reseal_event(types, stem, malformed)
                result = getattr(kernel, "apply_" + stem + "_event")(base, malformed)
                self.assertEqual(result["status"], status)
                result["state"]["local_annotation"]["tag"] = 1
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, status=status):
                    self.assert_blocked_result(name, base, malformed, result)

    def test_applied_cannot_change_identity_sources_settings_or_other_phase_fields(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name, 1)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            source_key = "source_decision_state_digest" if stem == "plural" else "source_plural_state_digest"
            changes = ((stem + "_id", "changed"), ("lineage_id", "changed"),
                       (source_key, "changed"), ("mission_contract_digest", "changed"),
                       ("thresholds", dict(before["thresholds"], minimum_support_weight=.8) if stem == "plural"
                        else dict(before["thresholds"], minimum_wa_floor=.1)),
                       ("unexpected_added_field", True))
            if stem == "plural":
                changes += (("source_binding_receipt_digest", "changed-after-registration"),)
            for field, value in changes:
                result = deepcopy(real)
                result["state"][field] = value
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, field=field):
                    self.assert_blocked_result(name, before, event, result)

    def test_plural_registration_receipt_is_bound_to_event_payload(self):
        stem, kernel, types, before, event = self.case("DecisionOSPlural")
        result = kernel.apply_plural_event(before, event)
        self.assertNotEqual(before["source_binding_receipt_digest"], result["state"]["source_binding_receipt_digest"])
        result["state"]["source_binding_receipt_digest"] = "other-receipt"
        self.reseal_result(types, stem, result)
        self.assert_blocked_result("DecisionOSPlural", before, event, result)

    def test_phase_index_time_and_state_predecessor_bind_to_actual_event(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            for field, value in (("current_phase", before["current_phase"]),
                                 ("event_index", 0), ("updated_at_ms", event["created_at_ms"] + 1),
                                 ("predecessor_" + stem + "_state_digest", "other")):
                result = deepcopy(real)
                result["state"][field] = value
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, field=field):
                    self.assert_blocked_result(name, before, event, result)

    def test_history_prefix_and_exact_six_field_append_cannot_be_resealed_away(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name, 1)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            for change in ("prefix", "artifact", "extra", "float_index", "processed", "no_append"):
                result = deepcopy(real)
                state = result["state"]
                if change == "prefix":
                    state["event_history"][0]["artifact_digest"] = "altered-old-artifact"
                elif change == "artifact":
                    state["event_history"][-1]["artifact_digest"] = "altered-new-artifact"
                elif change == "extra":
                    state["event_history"][-1]["extra"] = True
                elif change == "float_index":
                    state["event_history"][-1]["event_index"] = float(event["event_index"])
                elif change == "processed":
                    state["processed_event_digests"][-1] = "different-event"
                else:
                    state["event_history"] = deepcopy(before["event_history"])
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, change=change):
                    self.assert_blocked_result(name, before, event, result)

    def test_commit_counter_summary_and_committed_digest_bindings(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name, -1)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            count = "completed_plural_deliberations" if stem == "plural" else "completed_wa_reviews"
            for change in ("version", "count", "summary_count", "summary_field", "summary_extra", "commit_digest"):
                result = deepcopy(real)
                state = result["state"]
                if change == "version":
                    state[stem + "_version"] = 99
                elif change == "count":
                    state[count] = 99
                elif change == "summary_count":
                    state[stem + "_summaries"] = []
                elif change == "summary_field":
                    state[stem + "_summaries"][-1]["commit_event_digest"] = "other-event"
                elif change == "summary_extra":
                    state[stem + "_summaries"][-1]["extra"] = True
                else:
                    state["latest_committed_" + stem + "_digest"] = "other-commit"
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, change=change):
                    self.assert_blocked_result(name, before, event, result)

    def test_commit_fields_cannot_change_in_other_phases(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            result = getattr(kernel, "apply_" + stem + "_event")(before, event)
            result["state"]["latest_committed_" + stem + "_digest"] = "premature-commit"
            self.reseal_result(types, stem, result)
            self.assert_blocked_result(name, before, event, result)

    def test_appeal_append_must_match_count_identity_and_keep_prefix(self):
        stem, kernel, types, before, event = self.case("DecisionOSPlural", 5)
        event["payload"]["appeals"] = [plural_fixture._appeal(
            appeal_id="new-appeal", stakeholder_id="patient", target_option_id="option-a", materiality=.2)]
        self.reseal_event(types, stem, event)
        original = kernel.apply_plural_event(before, event)
        self.assertEqual(original["status"], "APPLIED")
        for change in ("drop", "identity", "future_only", "prior_rewrite", "materiality", "material"):
            result = deepcopy(original)
            history = result["state"]["appeal_history"]
            if change == "drop":
                history.clear()
            elif change == "identity":
                history[-1]["appeal_id"] = "other-appeal"
            elif change == "future_only":
                history[-1]["future_only"] = 1
            elif change == "prior_rewrite":
                history[-1]["rewrites_prior_decision"] = True
            elif change == "materiality":
                history[-1]["materiality"] = .99
            else:
                history[-1]["material"] = not history[-1]["material"]
            self.reseal_result(types, stem, result)
            with self.subTest(change=change):
                self.assert_blocked_result("DecisionOSPlural", before, event, result)

    def test_post_state_authority_booleans_and_wa_selection_identity(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name, -2)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            for change in ("non_authority", "boundary", "pending_replan_activation"):
                result = deepcopy(real)
                if change == "pending_replan_activation":
                    result["state"][change] = int(result["state"][change])
                else:
                    first = next(iter(result["state"][change]))
                    result["state"][change][first] = int(result["state"][change][first])
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, field=change):
                    self.assert_blocked_result(name, before, event, result)
            if stem == "wa":
                result = deepcopy(real)
                result["state"]["endorsed_option_ids"] = ["not-a-source-option"]
                self.reseal_result(types, stem, result)
                self.assert_blocked_result(name, before, event, result)

    def test_non_json_native_result_and_missing_cached_digest_fail_closed(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            result = deepcopy(real)
            result["state"][stem + "_state_digest"] = None
            result[stem + "_apply_result_digest"] = self.digest(types, stem, "apply_result", result)
            self.assert_blocked_result(name, before, event, result)
            result = deepcopy(real)
            result["state"]["extra"] = float("nan")
            self.assert_blocked_result(name, before, event, result)
            self.assert_blocked_result(name, before, event, [])

    def test_registered_records_bind_to_actual_payload_not_only_resealed_state(self):
        for name in self.traces:
            stem, kernel, types, before, event = self.case(name)
            real = getattr(kernel, "apply_" + stem + "_event")(before, event)
            field = "stakeholders" if stem == "plural" else "profiles"
            for change in ("empty", "identity", "boolean", "content"):
                result = deepcopy(real)
                records = result["state"][field]
                if change == "empty":
                    records.clear()
                elif change == "identity":
                    records[0]["stakeholder_id" if stem == "plural" else "option_id"] = "not-from-event"
                elif change == "boolean":
                    records[0]["appeal_right" if stem == "plural" else "minority_preserved"] = False
                else:
                    records[0]["role" if stem == "plural" else "dialogue_receipt_digest"] = "other-content"
                if stem == "plural":
                    result["state"]["stakeholder_registry_digest"] = types.sha(records)
                elif records:
                    records[0]["wa_profile_digest"] = types.sha({
                        key: value for key, value in records[0].items() if key != "wa_profile_digest"})
                self.reseal_result(types, stem, result)
                with self.subTest(name=name, change=change):
                    self.assert_blocked_result(name, before, event, result)

    def test_wa_profile_cached_digest_and_record_source_binding_are_required(self):
        stem, kernel, types, before, event = self.case("DecisionOSWa", 1)
        real = kernel.apply_wa_event(before, event)
        for change in ("profile_digest", "record_digest", "record_source", "drop_record"):
            result = deepcopy(real)
            state = result["state"]
            if change == "profile_digest":
                state["profiles"][0]["wa_profile_digest"] = None
            elif change == "record_digest":
                state["wa_records"][0]["wa_profile_digest"] = "other-profile"
            elif change == "record_source":
                state["wa_records"][0]["option_digest"] = "other-option"
            else:
                state["wa_records"].clear()
            self.reseal_result(types, stem, result)
            with self.subTest(change=change):
                self.assert_blocked_result("DecisionOSWa", before, event, result)

    def test_veto_claims_cannot_acquire_nested_authority(self):
        stem, kernel, types, before, event = self.case("DecisionOSPlural")
        event["payload"]["stakeholders"][0]["veto"] = [plural_fixture._veto(
            "option-b", plural_fixture.MISSION_SAFETY, "nested-authority")]
        self.reseal_event(types, stem, event)
        first = kernel.apply_plural_event(before, event)
        for value in (True, 0):
            result = deepcopy(first)
            result["state"]["stakeholders"][0]["veto"][0]["raw_veto_grants_authority"] = value
            result["state"]["stakeholder_registry_digest"] = types.sha(result["state"]["stakeholders"])
            self.reseal_result(types, stem, result)
            with self.subTest(value=value):
                self.assert_blocked_result("DecisionOSPlural", before, event, result)

    def test_normalization_helpers_cannot_mutate_adapter_arguments(self):
        stem, kernel, _, before, event = self.case("DecisionOSWa")
        real = kernel.apply_wa_event(before, event)
        original = kernel._normalize_profile
        def mutating(state, raw):
            normalized = original(state, raw)
            raw["minority_preserved"] = 1
            return normalized
        with patch.object(kernel, "_normalize_profile", mutating):
            self.assert_blocked_result("DecisionOSWa", before, event, real)

    def test_native_receipt_and_record_normalization_is_preserved(self):
        for index, field in ((0, "source_binding_receipt_digest"), (2, "veto_validation_receipt_digest"),
                             (4, "explanation_receipt_digest"), (5, "appeal_window_receipt_digest")):
            stem, kernel, types, before, event = self.case("DecisionOSPlural", index)
            event["payload"][field] = "  " + event["payload"][field] + "  "
            if index == 0:
                event["payload"]["stakeholders"][0]["role"] = "  affected_person  "
            self.reseal_event(types, stem, event)
            expected = kernel.apply_plural_event(before, event)
            self.assertEqual(expected["status"], "APPLIED")
            with self.subTest(field=field):
                self.assertEqual(self.checked("DecisionOSPlural", before, event), expected)

    def test_forged_success_cannot_bypass_successful_payload_boolean_schema(self):
        cases = (("DecisionOSPlural", -2, "handover_required"),
                 ("DecisionOSWa", 0, "dissent_considered"))
        for name, index, flag in cases:
            stem, kernel, types, before, event = self.case(name, index)
            result = getattr(kernel, "apply_" + stem + "_event")(before, event)
            if stem == "plural":
                event["payload"][flag] = 1
            else:
                event["payload"]["profiles"][0][flag] = 1
            self.reseal_event(types, stem, event)
            self.assertEqual(getattr(kernel, "apply_" + stem + "_event")(before, event)["status"], "REJECTED")
            result[stem + "_event_digest"] = event[stem + "_event_digest"]
            result["state"]["processed_event_digests"][-1] = event[stem + "_event_digest"]
            result["state"]["event_history"][-1][stem + "_event_digest"] = event[stem + "_event_digest"]
            self.reseal_result(types, stem, result)
            with self.subTest(name=name, status="APPLIED"):
                self.assert_blocked_result(name, before, event, result)
            # A resealed supplied history does not make a non-Boolean payload
            # valid merely by changing the declared outcome to REPLAYED.
            replay_state = deepcopy(result["state"])
            replay = deepcopy(result)
            replay["status"] = "REPLAYED"
            replay["predecessor_" + stem + "_state_digest"] = replay_state[stem + "_state_digest"]
            self.reseal_result(types, stem, replay)
            with self.subTest(name=name, status="REPLAYED"):
                self.assert_blocked_result(name, replay_state, event, replay)

    def test_validating_vetoes_preserves_source_claims_and_partition(self):
        stem, kernel, types, initial, _ = self.case("DecisionOSPlural")
        store = _MemoryStore(initial, kernel.apply_plural_event)
        plural_fixture._complete_plural_cycle(
            store=store, state=initial,
            stakeholders=plural_fixture._stakeholders(patient_veto=[
                plural_fixture._veto("option-b", plural_fixture.MISSION_SAFETY, "veto-bind")]),
            requested_route="CONSENSUS_CANDIDATE", tick_base=30,
        )
        before, event = deepcopy(store.pairs[2])
        real = kernel.apply_plural_event(before, event)
        self.assertEqual(len(real["state"]["validated_veto_records"]), 1)
        for change in ("drop_all", "evidence", "partition", "excluded"):
            result = deepcopy(real)
            state = result["state"]
            if change == "drop_all":
                for field in ("veto_records", "validated_veto_records", "unvalidated_veto_records", "veto_excluded_option_ids"):
                    state[field] = []
            elif change == "evidence":
                state["veto_records"][0]["evidence_digest"] = "changed-evidence"
            elif change == "partition":
                state["validated_veto_records"] = []
            else:
                state["veto_excluded_option_ids"] = []
            self.reseal_result(types, stem, result)
            with self.subTest(change=change):
                self.assert_blocked_result("DecisionOSPlural", before, event, result)


if __name__ == "__main__":
    unittest.main()
