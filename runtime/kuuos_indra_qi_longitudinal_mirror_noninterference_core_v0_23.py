#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
import hashlib,json,os,pathlib,time
from typing import Any,Mapping

PLAN_VERSION="indra_qi_longitudinal_mirror_noninterference_plan_v0_23"; LICENSE_VERSION="indra_qi_longitudinal_mirror_noninterference_license_v0_23"; REPORT_VERSION="indra_qi_longitudinal_mirror_noninterference_report_v0_23"; STATE_VERSION="indra_qi_longitudinal_mirror_noninterference_state_v0_23"; LEDGER_VERSION="indra_qi_longitudinal_mirror_noninterference_ledger_record_v0_23"
READY="INDRA_QI_LONGITUDINAL_MIRROR_NONINTERFERENCE_V0_23_READY"; BLOCKED="INDRA_QI_LONGITUDINAL_MIRROR_NONINTERFERENCE_V0_23_BLOCKED"
SOURCE_DECISIONS={"hold_for_observation","mirror_observation_admission_ready","redesign_mirror_observation_admission_recommended","restore_shadow_diversity_recommended","extend_longitudinal_observation_recommended","rollback_recommended","quarantine_recommended"}
DECISIONS={"hold_for_observation","longitudinal_mirror_noninterference_ready","extend_mirror_observation_recommended","redesign_longitudinal_mirror_observation_recommended","restore_shadow_diversity_recommended","rollback_recommended","quarantine_recommended"}
METRICS=("latency_delta_ratio","output_divergence_score","allocation_drift","schedule_agreement_ratio","fairness_preservation_ratio","redaction_failure_ratio","live_response_influence_ratio","mirror_delivery_failure_ratio","replica_restore_ratio","deterministic_replay_ratio")
REQUIRED_BOUNDARY={k:True for k in ("source_world_state_required","source_world_state_digest_exact","source_v0_22_summary_required","source_v0_22_digest_chain_exact","world_source_read_only","mirror_source_read_only","longitudinal_cycle_chain_required","monotonic_cycle_index_required","monotonic_epoch_required","raw_payload_storage_forbidden","live_response_influence_forbidden","feedback_to_live_path_forbidden","routing_activation_forbidden","cumulative_latency_bounded","cumulative_divergence_bounded","allocation_drift_bounded","fairness_decay_bounded","schedule_agreement_required","redaction_stability_required","deterministic_replay_required","replica_restore_required","live_route_disabled","external_actuation_disabled","world_update_disabled","winner_selection_forbidden","candidate_weighting_not_truth","multi_world_noncollapse_preserved","non_markov_feedback_preserved","uses_process_tensor_feedback","recommendation_only","not_truth_authority","not_world_update_authority","not_lineage_selection_authority","not_lineage_execution_authority","not_live_routing_authority","not_external_world_actuation_authority","not_unlicensed_execution_authority","fail_closed_on_boundary_loss")}

def M(x:Any)->Mapping[str,Any]: return x if isinstance(x,Mapping) else {}
def L(x:Any)->list[Any]: return x if isinstance(x,list) else []
def N(x:Any,d:float=0.0)->float: return d if isinstance(x,bool) or not isinstance(x,(int,float)) else float(x)
def sha(x:Any)->str: return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def drop(x:Mapping[str,Any],f:str)->dict[str,Any]: y=dict(x);y.pop(f,None);return y
def valid_digest(x:Mapping[str,Any],f:str)->bool: return bool(x.get(f)) and x.get(f)==sha(drop(x,f))
def plan_digest(x:Mapping[str,Any])->str:return sha(drop(x,"longitudinal_mirror_plan_digest"))
def report_digest(x:Mapping[str,Any])->str:return sha(drop(x,"longitudinal_mirror_report_digest"))
def cycle_digest(x:Mapping[str,Any])->str:return sha(drop(x,"mirror_cycle_digest"))
def state_digest(x:Mapping[str,Any])->str:return sha(drop(x,"longitudinal_mirror_state_digest"))
def read(p:pathlib.Path)->dict[str,Any]:
 try:v=json.loads(p.read_text(encoding="utf-8"))
 except (OSError,json.JSONDecodeError):return {}
 return dict(v) if isinstance(v,Mapping) else {}
def readl(p:pathlib.Path)->list[dict[str,Any]]:
 if not p.is_file():return []
 out=[]
 for line in p.read_text(encoding="utf-8").splitlines():
  try:v=json.loads(line)
  except json.JSONDecodeError:v={"_invalid":True}
  out.append(dict(v) if isinstance(v,Mapping) else {"_invalid":True})
 return out
