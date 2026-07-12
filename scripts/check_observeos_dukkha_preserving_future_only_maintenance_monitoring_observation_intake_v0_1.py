#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_intake_v0_1 import *
from scripts.check_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_fixture_v0_1 import (
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
    assert receipt["maintenance_monitoring_observation_disposition"] == disposition
    assert receipt["observeos_version"] == "v0.6"
    return receipt


def review_route(field, value, disposition):
    src = source()
    ev = evidence(src)
    rv = review(src, ev)
    rv[field] = value
    rv = redigest_review(rv, ev)
    cx = redigest_context(src, ev, rv, context(src, ev, rv))
    assert_disposition(
        build(
            source_learnos_receipt=src,
            maintenance_monitoring_observation_evidence_packet=ev,
            maintenance_monitoring_observation_review_certificate=rv,
            maintenance_monitoring_observation_intake_context=cx,
        ),
        disposition,
    )


def main():
    observed = set()

    supported = assert_disposition(build(), DISPOSITION_SUPPORTED)
    observed.add(DISPOSITION_SUPPORTED)
    assert supported["maintenance_monitoring_observation_state_before"] == STATE_BEFORE
    assert (
        supported["maintenance_monitoring_observation_state_after"]
        == STATE_AFTER_SUPPORTED
    )
    for field in (
        "world_fact_confirmed",
        "causal_attribution_confirmed",
        "dukkha_reduction_realized_confirmed",
        "future_only_learning_delta_recorded",
        "maintenance_monitoring_handoff_prepared",
        "maintenance_monitoring_handoff_consumed_for_observation",
        "maintenance_monitoring_observation_supported",
        "maintenance_monitoring_observation_recorded",
        "maintenance_monitoring_observation_scope_exactly_bounded",
        "maintenance_monitoring_verification_handoff_prepared",
        "verification_intake_admitted",
        "verification_receipt_required",
        "verification_debt_open",
    ):
        assert supported[field] is True
    for field in (
        "future_only_learning_delta_activated",
        "maintenance_monitoring_activated",
        "verification_completed",
        "observation_collection_performed_by_kernel",
        "maintenance_action_performed",
        "persistent_world_state_changed_by_observation",
        "world_model_revision_incremented_by_observation",
        "current_plan_revised_by_observation",
        "current_policy_activated_by_observation",
        "learning_delta_activated_by_observation",
        "tool_invocation_performed",
        "external_side_effect_performed",
        "automatic_truth_generalization",
        "automatic_causal_attribution",
        "automatic_dukkha_realization_confirmation",
        "automatic_learning_update",
        "automatic_policy_activation",
        "automatic_maintenance_action",
        "automatic_plan_completion",
        "automatic_rollback",
        "automatic_compensation",
        "generalized_benefit_claimed",
        "selection_authority_granted_to_observeos",
        "plan_revision_authority_granted_to_observeos",
        "dukkha_minimization_authority_granted_to_observeos",
        "general_execution_authority_granted",
        "execution_permission",
        "world_mutation_authority_granted",
        "current_policy_activation_authority_granted",
        "maintenance_action_authority_granted_to_observeos",
        "active_now",
    ):
        assert supported[field] is False
    assert supported[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in supported.items() if key != RECEIPT_DIGEST_FIELD}
    )

    blocked = build(expected_source_learnos_receipt_digest="wrong")
    assert blocked.status == STATUS_BLOCKED and blocked.receipt is None
    assert "source_learnos_expected_binding_mismatch" in blocked.blockers

    src = source()
    ev = evidence(src)
    rv = review(src, ev)
    cx = context(src, ev, rv)

    stale = deepcopy(cx)
    stale["current_world_model_state_digest"] = "stale"
    stale = redigest_context(src, ev, rv, stale)
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=ev,
                maintenance_monitoring_observation_review_certificate=rv,
                maintenance_monitoring_observation_intake_context=stale,
            ),
            DISPOSITION_WORLD_REFRESH,
        )["maintenance_monitoring_observation_disposition"]
    )

    late = deepcopy(cx)
    late["monitoring_observation_intake_epoch"] = (
        late["source_future_only_learning_epoch"]
        + late["maximum_monitoring_observation_intake_delay"]
        + 1
    )
    late = redigest_context(src, ev, rv, late)
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=ev,
                maintenance_monitoring_observation_review_certificate=rv,
                maintenance_monitoring_observation_intake_context=late,
            ),
            DISPOSITION_CONTEXT_REFRESH,
        )["maintenance_monitoring_observation_disposition"]
    )

    replay = deepcopy(cx)
    replay["prior_monitoring_observation_intake_session_ids"] = [
        replay["monitoring_observation_intake_session_id"]
    ]
    replay = redigest_context(src, ev, rv, replay)
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=ev,
                maintenance_monitoring_observation_review_certificate=rv,
                maintenance_monitoring_observation_intake_context=replay,
            ),
            DISPOSITION_REPLAY_REJECTED,
        )["maintenance_monitoring_observation_disposition"]
    )

    old_review = deepcopy(rv)
    old_review["review_completed_epoch"] = (
        old_review["review_started_epoch"]
        + old_review["maximum_review_duration"]
        + 1
    )
    old_review = redigest_review(old_review, ev)
    old_context = redigest_context(
        src, ev, old_review, context(src, ev, old_review)
    )
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=ev,
                maintenance_monitoring_observation_review_certificate=old_review,
                maintenance_monitoring_observation_intake_context=old_context,
            ),
            DISPOSITION_REVIEW_REFRESH,
        )["maintenance_monitoring_observation_disposition"]
    )

    insufficient = deepcopy(ev)
    insufficient["independent_maintenance_monitoring_evidence"] = False
    insufficient = redigest_evidence(insufficient)
    insufficient_review = redigest_review(rv, insufficient)
    insufficient_context = redigest_context(
        src,
        insufficient,
        insufficient_review,
        context(src, insufficient, insufficient_review),
    )
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=insufficient,
                maintenance_monitoring_observation_review_certificate=insufficient_review,
                maintenance_monitoring_observation_intake_context=insufficient_context,
            ),
            DISPOSITION_ADDITIONAL_EVIDENCE,
        )["maintenance_monitoring_observation_disposition"]
    )

    routes = (
        ("source_receipt_correspondence_confirmed", DISPOSITION_SOURCE_REPAIR),
        (
            "future_only_learning_delta_correspondence_confirmed",
            DISPOSITION_DELTA_REPAIR,
        ),
        (
            "maintenance_handoff_correspondence_confirmed",
            DISPOSITION_HANDOFF_REPAIR,
        ),
        ("maintenance_window_adequate", DISPOSITION_MAINTENANCE_WINDOW_REPAIR),
        ("durability_observation_adequate", DISPOSITION_DURABILITY_REPAIR),
        ("adverse_effect_observation_adequate", DISPOSITION_ADVERSE_REPAIR),
        (
            "distributional_observation_adequate",
            DISPOSITION_DISTRIBUTIONAL_REPAIR,
        ),
        (
            "reobservation_trigger_adequate",
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
        review_route(field, False, disposition)
        observed.add(disposition)

    mutating = deepcopy(ev)
    mutating["current_policy_activated"] = True
    mutating = redigest_evidence(mutating)
    mutating_review = redigest_review(rv, mutating)
    mutating_context = redigest_context(
        src,
        mutating,
        mutating_review,
        context(src, mutating, mutating_review),
    )
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=mutating,
                maintenance_monitoring_observation_review_certificate=mutating_review,
                maintenance_monitoring_observation_intake_context=mutating_context,
            ),
            DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
        )["maintenance_monitoring_observation_disposition"]
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
    observed.add(
        assert_disposition(
            build(
                source_learnos_receipt=src,
                maintenance_monitoring_observation_evidence_packet=escalating,
                maintenance_monitoring_observation_review_certificate=escalating_review,
                maintenance_monitoring_observation_intake_context=escalating_context,
            ),
            DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        )["maintenance_monitoring_observation_disposition"]
    )

    expected = {
        DISPOSITION_SUPPORTED,
        DISPOSITION_WORLD_REFRESH,
        DISPOSITION_CONTEXT_REFRESH,
        DISPOSITION_REVIEW_REFRESH,
        DISPOSITION_ADDITIONAL_EVIDENCE,
        DISPOSITION_SOURCE_REPAIR,
        DISPOSITION_DELTA_REPAIR,
        DISPOSITION_HANDOFF_REPAIR,
        DISPOSITION_MAINTENANCE_WINDOW_REPAIR,
        DISPOSITION_DURABILITY_REPAIR,
        DISPOSITION_ADVERSE_REPAIR,
        DISPOSITION_DISTRIBUTIONAL_REPAIR,
        DISPOSITION_REOBSERVATION_TRIGGER_REPAIR,
        DISPOSITION_UNCERTAINTY_REPAIR,
        DISPOSITION_CALIBRATION_REPAIR,
        DISPOSITION_PROVENANCE_REPAIR,
        DISPOSITION_NONEXTERNALIZATION_REVIEW,
        DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
        DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        DISPOSITION_REPLAY_REJECTED,
    }
    assert observed == expected
    print(
        "PASS: ObserveOS v0.6 future-only maintenance-monitoring "
        "observation intake actual-chain validation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
