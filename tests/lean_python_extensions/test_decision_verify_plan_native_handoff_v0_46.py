"""v0.46 original DecisionOS→VerifyOS→PlanOS six-route native regressions.

Only test fixtures construct a source selection packet. The auditor itself
accepts independently supplied full source envelopes, has no write authority,
and never claims external issuer authenticity.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_decisionos_bounded_plan_synthesis_request_handoff_v0_8 as decision,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
    kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 as prior,
)
from runtime import kuuos_lean_python_decision_verify_plan_native_handoff_v0_46 as subject
from scripts import check_decisionos_bounded_plan_synthesis_request_handoff_v0_8 as decision_fixture
from scripts import check_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify_fixture


def build_original_decision_arguments() -> dict:
    source = decision_fixture._source()
    spec = decision_fixture._spec(source)
    policy = "synthesis-policy-v08"
    recipient = "planos-recipient-v08"
    owner = "decision-owner-v08"
    request = "synthesis-request-v08-001"
    selected = source["selected_candidate_id"]
    intent = "plan-intent-continue-v08"
    constraint_digest = decision.compute_synthesis_constraint_digest(spec)
    bundle = decision.compute_synthesis_handoff_bundle_digest(
        source_selection_receipt_digest=source[
            "decisionos_selection_justification_receipt_digest"
        ],
        synthesis_policy_digest=policy,
        planos_recipient_digest=recipient,
        request_owner_responsibility_digest=owner,
        synthesis_request_id=request,
        requested_selected_candidate_id=selected,
        selected_candidate_plan_intent_digest=intent,
        synthesis_constraint_digest=constraint_digest,
        synthesis_constraint_spec=spec,
    )
    return {
        "source_selection_receipt": source,
        "synthesis_policy_digest": policy,
        "planos_recipient_digest": recipient,
        "request_owner_responsibility_digest": owner,
        "synthesis_request_id": request,
        "requested_selected_candidate_id": selected,
        "selected_candidate_plan_intent_digest": intent,
        "synthesis_constraint_spec": spec,
        "synthesis_constraint_digest": constraint_digest,
        "synthesis_handoff_bundle_digest": bundle,
    }


def _all_nested_digests(packet: dict, key: str) -> list[str]:
    return sorted(set(
        digest
        for values in packet[key].values()
        for digest in values
    ))


def build_original_verify_plan_case(kind: str, decision_receipt: dict) -> dict:
    # Independent fixture cases must not alias one mutable source packet.
    # A local corruption of one route must not silently corrupt other routes.
    decision_receipt = deepcopy(decision_receipt)
    spec = verify_fixture._spec(decision_receipt, kind)
    # Retain the exact DecisionOS source evidence, never replace it with the
    # earlier synthetic VerifyOS test-source strings.
    spec["preserved_dissent_evidence_digests"] = _all_nested_digests(
        decision_receipt, "dissent_preservation_map",
    )
    spec["preserved_minority_evidence_digests"] = _all_nested_digests(
        decision_receipt, "minority_preservation_map",
    )
    transition_digest = verify.compute_transition_spec_digest(spec)
    policy = "middle-way-policy-v04"
    owner = "verify-owner-v04"
    request = "verify-request-v04-001"
    verify_args = {
        "source_handoff_receipt": decision_receipt,
        "verification_policy_digest": policy,
        "verification_owner_responsibility_digest": owner,
        "verification_request_id": request,
        "transition_spec": spec,
        "transition_spec_digest": transition_digest,
        "verification_bundle_digest": verify.compute_verification_bundle_digest(
            source_handoff_receipt_digest=decision_receipt[
                "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
            ],
            verification_policy_digest=policy,
            verification_owner_responsibility_digest=owner,
            verification_request_id=request,
            transition_spec_digest=transition_digest,
            transition_spec=spec,
        ),
    }
    verified = verify.build_verifyos_middle_way_conditional_continuity_certificate(
        **verify_args
    )
    assert verified.status == verify.STATUS_READY, verified.blockers
    assert verified.certificate is not None
    certificate = verified.certificate

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
        "expected_selected_candidate_id": certificate["selected_candidate_id"],
        "expected_selected_candidate_plan_intent_digest": certificate[
            "selected_candidate_plan_intent_digest"
        ],
        "expected_synthesis_constraint_digest": certificate[
            "source_synthesis_constraint_digest"
        ],
        "intake_policy_digest": "planos-intake-policy-v103",
        "planos_intake_responsibility_digest": "planos-owner-v103",
        "intake_request_id": "planos-intake-v103-001",
    }
    plan_args["intake_bundle_digest"] = (
        plan.compute_planos_middle_way_intake_bundle_digest(
            source_verifyos_certificate_digest=certificate[
                "verifyos_middle_way_conditional_continuity_certificate_digest"
            ],
            **{key: value for key, value in plan_args.items()
               if key != "source_verifyos_certificate"}
        )
    )
    original_intake = plan.build_planos_middle_way_bounded_synthesis_intake_certificate(
        **plan_args
    )
    assert original_intake.status == plan.STATUS_READY, original_intake.blockers
    assert original_intake.certificate is not None
    return {"verify": verify_args, "plan": plan_args}


def original_three_stage_fixture() -> tuple[dict, dict]:
    decision_args = build_original_decision_arguments()
    decision_result = decision.build_decisionos_bounded_plan_synthesis_request_handoff_receipt(
        **decision_args
    )
    assert decision_result.status == decision.STATUS_READY, decision_result.blockers
    assert decision_result.receipt is not None
    receipt = decision_result.receipt
    return decision_args, {
        kind: build_original_verify_plan_case(kind, receipt)
        for kind, _, _, _ in prior.ROUTES
    }


class NativeDecisionVerifyPlanSixRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.decision_args, cls.route_cases = original_three_stage_fixture()

    def run_audit(self, decision_args=None, routes=None):
        return subject.audit_original_decision_verify_plan_native_handoff(
            self.decision_args if decision_args is None else decision_args,
            self.route_cases if routes is None else routes,
        )

    def test_original_three_kernel_builders_execute_all_six_routes(self):
        result = self.run_audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.original_decision_cases_run, 1)
        self.assertEqual(result.original_verify_cases_run, 6)
        self.assertEqual(result.original_plan_cases_run, 6)
        self.assertTrue(result.full_decision_verify_packet_seams_checked)
        self.assertTrue(result.original_verify_plan_certificate_seams_checked)
        self.assertEqual(result.route_results, prior.ROUTES)

    def test_six_original_source_packets_have_independent_object_identity(self):
        first = self.route_cases["retain"]["verify"]["source_handoff_receipt"]
        for kind in prior.KIND_TO_STATUS:
            packet = self.route_cases[kind]["verify"]["source_handoff_receipt"]
            self.assertEqual(packet, first)
            if kind != "retain":
                self.assertIsNot(packet, first)

    def test_actual_decision_receipt_is_unchanged_and_shared_whole_packet(self):
        outcome = decision.build_decisionos_bounded_plan_synthesis_request_handoff_receipt(
            **self.decision_args
        )
        self.assertEqual(outcome.status, decision.STATUS_READY)
        for kind in prior.KIND_TO_STATUS:
            self.assertEqual(
                self.route_cases[kind]["verify"]["source_handoff_receipt"],
                outcome.receipt,
            )

    def test_each_original_source_and_caller_input_remains_unchanged(self):
        decision_before = deepcopy(self.decision_args)
        cases_before = deepcopy(self.route_cases)
        result = self.run_audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(self.decision_args, decision_before)
        self.assertEqual(self.route_cases, cases_before)
        self.assertTrue(result.original_decision_source_unchanged)
        self.assertTrue(result.original_verify_plan_sources_unchanged)

    def test_decision_handoff_source_selection_identity_is_retained(self):
        result = self.run_audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(
            result.source_selection_receipt_digest,
            self.decision_args["source_selection_receipt"][
                "decisionos_selection_justification_receipt_digest"
            ],
        )
        self.assertTrue(result.original_decision_handoff_receipt_digest)

    def test_only_retain_has_bounded_intake_not_plan_synthesis(self):
        report = self.run_audit()
        self.assertEqual(report.status, subject.SCOPED_COMPATIBLE, report.issues)
        self.assertEqual(
            [(route, admitted) for route, _, _, admitted in report.route_results],
            [(route, route == "retain") for route, _, _, _ in prior.ROUTES],
        )
        self.assertFalse(report.plan_synthesis_performed)
        self.assertFalse(report.execution_permission_granted)

    def test_all_advisory_boundaries_remain_false(self):
        result = self.run_audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        self.assertTrue(result.read_only)
        for name in (
            "external_source_authenticated", "global_descent_proved",
            "plan_synthesis_performed", "execution_permission_granted",
            "git_or_memory_written", "original_kernel_modified",
        ):
            self.assertIs(getattr(result, name), False, name)

    def test_missing_original_decision_or_cases_is_no_data(self):
        self.assertEqual(
            subject.audit_original_decision_verify_plan_native_handoff(
                None, self.route_cases,
            ).status, subject.NO_DATA,
        )
        self.assertEqual(
            subject.audit_original_decision_verify_plan_native_handoff(
                self.decision_args, None,
            ).status, subject.NO_DATA,
        )

    def test_missing_each_one_of_six_native_cases_is_no_data(self):
        for kind in prior.KIND_TO_STATUS:
            with self.subTest(kind=kind):
                cases = deepcopy(self.route_cases)
                cases.pop(kind)
                self.assertEqual(self.run_audit(routes=cases).status,
                                 subject.NO_DATA)

    def test_unknown_extra_case_is_blocked(self):
        cases = deepcopy(self.route_cases)
        cases["not_a_route"] = cases["retain"]
        self.assertEqual(self.run_audit(routes=cases).status, subject.BLOCKED)

    def test_missing_or_extra_decision_input_is_blocked(self):
        inputs = deepcopy(self.decision_args)
        inputs.pop("synthesis_handoff_bundle_digest")
        self.assertEqual(self.run_audit(decision_args=inputs).status,
                         subject.BLOCKED)
        inputs = deepcopy(self.decision_args)
        inputs["invented_parameter"] = "forged"
        self.assertEqual(self.run_audit(decision_args=inputs).status,
                         subject.BLOCKED)

    def test_forged_selection_receipt_is_rejected_by_original_decision(self):
        inputs = deepcopy(self.decision_args)
        inputs["source_selection_receipt"]["selected_candidate_id"] = "repair"
        report = self.run_audit(decision_args=inputs)
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("decision:original_handoff_not_ready", report.issues)

    def test_original_decision_to_verify_full_packet_substitution_is_blocked(self):
        cases = deepcopy(self.route_cases)
        cases["retain"]["verify"]["source_handoff_receipt"][
            "retained_alternative_candidate_ids"
        ] = []
        report = self.run_audit(routes=cases)
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("retain:original_decision_verify_full_receipt_mismatch",
                      report.issues)
        self.assertEqual(report.original_verify_cases_run, 0)
        self.assertEqual(report.original_plan_cases_run, 0)

    def test_original_decision_to_verify_digest_only_is_insufficient(self):
        cases = deepcopy(self.route_cases)
        cases["suspend"]["verify"]["source_handoff_receipt"][
            "minority_preservation_map"
        ] = {}
        report = self.run_audit(routes=cases)
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("suspend:original_decision_verify_full_receipt_mismatch",
                      report.issues)

    def test_verify_to_plan_whole_certificate_substitution_is_rejected(self):
        cases = deepcopy(self.route_cases)
        cases["retain"]["plan"]["source_verifyos_certificate"] = cases[
            "suspend"
        ]["plan"]["source_verifyos_certificate"]
        report = self.run_audit(routes=cases)
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn(
            "verify_plan:retain:original_full_certificate_seam_mismatch",
            report.issues,
        )

    def test_dissent_and_minority_evidence_are_native_original_values(self):
        receipt = self.route_cases["retain"]["verify"]["source_handoff_receipt"]
        dissent = _all_nested_digests(receipt, "dissent_preservation_map")
        minority = _all_nested_digests(receipt, "minority_preservation_map")
        self.assertTrue(dissent)
        self.assertTrue(minority)
        for kind in prior.KIND_TO_STATUS:
            spec = self.route_cases[kind]["verify"]["transition_spec"]
            self.assertTrue(set(dissent).issubset(
                set(spec["preserved_dissent_evidence_digests"])
            ))
            self.assertTrue(set(minority).issubset(
                set(spec["preserved_minority_evidence_digests"])
            ))

    def test_native_source_dissent_erasure_blocks(self):
        cases = deepcopy(self.route_cases)
        cases["request_revision"]["verify"]["transition_spec"][
            "preserved_dissent_evidence_digests"
        ] = []
        report = self.run_audit(routes=cases)
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("verify_plan:request_revision:original_verify_not_ready",
                      report.issues)

    def test_native_decision_policy_drift_blocks(self):
        inputs = deepcopy(self.decision_args)
        inputs["synthesis_policy_digest"] = "different-policy"
        report = self.run_audit(decision_args=inputs)
        self.assertEqual(report.status, subject.BLOCKED)

    def test_nonfinite_and_nonplain_data_fail_closed(self):
        for value in (float("nan"), float("inf"), object()):
            with self.subTest(name=type(value).__name__):
                cases = deepcopy(self.route_cases)
                cases["retain"]["verify"]["test_unknown"] = value
                self.assertEqual(self.run_audit(routes=cases).status,
                                 subject.BLOCKED)

    def test_non_dict_arguments_fail_without_executing_original_kernels(self):
        self.assertEqual(
            subject.audit_original_decision_verify_plan_native_handoff(
                ["not native"], self.route_cases
            ).status, subject.BLOCKED,
        )
        self.assertEqual(
            subject.audit_original_decision_verify_plan_native_handoff(
                self.decision_args, ["not native"]
            ).status, subject.BLOCKED,
        )

    def test_invalid_original_builder_output_never_proves_compatibility(self):
        with patch.object(
            decision, "build_decisionos_bounded_plan_synthesis_request_handoff_receipt",
            return_value=decision.DecisionOSBoundedPlanSynthesisRequestHandoffResult(
                decision.STATUS_BLOCKED, ["simulated"], None,
            ),
        ):
            self.assertEqual(self.run_audit().status, subject.BLOCKED)


if __name__ == "__main__":
    unittest.main()
