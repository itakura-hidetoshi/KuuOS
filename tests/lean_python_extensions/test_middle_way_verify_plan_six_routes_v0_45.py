"""v0.45 six actual VerifyOS and PlanOS builders, full certificate seams.

Fixtures are constructed from the repository's ORIGINAL test-input builders,
then passed to the actual unchanged VerifyOS and PlanOS Python kernels.
No local fixture is treated as external issuer or production-world evidence.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as native_plan,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as native_verify,
)
from scripts import (
    check_verifyos_middle_way_conditional_continuity_verification_v0_4 as fixture,
)
from runtime import kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 as subject


def build_native_case(kind: str) -> dict:
    """Only a TEST fixture constructs the earlier DecisionOS handoff packet."""
    source = fixture._source()
    spec = fixture._spec(source, kind)
    digest = native_verify.compute_transition_spec_digest(spec)
    policy = "middle-way-policy-v04"
    verify_owner = "verify-owner-v04"
    request = "verify-request-v04-001"
    verify_args = {
        "source_handoff_receipt": source,
        "verification_policy_digest": policy,
        "verification_owner_responsibility_digest": verify_owner,
        "verification_request_id": request,
        "transition_spec": spec,
        "transition_spec_digest": digest,
        "verification_bundle_digest": native_verify.compute_verification_bundle_digest(
            source_handoff_receipt_digest=source[
                "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
            ],
            verification_policy_digest=policy,
            verification_owner_responsibility_digest=verify_owner,
            verification_request_id=request,
            transition_spec_digest=digest,
            transition_spec=spec,
        ),
    }
    result = native_verify.build_verifyos_middle_way_conditional_continuity_certificate(
        **verify_args,
    )
    assert result.status == native_verify.STATUS_READY and result.certificate
    certificate = result.certificate
    intake_policy = "planos-intake-policy-v103"
    intake_owner = "planos-owner-v103"
    intake_id = "planos-intake-v103-001"
    plan_args = {
        "source_verifyos_certificate": certificate,
        "expected_source_verifyos_certificate_digest": certificate[
            "verifyos_middle_way_conditional_continuity_certificate_digest"
        ],
        "expected_source_handoff_receipt_digest": certificate[
            "source_handoff_receipt_digest"
        ],
        "expected_world_binding_digest": certificate[
            "source_world_binding_digest"
        ],
        "expected_world_model_state_digest": certificate[
            "source_world_model_state_digest"
        ],
        "expected_world_model_revision": certificate[
            "source_world_model_revision"
        ],
        "expected_world_lineage_digest": certificate[
            "source_world_lineage_digest"
        ],
        "expected_selected_candidate_id": certificate[
            "selected_candidate_id"
        ],
        "expected_selected_candidate_plan_intent_digest": certificate[
            "selected_candidate_plan_intent_digest"
        ],
        "expected_synthesis_constraint_digest": certificate[
            "source_synthesis_constraint_digest"
        ],
        "intake_policy_digest": intake_policy,
        "planos_intake_responsibility_digest": intake_owner,
        "intake_request_id": intake_id,
    }
    plan_args["intake_bundle_digest"] = (
        native_plan.compute_planos_middle_way_intake_bundle_digest(
            **{name: value for name, value in plan_args.items()
               if name != "source_verifyos_certificate"}
        )
    )
    # Confirm that the *actual* PlanOS kernel accepts the original data.
    plan_result = native_plan.build_planos_middle_way_bounded_synthesis_intake_certificate(
        **plan_args,
    )
    assert plan_result.status == native_plan.STATUS_READY, plan_result.blockers
    assert plan_result.certificate is not None
    return {"verify": verify_args, "plan": plan_args}


class OriginalVerifyPlanSixRoutesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {
            kind: build_native_case(kind)
            for kind, _, _, _ in subject.ROUTES
        }

    def audit(self, supplied=None):
        return subject.audit_original_verify_plan_six_routes(
            self.cases if supplied is None else supplied,
        )

    def test_all_six_original_verify_and_plan_kernels_run(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.original_verify_cases_run, 6)
        self.assertEqual(result.original_plan_cases_run, 6)
        self.assertTrue(result.original_python_source_tables_checked)
        self.assertTrue(result.complete_original_certificate_seams_checked)
        self.assertTrue(result.original_source_inputs_unchanged)
        self.assertEqual(result.route_results, subject.ROUTES)
        self.assertEqual(len(result.original_certificate_digest_pairs), 6)
        self.assertTrue(result.source_handoff_receipt_digest)

    def test_six_routes_preserve_separate_conditional_statuses(self):
        report = self.audit()
        self.assertEqual(report.status, subject.SCOPED_COMPATIBLE)
        self.assertEqual(set(report.route_results), set(subject.ROUTES))
        self.assertEqual({row[1] for row in report.route_results},
                         set(subject.STATUS_TO_DISPOSITION))

    def test_only_retain_is_admitted_without_executing_plan(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        self.assertEqual(
            [(kind, admitted) for kind, _, _, admitted in result.route_results],
            [(kind, kind == "retain") for kind, _, _, _ in subject.ROUTES],
        )
        self.assertFalse(result.plan_synthesis_performed)
        self.assertFalse(result.execution_permission_granted)

    def test_superseded_requests_lineage_reverification_not_synthesis(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        mapping = {kind: (disposition, admitted)
                   for kind, _, disposition, admitted in result.route_results}
        self.assertEqual(mapping["supersede_with_lineage"],
                         ("successor_lineage_reverification_required", False))

    def test_terminated_and_completed_do_not_synthesize(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        values = {kind: (disposition, admitted)
                  for kind, _, disposition, admitted in result.route_results}
        self.assertEqual(values["terminate"],
                         ("terminate_without_synthesis", False))
        self.assertEqual(values["complete"],
                         ("close_without_synthesis", False))

    def test_no_python_source_is_mutated(self):
        before = deepcopy(self.cases)
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(before, self.cases)
        self.assertFalse(result.original_kernel_modified)

    def test_original_verify_to_plan_certificate_binding_is_entire_packet(self):
        report = self.audit()
        self.assertEqual(report.status, subject.SCOPED_COMPATIBLE)
        for kind, original_verify_sha, original_plan_sha in (
            report.original_certificate_digest_pairs
        ):
            self.assertEqual(original_verify_sha, self.cases[kind]["plan"][
                "source_verifyos_certificate"
            ]["verifyos_middle_way_conditional_continuity_certificate_digest"])
            self.assertEqual(len(original_verify_sha), 64)
            self.assertEqual(len(original_plan_sha), 64)

    def test_missing_all_case_inventory_is_no_data(self):
        self.assertEqual(subject.audit_original_verify_plan_six_routes(None).status,
                         subject.NO_DATA)

    def test_missing_each_one_of_six_cases_is_no_data(self):
        for kind in subject.KIND_TO_STATUS:
            with self.subTest(kind=kind):
                cases = deepcopy(self.cases)
                cases.pop(kind)
                self.assertEqual(self.audit(cases).status, subject.NO_DATA)

    def test_unexpected_extra_transition_is_blocked(self):
        data = deepcopy(self.cases)
        data["invented"] = data["retain"]
        self.assertEqual(self.audit(data).status, subject.BLOCKED)

    def test_custom_mapping_cannot_invoke_conversion_hooks(self):
        class MaliciousInput:
            def items(self):
                raise AssertionError("injected custom conversion")
        self.assertEqual(self.audit(MaliciousInput()).status, subject.BLOCKED)
        self.assertEqual(self.audit([]).status, subject.BLOCKED)

    def test_original_verify_certificate_substituted_in_plan_envelope_blocks(self):
        data = deepcopy(self.cases)
        data["retain"]["plan"]["source_verifyos_certificate"] = data[
            "suspend"
        ]["plan"]["source_verifyos_certificate"]
        result = self.audit(data)
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("retain:original_full_certificate_seam_mismatch",
                      result.issues)

    def test_consistent_but_different_plan_policy_digest_is_rejected(self):
        cases = deepcopy(self.cases)
        cases["retain"]["plan"]["intake_policy_digest"] = "substituted-policy"
        result = self.audit(cases)
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("retain:original_intake_not_ready", result.issues)

    def test_source_receipt_forgery_fails_original_verify(self):
        cases = deepcopy(self.cases)
        cases["retain"]["verify"]["source_handoff_receipt"][
            "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
        ] = "forged-source-receipt"
        result = self.audit(cases)
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("retain:original_verify_not_ready", result.issues)

    def test_source_lineage_erasure_is_rejected_by_native_verify(self):
        cases = deepcopy(self.cases)
        cases["request_revision"]["verify"]["transition_spec"][
            "resulting_lineage_digests"
        ] = []
        result = self.audit(cases)
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("request_revision:original_verify_not_ready", result.issues)

    def test_real_python_route_table_drift_is_not_a_model_witness(self):
        patched = dict(native_plan.STATUS_TO_DISPOSITION)
        patched["superseded"] = "close_without_synthesis"
        with patch.object(native_plan, "STATUS_TO_DISPOSITION", patched):
            report = self.audit()
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("original_kernels:finite_routing_tables_changed",
                      report.issues)

    def test_rejected_original_verification_does_not_run_intake_for_that_case(self):
        cases = deepcopy(self.cases)
        cases["terminate"]["verify"]["verification_policy_digest"] = ""
        report = self.audit(cases)
        self.assertEqual(report.status, subject.BLOCKED, report.issues)
        self.assertEqual(report.original_plan_cases_run, 5)

    def test_undocumented_original_arguments_are_not_accepted(self):
        cases = deepcopy(self.cases)
        cases["retain"]["verify"]["extra_parameter"] = True
        self.assertEqual(self.audit(cases).status, subject.BLOCKED)
        cases = deepcopy(self.cases)
        cases["retain"]["plan"].pop("intake_bundle_digest")
        self.assertEqual(self.audit(cases).status, subject.BLOCKED)

    def test_original_boolean_permission_values_must_be_exact(self):
        cases = deepcopy(self.cases)
        cases["retain"]["verify"]["source_handoff_receipt"][
            "execution_permission"
        ] = 0
        self.assertEqual(self.audit(cases).status, subject.BLOCKED)

    def test_nonfinite_opaque_or_recursive_input_is_blocked(self):
        for value in (float("nan"), float("inf"), object()):
            with self.subTest(value=type(value).__name__):
                cases = deepcopy(self.cases)
                cases["retain"]["verify"]["test_unknown"] = value
                self.assertEqual(self.audit(cases).status, subject.BLOCKED)

    def test_source_identifier_differs_between_cases_blocks_cross_case(self):
        # A separately authored DecisionOS handoff is not a shared native
        # mission context merely because both certificate builders accept it.
        cases = deepcopy(self.cases)
        other = deepcopy(cases["retain"]["verify"]["source_handoff_receipt"])
        other["selected_candidate_id"] = "different"
        other.pop("decisionos_bounded_plan_synthesis_request_handoff_receipt_digest")
        other["decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"] = (
            native_verify.canonical_digest(other)
        )
        cases["suspend"] = build_native_case("suspend")
        cases["suspend"]["verify"]["source_handoff_receipt"] = other
        # Cached spec+bundle now mismatch, so at least one original source
        # check rejects before unjustified cross-case elevation.
        report = self.audit(cases)
        self.assertEqual(report.status, subject.BLOCKED)

    def test_no_host_authority_from_any_ready_certificate(self):
        report = self.audit()
        self.assertEqual(report.status, subject.SCOPED_COMPATIBLE)
        self.assertEqual(
            dict(report.read_only_consumer_advice),
            dict(subject.CHECKED_ADVICE),
        )
        for key in (
            "lean_model_witness_constructed_by_this_python_process",
            "lean_cpython_refinement_proved",
            "globally_atomic_six_case_history_proved",
            "external_source_authenticated",
            "common_causal_clock_proved",
            "global_descent_proved",
            "verification_grants_truth_authority",
            "selection_authority_granted_to_planos",
            "plan_synthesis_performed",
            "execution_permission_granted",
            "host_action_performed",
            "memoryos_write_performed",
            "git_authority_granted",
            "original_kernel_modified",
        ):
            self.assertIs(getattr(report, key), False, key)

    def test_negative_evidence_preserved_without_cancelling_other_cases(self):
        cases = deepcopy(self.cases)
        cases["suspend"]["verify"]["verification_request_id"] = ""
        result = self.audit(cases)
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertEqual(result.original_verify_cases_run, 6)
        self.assertEqual(result.original_plan_cases_run, 5)
        self.assertIn("suspend:original_verify_not_ready", result.issues)


if __name__ == "__main__":
    unittest.main()
