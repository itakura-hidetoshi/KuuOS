"""v0.49: genuine native bounded projection cannot promote unobserved sets."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
    kuuos_lean_python_plan_result_observation_obstruction_v0_49 as subject,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    ROUTES, NO_DATA, BLOCKED,
)
from tests.lean_python_extensions.test_original_verify_plan_certificate_seam_v0_48 import (
    native_certificates, reseal_plan,
)
from scripts import check_kuuos_lean_python_plan_result_obstruction_sources_v0_49 as source_audit


class OriginalPlanMissingResultSetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def test_all_six_original_kernels_produce_bounded_no_data_not_certification(self):
        for kind, _, _, _ in ROUTES:
            with self.subTest(kind=kind):
                verify_cert, plan_cert = self.cases[kind]
                result = subject.audit_original_plan_result_obstruction(verify_cert, plan_cert)
                self.assertEqual(result.status, NO_DATA)
                self.assertTrue(result.source_projection_checked)
                self.assertEqual(result.retained_source_transition, kind)
                self.assertFalse(result.plan_resulting_lineage_observed)
                self.assertFalse(result.plan_resulting_dissent_observed)
                self.assertFalse(result.plan_resulting_minority_observed)
                self.assertFalse(result.universal_lean_cpython_refinement)
                self.assertFalse(result.global_descent_certified)
                self.assertFalse(result.host_execution_permission)
                self.assertEqual(result.native_kernels_invoked, 0)

    def test_missing_original_receipt_is_no_data_without_checked_source(self):
        v, p = self.cases["retain"]
        result = subject.audit_original_plan_result_obstruction(None, p)
        self.assertEqual(result.status, NO_DATA)
        self.assertFalse(result.source_projection_checked)
        self.assertEqual(result.retained_source_transition, None)

    def test_bad_plain_json_type_is_blocked(self):
        _, p = self.cases["retain"]
        for invalid in ([], object(), {"fake": {1, 2}}):
            self.assertEqual(
                subject.audit_original_plan_result_obstruction(invalid, p).status,
                BLOCKED,
            )

    def test_three_unserialized_results_are_not_in_original_native_output(self):
        for _, plan_cert in self.cases.values():
            for field in subject.MISSING_ORIGINAL_OUTPUTS:
                self.assertNotIn(field, plan_cert)

    def test_resealed_forged_lineage_fails_closed(self):
        v, p = deepcopy(self.cases["retain"])
        p["resulting_lineage_digests"] = ["invented-fully-certified"]
        reseal_plan(p)
        result = subject.audit_original_plan_result_obstruction(v, p)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn(
            "unsupported_original_plan_result:resulting_lineage_digests",
            result.issues,
        )

    def test_resealed_forged_dissent_fails_closed(self):
        v, p = deepcopy(self.cases["suspend"])
        p["resulting_dissent_evidence_digests"] = []
        reseal_plan(p)
        result = subject.audit_original_plan_result_obstruction(v, p)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn(
            "unsupported_original_plan_result:resulting_dissent_evidence_digests",
            result.issues,
        )

    def test_resealed_forged_minority_fails_closed(self):
        v, p = deepcopy(self.cases["terminate"])
        p["resulting_minority_evidence_digests"] = ["invented-minority"]
        reseal_plan(p)
        self.assertEqual(
            subject.audit_original_plan_result_obstruction(v, p).status,
            BLOCKED,
        )

    def test_digest_mutation_cannot_transform_no_data_to_authentic(self):
        v, p = deepcopy(self.cases["retain"])
        p["resulting_lineage_digests"] = ["new-packet-claim"]
        reseal_plan(p)
        result = subject.audit_original_plan_result_obstruction(v, p)
        self.assertFalse(result.plan_resulting_lineage_observed)
        self.assertFalse(result.externally_authenticated)
        self.assertFalse(result.host_execution_permission)

    def test_source_certificates_are_not_mutated(self):
        v, p = deepcopy(self.cases["retain"])
        before = deepcopy((v, p))
        result = subject.audit_original_plan_result_obstruction(v, p)
        self.assertEqual(result.status, NO_DATA)
        self.assertEqual(before, (v, p))

    def test_read_only_audit_does_not_rerun_original_kernels(self):
        v, p = self.cases["retain"]
        with patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("no original verify rerun"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("no original plan rerun"),
        ):
            result = subject.audit_original_plan_result_obstruction(v, p)
        self.assertEqual(result.status, NO_DATA)

    def test_actual_original_source_checker_is_executed(self):
        self.assertEqual(source_audit.check(), ())

    def test_checker_detects_pinned_original_source_mutation(self):
        original_read = Path.read_bytes
        target = source_audit.ROOT / (
            "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean"
        )

        def tampered(path):
            original = original_read(path)
            return original + b"\n" if path == target else original

        with patch.object(Path, "read_bytes", tampered):
            errors = source_audit.check()
        self.assertIn(
            "changed_pinned_source:formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
