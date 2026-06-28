from __future__ import annotations

import unittest

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
    run_deterministic_alignment_trace,
)
from runtime.kuuos_repository_repair_cycle_v0_79 import run_repository_repair_cycle
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure
from runtime.kuuos_repository_structure_types_v0_79 import NO_CHANGE
from tests.kuuos_repository_repair_fixture_v0_79 import defective_repository_snapshot


class RepositoryAlignmentNormalFormV080Tests(unittest.TestCase):
    def test_all_candidate_orders_converge_to_one_terminal(self) -> None:
        snapshot = defective_repository_snapshot()
        certificate = certify_repository_alignment_normal_form(snapshot)
        self.assertEqual(certificate.initial_score, 70)
        self.assertEqual(certificate.explored_state_count, 16)
        self.assertEqual(certificate.explored_transition_count, 32)
        self.assertEqual(certificate.terminal_scores, (0,))
        self.assertTrue(certificate.all_transitions_strictly_decreasing)
        self.assertTrue(certificate.all_terminals_fixed_points)
        self.assertTrue(certificate.unique_terminal)
        self.assertTrue(certificate.unique_terminal_digest)
        self.assertTrue(certificate.deterministic_trace_matches_terminal)
        self.assertFalse(certificate.external_approval_required)
        self.assertTrue(certificate.certificate_digest)

    def test_deterministic_trace_is_strict_and_finite(self) -> None:
        snapshot = defective_repository_snapshot()
        final_snapshot, trace = run_deterministic_alignment_trace(snapshot)
        self.assertEqual(trace.initial_score, 70)
        self.assertEqual(trace.final_score, 0)
        self.assertEqual(trace.score_sequence, (70, 50, 30, 10, 0))
        self.assertEqual(len(trace.transition_digests), 4)
        self.assertTrue(trace.fixed_point_reached)
        self.assertEqual(final_snapshot.digest, trace.final_snapshot_digest)
        self.assertTrue(trace.trace_digest)

    def test_existing_normal_form_is_single_terminal(self) -> None:
        snapshot = defective_repository_snapshot()
        for index in range(5):
            snapshot, receipt = run_repository_repair_cycle(
                f"normal-form-fixture-{index}",
                snapshot,
            )
            if receipt.status == NO_CHANGE:
                break
        self.assertEqual(observe_repository_structure(snapshot).weighted_defect_score, 0)
        certificate = certify_repository_alignment_normal_form(snapshot)
        self.assertEqual(certificate.explored_state_count, 1)
        self.assertEqual(certificate.explored_transition_count, 0)
        self.assertEqual(certificate.terminal_scores, (0,))
        self.assertTrue(certificate.unique_terminal)
        self.assertEqual(certificate.unique_terminal_digest, snapshot.digest)

    def test_state_bound_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "alignment_state_bound_exceeded"):
            certify_repository_alignment_normal_form(
                defective_repository_snapshot(),
                max_states=4,
            )

    def test_cycle_bound_does_not_claim_fixed_point_early(self) -> None:
        _, trace = run_deterministic_alignment_trace(
            defective_repository_snapshot(),
            max_cycles=2,
        )
        self.assertEqual(trace.final_score, 30)
        self.assertFalse(trace.fixed_point_reached)


if __name__ == "__main__":
    unittest.main()
