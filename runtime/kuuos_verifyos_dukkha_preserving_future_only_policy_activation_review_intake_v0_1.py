#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_learnos_dukkha_preserving_future_only_maintenance_disposition_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD as SOURCE_CONTEXT_DIGEST_FIELD,
    DISPOSITION_SUPPORTED as SOURCE_DISPOSITION_SUPPORTED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED as SOURCE_STATE_AFTER_SUPPORTED,
    canonical_digest,
    compute_future_only_maintenance_disposition_evidence_packet_digest,
    compute_future_only_maintenance_disposition_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "verifyos_dukkha_preserving_future_only_policy_activation_review_intake_receipt_digest"
EVIDENCE_DIGEST_FIELD = "future_only_policy_activation_review_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "future_only_policy_activation_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "future_only_policy_activation_review_intake_context_digest"
STATE_BEFORE = SOURCE_STATE_AFTER_SUPPORTED
STATE_AFTER_SUPPORTED = STATE_BEFORE + "_policy_activation_reviewed_activation_authorization_pending"

DISPOSITION_SUPPORTED = "future_only_policy_activation_review_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "policy_activation_review_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "policy_activation_review_certificate_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_policy_activation_review_evidence_required"
DISPOSITION_SOURCE_REPAIR = "source_learnos_receipt_correspondence_repair_required"
DISPOSITION_DISPOSITION_RECORD_REPAIR = "maintenance_disposition_record_correspondence_repair_required"
DISPOSITION_HANDOFF_REPAIR = "policy_activation_review_handoff_correspondence_repair_required"
DISPOSITION_CANDIDATE_REPAIR = "maintenance_policy_candidate_correspondence_repair_required"
DISPOSITION_SCOPE_REPAIR = "policy_activation_scope_repair_required"
DISPOSITION_PRECONDITION_REPAIR = "activation_precondition_repair_required"
DISPOSITION_ROLLBACK_REPAIR = "rollback_plan_repair_required"
DISPOSITION_MONITORING_GUARD_REPAIR = "post_activation_monitoring_guard_repair_required"
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = "current_state_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

EVIDENCE_FIELDS = {
    "source_learnos_receipt_digest",
    "source_maintenance_disposition_evidence_packet_digest",
    "source_maintenance_disposition_review_certificate_digest",
    "source_maintenance_disposition_record_digest",
    "source_maintenance_disposition_debt_consumption_record_digest",
    "source_policy_activation_review_handoff_envelope_digest",
    "world_candidate_fact_digest", "world_candidate_relation_digest",
    "resulting_world_state_digest", "resulting_world_revision",
    "future_only_learning_delta_digest", "maintenance_policy_candidate_digest",
    "future_only_maintenance_objective_digest", "maintenance_noop_threshold_digest",
    "maintenance_escalation_trigger_digest", "reobservation_schedule_digest",
    "proposed_activation_scope_digest", "activation_precondition_set_digest",
    "bounded_subject_scope_digest", "activation_duration_limit_digest",
    "rollback_plan_digest", "post_activation_monitoring_guard_digest",
    "policy_activation_review_artifact_digests",
    "uncertainty_digest", "calibration_digest", "provenance_chain_digests",
    "tamper_evidence_digest", "protected_group_review_impact_digest",
    "future_subject_review_impact_digest", "review_assessor_id", "evidence_source_id",
    "assessment_started_epoch", "assessment_completed_epoch", "maximum_assessment_duration",
    "independent_policy_activation_review_evidence", "exactly_one_policy_activation_review",
    "maintenance_policy_candidate_activated", "maintenance_monitoring_activated",
    "maintenance_action_performed", "current_world_mutation_performed",
    "current_plan_revised", "current_policy_activated", "learning_delta_activated",
    "activation_authorization_granted", "generalized_benefit_claimed",
    "authority_escalation_claimed", EVIDENCE_DIGEST_FIELD,
}
REVIEW_FIELDS = {
    "source_learnos_receipt_digest", EVIDENCE_DIGEST_FIELD,
    "source_maintenance_disposition_record_digest",
    "source_policy_activation_review_handoff_envelope_digest",
    "world_candidate_fact_digest", "world_candidate_relation_digest",
    "resulting_world_state_digest", "resulting_world_revision",
    "future_only_learning_delta_digest", "maintenance_policy_candidate_digest",
    "reviewer_id", "review_method_digest", "review_evidence_digest",
    "review_started_epoch", "review_completed_epoch", "maximum_review_duration",
    "source_receipt_correspondence_confirmed",
    "maintenance_disposition_record_correspondence_confirmed",
    "policy_activation_review_handoff_correspondence_confirmed",
    "maintenance_policy_candidate_correspondence_confirmed",
    "policy_activation_scope_exactly_bounded",
    "activation_preconditions_adequate", "rollback_plan_adequate",
    "post_activation_monitoring_guard_adequate", "uncertainty_adequate",
    "calibration_adequate", "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported", "no_current_state_mutation",
    "no_policy_activation", "no_activation_authorization_granted",
    "no_maintenance_action_performed", "no_authority_escalation",
    REVIEW_DIGEST_FIELD,
}
CONTEXT_FIELDS = {
    "source_learnos_receipt_digest", EVIDENCE_DIGEST_FIELD, REVIEW_DIGEST_FIELD,
    "current_world_model_state_digest", "current_world_model_revision",
    "current_future_only_learning_delta_digest",
    "current_maintenance_policy_candidate_digest",
    "current_maintenance_disposition_record_digest",
    "source_maintenance_disposition_epoch", "policy_activation_review_intake_epoch",
    "maximum_policy_activation_review_intake_delay",
    "policy_activation_review_intake_session_id",
    "policy_activation_review_intake_nonce_digest",
    "prior_policy_activation_review_intake_session_ids",
    "prior_policy_activation_review_evidence_packet_digests",
    "prior_policy_activation_review_certificate_digests",
    "prior_policy_activation_review_intake_nonce_digests",
    "prior_policy_activation_review_source_receipt_digests",
    "requested_policy_activation_review_operation_digest",
    "exact_policy_activation_review_cycle_digest", CONTEXT_DIGEST_FIELD,
}

