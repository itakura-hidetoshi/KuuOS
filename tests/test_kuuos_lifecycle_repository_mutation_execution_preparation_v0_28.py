import unittest

from runtime.kuuos_lifecycle_governance_repository_mutation_execution_preparation_v0_28 import (
    BLOCKED,
    PREPARED,
    REJECTED,
    Rec,
    make_evidence,
    make_policy,
    make_preparation,
    preparation_digest,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_repository_mutation_authorization_v0_27 import (
    verify_artifact as verify_authorization_artifact,
)
from tests.test_kuuos_lifecycle_repository_mutation_authorization_v0_27 import (
    _args as _authorization_args,
    _authorization,
    _evidence as _authorization_evidence,
    _policy as _authorization_policy,
    _source as _authorization_source,
)


def _source():
    src = _authorization_source()
    pol = _authorization_policy(src)
    ev = _authorization_evidence(src)
    auth = _authorization(src, ev)
    rec = verify_authorization_artifact(*_authorization_args(src, ev, auth, pol))
    return auth, ev, pol, rec, tuple(_authorization_args(src, ev, auth, pol)[3:])


def _policy():
    return make_policy(
        "lifecycle-bounded-repository-mutation-execution-preparation-policy-v0-28",
        allowed_preparer_ids=("repository-mutation-execution-preparer-001",),
        allowed_preparer_organization_ids=("repository-mutation-execution-preparation-organization",),
        max_preparation_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_execution_delay_seconds=120,
    )


def _evidence(source, **kw):
    t = source[0].authorized_at_epoch_seconds
    data = dict(
        evidence_id="repository-mutation-execution-preparation-evidence-001",
        preparation_id="repository-mutation-execution-preparation-001",
        preparer_id="repository-mutation-execution-preparer-001",
        preparer_organization_id="repository-mutation-execution-preparation-organization",
        preparer_mandate_receipt_digest="m" * 64,
        preparer_mandate_verified=True,
        preparer_authority_receipt_digest="a" * 64,
        preparer_authority_verified=True,
        preparer_identity_confirmation_digest="i" * 64,
        preparer_identity_confirmed=True,
        authorization_record_freshness_receipt_digest="r" * 64,
        authorization_record_fresh=True,
        bounded_execution_plan_digest="e" * 64,
        bounded_execution_plan_receipt_digest="p" * 64,
        bounded_execution_plan_valid=True,
        sandbox_allocation_receipt_digest="s" * 64,
        sandbox_allocation_valid=True,
        checkpoint_intent_receipt_digest="c" * 64,
        checkpoint_intent_valid=True,
        mutation_package_integrity_receipt_digest="k" * 64,
        mutation_package_integrity_valid=True,
        execution_constraints_receipt_digest="x" * 64,
        execution_constraints_valid=True,
        rollback_plan_receipt_digest="b" * 64,
        rollback_plan_valid=True,
        preparation_confirmed=True,
        blocking_reason_digest="",
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
        preparation_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        prepared_at_epoch_seconds=t + 3,
        mutation_execution_deadline_at_epoch_seconds=t + 63,
    )
    data.update(kw)
    return make_evidence(source[0], source[1], source[2], source[3], source[4], **data)


def _prep(source, evidence, **kw):
    t = source[0].authorized_at_epoch_seconds
    data = dict(
        preparation_id=evidence.preparation_id,
        preparer_id=evidence.preparer_id,
        preparer_organization_id=evidence.preparer_organization_id,
        preparation_requested_at_epoch_seconds=t + 1,
        prepared_at_epoch_seconds=t + 3,
        source_authorization=source[0],
        source_record=source[3],
        preparation_evidence=evidence,
        bounded_execution_plan_digest=evidence.bounded_execution_plan_digest,
        mutation_execution_route_digest=evidence.mutation_execution_route_digest,
        mutation_execution_deadline_at_epoch_seconds=t + 63,
        preparation_confirmed=evidence.preparation_confirmed,
        blocking_reason_digest=evidence.blocking_reason_digest,
    )
    data.update(kw)
    return make_preparation(**data)


def _args(source, evidence, prep, policy):
    return prep, evidence, policy, source[0], source[1], source[2], source[3], *source[4]


def _refresh_record(record, **changes):
    payload = record.to_dict()
    payload.update(changes)
    payload["record_digest"] = ""
    out = Rec(**payload)
    out.record_digest = record_digest(out)
    return out


def _refresh_preparation(prep, **changes):
    payload = prep.to_dict()
    payload.update(changes)
    payload["preparation_digest"] = ""
    out = Rec(**payload)
    out.preparation_digest = preparation_digest(out)
    return out


class LifecycleRepositoryMutationExecutionPreparationV028Test(unittest.TestCase):
    def test_prepared_routes_without_repository_mutation(self):
        src = _source()
        ev = _evidence(src)
        prep = _prep(src, ev)
        artifact = verify_artifact(*_args(src, ev, prep, _policy()))
        self.assertEqual(PREPARED, artifact.status)
        self.assertTrue(artifact.bounded_repository_mutation_execution_required_next)
        self.assertFalse(artifact.repository_mutation_performed)
        self.assertFalse(artifact.repository_changed)

    def test_preparer_authority_failure_blocks(self):
        src = _source()
        ev = _evidence(src, preparer_authority_verified=False)
        prep = _prep(src, ev)
        artifact = verify_artifact(*_args(src, ev, prep, _policy()))
        self.assertEqual(BLOCKED, artifact.status)
        self.assertFalse(artifact.bounded_repository_mutation_execution_required_next)

    def test_non_authorized_source_is_rejected(self):
        src = _source()
        ev = _evidence(src)
        prep = _prep(src, ev)
        bad = (src[0], src[1], src[2], _refresh_record(src[3], status="not-authorized"), src[4])
        artifact = verify_artifact(*_args(bad, ev, prep, _policy()))
        self.assertEqual(REJECTED, artifact.status)
        self.assertFalse(artifact.repository_mutation_execution_preparation_record_issued)

    def test_route_swap_is_rejected(self):
        src = _source()
        ev = _evidence(src)
        prep = _refresh_preparation(_prep(src, ev), mutation_execution_route_digest="bad-route")
        artifact = verify_artifact(*_args(src, ev, prep, _policy()))
        self.assertEqual(REJECTED, artifact.status)


if __name__ == "__main__":
    unittest.main()
