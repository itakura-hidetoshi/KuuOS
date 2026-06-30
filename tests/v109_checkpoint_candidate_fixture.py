from __future__ import annotations

from runtime.kuuos_repository_checkpoint_candidate_v1_09 import (
    build_repository_checkpoint_candidate_policy,
    derive_repository_checkpoint_candidate,
)
from tests.v108_namespace_gate_fixture import NamespaceGateV108Fixture


class CheckpointCandidateV109Fixture(NamespaceGateV108Fixture):
    def setup_checkpoint_candidate_fixture(self) -> None:
        self.setup_namespace_gate_fixture()
        self.candidate_at = self.gate_at + 1
        self.candidate_policy = build_repository_checkpoint_candidate_policy(
            "checkpoint-candidate-policy-v109-fixture",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            max_gate_age_seconds=20,
        )

    def candidate_case(
        self,
        stability,
        context,
        observation,
        *,
        candidate_at=None,
    ):
        record, route, decision = self.gate_case(
            stability,
            context,
            observation,
        )
        candidate = derive_repository_checkpoint_candidate(
            "checkpoint-candidate-v109-fixture",
            decision,
            route,
            record,
            stability,
            context,
            self.policy,
            observation,
            self.routing_policy,
            self.gate_policy,
            self.candidate_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
            gate_evaluated_at_epoch_seconds=self.gate_at,
            evaluated_at_epoch_seconds=(
                self.candidate_at if candidate_at is None else candidate_at
            ),
        )
        return record, route, decision, candidate
