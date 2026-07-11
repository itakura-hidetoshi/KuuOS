#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
CONSTRAINT_FIELDS={"planning_horizon","maximum_plan_steps","maximum_branching_factor","maximum_revision_cycles","reversible_actions_required","irreversible_step_requires_checkpoint","stop_condition_digests","forbidden_effects"}
PLAN_FIELDS={"plan_id","plan_revision","selected_candidate_id","selected_candidate_plan_intent_digest","world_state_dependency_digest","stop_condition_digests","retained_alternative_records","preserved_evidence_lineage_digests","steps"}
STEP_FIELDS={"step_id","sequence_index","action_class","action_spec_digest","precondition_digests","expected_effect_digests","effect_tags","evidence_lineage_digests","stop_condition_digests","reversible","irreversible","checkpoint_step_id","branch_ids"}
ALT_FIELDS={"candidate_id","nonselection_reason_digest","retained_for_revision"}
ACTIONS={"analyze","condition_reassessment","evidence_collection","hold","prepare_reversible","request_revision","review_checkpoint","terminate"}
FORBIDDEN={"active_now","candidate_substitution","execution_permission","external_side_effect","persistent_world_mutation","selection_authority_transfer","tool_invocation","unreviewed_scope_expansion"}

@dataclass
class VerifyOSBoundedPlanMiddleWayVerificationResult:
    status:str; blockers:list[str]; certificate:dict|None

def canonical_digest(v:Any)->str:
    return sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def _sl(v:Any,empty=False):
    ok=isinstance(v,list) and (empty or bool(v)) and all(isinstance(x,str) and x for x in v) and v==sorted(v) and len(v)==len(set(v))
    return ok, list(v) if ok else []

def _map(s:Mapping[str,Any],fields:set[str]):
    x=[(k,dict(v)) for k,v in s.items() if isinstance(v,Mapping) and set(v)==fields]
    return x[0] if len(x)==1 else ("",{})

def _digest(s:Mapping[str,Any]):
    for k in ("planos_bounded_synthesis_receipt_digest","bounded_synthesis_receipt_digest","plan_receipt_digest"):
        if isinstance(s.get(k),str) and s[k]: return k,s[k]
    x=[(k,v) for k,v in s.items() if k.endswith("receipt_digest") and isinstance(v,str) and v]
    return x[0] if len(x)==1 else ("","")

def compute_verifyos_bounded_plan_verification_bundle_digest(**kw:Any)->str:
    return canonical_digest(kw)

