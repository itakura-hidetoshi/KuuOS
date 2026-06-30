from __future__ import annotations

from runtime.kuuos_repository_checkpoint_namespace_gate_v1_08 import (
    build_repository_checkpoint_namespace_gate_policy,
    evaluate_repository_checkpoint_namespace_gate,
)
from runtime.kuuos_repository_checkpoint_repair_routing_v1_07 import (
    build_repository_checkpoint_repair_routing_policy,
    route_repository_checkpoint_repair,
)
from tests.v106_review_fixture import ReviewV106Fixture


class NamespaceGateV108Fixture(ReviewV106Fixture):
    def setup_namespace_gate_fixture(self) -> None:
        self.setup_review_fixture()
        self.routed_at = self.evaluated_at + 1
        self.gate_at = self.routed_at + 1
        self.routing_policy = build_repository_checkpoint_repair_routing_policy(
            "checkpoint-routing-policy-v108-fixture",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_review_age_seconds=20,
        )
        self.gate_policy = build_repository_checkpoint_namespace_gate_policy(
            "checkpoint-namespace-gate-policy-v108-fixture",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_route_age_seconds=20,
        )

    def gate_case(self, stability, context, observation, *, gate_at=None):
        record = self.review(
            stability=stability,
            context=context,
            observation=observation,
        )
        route = route_repository_checkpoint_repair(
            "checkpoint-route-v108-fixture",
            record,
            stability,
            context,
            self.policy,
            observation,
            self.routing_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
        )
        decision = evaluate_repository_checkpoint_namespace_gate(
            "checkpoint-gate-v108-fixture",
            route,
            record,
            stability,
            context,
            self.policy,
            observation,
            self.routing_policy,
            self.gate_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
            evaluated_at_epoch_seconds=(self.gate_at if gate_at is None else gate_at),
        )
        return record, route, decision
