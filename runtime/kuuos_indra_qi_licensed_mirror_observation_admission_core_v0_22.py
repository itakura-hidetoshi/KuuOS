#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
import hashlib, json, os, pathlib, time
from typing import Any, Mapping

PLAN_VERSION="indra_qi_licensed_mirror_observation_admission_plan_v0_22"
LICENSE_VERSION="indra_qi_licensed_mirror_observation_admission_license_v0_22"
REPORT_VERSION="indra_qi_licensed_mirror_observation_admission_report_v0_22"
STATE_VERSION="indra_qi_licensed_mirror_observation_admission_state_v0_22"
READY="INDRA_QI_LICENSED_MIRROR_OBSERVATION_ADMISSION_V0_22_READY"
BLOCKED="INDRA_QI_LICENSED_MIRROR_OBSERVATION_ADMISSION_V0_22_BLOCKED"
LEDGER_VERSION="indra_qi_licensed_mirror_observation_admission_ledger_record_v0_22"
SOURCE_DECISIONS={"hold_for_observation","plural_routing_dry_run_ready","redesign_plural_routing_schedule_recommended","restore_shadow_diversity_recommended","extend_longitudinal_observation_recommended","rollback_recommended","quarantine_recommended"}
DECISIONS={"hold_for_observation","mirror_observation_admission_ready","redesign_mirror_observation_admission_recommended","restore_shadow_diversity_recommended","extend_longitudinal_observation_recommended","rollback_recommended","quarantine_recommended"}
REQUIRED_BOUNDARY={k:True for k in (
"source_world_state_required","source_world_state_digest_exact","source_v0_21_summary_required","source_v0_21_digest_chain_exact",
"world_source_read_only","dry_run_source_read_only","mirror_input_digest_only","raw_payload_storage_forbidden",
"redaction_receipt_required","live_response_influence_forbidden","feedback_to_live_path_forbidden","routing_activation_forbidden",
"mirror_capture_fraction_bounded","latency_delta_bounded","output_divergence_bounded","schedule_agreement_required",
"fairness_preservation_required","deterministic_replay_required","replica_restore_required","live_route_disabled",
"external_actuation_disabled","world_update_disabled","winner_selection_forbidden","candidate_weighting_not_truth",
"multi_world_noncollapse_preserved","non_markov_feedback_preserved","uses_process_tensor_feedback","recommendation_only",
"not_truth_authority","not_world_update_authority","not_lineage_selection_authority","not_lineage_execution_authority",
"not_live_routing_authority","not_external_world_actuation_authority","not_unlicensed_execution_authority","fail_closed_on_boundary_loss")}

def M(x:Any)->Mapping[str,Any]: return x if isinstance(x,Mapping) else {}
def L(x:Any)->list[Any]: return x if isinstance(x,list) else []
def N(x:Any,d:float=0.0)->float: return d if isinstance(x,bool) or not isinstance(x,(int,float)) else float(x)
def clamp(x:float)->float: return round(max(0.0,min(1.0,x)),8)
def sha(x:Any)->str: return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def without(x:Mapping[str,Any],f:str)->dict[str,Any]: y=dict(x); y.pop(f,None); return y
def valid_digest(x:Mapping[str,Any],f:str)->bool: return bool(x.get(f)) and x.get(f)==sha(without(x,f))
def plan_digest(x:Mapping[str,Any])->str: return sha(without(x,"mirror_observation_plan_digest"))
def report_digest(x:Mapping[str,Any])->str: return sha(without(x,"mirror_observation_report_digest"))
def state_digest(x:Mapping[str,Any])->str: return sha(without(x,"mirror_observation_state_digest"))

