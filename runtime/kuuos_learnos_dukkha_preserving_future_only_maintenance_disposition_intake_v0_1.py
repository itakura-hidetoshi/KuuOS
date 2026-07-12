#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD as SOURCE_CONTEXT_DIGEST_FIELD,
    DISPOSITION_SUPPORTED as SOURCE_DISPOSITION_SUPPORTED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    STATE_AFTER_SUPPORTED as SOURCE_STATE_AFTER_SUPPORTED,
    canonical_digest,
    compute_maintenance_monitoring_verification_evidence_packet_digest,
    compute_maintenance_monitoring_verification_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "learnos_dukkha_preserving_future_only_maintenance_disposition_intake_receipt_digest"
EVIDENCE_DIGEST_FIELD = "future_only_maintenance_disposition_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "future_only_maintenance_disposition_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "future_only_maintenance_disposition_intake_context_digest"
STATE_BEFORE = SOURCE_STATE_AFTER_SUPPORTED
STATE_AFTER_SUPPORTED = STATE_BEFORE + "_future_only_maintenance_disposition_recorded_policy_activation_review_pending"

DISPOSITION_SUPPORTED = "future_only_maintenance_disposition_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "maintenance_disposition_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "maintenance_disposition_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_maintenance_disposition_evidence_required"
DISPOSITION_SOURCE_REPAIR = "source_verifyos_receipt_correspondence_repair_required"
DISPOSITION_VERIFICATION_RECORD_REPAIR = "monitoring_verification_record_correspondence_repair_required"
DISPOSITION_HANDOFF_REPAIR = "maintenance_disposition_handoff_correspondence_repair_required"
DISPOSITION_CANDIDATE_REPAIR = "maintenance_policy_candidate_correspondence_repair_required"
DISPOSITION_OBJECTIVE_REPAIR = "maintenance_objective_repair_required"
DISPOSITION_NOOP_THRESHOLD_REPAIR = "maintenance_noop_threshold_repair_required"
DISPOSITION_ESCALATION_TRIGGER_REPAIR = "maintenance_escalation_trigger_repair_required"
DISPOSITION_REOBSERVATION_SCHEDULE_REPAIR = "reobservation_schedule_repair_required"
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = "current_state_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

@dataclass
class LearnOSFutureOnlyMaintenanceDispositionResult:
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
    return all(isinstance(n, int) and not isinstance(n, bool) for n in (x, y, z)) and 0 <= x <= y and y - x <= z

def compute_future_only_maintenance_disposition_evidence_packet_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, EVIDENCE_DIGEST_FIELD)

def compute_future_only_maintenance_disposition_review_certificate_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, REVIEW_DIGEST_FIELD)

def compute_future_only_maintenance_disposition_intake_context_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, CONTEXT_DIGEST_FIELD)

def compute_requested_maintenance_disposition_operation_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_verifyos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        "source_monitoring_verification_record_digest": source.get("maintenance_monitoring_verification_record_digest"),
        "source_maintenance_disposition_handoff_envelope_digest": source.get("maintenance_disposition_handoff_envelope_digest"),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD), REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER_SUPPORTED,
    })

def compute_exact_maintenance_disposition_cycle_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_verifyos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD), EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD), REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "maintenance_disposition_intake_session_id": context.get("maintenance_disposition_intake_session_id"),
        "maintenance_disposition_intake_nonce_digest": context.get("maintenance_disposition_intake_nonce_digest"),
        "maintenance_disposition_intake_epoch": context.get("maintenance_disposition_intake_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_maintenance_disposition_operation_digest": context.get("requested_maintenance_disposition_operation_digest"),
    })

def compute_future_only_maintenance_disposition_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)

