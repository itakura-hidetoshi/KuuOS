from __future__ import annotations

import unittest

from runtime.kuuos_repository_checkpoint_namespace_gate_types_v1_08 import (
    GATE_NOOP,
    REASON_CLEAN,
)
from runtime.kuuos_repository_checkpoint_namespace_gate_v1_08 import (
    build_repository_checkpoint_namespace_gate_policy,
    evaluate_repository_checkpoint_namespace_gate,
)
from runtime.kuuos_repository_checkpoint_repair_routing_v1_07 import (
    build_repository_checkpoint_repair_routing_policy,
    route_repository_checkpoint_repair,
)
from tests.v106_review_fixture import ReviewV106Fixture


class RepositoryCheckpointNamespaceGateV108Tests(
    ReviewV106Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_review_fixture()
        self.routed_at = self.evaluated_at + 1
        self.routing_policy = build_repository_checkpoint_repair_routing_policy(
            "checkpoint-routing-policy-v108",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_review_age_seconds=20,
        )
        self.gate_policy = build_repository_checkpoint_namespace_gate_policy(
            "checkpoint-namespace-gate-policy-v108",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_route_age_seconds=20,
        )

    def test_clean_route_is_noop(self) -> None:
        record = self.review()
        route = route_repository_checkpoint_repair(
            "checkpoint-route-v108-clean",
            record,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            self.routing_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
        )
        decision = evaluate_repository_checkpoint_namespace_gate(
            "checkpoint-gate-v108-clean",
            route,
            record,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            self.routing_policy,
            self.gate_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
            evaluated_at_epoch_seconds=self.routed_at + 1,
        )
        self.assertEqual(decision.status, GATE_NOOP)
        self.assertEqual(decision.reason, REASON_CLEAN)
        self.assertFalse(decision.compatible)


if __name__ == "__main__":
    unittest.main()
