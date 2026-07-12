#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD as SOURCE_CONTEXT_DIGEST_FIELD,
    DISPOSITION_SUPPORTED as SOURCE_DISPOSITION_SUPPORTED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED as SOURCE_STATE_AFTER_SUPPORTED,
    canonical_digest,
    compute_maintenance_monitoring_observation_evidence_packet_digest,
    compute_maintenance_monitoring_observation_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake_receipt_digest"
EVIDENCE_DIGEST_FIELD = "maintenance_monitoring_verification_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "maintenance_monitoring_verification_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "maintenance_monitoring_verification_intake_context_digest"
STATE_BEFORE = SOURCE_STATE_AFTER_SUPPORTED
STATE_AFTER_SUPPORTED = STATE_BEFORE + "_maintenance_monitoring_observation_verified_maintenance_disposition_pending"

DISPOSITION_SUPPORTED = "maintenance_monitoring_observation_verification_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "verification_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "verification_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_monitoring_verification_evidence_required"
DISPOSITION_SOURCE_REPAIR = "source_observeos_receipt_correspondence_repair_required"
DISPOSITION_OBSERVATION_RECORD_REPAIR = "observation_record_correspondence_repair_required"
DISPOSITION_HANDOFF_REPAIR = "verification_handoff_correspondence_repair_required"
DISPOSITION_BASELINE_REPAIR = "baseline_observation_correspondence_repair_required"
DISPOSITION_DURABILITY_REPAIR = "durability_verification_repair_required"
DISPOSITION_ADVERSE_REPAIR = "adverse_effect_verification_repair_required"
DISPOSITION_DISTRIBUTIONAL_REPAIR = "distributional_verification_repair_required"
DISPOSITION_REOBSERVATION_TRIGGER_REPAIR = "reobservation_trigger_verification_repair_required"
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = "current_state_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

EVIDENCE_FIELDS = {
    "source_observeos_receipt_digest",
    "source_maintenance_monitoring_observation_evidence_packet_digest",
    "source_maintenance_monitoring_observation_review_certificate_digest",
    "source_maintenance_monitoring_observation_record_digest",
    "source_maintenance_monitoring_observation_debt_consumption_record_digest",
    "source_maintenance_monitoring_verification_handoff_envelope_digest",
    "world_candidate_fact_digest", "world_candidate_relation_digest",
    "resulting_world_state_digest", "resulting_world_revision",
    "future_only_learning_delta_digest", "maintenance_policy_candidate_digest",
    "baseline_observation_digest", "durability_observation_digest",
    "adverse_effect_observation_digest", "distributional_observation_digest",
    "observation_record_correspondence_digest",
    "maintenance_window_verification_digest", "durability_verification_digest",
    "adverse_effect_verification_digest", "distributional_verification_digest",
    "reobservation_trigger_verification_digest", "verification_artifact_digests",
    "uncertainty_digest", "calibration_digest", "provenance_chain_digests",
    "tamper_evidence_digest", "protected_group_verification_impact_digest",
    "future_subject_verification_impact_digest", "verifier_id", "evidence_source_id",
    "verification_started_epoch", "verification_completed_epoch",
    "maximum_verification_duration",
    "independent_maintenance_monitoring_verification_evidence",
    "exactly_one_monitoring_verification", "observation_recollected",
    "maintenance_action_performed", "current_world_mutation_performed",
    "current_plan_revised", "current_policy_activated", "learning_delta_activated",
    "generalized_benefit_claimed", "authority_escalation_claimed",
    EVIDENCE_DIGEST_FIELD,
}
REVIEW_FIELDS = {
    "source_observeos_receipt_digest", EVIDENCE_DIGEST_FIELD,
    "source_maintenance_monitoring_observation_record_digest",
    "source_maintenance_monitoring_verification_handoff_envelope_digest",
    "world_candidate_fact_digest", "world_candidate_relation_digest",
    "resulting_world_state_digest", "resulting_world_revision",
    "future_only_learning_delta_digest", "maintenance_policy_candidate_digest",
    "reviewer_id", "review_method_digest", "review_evidence_digest",
    "review_started_epoch", "review_completed_epoch", "maximum_review_duration",
    "source_receipt_correspondence_confirmed",
    "observation_record_correspondence_confirmed",
    "verification_handoff_correspondence_confirmed",
    "baseline_observation_correspondence_confirmed",
    "durability_verification_adequate", "adverse_effect_verification_adequate",
    "distributional_verification_adequate",
    "reobservation_trigger_verification_adequate", "uncertainty_adequate",
    "calibration_adequate", "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported", "no_current_state_mutation",
    "no_maintenance_action_performed", "no_authority_escalation",
    REVIEW_DIGEST_FIELD,
}
CONTEXT_FIELDS = {
    "source_observeos_receipt_digest", EVIDENCE_DIGEST_FIELD, REVIEW_DIGEST_FIELD,
    "current_world_model_state_digest", "current_world_model_revision",
    "current_future_only_learning_delta_digest",
    "current_maintenance_policy_candidate_digest",
    "source_monitoring_observation_epoch", "monitoring_verification_intake_epoch",
    "maximum_monitoring_verification_intake_delay",
    "monitoring_verification_intake_session_id",
    "monitoring_verification_intake_nonce_digest",
    "prior_monitoring_verification_intake_session_ids",
    "prior_monitoring_verification_evidence_packet_digests",
    "prior_monitoring_verification_review_certificate_digests",
    "prior_monitoring_verification_intake_nonce_digests",
    "prior_monitoring_verification_source_receipt_digests",
    "requested_monitoring_verification_operation_digest",
    "exact_monitoring_verification_cycle_digest", CONTEXT_DIGEST_FIELD,
}