def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_verifyos_receipt_missing"); return "", {}, {}, 0, [], []
    _exact(source, {
        "kernel": "VerifyOS Dukkha-Preserving Future-Only Maintenance-Monitoring Observation Verification Intake Kernel",
        "kernel_version": "v0.1", "verifyos_version": "v0.11",
        "status": "VERIFYOS_DUKKHA_PRESERVING_FUTURE_ONLY_MAINTENANCE_MONITORING_OBSERVATION_VERIFICATION_ROUTED",
        "maintenance_monitoring_verification_disposition": SOURCE_DISPOSITION_SUPPORTED,
        "maintenance_monitoring_verification_state_after": STATE_BEFORE,
        "world_fact_confirmed": True, "causal_attribution_confirmed": True, "dukkha_reduction_realized_confirmed": True,
        "future_only_learning_delta_recorded": True, "future_only_learning_delta_activated": False,
        "maintenance_monitoring_observation_recorded": True, "maintenance_monitoring_observation_verified": True,
        "maintenance_monitoring_verification_completed": True, "maintenance_monitoring_verification_debt_open": False,
        "maintenance_disposition_handoff_prepared": True, "maintenance_disposition_completed": False,
        "maintenance_disposition_debt_open": True, "maintenance_monitoring_activated": False,
        "maintenance_action_performed": False, "persistent_world_state_changed_by_verification": False,
        "world_model_revision_incremented_by_verification": False, "current_plan_revised_by_verification": False,
        "current_policy_activated_by_verification": False, "learning_delta_activated_by_verification": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "history_read_only": True, "future_only": True, "active_now": False,
    }, "source", blockers)
    digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    if digest != _digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD): blockers.append("source_verifyos_receipt_digest_mismatch")
    if digest != expected: blockers.append("source_verifyos_expected_binding_mismatch")
    ev = _map(source.get("maintenance_monitoring_verification_evidence_packet"))
    rv = _map(source.get("maintenance_monitoring_verification_review_certificate"))
    record = _map(source.get("maintenance_monitoring_verification_record"))
    debt = _map(source.get("maintenance_monitoring_verification_debt_consumption_record"))
    handoff = _map(source.get("maintenance_disposition_handoff_envelope"))
    if source.get(SOURCE_EVIDENCE_DIGEST_FIELD) != compute_maintenance_monitoring_verification_evidence_packet_digest(ev): blockers.append("source_monitoring_verification_evidence_digest_mismatch")
    if source.get(SOURCE_REVIEW_DIGEST_FIELD) != compute_maintenance_monitoring_verification_review_certificate_digest(rv): blockers.append("source_monitoring_verification_review_digest_mismatch")
    for item, field in ((record,"maintenance_monitoring_verification_record_digest"),(debt,"maintenance_monitoring_verification_debt_consumption_record_digest"),(handoff,"maintenance_disposition_handoff_envelope_digest")):
        if not item or source.get(field) != canonical_digest(item): blockers.append(f"source_{field}_mismatch")
    _exact(record, {
        "source_observeos_receipt_digest": source.get("source_observeos_receipt_digest"), SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD), SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "source_maintenance_monitoring_observation_record_digest": source.get("source_maintenance_monitoring_observation_record_digest"),
        "source_maintenance_monitoring_verification_handoff_envelope_digest": source.get("source_maintenance_monitoring_verification_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"), "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("resulting_world_state_digest"), "resulting_world_revision": source.get("resulting_world_revision"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"), "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "disposition": SOURCE_DISPOSITION_SUPPORTED, "state_after": STATE_BEFORE,
    }, "source_monitoring_verification_record", blockers)
    _exact(debt, {"source_observeos_receipt_digest": source.get("source_observeos_receipt_digest"), "verification_record_digest": source.get("maintenance_monitoring_verification_record_digest"), "verification_debt_consumed": True, "source_verification_handoff_consumed": True, "double_verification_performed": False}, "source_monitoring_verification_debt", blockers)
    _exact(handoff, {
        "source_observeos_receipt_digest": source.get("source_observeos_receipt_digest"), SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD), SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
        "verification_record_digest": source.get("maintenance_monitoring_verification_record_digest"), "verification_debt_consumption_record_digest": source.get("maintenance_monitoring_verification_debt_consumption_record_digest"),
        "source_maintenance_monitoring_observation_record_digest": source.get("source_maintenance_monitoring_observation_record_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"), "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"), "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "monitoring_verification_state": "verified_pending_maintenance_disposition", "maintenance_disposition_state": "disposition_debt_open",
        "future_only": True, "active_now": False, "maintenance_monitoring_activated": False, "maintenance_action_performed": False,
        "current_policy_activated": False, "automatic_maintenance_action": False,
    }, "source_maintenance_disposition_handoff", blockers)
    lok, lineage = _strings(source.get("resulting_lineage_digests")); rok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lok: blockers.append("source_resulting_lineage_invalid")
    if not rok: blockers.append("source_resulting_responsibility_invalid")
    epoch = record.get("monitoring_verification_intake_epoch", 0)
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0: blockers.append("source_monitoring_verification_epoch_invalid"); epoch = 0
    return digest, record, handoff, epoch, lineage, responsibility

