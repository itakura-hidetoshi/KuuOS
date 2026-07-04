import unittest

from runtime.kuuos_lifecycle_governance_repository_mutation_authorization_v0_27 import (
    AUTHORIZED,
    DENIED,
    REJECTED,
    Rec,
    authorization_digest,
    evidence_digest,
    make_evidence,
    make_policy,
    make_submission,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_repository_mutation_review_v0_26 import (
    verify_artifact as verify_review_artifact,
)
from tests.test_kuuos_lifecycle_repository_mutation_review_v0_26 import (
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
        "lifecycle-bounded-repository-mutation-authorization-policy-v0-27",
        allowed_authorizer_ids=("repository-mutation-authorizer-001",),
        allowed_authorizer_organization_ids=("repository-mutation-authorization-organization",),
        max_authorization_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_execution_preparation_delay_seconds=120,
    )


def _evidence(source, **overrides):
    reviewed_at = source[0].reviewed_at_epoch_seconds
    values = dict(
        evidence_id="repository-mutation-authorization-evidence-001",
        authorization_id="repository-mutation-authorization-001",
        authorizer_id="repository-mutation-authorizer-001",
        authorizer_organization_id="repository-mutation-authorization-organization",
        authorizer_mandate_receipt_digest="m" * 64,
        authorizer_mandate_verified=True,
        authorizer_authority_receipt_digest="a" * 64,
        authorizer_authority_verified=True,
        authorizer_identity_confirmation_digest="i" * 64,
        authorizer_identity_confirmed=True,
        repository_review_record_freshness_receipt_digest="r" * 64,
        repository_review_record_fresh=True,
        authorization_receipt_digest="x" * 64,
        authorization_receipt_valid=True,
        repository_mutation_package_freshness_receipt_digest="p" * 64,
        repository_mutation_package_fresh=True,
        repository_mutation_package_bounded_receipt_digest="b" * 64,
        repository_mutation_package_bounded=True,
        adopted_state_freshness_receipt_digest="s" * 64,
        adopted_state_not_stale=True,
        authorization_confirmed=True,
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
        authorization_requested_at_epoch_seconds=reviewed_at + 1,
        captured_at_epoch_seconds=reviewed_at + 2,
        authorized_at_epoch_seconds=reviewed_at + 3,
        execution_preparation_deadline_at_epoch_seconds=reviewed_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _authorization(source, evidence, **overrides):
    reviewed_at = source[0].reviewed_at_epoch_seconds
    values = dict(
        authorization_id="repository-mutation-authorization-001",
        authorizer_id="repository-mutation-authorizer-001",
        authorizer_organization_id="repository-mutation-authorization-organization",
        authorization_requested_at_epoch_seconds=reviewed_at + 1,
        authorized_at_epoch_seconds=reviewed_at + 3,
        source_review=source[0],
        source_record=source[3],
        authorization_evidence=evidence,
        proposed_repository_mutation_package_digest=evidence.proposed_repository_mutation_package_digest,
        execution_preparation_route_digest=evidence.execution_preparation_route_digest,
        execution_preparation_deadline_at_epoch_seconds=reviewed_at + 63,
        authorization_confirmed=evidence.authorization_confirmed,
        denial_reason_digest=evidence.denial_reason_digest,
    )
    values.update(overrides)
    return make_submission(**values)


def _args(source, evidence, authorization, policy):
    return (
        authorization,
        evidence,
        policy,
        source[0],
        source[1],
        source[2],
        source[3],
        *source[4],
    )


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


def _refresh_authorization(authorization, **changes):
    payload = authorization.to_dict()
    payload.update(changes)
    payload["authorization_digest"] = ""
    value = Rec(**payload)
    value.authorization_digest = authorization_digest(value)
    return value


class LifecycleRepositoryMutationAuthorizationV027Test(unittest.TestCase):
    def test_authorized_routes_to_execution_preparation_without_repository_mutation(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        authorization = _authorization(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, authorization, policy))
        self.assertEqual(AUTHORIZED, artifact.status)
        self.assertTrue(artifact.repository_mutation_authorized)
        self.assertTrue(artifact.repository_mutation_execution_preparation_required_next)
        self.assertFalse(artifact.repository_mutation_execution_prepared)
        self.assertFalse(artifact.repository_mutation_performed)
        self.assertFalse(artifact.file_written)
        self.assertFalse(artifact.ref_updated)
        self.assertFalse(artifact.branch_moved)
        self.assertFalse(artifact.external_operation_performed)
        self.assertFalse(artifact.repository_changed)

    def test_authorizer_authority_failure_denies_without_execution_preparation_route(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source, authorizer_authority_verified=False)
        authorization = _authorization(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, authorization, policy))
        self.assertEqual(DENIED, artifact.status)
        self.assertTrue(artifact.repository_mutation_authorization_denied)
        self.assertFalse(artifact.repository_mutation_execution_preparation_required_next)
        self.assertTrue(artifact.repository_mutation_authorization_replan_required_next)

    def test_non_approved_source_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        authorization = _authorization(source, evidence)
        bad_source = (
            source[0],
            source[1],
            source[2],
            _refresh_record(source[3], status="not-approved"),
            source[4],
        )
        artifact = verify_artifact(*_args(bad_source, evidence, authorization, policy))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.repository_mutation_authorization_record_issued)

    def test_execution_preparation_route_swap_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        authorization = _refresh_authorization(
            _authorization(source, evidence),
            execution_preparation_route_digest="bad-route",
        )
        artifact = verify_artifact(*_args(source, evidence, authorization, policy))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