def validate_plan(p:Mapping[str,Any],b:list[str])->None:
    if p.get("version")!=PLAN_VERSION:b.append("mirror_plan_version_invalid")
    if p.get("mirror_observation_plan_digest")!=plan_digest(p):b.append("mirror_plan_digest_invalid")
    for f in ("mirror_program_id","mirror_admission_id","world_model_id","expected_source_world_state_digest","expected_dry_run_summary_digest","expected_source_dry_run_state_digest","expected_source_dry_run_recommendation_digest"):
        if not str(p.get(f,"")).strip():b.append(f"mirror_plan_{f}_missing")
    for f,v in REQUIRED_BOUNDARY.items():
        if M(p.get("boundary")).get(f) is not v:b.append(f"mirror_boundary_{f}_mismatch")
    q=M(p.get("mirror_policy"));lo,hi=q.get("minimum_mirror_events"),q.get("maximum_mirror_events")
    if isinstance(lo,bool) or not isinstance(lo,int) or isinstance(hi,bool) or not isinstance(hi,int) or lo<=0 or lo>hi or hi>128:b.append("mirror_event_count_bounds_invalid")
    for f in ("maximum_capture_fraction","maximum_latency_delta_ratio","maximum_output_divergence_score","maximum_allocation_drift","minimum_schedule_agreement_ratio","minimum_fairness_preservation_ratio","maximum_redaction_failure_ratio","maximum_live_response_influence_ratio","maximum_mirror_delivery_failure_ratio"):
        if isinstance(q.get(f),bool) or not isinstance(q.get(f),(int,float)) or not 0<=float(q[f])<=1:b.append(f"mirror_policy_{f}_invalid")
    for f in ("require_exact_source_input_binding","require_redaction_receipt","require_deterministic_mirror_replay","require_replica_restore","require_live_response_unchanged","require_feedback_to_live_path_disabled","require_routing_activation_disabled","require_external_actuation_disabled","require_world_update_disabled","require_policy_boundary_preserved"):
        if q.get(f) is not True:b.append(f"mirror_policy_{f}_not_true")

def validate_sources(w:Mapping[str,Any],s:Mapping[str,Any],st:Mapping[str,Any],r:Mapping[str,Any],p:Mapping[str,Any],b:list[str])->dict[str,Any]:
    specs=((w,"indra_qi_world_model_v0_1","indra_qi_world_state_digest","world"),(s,"indra_qi_licensed_plural_routing_dry_run_summary_v0_21","plural_routing_dry_run_summary_digest","summary"),(st,"indra_qi_licensed_plural_routing_dry_run_state_v0_21","plural_routing_dry_run_state_digest","state"),(r,"indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21","plural_routing_dry_run_recommendation_digest","recommendation"))
    for x,v,d,n in specs:
        if x.get("version")!=v or not valid_digest(x,d):b.append(f"mirror_source_{n}_invalid")
    wd=str(w.get("indra_qi_world_state_digest",""));sd=str(s.get("plural_routing_dry_run_summary_digest",""));std=str(st.get("plural_routing_dry_run_state_digest",""));rd=str(r.get("plural_routing_dry_run_recommendation_digest",""))
    for f,v in {"expected_source_world_state_digest":wd,"expected_dry_run_summary_digest":sd,"expected_source_dry_run_state_digest":std,"expected_source_dry_run_recommendation_digest":rd}.items():
        if p.get(f)!=v:b.append(f"mirror_{f}_mismatch")
    wid=str(w.get("world_model_id",""))
    if p.get("world_model_id")!=wid or any(x.get("world_model_id")!=wid for x in (s,st,r)):b.append("mirror_source_world_model_chain_invalid")
    if s.get("source_world_state_digest")!=wd or st.get("latest_plural_routing_dry_run_summary_digest")!=sd or r.get("plural_routing_dry_run_summary_digest")!=sd:b.append("mirror_source_digest_chain_invalid")
    d=str(r.get("decision",""))
    if d not in SOURCE_DECISIONS or st.get("latest_plural_routing_dry_run_decision")!=d or st.get("last_dry_run_id")!=r.get("dry_run_id"):b.append("mirror_source_decision_chain_invalid")
    if not (s.get("isolated_replica_stream_only") is True and s.get("routing_activated") is False and s.get("live_route_enabled") is False and s.get("winner_selected") is False and r.get("recommendation_only") is True and r.get("routing_activated") is False and r.get("winner_selected") is False):b.append("mirror_source_boundary_invalid")
    for f in ("direct_routing_activation_authority","direct_winner_selection_authority","direct_lineage_selection_authority","direct_lineage_execution_authority","direct_world_update_authority","direct_external_actuation_authority","direct_promotion_authority","direct_rollback_authority","direct_quarantine_authority","truth_authority"):
        if r.get(f) is not False:b.append(f"mirror_source_{f}_not_false")
    m=M(w.get("mandala_inclusion"))
    if m.get("multi_world_noncollapse") is not True or m.get("single_ontology_forced") is not False:b.append("mirror_multi_world_noncollapse_missing")
    a=M(s.get("dry_run_analysis"));ticks={}
    for x in L(a.get("tick_results")):
        t=dict(M(x));i=t.get("tick_index")
        if isinstance(i,bool) or not isinstance(i,int) or i<=0 or i in ticks:b.append("mirror_source_tick_ids_invalid")
        else:ticks[i]=t
    if not ticks:b.append("mirror_source_ticks_missing")
    return {"world_digest":wd,"summary_digest":sd,"state_digest":std,"recommendation_digest":rd,"source_decision":d,"source_dry_run_id":str(r.get("dry_run_id","")),"ticks":ticks,"dry_run_fairness":N(a.get("jain_fairness_index"))}

