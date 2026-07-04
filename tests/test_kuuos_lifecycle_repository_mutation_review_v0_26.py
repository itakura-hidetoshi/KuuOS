import unittest

from runtime.kuuos_lifecycle_governance_repository_mutation_review_v0_26 import (
    APPROVED,
    DENIED,
    REJECTED,
    Rec,
    evidence_digest,
    make_evidence,
    make_policy,
    make_submission,
    record_digest,
    review_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_state_adoption_v0_25 import (
    verify_artifact as verify_adoption_artifact,
)
from tests.test_kuuos_lifecycle_state_adoption_v0_25 import (
    _adoption,
    _args as _adoption_args,
    _evidence as _adoption_evidence,
    _policy as _adoption_policy,
    _source as _adoption_source,
)


def _source():
    adoption_source = _adoption_source()
    adoption_policy = _adoption_policy(adoption_source)
    adoption_evidence = _adoption_evidence(adoption_source)
    adoption = _adoption(adoption_source, adoption_evidence)
    adoption_record = verify_adoption_artifact(
        *_adoption_args(adoption_source, adoption_evidence, adoption, adoption_policy)
    )
    source_args = tuple(
        _adoption_args(adoption_source, adoption_evidence, adoption, adoption_policy)[3:]
    )
    return adoption, adoption_evidence, adoption_policy, adoption_record, source_args


def _policy(source):
    return make_policy(
        "lifecycle-bounded-repository-mutation-review-policy-v0-26",
        allowed_mutation_reviewer_ids=("repository-mutation-reviewer-001",),
        allowed_mutation_reviewer_organization_ids=("repository-mutation-review-organization",),
        max_review_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_mutation_authorization_delay_seconds=120,
    )


def _evidence(source, **overrides):
    adopted_at = source[0].adopted_at_epoch_seconds
    values = dict(
        evidence_id="repository-mutation-review-evidence-001",
        repository_review_id="repository-mutation-review-001",
        mutation_reviewer_id="repository-mutation-reviewer-001",
        mutation_reviewer_organization_id="repository-mutation-review-organization",
        mutation_reviewer_mandate_receipt_digest="m" * 64,
        mutation_reviewer_mandate_verified=True,
        mutation_reviewer_authority_receipt_digest="a" * 64,
        mutation_reviewer_authority_verified=True,
        mutation_reviewer_identity_confirmation_digest="i" * 64,
        mutation_reviewer_identity_confirmed=True,
        state_adoption_record_freshness_receipt_digest="r" * 64,
        state_adoption_record_fresh=True,
        adopted_state_freshness_receipt_digest="s" * 64,
        adopted_state_not_stale=True,
        repository_mutation_package_review_receipt_digest="v" * 64,
        repository_mutation_package_review_valid=True,
        repository_mutation_package_freshness_receipt_digest="p" * 64,
        repository_mutation_package_fresh=True,
        repository_mutation_package_bounded_receipt_digest="b" * 64,
        repository_mutation_package_bounded=True,
        proposed_repository_mutation_package_digest="u" * 64,
        review_confirmed=True,
        denial_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        repository_changed=False,
        file_written=False,
        ref_updated=False,
        branch_moved=False,
        terminal_marker_written=False,
        resource_removed=False,
        review_requested_at_epoch_seconds=adopted_at + 1,
        captured_at_epoch_seconds=adopted_at + 2,
        reviewed_at_epoch_seconds=adopted_at + 3,
        mutation_authorization_deadline_at_epoch_seconds=adopted_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _review(source, evidence, **overrides):
    adopted_at = source[0].adopted_at_epoch_seconds
    values = dict(
        repository_review_id="repository-mutation-review-001",
        mutation_reviewer_id="repository-mutation-reviewer-001",
        mutation_reviewer_organization_id="repository-mutation-review-organization",
        review_requested_at_epoch_seconds=adopted_at + 1,
        reviewed_at_epoch_seconds=adopted_at + 3,
        source_adoption=source[0],
        source_record=source[3],
        review_evidence=evidence,
        proposed_repository_mutation_package_digest=evidence.proposed_repository_mutation_package_digest,
        mutation_authorization_route_digest=evidence.mutation_authorization_route_digest,
        mutation_authorization_deadline_at_epoch_seconds=adopted_at + 63,
        review_confirmed=evidence.review_confirmed,
        denial_reason_digest=evidence.denial_reason_digest,
    )
    values.update(overrides)
    return make_submission(**values)


def _args(source, evidence, review, policy):
    return (review, evidence, policy, source[0], source[1], source[2], source[3], *source[4])


def _refresh_record(record, **changes):
    payload = record.to_dict()
    payload.update(changes)
    payload["record_digest"] = ""
    value = Rec(**payload)
    value.record_digest = record_digest(value)
    return value


def _refresh_evidence(evidence, **changes):
    payload = evidence.to_dict()
    payload.update(changes)
    payload["evidence_digest"] = ""
    value = Rec(**payload)
    value.evidence_digest = evidence_digest(value)
    return value


def _refresh_review(review, **changes):
    payload = review.to_dict()
    payload.update(changes)
    payload["review_digest"] = ""
    value = Rec(**payload)
    value.review_digest = review_digest(value)
    return value


class LifecycleRepositoryMutationReviewV026Test(unittest.TestCase):
    def test_approved_routes_to_authorization_without_repository_mutation(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        review = _review(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, review, policy))
        self.assertEqual(APPROVED, artifact.status)
        self.assertTrue(artifact.repository_mutation_review_approved)
        self.assertTrue(artifact.repository_mutation_authorization_required_next)
        self.assertFalse(artifact.repository_mutation_performed)
        self.assertFalse(artifact.file_written)
        self.assertFalse(artifact.ref_updated)
        self.assertFalse(artifact.branch_moved)
        self.assertFalse(artifact.external_operation_performed)
        self.assertFalse(artifact.repository_changed)

    def test_reviewer_authority_failure_denies_without_authorization_route(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source, mutation_reviewer_authority_verified=False)
        review = _review(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, review, policy))
        self.assertEqual(DENIED, artifact.status)
        self.assertTrue(artifact.repository_mutation_review_denied)
        self.assertFalse(artifact.repository_mutation_authorization_required_next)
        self.assertTrue(artifact.repository_mutation_review_replan_required_next)

    def test_non_adopted_source_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        review = _review(source, evidence)
        bad_source = (
            source[0],
            source[1],
            source[2],
            _refresh_record(source[3], status="not-adopted"),
            source[4],
        )
        artifact = verify_artifact(*_args(bad_source, evidence, review, policy))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.repository_mutation_review_record_issued)

    def test_mutation_authorization_route_swap_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        review = _refresh_review(
            _review(source, evidence),
            mutation_authorization_route_digest="bad-route",
        )
        artifact = verify_artifact(*_args(source, evidence, review, policy))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
