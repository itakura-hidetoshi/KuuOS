import unittest

from runtime.kuuos_lifecycle_governance_completion_v0_36 import (
    ALERT,
    COMPLETED,
    REJECTED,
    Rec,
    completion_digest,
    make_completion,
    make_evidence,
    make_policy,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_archive_v0_35 import verify_artifact as verify_stage_artifact
from tests.test_kuuos_lifecycle_archive_v0_35 import (
    args as stage_args,
    archive as make_stage,
    evidence as stage_evidence,
    policy as stage_policy,
    source as stage_source,
)


def source():
    src = stage_source()
    pol = stage_policy()
    ev = stage_evidence(src)
    st = make_stage(src, ev)
    rec = verify_stage_artifact(*stage_args(src, ev, st, pol))
    return st, ev, pol, rec, tuple(stage_args(src, ev, st, pol)[3:])


def policy():
    return make_policy(
        "completion-policy-v0-36",
        allowed_authority_ids=("completion-authority-001",),
        allowed_authority_organization_ids=("completion-organization",),
        max_delay_seconds=120,
        max_evidence_age_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].archived_at_epoch_seconds
    data = dict(
        evidence_id="completion-evidence-001",
        completion_id="completion-001",
        authority_id="completion-authority-001",
        authority_organization_id="completion-organization",
        mandate_receipt_digest="m" * 64,
        mandate_verified=True,
        authority_receipt_digest="a" * 64,
        authority_verified=True,
        identity_confirmation_digest="i" * 64,
        identity_confirmed=True,
        completion_receipt_digest="c" * 64,
        completion_receipt_confirmed=True,
        boundary_confirmed=True,
        memory_seal_confirmed=True,
        memorial_record_read_only=True,
        covenant_active=True,
        no_following_route=True,
        authority_closed=True,
        dependency_ingress_closed=True,
        activation_route_closed=True,
        reactivation_route_present=False,
        completion_confirmed=True,
        alert_reason_digest="",
        institutional_hold_active=False,
        emergency_state_active=False,
        repository_changed=False,
        external_operation_performed=False,
        requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        completed_at_epoch_seconds=t + 3,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def completion(src, ev, **kw):
    t = src[0].archived_at_epoch_seconds
    data = dict(
        completion_id=ev.completion_id,
        authority_id=ev.authority_id,
        authority_organization_id=ev.authority_organization_id,
        requested_at_epoch_seconds=t + 1,
        completed_at_epoch_seconds=t + 3,
        source_stage=src[0],
        source_record=src[3],
        completion_evidence=ev,
        completion_receipt_digest=ev.completion_receipt_digest,
        terminal_digest=ev.terminal_digest,
        completion_confirmed=ev.completion_confirmed,
        alert_reason_digest=ev.alert_reason_digest,
    )
    data.update(kw)
    return make_completion(**data)


def args(src, ev, cp, pol):
    return cp, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_completion(cp, **kw):
    data = cp.to_dict(); data.update(kw); data["completion_digest"] = ""
    out = Rec(**data); out.completion_digest = completion_digest(out); return out


class CompletionV036Test(unittest.TestCase):
    def test_completed_is_terminal(self):
        src = source(); ev = evidence(src); cp = completion(src, ev)
        art = verify_artifact(*args(src, ev, cp, policy()))
        self.assertEqual(COMPLETED, art.status)
        self.assertTrue(art.lifecycle_terminal)
        self.assertFalse(art.following_route_required_next)
        self.assertFalse(art.following_route_permitted)
        self.assertTrue(art.covenant_active)
        self.assertFalse(art.repository_changed)

    def test_authority_failure_alerts(self):
        src = source(); ev = evidence(src, authority_verified=False); cp = completion(src, ev)
        art = verify_artifact(*args(src, ev, cp, policy()))
        self.assertEqual(ALERT, art.status)
        self.assertFalse(art.lifecycle_terminal)
        self.assertTrue(art.completion_response_required_next)

    def test_non_ready_source_is_rejected(self):
        src = source(); ev = evidence(src); cp = completion(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-ready"), src[4])
        art = verify_artifact(*args(bad, ev, cp, policy()))
        self.assertEqual(REJECTED, art.status)
        self.assertFalse(art.completion_record_issued)

    def test_terminal_digest_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        cp = refresh_completion(completion(src, ev), terminal_digest="bad-terminal")
        art = verify_artifact(*args(src, ev, cp, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