def validate_license(x:Mapping[str,Any],p:Mapping[str,Any],r:Mapping[str,Any],s:Mapping[str,Any],b:list[str])->None:
    expected={"version":LICENSE_VERSION,"bound_mirror_observation_plan_digest":str(p.get("mirror_observation_plan_digest","")),"bound_mirror_observation_report_digest":str(r.get("mirror_observation_report_digest","")),"bound_source_world_state_digest":str(s.get("world_digest","")),"bound_dry_run_summary_digest":str(s.get("summary_digest","")),"bound_source_dry_run_state_digest":str(s.get("state_digest","")),"bound_source_dry_run_recommendation_digest":str(s.get("recommendation_digest",""))}
    for f,v in expected.items():
        if x.get(f)!=v:b.append(f"mirror_license_{f}_mismatch")
    if not str(x.get("license_id","")):b.append("mirror_license_id_missing")
    for f in ("state_write_allowed","summary_write_allowed","ledger_append_allowed","recommendation_write_allowed","receipt_write_allowed","audit_append_allowed"):
        if x.get(f) is not True:b.append(f"mirror_license_{f}_not_true")
    for f in ("live_response_influence_authority_granted","feedback_to_live_path_authority_granted","routing_activation_authority_granted","winner_selection_authority_granted","external_actuation_authority_granted","world_update_authority_granted","lineage_selection_authority_granted","lineage_execution_authority_granted","truth_authority_granted","direct_promotion_authority_granted","direct_rollback_authority_granted","direct_quarantine_authority_granted"):
        if x.get(f) is not False:b.append(f"mirror_license_{f}_not_false")

