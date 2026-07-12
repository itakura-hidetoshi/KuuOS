#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass
from typing import Any, Mapping

STATUS_READY="ready"; STATUS_BLOCKED="blocked"
STATE_BEFORE="world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded"
STATE_AFTER_SUPPORTED=STATE_BEFORE+"_maintenance_monitoring_observation_recorded"
RECEIPT_DIGEST_FIELD="maintenance_monitoring_observation_receipt_digest"
SOURCE_DIGEST_FIELD="future_only_learning_receipt_digest"
EVIDENCE_DIGEST_FIELD="maintenance_monitoring_observation_evidence_packet_digest"
REVIEW_DIGEST_FIELD="maintenance_monitoring_observation_review_certificate_digest"
CONTEXT_DIGEST_FIELD="maintenance_monitoring_observation_intake_context_digest"
DISPOSITION_SUPPORTED="maintenance_monitoring_observation_supported"
DISPOSITION_WORLD_REFRESH="world_refresh_required"
DISPOSITION_CONTEXT_REFRESH="observation_context_refresh_required"
DISPOSITION_REVIEW_REFRESH="observation_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE="additional_monitoring_evidence_required"
DISPOSITION_SOURCE_REPAIR="source_learning_receipt_correspondence_repair_required"
DISPOSITION_HANDOFF_REPAIR="maintenance_handoff_correspondence_repair_required"
DISPOSITION_WINDOW_REPAIR="maintenance_window_repair_required"
DISPOSITION_DURABILITY_REPAIR="durability_observation_repair_required"
DISPOSITION_ADVERSE_REPAIR="adverse_effect_observation_repair_required"
DISPOSITION_DISTRIBUTIONAL_REPAIR="distributional_observation_repair_required"
DISPOSITION_TRIGGER_REPAIR="reobservation_trigger_repair_required"
DISPOSITION_RETENTION_REPAIR="retention_window_repair_required"
DISPOSITION_UNCERTAINTY_REPAIR="uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR="calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR="provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW="nonexternalization_review_required"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED="current_state_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED="authority_escalation_rejected"
DISPOSITION_REPLAY_REJECTED="replay_conflict_rejected"

def canonical_digest(value: Any)->str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def as_map(v): return dict(v) if isinstance(v,Mapping) else {}
def digest_without(value,key): return canonical_digest({k:v for k,v in value.items() if k!=key})
@dataclass(frozen=True)
class ObserveOSMaintenanceMonitoringObservationResult:
    status:str; blockers:list[str]; receipt:dict[str,Any]|None

