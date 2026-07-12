#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD as SOURCE_CONTEXT_DIGEST_FIELD,
    DISPOSITION_SUPPORTED as SOURCE_DISPOSITION_SUPPORTED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED as SOURCE_STATE_AFTER_SUPPORTED,
    canonical_digest,
    compute_future_only_learning_evidence_packet_digest,
    compute_future_only_learning_review_certificate_digest,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

RECEIPT_DIGEST_FIELD = (
    "observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_"
    "intake_receipt_digest"
)
EVIDENCE_DIGEST_FIELD = "maintenance_monitoring_observation_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "maintenance_monitoring_observation_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "maintenance_monitoring_observation_intake_context_digest"

STATE_BEFORE = SOURCE_STATE_AFTER_SUPPORTED
STATE_AFTER_SUPPORTED = (
    STATE_BEFORE + "_maintenance_monitoring_observation_recorded"
)

DISPOSITION_SUPPORTED = "maintenance_monitoring_observation_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "monitoring_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "monitoring_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = (
    "additional_maintenance_monitoring_evidence_required"
)
DISPOSITION_SOURCE_REPAIR = "source_receipt_correspondence_repair_required"
DISPOSITION_DELTA_REPAIR = (
    "future_only_learning_delta_correspondence_repair_required"
)
DISPOSITION_HANDOFF_REPAIR = (
    "maintenance_handoff_correspondence_repair_required"
)
DISPOSITION_MAINTENANCE_WINDOW_REPAIR = "maintenance_window_repair_required"
DISPOSITION_DURABILITY_REPAIR = "durability_observation_repair_required"
DISPOSITION_ADVERSE_REPAIR = "adverse_effect_observation_repair_required"
DISPOSITION_DISTRIBUTIONAL_REPAIR = (
    "distributional_observation_repair_required"
)
DISPOSITION_REOBSERVATION_TRIGGER_REPAIR = (
    "reobservation_trigger_repair_required"
)
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = (
    "current_state_mutation_rejected"
)
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

EVIDENCE_FIELDS = {
    "source_learnos_receipt_digest",
    "source_future_only_learning_evidence_packet_digest",
    "source_future_only_learning_review_certificate_digest",
    "source_future_only_learning_record_digest",
    "source_future_only_learning_debt_consumption_record_digest",
    "source_future_only_learning_delta_binding_digest",
    "source_maintenance_monitoring_handoff_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "future_only_learning_delta_digest",
    "maintenance_policy_candidate_digest",
    "maintenance_window_digest",
    "durability_monitoring_specification_digest",
    "adverse_effect_monitoring_specification_digest",
    "distributional_monitoring_specification_digest",
    "reobservation_trigger_digest",
    "retention_window_digest",
    "observation_window_digest",
    "baseline_observation_digest",
    "durability_observation_digest",
    "adverse_effect_observation_digest",
    "distributional_observation_digest",
    "raw_artifact_digests",
    "uncertainty_digest",
    "calibration_digest",
    "provenance_chain_digests",
    "tamper_evidence_digest",
    "protected_group_observation_impact_digest",
    "future_subject_observation_impact_digest",
    "collector_id",
    "evidence_source_id",
    "collection_started_epoch",
    "collection_completed_epoch",
    "maximum_collection_duration",
    "independent_maintenance_monitoring_evidence",
    "exactly_one_monitoring_observation_collection",
    "maintenance_action_performed",
    "current_world_mutation_performed",
    "current_plan_revised",
    "current_policy_activated",
    "learning_delta_activated",
    "generalized_benefit_claimed",
    "authority_escalation_claimed",
    EVIDENCE_DIGEST_FIELD,
}