@dataclass
class VerifyOSFutureOnlyPolicyActivationReviewResult:
    status: str
    blockers: list[str]
    receipt: dict | None

def _map(v: Any) -> dict:
    return dict(v) if isinstance(v, Mapping) else {}

def _digest_without(v: Mapping[str, Any], key: str) -> str:
    out = dict(v); out.pop(key, None); return canonical_digest(out)

def _exact(actual: Mapping[str, Any], expected: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    blockers.extend(f"{prefix}_{k}_mismatch" for k, x in expected.items() if actual.get(k) != x)

def _strings(v: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(v, list) and (allow_empty or bool(v)) and all(isinstance(x, str) and x for x in v)
    return bool(ok and v == sorted(v) and len(v) == len(set(v))), list(v) if isinstance(v, list) else []

def _duration(v: Mapping[str, Any], a: str, b: str, m: str) -> bool:
    x, y, z = v.get(a), v.get(b), v.get(m)
    return all(isinstance(n, int) and not isinstance(n, bool) for n in (x, y, z)) and 0 <= x <= y and 0 <= y - x <= z

def compute_future_only_policy_activation_review_evidence_packet_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, EVIDENCE_DIGEST_FIELD)

def compute_future_only_policy_activation_review_certificate_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, REVIEW_DIGEST_FIELD)

def compute_future_only_policy_activation_review_intake_context_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, CONTEXT_DIGEST_FIELD)

def compute_requested_policy_activation_review_operation_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        "source_maintenance_disposition_record_digest": source.get("future_only_maintenance_disposition_record_digest"),
        "source_policy_activation_review_handoff_envelope_digest": source.get("policy_activation_review_handoff_envelope_digest"),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER_SUPPORTED,
    })

def compute_exact_policy_activation_review_cycle_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "policy_activation_review_intake_session_id": context.get("policy_activation_review_intake_session_id"),
        "policy_activation_review_intake_nonce_digest": context.get("policy_activation_review_intake_nonce_digest"),
        "policy_activation_review_intake_epoch": context.get("policy_activation_review_intake_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_policy_activation_review_operation_digest": context.get("requested_policy_activation_review_operation_digest"),
    })

def compute_future_only_policy_activation_review_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)

