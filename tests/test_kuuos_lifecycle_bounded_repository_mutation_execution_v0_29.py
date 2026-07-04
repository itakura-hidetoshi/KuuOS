import unittest

from runtime.kuuos_lifecycle_governance_bounded_repository_mutation_execution_v0_29 import (
    ABORTED, EXECUTED, REJECTED, Rec, execution_digest,
    make_evidence, make_execution, make_policy, record_digest, verify_artifact,
)
from runtime.kuuos_lifecycle_governance_repository_mutation_execution_preparation_v0_28 import verify_artifact as verify_preparation_artifact
from tests.test_kuuos_lifecycle_repository_mutation_execution_preparation_v0_28 import (
    _args as prep_args, _evidence as prep_evidence, _policy as prep_policy,
    _prep as make_prep, _source as prep_source,
)


def source():
    src = prep_source()
    pol = prep_policy()
    ev = prep_evidence(src)
    prep = make_prep(src, ev)
    rec = verify_preparation_artifact(*prep_args(src, ev, prep, pol))
    return prep, ev, pol, rec, tuple(prep_args(src, ev, prep, pol)[3:])


def policy():
    return make_policy(
        "bounded-repository-mutation-execution-policy-v0-29",
        allowed_executor_ids=("bounded-repository-mutation-executor-001",),
        allowed_executor_organization_ids=("bounded-repository-mutation-execution-organization",),
        max_execution_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_result_review_delay_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].prepared_at_epoch_seconds
    data = dict(
        evidence_id="bounded-repository-mutation-execution-evidence-001",
        execution_id="bounded-repository-mutation-execution-001",
        executor_id="bounded-repository-mutation-executor-001",
        executor_organization_id="bounded-repository-mutation-execution-organization",
        executor_mandate_receipt_digest="m" * 64, executor_mandate_verified=True,
        executor_authority_receipt_digest="a" * 64, executor_authority_verified=True,
        executor_identity_confirmation_digest="i" * 64, executor_identity_confirmed=True,
        preparation_record_freshness_receipt_digest="r" * 64, preparation_record_fresh=True,
        bounded_execution_receipt_digest="e" * 64, bounded_execution_receipt_valid=True,
        mutation_package_integrity_receipt_digest="p" * 64, mutation_package_integrity_valid=True,
        sandbox_receipt_digest="s" * 64, sandbox_receipt_valid=True,
        rollback_guard_receipt_digest="b" * 64, rollback_guard_valid=True,
        execution_confirmed=True, abort_reason_digest="",
        unresolved_anomaly_present=False, recovery_in_progress=False,
        institutional_hold_active=False, emergency_state_active=False,
        external_operation_performed=False, uncontrolled_file_written=False,
        uncontrolled_ref_updated=False, uncontrolled_branch_moved=False,
        terminal_marker_written=False, resource_removed=False,
        execution_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        executed_at_epoch_seconds=t + 3,
        result_review_deadline_at_epoch_seconds=t + 63,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def execution(src, ev, **kw):
    t = src[0].prepared_at_epoch_seconds
    data = dict(
        execution_id=ev.execution_id,
        executor_id=ev.executor_id,
        executor_organization_id=ev.executor_organization_id,
        execution_requested_at_epoch_seconds=t + 1,
        executed_at_epoch_seconds=t + 3,
        source_preparation=src[0], source_record=src[3], execution_evidence=ev,
        bounded_execution_receipt_digest=ev.bounded_execution_receipt_digest,
        result_review_route_digest=ev.result_review_route_digest,
        result_review_deadline_at_epoch_seconds=t + 63,
        execution_confirmed=ev.execution_confirmed,
        abort_reason_digest=ev.abort_reason_digest,
    )
    data.update(kw)
    return make_execution(**data)


def args(src, ev, ex, pol):
    return ex, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_execution(ex, **kw):
    data = ex.to_dict(); data.update(kw); data["execution_digest"] = ""
    out = Rec(**data); out.execution_digest = execution_digest(out); return out


class BoundedRepositoryMutationExecutionV029Test(unittest.TestCase):
    def test_recorded_execution_routes_to_result_review(self):
        src = source(); ev = evidence(src); ex = execution(src, ev)
        art = verify_artifact(*args(src, ev, ex, policy()))
        self.assertEqual(EXECUTED, art.status)
        self.assertTrue(art.repository_mutation_execution_result_review_required_next)
        self.assertFalse(art.repository_changed)

    def test_authority_failure_aborts(self):
        src = source(); ev = evidence(src, executor_authority_verified=False); ex = execution(src, ev)
        art = verify_artifact(*args(src, ev, ex, policy()))
        self.assertEqual(ABORTED, art.status)
        self.assertFalse(art.repository_mutation_execution_result_review_required_next)

    def test_non_prepared_source_is_rejected(self):
        src = source(); ev = evidence(src); ex = execution(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-prepared"), src[4])
        art = verify_artifact(*args(bad, ev, ex, policy()))
        self.assertEqual(REJECTED, art.status)

    def test_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        ex = refresh_execution(execution(src, ev), result_review_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, ex, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
