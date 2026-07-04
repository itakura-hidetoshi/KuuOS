import unittest

from runtime.kuuos_lifecycle_governance_transition_start_v0_22 import (
    DENIED,
    REJECTED,
    STARTED,
    Rec,
    evidence_digest,
    make_evidence,
    make_policy,
    make_submission,
    record_digest,
    start_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_transition_start_authorization_v0_21 import (
    verify_artifact as verify_authorization_artifact,
)
from tests.test_kuuos_lifecycle_transition_start_authorization_v0_21 import (
    _args as _authorization_args,
    _authorization,
    _evidence as _authorization_evidence,
    _policy as _authorization_policy,
    _source as _authorization_source,
)


def _source():
    _, authorization_source = _authorization_source()
    authorization_policy = _authorization_policy(authorization_source)
    authorization_evidence = _authorization_evidence(authorization_source)
    authorization = _authorization(authorization_source, authorization_evidence)
    authorization_record = verify_authorization_artifact(
        *_authorization_args(
            authorization_source,
            authorization_evidence,
            authorization,
            authorization_policy,
        )
    )
    source_args = tuple(
        _authorization_args(
            authorization_source,
            authorization_evidence,
            authorization,
            authorization_policy,
        )[3:]
    )
    return authorization, authorization_evidence, authorization_policy, authorization_record, source_args


def _policy(source):
    return make_policy(
        "lifecycle-bounded-transition-start-policy-v0-22",
        allowed_transition_operator_ids=(source[0].future_transition_operator_id,),
        allowed_transition_operator_organization_ids=("lifecycle-transition-operator-organization",),
        max_start_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_completion_review_delay_seconds=120,
    )


def _evidence(source, **overrides):
    authorized_at = source[0].authorized_at_epoch_seconds
    values = dict(
        evidence_id="lifecycle-transition-start-evidence-001",
        transition_start_id="lifecycle-transition-start-001",
        transition_operator_id=source[0].future_transition_operator_id,
        transition_operator_organization_id="lifecycle-transition-operator-organization",
        operator_mandate_receipt_digest="m" * 64,
        operator_mandate_verified=True,
        operator_authority_receipt_digest="a" * 64,
        operator_authority_verified=True,
        operator_identity_confirmation_digest="i" * 64,
        operator_identity_confirmed=True,
        start_authorization_freshness_receipt_digest="s" * 64,
        start_authorization_fresh=True,
        package_freshness_receipt_digest="p" * 64,
        package_fresh=True,
        current_state_freshness_receipt_digest="c" * 64,
        current_state_not_stale=True,
        target_state_validity_receipt_digest="t" * 64,
        target_state_still_valid=True,
        transition_start_confirmed=True,
        denial_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        repository_changed=False,
        start_requested_at_epoch_seconds=authorized_at + 1,
        captured_at_epoch_seconds=authorized_at + 2,
        started_at_epoch_seconds=authorized_at + 3,
        transition_completion_review_deadline_at_epoch_seconds=authorized_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _start(source, evidence, **overrides):
    authorized_at = source[0].authorized_at_epoch_seconds
    values = dict(
        transition_start_id="lifecycle-transition-start-001",
        transition_operator_id=source[0].future_transition_operator_id,
        transition_operator_organization_id="lifecycle-transition-operator-organization",
        start_requested_at_epoch_seconds=authorized_at + 1,
        started_at_epoch_seconds=authorized_at + 3,
        source_authorization=source[0],
        source_record=source[3],
        start_evidence=evidence,
        transition_completion_review_route_digest=evidence.transition_completion_review_route_digest,
        transition_completion_review_deadline_at_epoch_seconds=authorized_at + 63,
        transition_start_confirmed=evidence.transition_start_confirmed,
        denial_reason_digest=evidence.denial_reason_digest,
    )
    values.update(overrides)
    return make_submission(**values)


def _args(source, evidence, start, policy):
    return (start, evidence, policy, source[0], source[1], source[2], source[3], *source[4])


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


def _refresh_start(start, **changes):
    payload = start.to_dict()
    payload.update(changes)
    payload["start_digest"] = ""
    value = Rec(**payload)
    value.start_digest = start_digest(value)
    return value


class LifecycleTransitionStartV022Test(unittest.TestCase):
    def test_started_routes_to_completion_review_without_mutation(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        start = _start(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, start, policy))
        self.assertEqual(STARTED, artifact.status)
        self.assertTrue(artifact.lifecycle_transition_started)
        self.assertTrue(artifact.ready_for_separate_transition_completion_review)
        self.assertTrue(artifact.transition_completion_review_required_next)
        self.assertFalse(artifact.lifecycle_transition_completed)
        self.assertFalse(artifact.lifecycle_transition_performed)
        self.assertFalse(artifact.lifecycle_state_changed)
        self.assertFalse(artifact.repository_changed)

    def test_operator_authority_failure_denies_without_start(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source, operator_authority_verified=False)
        start = _start(source, evidence)
        artifact = verify_artifact(*_args(source, evidence, start, policy))
        self.assertEqual(DENIED, artifact.status)
        self.assertTrue(artifact.transition_start_denied)
        self.assertFalse(artifact.lifecycle_transition_started)
        self.assertTrue(artifact.transition_restart_or_reauthorization_required_next)

    def test_non_authorized_source_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        start = _start(source, evidence)
        bad_source = (
            source[0],
            source[1],
            source[2],
            _refresh_record(source[3], status="not-authorized"),
            source[4],
        )
        artifact = verify_artifact(*_args(bad_source, evidence, start, policy))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.transition_start_record_issued)

    def test_completion_review_route_swap_is_rejected(self):
        source = _source()
        policy = _policy(source)
        evidence = _evidence(source)
        start = _refresh_start(
            _start(source, evidence),
            transition_completion_review_route_digest="bad-route",
        )
        artifact = verify_artifact(*_args(source, evidence, start, policy))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
