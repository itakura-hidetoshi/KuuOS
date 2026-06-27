#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_discrete_gauge_connection_v0_60 import KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import AssociatedField, SignedPermutation
from runtime.kuuos_os_curvature_holonomy_v0_61 import (
    OSGaugeBundle,
    decompose_os_curvature,
    memory_holonomy,
    os_gauge_invariance_residual,
)
from runtime.kuuos_os_gauge_field_types_v0_61 import (
    ChannelPreservingGaugeGroup,
    OSAssociatedGaugeField,
    os_field_values,
)


class OSCurvatureHolonomyV061Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.group = ChannelPreservingGaugeGroup()
        self.identity = self.group.identity()
        self.channel_swap = SignedPermutation(
            permutation=(0, 1, 2, 3, 5, 4, 6, 8, 7, 10, 9, 11),
            signs=(1,) * 12,
        )
        self.channel_sign = SignedPermutation(
            permutation=tuple(range(12)),
            signs=(1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1),
        )
        self.group.require_admissible(self.channel_swap)
        self.group.require_admissible(self.channel_sign)

    def field(
        self,
        role: str,
        chart: str,
        *,
        support: float,
        uncertainty: float,
        contradiction: float,
        criterion: float,
        debt: float,
        history: float,
        residue: float,
        prediction: float,
    ) -> OSAssociatedGaugeField:
        associated = AssociatedField(
            field_id=f"{role}-field",
            chart_id=chart,
            values=os_field_values(
                evidence_support=support,
                uncertainty=uncertainty,
                contradiction=contradiction,
                criterion_coverage=criterion,
                verification_debt=debt,
                history_depth=history,
                residue_load=residue,
                predictive_uncertainty=prediction,
            ),
            owner=role.capitalize() + "OS",
            authority_class="non_authoritative",
            lineage_digest=f"{role}-source-digest",
        )
        return OSAssociatedGaugeField(
            role=role,
            source_version=f"{role}-version",
            source_digest=f"{role}-source-digest",
            boundary_digest=f"{role}-boundary-digest",
            field=associated,
        )

    def fields(self) -> dict[str, OSAssociatedGaugeField]:
        return {
            "observe": self.field(
                "observe",
                "observe",
                support=0.9,
                uncertainty=0.1,
                contradiction=0.1,
                criterion=0.0,
                debt=1.0,
                history=0.7,
                residue=0.0,
                prediction=1.0,
            ),
            "verify": self.field(
                "verify",
                "verify",
                support=0.85,
                uncertainty=0.15,
                contradiction=0.0,
                criterion=0.95,
                debt=0.0,
                history=0.8,
                residue=0.0,
                prediction=0.15,
            ),
            "memory": self.field(
                "memory",
                "memory",
                support=0.8,
                uncertainty=0.2,
                contradiction=0.2,
                criterion=0.0,
                debt=0.0,
                history=0.5,
                residue=0.2,
                prediction=0.25,
            ),
        }

    def bundle(self, *, twisted: bool = False) -> OSGaugeBundle:
        connection = KuuConnection(
            self.group,
            {
                ("observe", "verify"): self.identity,
                ("verify", "memory"): self.identity,
                ("memory", "observe"): self.channel_swap if twisted else self.identity,
            },
        )
        return OSGaugeBundle(self.group, connection, self.fields())

    def test_cross_channel_gauge_transformation_is_rejected(self) -> None:
        cross_channel = SignedPermutation(
            permutation=(0, 1, 2, 3, 7, 5, 6, 4, 8, 9, 10, 11),
            signs=(1,) * 12,
        )
        with self.assertRaisesRegex(ValueError, "os_channel_gauge_element_forbidden"):
            self.group.require_admissible(cross_channel)

    def test_curvature_decomposes_into_three_nonnegative_channels(self) -> None:
        receipt = decompose_os_curvature(self.bundle())
        self.assertGreaterEqual(receipt.epistemic_curvature, 0.0)
        self.assertGreaterEqual(receipt.verification_curvature, 0.0)
        self.assertGreaterEqual(receipt.memory_return_curvature, 0.0)
        self.assertAlmostEqual(
            receipt.total_curvature,
            receipt.epistemic_curvature
            + receipt.verification_curvature
            + receipt.memory_return_curvature,
        )

    def test_channel_curvature_and_memory_holonomy_are_gauge_invariant(self) -> None:
        bundle = self.bundle(twisted=True)
        residual = os_gauge_invariance_residual(
            bundle,
            {
                "observe": self.channel_swap,
                "verify": self.channel_sign,
                "memory": self.channel_swap.compose(self.channel_sign),
            },
        )
        self.assertLessEqual(residual, 1e-12)

    def test_memory_holonomy_detects_nontrivial_closed_transport(self) -> None:
        flat = memory_holonomy(self.bundle(twisted=False))
        twisted = memory_holonomy(self.bundle(twisted=True))
        self.assertAlmostEqual(flat.wilson_observable, 1.0)
        self.assertAlmostEqual(flat.holonomy_defect, 0.0)
        self.assertLess(twisted.wilson_observable, 1.0)
        self.assertGreater(twisted.holonomy_defect, 0.0)


if __name__ == "__main__":
    unittest.main()