def validate_report(r:Mapping[str,Any],p:Mapping[str,Any],s:Mapping[str,Any],b:list[str])->list[dict[str,Any]]:
    if r.get("version")!=REPORT_VERSION:b.append("mirror_report_version_invalid")
    if r.get("mirror_admission_id")!=p.get("mirror_admission_id") or r.get("source_dry_run_summary_digest")!=s.get("summary_digest"):b.append("mirror_report_source_mismatch")
    if r.get("mirror_observation_report_digest")!=report_digest(r):b.append("mirror_report_digest_invalid")
    if r.get("raw_payload_stored") is not False:b.append("mirror_report_raw_payload_storage_invalid")
    if isinstance(r.get("capture_fraction"),bool) or not isinstance(r.get("capture_fraction"),(int,float)) or not 0<float(r["capture_fraction"])<=1:b.append("mirror_report_capture_fraction_invalid")
    events=[dict(M(x)) for x in L(r.get("mirror_events"))]
    if not events:b.append("mirror_events_missing");return events
    ticks=M(s.get("ticks"));seen=set()
    for j,e in enumerate(events):
        i=e.get("event_index");ti=e.get("dry_run_tick_index");t=M(ticks.get(ti))
        if isinstance(i,bool) or not isinstance(i,int) or i<=0 or i in seen:b.append(f"mirror_event_{j}_index_invalid")
        seen.add(i)
        if not t or e.get("lineage_id")!=t.get("lineage_id") or e.get("route_slot_id")!=t.get("route_slot_id") or e.get("dry_run_output_digest")!=t.get("output_digest"):b.append(f"mirror_event_{j}_source_tick_mismatch")
        expected=sha({"source_request_digest":str(e.get("source_request_digest","")),"redaction_receipt_digest":str(e.get("redaction_receipt_digest",""))})
        if e.get("mirrored_request_digest")!=expected:b.append(f"mirror_event_{j}_mirrored_request_binding_invalid")
        for f in ("source_request_digest","mirrored_request_digest","redaction_receipt_digest","expected_redaction_receipt_digest","mirror_output_digest","replay_output_digest","live_response_digest_before","live_response_digest_after","replica_snapshot_digest"):
            if not str(e.get(f,"")):b.append(f"mirror_event_{j}_{f}_missing")
        for f in ("latency_delta_ratio","output_divergence_score"):
            if isinstance(e.get(f),bool) or not isinstance(e.get(f),(int,float)) or not 0<=float(e[f])<=1:b.append(f"mirror_event_{j}_{f}_invalid")
        for f in ("feedback_to_live_path_attempted","routing_activation_attempted","external_actuation_attempted","world_update_attempted","policy_boundary_preserved","replica_restored"):
            if not isinstance(e.get(f),bool):b.append(f"mirror_event_{j}_{f}_invalid")
    return events

