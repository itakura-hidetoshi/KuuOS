#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_learnos_dukkha_preserving_future_only_maintenance_disposition_intake_v0_1 import *
from scripts.check_learnos_dukkha_preserving_future_only_maintenance_disposition_fixture_v0_1 import (
    build,
    context,
    evidence,
    redigest_context,
    redigest_evidence,
    redigest_review,
    review,
    source,
)


def main() -> int:
    supported = build()
    assert supported.status == STATUS_READY, supported.blockers
    assert supported.receipt is not None
    receipt = supported.receipt
    assert receipt["future_only_maintenance_disposition"] == DISPOSITION_SUPPORTED
    assert receipt["future_only_maintenance_disposition_recorded"] is True
    assert receipt["policy_activation_review_handoff_prepared"] is True
    assert receipt["policy_activation_review_completed"] is False
    assert receipt["policy_activation_review_debt_open"] is True
    for field in (
        "maintenance_policy_candidate_activated",
        "maintenance_monitoring_activated",
        "maintenance_action_performed",
        "persistent_world_state_changed_by_disposition",
        "world_model_revision_incremented_by_disposition",
        "current_plan_revised_by_disposition",
        "current_policy_activated_by_disposition",
        "learning_delta_activated_by_disposition",
        "tool_invocation_performed",
        "external_side_effect_performed",
        "general_execution_authority_granted",
        "world_mutation_authority_granted",
        "current_policy_activation_authority_granted",
        "maintenance_action_authority_granted_to_learnos",
        "active_now",
    ):
        assert receipt[field] is False, field
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {key: value for key, value in receipt.items() if key != RECEIPT_DIGEST_FIELD}
    )
    assert build(expected_source_verifyos_receipt_digest="wrong").status == STATUS_BLOCKED

    src = source()
    ev = evidence(src)
    rv = review(src, ev)
    cx = context(src, ev, rv)
    cases: list[tuple[dict, str]] = []

    item = deepcopy(cx)
    item["current_world_model_state_digest"] = "stale"
    cases.append(
        (
            {
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, ev, rv, item
                )
            },
            DISPOSITION_WORLD_REFRESH,
        )
    )

    item = deepcopy(cx)
    item["maintenance_disposition_intake_epoch"] = (
        item["source_monitoring_verification_epoch"]
        + item["maximum_maintenance_disposition_intake_delay"]
        + 1
    )
    cases.append(
        (
            {
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, ev, rv, item
                )
            },
            DISPOSITION_CONTEXT_REFRESH,
        )
    )

    item = deepcopy(cx)
    item["prior_maintenance_disposition_intake_session_ids"] = [
        item["maintenance_disposition_intake_session_id"]
    ]
    cases.append(
        (
            {
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, ev, rv, item
                )
            },
            DISPOSITION_REPLAY_REJECTED,
        )
    )

    item = deepcopy(rv)
    item["review_completed_epoch"] = (
        item["review_started_epoch"] + item["maximum_review_duration"] + 1
    )
    changed_review = redigest_review(item, ev)
    cases.append(
        (
            {
                "future_only_maintenance_disposition_review_certificate": changed_review,
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, ev, changed_review, cx
                ),
            },
            DISPOSITION_REVIEW_REFRESH,
        )
    )

    item = deepcopy(ev)
    item["independent_future_only_maintenance_disposition_evidence"] = False
    changed_evidence = redigest_evidence(item)
    changed_review = redigest_review(rv, changed_evidence)
    cases.append(
        (
            {
                "future_only_maintenance_disposition_evidence_packet": changed_evidence,
                "future_only_maintenance_disposition_review_certificate": changed_review,
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, changed_evidence, changed_review, cx
                ),
            },
            DISPOSITION_ADDITIONAL_EVIDENCE,
        )
    )

    review_routes = (
        ("source_receipt_correspondence_confirmed", DISPOSITION_SOURCE_REPAIR),
        (
            "monitoring_verification_record_correspondence_confirmed",
            DISPOSITION_VERIFICATION_RECORD_REPAIR,
        ),
        (
            "maintenance_disposition_handoff_correspondence_confirmed",
            DISPOSITION_HANDOFF_REPAIR,
        ),
        (
            "maintenance_policy_candidate_correspondence_confirmed",
            DISPOSITION_CANDIDATE_REPAIR,
        ),
        ("maintenance_objective_adequate", DISPOSITION_OBJECTIVE_REPAIR),
        (
            "maintenance_noop_threshold_adequate",
            DISPOSITION_NOOP_THRESHOLD_REPAIR,
        ),
        (
            "maintenance_escalation_trigger_adequate",
            DISPOSITION_ESCALATION_TRIGGER_REPAIR,
        ),
        (
            "reobservation_schedule_adequate",
            DISPOSITION_REOBSERVATION_SCHEDULE_REPAIR,
        ),
        ("uncertainty_adequate", DISPOSITION_UNCERTAINTY_REPAIR),
        ("calibration_adequate", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
    )
    for field, disposition in review_routes:
        item = deepcopy(rv)
        item[field] = False
        changed_review = redigest_review(item, ev)
        cases.append(
            (
                {
                    "future_only_maintenance_disposition_review_certificate": changed_review,
                    "future_only_maintenance_disposition_intake_context": redigest_context(
                        src, ev, changed_review, cx
                    ),
                },
                disposition,
            )
        )

    item = deepcopy(rv)
    item["protected_group_nonexternalization_supported"] = False
    changed_review = redigest_review(item, ev)
    cases.append(
        (
            {
                "future_only_maintenance_disposition_review_certificate": changed_review,
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, ev, changed_review, cx
                ),
            },
            DISPOSITION_NONEXTERNALIZATION_REVIEW,
        )
    )

    item = deepcopy(ev)
    item["current_policy_activated"] = True
    changed_evidence = redigest_evidence(item)
    changed_review = redigest_review(rv, changed_evidence)
    cases.append(
        (
            {
                "future_only_maintenance_disposition_evidence_packet": changed_evidence,
                "future_only_maintenance_disposition_review_certificate": changed_review,
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, changed_evidence, changed_review, cx
                ),
            },
            DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
        )
    )

    item = deepcopy(ev)
    item["authority_escalation_claimed"] = True
    changed_evidence = redigest_evidence(item)
    changed_review = redigest_review(rv, changed_evidence)
    cases.append(
        (
            {
                "future_only_maintenance_disposition_evidence_packet": changed_evidence,
                "future_only_maintenance_disposition_review_certificate": changed_review,
                "future_only_maintenance_disposition_intake_context": redigest_context(
                    src, changed_evidence, changed_review, cx
                ),
            },
            DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        )
    )

    assert len(cases) == 19
    seen = {DISPOSITION_SUPPORTED}
    for kwargs, expected in cases:
        result = build(**kwargs)
        assert result.status == STATUS_READY, (expected, result.blockers)
        assert result.receipt is not None
        actual = result.receipt["future_only_maintenance_disposition"]
        assert actual == expected, (expected, actual)
        assert result.receipt["future_only_maintenance_disposition_recorded"] is False
        assert result.receipt["future_only_maintenance_disposition_debt_open"] is True
        assert result.receipt["policy_activation_review_handoff_prepared"] is False
        seen.add(actual)

    assert len(seen) == 20
    print(
        "PASS: LearnOS v0.5 future-only maintenance disposition intake "
        "actual-chain validation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
