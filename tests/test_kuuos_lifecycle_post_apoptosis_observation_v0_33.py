import unittest

from runtime.kuuos_lifecycle_governance_post_apoptosis_observation_v0_33 import (
    ALERT,
    REJECTED,
    STABLE,
    Rec,
    make_evidence,
    make_observation,
    make_policy,
    observation_digest,
    record_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_governance_post_apoptosis_quarantine_v0_32 import verify_artifact as verify_quarantine_artifact
from tests.test_kuuos_lifecycle_post_apoptosis_quarantine_v0_32 import (
    args as quarantine_args,
    evidence as quarantine_evidence,
    policy as quarantine_policy,
    quarantine as make_quarantine,
    source as quarantine_source,
)


def source():
    src = quarantine_source()
    pol = quarantine_policy()
    ev = quarantine_evidence(src)
    qt = make_quarantine(src, ev)
    rec = verify_quarantine_artifact(*quarantine_args(src, ev, qt, pol))
    return qt, ev, pol, rec, tuple(quarantine_args(src, ev, qt, pol)[3:])


def policy():
    return make_policy(
        "post-apoptosis-observation-policy-v0-33",
        allowed_observer_ids=("post-apoptosis-observer-001",),
        allowed_observer_organization_ids=("post-apoptosis-observation-organization",),
        max_observation_delay_seconds=120,
        max_evidence_age_seconds=120,
    )


def evidence(src, **kw):
    t = src[0].quarantined_at_epoch_seconds
    data = dict(
        evidence_id="post-apoptosis-observation-evidence-001",
        observation_id="post-apoptosis-observation-001",
        observer_id="post-apoptosis-observer-001",
        observer_organization_id="post-apoptosis-observation-organization",
        observer_mandate_receipt_digest="m" * 64,
        observer_mandate_verified=True,
        observer_authority_receipt_digest="a" * 64,
        observer_authority_verified=True,
        observer_identity_confirmation_digest="i" * 64,
        observer_identity_confirmed=True,
        stability_window_digest="w" * 64,
        observation_receipt_digest="o" * 64,
        memorial_record_read_only=True,
        non_resurrection_covenant_active=True,
        authority_closed=True,
        dependency_ingress_closed=True,
        activation_route_closed=True,
        successor_captures_quarantined_target=False,
        reactivation_route_present=False,
        quarantine_boundary_drift_detected=False,
        stability_confirmed=True,
        alert_reason_digest="",
        institutional_hold_active=False,
        emergency_state_active=False,
        repository_changed=False,
        external_operation_performed=False,
        observation_requested_at_epoch_seconds=t + 1,
        captured_at_epoch_seconds=t + 2,
        observed_at_epoch_seconds=t + 3,
    )
    data.update(kw)
    return make_evidence(src[0], src[1], src[2], src[3], src[4], **data)


def observation(src, ev, **kw):
    t = src[0].quarantined_at_epoch_seconds
    data = dict(
        observation_id=ev.observation_id,
        observer_id=ev.observer_id,
        observer_organization_id=ev.observer_organization_id,
        observation_requested_at_epoch_seconds=t + 1,
        observed_at_epoch_seconds=t + 3,
        source_quarantine=src[0],
        source_record=src[3],
        observation_evidence=ev,
        stability_window_digest=ev.stability_window_digest,
        observation_receipt_digest=ev.observation_receipt_digest,
        long_term_memory_route_digest=ev.long_term_memory_route_digest,
        stability_confirmed=ev.stability_confirmed,
        alert_reason_digest=ev.alert_reason_digest,
    )
    data.update(kw)
    return make_observation(**data)


def args(src, ev, obs, pol):
    return obs, ev, pol, src[0], src[1], src[2], src[3], *src[4]


def refresh_record(rec, **kw):
    data = rec.to_dict(); data.update(kw); data["record_digest"] = ""
    out = Rec(**data); out.record_digest = record_digest(out); return out


def refresh_observation(obs, **kw):
    data = obs.to_dict(); data.update(kw); data["observation_digest"] = ""
    out = Rec(**data); out.observation_digest = observation_digest(out); return out


class PostApoptosisObservationV033Test(unittest.TestCase):
    def test_stable_routes_to_long_term_memory(self):
        src = source(); ev = evidence(src); obs = observation(src, ev)
        art = verify_artifact(*args(src, ev, obs, policy()))
        self.assertEqual(STABLE, art.status)
        self.assertTrue(art.long_term_memory_required_next)
        self.assertTrue(art.non_resurrection_covenant_active)
        self.assertTrue(art.memorial_record_read_only)
        self.assertFalse(art.repository_changed)

    def test_boundary_drift_alerts(self):
        src = source(); ev = evidence(src, quarantine_boundary_drift_detected=True); obs = observation(src, ev)
        art = verify_artifact(*args(src, ev, obs, policy()))
        self.assertEqual(ALERT, art.status)
        self.assertFalse(art.long_term_memory_required_next)
        self.assertTrue(art.post_apoptosis_observation_response_required_next)

    def test_non_quarantined_source_is_rejected(self):
        src = source(); ev = evidence(src); obs = observation(src, ev)
        bad = (src[0], src[1], src[2], refresh_record(src[3], status="not-quarantined"), src[4])
        art = verify_artifact(*args(bad, ev, obs, policy()))
        self.assertEqual(REJECTED, art.status)
        self.assertFalse(art.post_apoptosis_observation_record_issued)

    def test_long_term_memory_route_swap_is_rejected(self):
        src = source(); ev = evidence(src)
        obs = refresh_observation(observation(src, ev), long_term_memory_route_digest="bad-route")
        art = verify_artifact(*args(src, ev, obs, policy()))
        self.assertEqual(REJECTED, art.status)


if __name__ == "__main__":
    unittest.main()
