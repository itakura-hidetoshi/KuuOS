from __future__ import annotations

from runtime.kuuos_repository_checkpoint_candidate_revalidation_v1_11 import (
    build_repository_checkpoint_candidate_revalidation_policy,
    derive_repository_checkpoint_candidate_revalidation_receipt,
)
from tests.v109_checkpoint_candidate_fixture import CheckpointCandidateV109Fixture


class CandidateRevalidationV111Fixture(CheckpointCandidateV109Fixture):
    def setup_candidate_revalidation_fixture(self) -> None:
        self.setup_checkpoint_candidate_fixture()
        self.revalidated_at = self.candidate_at + 1
        self.revalidation_policy = (
            build_repository_checkpoint_candidate_revalidation_policy(
                "checkpoint-candidate-revalidation-policy-v111-fixture",
                allowed_repository_ids=(self.stability.repository_id,),
                allowed_checkpoint_references=(
                    self.stability.checkpoint_reference,
                ),
                max_candidate_age_seconds=30,
            )
        )

    def derive_receipt(
        self,
        candidate,
        decision,
        route,
        record,
        stability,
        context,
        observation,
        *,
        revalidated_at=None,
    ):
        return derive_repository_checkpoint_candidate_revalidation_receipt(
            "checkpoint-candidate-revalidation-receipt-v111-fixture",
            candidate,
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
            self.revalidation_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
            gate_evaluated_at_epoch_seconds=self.gate_at,
            revalidated_at_epoch_seconds=(
                self.revalidated_at
                if revalidated_at is None
                else revalidated_at
            ),
        )

    def receipt_case(
        self,
        stability,
        context,
        observation,
        *,
        candidate_at=None,
        revalidated_at=None,
    ):
        record, route, decision, candidate = self.candidate_case(
            stability,
            context,
            observation,
            candidate_at=candidate_at,
        )
        receipt = self.derive_receipt(
            candidate,
            decision,
            route,
            record,
            stability,
            context,
            observation,
            revalidated_at=revalidated_at,
        )
        return record, route, decision, candidate, receipt