@dataclass
class VerifyOSFutureOnlyMaintenanceMonitoringVerificationResult:
    status: str
    blockers: list[str]
    receipt: dict | None

def _map(v: Any) -> dict:
    return dict(v) if isinstance(v, Mapping) else {}

def _digest_without(v: Mapping[str, Any], key: str) -> str:
    d = dict(v); d.pop(key, None); return canonical_digest(d)

def _exact(actual: Mapping[str, Any], expected: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    blockers.extend(f"{prefix}_{k}_mismatch" for k, v in expected.items() if actual.get(k) != v)

def _strings(v: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(v, list) and (allow_empty or bool(v)) and all(isinstance(x, str) and x for x in v)
    return bool(ok and v == sorted(v) and len(v) == len(set(v))), list(v) if isinstance(v, list) else []

def _duration(v: Mapping[str, Any], start: str, end: str, maximum: str) -> bool:
    a, b, m = v.get(start), v.get(end), v.get(maximum)
    return all(isinstance(x, int) and not isinstance(x, bool) for x in (a, b, m)) and 0 <= a <= b and 0 <= b - a <= m

def compute_maintenance_monitoring_verification_evidence_packet_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, EVIDENCE_DIGEST_FIELD)

def compute_maintenance_monitoring_verification_review_certificate_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, REVIEW_DIGEST_FIELD)

def compute_maintenance_monitoring_verification_intake_context_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, CONTEXT_DIGEST_FIELD)

def compute_requested_monitoring_verification_operation_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_observeos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        "source_observation_record_digest": source.get("maintenance_monitoring_observation_record_digest"),
        "source_verification_handoff_digest": source.get("maintenance_monitoring_verification_handoff_envelope_digest"),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER_SUPPORTED,
    })

def compute_exact_monitoring_verification_cycle_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_observeos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "monitoring_verification_intake_session_id": context.get("monitoring_verification_intake_session_id"),
        "monitoring_verification_intake_nonce_digest": context.get("monitoring_verification_intake_nonce_digest"),
        "monitoring_verification_intake_epoch": context.get("monitoring_verification_intake_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_monitoring_verification_operation_digest": context.get("requested_monitoring_verification_operation_digest"),
    })

def compute_future_only_maintenance_monitoring_verification_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)