def _verify_evidence(evidence: dict, expected: str, source: dict, record: dict, handoff: dict, blockers: list[str]):
    if not evidence:
        blockers.append("future_only_maintenance_disposition_evidence_missing"); return "", False, [], []
    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if digest != compute_future_only_maintenance_disposition_evidence_packet_digest(evidence): blockers.append("future_only_maintenance_disposition_evidence_digest_mismatch")
    if digest != expected: blockers.append("future_only_maintenance_disposition_evidence_expected_binding_mismatch")
    _exact(evidence, {
        "source_verifyos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD), "source_monitoring_verification_evidence_packet_digest": source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        "source_monitoring_verification_review_certificate_digest": source.get(SOURCE_REVIEW_DIGEST_FIELD), "source_monitoring_verification_record_digest": source.get("maintenance_monitoring_verification_record_digest"),
        "source_monitoring_verification_debt_consumption_record_digest": source.get("maintenance_monitoring_verification_debt_consumption_record_digest"),
        "source_maintenance_disposition_handoff_envelope_digest": source.get("maintenance_disposition_handoff_envelope_digest"),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"), "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("resulting_world_state_digest"), "resulting_world_revision": source.get("resulting_world_revision"),
        "future_only_learning_delta_digest": source.get("future_only_learning_delta_digest"), "maintenance_policy_candidate_digest": source.get("maintenance_policy_candidate_digest"),
        "source_monitoring_observation_record_digest": source.get("source_maintenance_monitoring_observation_record_digest"),
        "verified_baseline_observation_digest": record.get("baseline_observation_digest"), "verified_durability_digest": record.get("durability_verification_digest"),
        "verified_adverse_effect_digest": record.get("adverse_effect_verification_digest"), "verified_distributional_digest": record.get("distributional_verification_digest"),
    }, "maintenance_disposition_evidence", blockers)
    if handoff.get("maintenance_policy_candidate_digest") != evidence.get("maintenance_policy_candidate_digest"): blockers.append("maintenance_disposition_handoff_candidate_mismatch")
    aok, artifacts = _strings(evidence.get("maintenance_disposition_artifact_digests")); pok, provenance = _strings(evidence.get("provenance_chain_digests"))
    if not aok: blockers.append("maintenance_disposition_artifacts_invalid")
    if not pok: blockers.append("maintenance_disposition_provenance_invalid")
    return digest, _duration(evidence,"assessment_started_epoch","assessment_completed_epoch","maximum_assessment_duration"), artifacts, provenance

