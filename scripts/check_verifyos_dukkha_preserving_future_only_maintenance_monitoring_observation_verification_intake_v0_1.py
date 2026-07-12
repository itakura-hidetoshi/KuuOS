#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake_v0_1 import *
from scripts.check_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_fixture_v0_1 import (
    build,
    context,
    evidence,
    redigest_context,
    redigest_evidence,
    redigest_review,
    review,
    source,
)


def assert_disposition(result, disposition):
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["maintenance_monitoring_verification_disposition"] == disposition
    assert receipt["verifyos_version"] == "v0.11"
    assert receipt["world_fact_confirmed"] is True
    assert receipt["causal_attribution_confirmed"] is True
    assert receipt["dukkha_reduction_realized_confirmed"] is True
    assert receipt["future_only_learning_delta_recorded"] is True
    assert receipt["future_only_learning_delta_activated"] is False
    assert receipt["maintenance_monitoring_observation_recorded"] is True
    assert receipt["maintenance_monitoring_activated"] is False
    assert receipt["maintenance_action_performed"] is False
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in receipt.items() if key != RECEIPT_DIGEST_FIELD}
    )
    return receipt


def review_route(field, disposition):
    src = source()
    ev = evidence(src)
    rv = review(src, ev)
    rv[field] = False
    rv = redigest_review(rv, ev)
    cx = redigest_context(src, ev, rv, context(src, ev, rv))
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=ev,
            maintenance_monitoring_verification_review_certificate=rv,
            maintenance_monitoring_verification_intake_context=cx,
        ),
        disposition,
    )


