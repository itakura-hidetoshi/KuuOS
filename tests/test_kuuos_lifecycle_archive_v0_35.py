import unittest

from runtime.kuuos_lifecycle_governance_archive_v0_35 import (
    ALERT,
    ARCHIVED,
    REJECTED,
    Rec,
    archive_digest,
    make_archive,
    make_evidence,
    make_policy,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_long_term_memory_v0_34 import verify_artifact as verify_memory_artifact
from tests.test_kuuos_lifecycle_long_term_memory_v0_34 import (
    args as memory_args,
    evidence as memory_evidence,
    memory as make_memory,
    policy as memory_policy,
    source as memory_source,
)


def source():
    src = memory_source()
    pol = memory_policy()
    ev = memory_evidence(src)
    mem = make_memory(src, ev)
    rec = verify_memory_artifact(*memory_args(src, ev, mem, pol))
    return mem, ev, pol, rec, tuple(memory_args(src, ev, mem, pol)[3:])


def policy():
    return make_policy(
        "archive-policy-v0-35",
        allowed_archive_steward_ids=("archive-steward-001",),
        allowed_archive_steward_organization_ids=("archive-organization",),
        max_archive_delay_seconds=120,
        max_evidence_age_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].sealed_at_epoch_seconds
    data = dict(
        evidence_id="archive-evidence-001",
        archive_id="archive-001",
        archive_steward_id="archive-steward-001",
        archive_steward_organization_id="archive-organization",
        archive_steward_mandate_receipt_digest="m" * 64,
        archive_steward_mandate_verified=True,
        archive_steward_authority_receipt_digest="a" * 64,
        archive_steward_authority_verified=True,
        archive_steward_identity_confirmation_digest="i" * 64,
        archive_steward_identity_confirmed=True,
        archive_receipt_digest="r" * 64,
        archive_receipt_confirmed=True,
        archive_boundary_confirmed=True,
        memory_seal_confirmed=True,
        memorial_record_read_only=True,
        covenant_active=True,
        retrieval_read_only=True,
        authority_closed=True,
        dependency_ingress_closed=True,
        activation_route_closed=True,
        reactivation_route_present=False,
        archive_confirmed=True,
        alert_reason_digest="",
        institutional_hold_active=False,
        emergency_state_active=False,
        repository_changed=False,
        external_operation_performed=False,
        archive_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        archived_at_epoch_seconds=t + 3,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def archive(src, ev, **kw):
    t = src[0].sealed_at_epoch_seconds
    data = dict(
        archive_id=ev.archive_id,
        archive_steward_id=ev.archive_steward_id,
        archive_steward_organization_id=ev.archive_steward_organization_id,
        archive_requested_at_epoch_seconds=t + 1,
        archived_at_epoch_seconds=t + 3,
        source_memory=src[0],
        source_record=src[3],
        archive_evidence=ev,
        archive_receipt_digest=ev.archive_receipt_digest,
        final_closure_route_digest=ev.final_closure_route_digest,
        archive_confirmed=ev.archive_confirmed,
        alert_reason_digest=ev.alert_reason_digest,
    )
    data.update(kw)
    return make_archive(**data)


def args(src, ev, ar, pol):
    return ar, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_archive(ar, **kw):
    data = ar.to_dict(); data.update(kw); data["archive_digest"] = ""
    out = Rec(**data); out.archive_digest = archive_digest(out); return out


class ArchiveV035Test(unittest.TestCase):
    def test_archived_routes_to_final_closure(self):
        src = source(); ev = evidence(src); ar = archive(src, ev)
        art = verify_artifact(*args(src, ev, ar, policy()))
        self.assertEqual(ARCHIVED, art.status)
        self.assertTrue(art.final_closure_required_next)
        self.assertTrue(art.covenant_active)
        self.assertTrue(art.memorial_record_read_only)
        self.assertFalse(art.repository_changed)

    def test_archive_steward_authority_failure_alerts(self):
        src = source(); ev = evidence(src, archive_steward_authority_verified=False); ar = archive(src, ev)
        art = verify_artifact(*args(src, ev, ar, policy()))
        self.assertEqual(ALERT, art.status)
        self.assertFalse(art.final_closure_required_next)
        self.assertTrue(art.archive_response_required_next)

    def test_non_sealed_source_is_rejected(self):
        src = source(); ev = evidence(src); ar = archive(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-sealed"), src[4])
        art = verify_artifact(*args(bad, ev, ar, policy()))
        self.assertEqual(REJECTED, art.status)
        self.assertFalse(art.archive_record_issued)

    def test_final_closure_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        ar = refresh_archive(archive(src, ev), final_closure_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, ar, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
