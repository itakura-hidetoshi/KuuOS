#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_gauge_invariant_dependent_origination_descent_v0_1 import (
    GaugeInvariantDependentOriginationDescentClaim,
    evaluate_gauge_invariant_dependent_origination_descent,
)


class GaugeInvariantDependentOriginationDescentTests(unittest.TestCase):
    def evaluate(self, **changes):
        claim = GaugeInvariantDependentOriginationDescentClaim(**changes)
        return evaluate_gauge_invariant_dependent_origination_descent(claim)

    def test_default_claim_is_candidate(self):
        result = self.evaluate()
        self.assertEqual(result["status"], "CANDIDATE")
        self.assertTrue(result["global_gauge_invariance_theorem_schema_eligible"])
        self.assertTrue(
            result["cross_scale_compatibility_generated_from_exact_global_readout"]
        )

    def test_privileged_representative_is_rejected(self):
        result = self.evaluate(privileges_local_representative_as_real=True)
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(
            result["reason"], "privileged_gauge_representative_is_forbidden"
        )

    def test_orbit_reification_is_rejected(self):
        result = self.evaluate(reifies_gauge_orbit_as_ultimate_substance=True)
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(
            result["reason"], "gauge_orbit_must_not_be_reified_as_paramartha"
        )

    def test_invariance_equivariance_conflation_requires_repair(self):
        result = self.evaluate(conflates_invariance_and_equivariance=True)
        self.assertEqual(result["status"], "REPAIR")
        self.assertEqual(
            result["reason"],
            "separate_semantic_invariance_from_presentation_equivariance",
        )

    def test_same_root_readout_is_required(self):
        result = self.evaluate(exact_same_root_readout_witness=False)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["reason"], "exact_same_root_readout_witness_required")

    def test_interpolation_equivariance_is_required(self):
        result = self.evaluate(interpolation_equivariance_witness=False)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["reason"], "interpolation_equivariance_witness_required")

    def test_local_gauge_invariance_is_required(self):
        result = self.evaluate(local_gauge_invariance_witness=False)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["reason"], "local_gauge_invariance_witness_required")

    def test_dense_union_is_required_for_this_route(self):
        result = self.evaluate(dense_union_of_interpolation_images_witness=False)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(
            result["reason"], "dense_union_witness_required_for_dense_extension_route"
        )

    def test_extension_existence_is_not_inferred_from_compatibility_or_density(self):
        result = self.evaluate(continuous_global_extension_witness=False)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(
            result["reason"],
            "continuous_global_extension_existence_is_a_separate_obligation",
        )
        self.assertFalse(result["continuous_extension_existence_theorem_generated"])
        self.assertFalse(result["global_gauge_invariance_theorem_schema_eligible"])

    def test_no_global_readout_claim_holds(self):
        result = self.evaluate(global_continuous_extension_claimed=False)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(
            result["reason"], "global_relational_readout_not_yet_claimed_or_constructed"
        )

    def test_cross_scale_compatibility_generation_requires_exact_global_readout(self):
        result = self.evaluate(exact_same_root_readout_witness=False)
        self.assertFalse(
            result["cross_scale_compatibility_generated_from_exact_global_readout"]
        )

    def test_two_truths_collapse_is_rejected(self):
        result = self.evaluate(two_truths_noncollapse=False)
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(
            result["reason"],
            "gauge_invariant_samvrti_structure_must_not_collapse_into_paramartha",
        )

    def test_runtime_never_grants_authority(self):
        result = self.evaluate()
        for key in (
            "proof_authority_granted",
            "theorem_authority_granted",
            "truth_authority_granted",
            "essence_authority_granted",
            "clinical_authority_granted",
            "institutional_authority_granted",
            "execution_authority_granted",
        ):
            self.assertFalse(result[key], key)


if __name__ == "__main__":
    unittest.main()