def main():
    supported = assert_disposition(build(), DISPOSITION_SUPPORTED)
    assert supported["maintenance_monitoring_verification_state_before"] == STATE_BEFORE
    assert supported["maintenance_monitoring_verification_state_after"] == STATE_AFTER_SUPPORTED
    for field in (
        "maintenance_monitoring_observation_verified",
        "maintenance_monitoring_verification_supported",
        "maintenance_monitoring_verification_scope_exactly_bounded",
        "maintenance_monitoring_verification_completed",
        "maintenance_monitoring_verification_debt_consumed",
        "maintenance_disposition_handoff_prepared",
        "maintenance_disposition_debt_open",
    ):
        assert supported[field] is True
    for field in (
        "maintenance_monitoring_verification_debt_open",
        "maintenance_disposition_completed",
        "verification_evidence_collection_performed_by_kernel",
        "observation_collection_reperformed_by_kernel",
        "persistent_world_state_changed_by_verification",
        "world_model_revision_incremented_by_verification",
        "current_plan_revised_by_verification",
        "current_policy_activated_by_verification",
        "learning_delta_activated_by_verification",
        "tool_invocation_performed",
        "external_side_effect_performed",
        "general_execution_authority_granted",
        "world_mutation_authority_granted",
        "current_policy_activation_authority_granted",
        "maintenance_action_authority_granted_to_verifyos",
        "active_now",
    ):
        assert supported[field] is False

    blocked = build(expected_source_observeos_receipt_digest="wrong")
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert "source_observeos_expected_binding_mismatch" in blocked.blockers

    src = source()
    ev = evidence(src)
    rv = review(src, ev)
    cx = context(src, ev, rv)

    stale = deepcopy(cx)
    stale["current_world_model_state_digest"] = "stale"
    stale = redigest_context(src, ev, rv, stale)
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=ev,
            maintenance_monitoring_verification_review_certificate=rv,
            maintenance_monitoring_verification_intake_context=stale,
        ),
        DISPOSITION_WORLD_REFRESH,
    )

    late = deepcopy(cx)
    late["monitoring_verification_intake_epoch"] = (
        late["source_monitoring_observation_epoch"]
        + late["maximum_monitoring_verification_intake_delay"]
        + 1
    )
    late = redigest_context(src, ev, rv, late)
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=ev,
            maintenance_monitoring_verification_review_certificate=rv,
            maintenance_monitoring_verification_intake_context=late,
        ),
        DISPOSITION_CONTEXT_REFRESH,
    )

    replay = deepcopy(cx)
    replay["prior_monitoring_verification_intake_session_ids"] = [
        replay["monitoring_verification_intake_session_id"]
    ]
    replay = redigest_context(src, ev, rv, replay)
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=ev,
            maintenance_monitoring_verification_review_certificate=rv,
            maintenance_monitoring_verification_intake_context=replay,
        ),
        DISPOSITION_REPLAY_REJECTED,
    )

    old_review = deepcopy(rv)
    old_review["review_completed_epoch"] = (
        old_review["review_started_epoch"] + old_review["maximum_review_duration"] + 1
    )
    old_review = redigest_review(old_review, ev)
    old_context = redigest_context(
        src, ev, old_review, context(src, ev, old_review)
    )
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=ev,
            maintenance_monitoring_verification_review_certificate=old_review,
            maintenance_monitoring_verification_intake_context=old_context,
        ),
        DISPOSITION_REVIEW_REFRESH,
    )

    insufficient = deepcopy(ev)
    insufficient["independent_maintenance_monitoring_verification_evidence"] = False
    insufficient = redigest_evidence(insufficient)
    insufficient_review = redigest_review(rv, insufficient)
    insufficient_context = redigest_context(
        src,
        insufficient,
        insufficient_review,
        context(src, insufficient, insufficient_review),
    )
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=insufficient,
            maintenance_monitoring_verification_review_certificate=insufficient_review,
            maintenance_monitoring_verification_intake_context=insufficient_context,
        ),
        DISPOSITION_ADDITIONAL_EVIDENCE,
    )

    routes = (
        ("source_receipt_correspondence_confirmed", DISPOSITION_SOURCE_REPAIR),
        (
            "observation_record_correspondence_confirmed",
            DISPOSITION_OBSERVATION_RECORD_REPAIR,
        ),
        (
            "verification_handoff_correspondence_confirmed",
            DISPOSITION_HANDOFF_REPAIR,
        ),
        (
            "baseline_observation_correspondence_confirmed",
            DISPOSITION_BASELINE_REPAIR,
        ),
        ("durability_verification_adequate", DISPOSITION_DURABILITY_REPAIR),
        ("adverse_effect_verification_adequate", DISPOSITION_ADVERSE_REPAIR),
        (
            "distributional_verification_adequate",
            DISPOSITION_DISTRIBUTIONAL_REPAIR,
        ),
        (
            "reobservation_trigger_verification_adequate",
            DISPOSITION_REOBSERVATION_TRIGGER_REPAIR,
        ),
        ("uncertainty_adequate", DISPOSITION_UNCERTAINTY_REPAIR),
        ("calibration_adequate", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
        (
            "protected_group_nonexternalization_supported",
            DISPOSITION_NONEXTERNALIZATION_REVIEW,
        ),
    )
    for field, disposition in routes:
        review_route(field, disposition)

    mutating = deepcopy(ev)
    mutating["current_policy_activated"] = True
    mutating = redigest_evidence(mutating)
    mutating_review = redigest_review(rv, mutating)
    mutating_context = redigest_context(
        src, mutating, mutating_review, context(src, mutating, mutating_review)
    )
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=mutating,
            maintenance_monitoring_verification_review_certificate=mutating_review,
            maintenance_monitoring_verification_intake_context=mutating_context,
        ),
        DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    )

    escalating = deepcopy(ev)
    escalating["authority_escalation_claimed"] = True
    escalating = redigest_evidence(escalating)
    escalating_review = redigest_review(rv, escalating)
    escalating_context = redigest_context(
        src,
        escalating,
        escalating_review,
        context(src, escalating, escalating_review),
    )
    assert_disposition(
        build(
            source_observeos_receipt=src,
            maintenance_monitoring_verification_evidence_packet=escalating,
            maintenance_monitoring_verification_review_certificate=escalating_review,
            maintenance_monitoring_verification_intake_context=escalating_context,
        ),
        DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    )

    print(
        "PASS: VerifyOS v0.11 future-only maintenance-monitoring observation "
        "verification intake actual-chain validation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
