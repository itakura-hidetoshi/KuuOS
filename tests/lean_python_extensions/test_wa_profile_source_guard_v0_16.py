"""v0.16 Wa local committed-Plural witness and profile hash regressions.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_wa_profile_source_guard_v0_16 as guarded
from runtime import kuuos_lean_python_wa_evaluation_guard_v0_15 as prior
from runtime import kuuos_decision_os_wa_kernel_v0_3 as native
from runtime import kuuos_decision_os_wa_types_v0_3 as types
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from tests.lean_python_extensions.test_mediator_transition_v0_12 import _native_traces


class WaProfileSourceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        traces = _native_traces()
        cls.source_witness = traces["DecisionOSPlural"][3].state
        cls.wa_trace = traces["DecisionOSWa"][3]

    def pair(self, n=0):
        return deepcopy(self.wa_trace.pairs[n])

    def event(self, state, phase, payload):
        return native.build_wa_event(
            state=state, target_phase=phase, artifact_digest=types.sha("v016-" + phase),
            payload=payload, now_ms=state["updated_at_ms"] + 1,
        )

    def seal_state(self, state):
        state["wa_state_digest"] = types.wa_state_digest(state)
        return state

    def seal_result(self, result):
        state = self.seal_state(result["state"])
        result["result_wa_state_digest"] = state["wa_state_digest"]
        result["wa_apply_result_digest"] = types.wa_apply_result_digest(result)
        return result

    def reject_pre(self, state, event, source=None, status="BLOCKED"):
        src = self.source_witness if source is None else source
        fingerprint = _fingerprint([state, event, src]) if state is not None and event is not None else None
        with patch.object(prior, "checked_apply_wa_evaluation_event",
                          wraps=prior.checked_apply_wa_evaluation_event) as prior_guard:
            with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                guarded.checked_apply_wa_profile_source_event(state, event, src)
            prior_guard.assert_not_called()
        self.assertEqual(caught.exception.status, status)
        if fingerprint is not None:
            self.assertEqual(_fingerprint([state, event, src]), fingerprint)
        return caught.exception

    def reject_post(self, state, event, fake_result):
        with patch.object(prior, "checked_apply_wa_evaluation_event", return_value=fake_result) as checked:
            with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                guarded.checked_apply_wa_profile_source_event(state, event, self.source_witness)
        checked.assert_called_once()
        self.assertEqual(caught.exception.status, "BLOCKED")
        return caught.exception

    def test_original_six_phase_results_and_replays_are_byte_equal(self):
        for state, event in self.wa_trace.pairs:
            expected = prior.checked_apply_wa_evaluation_event(state, event)
            actual = guarded.checked_apply_wa_profile_source_event(state, event, self.source_witness)
            self.assertEqual(expected, actual)
            replay = guarded.checked_apply_wa_profile_source_event(expected["state"], event, self.source_witness)
            self.assertEqual(replay, prior.checked_apply_wa_evaluation_event(expected["state"], event))
            self.assertEqual(replay["status"], "REPLAYED")

    def test_witness_projection_reconstructs_all_19_original_wa_fields(self):
        source = deepcopy(self.source_witness)
        state, _ = self.pair()
        guarded._validate_source(source)
        expected = guarded._source_projection(source)
        self.assertEqual(len(expected), 19)
        self.assertEqual(set(expected), set(guarded._DIRECT_SOURCE) | set(guarded._HASHED_SOURCE) |
                         {"source_option_digest_by_id"})
        for field, value in expected.items():
            self.assertEqual(_fingerprint(state[field]), _fingerprint(value), field)

    def test_original_v015_accepts_resent_wa_source_fields_but_v016_blocks(self):
        before, event = self.pair()
        for field in ("source_options_digest", "source_utility_records_digest",
                      "source_appeal_history_digest", "source_stakeholder_registry_digest",
                      "source_plural_state_digest", "mission_contract_digest"):
            changed = self.seal_state(deepcopy(before))
            changed[field] = types.sha("tampered-" + field)
            self.seal_state(changed)
            new_event = self.event(changed, "profile", event["payload"])
            with self.subTest(field=field):
                old_result = prior.checked_apply_wa_evaluation_event(changed, new_event)
                self.assertEqual(old_result["status"], "APPLIED")
                self.assertIn(field, str(self.reject_pre(changed, new_event)))

    def test_source_option_digest_map_must_match_actual_recovered_plural(self):
        before, event = self.pair()
        changed = deepcopy(before)
        option_id = next(iter(changed["source_option_digest_by_id"]))
        changed["source_option_digest_by_id"][option_id] = types.sha("different")
        self.seal_state(changed)
        self.assertIn("source_option_digest_by_id",
                      str(self.reject_pre(changed, event)))

    def test_resealed_unrelated_supplied_plural_snapshot_cannot_satisfy_projection(self):
        before, event = self.pair()
        source = deepcopy(self.source_witness)
        source["route"] = "HOLD"
        source["plural_state_digest"] = _fingerprint(
            {k: v for k, v in source.items() if k != "plural_state_digest"}
        )
        # An external assertion of digest agreement is insufficient. The
        # source's local validity and projection must both be checked.
        self.reject_pre(before, event, source=source)

    def test_missing_plur_source_does_not_fall_back_to_bare_wa_digest(self):
        before, event = self.pair()
        with patch.object(prior, "checked_apply_wa_evaluation_event") as old:
            with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                guarded.checked_apply_wa_profile_source_event(before, event, None)
            old.assert_not_called()
        self.assertEqual(caught.exception.status, "NO_DATA")

    def test_missing_source_projection_field_is_no_data(self):
        before, event = self.pair()
        for field in ("source_options_digest", "source_plural_id",
                      "source_committed_plural_digest", "source_veto_records_digest"):
            state = deepcopy(before)
            state.pop(field)
            with self.subTest(field=field):
                self.reject_pre(state, event, status="NO_DATA")

    def test_missing_plural_witness_field_is_no_data(self):
        before, event = self.pair()
        for field in ("source_options", "source_option_ids", "plural_id",
                      "utility_records", "appeal_history"):
            source = deepcopy(self.source_witness)
            source.pop(field)
            with self.subTest(field=field):
                outcome = self.reject_pre(before, event, source=source)
                self.assertIn(outcome.status, ("NO_DATA", "BLOCKED"))

    def test_committed_plural_phase_and_canonical_state_hash_are_required(self):
        before, event = self.pair()
        for action in ("wrong_phase", "digest_changed", "numeric_digest"):
            source = deepcopy(self.source_witness)
            if action == "wrong_phase":
                source["current_phase"] = "adjudicate"
                source["plural_state_digest"] = _fingerprint({k: v for k, v in source.items()
                                                               if k != "plural_state_digest"})
            elif action == "digest_changed":
                source["plural_state_digest"] = types.sha("forged")
            else:
                source["plural_state_digest"] = 1
            with self.subTest(action=action):
                self.reject_pre(before, event, source=source)

    def test_untampered_wa_profile_preimages_match_digest_and_schema(self):
        state, _ = self.pair(1)
        self.assertEqual(state["current_phase"], "profile")
        for profile in state["profiles"]:
            self.assertEqual(set(profile), set(guarded._PROFILE_FIELDS))
            expected = _fingerprint({field: profile[field] for field in guarded._PROFILE_FIELDS
                                     if field != "wa_profile_digest"})
            self.assertEqual(profile["wa_profile_digest"], expected)

    def test_stale_dialogue_digest_is_rejected_before_native_evaluation(self):
        state, event = self.pair(1)
        state["profiles"][0]["dialogue_receipt_digest"] = types.sha("opaque-changed")
        self.seal_state(state)
        fresh = self.event(state, "evaluate", event["payload"])
        # The earlier v0.12 mediator already checks the profile digest.
        # v0.16 also rejects it before any v0.15 evaluation call.
        with self.assertRaises(prior.WaEvaluationBoundaryError):
            prior.checked_apply_wa_evaluation_event(state, fresh)
        self.assertIn("profile_digest", str(self.reject_pre(state, fresh)))

    def test_stale_profile_digest_on_native_result_is_rejected_before_commit(self):
        before, event = self.pair()
        original = prior.checked_apply_wa_evaluation_event(before, event)
        result = deepcopy(original)
        result["state"]["profiles"][0]["dialogue_receipt_digest"] = types.sha("tampered-after-native")
        self.seal_result(result)
        # The earlier v0.12 mediator also rejects this malformed poststate.
        # Here the substituted prior result tests the independent new check.
        self.assertIn("profile_digest", str(self.reject_post(before, event, result)))

    def test_full_profile_schema_rejects_missing_and_extra_receipts(self):
        state, event = self.pair(1)
        for action in ("missing", "extra", "bad_type", "duplicate"):
            changed = deepcopy(state)
            profile = changed["profiles"][0]
            if action == "missing":
                profile.pop("dialogue_receipt_digest")
            elif action == "extra":
                profile["granted_authority"] = True
            elif action == "bad_type":
                profile["minority_preserved"] = 1
            else:
                profile["dissent_evidence_digests"] = ["repeat", "repeat"]
            self.seal_state(changed)
            with self.subTest(action=action):
                self.reject_pre(changed, event)

    def test_self_consistent_but_unproven_receipt_value_is_not_authenticity(self):
        state, event = self.pair(1)
        profile = state["profiles"][0]
        profile["dialogue_receipt_digest"] = types.sha("opaque-unverified-issuer")
        profile["wa_profile_digest"] = _fingerprint(
            {key: value for key, value in profile.items() if key != "wa_profile_digest"}
        )
        self.seal_state(state)
        action = self.event(state, "evaluate", event["payload"])
        self.assertEqual(
            guarded.checked_apply_wa_profile_source_event(state, action, self.source_witness),
            prior.checked_apply_wa_evaluation_event(state, action),
        )

    def test_native_rejected_status_and_errors_remain_identical(self):
        before, event = self.pair()
        event.pop("wa_event_digest")
        old = prior.checked_apply_wa_evaluation_event(before, event)
        self.assertEqual(old["status"], "REJECTED")
        self.assertEqual(guarded.checked_apply_wa_profile_source_event(before, event, self.source_witness), old)

    def test_invalid_prestate_replay_stops_before_prior_call(self):
        state, event = self.pair(2)
        state["profiles"][0]["wa_profile_digest"] = types.sha("stale")
        self.seal_state(state)
        self.reject_pre(state, event)
        self.reject_pre(state, self.pair(1)[1])

    def test_caller_inputs_and_witness_are_not_mutated(self):
        state, event = self.pair()
        source = deepcopy(self.source_witness)
        before = _fingerprint([state, event, source])
        result = guarded.checked_apply_wa_profile_source_event(state, event, source)
        result["state"]["profiles"].clear()
        self.assertEqual(before, _fingerprint([state, event, source]))

    def test_nonbuiltin_cycles_nonfinite_or_tuple_witness_fail_before_prior(self):
        state, event = self.pair()
        for invalid in (float("nan"), float("inf"), (1,), object()):
            witness = deepcopy(self.source_witness)
            witness["unexpected"] = invalid
            with patch.object(prior, "checked_apply_wa_evaluation_event") as old:
                with self.assertRaises(guarded.WaProfileSourceBoundaryError):
                    guarded.checked_apply_wa_profile_source_event(state, event, witness)
                old.assert_not_called()

    def test_prerequisites_missing_cannot_promote_no_data_to_success(self):
        state, event = self.pair()
        for attr in ("_finite_json", "_fingerprint", "validate_plural_state"):
            with self.subTest(attr=attr), patch.object(guarded, attr, None):
                with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                    guarded.checked_apply_wa_profile_source_event(state, event, self.source_witness)
                self.assertEqual(caught.exception.status, "NO_DATA")
        with patch.object(prior, "checked_apply_wa_evaluation_event", None):
            with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                guarded.checked_apply_wa_profile_source_event(state, event, self.source_witness)
            self.assertEqual(caught.exception.status, "NO_DATA")

    def test_prior_no_data_and_blocked_statuses_are_preserved(self):
        state, event = self.pair()
        for status in ("NO_DATA", "BLOCKED"):
            with patch.object(prior, "checked_apply_wa_evaluation_event",
                              side_effect=prior.WaEvaluationBoundaryError(status, ("retained",))):
                with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                    guarded.checked_apply_wa_profile_source_event(state, event, self.source_witness)
            self.assertEqual(caught.exception.status, status)

    def test_prior_argument_mutation_is_detected(self):
        state, event = self.pair()
        def mutation(s, e):
            s["event_index"] = 7
            return {"status": "REJECTED", "state": s}
        with patch.object(prior, "checked_apply_wa_evaluation_event", side_effect=mutation):
            with self.assertRaises(guarded.WaProfileSourceBoundaryError) as caught:
                guarded.checked_apply_wa_profile_source_event(state, event, self.source_witness)
        self.assertIn("mutated", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
