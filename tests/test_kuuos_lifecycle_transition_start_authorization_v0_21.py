from runtime.kuuos_lifecycle_governance_transition_start_authorization_v0_21 import (
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
from tests.kuuos_lifecycle_transition_approval_fixture_v0_20 import (
    LifecycleTransitionApprovalFixtureV020,
)


def _source():
    upstream = LifecycleTransitionApprovalFixtureV020(methodName="runTest")
    upstream.setUp()
    approval_source = upstream.make_source()
    approval_evidence = upstream.make_approval_evidence(approval_source)
    approval = upstream.make_approval(approval_source, approval_evidence)
    approval_record = upstream.evaluate_approval(approval_source, approval_evidence, approval)
    source_args = tuple(upstream.artifact_args(approval_source, approval_evidence, approval)[3:])
    return upstream, (approval, approval_evidence, upstream.policy, approval_record, source_args)


def _policy(source):
    return make_policy(
        "lifecycle-bounded-transition-start-authorization-policy-v0-21",
        allowed_transition_start_authorizer_ids=("lifecycle-transition-start-authorizer-001",),
        allowed_transition_start_authorizer_organization_ids=("lifecycle-transition-start-authorizer-organization",),
        allowed_future_transition_operator_ids=(source[0].future_transition_operator_id,),
        max_authorization_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_transition_start_delay_seconds=120,
    )


def _evidence(source, **overrides):
    approved_at = source[0].approved_at_epoch_seconds
    values = dict(
        evidence_id="lifecycle-transition-start-authorization-evidence-001",
        transition_start_authorization_id="lifecycle-transition-start-authorization-001",
        transition_start_authorizer_id="lifecycle-transition-start-authorizer-001",
        transition_start_authorizer_organization_id="lifecycle-transition-start-authorizer-organization",
        authorizer_mandate_receipt_digest="m" * 64,
        authorizer_mandate_verified=True,
        authorizer_authority_receipt_digest="a" * 64,
        authorizer_authority_verified=True,
        authorizer_identity_confirmation_digest="i" * 64,
        authorizer_identity_confirmed=True,
        conflict_disclosure_digest="d" * 64,
        conflict_disclosure_complete=True,
        material_conflict_present=False,
        jurisdiction_receipt_digest="j" * 64,
        jurisdiction_verified=True,
        approval_record_freshness_receipt_digest="r" * 64,
        approval_record_fresh=True,
        package_freshness_receipt_digest="p" * 64,
        package_fresh=True,
        current_state_freshness_receipt_digest="c" * 64,
        current_state_not_stale=True,
        target_state_validity_receipt_digest="t" * 64,
        target_state_still_valid=True,
        transition_start_authorized=True,
        denial_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        repository_changed=False,
        authorization_requested_at_epoch_seconds=approved_at + 1,
        captured_at_epoch_seconds=approved_at + 2,
        authorized_at_epoch_seconds=approved_at + 3,
        transition_start_deadline_at_epoch_seconds=approved_at + 63,
    )
    values.update(overrides)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)


def _authorization(source, evidence, **overrides):
    approved_at = source[0].approved_at_epoch_seconds
    values = dict(
        transition_start_authorization_id="lifecycle-transition-start-authorization-001",
        transition_start_authorizer_id="lifecycle-transition-start-authorizer-001",
        transition_start_authorizer_organization_id="lifecycle-transition-start-authorizer-organization",
        authorization_requested_at_epoch_seconds=approved_at + 1,
        authorized_at_epoch_seconds=approved_at + 3,
        source_approval=source[0],
        source_record=source[3],
        authorization_evidence=evidence,
        transition_start_route_digest=evidence.transition_start_route_digest,
        transition_start_deadline_at_epoch_seconds=approved_at + 63,
        transition_start_authorized=evidence.transition_start_authorized,
        denial_reason_digest=evidence.denial_reason_digest,
    )
    values.update(overrides)
    return make_submission(**values)


def _args(source, evidence, authorization, policy):
    return (authorization, evidence, policy, source[0], source[1], source[2], source[3], *source[4])


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


def test_authorized_routes_to_start_without_starting_transition():
    _, source = _source()
    policy = _policy(source)
    evidence = _evidence(source)
    authorization = _authorization(source, evidence)
    artifact = verify_artifact(*_args(source, evidence, authorization, policy))
    assert artifact.status == AUTHORIZED
    assert artifact.lifecycle_transition_start_authorized
    assert artifact.ready_for_separate_transition_start
    assert artifact.transition_start_required_next
    assert not artifact.lifecycle_transition_started
    assert not artifact.lifecycle_transition_performed
    assert not artifact.repository_changed


def test_authority_failure_denies_without_start_route():
    _, source = _source()
    policy = _policy(source)
    evidence = _evidence(source, authorizer_authority_verified=False)
    authorization = _authorization(source, evidence)
    artifact = verify_artifact(*_args(source, evidence, authorization, policy))
    assert artifact.status == DENIED
    assert artifact.transition_start_authorization_denied
    assert not artifact.lifecycle_transition_start_authorized
    assert artifact.transition_reauthorization_or_reapproval_required_next


def test_non_approved_source_is_rejected():
    _, source = _source()
    policy = _policy(source)
    evidence = _evidence(source)
    authorization = _authorization(source, evidence)
    bad_source = (source[0], source[1], source[2], _refresh_record(source[3], status="not-approved"), source[4])
    artifact = verify_artifact(*_args(bad_source, evidence, authorization, policy))
    assert artifact.status == REJECTED
    assert not artifact.transition_start_authorization_record_issued


def test_route_swap_is_rejected():
    _, source = _source()
    policy = _policy(source)
    evidence = _evidence(source)
    authorization = _refresh_authorization(_authorization(source, evidence), transition_start_route_digest="bad-route")
    artifact = verify_artifact(*_args(source, evidence, authorization, policy))
    assert artifact.status == REJECTED
