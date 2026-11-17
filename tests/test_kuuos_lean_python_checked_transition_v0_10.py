"""Checks on real native transitions and adversarial boundary substitutions.

Only malformed-output cases replace an original pure kernel. Positive cases
use the existing constructors, kernels, and one bounded local native fixture.
No Lean refinement or external execution authority is inferred.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from importlib import import_module
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_decision_os_kernel_v0_1 as decision
from runtime import kuuos_decision_os_types_v0_1 as decision_types
from runtime.v01_decision_os_relational_deliberation import _event, _initial, _option


OS_STEMS = (
    ("DecisionOS", "decision"), ("PlanOS", "plan"), ("ActOS", "act"),
    ("ObserveOS", "observe"), ("VerifyOS", "verify"), ("LearnOS", "learn"),
)


class CheckedTransitionTests(unittest.TestCase):
    native_cases = None

    def setUp(self):
        try:
            self.guard = import_module(
                "runtime.kuuos_lean_python_checked_transition_v0_10"
            )
        except ModuleNotFoundError as exc:
            if exc.name == "runtime.kuuos_lean_python_checked_transition_v0_10":
                self.fail("the checked transition adapter has not been implemented")
            raise
        self.before = _initial("checked-transition-v010")
        self.event = _event(
            self.before, "generate",
            {"options": [_option(option_id="observe-a", action_class="observe",
                                 positive=(0.5, 0.6), negative=(0.1, 0.2))]}, 1,
        )
        self.original = decision.apply_decision_event

    @staticmethod
    def reseal(packet):
        state = packet["state"]
        state["decision_state_digest"] = decision_types.state_digest(state)
        packet["result_decision_state_digest"] = state["decision_state_digest"]
        packet["decision_apply_result_digest"] = decision_types.apply_result_digest(packet)
        return packet

    def failure(self, before, event, *, status="BLOCKED", issue=None,
                os_name="DecisionOS"):
        with self.assertRaises(self.guard.CheckedTransitionError) as caught:
            self.guard.checked_apply_event(os_name, before, event)
        error = caught.exception
        self.assertEqual(error.status, status, str(error))
        self.assertIs(type(error.issues), tuple)
        self.assertTrue(error.issues)
        if issue is not None:
            self.assertTrue(any(issue in item for item in error.issues), str(error))
        return error

    def forged(self, packet, *, before=None, event=None, status="BLOCKED", issue=None):
        with patch.object(decision, "apply_decision_event", return_value=packet):
            return self.failure(
                self.before if before is None else before,
                self.event if event is None else event, status=status, issue=issue,
            )

    def native_samples(self):
        cls = type(self)
        if cls.native_cases is None:
            from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
                build_native_full_cycle_receipt,
            )
            temporary = TemporaryDirectory(prefix="kuuos-checked-v010-")
            cls.addClassCleanup(temporary.cleanup)
            root = Path(temporary.name)
            build_native_full_cycle_receipt(root)
            cls.native_cases = {}
            for os_name, stem in OS_STEMS:
                folder = root / stem if stem in ("decision", "plan", "act") else root / "downstream" / stem
                state = json.loads((folder / f"{stem}-genesis.json").read_text(encoding="utf-8"))
                commits = [json.loads(line) for line in
                           (folder / f"{stem}-ledger.jsonl").read_text(encoding="utf-8").splitlines()]
                self.assertGreater(len(commits), 1)
                cls.native_cases[os_name] = (state, [item["event"] for item in commits])
        return deepcopy(cls.native_cases)

    def test_real_decision_apply_result_and_caller_inputs_are_preserved(self):
        before, event = deepcopy(self.before), deepcopy(self.event)
        expected = self.original(before, event)
        actual = self.guard.checked_apply_event("DecisionOS", before, event)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["status"], "APPLIED")
        self.assertEqual(actual["state"]["current_phase"], "generate")
        self.assertEqual(actual["state"]["event_index"], 1)
        self.assertEqual(before, self.before)
        self.assertEqual(event, self.event)
        actual["state"]["non_authority"]["truth_authority_granted"] = True
        self.assertIs(before["non_authority"]["truth_authority_granted"], False)

    def test_real_rejected_event_keeps_native_diagnostics_and_status(self):
        event = deepcopy(self.event)
        event["target_phase"] = "commit"
        event["decision_event_digest"] = decision_types.event_digest(event)
        expected = self.original(self.before, event)
        actual = self.guard.checked_apply_event("DecisionOS", self.before, event)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["status"], "REJECTED")
        self.assertTrue(actual["errors"])
        self.assertEqual(actual["state"], self.before)

    def test_real_rejection_for_missing_event_fields_is_returned_unchanged(self):
        actual = self.guard.checked_apply_event("DecisionOS", self.before, {})
        self.assertEqual(actual, self.original(self.before, {}))
        self.assertEqual(actual["status"], "REJECTED")

    def test_real_replay_does_not_need_the_current_predecessor_in_old_event(self):
        after = self.original(self.before, self.event)["state"]
        expected = self.original(after, self.event)
        actual = self.guard.checked_apply_event("DecisionOS", after, self.event)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["status"], "REPLAYED")
        self.assertEqual(actual["state"], after)

    def test_six_original_kernels_apply_replay_and_reject_without_semantic_changes(self):
        cases = self.native_samples()
        for os_name, stem in OS_STEMS:
            with self.subTest(os_name=os_name):
                before, events = cases[os_name]
                kernel = import_module(f"runtime.kuuos_{stem}_os_kernel_v0_1")
                original = getattr(kernel, f"apply_{stem}_event")
                event = events[0]
                expected = original(before, event)
                actual = self.guard.checked_apply_event(os_name, before, event)
                self.assertEqual(actual, expected)
                self.assertEqual(actual["status"], "APPLIED")
                self.assertEqual(actual["state"]["event_index"], 1)
                self.assertEqual(self.guard.checked_apply_event(os_name, actual["state"], event),
                                 original(actual["state"], event))
                self.assertEqual(self.guard.checked_apply_event(os_name, actual["state"], event)["status"],
                                 "REPLAYED")
                self.assertEqual(self.guard.checked_apply_event(os_name, before, {}), original(before, {}))
                self.assertEqual(self.guard.checked_apply_event(os_name, before, {})["status"], "REJECTED")

    def test_all_six_full_native_ledgers_preserve_original_phase_payloads(self):
        for os_name, stem in OS_STEMS:
            with self.subTest(os_name=os_name):
                before, events = self.native_samples()[os_name]
                original = getattr(import_module(f"runtime.kuuos_{stem}_os_kernel_v0_1"), f"apply_{stem}_event")
                for event in events:
                    expected = original(before, event)
                    actual = self.guard.checked_apply_event(os_name, before, event)
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual["status"], "APPLIED")
                    before = actual["state"]
                self.assertEqual(before["current_phase"], "commit")

    def test_fixed_os_allowlist_blocks_other_modules_and_custom_string_hooks(self):
        class CustomName(str):
            def __hash__(self):
                raise AssertionError("custom OS name hook invoked")
        for name in (None, "BeliefOS", "DecisionOSPlural", "runtime.os", "../../os", CustomName("DecisionOS")):
            with self.subTest(name=type(name).__name__):
                self.failure(self.before, self.event, os_name=name, issue="os_name")

    def test_missing_inputs_stay_no_data(self):
        self.failure(None, self.event, status="NO_DATA", issue="state")
        self.failure(self.before, None, status="NO_DATA", issue="event")

    def test_null_unknown_and_nonstring_status_cannot_bypass_transition_checks(self):
        for status in (None, "UNKNOWN", "", True, 0, [], {}):
            with self.subTest(status=status):
                packet = self.original(self.before, self.event)
                packet["status"] = status
                self.reseal(packet)
                self.forged(packet, issue="status")

    def test_every_missing_envelope_field_stays_no_data(self):
        packet = self.original(self.before, self.event)
        for key in packet:
            with self.subTest(key=key):
                bad = deepcopy(packet)
                bad.pop(key)
                self.forged(bad, status="NO_DATA", issue=key)

    def test_extra_envelope_fields_and_wrong_version_are_blocked_after_reseal(self):
        packet = self.original(self.before, self.event)
        packet["truth_authority_granted"] = True
        self.forged(self.reseal(packet), issue="envelope")
        packet = self.original(self.before, self.event)
        packet["version"] = "unrecognized_apply_result"
        self.forged(self.reseal(packet), issue="version")

    def test_envelope_digests_bind_actual_event_prestate_poststate_and_result(self):
        for key in ("decision_event_digest", "predecessor_decision_state_digest",
                    "result_decision_state_digest", "decision_apply_result_digest"):
            with self.subTest(key=key):
                packet = self.original(self.before, self.event)
                packet[key] = "0" * 64
                if key != "decision_apply_result_digest":
                    packet["decision_apply_result_digest"] = decision_types.apply_result_digest(packet)
                self.forged(packet, issue=key)

    def test_errors_are_native_string_list_and_empty_for_successful_statuses(self):
        for errors in (None, "failure", [1], ["unexpected error"]):
            with self.subTest(errors=errors):
                packet = self.original(self.before, self.event)
                packet["errors"] = errors
                self.forged(self.reseal(packet), issue="errors")

    def test_original_apply_is_called_once_on_independent_input_copies(self):
        calls = []
        def counted(state, event):
            calls.append((state is self.before, event is self.event))
            return self.original(state, event)
        with patch.object(decision, "apply_decision_event", side_effect=counted):
            actual = self.guard.checked_apply_event("DecisionOS", self.before, self.event)
        self.assertEqual(actual["status"], "APPLIED")
        self.assertEqual(calls, [(False, False)])

    def test_original_argument_mutations_block_and_do_not_touch_the_caller(self):
        for field in ("state", "event"):
            with self.subTest(field=field):
                state, event = deepcopy(self.before), deepcopy(self.event)
                def mutate(state_arg, event_arg):
                    result = self.original(state_arg, event_arg)
                    (state_arg if field == "state" else event_arg)["mutated"] = True
                    return result
                with patch.object(decision, "apply_decision_event", side_effect=mutate):
                    self.failure(state, event, issue="mutated")
                self.assertEqual(state, self.before)
                self.assertEqual(event, self.event)

    def test_equal_python_numbers_cannot_hide_original_argument_mutation(self):
        def mutate(state, event):
            result = self.original(state, event)
            event["event_index"] = True
            return result
        with patch.object(decision, "apply_decision_event", side_effect=mutate):
            self.failure(self.before, self.event, issue="mutated")

    def test_original_exception_is_blocked_without_retry_or_input_changes(self):
        count = []
        def explode(state, event):
            count.append(1)
            state["mutated"] = True
            event["payload"].clear()
            raise RuntimeError("kernel failure")
        with patch.object(decision, "apply_decision_event", side_effect=explode):
            self.failure(self.before, self.event, issue="RuntimeError")
        self.assertEqual(count, [1])
        self.assertNotIn("mutated", self.before)
        self.assertIn("options", self.event["payload"])

    def test_missing_native_functions_and_version_are_no_data(self):
        for module, name in ((decision, "apply_decision_event"),
                             (decision, "validate_decision_state"),
                             (decision_types, "event_digest"),
                             (decision_types, "apply_result_digest"),
                             (decision_types, "APPLY_RESULT_VERSION")):
            with self.subTest(name=name), patch.object(module, name, None):
                self.failure(self.before, self.event, status="NO_DATA", issue=name)

    def test_invalid_prestate_is_refused_before_any_original_application(self):
        before = deepcopy(self.before)
        before["non_authority"]["truth_authority_granted"] = True
        before["decision_state_digest"] = decision_types.state_digest(before)
        with patch.object(decision, "apply_decision_event", side_effect=AssertionError("must not apply")) as call:
            self.failure(before, self.event, issue="pre_state")
        self.assertEqual(call.call_count, 0)

    def test_original_poststate_validator_is_required_independently_of_the_result_hash(self):
        packet = self.original(self.before, self.event)
        real_validator = decision.validate_decision_state
        def validator(state):
            return ["post_schema_denied"] if state["current_phase"] == "generate" else real_validator(state)
        with patch.object(decision, "validate_decision_state", side_effect=validator):
            self.forged(packet, issue="post_schema_denied")

    def test_replay_cannot_substitute_an_event_body_behind_an_old_digest(self):
        after = self.original(self.before, self.event)["state"]
        changed = deepcopy(self.event)
        changed["payload"] = {"changed": True}
        self.assertEqual(self.original(after, changed)["status"], "REPLAYED")
        self.failure(after, changed, issue="event_digest")

    def test_applied_and_replayed_indices_and_timestamps_require_exact_naturals(self):
        for field in ("event_index", "created_at_ms"):
            for value in (True, 1.0, -1, 1001.9):
                with self.subTest(field=field, value=value):
                    event = deepcopy(self.event)
                    event[field] = value
                    event["decision_event_digest"] = decision_types.event_digest(event)
                    packet = self.original(self.before, self.event)
                    packet["decision_event_digest"] = event["decision_event_digest"]
                    self.forged(self.reseal(packet), event=event, issue=field)
        # These coercions are accepted by the real v0.1 kernel. Exercise both
        # statuses without a replacement kernel so replay cannot evade the gate.
        for field, value in (("event_index", True), ("event_index", 1.0),
                             ("created_at_ms", 1001.9)):
            with self.subTest(real_native_field=field, value=value):
                event = deepcopy(self.event)
                event[field] = value
                event["decision_event_digest"] = decision_types.event_digest(event)
                applied = self.original(self.before, event)
                self.assertEqual(applied["status"], "APPLIED")
                self.failure(self.before, event, issue=field)
                self.assertEqual(self.original(applied["state"], event)["status"], "REPLAYED")
                self.failure(applied["state"], event, issue=field)

    def test_missing_auditor_and_original_import_dependency_remain_no_data(self):
        for name in ("audit_core_state", "audit_core_transition", "_finite_json"):
            with self.subTest(name=name), patch.object(self.guard, name, None):
                self.failure(self.before, self.event, status="NO_DATA", issue=name)
        with patch.object(self.guard, "import_module", side_effect=ModuleNotFoundError("missing original")):
            self.failure(self.before, self.event, status="NO_DATA", issue="dependency_unavailable")

    def test_structural_audit_failure_cannot_return_a_native_success(self):
        from dataclasses import replace
        original_audit = self.guard.audit_core_transition
        def fail_audit(*arguments):
            return replace(original_audit(*arguments), status="BLOCKED", issues=("deliberate_boundary_failure",))
        with patch.object(self.guard, "audit_core_transition", side_effect=fail_audit):
            self.failure(self.before, self.event, issue="deliberate_boundary_failure")

    def test_original_validator_mutation_is_blocked_before_apply(self):
        validator = decision.validate_decision_state
        def mutate(state):
            errors = validator(state)
            state["extra"] = True
            return errors
        with patch.object(decision, "validate_decision_state", side_effect=mutate), patch.object(
            decision, "apply_decision_event", side_effect=AssertionError("must not apply")
        ) as call:
            self.failure(self.before, self.event, issue="audit_argument_mutated")
        self.assertEqual(call.call_count, 0)
        self.assertNotIn("extra", self.before)

    def test_false_replay_of_unprocessed_event_is_blocked(self):
        packet = self.original(self.before, self.event)
        packet["status"] = "REPLAYED"
        packet["state"] = deepcopy(self.before)
        self.forged(self.reseal(packet), issue="replay")

    def test_nonapplied_results_require_exact_unchanged_json_state(self):
        event = {}
        packet = self.original(self.before, event)
        packet["state"]["decision_budget"] = 1
        self.assertEqual(packet["state"]["decision_budget"], self.before["decision_budget"])
        self.forged(self.reseal(packet), event=event, issue="unchanged")

    def test_coherent_resealed_phase_index_history_and_predecessor_tampering_is_blocked(self):
        for field, value in (("current_phase", "frame"), ("event_index", 0),
                             ("event_history", []), ("processed_event_digests", []),
                             ("predecessor_decision_state_digest", "0" * 64)):
            with self.subTest(field=field):
                packet = self.original(self.before, self.event)
                packet["state"][field] = value
                self.forged(self.reseal(packet))

    def test_applied_history_row_must_match_all_six_event_fields(self):
        for key in ("event_index", "source_phase", "target_phase", "artifact_digest",
                    "decision_event_digest", "created_at_ms"):
            with self.subTest(key=key):
                packet = self.original(self.before, self.event)
                packet["state"]["event_history"][-1][key] = "forged"
                self.forged(self.reseal(packet), issue="history")
        packet = self.original(self.before, self.event)
        packet["state"]["event_history"][-1]["authority"] = True
        self.forged(self.reseal(packet), issue="history")

    def test_equal_python_history_prefix_cannot_hide_a_type_rewrite(self):
        before = self.original(self.before, self.event)["state"]
        event = _event(before, "constrain", {"constraint_receipt_digest": "receipt"}, 2)
        packet = self.original(before, event)
        packet["state"]["event_history"][0]["event_index"] = True
        self.assertEqual(packet["state"]["event_history"][0], before["event_history"][0])
        self.forged(self.reseal(packet), before=before, event=event, issue="history")

    def test_applied_timestamp_must_match_the_event(self):
        packet = self.original(self.before, self.event)
        packet["state"]["updated_at_ms"] += 1
        self.forged(self.reseal(packet), issue="updated_at_ms")

    def test_identity_lineage_and_source_bindings_remain_immutable_in_all_six_os(self):
        examples = {
            "DecisionOS": "source_belief_receipt_digest", "PlanOS": "source_wa_state_digest",
            "ActOS": "source_plan_state_digest", "ObserveOS": "source_act_state_digest",
            "VerifyOS": "source_observe_state_digest", "LearnOS": "source_verify_state_digest",
        }
        for os_name, stem in OS_STEMS:
            before, events = self.native_samples()[os_name]
            kernel = import_module(f"runtime.kuuos_{stem}_os_kernel_v0_1")
            types = import_module(f"runtime.kuuos_{stem}_os_types_v0_1")
            original = getattr(kernel, f"apply_{stem}_event")
            state_digest = getattr(types, "plan_state_digest" if stem == "plan" else "state_digest")
            result_digest = getattr(types, "plan_apply_result_digest" if stem == "plan" else "apply_result_digest")
            for field in (f"{stem}_id", "lineage_id", "mission_contract_digest", examples[os_name]):
                with self.subTest(os_name=os_name, field=field):
                    packet = original(before, events[0])
                    packet["state"][field] = "replacement"
                    packet["state"][f"{stem}_state_digest"] = state_digest(packet["state"])
                    packet[f"result_{stem}_state_digest"] = packet["state"][f"{stem}_state_digest"]
                    packet[f"{stem}_apply_result_digest"] = result_digest(packet)
                    with patch.object(kernel, f"apply_{stem}_event", return_value=packet):
                        self.failure(before, events[0], os_name=os_name)

    def test_nonfinite_custom_cyclic_and_oversized_json_is_blocked_before_apply(self):
        class CustomDict(dict):
            def __iter__(self):
                raise AssertionError("custom data hook invoked")
            def __deepcopy__(self, memo):
                raise AssertionError("custom copy hook invoked")
        cycle = []
        cycle.append(cycle)
        for value in (float("nan"), float("inf"), CustomDict(), cycle, (1,), {1: 2}, "x" * 4_000_001):
            with self.subTest(kind=type(value).__name__):
                event = deepcopy(self.event)
                event["bad"] = value
                with patch.object(decision, "apply_decision_event", side_effect=AssertionError("must not apply")) as call:
                    self.failure(self.before, event, issue="json")
                self.assertEqual(call.call_count, 0)

    def test_result_must_also_be_exact_bounded_finite_json(self):
        class CustomDict(dict):
            pass
        for value in (None, [], CustomDict(), {"bad": float("nan")}, {"bad": "x" * 4_000_001}):
            with self.subTest(kind=type(value).__name__):
                self.forged(value, status="NO_DATA" if value is None else "BLOCKED")


if __name__ == "__main__":
    unittest.main()
