#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_bounded_policy_activation_authorization_intake_v0_1 import *
from scripts.check_actos_dukkha_preserving_bounded_policy_activation_authorization_fixture_v0_1 import (
    build,
    context,
    evidence,
    redigest_context,
    redigest_evidence,
    redigest_review,
    review,
    source,
)


def assert_route(result, expected):
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["bounded_policy_activation_authorization_disposition"] == expected
    supported = expected == DISPOSITION_SUPPORTED
    assert receipt["bounded_policy_activation_authorization_granted"] is supported
    assert receipt["bounded_policy_activation_authorization_debt_open"] is (not supported)
    assert receipt["single_use_policy_activation_authorization_reserved"] is supported
    assert receipt["policy_activation_authorization_token_issued"] is supported
    assert receipt["policy_activation_authorization_token_consumed"] is False
    assert receipt["policy_activation_handoff_prepared"] is supported
    assert receipt["policy_activation_completed"] is False
    assert receipt["maintenance_policy_candidate_activated"] is False
    assert receipt["current_policy_activated"] is False
    assert receipt["policy_activation_performed"] is False
    assert receipt["maintenance_action_performed"] is False
    assert receipt["persistent_world_state_changed_by_authorization"] is False
    assert receipt["world_model_revision_incremented_by_authorization"] is False
    assert receipt["current_plan_revised_by_authorization"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["execution_permission"] is False
    assert receipt["current_policy_activation_authority_granted"] is False
    assert receipt["active_now"] is False


def main():
    supported = build()
    assert_route(supported, DISPOSITION_SUPPORTED)
    receipt = supported.receipt
    assert receipt is not None
    assert receipt["bounded_policy_activation_authorization_state_after"] == (
        STATE_AFTER_SUPPORTED
    )
    assert receipt["policy_activation_authorization_token_envelope"] is not None
    assert receipt["policy_activation_handoff_envelope"] is not None
    assert receipt["bounded_policy_activation_authorization_debt_consumption_record"][
        "activation_authorization_debt_consumed"
    ] is True

    src = source()
    ev = evidence(src)
    rv = review(src, ev)
    cx = context(src, ev, rv)

    world_cx = deepcopy(cx)
    world_cx["current_world_model_state_digest"] = "stale-world"
    world_cx = redigest_context(src, ev, rv, world_cx)
    assert_route(
        build(bounded_policy_activation_authorization_intake_context=world_cx),
        DISPOSITION_WORLD_REFRESH,
    )

    stale_cx = deepcopy(cx)
    stale_cx["activation_authorization_intake_epoch"] = (
        stale_cx["source_policy_activation_review_epoch"]
        + stale_cx["maximum_activation_authorization_intake_delay"]
        + 1
    )
    stale_cx = redigest_context(src, ev, rv, stale_cx)
    assert_route(
        build(bounded_policy_activation_authorization_intake_context=stale_cx),
        DISPOSITION_CONTEXT_REFRESH,
    )

    stale_rv = deepcopy(rv)
    stale_rv["review_completed_epoch"] = (
        stale_rv["review_started_epoch"]
        + stale_rv["maximum_review_duration"]
        + 1
    )
    stale_rv = redigest_review(stale_rv, ev)
    assert_route(
        build(
            bounded_policy_activation_authorization_review_certificate=stale_rv
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    insufficient_ev = deepcopy(ev)
    insufficient_ev["independent_activation_authorization_evidence"] = False
    insufficient_ev = redigest_evidence(insufficient_ev)
    assert_route(
        build(
            bounded_policy_activation_authorization_evidence_packet=insufficient_ev
        ),
        DISPOSITION_ADDITIONAL_EVIDENCE,
    )

    review_routes = (
        ("source_receipt_correspondence_confirmed", DISPOSITION_SOURCE_REPAIR),
        (
            "policy_activation_review_record_correspondence_confirmed",
            DISPOSITION_REVIEW_RECORD_REPAIR,
        ),
        (
            "activation_authorization_handoff_correspondence_confirmed",
            DISPOSITION_HANDOFF_REPAIR,
        ),
        (
            "maintenance_policy_candidate_correspondence_confirmed",
            DISPOSITION_CANDIDATE_REPAIR,
        ),
        (
            "authorization_scope_exactly_bounded",
            DISPOSITION_SCOPE_REPAIR,
        ),
        (
            "activation_preconditions_adequate",
            DISPOSITION_PRECONDITION_REPAIR,
        ),
        ("rollback_plan_adequate", DISPOSITION_ROLLBACK_REPAIR),
        (
            "post_activation_monitoring_guard_adequate",
            DISPOSITION_MONITORING_GUARD_REPAIR,
        ),
        ("uncertainty_adequate", DISPOSITION_UNCERTAINTY_REPAIR),
        ("calibration_adequate", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
    )
    for field, expected in review_routes:
        routed = deepcopy(rv)
        routed[field] = False
        routed = redigest_review(routed, ev)
        assert_route(
            build(
                bounded_policy_activation_authorization_review_certificate=routed
            ),
            expected,
        )

    nonexternal = deepcopy(rv)
    nonexternal["protected_group_nonexternalization_supported"] = False
    nonexternal = redigest_review(nonexternal, ev)
    assert_route(
        build(
            bounded_policy_activation_authorization_review_certificate=nonexternal
        ),
        DISPOSITION_NONEXTERNALIZATION_REVIEW,
    )

    mutation_ev = deepcopy(ev)
    mutation_ev["current_policy_activated"] = True
    mutation_ev = redigest_evidence(mutation_ev)
    assert_route(
        build(
            bounded_policy_activation_authorization_evidence_packet=mutation_ev
        ),
        DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    )

    escalation_ev = deepcopy(ev)
    escalation_ev["authority_escalation_claimed"] = True
    escalation_ev = redigest_evidence(escalation_ev)
    assert_route(
        build(
            bounded_policy_activation_authorization_evidence_packet=escalation_ev
        ),
        DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    )

    replay_cx = deepcopy(cx)
    replay_cx["prior_activation_authorization_intake_session_ids"] = [
        replay_cx["activation_authorization_intake_session_id"]
    ]
    replay_cx = redigest_context(src, ev, rv, replay_cx)
    assert_route(
        build(bounded_policy_activation_authorization_intake_context=replay_cx),
        DISPOSITION_REPLAY_REJECTED,
    )

    tampered_source = source()
    tampered_source["activation_authorization_handoff_envelope"][
        "activation_authorization_state"
    ] = "tampered"
    blocked = build(source_verifyos_receipt=tampered_source)
    assert blocked.status == STATUS_BLOCKED
    assert blocked.receipt is None
    assert any(
        "activation_authorization_handoff_envelope_digest" in item
        for item in blocked.blockers
    )

    bad_bundle = build(
        bounded_policy_activation_authorization_bundle_digest="wrong"
    )
    assert bad_bundle.status == STATUS_BLOCKED
    assert (
        "bounded_policy_activation_authorization_bundle_digest_mismatch"
        in bad_bundle.blockers
    )

    print(
        "PASS: ActOS v0.12 bounded policy activation authorization "
        "actual-chain and 20 dispositions"
    )


if __name__ == "__main__":
    main()
