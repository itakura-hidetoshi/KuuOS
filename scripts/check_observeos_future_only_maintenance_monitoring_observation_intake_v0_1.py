#!/usr/bin/env python3
from copy import deepcopy
from runtime.kuuos_observeos_future_only_maintenance_monitoring_observation_intake_v0_1 import *
from scripts.check_observeos_future_only_maintenance_monitoring_observation_fixture_v0_1 import *
def main():
    x=build(); assert x.status==STATUS_READY and x.receipt; q=x.receipt
    assert q["maintenance_monitoring_observation_disposition"]==DISPOSITION_SUPPORTED
    assert q["maintenance_monitoring_observation_recorded"] and not q["maintenance_monitoring_activated"]
    for f in ("current_world_state_changed","world_revision_incremented","current_plan_revised","current_policy_activated","tool_invocation_performed","external_side_effect_performed","general_execution_authority_granted","world_mutation_authority_granted","policy_activation_authority_granted","active_now"): assert q[f] is False
    assert q[RECEIPT_DIGEST_FIELD]==canonical_digest({k:v for k,v in q.items() if k!=RECEIPT_DIGEST_FIELD})
    assert build(expected_source_future_only_learning_receipt_digest="wrong").status==STATUS_BLOCKED
    s=source(); e=evidence(s); r=review(s,e); c=context(s,e,r); cases=[]
    z=deepcopy(c); z["current_world_model_state_digest"]="stale"; cases.append((dict(monitoring_observation_intake_context=redigest(z,CONTEXT_DIGEST_FIELD)),DISPOSITION_WORLD_REFRESH))
    z=deepcopy(c); z["observation_intake_epoch"]=z["source_learning_epoch"]+z["maximum_observation_intake_delay"]+1; cases.append((dict(monitoring_observation_intake_context=redigest(z,CONTEXT_DIGEST_FIELD)),DISPOSITION_CONTEXT_REFRESH))
    z=deepcopy(c); z["prior_observation_intake_session_ids"]=[z["observation_intake_session_id"]]; cases.append((dict(monitoring_observation_intake_context=redigest(z,CONTEXT_DIGEST_FIELD)),DISPOSITION_REPLAY_REJECTED))
    z=deepcopy(r); z["review_completed_epoch"]=z["review_started_epoch"]+z["maximum_review_duration"]+1; cases.append((dict(monitoring_observation_review_certificate=redigest(z,REVIEW_DIGEST_FIELD)),DISPOSITION_REVIEW_REFRESH))
    z=deepcopy(e); z["independent_monitoring_observation_evidence"]=False; cases.append((dict(monitoring_observation_evidence_packet=redigest(z,EVIDENCE_DIGEST_FIELD)),DISPOSITION_ADDITIONAL_EVIDENCE))
    routes=(("source_learning_receipt_correspondence_confirmed",DISPOSITION_SOURCE_REPAIR),("maintenance_handoff_correspondence_confirmed",DISPOSITION_HANDOFF_REPAIR),("maintenance_window_observed",DISPOSITION_WINDOW_REPAIR),("durability_observed",DISPOSITION_DURABILITY_REPAIR),("adverse_effects_observed",DISPOSITION_ADVERSE_REPAIR),("distributional_effects_observed",DISPOSITION_DISTRIBUTIONAL_REPAIR),("reobservation_trigger_evaluated",DISPOSITION_TRIGGER_REPAIR),("retention_window_respected",DISPOSITION_RETENTION_REPAIR),("uncertainty_adequate",DISPOSITION_UNCERTAINTY_REPAIR),("calibration_adequate",DISPOSITION_CALIBRATION_REPAIR),("provenance_continuity_preserved",DISPOSITION_PROVENANCE_REPAIR),("protected_group_nonexternalization_supported",DISPOSITION_NONEXTERNALIZATION_REVIEW))
    for f,d in routes:
        z=deepcopy(r); z[f]=False; cases.append((dict(monitoring_observation_review_certificate=redigest(z,REVIEW_DIGEST_FIELD)),d))
    z=deepcopy(e); z["current_state_mutation_performed"]=True; cases.append((dict(monitoring_observation_evidence_packet=redigest(z,EVIDENCE_DIGEST_FIELD)),DISPOSITION_CURRENT_STATE_MUTATION_REJECTED))
    z=deepcopy(e); z["authority_escalation_claimed"]=True; cases.append((dict(monitoring_observation_evidence_packet=redigest(z,EVIDENCE_DIGEST_FIELD)),DISPOSITION_AUTHORITY_ESCALATION_REJECTED))
    for kw,d in cases:
        y=build(**kw); assert y.status==STATUS_READY and y.receipt["maintenance_monitoring_observation_disposition"]==d,(d,y)
    print("PASS: ObserveOS v0.4 future-only maintenance-monitoring observation intake actual-chain validation")
    return 0
if __name__=="__main__": raise SystemExit(main())