def _verify_review(review: dict, expected: str, source: dict, evidence: dict, blockers: list[str]):
    if not review:
        blockers.append("future_only_maintenance_disposition_review_missing"); return "", False
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if digest != compute_future_only_maintenance_disposition_review_certificate_digest(review): blockers.append("future_only_maintenance_disposition_review_digest_mismatch")
    if digest != expected: blockers.append("future_only_maintenance_disposition_review_expected_binding_mismatch")
    _exact(review, {"source_verifyos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD), EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD), "source_monitoring_verification_record_digest": source.get("maintenance_monitoring_verification_record_digest"), "source_maintenance_disposition_handoff_envelope_digest": source.get("maintenance_disposition_handoff_envelope_digest"), "world_candidate_fact_digest": evidence.get("world_candidate_fact_digest"), "world_candidate_relation_digest": evidence.get("world_candidate_relation_digest"), "resulting_world_state_digest": evidence.get("resulting_world_state_digest"), "resulting_world_revision": evidence.get("resulting_world_revision"), "future_only_learning_delta_digest": evidence.get("future_only_learning_delta_digest"), "maintenance_policy_candidate_digest": evidence.get("maintenance_policy_candidate_digest")}, "maintenance_disposition_review", blockers)
    return digest, _duration(review,"review_started_epoch","review_completed_epoch","maximum_review_duration")

def _verify_context(context: dict, expected: str, source: dict, evidence: dict, review: dict, epoch: int, blockers: list[str]):
    if not context:
        blockers.append("future_only_maintenance_disposition_context_missing"); return "", {}
    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if digest != compute_future_only_maintenance_disposition_intake_context_digest(context): blockers.append("future_only_maintenance_disposition_context_digest_mismatch")
    if digest != expected: blockers.append("future_only_maintenance_disposition_context_expected_binding_mismatch")
    _exact(context, {"source_verifyos_receipt_digest": source.get(SOURCE_RECEIPT_DIGEST_FIELD), EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD), REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD), "source_monitoring_verification_epoch": epoch}, "maintenance_disposition_context", blockers)
    if context.get("requested_maintenance_disposition_operation_digest") != compute_requested_maintenance_disposition_operation_digest(source,evidence,review): blockers.append("requested_maintenance_disposition_operation_digest_mismatch")
    if context.get("exact_maintenance_disposition_cycle_digest") != compute_exact_maintenance_disposition_cycle_digest(source,evidence,review,context): blockers.append("exact_maintenance_disposition_cycle_digest_mismatch")
    prior = ("prior_maintenance_disposition_intake_session_ids","prior_maintenance_disposition_evidence_packet_digests","prior_maintenance_disposition_review_certificate_digests","prior_maintenance_disposition_intake_nonce_digests","prior_maintenance_disposition_source_receipt_digests")
    for f in prior:
        if not _strings(context.get(f), True)[0]: blockers.append(f"{f}_invalid")
    world = context.get("current_world_model_state_digest") == source.get("resulting_world_state_digest") and context.get("current_world_model_revision") == source.get("resulting_world_revision") and context.get("current_future_only_learning_delta_digest") == source.get("future_only_learning_delta_digest") and context.get("current_maintenance_policy_candidate_digest") == source.get("maintenance_policy_candidate_digest")
    i, m = context.get("maintenance_disposition_intake_epoch"), context.get("maximum_maintenance_disposition_intake_delay")
    current = all(isinstance(x,int) and not isinstance(x,bool) for x in (i,m)) and epoch <= i and 0 <= i-epoch <= m
    replay = context.get("maintenance_disposition_intake_session_id") in context.get(prior[0],[]) or evidence.get(EVIDENCE_DIGEST_FIELD) in context.get(prior[1],[]) or review.get(REVIEW_DIGEST_FIELD) in context.get(prior[2],[]) or context.get("maintenance_disposition_intake_nonce_digest") in context.get(prior[3],[]) or source.get(SOURCE_RECEIPT_DIGEST_FIELD) in context.get(prior[4],[])
    return digest, {"world_current":world,"context_current":current,"replay":replay}

