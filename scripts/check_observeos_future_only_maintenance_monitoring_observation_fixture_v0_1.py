from __future__ import annotations
from copy import deepcopy
from runtime.kuuos_observeos_future_only_maintenance_monitoring_observation_intake_v0_1 import *
from scripts.check_learnos_dukkha_preserving_future_only_learning_maintenance_fixture_v0_1 import build as build_learnos

def source():
    x=build_learnos(); assert x.status=="ready" and x.receipt; return deepcopy(x.receipt)
def evidence(s):
    h=s["maintenance_monitoring_handoff_envelope"]
    v={"source_future_only_learning_receipt_digest":s["future_only_learning_receipt_digest"],"source_maintenance_monitoring_handoff_envelope_digest":s["maintenance_monitoring_handoff_envelope_digest"],"maintenance_window_digest":h["maintenance_window"],"durability_specification_digest":h["durability"],"adverse_effect_specification_digest":h["adverse"],"distributional_specification_digest":h["distributional"],"reobservation_trigger_digest":h["reobservation"],"retention_window_digest":h["retention"],"durability_status_digest":"durability-observed-v04","adverse_effect_status_digest":"adverse-observed-v04","distributional_status_digest":"distributional-observed-v04","reobservation_status_digest":"reobservation-evaluated-v04","uncertainty_digest":"observeos-uncertainty-v04","calibration_digest":"observeos-calibration-v04","provenance_digest":"observeos-provenance-v04","independent_monitoring_observation_evidence":True,"current_state_mutation_performed":False,"authority_escalation_claimed":False}
    v[EVIDENCE_DIGEST_FIELD]=digest_without(v,EVIDENCE_DIGEST_FIELD); return v
def review(s,e):
    v={"source_learning_receipt_correspondence_confirmed":True,"maintenance_handoff_correspondence_confirmed":True,"maintenance_window_observed":True,"durability_observed":True,"adverse_effects_observed":True,"distributional_effects_observed":True,"reobservation_trigger_evaluated":True,"retention_window_respected":True,"uncertainty_adequate":True,"calibration_adequate":True,"provenance_continuity_preserved":True,"protected_group_nonexternalization_supported":True,"review_started_epoch":150,"review_completed_epoch":151,"maximum_review_duration":4}
    v[REVIEW_DIGEST_FIELD]=digest_without(v,REVIEW_DIGEST_FIELD); return v
def context(s,e,r):
    v={"current_world_model_state_digest":s["source_world_model_state_digest"],"source_learning_epoch":s["future_only_learning_record"]["epoch"],"observation_intake_epoch":s["future_only_learning_record"]["epoch"]+3,"maximum_observation_intake_delay":8,"observation_intake_session_id":"observeos-maintenance-v04-001","prior_observation_intake_session_ids":[]}
    v[CONTEXT_DIGEST_FIELD]=digest_without(v,CONTEXT_DIGEST_FIELD); return v
def redigest(v,key): v=deepcopy(v); v.pop(key,None); v[key]=digest_without(v,key); return v
def build(**kw):
    s=deepcopy(kw.pop("source_future_only_learning_receipt",None) or source()); e=deepcopy(kw.pop("monitoring_observation_evidence_packet",None) or evidence(s)); r=deepcopy(kw.pop("monitoring_observation_review_certificate",None) or review(s,e)); c=deepcopy(kw.pop("monitoring_observation_intake_context",None) or context(s,e,r))
    p="observeos-maintenance-policy-v04"; resp="observeos-maintenance-responsibility-v04"; req="observeos-maintenance-request-v04"
    args=dict(source_future_only_learning_receipt=s,expected_source_future_only_learning_receipt_digest=s["future_only_learning_receipt_digest"],monitoring_observation_evidence_packet=e,expected_monitoring_observation_evidence_packet_digest=e[EVIDENCE_DIGEST_FIELD],monitoring_observation_review_certificate=r,expected_monitoring_observation_review_certificate_digest=r[REVIEW_DIGEST_FIELD],monitoring_observation_intake_context=c,expected_monitoring_observation_intake_context_digest=c[CONTEXT_DIGEST_FIELD],observation_policy_digest=p,observation_responsibility_digest=resp,observation_request_id=req,observation_bundle_digest=canonical_digest({"source":s["future_only_learning_receipt_digest"],"evidence":e[EVIDENCE_DIGEST_FIELD],"review":r[REVIEW_DIGEST_FIELD],"context":c[CONTEXT_DIGEST_FIELD],"policy":p,"responsibility":resp,"request":req}))
    args.update(kw); return build_observeos_future_only_maintenance_monitoring_observation_intake(**args)
