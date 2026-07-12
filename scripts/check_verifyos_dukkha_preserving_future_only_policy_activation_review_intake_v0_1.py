#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_future_only_policy_activation_review_intake_v0_1 import *
from scripts.check_verifyos_dukkha_preserving_future_only_policy_activation_review_fixture_v0_1 import (
    build, context, evidence, redigest_context, redigest_evidence, redigest_review, review, source,
)

def assert_ready(result, disposition):
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["future_only_policy_activation_review_disposition"] == disposition
    assert receipt["maintenance_policy_candidate_activated"] is False
    assert receipt["current_policy_activated"] is False
    assert receipt["maintenance_action_performed"] is False
    assert receipt["activation_authorization_granted"] is False
    assert receipt["persistent_world_state_changed_by_review"] is False
    assert receipt["world_model_revision_incremented_by_review"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    return receipt

def run_route(disposition, *, ev_mut=None, rv_mut=None, cx_mut=None):
    src = source()
    ev = evidence(src)
    if ev_mut:
        ev_mut(ev)
        ev = redigest_evidence(ev)
    rv = review(src, ev)
    if rv_mut:
        rv_mut(rv)
        rv = redigest_review(rv, ev)
    cx = context(src, ev, rv)
    if cx_mut:
        cx_mut(cx, src, ev, rv)
        cx = redigest_context(src, ev, rv, cx)
    result = build(
        source_learnos_receipt=src,
        future_only_policy_activation_review_evidence_packet=ev,
        future_only_policy_activation_review_certificate=rv,
        future_only_policy_activation_review_intake_context=cx,
    )
    receipt = assert_ready(result, disposition)
    supported = disposition == DISPOSITION_SUPPORTED
    assert receipt["policy_activation_review_supported"] is supported
    assert receipt["policy_activation_review_completed"] is supported
    assert receipt["policy_activation_review_debt_open"] is (not supported)
    assert receipt["activation_authorization_handoff_prepared"] is supported
    assert receipt["activation_authorization_completed"] is False
    assert receipt["activation_authorization_debt_open"] is supported
    if supported:
        assert receipt["future_only_policy_activation_review_state_after"] == STATE_AFTER_SUPPORTED
        assert receipt["activation_authorization_handoff_envelope"] is not None
    else:
        assert receipt["future_only_policy_activation_review_state_after"] == STATE_BEFORE
        assert receipt["activation_authorization_handoff_envelope"] is None

def main():
    supported = assert_ready(build(), DISPOSITION_SUPPORTED)
    assert supported["world_fact_confirmed"] is True
    assert supported["causal_attribution_confirmed"] is True
    assert supported["dukkha_reduction_realized_confirmed"] is True
    assert supported["future_only_maintenance_disposition_recorded"] is True
    assert supported["policy_activation_review_recorded"] is True
    assert supported["activation_authorization_handoff_envelope"]["activation_authorization_state"] == "authorization_debt_open"

    run_route(DISPOSITION_REPLAY_REJECTED, cx_mut=lambda c,s,e,r: c["prior_policy_activation_review_intake_session_ids"].append(c["policy_activation_review_intake_session_id"]))
    run_route(DISPOSITION_WORLD_REFRESH, cx_mut=lambda c,s,e,r: c.__setitem__("current_world_model_revision", c["current_world_model_revision"] + 1))
    run_route(DISPOSITION_CONTEXT_REFRESH, cx_mut=lambda c,s,e,r: c.__setitem__("policy_activation_review_intake_epoch", c["source_maintenance_disposition_epoch"] + c["maximum_policy_activation_review_intake_delay"] + 1))
    run_route(DISPOSITION_REVIEW_REFRESH, rv_mut=lambda r: r.__setitem__("review_completed_epoch", r["review_started_epoch"] + r["maximum_review_duration"] + 1))
    run_route(DISPOSITION_ADDITIONAL_EVIDENCE, ev_mut=lambda e: e.__setitem__("independent_policy_activation_review_evidence", False))
    review_routes = (
        ("source_receipt_correspondence_confirmed", DISPOSITION_SOURCE_REPAIR),
        ("maintenance_disposition_record_correspondence_confirmed", DISPOSITION_DISPOSITION_RECORD_REPAIR),
        ("policy_activation_review_handoff_correspondence_confirmed", DISPOSITION_HANDOFF_REPAIR),
        ("maintenance_policy_candidate_correspondence_confirmed", DISPOSITION_CANDIDATE_REPAIR),
        ("policy_activation_scope_exactly_bounded", DISPOSITION_SCOPE_REPAIR),
        ("activation_preconditions_adequate", DISPOSITION_PRECONDITION_REPAIR),
        ("rollback_plan_adequate", DISPOSITION_ROLLBACK_REPAIR),
        ("post_activation_monitoring_guard_adequate", DISPOSITION_MONITORING_GUARD_REPAIR),
        ("uncertainty_adequate", DISPOSITION_UNCERTAINTY_REPAIR),
        ("calibration_adequate", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
    )
    for field, disposition in review_routes:
        run_route(disposition, rv_mut=lambda r, f=field: r.__setitem__(f, False))
    run_route(DISPOSITION_NONEXTERNALIZATION_REVIEW, rv_mut=lambda r: r.__setitem__("protected_group_nonexternalization_supported", False))
    run_route(DISPOSITION_CURRENT_STATE_MUTATION_REJECTED, ev_mut=lambda e: e.__setitem__("maintenance_policy_candidate_activated", True))
    run_route(DISPOSITION_AUTHORITY_ESCALATION_REJECTED, ev_mut=lambda e: e.__setitem__("authority_escalation_claimed", True))

    src = source()
    src["policy_activation_review_handoff_envelope"]["active_now"] = True
    src["policy_activation_review_handoff_envelope_digest"] = canonical_digest(src["policy_activation_review_handoff_envelope"])
    src.pop(SOURCE_RECEIPT_DIGEST_FIELD, None)
    src[SOURCE_RECEIPT_DIGEST_FIELD] = canonical_digest(src)
    blocked = build(source_learnos_receipt=src)
    assert blocked.status == STATUS_BLOCKED
    assert "source_policy_activation_review_handoff_active_now_mismatch" in blocked.blockers

    bad_bundle = build(future_only_policy_activation_review_bundle_digest="wrong")
    assert bad_bundle.status == STATUS_BLOCKED
    assert "future_only_policy_activation_review_bundle_digest_mismatch" in bad_bundle.blockers

    print("PASS: VerifyOS v0.12 future-only policy activation review actual-chain and 20 dispositions")

if __name__ == "__main__":
    main()
