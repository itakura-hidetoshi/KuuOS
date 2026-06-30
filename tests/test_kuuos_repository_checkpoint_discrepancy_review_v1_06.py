from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    DISCREPANCY_EVIDENCE_INVALID,
    DISCREPANCY_LOST,
    DISCREPANCY_NONE,
    DISCREPANCY_SUBSTITUTED,
    REVIEW_AUTOMATIC_REPAIR_ELIGIBLE,
    REVIEW_CLEAN,
    REVIEW_REJECTED,
    repository_checkpoint_review_record_digest,
)
from runtime.v106_review_strict import repository_checkpoint_review_record_issues
from tests.v106_review_fixture import ReviewV106Fixture


class RepositoryCheckpointDiscrepancyReviewV106Tests(
    ReviewV106Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_review_fixture()

    def test_clean_checkpoint_requires_no_human_review(self) -> None:
        first = self.review()
        second = self.review()
        self.assertEqual(first, second)
        self.assertEqual(first.status, REVIEW_CLEAN)
        self.assertEqual(first.discrepancy_kind, DISCREPANCY_NONE)
        self.assertFalse(first.automatic_repair_eligible)
        self.assertFalse(first.human_review_required)

    def test_confirmed_loss_is_automatic_repair_eligible(self) -> None:
        stability, context, observation = self.lost_case()
        record = self.review(
            stability=stability,
            context=context,
            observation=observation,
        )
        self.assertEqual(record.status, REVIEW_AUTOMATIC_REPAIR_ELIGIBLE)
        self.assertEqual(record.discrepancy_kind, DISCREPANCY_LOST)
        self.assertTrue(record.automatic_repair_eligible)
        self.assertTrue(record.checks["exact_zero_to_known_oid_repair"])
        self.assertFalse(record.human_review_required)

    def test_confirmed_substitution_is_automatic_repair_eligible(self) -> None:
        stability, context, observation = self.substituted_case()
        record = self.review(
            stability=stability,
            context=context,
            observation=observation,
        )
        self.assertEqual(record.status, REVIEW_AUTOMATIC_REPAIR_ELIGIBLE)
        self.assertEqual(record.discrepancy_kind, DISCREPANCY_SUBSTITUTED)
        self.assertTrue(record.automatic_repair_eligible)
        self.assertTrue(record.checks["exact_existing_to_known_oid_repair"])
        self.assertFalse(record.human_review_required)

    def test_stale_disposition_is_rejected_without_human_review(self) -> None:
        stability, context, _ = self.lost_case()
        observation = self.make_observation(
            stability,
            reference_present=True,
            observed_oid=stability.expected_oid,
            rechecked_oid=stability.expected_oid,
        )
        record = self.review(
            stability=stability,
            context=context,
            observation=observation,
        )
        self.assertEqual(record.status, REVIEW_REJECTED)
        self.assertEqual(record.discrepancy_kind, DISCREPANCY_EVIDENCE_INVALID)
        self.assertFalse(record.automatic_repair_eligible)
        self.assertFalse(record.human_review_required)

    def test_observer_and_binding_are_exact(self) -> None:
        observation = self.resign_observation(
            self.observation,
            observer_id="unknown-review-observer",
        )
        record = self.review(observation=observation)
        self.assertEqual(record.status, REVIEW_REJECTED)
        self.assertFalse(record.checks["observer_accepted"])

        observation = self.resign_observation(
            self.observation,
            checkpoint_reference="refs/kuuos/checkpoints/other",
        )
        record = self.review(observation=observation)
        self.assertFalse(record.checks["evidence_binding_exact"])

    def test_review_sources_are_direct_local_and_read_only(self) -> None:
        for changes in (
            {"direct": False},
            {"symbolic": True},
            {"reference_store_read": False},
            {"object_database_read": False},
            {"working_tree_read": True},
            {"reflog_read": True},
            {"remote_read": True},
        ):
            observation = self.resign_observation(
                self.observation,
                **changes,
            )
            record = self.review(observation=observation)
            self.assertEqual(record.status, REVIEW_REJECTED)
            self.assertFalse(record.checks["direct_local_sources_only"])

    def test_recheck_must_be_stable(self) -> None:
        observation = self.resign_observation(
            self.observation,
            rechecked_oid="b" * 40,
        )
        record = self.review(observation=observation)
        self.assertEqual(record.status, REVIEW_REJECTED)
        self.assertFalse(record.checks["current_state_recheck_stable"])

    def test_observation_must_be_fresh_and_not_future_dated(self) -> None:
        stale = self.resign_observation(
            self.observation,
            observed_at_epoch_seconds=10_200,
            rechecked_at_epoch_seconds=10_201,
        )
        record = self.review(observation=stale)
        self.assertFalse(record.checks["observation_fresh"])

        future = self.resign_observation(
            self.observation,
            observed_at_epoch_seconds=self.evaluated_at + 1,
            rechecked_at_epoch_seconds=self.evaluated_at + 2,
        )
        record = self.review(observation=future)
        self.assertFalse(record.checks["no_future_evidence"])

    def test_target_commit_must_remain_present(self) -> None:
        for changes in (
            {"target_object_present": False},
            {"target_object_type": "blob"},
        ):
            observation = self.resign_observation(
                self.observation,
                **changes,
            )
            record = self.review(observation=observation)
            self.assertEqual(record.status, REVIEW_REJECTED)
            self.assertFalse(record.checks["target_commit_present"])
            self.assertFalse(record.automatic_repair_eligible)

    def test_no_case_requests_human_review(self) -> None:
        records = [self.review()]
        for stability, context, observation in (
            self.lost_case(),
            self.substituted_case(),
        ):
            records.append(
                self.review(
                    stability=stability,
                    context=context,
                    observation=observation,
                )
            )
        self.assertTrue(all(not record.human_review_required for record in records))
        self.assertTrue(
            all(not record.checks["human_review_required"] for record in records)
        )

    def test_review_has_no_repository_side_effect_claims(self) -> None:
        for stability, context, observation in (
            self.lost_case(),
            self.substituted_case(),
        ):
            record = self.review(
                stability=stability,
                context=context,
                observation=observation,
            )
            for key in (
                "review_granted_repository_change_authority",
                "review_performed_reference_mutation",
                "review_performed_object_write",
                "review_invoked_live_git_command",
                "review_mutated_live_repository",
                "review_consumed_nonce",
            ):
                self.assertFalse(record.checks[key])

    def test_record_tamper_is_detected(self) -> None:
        record = self.review()
        checks = dict(record.checks)
        checks["review_granted_repository_change_authority"] = True
        tampered = replace(record, checks=checks, record_digest="")
        tampered = replace(
            tampered,
            record_digest=repository_checkpoint_review_record_digest(tampered),
        )
        issues = repository_checkpoint_review_record_issues(
            tampered,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            evaluated_at_epoch_seconds=self.evaluated_at,
        )
        self.assertIn("checkpoint_review_recomputation_mismatch", issues)
        self.assertIn("checkpoint_review_forbidden_claim", issues)


if __name__ == "__main__":
    unittest.main()