def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_observeos_receipt_missing"); return "", {}, {}, {}, 0, [], []
    _exact(source, {
        "kernel": "ObserveOS Dukkha-Preserving Future-Only Maintenance-Monitoring Observation Intake Kernel",
        "kernel_version": "v0.1", "observeos_version": "v0.6",
        "status": "OBSERVEOS_DUKKHA_PRESERVING_FUTURE_ONLY_MAINTENANCE_MONITORING_OBSERVATION_ROUTED",
        "maintenance_monitoring_observation_disposition": SOURCE_DISPOSITION_SUPPORTED,
        "maintenance_monitoring_observation_state_after": STATE_BEFORE,
        "world_fact_confirmed": True, "causal_attribution_confirmed": True,
        "dukkha_reduction_realized_confirmed": True,
        "future_only_learning_delta_recorded": True,
        "future_only_learning_delta_activated": False,
        "maintenance_monitoring_observation_supported": True,
        "maintenance_monitoring_observation_recorded": True,
        "maintenance_monitoring_observation_scope_exactly_bounded": True,
        "maintenance_monitoring_verification_handoff_prepared": True,
        "verification_intake_admitted": True, "verification_receipt_required": True,
        "verification_completed": False, "verification_debt_open": True,
        "maintenance_monitoring_activated": False, "maintenance_action_performed": False,
        "persistent_world_state_changed_by_observation": False,
        "world_model_revision_incremented_by_observation": False,
        "current_plan_revised_by_observation": False,
        "current_policy_activated_by_observation": False,
        "learning_delta_activated_by_observation": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "history_read_only": True, "future_only": True, "active_now": False,
    }, "source", blockers)
    digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    if digest != _digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD): blockers.append("source_observeos_receipt_digest_mismatch")
    if digest != expected: blockers.append("source_observeos_expected_binding_mismatch")
    obs_ev = _map(source.get("maintenance_monitoring_observation_evidence_packet"))
    obs_rv = _map(source.get("maintenance_monitoring_observation_review_certificate"))
    record = _map(source.get("maintenance_monitoring_observation_record"))
    debt = _map(source.get("maintenance_monitoring_observation_debt_consumption_record"))
    handoff = _map(source.get("maintenance_monitoring_verification_handoff_envelope"))
    if source.get(SOURCE_EVIDENCE_DIGEST_FIELD) != compute_maintenance_monitoring_observation_evidence_packet_digest(obs_ev): blockers.append("source_monitoring_observation_evidence_digest_mismatch")
    if source.get(SOURCE_REVIEW_DIGEST_FIELD) != compute_maintenance_monitoring_observation_review_certificate_digest(obs_rv): blockers.append("source_monitoring_observation_review_digest_mismatch")
    for item, field in ((record, "maintenance_monitoring_observation_record_digest"), (debt, "maintenance_monitoring_observation_debt_consumption_record_digest"), (handoff, "maintenance_monitoring_verification_handoff_envelope_digest")):
        if not item or source.get(field) != canonical_digest(item): blockers.append(f"source_{field}_mismatch")
    _exact(record, {
        "source_learnos_receipt_digest": source.get("source_learnos_receipt_digest"),
        SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "source_future_only_learning_delta_binding_digest": source.get("source_future_only_learning_delta_binding_digest"),
        "source_maintenance_monitoring_handoff_envelope_digest": source.get("source_maintenance_monitoring_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("resulting_world_state_digest"),
        "resulting_world_revision": source.get("resulting_world_revision"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "disposition": SOURCE_DISPOSITION_SUPPORTED, "state_after": STATE_BEFORE,
    }, "source_observation_record", blockers)
    _exact(debt, {
        "observation_record_digest": source.get("maintenance_monitoring_observation_record_digest"),
        "observation_debt_consumed": True,
        "source_maintenance_monitoring_handoff_consumed": True,
        "double_observation_performed": False,
    }, "source_observation_debt", blockers)
    _exact(handoff, {
        "source_learnos_receipt_digest": source.get("source_learnos_receipt_digest"),
        SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "observation_record_digest": source.get("maintenance_monitoring_observation_record_digest"),
        "source_future_only_learning_delta_binding_digest": source.get("source_future_only_learning_delta_binding_digest"),
        "source_maintenance_monitoring_handoff_envelope_digest": source.get("source_maintenance_monitoring_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "monitoring_state": "observed_pending_verification",
        "verification_state": "verification_debt_open",
        "verification_intake_admitted": True, "verification_receipt_required": True,
        "future_only": True, "active_now": False, "maintenance_action_performed": False,
        "current_policy_activated": False, "automatic_learning_update": False,
    }, "source_verification_handoff", blockers)
    lok, lineage = _strings(source.get("resulting_lineage_digests"))
    rok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lok: blockers.append("source_resulting_lineage_invalid")
    if not rok: blockers.append("source_resulting_responsibility_invalid")
    epoch = record.get("monitoring_observation_intake_epoch", 0)
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        blockers.append("source_monitoring_observation_epoch_invalid"); epoch = 0
    return digest, obs_ev, record, handoff, epoch, lineage, responsibility

def _verify_evidence(evidence: dict, expected: str, source: dict, handoff: dict, blockers: list[str]):
    if not evidence:
        blockers.append("maintenance_monitoring_verification_evidence_missing"); return "", False, [], []
    if set(evidence) != EVIDENCE_FIELDS: blockers.append("maintenance_monitoring_verification_evidence_schema_invalid")
    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if digest != compute_maintenance_monitoring_verification_evidence_packet_digest(evidence): blockers.append("maintenance_monitoring_verification_evidence_digest_mismatch")
    if digest != expected: blockers.append("maintenance_monitoring_verification_evidence_expected_binding_mismatch")
    _exact(evidence, {
        "source_observeos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        "source_maintenance_monitoring_observation_evidence_packet_digest": source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        "source_maintenance_monitoring_observation_review_certificate_digest": source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "source_maintenance_monitoring_observation_record_digest": source.get("maintenance_monitoring_observation_record_digest"),
        "source_maintenance_monitoring_observation_debt_consumption_record_digest": source.get("maintenance_monitoring_observation_debt_consumption_record_digest"),
        "source_maintenance_monitoring_verification_handoff_envelope_digest": source.get("maintenance_monitoring_verification_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("resulting_world_state_digest"),
        "resulting_world_revision": source.get("resulting_world_revision"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "baseline_observation_digest": handoff.get("baseline_observation_digest"),
        "durability_observation_digest": handoff.get("durability_observation_digest"),
        "adverse_effect_observation_digest": handoff.get("adverse_effect_observation_digest"),
        "distributional_observation_digest": handoff.get("distributional_observation_digest"),
    }, "verification_evidence", blockers)
    aok, artifacts = _strings(evidence.get("verification_artifact_digests"))
    pok, provenance = _strings(evidence.get("provenance_chain_digests"))
    if not aok: blockers.append("maintenance_monitoring_verification_artifacts_invalid")
    if not pok: blockers.append("maintenance_monitoring_verification_provenance_invalid")
    return digest, _duration(evidence, "verification_started_epoch", "verification_completed_epoch", "maximum_verification_duration"), artifacts, provenance

def _verify_review(review: dict, expected: str, source: dict, evidence: dict, blockers: list[str]):
    if not review:
        blockers.append("maintenance_monitoring_verification_review_missing"); return "", False
    if set(review) != REVIEW_FIELDS: blockers.append("maintenance_monitoring_verification_review_schema_invalid")
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if digest != compute_maintenance_monitoring_verification_review_certificate_digest(review): blockers.append("maintenance_monitoring_verification_review_digest_mismatch")
    if digest != expected: blockers.append("maintenance_monitoring_verification_review_expected_binding_mismatch")
    _exact(review, {
        "source_observeos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "source_maintenance_monitoring_observation_record_digest": source.get("maintenance_monitoring_observation_record_digest"),
        "source_maintenance_monitoring_verification_handoff_envelope_digest": source.get("maintenance_monitoring_verification_handoff_envelope_digest"),
        "world_candidate_fact_digest": evidence.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": evidence.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": evidence.get("resulting_world_state_digest"),
        "resulting_world_revision": evidence.get("resulting_world_revision"),
        "future_only_learning_delta_digest": evidence.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": evidence.get("maintenance_policy_candidate_digest"),
    }, "verification_review", blockers)
    return digest, _duration(review, "review_started_epoch", "review_completed_epoch", "maximum_review_duration")

def _verify_context(context: dict, expected: str, source: dict, evidence: dict, review: dict, source_epoch: int, blockers: list[str]):
    if not context:
        blockers.append("maintenance_monitoring_verification_context_missing"); return "", {}
    if set(context) != CONTEXT_FIELDS: blockers.append("maintenance_monitoring_verification_context_schema_invalid")
    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if digest != compute_maintenance_monitoring_verification_intake_context_digest(context): blockers.append("maintenance_monitoring_verification_context_digest_mismatch")
    if digest != expected: blockers.append("maintenance_monitoring_verification_context_expected_binding_mismatch")
    _exact(context, {
        "source_observeos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "source_monitoring_observation_epoch": source_epoch,
    }, "verification_context", blockers)
    if context.get("requested_monitoring_verification_operation_digest") != compute_requested_monitoring_verification_operation_digest(source, evidence, review): blockers.append("requested_monitoring_verification_operation_digest_mismatch")
    if context.get("exact_monitoring_verification_cycle_digest") != compute_exact_monitoring_verification_cycle_digest(source, evidence, review, context): blockers.append("exact_monitoring_verification_cycle_digest_mismatch")
    prior_fields = (
        "prior_monitoring_verification_intake_session_ids",
        "prior_monitoring_verification_evidence_packet_digests",
        "prior_monitoring_verification_review_certificate_digests",
        "prior_monitoring_verification_intake_nonce_digests",
        "prior_monitoring_verification_source_receipt_digests",
    )
    for field in prior_fields:
        if not _strings(context.get(field), True)[0]: blockers.append(f"{field}_invalid")
    world_current = all((
        context.get("current_world_model_state_digest") == source.get("resulting_world_state_digest"),
        context.get("current_world_model_revision") == source.get("resulting_world_revision"),
        context.get("current_future_only_learning_delta_digest") == source.get("future_only_learning_delta_digest"),
        context.get("current_maintenance_policy_candidate_digest") == source.get("maintenance_policy_candidate_digest"),
    ))
    intake, maximum = context.get("monitoring_verification_intake_epoch"), context.get("maximum_monitoring_verification_intake_delay")
    context_current = all(isinstance(x, int) and not isinstance(x, bool) for x in (intake, maximum)) and source_epoch <= intake and 0 <= intake - source_epoch <= maximum
    replay = any((
        context.get("monitoring_verification_intake_session_id") in context.get(prior_fields[0], []),
        evidence.get(EVIDENCE_DIGEST_FIELD) in context.get(prior_fields[1], []),
        review.get(REVIEW_DIGEST_FIELD) in context.get(prior_fields[2], []),
        context.get("monitoring_verification_intake_nonce_digest") in context.get(prior_fields[3], []),
        source.get(SOURCE_RECEIPT_DIGEST_FIELD) in context.get(prior_fields[4], []),
    ))
    return digest, {"world_current": world_current, "context_current": context_current, "replay": replay}

def _route(evidence: Mapping[str, Any], review: Mapping[str, Any], checks: Mapping[str, bool], evidence_current: bool, review_current: bool) -> str:
    if checks.get("replay"): return DISPOSITION_REPLAY_REJECTED
    if not checks.get("world_current"): return DISPOSITION_WORLD_REFRESH
    if not checks.get("context_current"): return DISPOSITION_CONTEXT_REFRESH
    if not review_current: return DISPOSITION_REVIEW_REFRESH
    if not evidence_current or not evidence.get("independent_maintenance_monitoring_verification_evidence") or not evidence.get("exactly_one_monitoring_verification") or evidence.get("observation_recollected"): return DISPOSITION_ADDITIONAL_EVIDENCE
    routes = (
        ("source_receipt_correspondence_confirmed", DISPOSITION_SOURCE_REPAIR),
        ("observation_record_correspondence_confirmed", DISPOSITION_OBSERVATION_RECORD_REPAIR),
        ("verification_handoff_correspondence_confirmed", DISPOSITION_HANDOFF_REPAIR),
        ("baseline_observation_correspondence_confirmed", DISPOSITION_BASELINE_REPAIR),
        ("durability_verification_adequate", DISPOSITION_DURABILITY_REPAIR),
        ("adverse_effect_verification_adequate", DISPOSITION_ADVERSE_REPAIR),
        ("distributional_verification_adequate", DISPOSITION_DISTRIBUTIONAL_REPAIR),
        ("reobservation_trigger_verification_adequate", DISPOSITION_REOBSERVATION_TRIGGER_REPAIR),
        ("uncertainty_adequate", DISPOSITION_UNCERTAINTY_REPAIR),
        ("calibration_adequate", DISPOSITION_CALIBRATION_REPAIR),
        ("provenance_continuity_preserved", DISPOSITION_PROVENANCE_REPAIR),
    )
    for field, disposition in routes:
        if not review.get(field): return disposition
    if not review.get("protected_group_nonexternalization_supported") or not review.get("future_nonexternalization_supported"): return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if any((evidence.get("maintenance_action_performed"), evidence.get("current_world_mutation_performed"), evidence.get("current_plan_revised"), evidence.get("current_policy_activated"), evidence.get("learning_delta_activated"), not review.get("no_current_state_mutation"), not review.get("no_maintenance_action_performed"))): return DISPOSITION_CURRENT_STATE_MUTATION_REJECTED
    if evidence.get("generalized_benefit_claimed") or evidence.get("authority_escalation_claimed") or not review.get("no_authority_escalation"): return DISPOSITION_AUTHORITY_ESCALATION_REJECTED
    return DISPOSITION_SUPPORTED

def build_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake(
    *, source_observeos_receipt: Mapping[str, Any],
    expected_source_observeos_receipt_digest: str,
    maintenance_monitoring_verification_evidence_packet: Mapping[str, Any],
    expected_maintenance_monitoring_verification_evidence_packet_digest: str,
    maintenance_monitoring_verification_review_certificate: Mapping[str, Any],
    expected_maintenance_monitoring_verification_review_certificate_digest: str,
    maintenance_monitoring_verification_intake_context: Mapping[str, Any],
    expected_maintenance_monitoring_verification_intake_context_digest: str,
    maintenance_monitoring_verification_policy_digest: str,
    verifyos_monitoring_responsibility_digest: str,
    maintenance_monitoring_verification_request_id: str,
    future_only_maintenance_monitoring_verification_bundle_digest: str,
) -> VerifyOSFutureOnlyMaintenanceMonitoringVerificationResult:
    source, evidence, review, context = map(_map, (source_observeos_receipt, maintenance_monitoring_verification_evidence_packet, maintenance_monitoring_verification_review_certificate, maintenance_monitoring_verification_intake_context))
    blockers: list[str] = []
    source_digest, _, source_record, handoff, source_epoch, source_lineage, source_responsibility = _verify_source(source, expected_source_observeos_receipt_digest, blockers)
    evidence_digest, evidence_current, artifacts, provenance = _verify_evidence(evidence, expected_maintenance_monitoring_verification_evidence_packet_digest, source, handoff, blockers)
    review_digest, review_current = _verify_review(review, expected_maintenance_monitoring_verification_review_certificate_digest, source, evidence, blockers)
    context_digest, checks = _verify_context(context, expected_maintenance_monitoring_verification_intake_context_digest, source, evidence, review, source_epoch, blockers)
    if not blockers:
        bundle = compute_future_only_maintenance_monitoring_verification_bundle_digest(
            source_observeos_receipt_digest=source_digest,
            expected_source_observeos_receipt_digest=expected_source_observeos_receipt_digest,
            source_maintenance_monitoring_observation_record_digest=source.get("maintenance_monitoring_observation_record_digest"),
            source_maintenance_monitoring_verification_handoff_envelope_digest=source.get("maintenance_monitoring_verification_handoff_envelope_digest"),
            maintenance_monitoring_verification_evidence_packet_digest=evidence_digest,
            expected_maintenance_monitoring_verification_evidence_packet_digest=expected_maintenance_monitoring_verification_evidence_packet_digest,
            maintenance_monitoring_verification_review_certificate_digest=review_digest,
            expected_maintenance_monitoring_verification_review_certificate_digest=expected_maintenance_monitoring_verification_review_certificate_digest,
            maintenance_monitoring_verification_intake_context_digest=context_digest,
            expected_maintenance_monitoring_verification_intake_context_digest=expected_maintenance_monitoring_verification_intake_context_digest,
            requested_monitoring_verification_operation_digest=context.get("requested_monitoring_verification_operation_digest"),
            exact_monitoring_verification_cycle_digest=context.get("exact_monitoring_verification_cycle_digest"),
            maintenance_monitoring_verification_policy_digest=maintenance_monitoring_verification_policy_digest,
            verifyos_monitoring_responsibility_digest=verifyos_monitoring_responsibility_digest,
            maintenance_monitoring_verification_request_id=maintenance_monitoring_verification_request_id,
        )
        if bundle != future_only_maintenance_monitoring_verification_bundle_digest: blockers.append("future_only_maintenance_monitoring_verification_bundle_digest_mismatch")
    if blockers: return VerifyOSFutureOnlyMaintenanceMonitoringVerificationResult(STATUS_BLOCKED, sorted(set(blockers)), None)
    disposition = _route(evidence, review, checks, evidence_current, review_current)
    supported, state_after = disposition == DISPOSITION_SUPPORTED, STATE_AFTER_SUPPORTED if disposition == DISPOSITION_SUPPORTED else STATE_BEFORE
    record = {
        "source_observeos_receipt_digest": source_digest, EVIDENCE_DIGEST_FIELD: evidence_digest, REVIEW_DIGEST_FIELD: review_digest,
        "source_maintenance_monitoring_observation_record_digest": source["maintenance_monitoring_observation_record_digest"],
        "source_maintenance_monitoring_verification_handoff_envelope_digest": source["maintenance_monitoring_verification_handoff_envelope_digest"],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"], "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"], "resulting_world_revision": evidence["resulting_world_revision"],
        "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"], "maintenance_policy_candidate_digest": evidence["maintenance_policy_candidate_digest"],
        "baseline_observation_digest": evidence["baseline_observation_digest"], "durability_verification_digest": evidence["durability_verification_digest"],
        "adverse_effect_verification_digest": evidence["adverse_effect_verification_digest"], "distributional_verification_digest": evidence["distributional_verification_digest"],
        "monitoring_verification_intake_session_id": context["monitoring_verification_intake_session_id"],
        "monitoring_verification_intake_nonce_digest": context["monitoring_verification_intake_nonce_digest"],
        "monitoring_verification_intake_epoch": context["monitoring_verification_intake_epoch"],
        "disposition": disposition, "state_before": STATE_BEFORE, "state_after": state_after,
    }
    record_digest = canonical_digest(record)
    debt = {"source_observeos_receipt_digest": source_digest, "verification_record_digest": record_digest, "verification_debt_consumed": supported, "source_verification_handoff_consumed": supported, "double_verification_performed": False}
    debt_digest = canonical_digest(debt)
    maintenance_handoff = None
    maintenance_handoff_digest = ""
    if supported:
        maintenance_handoff = {
            "source_observeos_receipt_digest": source_digest, EVIDENCE_DIGEST_FIELD: evidence_digest, REVIEW_DIGEST_FIELD: review_digest,
            "verification_record_digest": record_digest, "verification_debt_consumption_record_digest": debt_digest,
            "source_maintenance_monitoring_observation_record_digest": source["maintenance_monitoring_observation_record_digest"],
            "world_candidate_fact_digest": evidence["world_candidate_fact_digest"], "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
            "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"], "maintenance_policy_candidate_digest": evidence["maintenance_policy_candidate_digest"],
            "monitoring_verification_state": "verified_pending_maintenance_disposition", "maintenance_disposition_state": "disposition_debt_open",
            "future_only": True, "active_now": False, "maintenance_monitoring_activated": False, "maintenance_action_performed": False,
            "current_policy_activated": False, "automatic_maintenance_action": False,
        }
        maintenance_handoff_digest = canonical_digest(maintenance_handoff)
    lineage = sorted(set(source_lineage) | set(artifacts) | set(provenance) | {source_digest, evidence_digest, review_digest, context_digest, context["requested_monitoring_verification_operation_digest"], context["exact_monitoring_verification_cycle_digest"], record_digest, debt_digest, future_only_maintenance_monitoring_verification_bundle_digest} | ({maintenance_handoff_digest} if maintenance_handoff_digest else set()))
    responsibility = sorted(set(source_responsibility) | {evidence["verifier_id"], evidence["evidence_source_id"], review["reviewer_id"], verifyos_monitoring_responsibility_digest})
    receipt = {
        "kernel": "VerifyOS Dukkha-Preserving Future-Only Maintenance-Monitoring Observation Verification Intake Kernel",
        "kernel_version": "v0.1", "verifyos_version": "v0.11",
        "status": "VERIFYOS_DUKKHA_PRESERVING_FUTURE_ONLY_MAINTENANCE_MONITORING_OBSERVATION_VERIFICATION_ROUTED",
        "source_observeos_receipt": source, "source_observeos_receipt_digest": source_digest,
        "source_maintenance_monitoring_observation_evidence_packet_digest": source[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_review_certificate_digest": source[SOURCE_REVIEW_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_intake_context_digest": source[SOURCE_CONTEXT_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_record_digest": source["maintenance_monitoring_observation_record_digest"],
        "source_maintenance_monitoring_observation_debt_consumption_record_digest": source["maintenance_monitoring_observation_debt_consumption_record_digest"],
        "source_maintenance_monitoring_verification_handoff_envelope_digest": source["maintenance_monitoring_verification_handoff_envelope_digest"],
        "maintenance_monitoring_verification_evidence_packet": evidence, EVIDENCE_DIGEST_FIELD: evidence_digest,
        "maintenance_monitoring_verification_review_certificate": review, REVIEW_DIGEST_FIELD: review_digest, CONTEXT_DIGEST_FIELD: context_digest,
        "maintenance_monitoring_verification_policy_digest": maintenance_monitoring_verification_policy_digest,
        "verifyos_monitoring_responsibility_digest": verifyos_monitoring_responsibility_digest,
        "maintenance_monitoring_verification_request_id": maintenance_monitoring_verification_request_id,
        "future_only_maintenance_monitoring_verification_bundle_digest": future_only_maintenance_monitoring_verification_bundle_digest,
        "maintenance_monitoring_verification_disposition": disposition,
        "maintenance_monitoring_verification_state_before": STATE_BEFORE, "maintenance_monitoring_verification_state_after": state_after,
        "maintenance_monitoring_verification_record": record, "maintenance_monitoring_verification_record_digest": record_digest,
        "maintenance_monitoring_verification_debt_consumption_record": debt, "maintenance_monitoring_verification_debt_consumption_record_digest": debt_digest,
        "maintenance_disposition_handoff_envelope": maintenance_handoff, "maintenance_disposition_handoff_envelope_digest": maintenance_handoff_digest,
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"], "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"], "resulting_world_revision": evidence["resulting_world_revision"],
        "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"], "maintenance_policy_candidate_digest": evidence["maintenance_policy_candidate_digest"],
        "source_observeos_receipt_supplied": True, "source_observeos_receipt_fully_revalidated": True,
        "world_fact_confirmed": True, "causal_attribution_confirmed": True, "dukkha_reduction_realized_confirmed": True,
        "future_only_learning_delta_recorded": True, "future_only_learning_delta_activated": False,
        "maintenance_monitoring_observation_recorded": True, "maintenance_monitoring_observation_scope_exactly_bounded": True,
        "maintenance_monitoring_observation_verified": supported, "maintenance_monitoring_verification_supported": supported,
        "maintenance_monitoring_verification_scope_exactly_bounded": supported, "maintenance_monitoring_verification_completed": supported,
        "maintenance_monitoring_verification_debt_consumed": supported, "maintenance_monitoring_verification_debt_open": not supported,
        "maintenance_monitoring_verification_replay_closed": supported, "source_observeos_receipt_replay_closed": supported,
        "monitoring_verification_evidence_replay_closed": supported, "monitoring_verification_review_replay_closed": supported,
        "monitoring_verification_nonce_consumed": supported, "monitoring_verification_nonce_replay_closed": supported,
        "monitoring_verification_session_replay_closed": supported, "maintenance_disposition_handoff_prepared": supported,
        "maintenance_disposition_completed": False, "maintenance_disposition_debt_open": supported,
        "verification_evidence_collection_performed_by_kernel": False, "observation_collection_reperformed_by_kernel": False,
        "maintenance_monitoring_activated": False, "maintenance_action_performed": False,
        "persistent_world_state_changed_by_verification": False, "world_model_revision_incremented_by_verification": False,
        "current_plan_revised_by_verification": False, "current_policy_activated_by_verification": False,
        "learning_delta_activated_by_verification": False, "tool_invocation_performed": False, "external_side_effect_performed": False,
        "automatic_truth_generalization": False, "automatic_causal_attribution": False, "automatic_dukkha_realization_confirmation": False,
        "automatic_learning_update": False, "automatic_policy_activation": False, "automatic_maintenance_action": False,
        "automatic_plan_completion": False, "automatic_rollback": False, "automatic_compensation": False, "generalized_benefit_claimed": False,
        "selection_remains_decisionos_owned": True, "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False, "dukkha_minimization_authority_granted_to_verifyos": False,
        "general_execution_authority_granted": False, "execution_permission": False, "world_mutation_authority_granted": False,
        "current_policy_activation_authority_granted": False, "maintenance_action_authority_granted_to_verifyos": False,
        "evidence_lineage_preserved": True, "responsibility_lineage_preserved": True,
        "protected_group_nonexternalization_preserved": True, "future_nonexternalization_preserved": True,
        "history_read_only": True, "future_only": True, "active_now": False,
        "resulting_lineage_digests": lineage, "resulting_responsibility_lineage_digests": responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return VerifyOSFutureOnlyMaintenanceMonitoringVerificationResult(STATUS_READY, [], receipt)
