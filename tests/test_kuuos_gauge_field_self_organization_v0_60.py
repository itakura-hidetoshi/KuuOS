#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    AssociatedField,
    ConstitutionalGaugeGroup,
    SignedPermutation,
)
from runtime.kuuos_gauge_field_self_organization_v0_60 import (
    GaugeConfiguration,
    KuuConnection,
    build_covariant_relaxation_candidate,
    evaluate_self_organization_candidate,
    gauge_covariance_residual,
)


class GaugeFieldSelfOrganizationV060Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.group = ConstitutionalGaugeGroup.standard(adaptive_dimension=2)
        self.identity = self.group.identity()
        self.swap_adaptive = SignedPermutation(
            permutation=(0, 1, 2, 3, 5, 4),
            signs=(1, 1, 1, 1, 1, -1),
        )
        self.group.require_admissible(self.swap_adaptive)

    def field(self, chart: str, adaptive: tuple[float, float]) -> AssociatedField:
        return AssociatedField(
            field_id=f"field-{chart}",
            chart_id=chart,
            values=(1.0, 1.0, 1.0, 1.0, adaptive[0], adaptive[1]),
            owner="ObserveOS",
            authority_class="candidate_only",
        )

    def test_signed_permutation_inverse_and_constitutional_boundary(self) -> None:
        vector = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        moved = self.swap_adaptive.apply(vector)
        restored = self.swap_adaptive.inverse().apply(moved)
        self.assertEqual(vector, restored)
        self.assertEqual(self.identity, self.swap_adaptive.compose(self.swap_adaptive.inverse()))
        forbidden = SignedPermutation((1, 0, 2, 3, 4, 5), (1, 1, 1, 1, 1, 1))
        with self.assertRaisesRegex(ValueError, "constitutional_gauge_element_forbidden"):
            self.group.require_admissible(forbidden)

    def test_gauge_covariance_and_wilson_invariance(self) -> None:
        connection = KuuConnection(
            self.group,
            {
                ("a", "b"): self.swap_adaptive,
                ("b", "c"): self.identity,
                ("c", "d"): self.swap_adaptive.inverse(),
                ("d", "a"): self.identity,
            },
        )
        configuration = GaugeConfiguration(
            self.group,
            connection,
            {
                "a": self.field("a", (2.0, 3.0)),
                "b": self.field("b", (3.0, -2.0)),
                "c": self.field("c", (3.0, -2.0)),
                "d": self.field("d", (2.0, 3.0)),
            },
            (("a", "b", "c", "d"),),
        )
        local_gauges = {
            "a": self.swap_adaptive,
            "b": self.identity,
            "c": self.swap_adaptive,
            "d": self.identity,
        }
        self.assertLessEqual(gauge_covariance_residual(configuration, local_gauges), 1e-12)
        before = connection.wilson_observable(("a", "b", "c", "d"))
        after = configuration.gauge_transform(local_gauges).connection.wilson_observable(("a", "b", "c", "d"))
        self.assertAlmostEqual(before, after)

    def test_covariant_relaxation_is_bounded_candidate(self) -> None:
        connection = KuuConnection(self.group, {("a", "b"): self.identity})
        source = GaugeConfiguration(
            self.group,
            connection,
            {"a": self.field("a", (0.0, 0.0)), "b": self.field("b", (4.0, 2.0))},
        )
        candidate = build_covariant_relaxation_candidate(source, rate=0.5)
        receipt = evaluate_self_organization_candidate(source, candidate)
        self.assertTrue(receipt.admissible)
        self.assertTrue(receipt.protected_state_preserved)
        self.assertLess(candidate.action().total, source.action().total)
        self.assertEqual(source.protected_state(), candidate.protected_state())

    def test_authority_change_is_blocked_even_when_action_falls(self) -> None:
        connection = KuuConnection(self.group, {("a", "b"): self.identity})
        source = GaugeConfiguration(
            self.group,
            connection,
            {"a": self.field("a", (0.0, 0.0)), "b": self.field("b", (4.0, 2.0))},
        )
        relaxed = build_covariant_relaxation_candidate(source, rate=0.5)
        fields = dict(relaxed.fields)
        fields["a"] = replace(fields["a"], authority_class="execution_authority")
        receipt = evaluate_self_organization_candidate(
            source,
            GaugeConfiguration(self.group, relaxed.connection, fields),
        )
        self.assertFalse(receipt.admissible)
        self.assertIn("field_authority_changed", receipt.blockers)

    def test_protected_coordinate_change_is_blocked(self) -> None:
        connection = KuuConnection(self.group, {("a", "b"): self.identity})
        source = GaugeConfiguration(
            self.group,
            connection,
            {"a": self.field("a", (0.0, 0.0)), "b": self.field("b", (1.0, 1.0))},
        )
        fields = dict(source.fields)
        fields["a"] = replace(fields["a"], values=(0.0, 1.0, 1.0, 1.0, 0.0, 0.0))
        receipt = evaluate_self_organization_candidate(
            source,
            GaugeConfiguration(self.group, source.connection, fields),
        )
        self.assertFalse(receipt.admissible)
        self.assertIn("protected_state_changed", receipt.blockers)


if __name__ == "__main__":
    unittest.main()
