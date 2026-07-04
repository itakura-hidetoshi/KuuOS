import unittest

from runtime.kuuos_lifecycle_governance_transition_completion_v0_24 import (
    COMPLETED,
    DENIED,
    REJECTED,
    Rec,
    completion_digest,
    evidence_digest,
    make_evidence,
    make_policy,
    make_submission,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_transition_completion_review_v0_23 import (
    verify_artifact as verify_review_artifact,
)
from tests.test_kuuos_lifecycle_transition_completion_review_v0_23 import (
    _args as _review_args,
    _evidence as _review_evidence,
    _policy as _review_policy,
    _review,
    _source as _review_source,
)


def _source():
    review_source = _review_source()
    review_policy = _review_policy(review_source)
    review_evidence = _review_evidence(review_source)
    review = _review(review_source, review_evidence)
    review_record = verify_review_artifact(
        *_review_args(review_source, review_evidence, review, review_policy)
    )
    source_args = tuple(_review_args(review_source, review_evidence, review, review_policy)[3:])
    return review, review_evidence, review_policy, review_record, source_args


def _policy(source):
    return make_policy(
        "lifecycle-bounded-transition-completion-policy-v0-24",
        allowed_completion_operator_ids=(source[0].source_transition_operator_id,),
        allowed_completion_operator_organization_ids=("lifecycle-transition-completion-operator-organization",),
        max_completion_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_state_adoption_delay_seconds=120,
    )


def _evidence(source, **overrides):
    reviewed_at = source[0].reviewed_at_epoch_seconds
    values = dict(
        evidence_id="lifecycle-transition-completion-evidence-001",
        transition_completion_id="lifecycle-transition-completion-001",
        completion_operator_id=source[0].source_transition_operator_id,
        completion_operator_organization_id="lifecycle-transition-completion-operator-organization",
        completion_operator_mandate_receipt_digest="m" * 64,
        completion_operator_mandate_verified=True,
        completion_operator_authority_receipt_digest="a" * 64,
        completion_operator_authority_verified=True,
        completion_operator_identity_confirmation_digest="i" * 64,
        completion_operator_identity_confirmed=True,
        completion_review_freshness_receipt_digest="r" * 64,
        completion_review_fresh=True,
        completion_receipt_digest="x" * 64,
        completion_receipt_valid=True,
        package_freshness_receipt_digest="p" * 64,
        package_fresh=True,
        current_state_freshness_receipt_digest="c" * 64,
        current_state_not_stale=True,
        target_state_validity_receipt_digest="t" * 64,
        target_state_still_valid=True,
        transition_completion_confirmed=True,
        denial_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        repository_changed=False,
        completion_requested_at_epoch_seconds=reviewed_at + 1,
        captured_at_epoch_seconds=reviewed_at + 2,
        completed_at_epoch_seconds=reviewed_at + 3,
        lifecycle_state_adoption_deadline_at_epoch_seconds=reviewed_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _completion(source, evidence, **overrides):
    reviewed_at = source[0].reviewed_at_epoch_seconds
    values = dict(
        transition_completion_id="lifecycle-transition-completion-001",
        completion_operator_id=source[0].source_transition_operator_id,
        completion_operator_organization_id="lifecycle-transition-completion-operator-organization",
        completion_requested_at_epoch_seconds=reviewed_at + 1,
        completed_at_epoch_seconds=reviewed_at + 3,
        source_review=source[0],
        source_record=source[3],
        completion_evidence=evidence,
        lifecycle_state_adoption_route_digest=evidence.lifecycle_state_adoption_route_digest,
        lifecycle_state_adoption_deadline_at_epoch_seconds=reviewed_at + 63,
        transition_completion_confirmed=evidence.transition_completion_confirmed,
        denial_reason_digest=evidence.denial_reason_digest,
    )
    values.update(overrides)
    return make_submission(**values)


def _args(source, evidence, completion, policy):
    return (completion, evidence, policy, source[0], source[1], source[2], source[3], *source[4])


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


def _refresh_completion(completion, **changes):
    payload = completion.to_dict()
    payload.update(changes)
    payload["completion_digest"] = ""
    value = Rec(**payload)
    value.completion_digest = completion_digest(value)
    return value


class LifecycleTransitionCompletionV024Test(unittest.TestCase):
    def test_completed_routes_to_state_adoption_without_state_mutation(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        completion = _completion(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, completion, policy))
        self.assertEqual(COMPLETED, artifact.status)
        self.assertTrue(artifact.lifecycle_transition_completed)
        self.assertTrue(artifact.ready_for_separate_lifecycle_state_adoption)
        self.assertTrue(artifact.lifecycle_state_adoption_required_next)
        self.assertFalse(artifact.lifecycle_transition_performed)
        self.assertFalse(artifact.lifecycle_state_changed)
        self.assertFalse(artifact.repository_changed)

    def test_completion_operator_authority_failure_denies_without_state_adoption_route(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source, completion_operator_authority_verified=False)
        completion = _completion(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, completion, policy))
        self.assertEqual(DENIED, artifact.status)
        self.assertTrue(artifact.transition_completion_denied)
        self.assertFalse(artifact.lifecycle_transition_completed)
        self.assertTrue(artifact.transition_recompletion_or_replan_required_next)

    def test_non_approved_source_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        completion = _completion(source, evidence)
        bad_source = (
            source[0],
            source[1],
            source[2],
            _refresh_record(source[3], status="not-approved"),
            source[4],
        )
        artifact = verify_artifact(*_args(bad_source, evidence, completion, policy))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.transition_completion_record_issued)

    def test_state_adoption_route_swap_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        completion = _refresh_completion(
            _completion(source, evidence),
            lifecycle_state_adoption_route_digest="bad-route",
        )
        artifact = verify_artifact(*_args(source, evidence, completion, policy))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
