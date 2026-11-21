"""v0.50 conditional supplied result witness: original kernels remain unchanged."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_explicit_plan_result_evidence_v0_50 as subject,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, ROUTES,
)
from tests.lean_python_extensions.test_original_verify_plan_certificate_seam_v0_48 import (
    native_certificates,
)
from scripts import check_kuuos_lean_python_explicit_result_evidence_sources_v0_50 as audit


def evidence(v: dict, p: dict) -> dict:
    spec = p["source_transition_spec"]
    return {
        "schema_version": subject.SCHEMA,
        "source_verifyos_certificate_digest":
            v["verifyos_middle_way_conditional_continuity_certificate_digest"],
        "source_planos_certificate_digest":
            p["planos_middle_way_bounded_synthesis_intake_certificate_digest"],
        "resulting_lineage_digests": list(spec["resulting_lineage_digests"]),
        "resulting_dissent_evidence_digests":
            list(spec["preserved_dissent_evidence_digests"]),
        "resulting_minority_evidence_digests":
            list(spec["preserved_minority_evidence_digests"]),
    }


class SuppliedPlanResultEvidenceV050Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def test_six_original_routes_remain_no_data_without_new_evidence(self):
        for kind, _, _, _ in ROUTES:
            with self.subTest(kind=kind):
                v, p = self.cases[kind]
                r = subject.audit_supplied_plan_result_evidence(v, p)
                self.assertEqual(r.status, NO_DATA)
                self.assertTrue(r.source_projection_checked)
                self.assertFalse(r.native_result_sets_observed)

    def test_six_supplied_consistent_witnesses_remain_proposal_only(self):
        for kind, _, _, _ in ROUTES:
            with self.subTest(kind=kind):
                v, p = self.cases[kind]
                r = subject.audit_supplied_plan_result_evidence(v, p, evidence(v, p))
                self.assertEqual(r.status, subject.PROPOSAL_ONLY, r.issues)
                self.assertTrue(r.submitted_sets_consistent_with_source)
                self.assertEqual(r.original_plan_result_state, NO_DATA)
                self.assertFalse(r.original_lean_evidence_proof_constructed)
                self.assertFalse(r.external_issuer_authenticated)
                self.assertFalse(r.host_execution_authorized)

    def test_extra_possible_results_are_not_misreported_as_observed(self):
        v, p = self.cases["retain"]
        e = evidence(v, p)
        e["resulting_lineage_digests"].append("zz-extra-unverified")
        r = subject.audit_supplied_plan_result_evidence(v, p, e)
        self.assertEqual(r.status, subject.PROPOSAL_ONLY, r.issues)
        self.assertFalse(r.native_result_sets_observed)

    def test_missing_and_untyped_evidence_fail_closed(self):
        v, p = self.cases["retain"]
        self.assertEqual(subject.audit_supplied_plan_result_evidence(None, p).status, NO_DATA)
        for bad in ([], object(), "caller-claim"):
            self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, bad).status, BLOCKED)

    def test_wrong_source_plan_binding_blocked(self):
        v, p = self.cases["retain"]
        e = evidence(v, p)
        e["source_planos_certificate_digest"] = "0" * 64
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_wrong_source_verify_binding_blocked(self):
        v, p = self.cases["suspend"]
        e = evidence(v, p)
        e["source_verifyos_certificate_digest"] = "0" * 64
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_forged_omission_of_original_lineage_blocked(self):
        v, p = self.cases["retain"]
        e = evidence(v, p)
        e["resulting_lineage_digests"] = []
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_forged_erasure_of_original_dissent_blocked(self):
        v, p = self.cases["suspend"]
        e = evidence(v, p)
        e["resulting_dissent_evidence_digests"] = []
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_forged_erasure_of_original_minority_blocked(self):
        v, p = self.cases["terminate"]
        e = evidence(v, p)
        e["resulting_minority_evidence_digests"] = []
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_noncanonical_duplicated_digests_blocked(self):
        v, p = self.cases["retain"]
        e = evidence(v, p)
        e["resulting_lineage_digests"].append(e["resulting_lineage_digests"][0])
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_unknown_evidence_fields_are_not_admitted(self):
        v, p = self.cases["retain"]
        e = evidence(v, p)
        e["external_authenticated"] = True
        self.assertEqual(subject.audit_supplied_plan_result_evidence(v, p, e).status, BLOCKED)

    def test_original_kernel_is_not_executed_by_audit(self):
        v, p = self.cases["retain"]
        with patch.object(verify, "build_verifyos_middle_way_conditional_continuity_certificate",
                          side_effect=AssertionError("verify executed")), patch.object(
                plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
                side_effect=AssertionError("plan executed")):
            r = subject.audit_supplied_plan_result_evidence(v, p, evidence(v, p))
        self.assertEqual(r.status, subject.PROPOSAL_ONLY)

    def test_original_source_and_supplied_evidence_remain_unmodified(self):
        v, p = deepcopy(self.cases["retain"])
        e = evidence(v, p)
        before = deepcopy((v, p, e))
        r = subject.audit_supplied_plan_result_evidence(v, p, e)
        self.assertEqual(r.status, subject.PROPOSAL_ONLY)
        self.assertEqual(before, (v, p, e))
        self.assertTrue(r.input_source_unchanged)

    def test_static_source_pins_and_new_declarations_checked(self):
        self.assertEqual(audit.check(), ())

    def test_source_checker_rejects_original_plan_mutation(self):
        target = audit.ROOT / "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean"
        read = Path.read_bytes
        def mutated(path):
            value = read(path)
            return value + b"\n" if path == target else value
        with patch.object(Path, "read_bytes", mutated):
            result = audit.check()
        self.assertIn(
            "changed_pinned_source:formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
            result,
        )


if __name__ == "__main__":
    unittest.main()
