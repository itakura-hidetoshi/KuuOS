from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    repository_checkpoint_review_record_digest,
)
from runtime.kuuos_repository_checkpoint_repair_routing_types_v1_07 import (
    PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02,
    PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97,
    PRIMITIVE_NONE,
    ROUTE_AUTOMATIC,
    ROUTE_NOOP,
    ROUTE_REJECTED,
    repository_checkpoint_repair_route_digest,
)
from runtime.kuuos_repository_checkpoint_repair_routing_v1_07 import (
    build_repository_checkpoint_repair_routing_policy,
    repository_checkpoint_repair_route_issues,
    route_repository_checkpoint_repair,
)
from tests.v106_review_fixture import ReviewV106Fixture


class RepositoryCheckpointRepairRoutingV107Tests(
    ReviewV106Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_review_fixture()
        self.routed_at = self.evaluated_at + 1
        self.routing_policy = build_repository_checkpoint_repair_routing_policy(
            "checkpoint-repair-routing-policy-v107",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_review_age_seconds=20,
        )

    def route(self, *, stability=None, context=None, observation=None, routed_at=None):
        selected_stability = stability or self.stability
        selected_context = context or self.v105_context
        selected_observation = observation or self.observation
        record = self.review(
            stability=selected_stability,
            context=selected_context,
            observation=selected_observation,
        )
        route = route_repository_checkpoint_repair(
            "checkpoint-repair-route-v107-001",
            record,
            selected_stability,
            selected_context,
            self.policy,
            selected_observation,
            self.routing_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=(
                self.routed_at if routed_at is None else routed_at
            ),
        )
        return record, route

    def test_clean_checkpoint_routes_to_noop(self) -> None:
        first_record, first = self.route()
        second_record, second = self.route()
        self.assertEqual(first_record, second_record)
        self.assertEqual(first, second)
        self.assertEqual(first.status, ROUTE_NOOP)
        self.assertEqual(first.primitive, PRIMITIVE_NONE)
        self.assertFalse(first.automatic_route_eligible)
        self.assertFalse(first.human_review_required)

    def test_lost_checkpoint_routes_to_atomic_creation_v102(self) -> None:
        stability, context, observation = self.lost_case()
        _, route = self.route(
            stability=stability,
            context=context,
            observation=observation,
        )
        self.assertEqual(route.status, ROUTE_AUTOMATIC)
        self.assertEqual(
            route.primitive,
            PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02,
        )
        self.assertTrue(route.automatic_route_eligible)
        self.assertTrue(route.checks["lost_shape"])
        self.assertFalse(route.human_review_required)

    def test_substituted_checkpoint_routes_to_atomic_update_v097(self) -> None:
        stability, context, observation = self.substituted_case()
        _, route = self.route(
            stability=stability,
            context=context,
            observation=observation,
        )
        self.assertEqual(route.status, ROUTE_AUTOMATIC)
        self.assertEqual(
            route.primitive,
            PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97,
        )
        self.assertTrue(route.automatic_route_eligible)
        self.assertTrue(route.checks["substituted_shape"])
        self.assertFalse(route.human_review_required)

    def test_stale_review_is_rejected(self) -> None:
        _, route = self.route(routed_at=self.evaluated_at + 21)
        self.assertEqual(route.status, ROUTE_REJECTED)
        self.assertEqual(route.primitive, PRIMITIVE_NONE)
        self.assertFalse(route.checks["review_fresh"])
        self.assertFalse(route.automatic_route_eligible)

    def test_policy_binding_mismatch_is_rejected(self) -> None:
        record = self.review()
        policy = build_repository_checkpoint_repair_routing_policy(
            "other-routing-policy-v107",
            allowed_repository_ids=("other-repository",),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_review_age_seconds=20,
        )
        route = route_repository_checkpoint_repair(
            "checkpoint-repair-route-v107-binding",
            record,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
        )
        self.assertEqual(route.status, ROUTE_REJECTED)
        self.assertFalse(route.checks["binding_exact"])

    def test_tampered_review_record_is_rejected(self) -> None:
        record = self.review()
        tampered = replace(
            record,
            human_review_required=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=repository_checkpoint_review_record_digest(tampered),
        )
        route = route_repository_checkpoint_repair(
            "checkpoint-repair-route-v107-tampered",
            tampered,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            self.routing_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
        )
        self.assertEqual(route.status, ROUTE_REJECTED)
        self.assertFalse(route.checks["upstream_review_valid"])

    def test_all_routes_are_read_only_and_require_no_human_review(self) -> None:
        routes = [self.route()[1]]
        for stability, context, observation in (
            self.lost_case(),
            self.substituted_case(),
        ):
            routes.append(
                self.route(
                    stability=stability,
                    context=context,
                    observation=observation,
                )[1]
            )
        for route in routes:
            self.assertFalse(route.human_review_required)
            self.assertFalse(route.repository_change_authority_granted)
            self.assertFalse(route.live_git_execution_performed)
            self.assertFalse(route.checks["side_effect_performed"])

    def test_route_tamper_is_detected(self) -> None:
        record, route = self.route()
        tampered = replace(
            route,
            primitive=PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97,
            route_digest="",
        )
        tampered = replace(
            tampered,
            route_digest=repository_checkpoint_repair_route_digest(tampered),
        )
        issues = repository_checkpoint_repair_route_issues(
            tampered,
            record,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            self.routing_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
        )
        self.assertIn("repair_route_recomputation_mismatch", issues)


if __name__ == "__main__":
    unittest.main()
