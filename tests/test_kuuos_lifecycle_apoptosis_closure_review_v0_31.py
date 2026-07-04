import unittest

from runtime.kuuos_lifecycle_governance_apoptosis_closure_review_v0_31 import (
    BLOCKED,
    CLOSED,
    REJECTED,
    Rec,
    closure_review_digest,
    make_closure_review,
    make_evidence,
    make_policy,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_execution_result_review_v0_30 import verify_artifact as verify_review_artifact
from tests.test_kuuos_lifecycle_execution_result_review_v0_30 import (
    args as review_args,
    evidence as review_evidence,
    policy as review_policy,
    review as make_review,
    source as review_source,
)


def source():
    src = review_source()
    pol = review_policy()
    ev = review_evidence(src)
    rv = make_review(src, ev)
    rec = verify_review_artifact(*review_args(src, ev, rv, pol))
    return rv, ev, pol, rec, tuple(review_args(src, ev, rv, pol)[3:])


def policy():
    return make_policy(
        "apoptosis-closure-review-policy-v0-31",
        allowed_closure_reviewer_ids=("apoptosis-closure-reviewer-001",),
        allowed_closure_reviewer_organization_ids=("apoptosis-closure-review-organization",),
        max_closure_review_delay_seconds=120,
        max_evidence_age_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].reviewed_at_epoch_seconds
    data = dict(
        evidence_id="apoptosis-closure-review-evidence-001",
        closure_review_id="apoptosis-closure-review-001",
        closure_reviewer_id="apoptosis-closure-reviewer-001",
        closure_reviewer_organization_id="apoptosis-closure-review-organization",
        closure_reviewer_mandate_receipt_digest="m" * 64,
        closure_reviewer_mandate_verified=True,
        closure_reviewer_authority_receipt_digest="a" * 64,
        closure_reviewer_authority_verified=True,
        closure_reviewer_identity_confirmation_digest="i" * 64,
        closure_reviewer_identity_confirmed=True,
        apoptosis_target_id="candidate-component-001",
        apoptosis_boundary_digest="b" * 64,
        authority_closure_receipt_digest="c" * 64,
        authority_closed=True,
        dependency_ingress_closure_receipt_digest="d" * 64,
        dependency_ingress_closed=True,
        activation_route_closure_receipt_digest="x" * 64,
        activation_route_closed=True,
        quarantine_binding_digest="q" * 64,
        quarantine_binding_confirmed=True,
        memorial_record_digest="r" * 64,
        memorial_record_confirmed=True,
        successor_binding_digest="s" * 64,
        successor_binding_confirmed=False,
        non_resurrection_covenant_digest="n" * 64,
        non_resurrection_covenant_confirmed=True,
        closure_confirmed=True,
        blocking_reason_digest="",
        unresolved_dependency_present=False,
        reactivation_route_present=False,
        institutional_hold_active=False,
        emergency_state_active=False,
        repository_changed=False,
        external_operation_performed=False,
        closure_review_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        reviewed_at_epoch_seconds=t + 3,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def closure_review(src, ev, **kw):
    t = src[0].reviewed_at_epoch_seconds
    data = dict(
        closure_review_id=ev.closure_review_id,
        closure_reviewer_id=ev.closure_reviewer_id,
        closure_reviewer_organization_id=ev.closure_reviewer_organization_id,
        closure_review_requested_at_epoch_seconds=t + 1,
        reviewed_at_epoch_seconds=t + 3,
        source_review=src[0],
        source_record=src[3],
        closure_evidence=ev,
        apoptosis_target_id=ev.apoptosis_target_id,
        apoptosis_boundary_digest=ev.apoptosis_boundary_digest,
        quarantine_binding_digest=ev.quarantine_binding_digest,
        memorial_record_digest=ev.memorial_record_digest,
        non_resurrection_covenant_digest=ev.non_resurrection_covenant_digest,
        post_apoptosis_route_digest=ev.post_apoptosis_route_digest,
        closure_confirmed=ev.closure_confirmed,
        blocking_reason_digest=ev.blocking_reason_digest,
    )
    data.update(kw)
    return make_closure_review(**data)


def args(src, ev, cr, pol):
    return cr, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_closure_review(cr, **kw):
    data = cr.to_dict(); data.update(kw); data["closure_review_digest"] = ""
    out = Rec(**data); out.closure_review_digest = closure_review_digest(out); return out


class ApoptosisClosureReviewV031Test(unittest.TestCase):
    def test_closed_routes_to_post_apoptosis_quarantine(self):
        src = source(); ev = evidence(src); cr = closure_review(src, ev)
        art = verify_artifact(*args(src, ev, cr, policy()))
        self.assertEqual(CLOSED, art.status)
        self.assertTrue(art.post_apoptosis_quarantine_required_next)
        self.assertTrue(art.authority_closed)
        self.assertTrue(art.non_resurrection_covenant_confirmed)
        self.assertFalse(art.repository_changed)

    def test_authority_not_closed_blocks(self):
        src = source(); ev = evidence(src, authority_closed=False); cr = closure_review(src, ev)
        art = verify_artifact(*args(src, ev, cr, policy()))
        self.assertEqual(BLOCKED, art.status)
        self.assertFalse(art.post_apoptosis_quarantine_required_next)

    def test_non_accepted_source_is_rejected(self):
        src = source(); ev = evidence(src); cr = closure_review(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-accepted"), src[4])
        art = verify_artifact(*args(bad, ev, cr, policy()))
        self.assertEqual(REJECTED, art.status)
        self.assertFalse(art.apoptosis_closure_review_record_issued)

    def test_post_apoptosis_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        cr = refresh_closure_review(closure_review(src, ev), post_apoptosis_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, cr, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