def write(p:pathlib.Path,x:Mapping[str,Any])->None:
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+".tmp");t.write_text(json.dumps(dict(x),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");os.replace(t,p)
def append(p:pathlib.Path,x:Mapping[str,Any])->None:
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("a",encoding="utf-8") as h:h.write(json.dumps(dict(x),ensure_ascii=False,sort_keys=True)+"\n")

def validate_plan(p:Mapping[str,Any],b:list[str])->None:
 if p.get("version")!=PLAN_VERSION:b.append("longitudinal_mirror_plan_version_invalid")
 if p.get("longitudinal_mirror_plan_digest")!=plan_digest(p):b.append("longitudinal_mirror_plan_digest_invalid")
 for f in ("evidence_program_id","evidence_run_id","world_model_id","expected_source_world_state_digest","expected_mirror_summary_digest","expected_source_mirror_state_digest","expected_source_mirror_recommendation_digest"):
  if not str(p.get(f,"")):b.append(f"longitudinal_mirror_plan_{f}_missing")
 for f,v in REQUIRED_BOUNDARY.items():
  if M(p.get("boundary")).get(f) is not v:b.append(f"longitudinal_mirror_boundary_{f}_mismatch")
 q=M(p.get("evidence_policy"));lo=q.get("minimum_evidence_cycles");hi=q.get("maximum_evidence_cycles")
 if isinstance(lo,bool) or not isinstance(lo,int) or isinstance(hi,bool) or not isinstance(hi,int) or lo<=0 or lo>hi or hi>64:b.append("longitudinal_mirror_cycle_count_bounds_invalid")
 for f in ("maximum_mean_latency_delta_ratio","maximum_cumulative_latency_delta_ratio","maximum_mean_output_divergence_score","maximum_cumulative_output_divergence_score","maximum_mean_allocation_drift","maximum_fairness_decay","minimum_schedule_agreement_ratio","minimum_fairness_preservation_ratio","maximum_redaction_failure_ratio","maximum_live_response_influence_ratio","maximum_mirror_delivery_failure_ratio","minimum_replica_restore_ratio","minimum_deterministic_replay_ratio"):
  if isinstance(q.get(f),bool) or not isinstance(q.get(f),(int,float)) or not 0<=float(q[f])<=1:b.append(f"longitudinal_mirror_policy_{f}_invalid")

def validate_sources(w:Mapping[str,Any],s:Mapping[str,Any],st:Mapping[str,Any],r:Mapping[str,Any],p:Mapping[str,Any],b:list[str])->dict[str,Any]:
 specs=((w,"indra_qi_world_model_v0_1","indra_qi_world_state_digest","world"),(s,"indra_qi_licensed_mirror_observation_admission_summary_v0_22","mirror_observation_summary_digest","summary"),(st,"indra_qi_licensed_mirror_observation_admission_state_v0_22","mirror_observation_state_digest","state"),(r,"indra_qi_licensed_mirror_observation_admission_recommendation_v0_22","mirror_observation_recommendation_digest","recommendation"))
 for x,v,d,n in specs:
  if x.get("version")!=v or not valid_digest(x,d):b.append(f"longitudinal_mirror_source_{n}_invalid")
 wd=str(w.get("indra_qi_world_state_digest",""));sd=str(s.get("mirror_observation_summary_digest",""));std=str(st.get("mirror_observation_state_digest",""));rd=str(r.get("mirror_observation_recommendation_digest",""))
 for f,v in {"expected_source_world_state_digest":wd,"expected_mirror_summary_digest":sd,"expected_source_mirror_state_digest":std,"expected_source_mirror_recommendation_digest":rd}.items():
  if p.get(f)!=v:b.append(f"longitudinal_mirror_{f}_mismatch")
 wid=str(w.get("world_model_id",""))
 if p.get("world_model_id")!=wid or any(x.get("world_model_id")!=wid for x in (s,st,r)):b.append("longitudinal_mirror_source_world_model_chain_invalid")
 d=str(r.get("decision",""))
 if s.get("source_world_state_digest")!=wd or st.get("latest_mirror_observation_summary_digest")!=sd or r.get("mirror_observation_summary_digest")!=sd or st.get("latest_mirror_observation_decision")!=d or st.get("last_mirror_admission_id")!=r.get("mirror_admission_id") or d not in SOURCE_DECISIONS:b.append("longitudinal_mirror_source_digest_or_decision_chain_invalid")
 if not (s.get("raw_payload_stored") is False and s.get("live_response_influenced") is False and s.get("feedback_to_live_path_enabled") is False and s.get("routing_activated") is False and s.get("winner_selected") is False and r.get("recommendation_only") is True and r.get("live_response_influenced") is False and r.get("routing_activated") is False and r.get("winner_selected") is False):b.append("longitudinal_mirror_source_boundary_invalid")
 m=M(w.get("mandala_inclusion"))
 if m.get("multi_world_noncollapse") is not True or m.get("single_ontology_forced") is not False:b.append("longitudinal_mirror_multi_world_noncollapse_missing")
 return {"world_digest":wd,"summary_digest":sd,"state_digest":std,"recommendation_digest":rd,"source_decision":d,"source_admission_id":str(r.get("mirror_admission_id",""))}

def validate_license(x:Mapping[str,Any],p:Mapping[str,Any],r:Mapping[str,Any],s:Mapping[str,Any],b:list[str])->None:
 expected={"version":LICENSE_VERSION,"bound_longitudinal_mirror_plan_digest":str(p.get("longitudinal_mirror_plan_digest","")),"bound_longitudinal_mirror_report_digest":str(r.get("longitudinal_mirror_report_digest","")),"bound_source_world_state_digest":str(s.get("world_digest","")),"bound_mirror_summary_digest":str(s.get("summary_digest","")),"bound_source_mirror_state_digest":str(s.get("state_digest","")),"bound_source_mirror_recommendation_digest":str(s.get("recommendation_digest",""))}
 for f,v in expected.items():
  if x.get(f)!=v:b.append(f"longitudinal_mirror_license_{f}_mismatch")
 for f in ("state_write_allowed","summary_write_allowed","ledger_append_allowed","recommendation_write_allowed","receipt_write_allowed","audit_append_allowed"):
  if x.get(f) is not True:b.append(f"longitudinal_mirror_license_{f}_not_true")

def validate_report(r:Mapping[str,Any],p:Mapping[str,Any],s:Mapping[str,Any],b:list[str])->list[dict[str,Any]]:
 if r.get("version")!=REPORT_VERSION or r.get("evidence_run_id")!=p.get("evidence_run_id") or r.get("latest_mirror_summary_digest")!=s.get("summary_digest"):b.append("longitudinal_mirror_report_source_mismatch")
 if r.get("longitudinal_mirror_report_digest")!=report_digest(r):b.append("longitudinal_mirror_report_digest_invalid")
 c=[dict(M(x)) for x in L(r.get("cycles"))];q=M(p.get("evidence_policy"))
 if not int(q.get("minimum_evidence_cycles",0))<=len(c)<=int(q.get("maximum_evidence_cycles",0)):b.append("longitudinal_mirror_cycle_count_out_of_bounds")
 prev="GENESIS";epoch=-1;seen=set()
 for i,x in enumerate(c):
  cid=str(x.get("mirror_admission_id",""));ep=x.get("epoch")
  if not cid or cid in seen or x.get("cycle_index")!=i+1:b.append(f"longitudinal_mirror_cycle_{i}_identity_invalid")
  seen.add(cid)
  if isinstance(ep,bool) or not isinstance(ep,int) or ep<=epoch:b.append(f"longitudinal_mirror_cycle_{i}_epoch_invalid")
  if isinstance(ep,int) and not isinstance(ep,bool):epoch=ep
  if x.get("prev_mirror_cycle_digest")!=prev or x.get("mirror_cycle_digest")!=cycle_digest(x):b.append(f"longitudinal_mirror_cycle_{i}_chain_invalid")
  prev=str(x.get("mirror_cycle_digest",""))
  for f in METRICS:
   if isinstance(x.get(f),bool) or not isinstance(x.get(f),(int,float)) or not 0<=float(x[f])<=1:b.append(f"longitudinal_mirror_cycle_{i}_{f}_invalid")
 if not c or c[-1].get("source_mirror_summary_digest")!=s.get("summary_digest") or c[-1].get("mirror_admission_id")!=s.get("source_admission_id"):b.append("longitudinal_mirror_latest_source_mismatch")
 return c

def analyze(c:list[dict[str,Any]],p:Mapping[str,Any])->dict[str,Any]:
 q=M(p.get("evidence_policy"));n=max(len(c),1);means={f:round(sum(N(x.get(f)) for x in c)/n,8) for f in METRICS};maximums={f:round(max((N(x.get(f)) for x in c),default=0),8) for f in METRICS};trends={f:round(N(c[-1].get(f))-N(c[0].get(f)),8) if c else 0 for f in METRICS};fair=[N(x.get("fairness_preservation_ratio")) for x in c];lat=round(sum(N(x.get("latency_delta_ratio")) for x in c),8);div=round(sum(N(x.get("output_divergence_score")) for x in c),8);decay=round(max(0,fair[0]-min(fair)),8) if fair else 1;breach=sum(not (x.get("raw_payload_stored") is False and x.get("live_response_influenced") is False and x.get("feedback_to_live_path_enabled") is False and x.get("routing_activated") is False and x.get("external_actuation_enabled") is False and x.get("world_update_enabled") is False and x.get("winner_selected") is False and x.get("policy_boundary_preserved") is True) for x in c)
 dg={"allocation_drift_bounded":means["allocation_drift"]<=N(q.get("maximum_mean_allocation_drift")),"fairness_preservation_sufficient":min(fair,default=0)>=N(q.get("minimum_fairness_preservation_ratio")),"fairness_decay_bounded":decay<=N(q.get("maximum_fairness_decay")),"schedule_agreement_sufficient":min((N(x.get("schedule_agreement_ratio")) for x in c),default=0)>=N(q.get("minimum_schedule_agreement_ratio"))}
 sg={"mean_latency_bounded":means["latency_delta_ratio"]<=N(q.get("maximum_mean_latency_delta_ratio")),"cumulative_latency_bounded":lat<=N(q.get("maximum_cumulative_latency_delta_ratio")),"mean_output_divergence_bounded":means["output_divergence_score"]<=N(q.get("maximum_mean_output_divergence_score")),"cumulative_output_divergence_bounded":div<=N(q.get("maximum_cumulative_output_divergence_score")),"redaction_stable":maximums["redaction_failure_ratio"]<=N(q.get("maximum_redaction_failure_ratio")),"live_response_noninterference_sustained":maximums["live_response_influence_ratio"]<=N(q.get("maximum_live_response_influence_ratio")),"mirror_delivery_stable":maximums["mirror_delivery_failure_ratio"]<=N(q.get("maximum_mirror_delivery_failure_ratio")),"replica_restore_sustained":min((N(x.get("replica_restore_ratio")) for x in c),default=0)>=N(q.get("minimum_replica_restore_ratio")),"deterministic_replay_sustained":min((N(x.get("deterministic_replay_ratio")) for x in c),default=0)>=N(q.get("minimum_deterministic_replay_ratio")),"noninterference_boundary_preserved":breach==0}
 return {"evidence_cycle_count":len(c),"metric_means":means,"metric_maximums":maximums,"metric_trends":trends,"cumulative_latency_delta_ratio":lat,"cumulative_output_divergence_score":div,"fairness_decay":decay,"boundary_breach_count":breach,"diversity_gates":dg,"stability_gates":sg,"all_gates":{**dg,**sg}}
def evaluate(a:Mapping[str,Any],d:str)->tuple[str,str]:
 dg=M(a.get("diversity_gates"));sg=M(a.get("stability_gates"))
 if d in {"quarantine_recommended","rollback_recommended","hold_for_observation"}:return d,f"source_v0_22_{d}"
 if int(a.get("boundary_breach_count",0))>0:return "quarantine_recommended","longitudinal_live_noninterference_boundary_breach"
 if d=="restore_shadow_diversity_recommended":return d,"source_v0_22_diversity_restoration_required"
 if d=="extend_longitudinal_observation_recommended":return "extend_mirror_observation_recommended","source_v0_22_more_mirror_evidence_required"
 if d=="redesign_mirror_observation_admission_recommended":return "redesign_longitudinal_mirror_observation_recommended","source_v0_22_mirror_admission_redesign_required"
 if d=="mirror_observation_admission_ready" and not all(v is True for v in dg.values()):return "restore_shadow_diversity_recommended","longitudinal_fairness_or_allocation_drift_failed"
 if d=="mirror_observation_admission_ready" and all(v is True for v in sg.values()):return "longitudinal_mirror_noninterference_ready","sustained_mirror_noninterference_without_cumulative_drift_observed"
 if d=="mirror_observation_admission_ready":return "redesign_longitudinal_mirror_observation_recommended","longitudinal_stability_gate_failed"
 return "quarantine_recommended","unknown_source_v0_22_decision"

@dataclass(frozen=True)
class Result:
 version:str;status:str;packet_id:str;runtime_root:str;evidence_program_id:str;evidence_run_id:str;world_model_id:str;source_mirror_decision:str;decision:str;recommendation_only:bool;live_response_influenced:bool;source_world_state_digest:str;source_mirror_summary_digest:str;source_mirror_state_digest:str;source_mirror_recommendation_digest:str;longitudinal_mirror_report_digest:str;longitudinal_mirror_state_digest:str;ledger_record_digest:str;blockers:list[str]

def build_longitudinal_mirror_noninterference(*,runtime_context:Mapping[str,Any],longitudinal_mirror_plan:Mapping[str,Any],longitudinal_mirror_license:Mapping[str,Any],longitudinal_mirror_report:Mapping[str,Any])->Result:
 c=M(runtime_context);p=dict(M(longitudinal_mirror_plan));lic=M(longitudinal_mirror_license);r=dict(M(longitudinal_mirror_report));b=[];rv=c.get("runtime_root");root=pathlib.Path(str(rv)).expanduser().resolve() if rv else pathlib.Path(".").resolve()
 if not rv or root==pathlib.Path("/").resolve():b.append("runtime_root_invalid")
 if c.get("indra_qi_longitudinal_mirror_noninterference_v0_23_enabled") is not True or c.get("apply_indra_qi_longitudinal_mirror_noninterference_v0_23") is not True:b.append("longitudinal_mirror_not_enabled")
 validate_plan(p,b);w=read(root/"ku_indra_qi_noncommutative_mandala_world_state.json");su=read(root/"indra_qi_licensed_mirror_observation_admission_summary_v0_22.json");st=read(root/"indra_qi_licensed_mirror_observation_admission_state_v0_22.json");rec0=read(root/"indra_qi_licensed_mirror_observation_admission_recommendation_v0_22.json");src=validate_sources(w,su,st,rec0,p,b);cycles=validate_report(r,p,src,b);validate_license(lic,p,r,src,b)
 program=str(p.get("evidence_program_id",""));run=str(p.get("evidence_run_id",""));wid=str(p.get("world_model_id",""));lp=root/"indra_qi_longitudinal_mirror_noninterference_ledger_v0_23.jsonl";prior=readl(lp);prev="GENESIS"
 for i,row in enumerate(prior):
  if row.get("_invalid") or row.get("version")!=LEDGER_VERSION or not valid_digest(row,"record_digest") or row.get("prev_record_digest")!=prev or row.get("evidence_program_id")!=program or row.get("world_model_id")!=wid:b.append(f"longitudinal_mirror_ledger_record_{i}_invalid")
  prev=str(row.get("record_digest",""))
 pair=(str(src.get("summary_digest","")),str(src.get("recommendation_digest","")));rs=str(r.get("longitudinal_mirror_report_digest",""))
 if any(x.get("evidence_run_id")==run or (x.get("source_mirror_summary_digest"),x.get("source_mirror_recommendation_digest"))==pair or x.get("longitudinal_mirror_report_digest")==rs for x in prior):b.append("longitudinal_mirror_replay_detected")
 ps=read(root/"indra_qi_longitudinal_mirror_noninterference_state_v0_23.json")
 if ps and not valid_digest(ps,"longitudinal_mirror_state_digest"):b.append("longitudinal_mirror_prior_state_digest_invalid")
 a=analyze(cycles,p);decision,reason=evaluate(a,str(src.get("source_decision","")))
 if decision not in DECISIONS:b.append("longitudinal_mirror_decision_invalid")
 if b:decision="quarantine_recommended";reason="fail_closed_on_validation_or_integrity_loss"
 now=int(time.time());sf={"source_world_state_digest":str(src.get("world_digest","")),"source_mirror_summary_digest":str(src.get("summary_digest","")),"source_mirror_state_digest":str(src.get("state_digest","")),"source_mirror_recommendation_digest":str(src.get("recommendation_digest","")),"longitudinal_mirror_report_digest":rs};out={"version":"indra_qi_longitudinal_mirror_noninterference_summary_v0_23","evidence_program_id":program,"evidence_run_id":run,"world_model_id":wid,"source_mirror_decision":str(src.get("source_decision","")),**sf,"longitudinal_analysis":a,"raw_payload_stored":False,"live_response_influenced":False,"feedback_to_live_path_enabled":False,"routing_activated":False,"winner_selected":False,"external_actuation_enabled":False,"world_update_enabled":False,"recommendation_only":True,"epoch":now};out["longitudinal_mirror_summary_digest"]=sha(out)
 rec={"version":"indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23","evidence_program_id":program,"evidence_run_id":run,"world_model_id":wid,"source_mirror_decision":str(src.get("source_decision","")),"decision":decision,"decision_reasons":[reason],"longitudinal_noninterference_ready":decision=="longitudinal_mirror_noninterference_ready","live_response_influenced":False,"routing_activated":False,"winner_selected":False,"longitudinal_mirror_summary_digest":out["longitudinal_mirror_summary_digest"],"longitudinal_analysis":a,**sf,"recommendation_only":True,"direct_live_response_influence_authority":False,"direct_feedback_to_live_path_authority":False,"direct_routing_activation_authority":False,"direct_winner_selection_authority":False,"direct_lineage_selection_authority":False,"direct_lineage_execution_authority":False,"direct_world_update_authority":False,"direct_external_actuation_authority":False,"direct_promotion_authority":False,"direct_rollback_authority":False,"direct_quarantine_authority":False,"truth_authority":False,"boundary":dict(REQUIRED_BOUNDARY),"epoch":now};rec["longitudinal_mirror_recommendation_digest"]=sha(rec)
 ledger={"version":LEDGER_VERSION,"record_type":"longitudinal_mirror_noninterference_evidence","evidence_program_id":program,"evidence_run_id":run,"world_model_id":wid,**sf,"source_mirror_decision":str(src.get("source_decision","")),"longitudinal_mirror_summary_digest":out["longitudinal_mirror_summary_digest"],"longitudinal_analysis":a,"decision":decision,"live_response_influenced":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True,"prev_record_digest":str(prior[-1].get("record_digest","GENESIS")) if prior else "GENESIS","epoch":now};ledger["record_digest"]=sha(ledger)
 state={"version":STATE_VERSION,"evidence_program_id":program,"world_model_id":wid,"last_evidence_run_id":run,"last_source_mirror_state_digest":sf["source_mirror_state_digest"],"latest_longitudinal_mirror_decision":decision,"latest_longitudinal_mirror_summary_digest":out["longitudinal_mirror_summary_digest"],"latest_longitudinal_record_digest":ledger["record_digest"],"prev_longitudinal_mirror_state_digest":str(ps.get("longitudinal_mirror_state_digest","GENESIS")) if ps else "GENESIS","boundary":{"live_response_influenced":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True},"epoch":now};state["longitudinal_mirror_state_digest"]=state_digest(state)
 status=READY if not b else BLOCKED;receipt={"version":"indra_qi_longitudinal_mirror_noninterference_v0_23","status":status,"evidence_program_id":program,"evidence_run_id":run,"world_model_id":wid,"source_mirror_decision":str(src.get("source_decision","")),"decision":decision,"live_response_influenced":False,"routing_activated":False,"winner_selected":False,"recommendation_only":True,**sf,"longitudinal_mirror_summary_digest":out["longitudinal_mirror_summary_digest"] if not b else "","longitudinal_mirror_state_digest":state["longitudinal_mirror_state_digest"] if not b else str(ps.get("longitudinal_mirror_state_digest","")),"ledger_record_digest":ledger["record_digest"] if not b else "","blockers":b,"epoch":now};receipt["packet_id"]="indra-qi-longitudinal-mirror-noninterference-"+sha(receipt)[:16]
 if not b:write(root/"indra_qi_longitudinal_mirror_noninterference_summary_v0_23.json",out);write(root/"indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23.json",rec);write(root/"indra_qi_longitudinal_mirror_noninterference_state_v0_23.json",state);append(lp,ledger)
 if lic.get("receipt_write_allowed") is True:write(root/"indra_qi_longitudinal_mirror_noninterference_receipt_v0_23.json",receipt)
 if lic.get("audit_append_allowed") is True:append(root/"indra_qi_longitudinal_mirror_noninterference_audit_v0_23.jsonl",{**receipt,"audit_record_digest":sha(receipt)})
 return Result("indra_qi_longitudinal_mirror_noninterference_v0_23",status,str(receipt["packet_id"]),str(root),program,run,wid,str(src.get("source_decision","")),decision,True,False,sf["source_world_state_digest"],sf["source_mirror_summary_digest"],sf["source_mirror_state_digest"],sf["source_mirror_recommendation_digest"],rs,state["longitudinal_mirror_state_digest"] if not b else str(ps.get("longitudinal_mirror_state_digest","")),ledger["record_digest"] if not b else "",b)
