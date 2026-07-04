import unittest

from runtime.kuuos_lifecycle_governance_transition_completion_review_v0_23 import (
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
from runtime.kuuos_lifecycle_governance_transition_start_v0_22 import (
    verify_artifact as verify_start_artifact,
)
from tests.test_kuuos_lifecycle_transition_start_v0_22 import (
    _args as _start_args,
    _evidence as _start_evidence,
    _policy as _start_policy,
    _source as _start_source,
    _start,
)


def _source():
    start_source = _start_source()
    start_policy = _start_policy(start_source)
    start_evidence = _start_evidence(start_source)
    start = _start(start_source, start_evidence)
    start_record = verify_start_artifact(
        *_start_args(start_source, start_evidence, start, start_policy)
    )
    source_args = tuple(_start_args(start_source, start_evidence, start, start_policy)[3:])
    return start, start_evidence, start_policy, start_record, source_args


def _policy(source):
    return make_policy(
        "lifecycle-bounded-transition-completion-review-policy-v0-23",
        allowed_completion_reviewer_ids=("lifecycle-transition-completion-reviewer-001",),
        allowed_completion_reviewer_organization_ids=("lifecycle-transition-completion-review-organization",),
        max_review_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_completion_delay_seconds=120,
    )


def _evidence(source, **overrides):
    started_at = source[0].started_at_epoch_seconds
    values = dict(
        evidence_id="lifecycle-transition-completion-review-evidence-001",
        completion_review_id="lifecycle-transition-completion-review-001",
        completion_reviewer_id="lifecycle-transition-completion-reviewer-001",
        completion_reviewer_organization_id="lifecycle-transition-completion-review-organization",
        reviewer_mandate_receipt_digest="m" * 64,
        reviewer_mandate_verified=True,
        reviewer_authority_receipt_digest="a" * 64,
        reviewer_authority_verified=True,
        reviewer_identity_confirmation_digest="i" * 64,
        reviewer_identity_confirmed=True,
        start_record_freshness_receipt_digest="s" * 64,
        start_record_fresh=True,
        completion_evidence_receipt_digest="e" * 64,
        completion_evidence_valid=True,
        package_freshness_receipt_digest="p" * 64,
        package_fresh=True,
        current_state_freshness_receipt_digest="c" * 64,
        current_state_not_stale=True,
        target_state_validity_receipt_digest="t" * 64,
        target_state_still_valid=True,
        completion_review_approved=True,
        denial_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        repository_changed=False,
        review_requested_at_epoch_seconds=started_at + 1,
        captured_at_epoch_seconds=started_at + 2,
        reviewed_at_epoch_seconds=started_at + 3,
        transition_completion_deadline_at_epoch_seconds=started_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _review(source, evidence, **overrides):
    started_at = source[0].started_at_epoch_seconds
    values = dict(
        completion_review_id="lifecycle-transition-completion-review-001",
        completion_reviewer_id="lifecycle-transition-completion-reviewer-001",
        completion_reviewer_organization_id="lifecycle-transition-completion-review-organization",
        review_requested_at_epoch_seconds=started_at + 1,
        reviewed_at_epoch_seconds=started_at + 3,
        source_start=source[0],
        source_record=source[3],
        review_evidence=evidence,
        transition_completion_route_digest=evidence.transition_completion_route_digest,
        transition_completion_deadline_at_epoch_seconds=started_at + 63,
        completion_review_approved=evidence.completion_review_approved,
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


class LifecycleTransitionCompletionReviewV023Test(unittest.TestCase):
    def test_approved_routes_to_separate_completion_without_mutation(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        review = _review(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, review, policy))
        self.assertEqual(APPROVED, artifact.status)
        self.assertTrue(artifact.completion_review_approved)
        self.assertTrue(artifact.ready_for_separate_transition_completion)
        self.assertTrue(artifact.transition_completion_required_next)
        self.assertFalse(artifact.lifecycle_transition_completed)
        self.assertFalse(artifact.lifecycle_transition_performed)
        self.assertFalse(artifact.lifecycle_state_changed)
        self.assertFalse(artifact.repository_changed)

    def test_reviewer_authority_failure_denies_without_completion_route(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source, reviewer_authority_verified=False)
        review = _review(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, review, policy))
        self.assertEqual(DENIED, artifact.status)
        self.assertTrue(artifact.completion_review_denied)
        self.assertFalse(artifact.ready_for_separate_transition_completion)
        self.assertTrue(artifact.transition_completion_replan_required_next)

    def test_non_started_source_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        review = _review(source, evidence)
        bad_source = (
            source[0],
            source[1],
            source[2],
            _refresh_record(source[3], status="not-started"),
            source[4],
        )
        artifact = verify_artifact(*_args(bad_source, evidence, review, policy))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.completion_review_record_issued)

    def test_completion_route_swap_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        review = _refresh_review(
            _review(source, evidence),
            transition_completion_route_digest="bad-route",
        )
        artifact = verify_artifact(*_args(source, evidence, review, policy))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
