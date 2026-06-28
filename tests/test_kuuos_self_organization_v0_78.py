from __future__ import annotations

import unittest

from runtime.kuuos_self_organization_cycle_v0_78 import (
    diagnose_structure,
    generate_finite_candidates,
    observe_structure,
    run_self_organization_cycle,
)
from runtime.kuuos_self_organization_types_v0_78 import (
    ADOPTED,
    NO_CHANGE,
    ROLLED_BACK,
)
from tests.kuuos_self_organization_fixture_v0_78 import (
    make_context,
    make_policy,
    make_source,
)


class SelfOrganizationV078Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = make_source()
        self.policy = make_policy()
        self.primary = make_context("primary", 0.0, 1.0, 1.0, 1.0)
        self.shadow_a = make_context("shadow-a", 1.0, 1.0, 1.0, 1.0)
        self.shadow_b = make_context("shadow-b", 1.0, 1.0, 0.8, 0.8)
        self.confirm = make_context("confirm", 1.0, 1.0, 0.9, 0.9)

    def test_finite_candidates_exclude_protected_coordinates(self) -> None:
        observation = observe_structure(self.source, self.primary)
        diagnosis = diagnose_structure(self.source, observation, self.primary)
        self.assertTrue(diagnosis.protected_pressure_detected)
        candidates = generate_finite_candidates(
            self.source,
            diagnosis,
            self.policy,
        )
        self.assertTrue(candidates)
        self.assertLessEqual(len(candidates), self.policy.max_candidates)
        for candidate in candidates:
            self.assertLessEqual(
                len(candidate.changes),
                self.policy.max_changed_coordinates,
            )
            for name, _ in candidate.changes:
                self.assertNotIn(name, self.source.protected_coordinates)

    def test_adoption_is_internal_and_deterministic(self) -> None:
        adopted_state, receipt = run_self_organization_cycle(
            "adopt-cycle",
            self.source,
            self.primary,
            (self.shadow_a, self.shadow_b),
            self.confirm,
            self.policy,
        )
        repeated_state, repeated = run_self_organization_cycle(
            "adopt-cycle-repeat",
            self.source,
            self.primary,
            (self.shadow_b, self.shadow_a),
            self.confirm,
            self.policy,
        )
        self.assertEqual(receipt.status, ADOPTED)
        self.assertEqual(adopted_state.revision, self.source.revision + 1)
        self.assertEqual(adopted_state.coordinates, repeated_state.coordinates)
        self.assertEqual(
            receipt.selected_candidate_digest,
            repeated.selected_candidate_digest,
        )
        self.assertFalse(receipt.external_approval_required)
        self.assertFalse(receipt.authority_widening_performed)
        self.assertFalse(receipt.host_state_write_performed)
        self.assertEqual(
            adopted_state.values["authority"],
            self.source.values["authority"],
        )
        self.assertEqual(
            adopted_state.values["audit"],
            self.source.values["audit"],
        )

    def test_failed_reobservation_restores_source(self) -> None:
        rollback_context = make_context(
            "rollback-confirm",
            1.0,
            1.0,
            0.0,
            0.0,
        )
        final_state, receipt = run_self_organization_cycle(
            "rollback-cycle",
            self.source,
            self.primary,
            (self.shadow_a, self.shadow_b),
            rollback_context,
            self.policy,
        )
        self.assertEqual(receipt.status, ROLLED_BACK)
        self.assertEqual(final_state.digest, self.source.digest)
        self.assertTrue(receipt.rollback_performed)
        self.assertTrue(receipt.source_restored_on_failure)
        self.assertFalse(receipt.external_approval_required)

    def test_stable_state_produces_no_change(self) -> None:
        stable = make_context("stable", 1.0, 1.0, 0.0, 0.0)
        final_state, receipt = run_self_organization_cycle(
            "stable-cycle",
            self.source,
            stable,
            (stable,),
            stable,
            self.policy,
        )
        self.assertEqual(receipt.status, NO_CHANGE)
        self.assertEqual(final_state.digest, self.source.digest)
        self.assertEqual(receipt.candidate_digests, ())
        self.assertFalse(receipt.external_approval_required)


if __name__ == "__main__":
    unittest.main()