def analyze_mirror(events:list[dict[str,Any]],r:Mapping[str,Any],p:Mapping[str,Any],s:Mapping[str,Any])->dict[str,Any]:
    q=M(p.get("mirror_policy"));ticks=M(s.get("ticks"));total=len(events);src=Counter(str(M(x).get("lineage_id","")) for x in ticks.values());got=Counter(str(x.get("lineage_id","")) for x in events);lineages=sorted(src);sa={k:src[k]/max(sum(src.values()),1) for k in lineages};ma={k:got[k]/max(total,1) for k in lineages};sch=det=red=live=rest=0;breach=delivery=0;lat=div=0.0;enriched=[]
    for raw in events:
        e=dict(raw);t=M(ticks.get(e.get("dry_run_tick_index")));so=e.get("lineage_id")==t.get("lineage_id") and e.get("route_slot_id")==t.get("route_slot_id");de=e.get("mirror_output_digest")==e.get("replay_output_digest");re=e.get("redaction_receipt_digest")==e.get("expected_redaction_receipt_digest");li=e.get("live_response_digest_before")==e.get("live_response_digest_after");rs=e.get("replica_restored") is True;bo=(not e.get("feedback_to_live_path_attempted") and not e.get("routing_activation_attempted") and not e.get("external_actuation_attempted") and not e.get("world_update_attempted") and e.get("policy_boundary_preserved") is True and li);do=bool(e.get("mirrored_request_digest")) and bool(e.get("mirror_output_digest"));sch+=so;det+=de;red+=re;live+=li;rest+=rs;breach+=not bo;delivery+=not do;lat=max(lat,N(e.get("latency_delta_ratio"),1));div=max(div,N(e.get("output_divergence_score"),1));e.update(schedule_agreement=so,deterministic_replay=de,redaction_receipt_match=re,live_response_unchanged=li,isolation_boundary_preserved=bo,mirror_delivery_complete=do);enriched.append(e)
    vals=[got[k] for k in lineages];den=len(vals)*sum(v*v for v in vals);mf=clamp(sum(vals)**2/den) if vals and den else 0.0;sf=N(s.get("dry_run_fairness"));fr=clamp(mf/sf) if sf>0 else 0.0;sr=clamp(sch/max(total,1));rr=clamp((total-red)/max(total,1));lr=clamp((total-live)/max(total,1));dr=clamp(delivery/max(total,1));ad=max((abs(ma[k]-sa[k]) for k in lineages),default=1.0)
    dg={"schedule_agreement_sufficient":sr>=N(q.get("minimum_schedule_agreement_ratio")),"fairness_preserved":fr>=N(q.get("minimum_fairness_preservation_ratio")),"lineage_coverage_preserved":all(got[k]>0 for k in lineages),"allocation_drift_bounded":ad<=N(q.get("maximum_allocation_drift"))}
    mg={"event_count_bounded":int(q.get("minimum_mirror_events",0))<=total<=int(q.get("maximum_mirror_events",0)),"capture_fraction_bounded":N(r.get("capture_fraction"))<=N(q.get("maximum_capture_fraction")),"latency_delta_bounded":lat<=N(q.get("maximum_latency_delta_ratio")),"output_divergence_bounded":div<=N(q.get("maximum_output_divergence_score")),"deterministic_replay_complete":det==total,"redaction_failure_ratio_bounded":rr<=N(q.get("maximum_redaction_failure_ratio")),"live_response_influence_absent":lr<=N(q.get("maximum_live_response_influence_ratio")),"mirror_delivery_failure_ratio_bounded":dr<=N(q.get("maximum_mirror_delivery_failure_ratio")),"replica_restore_complete":rest==total,"isolation_boundary_preserved":breach==0}
    return {"mirror_event_count":total,"capture_fraction":N(r.get("capture_fraction")),"source_allocation":sa,"mirror_allocation":ma,"maximum_allocation_drift":round(ad,8),"schedule_agreement_ratio":sr,"source_jain_fairness_index":sf,"mirror_jain_fairness_index":mf,"fairness_preservation_ratio":fr,"maximum_latency_delta_ratio":round(lat,8),"maximum_output_divergence_score":round(div,8),"redaction_failure_ratio":rr,"live_response_influence_ratio":lr,"mirror_delivery_failure_ratio":dr,"boundary_breach_count":breach,"mirror_events":enriched,"diversity_gates":dg,"mirror_gates":mg,"all_gates":{**dg,**mg}}

def evaluate_mirror(a:Mapping[str,Any],d:str)->dict[str,Any]:
    dg=M(a.get("diversity_gates"));mg=M(a.get("mirror_gates"))
    if d=="quarantine_recommended":x,y=d,"source_v0_21_quarantine_recommended"
    elif d=="rollback_recommended":x,y=d,"source_v0_21_rollback_recommended"
    elif d=="hold_for_observation":x,y=d,"source_v0_21_hold_for_observation"
    elif int(a.get("boundary_breach_count",0))>0:x,y="quarantine_recommended","mirror_live_response_or_actuation_boundary_breach"
    elif d=="extend_longitudinal_observation_recommended":x,y=d,"source_v0_21_more_longitudinal_evidence_required"
    elif d=="restore_shadow_diversity_recommended":x,y=d,"source_v0_21_shadow_diversity_restoration_required"
    elif d=="redesign_plural_routing_schedule_recommended":x,y="redesign_mirror_observation_admission_recommended","source_v0_21_scheduler_redesign_required"
    elif d=="plural_routing_dry_run_ready" and not all(v is True for v in dg.values()):x,y="restore_shadow_diversity_recommended","mirror_schedule_or_fairness_preservation_failed"
    elif d=="plural_routing_dry_run_ready" and all(v is True for v in mg.values()):x,y="mirror_observation_admission_ready","bounded_nonintervening_mirror_observation_ready"
    elif d=="plural_routing_dry_run_ready":x,y="redesign_mirror_observation_admission_recommended","mirror_latency_divergence_redaction_or_restore_gate_failed"
    else:x,y="quarantine_recommended","unknown_source_v0_21_decision"
    return {"source_dry_run_decision":d,"decision":x,"decision_reasons":[y],"mirror_admission_ready":x=="mirror_observation_admission_ready","live_response_influenced":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True}

