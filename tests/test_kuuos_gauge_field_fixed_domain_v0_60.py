#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_discrete_gauge_connection_v0_60 import KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import AssociatedField, ConstitutionalGaugeGroup
from runtime.kuuos_gauge_field_self_organization_v0_60 import GaugeConfiguration, evaluate_self_organization_candidate


class GaugeFieldFixedDomainV060Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.group = ConstitutionalGaugeGroup.standard(adaptive_dimension=2)
        self.identity = self.group.identity()

    def field(self, chart: str) -> AssociatedField:
        return AssociatedField(
            field_id=f"field-{chart}",
            chart_id=chart,
            values=(1.0, 1.0, 1.0, 1.0, 0.0, 0.0),
            owner="ObserveOS",
            authority_class="candidate_only",
        )

    def test_plaquette_domain_change_is_blocked(self) -> None:
        connection = KuuConnection(self.group, {
            ("a", "b"): self.identity,
            ("b", "c"): self.identity,
            ("c", "d"): self.identity,
            ("d", "a"): self.identity,
        })
        fields = {chart: self.field(chart) for chart in ("a", "b", "c", "d")}
        source = GaugeConfiguration(self.group, connection, fields, (("a", "b", "c", "d"),))
        candidate = GaugeConfiguration(self.group, connection, fields, ())
        receipt = evaluate_self_organization_candidate(source, candidate)
        self.assertFalse(receipt.admissible)
        self.assertIn("plaquette_domain_changed", receipt.blockers)

    def test_field_identity_change_is_blocked(self) -> None:
        connection = KuuConnection(self.group, {("a", "b"): self.identity})
        fields = {"a": self.field("a"), "b": self.field("b")}
        source = GaugeConfiguration(self.group, connection, fields)
        candidate_fields = dict(fields)
        candidate_fields["a"] = replace(candidate_fields["a"], field_id="field-a-next")
        candidate = GaugeConfiguration(self.group, connection, candidate_fields)
        receipt = evaluate_self_organization_candidate(source, candidate)
        self.assertFalse(receipt.admissible)
        self.assertIn("field_identity_changed", receipt.blockers)


if __name__ == "__main__":
    unittest.main()
