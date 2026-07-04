import unittest

from runtime.kuuos_lifecycle_governance_long_term_memory_v0_34 import (
    ALERT,
    REJECTED,
    SEALED,
    Rec,
    make_evidence,
    make_memory,
    make_policy,
    memory_digest,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_post_apoptosis_observation_v0_33 import verify_artifact as verify_observation_artifact
from tests.test_kuuos_lifecycle_post_apoptosis_observation_v0_33 import (
    args as observation_args,
    evidence as observation_evidence,
    observation as make_observation,
    policy as observation_policy,
    source as observation_source,
)


def source():
    src = observation_source()
    pol = observation_policy()
    ev = observation_evidence(src)
    obs = make_observation(src, ev)
    rec = verify_observation_artifact(*observation_args(src, ev, obs, pol))
    return obs, ev, pol, rec, tuple(observation_args(src, ev, obs, pol)[3:])


def policy():
    return make_policy(
        "long-term-memory-policy-v0-34",
        allowed_memory_steward_ids=("long-term-memory-steward-001",),
        allowed_memory_steward_organization_ids=("long-term-memory-organization",),
        max_memory_delay_seconds=120,
        max_evidence_age_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].observed_at_epoch_seconds
    data = dict(
        evidence_id="long-term-memory-evidence-001",
        memory_id="long-term-memory-001",
        memory_steward_id="long-term-memory-steward-001",
        memory_steward_organization_id="long-term-memory-organization",
        memory_steward_mandate_receipt_digest="m" * 64,
        memory_steward_mandate_verified=True,
        memory_steward_authority_receipt_digest="a" * 64,
        memory_steward_authority_verified=True,
        memory_steward_identity_confirmation_digest="i" * 64,
        memory_steward_identity_confirmed=True,
        memory_seal_digest="s" * 64,
        memory_seal_confirmed=True,
        archive_boundary_digest="b" * 64,
        archive_boundary_confirmed=True,
        memorial_record_read_only=True,
        non_resurrection_covenant_active=True,
        retrieval_read_only=True,
        authority_closed=True,
        dependency_ingress_closed=True,
        activation_route_closed=True,
        reactivation_route_present=False,
        memory_confirmed=True,
        alert_reason_digest="",
        institutional_hold_active=False,
        emergency_state_active=False,
        repository_changed=False,
        external_operation_performed=False,
        memory_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        sealed_at_epoch_seconds=t + 3,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def memory(src, ev, **kw):
    t = src[0].observed_at_epoch_seconds
    data = dict(
        memory_id=ev.memory_id,
        memory_steward_id=ev.memory_steward_id,
        memory_steward_organization_id=ev.memory_steward_organization_id,
        memory_requested_at_epoch_seconds=t + 1,
        sealed_at_epoch_seconds=t + 3,
        source_observation=src[0],
        source_record=src[3],
        memory_evidence=ev,
        memory_seal_digest=ev.memory_seal_digest,
        archive_boundary_digest=ev.archive_boundary_digest,
        archive_route_digest=ev.archive_route_digest,
        memory_confirmed=ev.memory_confirmed,
        alert_reason_digest=ev.alert_reason_digest,
    )
    data.update(kw)
    return make_memory(**data)


def args(src, ev, mem, pol):
    return mem, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_memory(mem, **kw):
    data = mem.to_dict(); data.update(kw); data["memory_digest"] = ""
    out = Rec(**data); out.memory_digest = memory_digest(out); return out


class LongTermMemoryV034Test(unittest.TestCase):
    def test_sealed_routes_to_non_resurrection_archive(self):
        src = source(); ev = evidence(src); mem = memory(src, ev)
        art = verify_artifact(*args(src, ev, mem, policy()))
        self.assertEqual(SEALED, art.status)
        self.assertTrue(art.non_resurrection_archive_required_next)
        self.assertTrue(art.non_resurrection_covenant_active)
        self.assertTrue(art.memorial_record_read_only)
        self.assertFalse(art.repository_changed)

    def test_memory_steward_authority_failure_alerts(self):
        src = source(); ev = evidence(src, memory_steward_authority_verified=False); mem = memory(src, ev)
        art = verify_artifact(*args(src, ev, mem, policy()))
        self.assertEqual(ALERT, art.status)
        self.assertFalse(art.non_resurrection_archive_required_next)
        self.assertTrue(art.long_term_memory_response_required_next)

    def test_non_stable_source_is_rejected(self):
        src = source(); ev = evidence(src); mem = memory(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-stable"), src[4])
        art = verify_artifact(*args(bad, ev, mem, policy()))
        self.assertEqual(REJECTED, art.status)
        self.assertFalse(art.long_term_memory_record_issued)

    def test_archive_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        mem = refresh_memory(memory(src, ev), archive_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, mem, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