REVIEW_FIELDS = {
    "source_learnos_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    "source_future_only_learning_delta_binding_digest",
    "source_maintenance_monitoring_handoff_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "future_only_learning_delta_digest",
    "maintenance_policy_candidate_digest",
    "reviewer_id",
    "verification_method_digest",
    "verification_evidence_digest",
    "review_started_epoch",
    "review_completed_epoch",
    "maximum_review_duration",
    "source_receipt_correspondence_confirmed",
    "future_only_learning_delta_correspondence_confirmed",
    "maintenance_handoff_correspondence_confirmed",
    "maintenance_window_adequate",
    "durability_observation_adequate",
    "adverse_effect_observation_adequate",
    "distributional_observation_adequate",
    "reobservation_trigger_adequate",
    "uncertainty_adequate",
    "calibration_adequate",
    "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "no_current_state_mutation",
    "no_maintenance_action_performed",
    "no_authority_escalation",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_learnos_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_future_only_learning_delta_digest",
    "current_maintenance_policy_candidate_digest",
    "source_future_only_learning_epoch",
    "monitoring_observation_intake_epoch",
    "maximum_monitoring_observation_intake_delay",
    "monitoring_observation_intake_session_id",
    "monitoring_observation_intake_nonce_digest",
    "prior_monitoring_observation_intake_session_ids",
    "prior_monitoring_observation_evidence_packet_digests",
    "prior_monitoring_observation_review_certificate_digests",
    "prior_monitoring_observation_intake_nonce_digests",
    "prior_monitoring_observation_source_receipt_digests",
    "requested_monitoring_observation_operation_digest",
    "exact_monitoring_observation_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass
class ObserveOSFutureOnlyMaintenanceMonitoringObservationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    return value == sorted(value) and len(value) == len(set(value)), list(value)


def _exact(
    actual: Mapping[str, Any],
    expected: Mapping[str, Any],
    prefix: str,
    blockers: list[str],
) -> None:
    for field, expected_value in expected.items():
        if actual.get(field) != expected_value:
            blockers.append(f"{prefix}_{field}_mismatch")


def compute_maintenance_monitoring_observation_evidence_packet_digest(
    packet: Mapping[str, Any],
) -> str:
    return _digest_without(packet, EVIDENCE_DIGEST_FIELD)


def compute_maintenance_monitoring_observation_review_certificate_digest(
    review: Mapping[str, Any],
) -> str:
    return _digest_without(review, REVIEW_DIGEST_FIELD)


def compute_maintenance_monitoring_observation_intake_context_digest(
    context: Mapping[str, Any],
) -> str:
    return _digest_without(context, CONTEXT_DIGEST_FIELD)


def compute_requested_monitoring_observation_operation_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    learning_evidence = _map(source.get("future_only_learning_evidence_packet"))
    return canonical_digest(
        {
            "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
            "source_future_only_learning_delta_binding_digest": source.get(
                "future_only_learning_delta_binding_digest"
            ),
            "source_maintenance_monitoring_handoff_envelope_digest": source.get(
                "maintenance_monitoring_handoff_envelope_digest"
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_candidate_fact_digest": learning_evidence.get(
                "world_candidate_fact_digest"
            ),
            "world_candidate_relation_digest": learning_evidence.get(
                "world_candidate_relation_digest"
            ),
            "future_only_learning_delta_digest": learning_evidence.get(
                "future_only_learning_delta_digest"
            ),
            "state_before": STATE_BEFORE,
            "state_after": STATE_AFTER_SUPPORTED,
        }
    )


def compute_exact_monitoring_observation_cycle_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "monitoring_observation_intake_session_id": context.get(
                "monitoring_observation_intake_session_id"
            ),
            "monitoring_observation_intake_nonce_digest": context.get(
                "monitoring_observation_intake_nonce_digest"
            ),
            "monitoring_observation_intake_epoch": context.get(
                "monitoring_observation_intake_epoch"
            ),
            "current_world_model_revision": context.get(
                "current_world_model_revision"
            ),
            "requested_monitoring_observation_operation_digest": context.get(
                "requested_monitoring_observation_operation_digest"
            ),
        }
    )


def compute_future_only_maintenance_monitoring_observation_bundle_digest(
    **fields: Any,
) -> str:
    return canonical_digest(fields)


