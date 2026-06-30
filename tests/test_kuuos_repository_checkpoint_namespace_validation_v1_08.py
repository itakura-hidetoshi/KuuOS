from __future__ import annotations

import unittest

from runtime.kuuos_repository_checkpoint_namespace_gate_types_v1_08 import (
    GATE_REJECTED,
    REASON_INVALID_ROUTE,
)
from tests.v108_namespace_gate_fixture import NamespaceGateV108Fixture


class RepositoryCheckpointNamespaceValidationV108Tests(
    NamespaceGateV108Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_namespace_gate_fixture()

    def test_stale_route_is_rejected(self) -> None:
        _, _, decision = self.gate_case(
            self.stability,
            self.v105_context,
            self.observation,
            gate_at=self.routed_at + 21,
        )
        self.assertEqual(decision.status, GATE_REJECTED)
        self.assertEqual(decision.reason, REASON_INVALID_ROUTE)
        self.assertFalse(decision.checks["route_fresh"])

    def test_all_cases_remain_checkpoint_namespaced(self) -> None:
        cases = [
            (self.stability, self.v105_context, self.observation),
            self.lost_case(),
            self.substituted_case(),
        ]
        for stability, context, observation in cases:
            _, _, decision = self.gate_case(stability, context, observation)
            self.assertTrue(decision.checks["checkpoint_namespace"])


if __name__ == "__main__":
    unittest.main()
