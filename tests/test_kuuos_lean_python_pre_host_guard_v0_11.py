"""Pre-host regressions using real Act/project fixtures and native bindings.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_act_os_kernel_v0_1 as act
from runtime import kuuos_act_os_types_v0_1 as act_types
from runtime import kuuos_cooperative_host_adapter_types_v0_17 as host_types
from runtime import kuuos_cooperative_execution_supervisor_types_v0_16 as supervisor_types
from runtime.kuuos_act_os_fixture_v0_1 import host_inputs, prepared_project_state, source_plan
from runtime.kuuos_cooperative_host_adapter_projection_v0_17 import project_host_work
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import ticket_digest
from runtime.v017_host_adapter_fixtures import queued_bundle, registry, steps


class PreHostGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = TemporaryDirectory(prefix="kuuos-v011-pre-host-")
        cls.addClassCleanup(temporary.cleanup)
        root = Path(temporary.name)
        plan, activation = source_plan(root)
        policy, bundle, license_packet, projection = host_inputs(job_id="pre-host-v011-job")
        _, state = prepared_project_state(
            root=root / "act", act_id="pre-host-v011-act", plan_state=plan,
            plan_activation=activation, job_id="pre-host-v011-job",
            host_license=license_packet, projection=projection,
        )
        cls.fixture = dict(state=state, supervisor_bundle=bundle, worker_id="act-worker",
                           now_ms=90_004, supervisor_policy=policy, registry=registry())

    def setUp(self):
        try:
            self.guard = import_module("runtime.kuuos_lean_python_pre_host_guard_v0_11")
        except ModuleNotFoundError as exc:
            if exc.name == "runtime.kuuos_lean_python_pre_host_guard_v0_11":
                self.fail("pre-host guard has not been implemented")
            raise
        self.inputs = deepcopy(self.fixture)

    @staticmethod
    def seal_state(inputs):
        state = inputs["state"]
        state["act_state_digest"] = act_types.state_digest(state)

    @classmethod
    def seal_authorization(cls, inputs):
        state = inputs["state"]
        authorization = state["step_authorization"]
        authorization["step_authorization_digest"] = act_types.authorization_digest(authorization)
        state["step_authorization_digest"] = authorization["step_authorization_digest"]
        cls.seal_state(inputs)

    @classmethod
    def seal_license(cls, inputs):
        state = inputs["state"]
        license_packet = state["host_license"]
        license_packet["host_license_digest"] = host_types.license_digest(license_packet)
        state["host_license_digest"] = license_packet["host_license_digest"]
        state["step_authorization"]["host_license_digest"] = license_packet["host_license_digest"]
        cls.seal_authorization(inputs)

    @classmethod
    def seal_projection(cls, inputs):
        state = inputs["state"]
        projection = state["host_projection"]
        projection["projection_digest"] = host_types.projection_digest(projection)
        state["host_projection_digest"] = projection["projection_digest"]
        cls.seal_state(inputs)

    @classmethod
    def bind_bundle(cls, inputs):
        bundle = inputs["supervisor_bundle"]
        bundle["supervisor_bundle_digest"] = supervisor_types.bundle_digest(bundle)
        state = inputs["state"]
        state["source_supervisor_bundle_digest"] = bundle["supervisor_bundle_digest"]
        state["step_authorization"]["source_supervisor_bundle_digest"] = bundle["supervisor_bundle_digest"]
        state["host_projection"] = project_host_work(
            supervisor_bundle=bundle, now_ms=90_000,
            operation_allowlist=state["host_license"]["operation_allowlist"],
        )
        state["host_projection_digest"] = state["host_projection"]["projection_digest"]
        cls.seal_authorization(inputs)

    def blocked_before_host(self, inputs, *, status="BLOCKED", issue=None):
        data_before = {key: _fingerprint(inputs[key]) for key in
                       ("state", "supervisor_bundle", "supervisor_policy")
                       if type(inputs[key]) is dict}
        with patch.object(act, "build_authorized_invoke_event", wraps=act.build_authorized_invoke_event) as builder:
            with patch.object(act, "run_host_tick", side_effect=AssertionError("host must not be reached")) as host:
                with self.assertRaises(self.guard.PreHostCheckError) as caught:
                    self.guard.checked_build_authorized_invoke_event(**inputs)
        error = caught.exception
        self.assertEqual(error.status, status, str(error))
        self.assertIs(type(error.issues), tuple)
        self.assertTrue(error.issues)
        self.assertIs(error.host_call_attempted, False)
        self.assertEqual(builder.call_count, 0)
        self.assertEqual(host.call_count, 0)
        if issue:
            self.assertTrue(any(issue in item for item in error.issues), str(error))
        self.assertEqual(data_before, {key: _fingerprint(inputs[key]) for key in data_before})

    def test_genuine_original_event_and_tick_are_preserved_without_input_mutation(self):
        before = {key: _fingerprint(self.inputs[key]) for key in
                  ("state", "supervisor_bundle", "supervisor_policy")}
        expected = act.build_authorized_invoke_event(**deepcopy(self.inputs))
        with patch.object(act, "build_authorized_invoke_event", wraps=act.build_authorized_invoke_event) as original:
            actual = self.guard.checked_build_authorized_invoke_event(**self.inputs)
        self.assertEqual(actual, expected)
        self.assertEqual(original.call_count, 1)
        self.assertEqual(actual[0]["target_phase"], "invoke")
        self.assertEqual(actual[1]["receipt"]["completed_step_ids_in_slice"], ["step-1"])
        self.assertEqual(before, {key: _fingerprint(self.inputs[key]) for key in before})
        self.assertIs(self.inputs["registry"]["fixture.success"], registry()["fixture.success"])

    def test_expired_and_future_authorization_are_blocked_before_host(self):
        for now in (200_000, 89_999):
            with self.subTest(now=now):
                inputs = deepcopy(self.inputs)
                inputs["now_ms"] = now
                self.blocked_before_host(inputs)
        inputs = deepcopy(self.inputs)
        inputs["state"]["step_authorization"]["issued_at_ms"] = 100_000
        self.seal_authorization(inputs)
        self.blocked_before_host(inputs, issue="authorization")

    def test_time_regression_is_blocked_even_while_authorization_is_valid(self):
        self.inputs["now_ms"] = 90_002
        self.blocked_before_host(self.inputs, issue="time_regression")

    def test_nested_digest_or_cached_digest_mismatch_is_blocked_before_host(self):
        for key in ("step_authorization_digest", "host_license_digest", "host_projection_digest"):
            with self.subTest(key=key):
                inputs = deepcopy(self.inputs)
                inputs["state"][key] = "0" * 64
                self.seal_state(inputs)
                self.blocked_before_host(inputs, issue=key)
        for field in ("step_authorization", "host_license", "host_projection"):
            inputs = deepcopy(self.inputs)
            inputs["state"][field]["unexpected"] = True
            self.seal_state(inputs)
            self.blocked_before_host(inputs)

    def test_coherently_resealed_authorization_bindings_cannot_change_the_selected_work(self):
        for field in ("act_id", "source_plan_state_digest", "selected_step_digest",
                      "operation_id", "operation_input_digest", "host_job_id", "host_step_id",
                      "source_supervisor_bundle_digest", "host_license_digest"):
            with self.subTest(field=field):
                inputs = deepcopy(self.inputs)
                inputs["state"]["step_authorization"][field] = "altered"
                self.seal_authorization(inputs)
                self.blocked_before_host(inputs)

    def test_cached_digests_cannot_use_null_or_nonstring_to_skip_binding(self):
        for field in ("selected_step_digest", "step_authorization_digest",
                      "host_license_digest", "host_projection_digest"):
            for value in (None, "", False, 0, []):
                with self.subTest(field=field, value=value):
                    inputs = deepcopy(self.inputs)
                    inputs["state"][field] = value
                    if field == "selected_step_digest":
                        inputs["state"]["step_authorization"][field] = value
                        self.seal_authorization(inputs)
                    else:
                        self.seal_state(inputs)
                    self.blocked_before_host(inputs)
            inputs = deepcopy(self.inputs)
            inputs["state"].pop(field)
            self.seal_state(inputs)
            self.blocked_before_host(inputs, status="NO_DATA")

    def test_human_review_single_use_and_authority_flags_use_exact_booleans(self):
        for field, value in (("single_use", 1), ("single_use", False),
                             ("authorization_does_not_widen_license", 1)):
            inputs = deepcopy(self.inputs)
            inputs["state"]["step_authorization"][field] = value
            self.seal_authorization(inputs)
            self.blocked_before_host(inputs)
        inputs = deepcopy(self.inputs)
        inputs["state"]["step_authorization"]["human_approval_receipt_digest"] = ""
        self.seal_authorization(inputs)
        self.blocked_before_host(inputs)
        inputs = deepcopy(self.inputs)
        inputs["state"]["step_authorization"]["non_authority"]["truth_authority_granted"] = 0
        self.seal_authorization(inputs)
        self.blocked_before_host(inputs)

    def test_selected_plan_step_content_digest_and_effect_flags_are_checked(self):
        for field, value in (("effectful", 1), ("requires_human_review", 1),
                             ("step_class", "prepare"), ("stop_condition_digests", [])):
            inputs = deepcopy(self.inputs)
            step = inputs["state"]["selected_step"]
            step[field] = value
            self.seal_state(inputs)
            self.blocked_before_host(inputs)

    def test_actual_job_input_is_bound_to_job_digest_state_and_authorization(self):
        for update_cached_digest in (False, True):
            with self.subTest(update_cached_digest=update_cached_digest):
                inputs = deepcopy(self.inputs)
                job = inputs["supervisor_bundle"]["jobs"][0]
                step = job["steps"][0]
                step["operation_input"]["value"] = 999
                if update_cached_digest:
                    step["operation_input_digest"] = supervisor_types.sha(step["operation_input"])
                job["manifest_digest"] = supervisor_types.manifest_digest(job)
                job["job_state_digest"] = supervisor_types.job_state_digest(job)
                self.bind_bundle(inputs)
                self.blocked_before_host(inputs, issue="operation_input")
        inputs = deepcopy(self.inputs)
        changed_digest = supervisor_types.sha({"value": 999})
        inputs["state"]["operation_input_digest"] = changed_digest
        inputs["state"]["step_authorization"]["operation_input_digest"] = changed_digest
        self.seal_authorization(inputs)
        self.blocked_before_host(inputs, issue="operation_input")

    def test_single_authorized_step_cannot_request_a_multistep_slice(self):
        self.inputs["state"]["host_license"]["max_steps_per_slice"] = 2
        self.inputs["state"]["host_license"]["max_cost_per_slice"] = 2.0
        self.inputs["supervisor_policy"]["max_steps_per_slice"] = 2
        self.inputs["supervisor_policy"]["max_cost_per_slice"] = 2.0
        self.seal_license(self.inputs)
        self.inputs["supervisor_bundle"] = queued_bundle(
            job_id="pre-host-v011-job", job_steps=steps(2), policy=self.inputs["supervisor_policy"],
        )
        self.bind_bundle(self.inputs)
        _, original_tick = act.build_authorized_invoke_event(**deepcopy(self.inputs))
        self.assertEqual(original_tick["receipt"]["completed_step_ids_in_slice"], ["step-1", "step-2"])
        self.blocked_before_host(self.inputs, issue="single_step")

    def test_integer_fields_reject_bool_float_strings_and_negative_values(self):
        cases = (("now_ms",), ("state", "step_authorization", "expires_at_ms"),
                 ("state", "host_license", "max_steps_per_slice"),
                 ("supervisor_policy", "max_steps_per_slice"))
        for path in cases:
            for value in (True, 1.0, "1", -1):
                with self.subTest(path=path, value=value):
                    inputs = deepcopy(self.inputs)
                    target = inputs
                    for key in path[:-1]:
                        target = target[key]
                    target[path[-1]] = value
                    if "step_authorization" in path:
                        self.seal_authorization(inputs)
                    elif "host_license" in path:
                        self.seal_license(inputs)
                    self.blocked_before_host(inputs)

    def test_license_permissions_cost_and_policy_types_fail_before_host(self):
        for field, value in (("bounded_slice_execute_allowed", 1),
                             ("max_cost_per_slice", True), ("max_cost_per_slice", "1"),
                             ("in_place_bundle_write_allowed", 0), ("max_jobs_per_invocation", 2)):
            inputs = deepcopy(self.inputs)
            inputs["state"]["host_license"][field] = value
            self.seal_license(inputs)
            self.blocked_before_host(inputs)
        for field, value in (("background_worker_available", 1),
                             ("max_cost_per_slice", True), ("retry_backoff_base_ms", 1.5)):
            inputs = deepcopy(self.inputs)
            inputs["supervisor_policy"][field] = value
            self.blocked_before_host(inputs)

    def test_projection_is_recomputed_and_cannot_forge_candidate_contents(self):
        for field, value in (("candidate_count", True), ("selected_job_state_digest", "altered"),
                             ("selected_ticket_digest", "altered"), ("projected_at_ms", 90_005)):
            inputs = deepcopy(self.inputs)
            inputs["state"]["host_projection"][field] = value
            self.seal_projection(inputs)
            self.blocked_before_host(inputs)
        inputs = deepcopy(self.inputs)
        inputs["state"]["host_projection"]["candidates"][0]["estimated_cost_units"] = 0.0
        self.seal_projection(inputs)
        self.blocked_before_host(inputs)

    def test_selected_ticket_identifiers_cannot_hide_native_string_coercions(self):
        for field in ("ticket_id", "checkpoint_digest"):
            with self.subTest(field=field):
                inputs = deepcopy(self.inputs)
                job = inputs["supervisor_bundle"]["jobs"][0]
                ticket = job["active_continuation_ticket"]
                ticket[field] = 1
                if field == "checkpoint_digest":
                    job["latest_checkpoint_digest"] = 1
                ticket["background_ticket_digest"] = ticket_digest(ticket)
                job["job_state_digest"] = supervisor_types.job_state_digest(job)
                self.bind_bundle(inputs)
                self.blocked_before_host(inputs)

    def test_native_step_availability_and_registry_are_checked_before_host(self):
        for value in (None, {}, {"fixture.success": None}, {1: registry()["fixture.success"]}):
            inputs = deepcopy(self.inputs)
            inputs["registry"] = value
            self.blocked_before_host(inputs, status="NO_DATA" if value is None else "BLOCKED")
        inputs = deepcopy(self.inputs)
        inputs["supervisor_policy"]["max_cost_per_slice"] = 0.0
        self.blocked_before_host(inputs)

    def test_missing_data_custom_containers_and_nonfinite_json_fail_closed(self):
        for field in ("state", "supervisor_bundle", "supervisor_policy"):
            inputs = deepcopy(self.inputs)
            inputs[field] = None
            self.blocked_before_host(inputs, status="NO_DATA")
        class CustomDict(dict):
            def __deepcopy__(self, memo):
                raise AssertionError("custom hook called")
        for field in ("state", "supervisor_bundle", "supervisor_policy", "registry"):
            inputs = deepcopy(self.inputs)
            inputs[field] = CustomDict(inputs[field])
            self.blocked_before_host(inputs)
        for value in (float("nan"), float("inf")):
            inputs = deepcopy(self.inputs)
            inputs["supervisor_policy"]["max_cost_per_slice"] = value
            # These cannot be fingerprinted; assert the pre-host boundary directly.
            with patch.object(act, "run_host_tick") as host:
                with self.assertRaises(self.guard.PreHostCheckError) as caught:
                    self.guard.checked_build_authorized_invoke_event(**inputs)
            self.assertIs(caught.exception.host_call_attempted, False)
            self.assertEqual(host.call_count, 0)

    def test_post_host_checked_transition_failure_marks_possible_effect(self):
        from runtime.kuuos_lean_python_checked_transition_v0_10 import CheckedTransitionError
        with patch.object(act, "run_host_tick", wraps=act.run_host_tick) as host:
            with patch.object(self.guard, "checked_apply_event", side_effect=CheckedTransitionError(
                "BLOCKED", ("post_host_boundary_failure",)
            )):
                with self.assertRaises(self.guard.PreHostCheckError) as caught:
                    self.guard.checked_build_authorized_invoke_event(**self.inputs)
        self.assertEqual(host.call_count, 1)
        self.assertIs(caught.exception.host_call_attempted, True)
        self.assertIn("post_host_boundary_failure", str(caught.exception))

    def test_original_builder_exception_after_host_is_not_reported_as_preflight_failure(self):
        original = act.build_authorized_invoke_event
        def fail_after_host(**kwargs):
            original(**kwargs)
            raise RuntimeError("after host")
        with patch.object(act, "run_host_tick", wraps=act.run_host_tick) as host:
            with patch.object(act, "build_authorized_invoke_event", side_effect=fail_after_host):
                with self.assertRaises(self.guard.PreHostCheckError) as caught:
                    self.guard.checked_build_authorized_invoke_event(**self.inputs)
        self.assertEqual(host.call_count, 1)
        self.assertIs(caught.exception.host_call_attempted, True)

    def test_post_host_input_mutation_and_event_tick_substitution_are_blocked(self):
        original = act.build_authorized_invoke_event
        for change in ("mutate", "substitute"):
            def changed(**kwargs):
                event, tick = original(**kwargs)
                if change == "mutate":
                    kwargs["state"]["mutated"] = True
                else:
                    tick["receipt"]["job_id"] = "other-job"
                return event, tick
            with self.subTest(change=change), patch.object(act, "build_authorized_invoke_event", side_effect=changed):
                with self.assertRaises(self.guard.PreHostCheckError) as caught:
                    self.guard.checked_build_authorized_invoke_event(**self.inputs)
            self.assertIs(caught.exception.host_call_attempted, True)
            self.assertNotIn("mutated", self.inputs["state"])


if __name__ == "__main__":
    unittest.main()