def _route(evidence: Mapping[str,Any], review: Mapping[str,Any], checks: Mapping[str,bool], ecur: bool, rcur: bool) -> str:
    if checks.get("replay"): return DISPOSITION_REPLAY_REJECTED
    if not checks.get("world_current"): return DISPOSITION_WORLD_REFRESH
    if not checks.get("context_current"): return DISPOSITION_CONTEXT_REFRESH
    if not rcur: return DISPOSITION_REVIEW_REFRESH
    if not ecur or not evidence.get("independent_future_only_maintenance_disposition_evidence") or not evidence.get("exactly_one_maintenance_disposition_assessment"): return DISPOSITION_ADDITIONAL_EVIDENCE
    routes = (("source_receipt_correspondence_confirmed",DISPOSITION_SOURCE_REPAIR),("monitoring_verification_record_correspondence_confirmed",DISPOSITION_VERIFICATION_RECORD_REPAIR),("maintenance_disposition_handoff_correspondence_confirmed",DISPOSITION_HANDOFF_REPAIR),("maintenance_policy_candidate_correspondence_confirmed",DISPOSITION_CANDIDATE_REPAIR),("maintenance_objective_adequate",DISPOSITION_OBJECTIVE_REPAIR),("maintenance_noop_threshold_adequate",DISPOSITION_NOOP_THRESHOLD_REPAIR),("maintenance_escalation_trigger_adequate",DISPOSITION_ESCALATION_TRIGGER_REPAIR),("reobservation_schedule_adequate",DISPOSITION_REOBSERVATION_SCHEDULE_REPAIR),("uncertainty_adequate",DISPOSITION_UNCERTAINTY_REPAIR),("calibration_adequate",DISPOSITION_CALIBRATION_REPAIR),("provenance_continuity_preserved",DISPOSITION_PROVENANCE_REPAIR))
    for f,d in routes:
        if not review.get(f): return d
    if not review.get("protected_group_nonexternalization_supported") or not review.get("future_nonexternalization_supported"): return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if any(evidence.get(f) for f in ("maintenance_policy_candidate_activated","maintenance_monitoring_activated","maintenance_action_performed","current_world_mutation_performed","current_plan_revised","current_policy_activated","learning_delta_activated")) or not review.get("no_current_state_mutation") or not review.get("no_policy_activation") or not review.get("no_maintenance_action_performed"): return DISPOSITION_CURRENT_STATE_MUTATION_REJECTED
    if evidence.get("generalized_benefit_claimed") or evidence.get("authority_escalation_claimed") or not review.get("no_authority_escalation"): return DISPOSITION_AUTHORITY_ESCALATION_REJECTED
    return DISPOSITION_SUPPORTED

