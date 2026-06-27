#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_discrete_gauge_connection_v0_60 import KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import AssociatedField, ConstitutionalGaugeGroup, SignedPermutation
from runtime.kuuos_gauge_field_self_organization_v0_60 import GaugeConfiguration, build_covariant_relaxation_candidate, evaluate_self_organization_candidate


class GaugeFieldFixedConnectionV060Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.group = ConstitutionalGaugeGroup.standard(adaptive_dimension=2)
        self.identity = self.group.identity()
        self.swap = SignedPermutation((0, 1, 2, 3, 5, 4), (1, 1, 1, 1, 1, -1))

    def field(self, chart: str, x: float, y: float) -> AssociatedField:
        return AssociatedField(
            field_id=f"field-{chart}",
            chart_id=chart,
            values=(1.0, 1.0, 1.0, 1.0, x, y),
            owner="ObserveOS",
            authority_class="candidate_only",
        )

    def source(self) -> GaugeConfiguration:
        return GaugeConfiguration(
            self.group,
            KuuConnection(self.group, {("a", "b"): self.identity}),
            {"a": self.field("a", 0.0, 0.0), "b": self.field("b", 4.0, 2.0)},
        )

    def test_source_digest_is_default_rollback_target(self) -> None:
        source = self.source()
        candidate = build_covariant_relaxation_candidate(source, rate=0.5)
        receipt = evaluate_self_organization_candidate(source, candidate)
        self.assertTrue(receipt.admissible)
        self.assertEqual(receipt.source_digest, receipt.rollback_digest)

    def test_connection_change_is_blocked(self) -> None:
        source = self.source()
        candidate = GaugeConfiguration(
            self.group,
            KuuConnection(self.group, {("a", "b"): self.swap}),
            source.fields,
        )
        receipt = evaluate_self_organization_candidate(source, candidate)
        self.assertFalse(receipt.admissible)
        self.assertIn("connection_change_not_authorized", receipt.blockers)


if __name__ == "__main__":
    unittest.main()
