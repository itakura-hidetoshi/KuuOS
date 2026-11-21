"""v0.51: two original-source-bound but untrusted PlanOS result declarations."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_two_declared_plan_result_claims_v0_51 as subject,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    ROUTES, NO_DATA, BLOCKED,
)
from tests.lean_python_extensions.test_original_verify_plan_certificate_seam_v0_48 import (
    native_certificates,
)
from tests.lean_python_extensions.test_explicit_plan_result_evidence_v0_50 import (
    evidence,
)
from scripts import (
    check_kuuos_lean_python_two_declared_plan_result_claims_sources_v0_51 as pins,
)


def two_claims(v: dict, p: dict) -> dict:
    one = evidence(v, p)
    return {
        "first": {
            "schema_version": subject.SCHEMA,
            "claim_id": "claim-001",
            "claimed_issuer_label": "declared-alpha",
            "supplied_result_evidence": deepcopy(one),
        },
        "second": {
            "schema_version": subject.SCHEMA,
            "claim_id": "claim-002",
            "claimed_issuer_label": "declared-beta",
            "supplied_result_evidence": deepcopy(one),
        },
    }


class TwoDeclaredOriginalPlanResultsV051Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {kind: native_certificates(kind) for kind, _, _, _ in ROUTES}

    def test_all_six_original_routes_agree_only_at_proposal_level(self):
        for kind, _, _, _ in ROUTES:
            with self.subTest(kind=kind):
                v, p = self.cases[kind]
                z = subject.audit_two_declared_plan_result_claims(v, p, two_claims(v, p))
                self.assertEqual(z.status, subject.PROPOSAL_ONLY, z.issues)
                self.assertEqual(z.original_plan_result_state, NO_DATA)
                self.assertTrue(z.original_source_projection_checked)
                self.assertTrue(z.pairwise_agreement_checked)
                self.assertTrue(z.first_supplement_locally_checked)
                self.assertTrue(z.second_supplement_locally_checked)
                self.assertEqual(len(z.result_sets_by_claim), 6)
                self.assertFalse(z.claimed_issuers_independent)
                self.assertFalse(z.external_issuer_authenticated)
                self.assertFalse(z.original_lean_match_proved)
                self.assertFalse(z.host_execution_authorized)

    def test_absent_claims_remain_no_data(self):
        v, p = self.cases["retain"]
        r = subject.audit_two_declared_plan_result_claims(v, p)
        self.assertEqual(r.status, NO_DATA)
        self.assertTrue(r.original_source_projection_checked)
        self.assertFalse(r.pairwise_agreement_checked)

    def test_one_missing_slot_is_no_data_not_consensus(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        del claims["second"]
        self.assertEqual(subject.audit_two_declared_plan_result_claims(v, p, claims).status, NO_DATA)

    def test_duplicate_claim_identifier_does_not_count_as_two(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        claims["second"]["claim_id"] = "claim-001"
        self.assertEqual(subject.audit_two_declared_plan_result_claims(v, p, claims).status, BLOCKED)

    def test_matching_claimed_issuer_labels_do_not_prove_independence(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        claims["second"]["claimed_issuer_label"] = "declared-alpha"
        res = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(res.status, subject.PROPOSAL_ONLY)
        self.assertFalse(res.claimed_issuers_independent)
        self.assertFalse(res.external_issuer_authenticated)

    def test_incompatible_claims_preserve_lineage_disagreement(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        claims["second"]["supplied_result_evidence"]["resulting_lineage_digests"].append("zz-distinct-history")
        result = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(result.status, subject.OBSTRUCTION)
        self.assertEqual(result.conflicting_fields, ("resulting_lineage_digests",))
        self.assertEqual(len(result.result_sets_by_claim), 6)
        self.assertNotEqual(result.result_sets_by_claim[0], result.result_sets_by_claim[3])
        self.assertFalse(result.pairwise_agreement_checked)

    def test_incompatible_claims_preserve_dissent_disagreement(self):
        v, p = self.cases["suspend"]
        claims = two_claims(v, p)
        claims["second"]["supplied_result_evidence"]["resulting_dissent_evidence_digests"].append("zz-dissent")
        result = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(result.status, subject.OBSTRUCTION)
        self.assertEqual(result.conflicting_fields, ("resulting_dissent_evidence_digests",))

    def test_incompatible_claims_preserve_minority_disagreement(self):
        v, p = self.cases["terminate"]
        claims = two_claims(v, p)
        claims["second"]["supplied_result_evidence"]["resulting_minority_evidence_digests"].append("zz-minority")
        result = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(result.status, subject.OBSTRUCTION)
        self.assertEqual(result.conflicting_fields, ("resulting_minority_evidence_digests",))

    def test_multiple_disagreements_are_all_retained_not_voted_away(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        for field in ("resulting_lineage_digests", "resulting_minority_evidence_digests"):
            claims["second"]["supplied_result_evidence"][field].append("zz-disagreement")
        r = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(r.status, subject.OBSTRUCTION)
        self.assertEqual(len(r.conflicting_fields), 2)
        self.assertEqual(len(r.declared_claims), 2)

    def test_wrong_original_plan_digest_blocks_before_comparison(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        claims["second"]["supplied_result_evidence"]["source_planos_certificate_digest"] = "f" * 64
        result = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(result.status, BLOCKED)
        self.assertFalse(result.pairwise_agreement_checked)

    def test_source_lineage_erasure_blocks_before_comparison(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        claims["first"]["supplied_result_evidence"]["resulting_lineage_digests"] = []
        self.assertEqual(subject.audit_two_declared_plan_result_claims(v, p, claims).status, BLOCKED)

    def test_unknown_permission_flag_is_rejected(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        claims["first"]["host_authorized"] = True
        self.assertEqual(subject.audit_two_declared_plan_result_claims(v, p, claims).status, BLOCKED)

    def test_invalid_identifier_type_or_whitespace_blocks(self):
        v, p = self.cases["retain"]
        for bad in ([], 5, " trailing ", ""):
            claims = two_claims(v, p)
            claims["first"]["claim_id"] = bad
            self.assertEqual(subject.audit_two_declared_plan_result_claims(v, p, claims).status, BLOCKED)

    def test_wrong_input_container_fails_closed(self):
        v, p = self.cases["retain"]
        for invalid in ([], object(), "claims"):
            self.assertEqual(subject.audit_two_declared_plan_result_claims(v, p, invalid).status, BLOCKED)

    def test_read_only_does_not_invoke_original_kernels(self):
        v, p = self.cases["retain"]
        claims = two_claims(v, p)
        with patch.object(verify, "build_verifyos_middle_way_conditional_continuity_certificate",
                          side_effect=AssertionError("original verify executed")), patch.object(
                plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
                side_effect=AssertionError("original plan executed")):
            result = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(result.status, subject.PROPOSAL_ONLY)

    def test_input_source_and_two_claims_unmodified(self):
        v, p = deepcopy(self.cases["retain"])
        claims = two_claims(v, p)
        before = deepcopy((v, p, claims))
        result = subject.audit_two_declared_plan_result_claims(v, p, claims)
        self.assertEqual(result.status, subject.PROPOSAL_ONLY)
        self.assertEqual((v, p, claims), before)

    def test_static_source_checker_runs_in_real_runtime_suite(self):
        self.assertEqual(pins.check(), ())

    def test_original_plan_source_tamper_is_detected(self):
        target = pins.ROOT / "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean"
        read = Path.read_bytes
        def mutated(path):
            source = read(path)
            return source + b"\n" if path == target else source
        with patch.object(Path, "read_bytes", mutated):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
                pins.check(),
            )


if __name__ == "__main__":
    unittest.main()