def build_learnos_dukkha_preserving_future_only_maintenance_disposition_intake(*, source_verifyos_receipt: Mapping[str,Any], expected_source_verifyos_receipt_digest: str, future_only_maintenance_disposition_evidence_packet: Mapping[str,Any], expected_future_only_maintenance_disposition_evidence_packet_digest: str, future_only_maintenance_disposition_review_certificate: Mapping[str,Any], expected_future_only_maintenance_disposition_review_certificate_digest: str, future_only_maintenance_disposition_intake_context: Mapping[str,Any], expected_future_only_maintenance_disposition_intake_context_digest: str, future_only_maintenance_disposition_policy_digest: str, learnos_maintenance_responsibility_digest: str, future_only_maintenance_disposition_request_id: str, future_only_maintenance_disposition_bundle_digest: str) -> LearnOSFutureOnlyMaintenanceDispositionResult:
    source,evidence,review,context = map(_map,(source_verifyos_receipt,future_only_maintenance_disposition_evidence_packet,future_only_maintenance_disposition_review_certificate,future_only_maintenance_disposition_intake_context)); blockers=[]
    sd,record,handoff,epoch,sline,sresp = _verify_source(source,expected_source_verifyos_receipt_digest,blockers)
    ed,ecur,artifacts,prov = _verify_evidence(evidence,expected_future_only_maintenance_disposition_evidence_packet_digest,source,record,handoff,blockers)
    rd,rcur = _verify_review(review,expected_future_only_maintenance_disposition_review_certificate_digest,source,evidence,blockers)
    cd,checks = _verify_context(context,expected_future_only_maintenance_disposition_intake_context_digest,source,evidence,review,epoch,blockers)
    if not blockers:
        bundle = compute_future_only_maintenance_disposition_bundle_digest(source_verifyos_receipt_digest=sd,expected_source_verifyos_receipt_digest=expected_source_verifyos_receipt_digest,source_monitoring_verification_record_digest=source.get("maintenance_monitoring_verification_record_digest"),source_maintenance_disposition_handoff_envelope_digest=source.get("maintenance_disposition_handoff_envelope_digest"),future_only_maintenance_disposition_evidence_packet_digest=ed,expected_future_only_maintenance_disposition_evidence_packet_digest=expected_future_only_maintenance_disposition_evidence_packet_digest,future_only_maintenance_disposition_review_certificate_digest=rd,expected_future_only_maintenance_disposition_review_certificate_digest=expected_future_only_maintenance_disposition_review_certificate_digest,future_only_maintenance_disposition_intake_context_digest=cd,expected_future_only_maintenance_disposition_intake_context_digest=expected_future_only_maintenance_disposition_intake_context_digest,requested_maintenance_disposition_operation_digest=context.get("requested_maintenance_disposition_operation_digest"),exact_maintenance_disposition_cycle_digest=context.get("exact_maintenance_disposition_cycle_digest"),future_only_maintenance_disposition_policy_digest=future_only_maintenance_disposition_policy_digest,learnos_maintenance_responsibility_digest=learnos_maintenance_responsibility_digest,future_only_maintenance_disposition_request_id=future_only_maintenance_disposition_request_id)
        if bundle != future_only_maintenance_disposition_bundle_digest: blockers.append("future_only_maintenance_disposition_bundle_digest_mismatch")
    if blockers: return LearnOSFutureOnlyMaintenanceDispositionResult(STATUS_BLOCKED,sorted(set(blockers)),None)
    disposition = _route(evidence,review,checks,ecur,rcur); supported = disposition == DISPOSITION_SUPPORTED; state_after = STATE_AFTER_SUPPORTED if supported else STATE_BEFORE
    drecord = {"source_verifyos_receipt_digest":sd,EVIDENCE_DIGEST_FIELD:ed,REVIEW_DIGEST_FIELD:rd,"source_monitoring_verification_record_digest":source["maintenance_monitoring_verification_record_digest"],"source_maintenance_disposition_handoff_envelope_digest":source["maintenance_disposition_handoff_envelope_digest"],"world_candidate_fact_digest":evidence["world_candidate_fact_digest"],"world_candidate_relation_digest":evidence["world_candidate_relation_digest"],"resulting_world_state_digest":evidence["resulting_world_state_digest"],"resulting_world_revision":evidence["resulting_world_revision"],"future_only_learning_delta_digest":evidence["future_only_learning_delta_digest"],"maintenance_policy_candidate_digest":evidence["maintenance_policy_candidate_digest"],"future_only_maintenance_objective_digest":evidence["future_only_maintenance_objective_digest"],"maintenance_noop_threshold_digest":evidence["maintenance_noop_threshold_digest"],"maintenance_escalation_trigger_digest":evidence["maintenance_escalation_trigger_digest"],"reobservation_schedule_digest":evidence["reobservation_schedule_digest"],"maintenance_disposition_intake_session_id":context["maintenance_disposition_intake_session_id"],"maintenance_disposition_intake_nonce_digest":context["maintenance_disposition_intake_nonce_digest"],"maintenance_disposition_intake_epoch":context["maintenance_disposition_intake_epoch"],"disposition":disposition,"bounded_maintenance_outcome":"retain_future_only_maintenance_candidate_pending_policy_activation_review" if supported else "no_future_only_maintenance_disposition_recorded","state_before":STATE_BEFORE,"state_after":state_after}
    drd = canonical_digest(drecord); debt={"source_verifyos_receipt_digest":sd,"maintenance_disposition_record_digest":drd,"maintenance_disposition_debt_consumed":supported,"source_maintenance_disposition_handoff_consumed":supported,"double_maintenance_disposition_performed":False}; debt_d=canonical_digest(debt)
    hand=None; hand_d=""
    if supported:
        hand={"source_verifyos_receipt_digest":sd,EVIDENCE_DIGEST_FIELD:ed,REVIEW_DIGEST_FIELD:rd,"maintenance_disposition_record_digest":drd,"maintenance_disposition_debt_consumption_record_digest":debt_d,"source_monitoring_verification_record_digest":source["maintenance_monitoring_verification_record_digest"],"world_candidate_fact_digest":evidence["world_candidate_fact_digest"],"world_candidate_relation_digest":evidence["world_candidate_relation_digest"],"future_only_learning_delta_digest":evidence["future_only_learning_delta_digest"],"maintenance_policy_candidate_digest":evidence["maintenance_policy_candidate_digest"],"maintenance_disposition_state":"future_only_disposition_recorded_pending_policy_activation_review","policy_activation_review_state":"review_debt_open","future_only":True,"active_now":False,"maintenance_monitoring_activated":False,"maintenance_policy_candidate_activated":False,"maintenance_action_performed":False,"current_policy_activated":False,"automatic_policy_activation":False,"automatic_maintenance_action":False}; hand_d=canonical_digest(hand)
    lineage=sorted(set(sline)|set(artifacts)|set(prov)|{sd,ed,rd,cd,context["requested_maintenance_disposition_operation_digest"],context["exact_maintenance_disposition_cycle_digest"],drd,debt_d,future_only_maintenance_disposition_bundle_digest}|({hand_d} if hand_d else set()))
    resp=sorted(set(sresp)|{evidence["assessor_id"],evidence["evidence_source_id"],review["reviewer_id"],learnos_maintenance_responsibility_digest})
    receipt={
        "kernel":"LearnOS Dukkha-Preserving Future-Only Maintenance Disposition Intake Kernel","kernel_version":"v0.1","learnos_version":"v0.5","status":"LEARNOS_DUKKHA_PRESERVING_FUTURE_ONLY_MAINTENANCE_DISPOSITION_ROUTED",
        "source_verifyos_receipt":source,"source_verifyos_receipt_digest":sd,"source_monitoring_verification_evidence_packet_digest":source[SOURCE_EVIDENCE_DIGEST_FIELD],"source_monitoring_verification_review_certificate_digest":source[SOURCE_REVIEW_DIGEST_FIELD],"source_monitoring_verification_intake_context_digest":source[SOURCE_CONTEXT_DIGEST_FIELD],"source_monitoring_verification_record_digest":source["maintenance_monitoring_verification_record_digest"],"source_monitoring_verification_debt_consumption_record_digest":source["maintenance_monitoring_verification_debt_consumption_record_digest"],"source_maintenance_disposition_handoff_envelope_digest":source["maintenance_disposition_handoff_envelope_digest"],
        "future_only_maintenance_disposition_evidence_packet":evidence,EVIDENCE_DIGEST_FIELD:ed,"future_only_maintenance_disposition_review_certificate":review,REVIEW_DIGEST_FIELD:rd,CONTEXT_DIGEST_FIELD:cd,"future_only_maintenance_disposition_policy_digest":future_only_maintenance_disposition_policy_digest,"learnos_maintenance_responsibility_digest":learnos_maintenance_responsibility_digest,"future_only_maintenance_disposition_request_id":future_only_maintenance_disposition_request_id,"future_only_maintenance_disposition_bundle_digest":future_only_maintenance_disposition_bundle_digest,
        "future_only_maintenance_disposition":disposition,"future_only_maintenance_disposition_state_before":STATE_BEFORE,"future_only_maintenance_disposition_state_after":state_after,"future_only_maintenance_disposition_record":drecord,"future_only_maintenance_disposition_record_digest":drd,"future_only_maintenance_disposition_debt_consumption_record":debt,"future_only_maintenance_disposition_debt_consumption_record_digest":debt_d,"policy_activation_review_handoff_envelope":hand,"policy_activation_review_handoff_envelope_digest":hand_d,
        "world_candidate_fact_digest":evidence["world_candidate_fact_digest"],"world_candidate_relation_digest":evidence["world_candidate_relation_digest"],"resulting_world_state_digest":evidence["resulting_world_state_digest"],"resulting_world_revision":evidence["resulting_world_revision"],"future_only_learning_delta_digest":evidence["future_only_learning_delta_digest"],"maintenance_policy_candidate_digest":evidence["maintenance_policy_candidate_digest"],
        "source_verifyos_receipt_supplied":True,"source_verifyos_receipt_fully_revalidated":True,"world_fact_confirmed":True,"causal_attribution_confirmed":True,"dukkha_reduction_realized_confirmed":True,"future_only_learning_delta_recorded":True,"future_only_learning_delta_activated":False,"maintenance_monitoring_observation_recorded":True,"maintenance_monitoring_observation_verified":True,"maintenance_monitoring_verification_completed":True,
        "future_only_maintenance_disposition_supported":supported,"future_only_maintenance_disposition_recorded":supported,"future_only_maintenance_disposition_scope_exactly_bounded":supported,"future_only_maintenance_disposition_completed":supported,"future_only_maintenance_disposition_debt_consumed":supported,"future_only_maintenance_disposition_debt_open":not supported,"future_only_maintenance_disposition_replay_closed":supported,"source_verifyos_receipt_replay_closed":supported,"maintenance_disposition_evidence_replay_closed":supported,"maintenance_disposition_review_replay_closed":supported,"maintenance_disposition_nonce_consumed":supported,"maintenance_disposition_nonce_replay_closed":supported,"maintenance_disposition_session_replay_closed":supported,"source_maintenance_disposition_handoff_consumed":supported,"policy_activation_review_handoff_prepared":supported,"policy_activation_review_completed":False,"policy_activation_review_debt_open":supported,"maintenance_policy_candidate_retained_future_only":supported,
        "maintenance_policy_candidate_activated":False,"maintenance_monitoring_activated":False,"maintenance_action_performed":False,"disposition_evidence_collection_performed_by_kernel":False,"monitoring_observation_reperformed_by_kernel":False,"monitoring_verification_reperformed_by_kernel":False,"persistent_world_state_changed_by_disposition":False,"world_model_revision_incremented_by_disposition":False,"current_plan_revised_by_disposition":False,"current_policy_activated_by_disposition":False,"learning_delta_activated_by_disposition":False,"tool_invocation_performed":False,"external_side_effect_performed":False,"automatic_truth_generalization":False,"automatic_causal_attribution":False,"automatic_dukkha_realization_confirmation":False,"automatic_learning_update":False,"automatic_policy_activation":False,"automatic_maintenance_action":False,"automatic_plan_completion":False,"automatic_rollback":False,"automatic_compensation":False,"generalized_benefit_claimed":False,
        "selection_remains_decisionos_owned":True,"selection_authority_granted_to_learnos":False,"plan_revision_authority_granted_to_learnos":False,"dukkha_minimization_authority_granted_to_learnos":False,"general_execution_authority_granted":False,"execution_permission":False,"world_mutation_authority_granted":False,"current_policy_activation_authority_granted":False,"maintenance_action_authority_granted_to_learnos":False,"evidence_lineage_preserved":True,"responsibility_lineage_preserved":True,"protected_group_nonexternalization_preserved":True,"future_nonexternalization_preserved":True,"history_read_only":True,"future_only":True,"active_now":False,"resulting_lineage_digests":lineage,"resulting_responsibility_lineage_digests":resp,
    }
    receipt[RECEIPT_DIGEST_FIELD]=canonical_digest(receipt)
    return LearnOSFutureOnlyMaintenanceDispositionResult(STATUS_READY,[],receipt)
