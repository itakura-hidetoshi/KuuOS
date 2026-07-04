import unittest

from runtime.kuuos_lifecycle_governance_execution_result_adoption_v0_31 import (
    ADOPTED, HELD, REJECTED, Rec, adoption_digest, make_adoption,
    make_evidence, make_policy, record_digest, verify_artifact,
)
from runtime.kuuos_lifecycle_governance_execution_result_review_v0_30 import verify_artifact as verify_review_artifact
from tests.test_kuuos_lifecycle_execution_result_review_v0_30 import (
    args as review_args, evidence as review_evidence, policy as review_policy,
    review as make_review, source as review_source,
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
        "execution-result-adoption-policy-v0-31",
        allowed_adopter_ids=("execution-result-adopter-001",),
        allowed_adopter_organization_ids=("execution-result-adoption-organization",),
        max_adoption_delay_seconds=120,
        max_evidence_age_seconds=120,
        max_closure_review_delay_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].reviewed_at_epoch_seconds
    data = dict(
        evidence_id="execution-result-adoption-evidence-001",
        adoption_id="execution-result-adoption-001",
        adopter_id="execution-result-adopter-001",
        adopter_organization_id="execution-result-adoption-organization",
        adopter_mandate_receipt_digest="m" * 64,
        adopter_mandate_verified=True,
        adopter_authority_receipt_digest="a" * 64,
        adopter_authority_verified=True,
        adopter_identity_confirmation_digest="i" * 64,
        adopter_identity_confirmed=True,
        review_record_freshness_receipt_digest="r" * 64,
        review_record_fresh=True,
        adoption_receipt_digest="d" * 64,
        result_adoption_receipt_digest="p" * 64,
        result_adoption_receipt_valid=True,
        adoption_confirmed=True,
        hold_reason_digest="",
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
        adoption_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        adopted_at_epoch_seconds=t + 3,
        closure_review_deadline_at_epoch_seconds=t + 63,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def adoption(src, ev, **kw):
    t = src[0].reviewed_at_epoch_seconds
    data = dict(
        adoption_id=ev.adoption_id,
        adopter_id=ev.adopter_id,
        adopter_organization_id=ev.adopter_organization_id,
        adoption_requested_at_epoch_seconds=t + 1,
        adopted_at_epoch_seconds=t + 3,
        source_review=src[0],
        source_record=src[3],
        adoption_evidence=ev,
        adoption_receipt_digest=ev.adoption_receipt_digest,
        closure_review_route_digest=ev.closure_review_route_digest,
        closure_review_deadline_at_epoch_seconds=t + 63,
        adoption_confirmed=ev.adoption_confirmed,
        hold_reason_digest=ev.hold_reason_digest,
    )
    data.update(kw)
    return make_adoption(**data)


def args(src, ev, ad, pol):
    return ad, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_adoption(ad, **kw):
    data = ad.to_dict(); data.update(kw); data["adoption_digest"] = ""
    out = Rec(**data); out.adoption_digest = adoption_digest(out); return out


class ExecutionResultAdoptionV031Test(unittest.TestCase):
    def test_adopted_routes_to_closure_review(self):
        src = source(); ev = evidence(src); ad = adoption(src, ev)
        art = verify_artifact(*args(src, ev, ad, policy()))
        self.assertEqual(ADOPTED, art.status)
        self.assertTrue(art.lifecycle_closure_review_required_next)
        self.assertFalse(art.repository_changed)

    def test_adopter_authority_failure_holds(self):
        src = source(); ev = evidence(src, adopter_authority_verified=False); ad = adoption(src, ev)
        art = verify_artifact(*args(src, ev, ad, policy()))
        self.assertEqual(HELD, art.status)
        self.assertFalse(art.lifecycle_closure_review_required_next)

    def test_non_accepted_source_is_rejected(self):
        src = source(); ev = evidence(src); ad = adoption(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-accepted"), src[4])
        art = verify_artifact(*args(bad, ev, ad, policy()))
        self.assertEqual(REJECTED, art.status)

    def test_closure_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        ad = refresh_adoption(adoption(src, ev), closure_review_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, ad, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