def _verify_source(
    source: dict,
    expected_digest: str,
    blockers: list[str],
) -> tuple[str, dict, dict, dict, dict, int, list[str], list[str]]:
    if not source:
        blockers.append("source_learnos_receipt_missing")
        return "", {}, {}, {}, {}, 0, [], []

    _exact(
        source,
        {
            "kernel": (
                "LearnOS Dukkha-Preserving Future-Only Learning Maintenance "
                "Disposition Intake Kernel"
            ),
            "kernel_version": "v0.1",
            "learnos_version": "v0.4",
            "status": (
                "LEARNOS_DUKKHA_PRESERVING_FUTURE_ONLY_LEARNING_"
                "MAINTENANCE_DISPOSITION_ROUTED"
            ),
            "future_only_learning_disposition": SOURCE_DISPOSITION_SUPPORTED,
            "future_only_learning_state_after": STATE_BEFORE,
            "world_fact_confirmed": True,
            "causal_attribution_confirmed": True,
            "dukkha_reduction_realized_confirmed": True,
            "future_only_learning_supported": True,
            "future_only_learning_debt_consumed": True,
            "future_only_learning_debt_open": False,
            "future_only_learning_delta_recorded": True,
            "future_only_learning_delta_scope_exactly_bounded": True,
            "future_only_learning_delta_activated": False,
            "maintenance_monitoring_handoff_prepared": True,
            "maintenance_monitoring_activated": False,
            "persistent_world_state_changed_by_learning": False,
            "world_model_revision_incremented_by_learning": False,
            "current_plan_revised_by_learning": False,
            "current_policy_activated_by_learning": False,
            "tool_invocation_performed": False,
            "external_side_effect_performed": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        },
        "source",
        blockers,
    )

    digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_learnos_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD):
        blockers.append("source_learnos_receipt_digest_mismatch")
    if digest != expected_digest:
        blockers.append("source_learnos_expected_binding_mismatch")

    learning_evidence = _map(source.get("future_only_learning_evidence_packet"))
    learning_review = _map(source.get("future_only_learning_review_certificate"))
    learning_record = _map(source.get("future_only_learning_record"))
    learning_debt = _map(source.get("future_only_learning_debt_consumption_record"))
    delta_binding = _map(source.get("future_only_learning_delta_binding"))
    monitoring_handoff = _map(source.get("maintenance_monitoring_handoff_envelope"))

    if (
        source.get(SOURCE_EVIDENCE_DIGEST_FIELD)
        != compute_future_only_learning_evidence_packet_digest(learning_evidence)
    ):
        blockers.append("source_future_only_learning_evidence_digest_mismatch")
    if (
        source.get(SOURCE_REVIEW_DIGEST_FIELD)
        != compute_future_only_learning_review_certificate_digest(learning_review)
    ):
        blockers.append("source_future_only_learning_review_digest_mismatch")

    for name, item, digest_field in (
        (
            "future_only_learning_record",
            learning_record,
            "future_only_learning_record_digest",
        ),
        (
            "future_only_learning_debt_consumption_record",
            learning_debt,
            "future_only_learning_debt_consumption_record_digest",
        ),
        (
            "future_only_learning_delta_binding",
            delta_binding,
            "future_only_learning_delta_binding_digest",
        ),
        (
            "maintenance_monitoring_handoff_envelope",
            monitoring_handoff,
            "maintenance_monitoring_handoff_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_{name}_invalid")
        elif source.get(digest_field) != canonical_digest(item):
            blockers.append(f"source_{digest_field}_mismatch")

    _exact(
        learning_record,
        {
            "evidence": source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
            "review": source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "fact": learning_evidence.get("world_candidate_fact_digest"),
            "relation": learning_evidence.get("world_candidate_relation_digest"),
            "revision": learning_evidence.get("resulting_world_revision"),
            "target": learning_evidence.get("learning_target_digest"),
            "delta": learning_evidence.get("future_only_learning_delta_digest"),
            "maintenance": learning_evidence.get(
                "maintenance_policy_candidate_digest"
            ),
            "disposition": SOURCE_DISPOSITION_SUPPORTED,
            "state_after": STATE_BEFORE,
        },
        "source_future_only_learning_record",
        blockers,
    )
    _exact(
        learning_debt,
        {
            "record": source.get("future_only_learning_record_digest"),
            "consumed": True,
            "double": False,
        },
        "source_future_only_learning_debt",
        blockers,
    )
    _exact(
        delta_binding,
        {
            "record": source.get("future_only_learning_record_digest"),
            "debt": source.get(
                "future_only_learning_debt_consumption_record_digest"
            ),
            "target": learning_evidence.get("learning_target_digest"),
            "delta": learning_evidence.get("future_only_learning_delta_digest"),
            "maintenance": learning_evidence.get(
                "maintenance_policy_candidate_digest"
            ),
            "future_only": True,
            "active_now": False,
            "world_changed": False,
            "plan_changed": False,
            "policy_activated": False,
        },
        "source_future_only_learning_delta",
        blockers,
    )
    _exact(
        monitoring_handoff,
        {
            "delta_binding": source.get(
                "future_only_learning_delta_binding_digest"
            ),
            "maintenance_window": learning_evidence.get(
                "maintenance_window_digest"
            ),
            "durability": learning_evidence.get(
                "durability_monitoring_specification_digest"
            ),
            "adverse": learning_evidence.get(
                "adverse_effect_monitoring_specification_digest"
            ),
            "distributional": learning_evidence.get(
                "distributional_monitoring_specification_digest"
            ),
            "reobservation": learning_evidence.get(
                "reobservation_trigger_digest"
            ),
            "retention": learning_evidence.get("retention_window_digest"),
            "state": "prepared_not_activated",
            "automatic_action": False,
        },
        "source_maintenance_monitoring_handoff",
        blockers,
    )

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")

    epoch = learning_record.get("epoch", 0)
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        blockers.append("source_future_only_learning_epoch_invalid")
        epoch = 0

    return (
        digest,
        learning_evidence,
        learning_record,
        delta_binding,
        monitoring_handoff,
        epoch,
        lineage,
        responsibility,
    )


def _verify_evidence(
    evidence: dict,
    expected_digest: str,
    source: dict,
    learning_evidence: dict,
    delta_binding: dict,
    monitoring_handoff: dict,
    blockers: list[str],
) -> tuple[str, bool, list[str], list[str]]:
    if not evidence:
        blockers.append("maintenance_monitoring_observation_evidence_missing")
        return "", False, [], []
    if set(evidence) != EVIDENCE_FIELDS:
        blockers.append(
            "maintenance_monitoring_observation_evidence_schema_invalid"
        )

    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append(
            "maintenance_monitoring_observation_evidence_digest_missing"
        )
    elif digest != compute_maintenance_monitoring_observation_evidence_packet_digest(
        evidence
    ):
        blockers.append(
            "maintenance_monitoring_observation_evidence_digest_mismatch"
        )
    if digest != expected_digest:
        blockers.append(
            "maintenance_monitoring_observation_evidence_expected_binding_mismatch"
        )

    _exact(
        evidence,
        {
            "source_learnos_receipt_digest": source.get(
                SOURCE_RECEIPT_DIGEST_FIELD
            ),
            "source_future_only_learning_evidence_packet_digest": source.get(
                SOURCE_EVIDENCE_DIGEST_FIELD
            ),
            "source_future_only_learning_review_certificate_digest": source.get(
                SOURCE_REVIEW_DIGEST_FIELD
            ),
            "source_future_only_learning_record_digest": source.get(
                "future_only_learning_record_digest"
            ),
            "source_future_only_learning_debt_consumption_record_digest": source.get(
                "future_only_learning_debt_consumption_record_digest"
            ),
            "source_future_only_learning_delta_binding_digest": source.get(
                "future_only_learning_delta_binding_digest"
            ),
            "source_maintenance_monitoring_handoff_envelope_digest": source.get(
                "maintenance_monitoring_handoff_envelope_digest"
            ),
            "world_candidate_fact_digest": learning_evidence.get(
                "world_candidate_fact_digest"
            ),
            "world_candidate_relation_digest": learning_evidence.get(
                "world_candidate_relation_digest"
            ),
            "resulting_world_state_digest": learning_evidence.get(
                "resulting_world_state_digest"
            ),
            "resulting_world_revision": learning_evidence.get(
                "resulting_world_revision"
            ),
            "future_only_learning_delta_digest": delta_binding.get("delta"),
            "maintenance_policy_candidate_digest": delta_binding.get(
                "maintenance"
            ),
            "maintenance_window_digest": monitoring_handoff.get(
                "maintenance_window"
            ),
            "durability_monitoring_specification_digest": monitoring_handoff.get(
                "durability"
            ),
            "adverse_effect_monitoring_specification_digest": monitoring_handoff.get(
                "adverse"
            ),
            "distributional_monitoring_specification_digest": monitoring_handoff.get(
                "distributional"
            ),
            "reobservation_trigger_digest": monitoring_handoff.get(
                "reobservation"
            ),
            "retention_window_digest": monitoring_handoff.get("retention"),
        },
        "maintenance_monitoring_observation_evidence",
        blockers,
    )

    for field in (
        "observation_window_digest",
        "baseline_observation_digest",
        "durability_observation_digest",
        "adverse_effect_observation_digest",
        "distributional_observation_digest",
        "uncertainty_digest",
        "calibration_digest",
        "tamper_evidence_digest",
        "protected_group_observation_impact_digest",
        "future_subject_observation_impact_digest",
        "collector_id",
        "evidence_source_id",
    ):
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            blockers.append(
                f"maintenance_monitoring_observation_evidence_{field}_invalid"
            )

    raw_ok, raw_artifacts = _strings(evidence.get("raw_artifact_digests"))
    provenance_ok, provenance = _strings(
        evidence.get("provenance_chain_digests")
    )
    if not raw_ok:
        blockers.append(
            "maintenance_monitoring_observation_raw_artifacts_invalid"
        )
    if not provenance_ok:
        blockers.append(
            "maintenance_monitoring_observation_provenance_invalid"
        )

    source_review = _map(source.get("future_only_learning_review_certificate"))
    source_evidence = _map(source.get("future_only_learning_evidence_packet"))
    if evidence.get("collector_id") in {
        source_review.get("reviewer_id"),
        source_evidence.get("evidence_collector_id"),
    }:
        blockers.append(
            "maintenance_monitoring_observer_not_independent_from_learning"
        )
    if evidence.get("evidence_source_id") == source_evidence.get(
        "evidence_source_id"
    ):
        blockers.append(
            "maintenance_monitoring_evidence_source_not_independent_from_learning"
        )

    start = evidence.get("collection_started_epoch")
    end = evidence.get("collection_completed_epoch")
    maximum = evidence.get("maximum_collection_duration")
    duration_current = (
        all(
            isinstance(item, int) and not isinstance(item, bool)
            for item in (start, end, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= end - start <= maximum
    )

    return digest, duration_current, raw_artifacts, provenance


def _verify_review(
    review: dict,
    expected_digest: str,
    source: dict,
    evidence: dict,
    blockers: list[str],
) -> tuple[str, bool]:
    if not review:
        blockers.append("maintenance_monitoring_observation_review_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("maintenance_monitoring_observation_review_schema_invalid")

    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append(
            "maintenance_monitoring_observation_review_digest_missing"
        )
    elif digest != compute_maintenance_monitoring_observation_review_certificate_digest(
        review
    ):
        blockers.append(
            "maintenance_monitoring_observation_review_digest_mismatch"
        )
    if digest != expected_digest:
        blockers.append(
            "maintenance_monitoring_observation_review_expected_binding_mismatch"
        )

    _exact(
        review,
        {
            "source_learnos_receipt_digest": source.get(
                SOURCE_RECEIPT_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            "source_future_only_learning_delta_binding_digest": source.get(
                "future_only_learning_delta_binding_digest"
            ),
            "source_maintenance_monitoring_handoff_envelope_digest": source.get(
                "maintenance_monitoring_handoff_envelope_digest"
            ),
            "world_candidate_fact_digest": evidence.get(
                "world_candidate_fact_digest"
            ),
            "world_candidate_relation_digest": evidence.get(
                "world_candidate_relation_digest"
            ),
            "resulting_world_state_digest": evidence.get(
                "resulting_world_state_digest"
            ),
            "resulting_world_revision": evidence.get("resulting_world_revision"),
            "future_only_learning_delta_digest": evidence.get(
                "future_only_learning_delta_digest"
            ),
            "maintenance_policy_candidate_digest": evidence.get(
                "maintenance_policy_candidate_digest"
            ),
        },
        "maintenance_monitoring_observation_review",
        blockers,
    )

    for field in (
        "reviewer_id",
        "verification_method_digest",
        "verification_evidence_digest",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(
                f"maintenance_monitoring_observation_review_{field}_invalid"
            )

    start = review.get("review_started_epoch")
    end = review.get("review_completed_epoch")
    maximum = review.get("maximum_review_duration")
    duration_current = (
        all(
            isinstance(item, int) and not isinstance(item, bool)
            for item in (start, end, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= end - start <= maximum
    )
    return digest, duration_current


def _verify_context(
    context: dict,
    expected_digest: str,
    source: dict,
    evidence: dict,
    review: dict,
    learning_evidence: dict,
    source_epoch: int,
    blockers: list[str],
) -> tuple[str, tuple[bool, ...]]:
    if not context:
        blockers.append("maintenance_monitoring_observation_context_missing")
        return "", (False,) * 7
    if set(context) != CONTEXT_FIELDS:
        blockers.append("maintenance_monitoring_observation_context_schema_invalid")

    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest:
        blockers.append(
            "maintenance_monitoring_observation_context_digest_missing"
        )
    elif digest != compute_maintenance_monitoring_observation_intake_context_digest(
        context
    ):
        blockers.append(
            "maintenance_monitoring_observation_context_digest_mismatch"
        )
    if digest != expected_digest:
        blockers.append(
            "maintenance_monitoring_observation_context_expected_binding_mismatch"
        )

    _exact(
        context,
        {
            "source_learnos_receipt_digest": source.get(
                SOURCE_RECEIPT_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        },
        "maintenance_monitoring_observation_context",
        blockers,
    )

    if context.get(
        "requested_monitoring_observation_operation_digest"
    ) != compute_requested_monitoring_observation_operation_digest(
        source, evidence, review
    ):
        blockers.append(
            "maintenance_monitoring_observation_context_operation_digest_mismatch"
        )
    if context.get(
        "exact_monitoring_observation_cycle_digest"
    ) != compute_exact_monitoring_observation_cycle_digest(
        source, evidence, review, context
    ):
        blockers.append(
            "maintenance_monitoring_observation_context_cycle_digest_mismatch"
        )

    world_current = (
        context.get("current_world_model_state_digest")
        == learning_evidence.get("resulting_world_state_digest")
        and context.get("current_world_model_revision")
        == learning_evidence.get("resulting_world_revision")
        and context.get("current_future_only_learning_delta_digest")
        == learning_evidence.get("future_only_learning_delta_digest")
        and context.get("current_maintenance_policy_candidate_digest")
        == learning_evidence.get("maintenance_policy_candidate_digest")
    )

    intake_epoch = context.get("monitoring_observation_intake_epoch")
    maximum_delay = context.get("maximum_monitoring_observation_intake_delay")
    delay_current = (
        all(
            isinstance(item, int) and not isinstance(item, bool)
            for item in (source_epoch, intake_epoch, maximum_delay)
        )
        and 1 <= maximum_delay <= 64
        and 0 <= intake_epoch - source_epoch <= maximum_delay
    )

    collections: list[list[str]] = []
    for field in (
        "prior_monitoring_observation_intake_session_ids",
        "prior_monitoring_observation_evidence_packet_digests",
        "prior_monitoring_observation_review_certificate_digests",
        "prior_monitoring_observation_intake_nonce_digests",
        "prior_monitoring_observation_source_receipt_digests",
    ):
        ok, values = _strings(context.get(field), True)
        if not ok:
            blockers.append(
                f"maintenance_monitoring_observation_context_{field}_invalid"
            )
        collections.append(values)

    sessions, evidence_seen, reviews_seen, nonces, sources = collections
    return digest, (
        world_current,
        delay_current,
        context.get("monitoring_observation_intake_session_id") not in sessions,
        evidence.get(EVIDENCE_DIGEST_FIELD) not in evidence_seen,
        review.get(REVIEW_DIGEST_FIELD) not in reviews_seen,
        context.get("monitoring_observation_intake_nonce_digest") not in nonces,
        source.get(SOURCE_RECEIPT_DIGEST_FIELD) not in sources,
    )


def _route(
    evidence: dict,
    review: dict,
    checks: tuple[bool, ...],
    evidence_duration_current: bool,
    review_duration_current: bool,
) -> str:
    world_current, delay_current, *replay_fresh = checks
    if not world_current:
        return DISPOSITION_WORLD_REFRESH
    if not delay_current:
        return DISPOSITION_CONTEXT_REFRESH
    if not all(replay_fresh):
        return DISPOSITION_REPLAY_REJECTED
    if not review_duration_current:
        return DISPOSITION_REVIEW_REFRESH
    if (
        not evidence_duration_current
        or evidence.get("independent_maintenance_monitoring_evidence") is not True
        or evidence.get(
            "exactly_one_monitoring_observation_collection"
        )
        is not True
    ):
        return DISPOSITION_ADDITIONAL_EVIDENCE

    review_routes = (
        (
            "source_receipt_correspondence_confirmed",
            DISPOSITION_SOURCE_REPAIR,
        ),
        (
            "future_only_learning_delta_correspondence_confirmed",
            DISPOSITION_DELTA_REPAIR,
        ),
        (
            "maintenance_handoff_correspondence_confirmed",
            DISPOSITION_HANDOFF_REPAIR,
        ),
        (
            "maintenance_window_adequate",
            DISPOSITION_MAINTENANCE_WINDOW_REPAIR,
        ),
        (
            "durability_observation_adequate",
            DISPOSITION_DURABILITY_REPAIR,
        ),
        (
            "adverse_effect_observation_adequate",
            DISPOSITION_ADVERSE_REPAIR,
        ),
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
        (
            "provenance_continuity_preserved",
            DISPOSITION_PROVENANCE_REPAIR,
        ),
    )
    for field, disposition in review_routes:
        if review.get(field) is not True:
            return disposition

    if (
        review.get("protected_group_nonexternalization_supported") is not True
        or review.get("future_nonexternalization_supported") is not True
    ):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW

    if (
        evidence.get("maintenance_action_performed")
        or evidence.get("current_world_mutation_performed")
        or evidence.get("current_plan_revised")
        or evidence.get("current_policy_activated")
        or evidence.get("learning_delta_activated")
        or review.get("no_current_state_mutation") is not True
        or review.get("no_maintenance_action_performed") is not True
    ):
        return DISPOSITION_CURRENT_STATE_MUTATION_REJECTED

    if (
        evidence.get("generalized_benefit_claimed")
        or evidence.get("authority_escalation_claimed")
        or review.get("no_authority_escalation") is not True
    ):
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED

    return DISPOSITION_SUPPORTED


def build_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_intake(
    *,
    source_learnos_receipt: Mapping[str, Any],
    expected_source_learnos_receipt_digest: str,
    maintenance_monitoring_observation_evidence_packet: Mapping[str, Any],
    expected_maintenance_monitoring_observation_evidence_packet_digest: str,
    maintenance_monitoring_observation_review_certificate: Mapping[str, Any],
    expected_maintenance_monitoring_observation_review_certificate_digest: str,
    maintenance_monitoring_observation_intake_context: Mapping[str, Any],
    expected_maintenance_monitoring_observation_intake_context_digest: str,
    maintenance_monitoring_observation_policy_digest: str,
    observeos_monitoring_responsibility_digest: str,
    maintenance_monitoring_observation_request_id: str,
    future_only_maintenance_monitoring_observation_bundle_digest: str,
) -> ObserveOSFutureOnlyMaintenanceMonitoringObservationResult:
    source = _map(source_learnos_receipt)
    evidence = _map(maintenance_monitoring_observation_evidence_packet)
    review = _map(maintenance_monitoring_observation_review_certificate)
    context = _map(maintenance_monitoring_observation_intake_context)
    blockers: list[str] = []

    required_strings = {
        "expected_source_learnos_receipt_digest": (
            expected_source_learnos_receipt_digest
        ),
        "expected_maintenance_monitoring_observation_evidence_packet_digest": (
            expected_maintenance_monitoring_observation_evidence_packet_digest
        ),
        "expected_maintenance_monitoring_observation_review_certificate_digest": (
            expected_maintenance_monitoring_observation_review_certificate_digest
        ),
        "expected_maintenance_monitoring_observation_intake_context_digest": (
            expected_maintenance_monitoring_observation_intake_context_digest
        ),
        "maintenance_monitoring_observation_policy_digest": (
            maintenance_monitoring_observation_policy_digest
        ),
        "observeos_monitoring_responsibility_digest": (
            observeos_monitoring_responsibility_digest
        ),
        "maintenance_monitoring_observation_request_id": (
            maintenance_monitoring_observation_request_id
        ),
        "future_only_maintenance_monitoring_observation_bundle_digest": (
            future_only_maintenance_monitoring_observation_bundle_digest
        ),
    }
    for name, value in required_strings.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    (
        source_digest,
        learning_evidence,
        learning_record,
        delta_binding,
        monitoring_handoff,
        source_epoch,
        source_lineage,
        source_responsibility,
    ) = _verify_source(
        source, expected_source_learnos_receipt_digest, blockers
    )

    (
        evidence_digest,
        evidence_duration_current,
        raw_artifacts,
        provenance,
    ) = _verify_evidence(
        evidence,
        expected_maintenance_monitoring_observation_evidence_packet_digest,
        source,
        learning_evidence,
        delta_binding,
        monitoring_handoff,
        blockers,
    )

    review_digest, review_duration_current = _verify_review(
        review,
        expected_maintenance_monitoring_observation_review_certificate_digest,
        source,
        evidence,
        blockers,
    )

    context_digest, checks = _verify_context(
        context,
        expected_maintenance_monitoring_observation_intake_context_digest,
        source,
        evidence,
        review,
        learning_evidence,
        source_epoch,
        blockers,
    )

    if not blockers:
        expected_bundle = (
            compute_future_only_maintenance_monitoring_observation_bundle_digest(
                source_learnos_receipt_digest=source_digest,
                expected_source_learnos_receipt_digest=(
                    expected_source_learnos_receipt_digest
                ),
                source_future_only_learning_delta_binding_digest=source.get(
                    "future_only_learning_delta_binding_digest"
                ),
                source_maintenance_monitoring_handoff_envelope_digest=source.get(
                    "maintenance_monitoring_handoff_envelope_digest"
                ),
                maintenance_monitoring_observation_evidence_packet_digest=(
                    evidence_digest
                ),
                expected_maintenance_monitoring_observation_evidence_packet_digest=(
                    expected_maintenance_monitoring_observation_evidence_packet_digest
                ),
                maintenance_monitoring_observation_review_certificate_digest=(
                    review_digest
                ),
                expected_maintenance_monitoring_observation_review_certificate_digest=(
                    expected_maintenance_monitoring_observation_review_certificate_digest
                ),
                maintenance_monitoring_observation_intake_context_digest=(
                    context_digest
                ),
                expected_maintenance_monitoring_observation_intake_context_digest=(
                    expected_maintenance_monitoring_observation_intake_context_digest
                ),
                requested_monitoring_observation_operation_digest=context.get(
                    "requested_monitoring_observation_operation_digest"
                ),
                exact_monitoring_observation_cycle_digest=context.get(
                    "exact_monitoring_observation_cycle_digest"
                ),
                maintenance_monitoring_observation_policy_digest=(
                    maintenance_monitoring_observation_policy_digest
                ),
                observeos_monitoring_responsibility_digest=(
                    observeos_monitoring_responsibility_digest
                ),
                maintenance_monitoring_observation_request_id=(
                    maintenance_monitoring_observation_request_id
                ),
            )
        )
        if (
            future_only_maintenance_monitoring_observation_bundle_digest
            != expected_bundle
        ):
            blockers.append(
                "future_only_maintenance_monitoring_observation_bundle_digest_mismatch"
            )

    if blockers:
        return ObserveOSFutureOnlyMaintenanceMonitoringObservationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route(
        evidence,
        review,
        checks,
        evidence_duration_current,
        review_duration_current,
    )
    supported = disposition == DISPOSITION_SUPPORTED
    state_after = STATE_AFTER_SUPPORTED if supported else STATE_BEFORE

    observation_record = {
        "source_learnos_receipt_digest": source_digest,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "source_future_only_learning_delta_binding_digest": source[
            "future_only_learning_delta_binding_digest"
        ],
        "source_maintenance_monitoring_handoff_envelope_digest": source[
            "maintenance_monitoring_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence[
            "world_candidate_relation_digest"
        ],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "future_only_learning_delta_digest": evidence[
            "future_only_learning_delta_digest"
        ],
        "maintenance_policy_candidate_digest": evidence[
            "maintenance_policy_candidate_digest"
        ],
        "baseline_observation_digest": evidence[
            "baseline_observation_digest"
        ],
        "durability_observation_digest": evidence[
            "durability_observation_digest"
        ],
        "adverse_effect_observation_digest": evidence[
            "adverse_effect_observation_digest"
        ],
        "distributional_observation_digest": evidence[
            "distributional_observation_digest"
        ],
        "monitoring_observation_intake_session_id": context[
            "monitoring_observation_intake_session_id"
        ],
        "monitoring_observation_intake_nonce_digest": context[
            "monitoring_observation_intake_nonce_digest"
        ],
        "monitoring_observation_intake_epoch": context[
            "monitoring_observation_intake_epoch"
        ],
        "disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
    }
    observation_record_digest = canonical_digest(observation_record)

    debt_record = {
        "source_learnos_receipt_digest": source_digest,
        "observation_record_digest": observation_record_digest,
        "observation_debt_consumed": supported,
        "source_maintenance_monitoring_handoff_consumed": supported,
        "double_observation_performed": False,
    }
    debt_digest = canonical_digest(debt_record)

    verification_handoff = None
    verification_handoff_digest = ""
    if supported:
        verification_handoff = {
            "source_learnos_receipt_digest": source_digest,
            EVIDENCE_DIGEST_FIELD: evidence_digest,
            REVIEW_DIGEST_FIELD: review_digest,
            "observation_record_digest": observation_record_digest,
            "source_future_only_learning_delta_binding_digest": source[
                "future_only_learning_delta_binding_digest"
            ],
            "source_maintenance_monitoring_handoff_envelope_digest": source[
                "maintenance_monitoring_handoff_envelope_digest"
            ],
            "world_candidate_fact_digest": evidence[
                "world_candidate_fact_digest"
            ],
            "world_candidate_relation_digest": evidence[
                "world_candidate_relation_digest"
            ],
            "future_only_learning_delta_digest": evidence[
                "future_only_learning_delta_digest"
            ],
            "maintenance_policy_candidate_digest": evidence[
                "maintenance_policy_candidate_digest"
            ],
            "baseline_observation_digest": evidence[
                "baseline_observation_digest"
            ],
            "durability_observation_digest": evidence[
                "durability_observation_digest"
            ],
            "adverse_effect_observation_digest": evidence[
                "adverse_effect_observation_digest"
            ],
            "distributional_observation_digest": evidence[
                "distributional_observation_digest"
            ],
            "uncertainty_digest": evidence["uncertainty_digest"],
            "calibration_digest": evidence["calibration_digest"],
            "provenance_chain_digests": list(provenance),
            "monitoring_state": "observed_pending_verification",
            "verification_state": "verification_debt_open",
            "verification_intake_admitted": True,
            "verification_receipt_required": True,
            "future_only": True,
            "active_now": False,
            "maintenance_action_performed": False,
            "current_policy_activated": False,
            "automatic_learning_update": False,
        }
        verification_handoff_digest = canonical_digest(verification_handoff)

    resulting_lineage = sorted(
        set(source_lineage)
        | set(raw_artifacts)
        | set(provenance)
        | {
            source_digest,
            evidence_digest,
            review_digest,
            context_digest,
            context["requested_monitoring_observation_operation_digest"],
            context["exact_monitoring_observation_cycle_digest"],
            observation_record_digest,
            debt_digest,
            future_only_maintenance_monitoring_observation_bundle_digest,
            *(
                {verification_handoff_digest}
                if verification_handoff_digest
                else set()
            ),
        }
    )
    resulting_responsibility = sorted(
        set(source_responsibility)
        | {
            evidence["collector_id"],
            evidence["evidence_source_id"],
            review["reviewer_id"],
            observeos_monitoring_responsibility_digest,
        }
    )

    receipt = {
        "kernel": (
            "ObserveOS Dukkha-Preserving Future-Only Maintenance-Monitoring "
            "Observation Intake Kernel"
        ),
        "kernel_version": "v0.1",
        "observeos_version": "v0.6",
        "status": (
            "OBSERVEOS_DUKKHA_PRESERVING_FUTURE_ONLY_MAINTENANCE_MONITORING_"
            "OBSERVATION_ROUTED"
        ),
        "source_learnos_receipt": source,
        "source_learnos_receipt_digest": source_digest,
        "source_future_only_learning_evidence_packet_digest": source[
            SOURCE_EVIDENCE_DIGEST_FIELD
        ],
        "source_future_only_learning_review_certificate_digest": source[
            SOURCE_REVIEW_DIGEST_FIELD
        ],
        "source_future_only_learning_intake_context_digest": source[
            SOURCE_CONTEXT_DIGEST_FIELD
        ],
        "source_future_only_learning_record_digest": source[
            "future_only_learning_record_digest"
        ],
        "source_future_only_learning_debt_consumption_record_digest": source[
            "future_only_learning_debt_consumption_record_digest"
        ],
        "source_future_only_learning_delta_binding_digest": source[
            "future_only_learning_delta_binding_digest"
        ],
        "source_maintenance_monitoring_handoff_envelope_digest": source[
            "maintenance_monitoring_handoff_envelope_digest"
        ],
        "maintenance_monitoring_observation_evidence_packet": evidence,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        "maintenance_monitoring_observation_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "maintenance_monitoring_observation_policy_digest": (
            maintenance_monitoring_observation_policy_digest
        ),
        "observeos_monitoring_responsibility_digest": (
            observeos_monitoring_responsibility_digest
        ),
        "maintenance_monitoring_observation_request_id": (
            maintenance_monitoring_observation_request_id
        ),
        "future_only_maintenance_monitoring_observation_bundle_digest": (
            future_only_maintenance_monitoring_observation_bundle_digest
        ),
        "maintenance_monitoring_observation_disposition": disposition,
        "maintenance_monitoring_observation_state_before": STATE_BEFORE,
        "maintenance_monitoring_observation_state_after": state_after,
        "maintenance_monitoring_observation_record": observation_record,
        "maintenance_monitoring_observation_record_digest": (
            observation_record_digest
        ),
        "maintenance_monitoring_observation_debt_consumption_record": (
            debt_record
        ),
        "maintenance_monitoring_observation_debt_consumption_record_digest": (
            debt_digest
        ),
        "maintenance_monitoring_verification_handoff_envelope": (
            verification_handoff
        ),
        "maintenance_monitoring_verification_handoff_envelope_digest": (
            verification_handoff_digest
        ),
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence[
            "world_candidate_relation_digest"
        ],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "future_only_learning_delta_digest": evidence[
            "future_only_learning_delta_digest"
        ],
        "maintenance_policy_candidate_digest": evidence[
            "maintenance_policy_candidate_digest"
        ],
        "source_learnos_receipt_supplied": True,
        "source_learnos_receipt_fully_revalidated": True,
        "world_fact_confirmed": True,
        "causal_attribution_confirmed": True,
        "dukkha_reduction_realized_confirmed": True,
        "future_only_learning_delta_recorded": True,
        "future_only_learning_delta_activated": False,
        "maintenance_monitoring_handoff_prepared": True,
        "maintenance_monitoring_handoff_consumed_for_observation": supported,
        "maintenance_monitoring_activated": False,
        "maintenance_monitoring_observation_supported": supported,
        "maintenance_monitoring_observation_recorded": supported,
        "maintenance_monitoring_observation_scope_exactly_bounded": supported,
        "maintenance_monitoring_observation_debt_consumed": supported,
        "maintenance_monitoring_observation_debt_open": not supported,
        "maintenance_monitoring_observation_replay_closed": supported,
        "source_learnos_receipt_replay_closed": supported,
        "monitoring_observation_evidence_replay_closed": supported,
        "monitoring_observation_review_replay_closed": supported,
        "monitoring_observation_nonce_consumed": supported,
        "monitoring_observation_nonce_replay_closed": supported,
        "monitoring_observation_session_replay_closed": supported,
        "maintenance_monitoring_verification_handoff_prepared": supported,
        "verification_intake_admitted": supported,
        "verification_receipt_required": supported,
        "verification_completed": False,
        "verification_debt_open": supported,
        "observation_collection_performed_by_kernel": False,
        "maintenance_action_performed": False,
        "persistent_world_state_changed_by_observation": False,
        "world_model_revision_incremented_by_observation": False,
        "current_plan_revised_by_observation": False,
        "current_policy_activated_by_observation": False,
        "learning_delta_activated_by_observation": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "automatic_truth_generalization": False,
        "automatic_causal_attribution": False,
        "automatic_dukkha_realization_confirmation": False,
        "automatic_learning_update": False,
        "automatic_policy_activation": False,
        "automatic_maintenance_action": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "automatic_compensation": False,
        "generalized_benefit_claimed": False,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_observeos": False,
        "plan_revision_authority_granted_to_observeos": False,
        "dukkha_minimization_authority_granted_to_observeos": False,
        "general_execution_authority_granted": False,
        "execution_permission": False,
        "world_mutation_authority_granted": False,
        "current_policy_activation_authority_granted": False,
        "maintenance_action_authority_granted_to_observeos": False,
        "evidence_lineage_preserved": True,
        "responsibility_lineage_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return ObserveOSFutureOnlyMaintenanceMonitoringObservationResult(
        STATUS_READY, [], receipt
    )