def build_verifyos_bounded_plan_middle_way_verification_certificate(*,source_plan_receipt:Mapping[str,Any],expected_source_plan_receipt_digest:str,current_world_binding_digest:str,current_world_model_state_digest:str,current_world_model_revision:int,current_world_lineage_digest:str,expected_selected_candidate_id:str,expected_selected_candidate_plan_intent_digest:str,verification_policy_digest:str,verification_owner_responsibility_digest:str,verification_request_id:str,verification_bundle_digest:str)->VerifyOSBoundedPlanMiddleWayVerificationResult:
    b=[]; s=dict(source_plan_receipt) if isinstance(source_plan_receipt,Mapping) else {}
    texts=[expected_source_plan_receipt_digest,current_world_binding_digest,current_world_model_state_digest,current_world_lineage_digest,expected_selected_candidate_id,expected_selected_candidate_plan_intent_digest,verification_policy_digest,verification_owner_responsibility_digest,verification_request_id,verification_bundle_digest]
    if any(not isinstance(x,str) or not x for x in texts): b.append("required_text_missing")
    if not isinstance(current_world_model_revision,int) or isinstance(current_world_model_revision,bool) or current_world_model_revision<0:b.append("current_world_revision_invalid")
    if not s:return VerifyOSBoundedPlanMiddleWayVerificationResult(STATUS_BLOCKED,["source_plan_receipt_missing"],None)
    for k,v in {"kernel":"PlanOS Bounded Synthesis Receipt Kernel","kernel_version":"v0.1","planos_version":"v1.04"}.items():
        if s.get(k)!=v:b.append(f"source_{k}_invalid")
    dk,sd=_digest(s)
    if not dk:b.append("source_receipt_digest_missing")
    else:
        u=dict(s);u.pop(dk,None)
        if sd!=canonical_digest(u):b.append("source_receipt_digest_mismatch")
        if sd!=expected_source_plan_receipt_digest:b.append("source_receipt_binding_mismatch")
    for k in ("plan_synthesis_performed","concrete_plan_issued","plan_receipt_issued","finite_plan_constructed","selected_candidate_preserved","plan_intent_binding_preserved","world_state_dependency_preserved","branching_factor_bounded","revision_cycles_bounded","irreversible_steps_checkpoint_guarded","stop_conditions_preserved","forbidden_effects_absent","alternative_candidates_retained","dissent_evidence_preserved","minority_evidence_preserved","lineage_extended_not_replaced","responsibility_extended_not_replaced","plan_is_conditionally_binding","plan_is_not_absolute_command","plan_is_not_contentless_proposal","selection_remains_decisionos_owned","persistent_world_state_unchanged","world_model_prediction_not_truth","world_mutation_not_granted","history_read_only","qi_grants_no_authority","future_only"):
        if s.get(k) is not True:b.append(f"source_boundary_{k}_missing")
    for k in ("selection_authority_granted_to_planos","plan_activated","materialization_performed","execution_authority_granted","execution_permission","active_now"):
        if s.get(k) is not False:b.append(f"source_boundary_{k}_promoted")
    ck,c=_map(s,CONSTRAINT_FIELDS);pk,p=_map(s,PLAN_FIELDS)
    if not ck:b.append("constraints_missing")
    if not pk:b.append("plan_missing")
    stops=[];maxsteps=maxbranch=None
    if c:
        h,maxsteps,maxbranch,mr=[c.get(x) for x in ("planning_horizon","maximum_plan_steps","maximum_branching_factor","maximum_revision_cycles")]
        for n,v,lo,hi in (("horizon",h,1,64),("steps",maxsteps,1,32),("branches",maxbranch,1,8),("revisions",mr,0,8)):
            if not isinstance(v,int) or isinstance(v,bool) or not lo<=v<=hi:b.append(f"constraint_{n}_invalid")
        if isinstance(h,int) and isinstance(maxsteps,int) and maxsteps>h:b.append("steps_exceed_horizon")
        if c.get("reversible_actions_required") is not True or c.get("irreversible_step_requires_checkpoint") is not True:b.append("constraint_guards_missing")
        ok,stops=_sl(c.get("stop_condition_digests"));
        if not ok:b.append("constraint_stops_invalid")
        fx=c.get("forbidden_effects")
        if not isinstance(fx,list) or fx!=sorted(FORBIDDEN):b.append("forbidden_effect_set_invalid")
    evidence=[]
    if p:
        if p.get("plan_revision")!=0:b.append("plan_revision_invalid")
        if p.get("selected_candidate_id")!=expected_selected_candidate_id:b.append("candidate_mismatch")
        if p.get("selected_candidate_plan_intent_digest")!=expected_selected_candidate_plan_intent_digest:b.append("intent_mismatch")
        ok,ps=_sl(p.get("stop_condition_digests"));
        if not ok or ps!=stops:b.append("plan_stops_invalid")
        ok,evidence=_sl(p.get("preserved_evidence_lineage_digests"));
        if not ok:b.append("plan_evidence_invalid")
        alts=p.get("retained_alternative_records")
        if not isinstance(alts,list) or not alts:b.append("alternatives_empty")
        else:
            ids=[]
            for i,a in enumerate(alts):
                if not isinstance(a,Mapping) or set(a)!=ALT_FIELDS:b.append(f"alternative_schema_{i}");continue
                cid=a.get("candidate_id");ids.append(cid)
                if not isinstance(cid,str) or not cid or cid==expected_selected_candidate_id:b.append(f"alternative_candidate_{i}")
                if not isinstance(a.get("nonselection_reason_digest"),str) or not a.get("nonselection_reason_digest"):b.append(f"alternative_reason_{i}")
                if a.get("retained_for_revision") is not True:b.append(f"alternative_retention_{i}")
            if ids!=sorted(ids) or len(ids)!=len(set(ids)):b.append("alternatives_not_canonical")
        steps=p.get("steps")
        if not isinstance(steps,list) or not steps:b.append("steps_empty")
        else:
            if isinstance(maxsteps,int) and len(steps)>maxsteps:b.append("step_bound_exceeded")
            ids=[];acts=[];checks={};branches=set()
            for i,x in enumerate(steps,1):
                if not isinstance(x,Mapping) or set(x)!=STEP_FIELDS:b.append(f"step_schema_{i}");continue
                sid=x.get("step_id");act=x.get("action_spec_digest");ids.append(sid);acts.append(act)
                if not isinstance(sid,str) or not sid or not isinstance(act,str) or not act:b.append(f"step_identity_{i}")
                if x.get("sequence_index")!=i:b.append(f"step_sequence_{i}")
                cls=x.get("action_class")
                if cls not in ACTIONS:b.append(f"action_class_{i}")
                vals={}
                for f,e in (("precondition_digests",False),("expected_effect_digests",False),("effect_tags",False),("evidence_lineage_digests",False),("stop_condition_digests",False),("branch_ids",True)):
                    ok,v=_sl(x.get(f),e);vals[f]=v
                    if not ok:b.append(f"step_{f}_{i}")
                if set(vals["effect_tags"])&FORBIDDEN:b.append(f"forbidden_effect_{i}")
                if not set(vals["evidence_lineage_digests"]).issubset(evidence):b.append(f"evidence_outside_plan_{i}")
                if vals["stop_condition_digests"]!=stops:b.append(f"step_stops_{i}")
                if isinstance(maxbranch,int) and len(vals["branch_ids"])>maxbranch:b.append(f"branch_bound_{i}")
                branches.update(vals["branch_ids"])
                rev,ir,cp=x.get("reversible"),x.get("irreversible"),x.get("checkpoint_step_id")
                if (rev is True)==(ir is True):b.append(f"reversibility_{i}")
                if cls=="review_checkpoint" and isinstance(sid,str):checks[sid]=i
                if ir is True and (not isinstance(cp,str) or not cp or cp not in checks or checks[cp]>=i):b.append(f"checkpoint_{i}")
                if ir is not True and cp:b.append(f"unexpected_checkpoint_{i}")
            if len(ids)!=len(set(ids)):b.append("duplicate_step_id")
            if len(acts)!=len(set(acts)):b.append("duplicate_action_digest")
            if isinstance(maxbranch,int) and len(branches)>maxbranch:b.append("global_branch_bound")
    candidate=s.get("selected_candidate_id",p.get("selected_candidate_id"));intent=s.get("selected_candidate_plan_intent_digest",p.get("selected_candidate_plan_intent_digest"))
    if candidate!=expected_selected_candidate_id:b.append("top_candidate_mismatch")
    if intent!=expected_selected_candidate_plan_intent_digest:b.append("top_intent_mismatch")
    swb,sws,swr,swl=[s.get(x) for x in ("source_world_binding_digest","source_world_model_state_digest","source_world_model_revision","source_world_lineage_digest")]
    if not isinstance(swb,str) or not swb or not isinstance(sws,str) or not sws or not isinstance(swl,str) or not swl:b.append("source_world_binding_missing")
    if not isinstance(swr,int) or isinstance(swr,bool) or swr<0:b.append("source_world_revision_invalid")
    if p and p.get("world_state_dependency_digest")!=sws:b.append("world_dependency_mismatch")
    lists={}
    for k,e in (("resulting_lineage_digests",False),("resulting_responsibility_lineage_digests",False),("preserved_dissent_evidence_digests",True),("preserved_minority_evidence_digests",True)):
        ok,v=_sl(s.get(k),e);lists[k]=v
        if not ok:b.append(f"source_{k}_invalid")
    if not set(lists["preserved_dissent_evidence_digests"]).issubset(evidence):b.append("dissent_erased")
    if not set(lists["preserved_minority_evidence_digests"]).issubset(evidence):b.append("minority_erased")
    if not b:
        expected=compute_verifyos_bounded_plan_verification_bundle_digest(source_plan_receipt_digest=sd,expected_source_plan_receipt_digest=expected_source_plan_receipt_digest,current_world_binding_digest=current_world_binding_digest,current_world_model_state_digest=current_world_model_state_digest,current_world_model_revision=current_world_model_revision,current_world_lineage_digest=current_world_lineage_digest,expected_selected_candidate_id=expected_selected_candidate_id,expected_selected_candidate_plan_intent_digest=expected_selected_candidate_plan_intent_digest,verification_policy_digest=verification_policy_digest,verification_owner_responsibility_digest=verification_owner_responsibility_digest,verification_request_id=verification_request_id)
        if verification_bundle_digest!=expected:b.append("verification_bundle_digest_mismatch")
    if b:return VerifyOSBoundedPlanMiddleWayVerificationResult(STATUS_BLOCKED,sorted(set(b)),None)
    current=current_world_binding_digest==swb and current_world_model_state_digest==sws and current_world_model_revision==swr and current_world_lineage_digest==swl
    status="valid" if current else "revision_required";disp="bounded_plan_verified_for_materialization_intake" if current else "return_to_planos_revision"
    record={"source_plan_receipt_digest":sd,"source_world_binding_digest":swb,"source_world_model_state_digest":sws,"source_world_model_revision":swr,"source_world_lineage_digest":swl,"current_world_binding_digest":current_world_binding_digest,"current_world_model_state_digest":current_world_model_state_digest,"current_world_model_revision":current_world_model_revision,"current_world_lineage_digest":current_world_lineage_digest,"world_conditions_current":current,"conditional_validity_status":status,"verification_disposition":disp}
    cert={"kernel":"VerifyOS Bounded Plan Middle-Way Verification Kernel","kernel_version":"v0.1","verifyos_version":"v0.5","status":"VERIFYOS_BOUNDED_PLAN_MIDDLE_WAY_VERIFIED","source_planos_version":"v1.04","source_plan_receipt_digest":sd,"source_plan_receipt_digest_field":dk,"source_bounded_plan_field":pk,"source_synthesis_constraints_field":ck,"source_world_binding_digest":swb,"source_world_model_state_digest":sws,"source_world_model_revision":swr,"source_world_lineage_digest":swl,"current_world_binding_digest":current_world_binding_digest,"current_world_model_state_digest":current_world_model_state_digest,"current_world_model_revision":current_world_model_revision,"current_world_lineage_digest":current_world_lineage_digest,"selected_candidate_id":expected_selected_candidate_id,"selected_candidate_plan_intent_digest":expected_selected_candidate_plan_intent_digest,"verification_policy_digest":verification_policy_digest,"verification_owner_responsibility_digest":verification_owner_responsibility_digest,"verification_request_id":verification_request_id,"verification_bundle_digest":verification_bundle_digest,"verification_record":record,"verification_record_digest":canonical_digest(record),"conditional_validity_status":status,"verification_disposition":disp,"bounded_plan_verified_for_materialization_intake":current,"plan_revision_required":not current,"materialization_intake_admitted":current}
    for k in ("structural_verification_passed","source_receipt_digest_verified","finite_plan_verified","step_sequence_verified","step_bound_verified","branch_bound_verified","revision_bound_verified","checkpoint_order_verified","stop_conditions_verified","forbidden_effects_absent","selected_candidate_preserved","plan_intent_preserved","world_dependency_explicit","alternative_candidates_preserved","dissent_evidence_preserved","minority_evidence_preserved","source_lineage_preserved","source_responsibility_preserved","plan_remains_conditionally_binding","plan_not_reified","plan_not_erased","condition_change_routes_to_revision","selection_remains_decisionos_owned","persistent_world_state_unchanged","world_model_prediction_not_truth","world_mutation_not_granted","history_read_only","qi_grants_no_authority","future_only"):cert[k]=True
    for k in ("selection_authority_granted_to_verifyos","plan_revision_authority_granted_to_verifyos","plan_activated","materialization_performed","execution_authority_granted","execution_permission","active_now"):cert[k]=False
    cert["resulting_lineage_digests"]=sorted(set(lists["resulting_lineage_digests"])|{sd,canonical_digest(record),verification_bundle_digest})
    cert["resulting_responsibility_lineage_digests"]=sorted(set(lists["resulting_responsibility_lineage_digests"])|{verification_owner_responsibility_digest})
    cert["preserved_dissent_evidence_digests"]=lists["preserved_dissent_evidence_digests"]
    cert["preserved_minority_evidence_digests"]=lists["preserved_minority_evidence_digests"]
    cert["verifyos_bounded_plan_middle_way_verification_certificate_digest"]=canonical_digest(cert)
    return VerifyOSBoundedPlanMiddleWayVerificationResult(STATUS_READY,[],cert)
