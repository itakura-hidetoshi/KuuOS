import unittest

from runtime.kuuos_lifecycle_governance_state_adoption_v0_25 import (
    ADOPTED,
    DENIED,
    REJECTED,
    Rec,
    adoption_digest,
    evidence_digest,
    make_evidence,
    make_policy,
    make_submission,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_transition_completion_v0_24 import (
    verify_artifact as verify_completion_artifact,
)
from tests.test_kuuos_lifecycle_transition_completion_v0_24 import (
    _args as _completion_args,
    _completion,
    _evidence as _completion_evidence,
    _policy as _completion_policy,
    _source as _completion_source,
)


def _source():
    completion_source = _completion_source()
    completion_policy = _completion_policy(completion_source)
    completion_evidence = _completion_evidence(completion_source)
    completion = _completion(completion_source, completion_evidence)
    completion_record = verify_completion_artifact(
        *_completion_args(completion_source, completion_evidence, completion, completion_policy)
    )
    source_args = tuple(
        _completion_args(completion_source, completion_evidence, completion, completion_policy)[3:]
    )
    return completion, completion_evidence, completion_policy, completion_record, source_args


def _policy(source):
    return make_policy(
        "lifecycle-bounded-state-adoption-policy-v0-25",
        allowed_state_adopter_ids=("lifecycle-state-adopter-001",),
        allowed_state_adopter_organization_ids=("lifecycle-state-adoption-organization",),
        max_adoption_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_repository_review_delay_seconds=120,
    )


def _evidence(source, **overrides):
    completed_at = source[0].completed_at_epoch_seconds
    values = dict(
        evidence_id="lifecycle-state-adoption-evidence-001",
        state_adoption_id="lifecycle-state-adoption-001",
        state_adopter_id="lifecycle-state-adopter-001",
        state_adopter_organization_id="lifecycle-state-adoption-organization",
        state_adopter_mandate_receipt_digest="m" * 64,
        state_adopter_mandate_verified=True,
        state_adopter_authority_receipt_digest="a" * 64,
        state_adopter_authority_verified=True,
        state_adopter_identity_confirmation_digest="i" * 64,
        state_adopter_identity_confirmed=True,
        completion_record_freshness_receipt_digest="r" * 64,
        completion_record_fresh=True,
        state_adoption_receipt_digest="s" * 64,
        state_adoption_receipt_valid=True,
        package_freshness_receipt_digest="p" * 64,
        package_fresh=True,
        previous_state_freshness_receipt_digest="c" * 64,
        previous_state_not_stale=True,
        target_state_validity_receipt_digest="t" * 64,
        target_state_still_valid=True,
        state_adoption_confirmed=True,
        denial_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        repository_changed=False,
        adoption_requested_at_epoch_seconds=completed_at + 1,
        captured_at_epoch_seconds=completed_at + 2,
        adopted_at_epoch_seconds=completed_at + 3,
        repository_review_deadline_at_epoch_seconds=completed_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _adoption(source, evidence, **overrides):
    completed_at = source[0].completed_at_epoch_seconds
    values = dict(
        state_adoption_id="lifecycle-state-adoption-001",
        state_adopter_id="lifecycle-state-adopter-001",
        state_adopter_organization_id="lifecycle-state-adoption-organization",
        adoption_requested_at_epoch_seconds=completed_at + 1,
        adopted_at_epoch_seconds=completed_at + 3,
        source_completion=source[0],
        source_record=source[3],
        adoption_evidence=evidence,
        repository_review_route_digest=evidence.repository_review_route_digest,
        repository_review_deadline_at_epoch_seconds=completed_at + 63,
        state_adoption_confirmed=evidence.state_adoption_confirmed,
        denial_reason_digest=evidence.denial_reason_digest,
    )
    values.update(overrides)
    return make_submission(**values)


def _args(source, evidence, adoption, policy):
    return (adoption, evidence, policy, source[0], source[1], source[2], source[3], *source[4])


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


def _refresh_adoption(adoption, **changes):
    payload = adoption.to_dict()
    payload.update(changes)
    payload["adoption_digest"] = ""
    value = Rec(**payload)
    value.adoption_digest = adoption_digest(value)
    return value


class LifecycleStateAdoptionV025Test(unittest.TestCase):
    def test_adopted_routes_to_repository_review_without_repository_mutation(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        adoption = _adoption(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, adoption, policy))
        self.assertEqual(ADOPTED, artifact.status)
        self.assertTrue(artifact.lifecycle_state_adopted)
        self.assertTrue(artifact.lifecycle_transition_performed)
        self.assertTrue(artifact.lifecycle_state_changed)
        self.assertTrue(artifact.repository_mutation_review_required_next)
        self.assertFalse(artifact.external_operation_performed)
        self.assertFalse(artifact.repository_changed)

    def test_adopter_authority_failure_denies_without_repository_review_route(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source, state_adopter_authority_verified=False)
        adoption = _adoption(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, adoption, policy))
        self.assertEqual(DENIED, artifact.status)
        self.assertTrue(artifact.state_adoption_denied)
        self.assertFalse(artifact.lifecycle_state_adopted)
        self.assertFalse(artifact.repository_mutation_review_required_next)
        self.assertTrue(artifact.state_adoption_replan_required_next)

    def test_non_completed_source_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        adoption = _adoption(source, evidence)
        bad_source = (
            source[0],
            source[1],
            source[2],
            _refresh_record(source[3], status="not-completed"),
            source[4],
        )
        artifact = verify_artifact(*_args(bad_source, evidence, adoption, policy))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.state_adoption_record_issued)

    def test_repository_review_route_swap_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        adoption = _refresh_adoption(
            _adoption(source, evidence),
            repository_review_route_digest="bad-route",
        )
        artifact = verify_artifact(*_args(source, evidence, adoption, policy))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