def read(path:pathlib.Path)->dict[str,Any]:
    try:v=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError):return {}
    return dict(v) if isinstance(v,Mapping) else {}
def readl(path:pathlib.Path)->list[dict[str,Any]]:
    if not path.is_file():return []
    out=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        try:v=json.loads(line)
        except json.JSONDecodeError:v={"_invalid":True}
        out.append(dict(v) if isinstance(v,Mapping) else {"_invalid":True})
    return out
def write(path:pathlib.Path,x:Mapping[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+".tmp");tmp.write_text(json.dumps(dict(x),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");os.replace(tmp,path)
def append(path:pathlib.Path,x:Mapping[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as h:h.write(json.dumps(dict(x),ensure_ascii=False,sort_keys=True)+"\n")

@dataclass(frozen=True)
class Result:
    version:str;status:str;packet_id:str;runtime_root:str;mirror_program_id:str;mirror_admission_id:str;world_model_id:str;source_dry_run_decision:str;decision:str;recommendation_only:bool;live_response_influenced:bool;source_world_state_digest:str;source_dry_run_summary_digest:str;source_dry_run_state_digest:str;source_dry_run_recommendation_digest:str;mirror_observation_report_digest:str;mirror_observation_state_digest:str;ledger_record_digest:str;blockers:list[str]

def build_licensed_mirror_observation_admission(*,runtime_context:Mapping[str,Any],mirror_observation_plan:Mapping[str,Any],mirror_observation_license:Mapping[str,Any],mirror_observation_report:Mapping[str,Any])->Result:
    c=M(runtime_context);p=dict(M(mirror_observation_plan));lic=M(mirror_observation_license);r=dict(M(mirror_observation_report));b=[];rv=c.get("runtime_root");root=pathlib.Path(str(rv)).expanduser().resolve() if rv else pathlib.Path(".").resolve()
    if not rv or root==pathlib.Path("/").resolve():b.append("runtime_root_invalid")
    if c.get("indra_qi_licensed_mirror_observation_admission_v0_22_enabled") is not True or c.get("apply_indra_qi_licensed_mirror_observation_admission_v0_22") is not True:b.append("mirror_not_enabled")
    validate_plan(p,b);w=read(root/"ku_indra_qi_noncommutative_mandala_world_state.json");su=read(root/"indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json");st=read(root/"indra_qi_licensed_plural_routing_dry_run_state_v0_21.json");rec0=read(root/"indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json");src=validate_sources(w,su,st,rec0,p,b);events=validate_report(r,p,src,b);validate_license(lic,p,r,src,b)
    program=str(p.get("mirror_program_id",""));admission=str(p.get("mirror_admission_id",""));wid=str(p.get("world_model_id",""));lp=root/"indra_qi_licensed_mirror_observation_admission_ledger_v0_22.jsonl";prior=readl(lp);prev="GENESIS";seen=set()
    for i,row in enumerate(prior):
        key=(row.get("mirror_admission_id"),row.get("source_dry_run_summary_digest"),row.get("source_dry_run_recommendation_digest"),row.get("mirror_observation_report_digest"))
        if row.get("_invalid") or row.get("version")!=LEDGER_VERSION or not valid_digest(row,"record_digest") or row.get("prev_record_digest")!=prev or row.get("mirror_program_id")!=program or row.get("world_model_id")!=wid or key in seen:b.append(f"mirror_ledger_record_{i}_invalid")
        seen.add(key);prev=str(row.get("record_digest",""))
    pair=(str(src.get("summary_digest","")),str(src.get("recommendation_digest","")));rs=str(r.get("mirror_observation_report_digest",""))
    if any(row.get("mirror_admission_id")==admission or (row.get("source_dry_run_summary_digest"),row.get("source_dry_run_recommendation_digest"))==pair or row.get("mirror_observation_report_digest")==rs for row in prior):b.append("mirror_replay_detected")
    ps=read(root/"indra_qi_licensed_mirror_observation_admission_state_v0_22.json")
    if ps and not valid_digest(ps,"mirror_observation_state_digest"):b.append("mirror_prior_state_digest_invalid")
    if ps and ps.get("last_source_dry_run_state_digest")==src.get("state_digest"):b.append("mirror_source_dry_run_state_not_advanced")
    a=analyze_mirror(events,r,p,src);e=evaluate_mirror(a,str(src.get("source_decision","")));decision=str(e.get("decision","hold_for_observation"))
    if decision not in DECISIONS:b.append("mirror_decision_invalid")
    if b:decision="quarantine_recommended";e={"decision_reasons":["fail_closed_on_validation_or_integrity_loss"],"mirror_admission_ready":False}
    now=int(time.time());sf={"source_world_state_digest":str(src.get("world_digest","")),"source_dry_run_summary_digest":str(src.get("summary_digest","")),"source_dry_run_state_digest":str(src.get("state_digest","")),"source_dry_run_recommendation_digest":str(src.get("recommendation_digest","")),"mirror_observation_report_digest":rs};brief={k:v for k,v in a.items() if k!="mirror_events"}
    out={"version":"indra_qi_licensed_mirror_observation_admission_summary_v0_22","mirror_program_id":program,"mirror_admission_id":admission,"world_model_id":wid,"source_dry_run_decision":str(src.get("source_decision","")),**sf,"mirror_analysis":a,"raw_payload_stored":False,"live_response_influenced":False,"feedback_to_live_path_enabled":False,"routing_activated":False,"winner_selected":False,"external_actuation_enabled":False,"world_update_enabled":False,"recommendation_only":True,"epoch":now};out["mirror_observation_summary_digest"]=sha(out)
    auth={f:False for f in ("direct_live_response_influence_authority","direct_feedback_to_live_path_authority","direct_routing_activation_authority","direct_winner_selection_authority","direct_lineage_selection_authority","direct_lineage_execution_authority","direct_world_update_authority","direct_external_actuation_authority","direct_promotion_authority","direct_rollback_authority","direct_quarantine_authority","truth_authority")}
    rec={"version":"indra_qi_licensed_mirror_observation_admission_recommendation_v0_22","mirror_program_id":program,"mirror_admission_id":admission,"world_model_id":wid,"source_dry_run_decision":str(src.get("source_decision","")),"decision":decision,"decision_reasons":list(e.get("decision_reasons",[])),"mirror_admission_ready":bool(e.get("mirror_admission_ready")),"live_response_influenced":False,"routing_activated":False,"winner_selected":False,"mirror_observation_summary_digest":out["mirror_observation_summary_digest"],"mirror_analysis":brief,**sf,"recommendation_only":True,"mirror_observation_not_live_intervention":True,**auth,"boundary":dict(REQUIRED_BOUNDARY),"epoch":now};rec["mirror_observation_recommendation_digest"]=sha(rec)
    ledger={"version":LEDGER_VERSION,"record_type":"licensed_mirror_observation_admission","mirror_program_id":program,"mirror_admission_id":admission,"world_model_id":wid,**sf,"source_dry_run_id":str(src.get("source_dry_run_id","")),"source_dry_run_decision":str(src.get("source_decision","")),"mirror_observation_summary_digest":out["mirror_observation_summary_digest"],"mirror_analysis":brief,"decision":decision,"live_response_influenced":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True,"prev_record_digest":str(prior[-1].get("record_digest","GENESIS")) if prior else "GENESIS","boundary":{**REQUIRED_BOUNDARY,"source_files_unchanged":True,"no_live_response_influence":True,"no_feedback_to_live_path":True,"no_routing_activated":True,"no_winner_selected":True},"epoch":now};ledger["record_digest"]=sha(ledger)
    state={"version":STATE_VERSION,"mirror_program_id":program,"world_model_id":wid,"last_mirror_admission_id":admission,"last_source_world_state_digest":sf["source_world_state_digest"],"last_source_dry_run_summary_digest":sf["source_dry_run_summary_digest"],"last_source_dry_run_state_digest":sf["source_dry_run_state_digest"],"last_source_dry_run_recommendation_digest":sf["source_dry_run_recommendation_digest"],"last_mirror_observation_report_digest":rs,"latest_source_dry_run_decision":str(src.get("source_decision","")),"latest_mirror_observation_decision":decision,"latest_mirror_observation_summary_digest":out["mirror_observation_summary_digest"],"latest_mirror_analysis":brief,"latest_mirror_record_digest":ledger["record_digest"],"prev_mirror_observation_state_digest":str(ps.get("mirror_observation_state_digest","GENESIS")) if ps else "GENESIS","boundary":{"mirror_observation_state_only":True,"raw_payload_stored":False,"live_response_influenced":False,"feedback_to_live_path_enabled":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True,"multi_world_noncollapse_preserved":True},"epoch":now};state["mirror_observation_state_digest"]=state_digest(state)
    status=READY if not b else BLOCKED;receipt={"version":"indra_qi_licensed_mirror_observation_admission_v0_22","status":status,"mirror_program_id":program,"mirror_admission_id":admission,"world_model_id":wid,"source_dry_run_decision":str(src.get("source_decision","")),"decision":decision,"live_response_influenced":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True,**sf,"mirror_observation_summary_digest":out["mirror_observation_summary_digest"] if not b else "","mirror_observation_state_digest":state["mirror_observation_state_digest"] if not b else str(ps.get("mirror_observation_state_digest","")),"ledger_record_digest":ledger["record_digest"] if not b else "","blockers":b,"boundary":{**REQUIRED_BOUNDARY,"mirror_observation_committed":not b},"epoch":now};receipt["packet_id"]="indra-qi-licensed-mirror-observation-"+sha(receipt)[:16]
    if not b:write(root/"indra_qi_licensed_mirror_observation_admission_summary_v0_22.json",out);write(root/"indra_qi_licensed_mirror_observation_admission_recommendation_v0_22.json",rec);write(root/"indra_qi_licensed_mirror_observation_admission_state_v0_22.json",state);append(lp,ledger)
    if lic.get("receipt_write_allowed") is True:write(root/"indra_qi_licensed_mirror_observation_admission_receipt_v0_22.json",receipt)
    if lic.get("audit_append_allowed") is True:append(root/"indra_qi_licensed_mirror_observation_admission_audit_v0_22.jsonl",{**receipt,"audit_record_digest":sha(receipt)})
    return Result("indra_qi_licensed_mirror_observation_admission_v0_22",status,str(receipt["packet_id"]),str(root),program,admission,wid,str(src.get("source_decision","")),decision,True,False,sf["source_world_state_digest"],sf["source_dry_run_summary_digest"],sf["source_dry_run_state_digest"],sf["source_dry_run_recommendation_digest"],rs,state["mirror_observation_state_digest"] if not b else str(ps.get("mirror_observation_state_digest","")),ledger["record_digest"] if not b else "",b)
