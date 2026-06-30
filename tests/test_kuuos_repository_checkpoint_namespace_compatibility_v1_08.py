from __future__ import annotations

import unittest

from runtime.kuuos_repository_checkpoint_namespace_gate_types_v1_08 import (
    GATE_ACCEPTED,
    GATE_REJECTED,
    REASON_CREATION_ROUTE,
    REASON_NAMESPACE_MISMATCH,
)
from runtime.kuuos_repository_checkpoint_repair_routing_types_v1_07 import (
    PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97,
)
from tests.v108_namespace_gate_fixture import NamespaceGateV108Fixture


class RepositoryCheckpointNamespaceCompatibilityV108Tests(
    NamespaceGateV108Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_namespace_gate_fixture()

    def test_creation_route_is_compatible(self) -> None:
        stability, context, observation = self.lost_case()
        _, _, decision = self.gate_case(stability, context, observation)
        self.assertEqual(decision.status, GATE_ACCEPTED)
        self.assertEqual(decision.reason, REASON_CREATION_ROUTE)
        self.assertTrue(decision.compatible)

    def test_branch_route_is_not_checkpoint_compatible(self) -> None:
        stability, context, observation = self.substituted_case()
        _, route, decision = self.gate_case(stability, context, observation)
        self.assertEqual(route.primitive, PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97)
        self.assertEqual(decision.status, GATE_REJECTED)
        self.assertEqual(decision.reason, REASON_NAMESPACE_MISMATCH)
        self.assertFalse(decision.compatible)
        self.assertTrue(decision.checks["namespace_mismatch"])


if __name__ == "__main__":
    unittest.main()
