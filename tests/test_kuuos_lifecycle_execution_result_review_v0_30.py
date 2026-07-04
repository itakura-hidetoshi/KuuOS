import unittest

from runtime.kuuos_lifecycle_governance_execution_result_review_v0_30 import (
    ACCEPTED, FAILED, REJECTED, Rec, make_evidence, make_policy,
    make_review, record_digest, review_digest, verify_artifact,
)
from runtime.kuuos_lifecycle_governance_bounded_repository_mutation_execution_v0_29 import verify_artifact as verify_execution_artifact
from tests.test_kuuos_lifecycle_bounded_repository_mutation_execution_v0_29 import (
    args as execution_args, evidence as execution_evidence,
    execution as make_execution_event, policy as execution_policy, source as execution_source,
)


def source():
    src = execution_source()
    pol = execution_policy()
    ev = execution_evidence(src)
    ex = make_execution_event(src, ev)
    rec = verify_execution_artifact(*execution_args(src, ev, ex, pol))
    return ex, ev, pol, rec, tuple(execution_args(src, ev, ex, pol)[3:])


def policy():
    return make_policy(
        "execution-result-review-policy-v0-30",
        allowed_result_reviewer_ids=("execution-result-reviewer-001",),
        allowed_result_reviewer_organization_ids=("execution-result-review-organization",),
        max_review_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_result_adoption_delay_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].executed_at_epoch_seconds
    data = dict(
        evidence_id="execution-result-review-evidence-001",
        review_id="execution-result-review-001",
        result_reviewer_id="execution-result-reviewer-001",
        result_reviewer_organization_id="execution-result-review-organization",
        result_reviewer_mandate_receipt_digest="m" * 64,
        result_reviewer_mandate_verified=True,
        result_reviewer_authority_receipt_digest="a" * 64,
        result_reviewer_authority_verified=True,
        result_reviewer_identity_confirmation_digest="i" * 64,
        result_reviewer_identity_confirmed=True,
        execution_record_freshness_receipt_digest="r" * 64,
        execution_record_fresh=True,
        bounded_execution_receipt_freshness_digest="b" * 64,
        bounded_execution_receipt_fresh=True,
        result_review_receipt_digest="v" * 64,
        result_consistency_receipt_digest="c" * 64,
        result_consistency_valid=True,
        source_trace_receipt_digest="s" * 64,
        source_trace_valid=True,
        result_accepted=True,
        failure_reason_digest="",
        unresolved_anomaly_present=False,
        recovery_in_progress=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        external_operation_performed=False,
        file_written=False,
        ref_updated=False,
        branch_moved=False,
        terminal_marker_written=False,
        resource_removed=False,
        review_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        reviewed_at_epoch_seconds=t + 3,
        result_adoption_deadline_at_epoch_seconds=t + 63,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def review(src, ev, **kw):
    t = src[0].executed_at_epoch_seconds
    data = dict(
        review_id=ev.review_id,
        result_reviewer_id=ev.result_reviewer_id,
        result_reviewer_organization_id=ev.result_reviewer_organization_id,
        review_requested_at_epoch_seconds=t + 1,
        reviewed_at_epoch_seconds=t + 3,
        source_execution=src[0],
        source_record=src[3],
        review_evidence=ev,
        result_review_receipt_digest=ev.result_review_receipt_digest,
        result_adoption_route_digest=ev.result_adoption_route_digest,
        result_adoption_deadline_at_epoch_seconds=t + 63,
        result_accepted=ev.result_accepted,
        failure_reason_digest=ev.failure_reason_digest,
    )
    data.update(kw)
    return make_review(**data)


def args(src, ev, rv, pol):
    return rv, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_review(rv, **kw):
    data = rv.to_dict(); data.update(kw); data["review_digest"] = ""
    out = Rec(**data); out.review_digest = review_digest(out); return out


class ExecutionResultReviewV030Test(unittest.TestCase):
    def test_accepted_routes_to_result_adoption(self):
        src = source(); ev = evidence(src); rv = review(src, ev)
        art = verify_artifact(*args(src, ev, rv, policy()))
        self.assertEqual(ACCEPTED, art.status)
        self.assertTrue(art.execution_result_adoption_required_next)
        self.assertFalse(art.repository_changed)

    def test_reviewer_authority_failure_fails(self):
        src = source(); ev = evidence(src, result_reviewer_authority_verified=False); rv = review(src, ev)
        art = verify_artifact(*args(src, ev, rv, policy()))
        self.assertEqual(FAILED, art.status)
        self.assertFalse(art.execution_result_adoption_required_next)

    def test_non_executed_source_is_rejected(self):
        src = source(); ev = evidence(src); rv = review(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-executed"), src[4])
        art = verify_artifact(*args(bad, ev, rv, policy()))
        self.assertEqual(REJECTED, art.status)

    def test_result_adoption_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        rv = refresh_review(review(src, ev), result_adoption_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, rv, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