def build_observeos_future_only_maintenance_monitoring_observation_intake(
    *, source_future_only_learning_receipt:Mapping[str,Any],
    expected_source_future_only_learning_receipt_digest:str,
    monitoring_observation_evidence_packet:Mapping[str,Any],
    expected_monitoring_observation_evidence_packet_digest:str,
    monitoring_observation_review_certificate:Mapping[str,Any],
    expected_monitoring_observation_review_certificate_digest:str,
    monitoring_observation_intake_context:Mapping[str,Any],
    expected_monitoring_observation_intake_context_digest:str,
    observation_policy_digest:str, observation_responsibility_digest:str,
    observation_request_id:str, observation_bundle_digest:str,
)->ObserveOSMaintenanceMonitoringObservationResult:
    s,e,r,c=map(as_map,(source_future_only_learning_receipt,monitoring_observation_evidence_packet,monitoring_observation_review_certificate,monitoring_observation_intake_context))
    b=[]
    sd=s.get("future_only_learning_receipt_digest","")
    if sd!=digest_without(s,"future_only_learning_receipt_digest") or sd!=expected_source_future_only_learning_receipt_digest:b.append("source_future_only_learning_receipt_digest_mismatch")
    required_source={"learnos_version":"v0.4","future_only_learning_supported":True,"future_only_learning_delta_recorded":True,"future_only_learning_delta_activated":False,"maintenance_monitoring_handoff_prepared":True,"maintenance_monitoring_activated":False,"world_fact_confirmed":True,"causal_attribution_confirmed":True,"dukkha_reduction_realized_confirmed":True}
    for k,v in required_source.items():
        if s.get(k)!=v:b.append(f"source_{k}_mismatch")
    handoff=s.get("maintenance_monitoring_handoff_envelope")
    if not isinstance(handoff,Mapping) or s.get("maintenance_monitoring_handoff_envelope_digest")!=canonical_digest(handoff):b.append("source_maintenance_monitoring_handoff_mismatch")
    ed=e.get(EVIDENCE_DIGEST_FIELD,""); rd=r.get(REVIEW_DIGEST_FIELD,""); cd=c.get(CONTEXT_DIGEST_FIELD,"")
    if ed!=digest_without(e,EVIDENCE_DIGEST_FIELD) or ed!=expected_monitoring_observation_evidence_packet_digest:b.append("monitoring_observation_evidence_digest_mismatch")
    if rd!=digest_without(r,REVIEW_DIGEST_FIELD) or rd!=expected_monitoring_observation_review_certificate_digest:b.append("monitoring_observation_review_digest_mismatch")
    if cd!=digest_without(c,CONTEXT_DIGEST_FIELD) or cd!=expected_monitoring_observation_intake_context_digest:b.append("monitoring_observation_context_digest_mismatch")
    expected_bundle=canonical_digest({"source":sd,"evidence":ed,"review":rd,"context":cd,"policy":observation_policy_digest,"responsibility":observation_responsibility_digest,"request":observation_request_id})
    if observation_bundle_digest!=expected_bundle:b.append("monitoring_observation_bundle_digest_mismatch")
    if b:return ObserveOSMaintenanceMonitoringObservationResult(STATUS_BLOCKED,sorted(set(b)),None)
    disposition=DISPOSITION_SUPPORTED
    if c.get("current_world_model_state_digest")!=s.get("source_world_model_state_digest"): disposition=DISPOSITION_WORLD_REFRESH
    elif c.get("observation_intake_epoch",0)>c.get("source_learning_epoch",0)+c.get("maximum_observation_intake_delay",0): disposition=DISPOSITION_CONTEXT_REFRESH
    elif c.get("observation_intake_session_id") in c.get("prior_observation_intake_session_ids",[]): disposition=DISPOSITION_REPLAY_REJECTED
    elif r.get("review_completed_epoch",0)>r.get("review_started_epoch",0)+r.get("maximum_review_duration",0): disposition=DISPOSITION_REVIEW_REFRESH
    elif not e.get("independent_monitoring_observation_evidence"): disposition=DISPOSITION_ADDITIONAL_EVIDENCE
    else:
        routes=(("source_learning_receipt_correspondence_confirmed",DISPOSITION_SOURCE_REPAIR),("maintenance_handoff_correspondence_confirmed",DISPOSITION_HANDOFF_REPAIR),("maintenance_window_observed",DISPOSITION_WINDOW_REPAIR),("durability_observed",DISPOSITION_DURABILITY_REPAIR),("adverse_effects_observed",DISPOSITION_ADVERSE_REPAIR),("distributional_effects_observed",DISPOSITION_DISTRIBUTIONAL_REPAIR),("reobservation_trigger_evaluated",DISPOSITION_TRIGGER_REPAIR),("retention_window_respected",DISPOSITION_RETENTION_REPAIR),("uncertainty_adequate",DISPOSITION_UNCERTAINTY_REPAIR),("calibration_adequate",DISPOSITION_CALIBRATION_REPAIR),("provenance_continuity_preserved",DISPOSITION_PROVENANCE_REPAIR),("protected_group_nonexternalization_supported",DISPOSITION_NONEXTERNALIZATION_REVIEW))
        for f,d in routes:
            if not r.get(f): disposition=d; break
        else:
            if e.get("current_state_mutation_performed"): disposition=DISPOSITION_CURRENT_STATE_MUTATION_REJECTED
            elif e.get("authority_escalation_claimed"): disposition=DISPOSITION_AUTHORITY_ESCALATION_REJECTED
    supported=disposition==DISPOSITION_SUPPORTED
    record={"source":sd,"evidence":ed,"review":rd,"handoff":s.get("maintenance_monitoring_handoff_envelope_digest"),"session":c.get("observation_intake_session_id"),"epoch":c.get("observation_intake_epoch"),"disposition":disposition}
    recd=canonical_digest(record)
    handoff2=None; handoff2d=""
    if supported:
        handoff2={"source_observation_record":recd,"durability_status":e["durability_status_digest"],"adverse_effect_status":e["adverse_effect_status_digest"],"distributional_status":e["distributional_status_digest"],"reobservation_status":e["reobservation_status_digest"],"state":"observed_not_activated","automatic_action":False}
        handoff2d=canonical_digest(handoff2)
    receipt={"kernel":"ObserveOS Future-Only Maintenance-Monitoring Observation Intake Kernel","kernel_version":"v0.1","observeos_version":"v0.4",SOURCE_DIGEST_FIELD:sd,"source_future_only_learning_delta_binding_digest":s.get("future_only_learning_delta_binding_digest"),"source_maintenance_monitoring_handoff_envelope_digest":s.get("maintenance_monitoring_handoff_envelope_digest"),"monitoring_observation_evidence_packet":e,EVIDENCE_DIGEST_FIELD:ed,"monitoring_observation_review_certificate":r,REVIEW_DIGEST_FIELD:rd,CONTEXT_DIGEST_FIELD:cd,"maintenance_monitoring_observation_disposition":disposition,"maintenance_monitoring_observation_state_before":STATE_BEFORE,"maintenance_monitoring_observation_state_after":STATE_AFTER_SUPPORTED if supported else STATE_BEFORE,"maintenance_monitoring_observation_record":record,"maintenance_monitoring_observation_record_digest":recd,"maintenance_monitoring_reobservation_handoff_envelope":handoff2,"maintenance_monitoring_reobservation_handoff_envelope_digest":handoff2d,"world_fact_confirmed":True,"causal_attribution_confirmed":True,"dukkha_reduction_realized_confirmed":True,"future_only_learning_delta_recorded":True,"future_only_learning_delta_activated":False,"maintenance_monitoring_observation_recorded":supported,"maintenance_monitoring_activated":False,"current_world_state_changed":False,"world_revision_incremented":False,"current_plan_revised":False,"current_policy_activated":False,"tool_invocation_performed":False,"external_side_effect_performed":False,"general_execution_authority_granted":False,"world_mutation_authority_granted":False,"policy_activation_authority_granted":False,"future_only":True,"active_now":False}
    receipt[RECEIPT_DIGEST_FIELD]=canonical_digest(receipt)
    return ObserveOSMaintenanceMonitoringObservationResult(STATUS_READY,[],receipt)