def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_learnos_receipt_missing"); return "", {}, {}, 0, [], []
    _exact(source, {
        "kernel": "LearnOS Dukkha-Preserving Future-Only Maintenance Disposition Intake Kernel",
        "kernel_version": "v0.1", "learnos_version": "v0.5",
        "status": "LEARNOS_DUKKHA_PRESERVING_FUTURE_ONLY_MAINTENANCE_DISPOSITION_ROUTED",
        "future_only_maintenance_disposition": SOURCE_DISPOSITION_SUPPORTED,
        "future_only_maintenance_disposition_state_after": STATE_BEFORE,
        "world_fact_confirmed": True, "causal_attribution_confirmed": True,
        "dukkha_reduction_realized_confirmed": True,
        "future_only_learning_delta_recorded": True,
        "future_only_learning_delta_activated": False,
        "maintenance_monitoring_observation_recorded": True,
        "maintenance_monitoring_observation_verified": True,
        "maintenance_monitoring_verification_completed": True,
        "future_only_maintenance_disposition_recorded": True,
        "future_only_maintenance_disposition_scope_exactly_bounded": True,
        "future_only_maintenance_disposition_completed": True,
        "future_only_maintenance_disposition_debt_open": False,
        "maintenance_policy_candidate_retained_future_only": True,
        "policy_activation_review_handoff_prepared": True,
        "policy_activation_review_completed": False,
        "policy_activation_review_debt_open": True,
        "maintenance_policy_candidate_activated": False,
        "maintenance_monitoring_activated": False,
        "maintenance_action_performed": False,
        "current_policy_activated_by_disposition": False,
        "learning_delta_activated_by_disposition": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "history_read_only": True, "future_only": True, "active_now": False,
    }, "source", blockers)
    digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    if digest != _digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD): blockers.append("source_learnos_receipt_digest_mismatch")
    if digest != expected: blockers.append("source_learnos_expected_binding_mismatch")
    ev = _map(source.get("future_only_maintenance_disposition_evidence_packet"))
    rv = _map(source.get("future_only_maintenance_disposition_review_certificate"))
    record = _map(source.get("future_only_maintenance_disposition_record"))
    debt = _map(source.get("future_only_maintenance_disposition_debt_consumption_record"))
    handoff = _map(source.get("policy_activation_review_handoff_envelope"))
    if source.get(SOURCE_EVIDENCE_DIGEST_FIELD) != compute_future_only_maintenance_disposition_evidence_packet_digest(ev):
        blockers.append("source_maintenance_disposition_evidence_digest_mismatch")
    if source.get(SOURCE_REVIEW_DIGEST_FIELD) != compute_future_only_maintenance_disposition_review_certificate_digest(rv):
        blockers.append("source_maintenance_disposition_review_digest_mismatch")
    for item, field in (
        (record, "future_only_maintenance_disposition_record_digest"),
        (debt, "future_only_maintenance_disposition_debt_consumption_record_digest"),
        (handoff, "policy_activation_review_handoff_envelope_digest"),
    ):
        if not item or source.get(field) != canonical_digest(item):
            blockers.append(f"source_{field}_mismatch")
    _exact(record, {
        "source_verifyos_receipt_digest": source.get("source_verifyos_receipt_digest"),
        SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "source_monitoring_verification_record_digest": source.get("source_monitoring_verification_record_digest"),
        "source_maintenance_disposition_handoff_envelope_digest": source.get("source_maintenance_disposition_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("resulting_world_state_digest"),
        "resulting_world_revision": source.get("resulting_world_revision"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "disposition": SOURCE_DISPOSITION_SUPPORTED, "state_after": STATE_BEFORE,
        "bounded_maintenance_outcome": "retain_future_only_maintenance_candidate_pending_policy_activation_review",
    }, "source_maintenance_disposition_record", blockers)
    _exact(debt, {
        "source_verifyos_receipt_digest": source.get("source_verifyos_receipt_digest"),
        "maintenance_disposition_record_digest": source.get("future_only_maintenance_disposition_record_digest"),
        "maintenance_disposition_debt_consumed": True,
        "source_maintenance_disposition_handoff_consumed": True,
        "double_maintenance_disposition_performed": False,
    }, "source_maintenance_disposition_debt", blockers)
    _exact(handoff, {
        "source_verifyos_receipt_digest": source.get("source_verifyos_receipt_digest"),
        SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "maintenance_disposition_record_digest": source.get("future_only_maintenance_disposition_record_digest"),
        "maintenance_disposition_debt_consumption_record_digest": source.get("future_only_maintenance_disposition_debt_consumption_record_digest"),
        "source_monitoring_verification_record_digest": source.get("source_monitoring_verification_record_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "maintenance_disposition_state": "future_only_disposition_recorded_pending_policy_activation_review",
        "policy_activation_review_state": "review_debt_open",
        "future_only": True, "active_now": False, "maintenance_monitoring_activated": False,
        "maintenance_policy_candidate_activated": False, "maintenance_action_performed": False,
        "current_policy_activated": False, "automatic_policy_activation": False,
        "automatic_maintenance_action": False,
    }, "source_policy_activation_review_handoff", blockers)
    lok, lineage = _strings(source.get("resulting_lineage_digests"))
    rok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lok: blockers.append("source_resulting_lineage_invalid")
    if not rok: blockers.append("source_resulting_responsibility_invalid")
    epoch = record.get("maintenance_disposition_intake_epoch", 0)
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        blockers.append("source_maintenance_disposition_epoch_invalid"); epoch = 0
    return digest, record, handoff, epoch, lineage, responsibility

def _verify_evidence(evidence: dict, expected: str, source: dict, record: dict, handoff: dict, blockers: list[str]):
    if not evidence:
        blockers.append("future_only_policy_activation_review_evidence_missing"); return "", False, [], []
    if set(evidence) != EVIDENCE_FIELDS: blockers.append("future_only_policy_activation_review_evidence_schema_invalid")
    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if digest != compute_future_only_policy_activation_review_evidence_packet_digest(evidence): blockers.append("future_only_policy_activation_review_evidence_digest_mismatch")
    if digest != expected: blockers.append("future_only_policy_activation_review_evidence_expected_binding_mismatch")
    _exact(evidence, {
        "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        "source_maintenance_disposition_evidence_packet_digest": source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        "source_maintenance_disposition_review_certificate_digest": source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "source_maintenance_disposition_record_digest": source.get("future_only_maintenance_disposition_record_digest"),
        "source_maintenance_disposition_debt_consumption_record_digest": source.get("future_only_maintenance_disposition_debt_consumption_record_digest"),
        "source_policy_activation_review_handoff_envelope_digest": source.get("policy_activation_review_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("resulting_world_state_digest"),
        "resulting_world_revision": source.get("resulting_world_revision"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "future_only_maintenance_objective_digest": record.get("future_only_maintenance_objective_digest"),
        "maintenance_noop_threshold_digest": record.get("maintenance_noop_threshold_digest"),
        "maintenance_escalation_trigger_digest": record.get("maintenance_escalation_trigger_digest"),
        "reobservation_schedule_digest": record.get("reobservation_schedule_digest"),
    }, "policy_activation_review_evidence", blockers)
    if handoff.get("maintenance_policy_candidate_digest") != evidence.get("maintenance_policy_candidate_digest"):
        blockers.append("policy_activation_review_handoff_candidate_mismatch")
    aok, artifacts = _strings(evidence.get("policy_activation_review_artifact_digests"))
    pok, provenance = _strings(evidence.get("provenance_chain_digests"))
    if not aok: blockers.append("policy_activation_review_artifacts_invalid")
    if not pok: blockers.append("policy_activation_review_provenance_invalid")
    return digest, _duration(evidence, "assessment_started_epoch", "assessment_completed_epoch", "maximum_assessment_duration"), artifacts, provenance

def _verify_review(review: dict, expected: str, source: dict, evidence: dict, blockers: list[str]):
    if not review:
        blockers.append("future_only_policy_activation_review_certificate_missing"); return "", False
    if set(review) != REVIEW_FIELDS: blockers.append("future_only_policy_activation_review_certificate_schema_invalid")
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if digest != compute_future_only_policy_activation_review_certificate_digest(review): blockers.append("future_only_policy_activation_review_certificate_digest_mismatch")
    if digest != expected: blockers.append("future_only_policy_activation_review_certificate_expected_binding_mismatch")
    _exact(review, {
        "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "source_maintenance_disposition_record_digest": source.get("future_only_maintenance_disposition_record_digest"),
        "source_policy_activation_review_handoff_envelope_digest": source.get("policy_activation_review_handoff_envelope_digest"),
        "world_candidate_fact_digest": evidence.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": evidence.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": evidence.get("resulting_world_state_digest"),
        "resulting_world_revision": evidence.get("resulting_world_revision"),
        "future_only_learning_delta_digest": evidence.get("future_only_learning_delta_digest"),
        "maintenance_policy_candidate_digest": evidence.get("maintenance_policy_candidate_digest"),
    }, "policy_activation_review_certificate", blockers)
    return digest, _duration(review, "review_started_epoch", "review_completed_epoch", "maximum_review_duration")

def _verify_context(context: dict, expected: str, source: dict, evidence: dict, review: dict, epoch: int, blockers: list[str]):
    if not context:
        blockers.append("future_only_policy_activation_review_context_missing"); return "", {}
    if set(context) != CONTEXT_FIELDS: blockers.append("future_only_policy_activation_review_context_schema_invalid")
    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if digest != compute_future_only_policy_activation_review_intake_context_digest(context): blockers.append("future_only_policy_activation_review_context_digest_mismatch")
    if digest != expected: blockers.append("future_only_policy_activation_review_context_expected_binding_mismatch")
    _exact(context, {
        "source_learnos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "source_maintenance_disposition_epoch": epoch,
    }, "policy_activation_review_context", blockers)
    if context.get("requested_policy_activation_review_operation_digest") != compute_requested_policy_activation_review_operation_digest(source, evidence, review):
        blockers.append("requested_policy_activation_review_operation_digest_mismatch")
    if context.get("exact_policy_activation_review_cycle_digest") != compute_exact_policy_activation_review_cycle_digest(source, evidence, review, context):
        blockers.append("exact_policy_activation_review_cycle_digest_mismatch")
    prior = (
        "prior_policy_activation_review_intake_session_ids",
        "prior_policy_activation_review_evidence_packet_digests",
        "prior_policy_activation_review_certificate_digests",
        "prior_policy_activation_review_intake_nonce_digests",
        "prior_policy_activation_review_source_receipt_digests",
    )
    for f in prior:
        if not _strings(context.get(f), True)[0]: blockers.append(f"{f}_invalid")
    world = all((
        context.get("current_world_model_state_digest") == source.get("resulting_world_state_digest"),
        context.get("current_world_model_revision") == source.get("resulting_world_revision"),
        context.get("current_future_only_learning_delta_digest") == source.get("future_only_learning_delta_digest"),
        context.get("current_maintenance_policy_candidate_digest") == source.get("maintenance_policy_candidate_digest"),
        context.get("current_maintenance_disposition_record_digest") == source.get("future_only_maintenance_disposition_record_digest"),
    ))
    i, m = context.get("policy_activation_review_intake_epoch"), context.get("maximum_policy_activation_review_intake_delay")
    current = all(isinstance(x, int) and not isinstance(x, bool) for x in (i, m)) and epoch <= i and 0 <= i - epoch <= m
    replay = any((
        context.get("policy_activation_review_intake_session_id") in context.get(prior[0], []),
        evidence.get(EVIDENCE_DIGEST_FIELD) in context.get(prior[1], []),
        review.get(REVIEW_DIGEST_FIELD) in context.get(prior[2], []),
        context.get("policy_activation_review_intake_nonce_digest") in context.get(prior[3], []),
        source.get(SOURCE_RECEIPT_DIGEST_FIELD) in context.get(prior[4], []),
    ))
    return digest, {"world_current": world, "context_current": current, "replay": replay}

def _route(evidence: Mapping[str, Any], review: Mapping[str, Any], checks: Mapping[str, bool], ecur: bool, rcur: bool) -> str:
    if checks.get("replay"): return DISPOSITION_REPLAY_REJECTED
    if not checks.get("world_current"): return DISPOSITION_WORLD_REFRESH
    if not checks.get("context_current"): return DISPOSITION_CONTEXT_REFRESH
    if not rcur: return DISPOSITION_REVIEW_REFRESH
    if not ecur or not evidence.get("independent_policy_activation_review_evidence") or not evidence.get("exactly_one_policy_activation_review"):
        return DISPOSITION_ADDITIONAL_EVIDENCE
    routes = (
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
    for f, d in routes:
        if not review.get(f): return d
    if not review.get("protected_group_nonexternalization_supported") or not review.get("future_nonexternalization_supported"):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if any(evidence.get(f) for f in (
        "maintenance_policy_candidate_activated", "maintenance_monitoring_activated",
        "maintenance_action_performed", "current_world_mutation_performed",
        "current_plan_revised", "current_policy_activated", "learning_delta_activated",
        "activation_authorization_granted",
    )) or not review.get("no_current_state_mutation") or not review.get("no_policy_activation") or not review.get("no_activation_authorization_granted") or not review.get("no_maintenance_action_performed"):
        return DISPOSITION_CURRENT_STATE_MUTATION_REJECTED
    if evidence.get("generalized_benefit_claimed") or evidence.get("authority_escalation_claimed") or not review.get("no_authority_escalation"):
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED
    return DISPOSITION_SUPPORTED

def build_verifyos_dukkha_preserving_future_only_policy_activation_review_intake(
    *, source_learnos_receipt: Mapping[str, Any],
    expected_source_learnos_receipt_digest: str,
    future_only_policy_activation_review_evidence_packet: Mapping[str, Any],
    expected_future_only_policy_activation_review_evidence_packet_digest: str,
    future_only_policy_activation_review_certificate: Mapping[str, Any],
    expected_future_only_policy_activation_review_certificate_digest: str,
    future_only_policy_activation_review_intake_context: Mapping[str, Any],
    expected_future_only_policy_activation_review_intake_context_digest: str,
    future_only_policy_activation_review_policy_digest: str,
    verifyos_policy_review_responsibility_digest: str,
    future_only_policy_activation_review_request_id: str,
    future_only_policy_activation_review_bundle_digest: str,
) -> VerifyOSFutureOnlyPolicyActivationReviewResult:
    source, evidence, review, context = map(_map, (
        source_learnos_receipt, future_only_policy_activation_review_evidence_packet,
        future_only_policy_activation_review_certificate,
        future_only_policy_activation_review_intake_context,
    ))
    blockers: list[str] = []
    sd, record, handoff, epoch, sline, sresp = _verify_source(source, expected_source_learnos_receipt_digest, blockers)
    ed, ecur, artifacts, provenance = _verify_evidence(evidence, expected_future_only_policy_activation_review_evidence_packet_digest, source, record, handoff, blockers)
    rd, rcur = _verify_review(review, expected_future_only_policy_activation_review_certificate_digest, source, evidence, blockers)
    cd, checks = _verify_context(context, expected_future_only_policy_activation_review_intake_context_digest, source, evidence, review, epoch, blockers)
    if not blockers:
        bundle = compute_future_only_policy_activation_review_bundle_digest(
            source_learnos_receipt_digest=sd,
            expected_source_learnos_receipt_digest=expected_source_learnos_receipt_digest,
            source_maintenance_disposition_record_digest=source.get("future_only_maintenance_disposition_record_digest"),
            source_policy_activation_review_handoff_envelope_digest=source.get("policy_activation_review_handoff_envelope_digest"),
            future_only_policy_activation_review_evidence_packet_digest=ed,
            expected_future_only_policy_activation_review_evidence_packet_digest=expected_future_only_policy_activation_review_evidence_packet_digest,
            future_only_policy_activation_review_certificate_digest=rd,
            expected_future_only_policy_activation_review_certificate_digest=expected_future_only_policy_activation_review_certificate_digest,
            future_only_policy_activation_review_intake_context_digest=cd,
            expected_future_only_policy_activation_review_intake_context_digest=expected_future_only_policy_activation_review_intake_context_digest,
            requested_policy_activation_review_operation_digest=context.get("requested_policy_activation_review_operation_digest"),
            exact_policy_activation_review_cycle_digest=context.get("exact_policy_activation_review_cycle_digest"),
            future_only_policy_activation_review_policy_digest=future_only_policy_activation_review_policy_digest,
            verifyos_policy_review_responsibility_digest=verifyos_policy_review_responsibility_digest,
            future_only_policy_activation_review_request_id=future_only_policy_activation_review_request_id,
        )
        if bundle != future_only_policy_activation_review_bundle_digest:
            blockers.append("future_only_policy_activation_review_bundle_digest_mismatch")
    if blockers:
        return VerifyOSFutureOnlyPolicyActivationReviewResult(STATUS_BLOCKED, sorted(set(blockers)), None)
    disposition = _route(evidence, review, checks, ecur, rcur)
    supported = disposition == DISPOSITION_SUPPORTED
    state_after = STATE_AFTER_SUPPORTED if supported else STATE_BEFORE
    review_record = {
        "source_learnos_receipt_digest": sd, EVIDENCE_DIGEST_FIELD: ed, REVIEW_DIGEST_FIELD: rd,
        "source_maintenance_disposition_record_digest": source["future_only_maintenance_disposition_record_digest"],
        "source_policy_activation_review_handoff_envelope_digest": source["policy_activation_review_handoff_envelope_digest"],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": evidence["maintenance_policy_candidate_digest"],
        "proposed_activation_scope_digest": evidence["proposed_activation_scope_digest"],
        "activation_precondition_set_digest": evidence["activation_precondition_set_digest"],
        "bounded_subject_scope_digest": evidence["bounded_subject_scope_digest"],
        "activation_duration_limit_digest": evidence["activation_duration_limit_digest"],
        "rollback_plan_digest": evidence["rollback_plan_digest"],
        "post_activation_monitoring_guard_digest": evidence["post_activation_monitoring_guard_digest"],
        "policy_activation_review_intake_session_id": context["policy_activation_review_intake_session_id"],
        "policy_activation_review_intake_nonce_digest": context["policy_activation_review_intake_nonce_digest"],
        "policy_activation_review_intake_epoch": context["policy_activation_review_intake_epoch"],
        "disposition": disposition,
        "bounded_review_outcome": "eligible_for_independent_activation_authorization_review" if supported else "policy_activation_review_not_supported",
        "state_before": STATE_BEFORE, "state_after": state_after,
    }
    review_record_digest = canonical_digest(review_record)
    debt = {
        "source_learnos_receipt_digest": sd,
        "policy_activation_review_record_digest": review_record_digest,
        "policy_activation_review_debt_consumed": supported,
        "source_policy_activation_review_handoff_consumed": supported,
        "double_policy_activation_review_performed": False,
    }
    debt_digest = canonical_digest(debt)
    authorization_handoff = None
    authorization_handoff_digest = ""
    if supported:
        authorization_handoff = {
            "source_learnos_receipt_digest": sd, EVIDENCE_DIGEST_FIELD: ed, REVIEW_DIGEST_FIELD: rd,
            "policy_activation_review_record_digest": review_record_digest,
            "policy_activation_review_debt_consumption_record_digest": debt_digest,
            "source_maintenance_disposition_record_digest": source["future_only_maintenance_disposition_record_digest"],
            "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
            "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
            "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"],
            "maintenance_policy_candidate_digest": evidence["maintenance_policy_candidate_digest"],
            "policy_activation_review_state": "reviewed_pending_activation_authorization",
            "activation_authorization_state": "authorization_debt_open",
            "future_only": True, "active_now": False,
            "maintenance_policy_candidate_activated": False,
            "maintenance_monitoring_activated": False,
            "current_policy_activated": False, "maintenance_action_performed": False,
            "activation_authorization_granted": False,
            "automatic_policy_activation": False, "automatic_maintenance_action": False,
        }
        authorization_handoff_digest = canonical_digest(authorization_handoff)
    lineage = sorted(set(sline) | set(artifacts) | set(provenance) | {
        sd, ed, rd, cd, context["requested_policy_activation_review_operation_digest"],
        context["exact_policy_activation_review_cycle_digest"], review_record_digest,
        debt_digest, future_only_policy_activation_review_bundle_digest,
    } | ({authorization_handoff_digest} if authorization_handoff_digest else set()))
    responsibility = sorted(set(sresp) | {
        evidence["review_assessor_id"], evidence["evidence_source_id"],
        review["reviewer_id"], verifyos_policy_review_responsibility_digest,
    })
    receipt = {
        "kernel": "VerifyOS Dukkha-Preserving Future-Only Policy Activation Review Intake Kernel",
        "kernel_version": "v0.1", "verifyos_version": "v0.12",
        "status": "VERIFYOS_DUKKHA_PRESERVING_FUTURE_ONLY_POLICY_ACTIVATION_REVIEW_ROUTED",
        "source_learnos_receipt": source, "source_learnos_receipt_digest": sd,
        "source_maintenance_disposition_evidence_packet_digest": source[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_maintenance_disposition_review_certificate_digest": source[SOURCE_REVIEW_DIGEST_FIELD],
        "source_maintenance_disposition_intake_context_digest": source[SOURCE_CONTEXT_DIGEST_FIELD],
        "source_maintenance_disposition_record_digest": source["future_only_maintenance_disposition_record_digest"],
        "source_maintenance_disposition_debt_consumption_record_digest": source["future_only_maintenance_disposition_debt_consumption_record_digest"],
        "source_policy_activation_review_handoff_envelope_digest": source["policy_activation_review_handoff_envelope_digest"],
        "future_only_policy_activation_review_evidence_packet": evidence, EVIDENCE_DIGEST_FIELD: ed,
        "future_only_policy_activation_review_certificate": review, REVIEW_DIGEST_FIELD: rd,
        CONTEXT_DIGEST_FIELD: cd,
        "future_only_policy_activation_review_policy_digest": future_only_policy_activation_review_policy_digest,
        "verifyos_policy_review_responsibility_digest": verifyos_policy_review_responsibility_digest,
        "future_only_policy_activation_review_request_id": future_only_policy_activation_review_request_id,
        "future_only_policy_activation_review_bundle_digest": future_only_policy_activation_review_bundle_digest,
        "future_only_policy_activation_review_disposition": disposition,
        "future_only_policy_activation_review_state_before": STATE_BEFORE,
        "future_only_policy_activation_review_state_after": state_after,
        "future_only_policy_activation_review_record": review_record,
        "future_only_policy_activation_review_record_digest": review_record_digest,
        "future_only_policy_activation_review_debt_consumption_record": debt,
        "future_only_policy_activation_review_debt_consumption_record_digest": debt_digest,
        "activation_authorization_handoff_envelope": authorization_handoff,
        "activation_authorization_handoff_envelope_digest": authorization_handoff_digest,
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "future_only_learning_delta_digest": evidence["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": evidence["maintenance_policy_candidate_digest"],
        "source_learnos_receipt_supplied": True, "source_learnos_receipt_fully_revalidated": True,
        "world_fact_confirmed": True, "causal_attribution_confirmed": True,
        "dukkha_reduction_realized_confirmed": True,
        "future_only_learning_delta_recorded": True, "future_only_learning_delta_activated": False,
        "maintenance_monitoring_observation_recorded": True,
        "maintenance_monitoring_observation_verified": True,
        "maintenance_monitoring_verification_completed": True,
        "future_only_maintenance_disposition_recorded": True,
        "future_only_maintenance_disposition_completed": True,
        "policy_activation_review_supported": supported,
        "policy_activation_review_recorded": supported,
        "policy_activation_review_scope_exactly_bounded": supported,
        "policy_activation_review_completed": supported,
        "policy_activation_review_debt_consumed": supported,
        "policy_activation_review_debt_open": not supported,
        "policy_activation_review_replay_closed": supported,
        "source_learnos_receipt_replay_closed": supported,
        "policy_activation_review_evidence_replay_closed": supported,
        "policy_activation_review_certificate_replay_closed": supported,
        "policy_activation_review_nonce_consumed": supported,
        "policy_activation_review_nonce_replay_closed": supported,
        "policy_activation_review_session_replay_closed": supported,
        "source_policy_activation_review_handoff_consumed": supported,
        "activation_authorization_handoff_prepared": supported,
        "activation_authorization_completed": False,
        "activation_authorization_debt_open": supported,
        "maintenance_policy_candidate_retained_future_only": True,
        "maintenance_policy_candidate_activated": False,
        "maintenance_monitoring_activated": False, "current_policy_activated": False,
        "maintenance_action_performed": False, "activation_authorization_granted": False,
        "review_evidence_collection_performed_by_kernel": False,
        "maintenance_disposition_reperformed_by_kernel": False,
        "persistent_world_state_changed_by_review": False,
        "world_model_revision_incremented_by_review": False,
        "current_plan_revised_by_review": False,
        "current_policy_activated_by_review": False,
        "learning_delta_activated_by_review": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "automatic_truth_generalization": False, "automatic_causal_attribution": False,
        "automatic_dukkha_realization_confirmation": False, "automatic_learning_update": False,
        "automatic_policy_activation": False, "automatic_maintenance_action": False,
        "automatic_plan_completion": False, "automatic_rollback": False,
        "automatic_compensation": False, "generalized_benefit_claimed": False,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False,
        "dukkha_minimization_authority_granted_to_verifyos": False,
        "general_execution_authority_granted": False, "execution_permission": False,
        "world_mutation_authority_granted": False,
        "current_policy_activation_authority_granted": False,
        "activation_authorization_authority_granted_to_verifyos": False,
        "maintenance_action_authority_granted_to_verifyos": False,
        "evidence_lineage_preserved": True, "responsibility_lineage_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "history_read_only": True, "future_only": True, "active_now": False,
        "resulting_lineage_digests": lineage,
        "resulting_responsibility_lineage_digests": responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return VerifyOSFutureOnlyPolicyActivationReviewResult(STATUS_READY, [], receipt)
