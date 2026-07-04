import unittest

from runtime.kuuos_lifecycle_governance_post_apoptosis_quarantine_v0_32 import (
    BLOCKED,
    QUARANTINED,
    REJECTED,
    Rec,
    make_evidence,
    make_policy,
    make_quarantine,
    quarantine_digest,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_apoptosis_closure_review_v0_31 import verify_artifact as verify_closure_artifact
from tests.test_kuuos_lifecycle_apoptosis_closure_review_v0_31 import (
    args as closure_args,
    closure_review as make_closure_review,
    evidence as closure_evidence,
    policy as closure_policy,
    source as closure_source,
)


def source():
    src = closure_source()
    pol = closure_policy()
    ev = closure_evidence(src)
    cr = make_closure_review(src, ev)
    rec = verify_closure_artifact(*closure_args(src, ev, cr, pol))
    return cr, ev, pol, rec, tuple(closure_args(src, ev, cr, pol)[3:])


def policy():
    return make_policy(
        "post-apoptosis-quarantine-policy-v0-32",
        allowed_quarantine_guardian_ids=("post-apoptosis-quarantine-guardian-001",),
        allowed_quarantine_guardian_organization_ids=("post-apoptosis-quarantine-organization",),
        max_quarantine_delay_seconds=120,
        max_evidence_age_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].reviewed_at_epoch_seconds
    data = dict(
        evidence_id="post-apoptosis-quarantine-evidence-001",
        quarantine_id="post-apoptosis-quarantine-001",
        quarantine_guardian_id="post-apoptosis-quarantine-guardian-001",
        quarantine_guardian_organization_id="post-apoptosis-quarantine-organization",
        quarantine_guardian_mandate_receipt_digest="m" * 64,
        quarantine_guardian_mandate_verified=True,
        quarantine_guardian_authority_receipt_digest="a" * 64,
        quarantine_guardian_authority_verified=True,
        quarantine_guardian_identity_confirmation_digest="i" * 64,
        quarantine_guardian_identity_confirmed=True,
        quarantine_boundary_digest="q" * 64,
        quarantine_boundary_confirmed=True,
        observation_window_digest="o" * 64,
        memorial_record_read_only=True,
        non_resurrection_covenant_active=True,
        authority_closed=True,
        dependency_ingress_closed=True,
        activation_route_closed=True,
        successor_captures_quarantined_target=False,
        reactivation_route_present=False,
        quarantine_confirmed=True,
        blocking_reason_digest="",
        institutional_hold_active=False,
        emergency_state_active=False,
        repository_changed=False,
        external_operation_performed=False,
        quarantine_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        quarantined_at_epoch_seconds=t + 3,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def quarantine(src, ev, **kw):
    t = src[0].reviewed_at_epoch_seconds
    data = dict(
        quarantine_id=ev.quarantine_id,
        quarantine_guardian_id=ev.quarantine_guardian_id,
        quarantine_guardian_organization_id=ev.quarantine_guardian_organization_id,
        quarantine_requested_at_epoch_seconds=t + 1,
        quarantined_at_epoch_seconds=t + 3,
        source_closure=src[0],
        source_record=src[3],
        quarantine_evidence=ev,
        quarantine_boundary_digest=ev.quarantine_boundary_digest,
        observation_window_digest=ev.observation_window_digest,
        observation_route_digest=ev.observation_route_digest,
        quarantine_confirmed=ev.quarantine_confirmed,
        blocking_reason_digest=ev.blocking_reason_digest,
    )
    data.update(kw)
    return make_quarantine(**data)


def args(src, ev, qt, pol):
    return qt, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_quarantine(qt, **kw):
    data = qt.to_dict(); data.update(kw); data["quarantine_digest"] = ""
    out = Rec(**data); out.quarantine_digest = quarantine_digest(out); return out


class PostApoptosisQuarantineV032Test(unittest.TestCase):
    def test_quarantined_routes_to_observation(self):
        src = source(); ev = evidence(src); qt = quarantine(src, ev)
        art = verify_artifact(*args(src, ev, qt, policy()))
        self.assertEqual(QUARANTINED, art.status)
        self.assertTrue(art.post_apoptosis_observation_required_next)
        self.assertTrue(art.non_resurrection_covenant_active)
        self.assertTrue(art.memorial_record_read_only)
        self.assertFalse(art.repository_changed)

    def test_reactivation_route_blocks(self):
        src = source(); ev = evidence(src, reactivation_route_present=True); qt = quarantine(src, ev)
        art = verify_artifact(*args(src, ev, qt, policy()))
        self.assertEqual(BLOCKED, art.status)
        self.assertFalse(art.post_apoptosis_observation_required_next)

    def test_non_closed_source_is_rejected(self):
        src = source(); ev = evidence(src); qt = quarantine(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-closed"), src[4])
        art = verify_artifact(*args(bad, ev, qt, policy()))
        self.assertEqual(REJECTED, art.status)
        self.assertFalse(art.post_apoptosis_quarantine_record_issued)

    def test_observation_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        qt = refresh_quarantine(quarantine(src, ev), observation_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, qt, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
