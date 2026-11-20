"""Independent v0.48 original VerifyOS/PlanOS certificate projection tests."""
from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime import (
    kuuos_lean_python_original_verify_plan_certificate_seam_v0_48 as subject,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import ROUTES, NO_DATA, BLOCKED
from tests.lean_python_extensions.test_middle_way_verify_plan_six_routes_v0_45 import (
    build_native_case,
)


def native_certificates(kind: str) -> tuple[dict, dict]:
    case = build_native_case(kind)
    vr = verify.build_verifyos_middle_way_conditional_continuity_certificate(**case["verify"])
    pr = plan.build_planos_middle_way_bounded_synthesis_intake_certificate(**case["plan"])
    assert vr.status == verify.STATUS_READY and type(vr.certificate) is dict
    assert pr.status == plan.STATUS_READY and type(pr.certificate) is dict
    return vr.certificate, pr.certificate


def reseal_plan(p: dict) -> None:
    key = "planos_middle_way_bounded_synthesis_intake_certificate_digest"
    p[key] = plan.canonical_digest({name: val for name, val in p.items() if name != key})


class OriginalCertificateProjectionV048Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def test_all_six_genuine_original_certificates_have_bounded_projections(self):
        for kind, _, _, admitted in ROUTES:
            with self.subTest(kind=kind):
                v, p = self.native[kind]
                result = subject.audit_original_certificates(v, p)
                self.assertEqual(result.status, subject.SCOPED, result.issues)
                self.assertEqual(result.transition_kind, kind)
                self.assertIs(result.bounded_intake_admitted, admitted)
                self.assertTrue(result.exact_original_source_projection_checked)
                self.assertTrue(result.original_provenance_monotonicity_checked)
                self.assertTrue(result.resulting_plan_responsibility_checked)
                self.assertFalse(result.plan_resulting_lineage_finset_certified)
                self.assertFalse(result.lean_cpython_refinement_certified)
                self.assertFalse(result.execution_authority_granted)
                self.assertEqual(result.native_kernel_invocations, 0)

    def test_missing_and_foreign_input_fail_closed(self):
        v, p = self.native["retain"]
        self.assertEqual(subject.audit_original_certificates(None, p).status, NO_DATA)
        self.assertEqual(subject.audit_original_certificates(v, None).status, NO_DATA)
        for invalid in ([], "not-json", object()):
            self.assertEqual(subject.audit_original_certificates(invalid, p).status, BLOCKED)

    def test_plain_json_arguments_are_not_mutated(self):
        v, p = deepcopy(self.native["retain"])
        before = deepcopy((v, p))
        result = subject.audit_original_certificates(v, p)
        self.assertEqual(result.status, subject.SCOPED, result.issues)
        self.assertEqual((v, p), before)

    def test_projection_invokes_no_original_kernel_again(self):
        v, p = self.native["retain"]
        with patch.object(verify, "build_verifyos_middle_way_conditional_continuity_certificate",
                          side_effect=AssertionError("must not execute")), patch.object(
                plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
                side_effect=AssertionError("must not execute")):
            result = subject.audit_original_certificates(v, p)
        self.assertEqual(result.status, subject.SCOPED, result.issues)

    def test_resealed_substituted_transition_spec_still_blocks(self):
        v, p = deepcopy(self.native["retain"])
        p["source_transition_spec"] = deepcopy(self.native["suspend"][1]["source_transition_spec"])
        reseal_plan(p)
        result = subject.audit_original_certificates(v, p)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("original_transition_spec_seam_mismatch", result.issues)

    def test_resealed_false_approval_on_nonretain_blocks(self):
        v, p = deepcopy(self.native["terminate"])
        p["bounded_synthesis_request_admitted"] = True
        reseal_plan(p)
        self.assertEqual(subject.audit_original_certificates(v, p).status, BLOCKED)

    def test_resealed_wrong_source_receipt_blocks(self):
        v, p = deepcopy(self.native["retain"])
        p["source_decisionos_handoff_receipt_digest"] = "f" * 64
        reseal_plan(p)
        result = subject.audit_original_certificates(v, p)
        self.assertIn("original_source_field_mismatch:source_handoff_receipt_digest",
                      result.issues)

    def test_resealed_erased_plan_responsibility_blocks(self):
        v, p = deepcopy(self.native["retain"])
        p["resulting_responsibility_lineage_digests"] = []
        reseal_plan(p)
        self.assertIn("plan_responsibility_extension_mismatch",
                      subject.audit_original_certificates(v, p).issues)

    def test_resealed_authority_escalation_blocks(self):
        v, p = deepcopy(self.native["retain"])
        p["execution_authority_granted"] = True
        reseal_plan(p)
        self.assertEqual(subject.audit_original_certificates(v, p).status, BLOCKED)

    def test_resealed_integer_instead_of_boolean_blocks(self):
        v, p = deepcopy(self.native["suspend"])
        p["bounded_synthesis_request_admitted"] = 0
        reseal_plan(p)
        self.assertEqual(subject.audit_original_certificates(v, p).status, BLOCKED)



    def test_v048_exact_original_source_checker_runs_in_runtime_ci(self):
        """The real source pin checker must run, not merely exist on disk."""
        from scripts import (
            check_kuuos_lean_python_original_verify_plan_cert_seam_sources_v0_48 as audit,
        )
        self.assertEqual(audit.check(), ())

    def test_v048_source_checker_rejects_modified_original_lean_bytes(self):
        from pathlib import Path
        from scripts import (
            check_kuuos_lean_python_original_verify_plan_cert_seam_sources_v0_48 as audit,
        )
        target = audit.ROOT / "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean"
        real_read = Path.read_bytes

        def changed(path):
            raw = real_read(path)
            return raw + b"\\n" if path == target else raw

        with patch.object(Path, "read_bytes", changed):
            result = audit.check()
        self.assertIn(
            "pinned_source_modified:formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean",
            result,
        )

    def test_v048_source_checker_rejects_missing_formal_proof_declaration(self):
        from pathlib import Path
        from scripts import (
            check_kuuos_lean_python_original_verify_plan_cert_seam_sources_v0_48 as audit,
        )
        target = audit.ROOT / audit.NEW_LEAN
        real_read = Path.read_text

        def missing_declaration(path, *args, **kwargs):
            source = real_read(path, *args, **kwargs)
            if path == target:
                return source.replace(
                    "theorem original_status_transport",
                    "theorem replaced_status_transport", 1,
                )
            return source

        with patch.object(Path, "read_text", missing_declaration):
            result = audit.check()
        self.assertIn("missing_declaration:theorem original_status_transport", result)

if __name__ == "__main__":
    unittest.main()
