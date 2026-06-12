#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json, os, pathlib, time
from typing import Any, Mapping

STATUS_TO_V12={"guarded_execution_intent_ready":("transition_candidate_envelope_ready","transition_precheck_admit_candidate"),"guarded_execution_intent_hold":("transition_candidate_envelope_hold","transition_precheck_hold_candidate"),"guarded_execution_intent_block":("transition_candidate_envelope_block","transition_precheck_block_candidate")}
REQ=("receipt_ledger_only","guarded_intent_bridge_receipt_only","guarded_execution_intent_packet_traceable","guarded_execution_intent_bridge_state_traceable","uses_process_tensor_feedback","non_markov_feedback_preserved","history_window_feedback_preserved","memory_kernel_feedback_preserved","external_backaction_visible","candidate_weighting_not_truth","bridge_not_direct_execution","replayable_receipt","fail_closed_on_boundary_loss")
CTX=("process_tensor_digest","memory_kernel_digest","history_window_digest","instrument_trace_digest","non_markov_context_digest")

@dataclass(frozen=True)
class PhysicalQuantumQiV13_7ToV13_8CompatibilityBridgeResult:
    version:str; status:str; packet_id:str; runtime_root:str; compatibility_bridge_status:str; execution_intent_status:str; v12_5_envelope_status:str; v12_5_precheck_decision:str; intent_count:int; compatibility_ready_state_written:bool; bridge_ledger_appended:bool; compatibility_ready_state_path:str; bridge_ledger_path:str; summary_path:str; receipt_path:str; audit_path:str; blockers:list[str]; warnings:list[str]
    def to_dict(self)->dict[str,Any]: return asdict(self)

def _m(v:Any)->Mapping[str,Any]: return v if isinstance(v,Mapping) else {}
def _sha(v:Any)->str: return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def _int(v:Any)->int:
    try: return int(v or 0)
    except (TypeError,ValueError): return 0

def _root(v:Any,b:list[str])->pathlib.Path:
    if not v: b.append("runtime_root_missing"); return pathlib.Path(".").resolve()
    p=pathlib.Path(str(v)).expanduser().resolve()
    if p==pathlib.Path("/").resolve(): b.append("runtime_root_forbidden")
    return p

def _write(p:pathlib.Path,x:Mapping[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(dict(x),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(t,p)

def _append(p:pathlib.Path,x:Mapping[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as h: h.write(json.dumps(dict(x),ensure_ascii=False,sort_keys=True)+"\n")

def _latest(p:pathlib.Path,b:list[str])->dict[str,Any]:
    if not p.is_file(): b.append("guarded_intent_bridge_receipt_ledger_missing"); return {}
    last=""
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip(): last=line
    if not last: b.append("guarded_intent_bridge_receipt_ledger_empty"); return {}
    try: x=json.loads(last)
    except json.JSONDecodeError: b.append("guarded_intent_bridge_receipt_ledger_latest_line_invalid"); return {}
    return x if isinstance(x,dict) else {}

def _prev(p:pathlib.Path)->str:
    if not p.is_file(): return "GENESIS"
    last=""
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip(): last=line
    if not last: return "GENESIS"
    try: x=json.loads(last)
    except json.JSONDecodeError: return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(x.get("record_digest",_sha(x)))

def _weight(w:Mapping[str,Any])->dict[str,Any]:
    return {"path_weight_delta":_int(w.get("path_weight_delta")),"probe_potential_required":w.get("probe_potential_required") is True,"barrier_potential_required":w.get("barrier_potential_required") is True,"barrier_blocks_ready_weight":w.get("barrier_blocks_ready_weight") is True,"memory_feedback_weight":_int(w.get("memory_feedback_weight")),"external_backaction_weight":_int(w.get("external_backaction_weight")),"next_cycle_amplitude_delta":_int(w.get("next_cycle_amplitude_delta"))}

def _ctx(c:Mapping[str,Any],b:list[str])->dict[str,str]:
    out={k:str(c.get(k,"")) for k in CTX}
    for k,v in out.items():
        if not v: b.append(f"process_tensor_context_{k}_missing")
    return out

def _validate(r:Mapping[str,Any],b:list[str])->dict[str,Any]:
    if not r: return {}
    if r.get("record_type")!="physical_quantum_qi_guarded_intent_bridge_receipt": b.append("guarded_intent_bridge_receipt_record_type_invalid")
    for f in REQ:
        if _m(r.get("boundary")).get(f) is not True: b.append(f"guarded_intent_bridge_receipt_boundary_{f}_missing")
    status=str(r.get("guarded_execution_intent_status","guarded_execution_intent_block"))
    if status not in STATUS_TO_V12: b.append("guarded_execution_intent_status_invalid"); status="guarded_execution_intent_block"
    envelope,precheck=STATUS_TO_V12[status]
    intents=r.get("guarded_execution_intents",[])
    if not isinstance(intents,list): b.append("guarded_execution_intents_not_list"); intents=[]
    count=_int(r.get("guarded_execution_intent_count"))
    if count!=len(intents): b.append("guarded_execution_intent_count_mismatch")
    if status=="guarded_execution_intent_ready" and count<=0: b.append("v13_8_compat_ready_requires_intent")
    if status!="guarded_execution_intent_ready" and count!=0: b.append("v13_8_compat_hold_or_block_with_intent")
    return {"execution_intent_status":status,"v12_5_envelope_status":envelope,"v12_5_precheck_decision":precheck,"intent_count":count,"guarded_execution_intents":[dict(_m(i)) for i in intents],"candidate_weighting":_weight(_m(r.get("candidate_weighting"))),"process_tensor_context":_ctx(_m(r.get("process_tensor_context")),b),"source_guarded_intent_bridge_receipt_digest":str(r.get("record_digest",_sha(dict(r)))),"source_guarded_execution_intent_packet_digest":str(r.get("source_guarded_execution_intent_packet_digest","")),"source_integrated_candidate_to_guarded_intent_bridge_digest":str(r.get("source_integrated_candidate_to_guarded_intent_bridge_digest",""))}

def build_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge(*,runtime_context:Mapping[str,Any],v13_7_to_v13_8_compatibility_bridge_license:Mapping[str,Any])->PhysicalQuantumQiV13_7ToV13_8CompatibilityBridgeResult:
    ctx,lic=_m(runtime_context),_m(v13_7_to_v13_8_compatibility_bridge_license); b:list[str]=[]; w:list[str]=[]; root=_root(ctx.get("runtime_root"),b)
    ledger=root/"physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl"; ready=root/"physical_quantum_qi_v13_8_guarded_intent_receipt_ledger_compatibility_bridge_ready_state.json"; blog=root/"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_ledger.jsonl"; summary=root/"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_summary.json"; receipt=root/"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_receipt.json"; audit=root/"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_audit.jsonl"
    if ctx.get("physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_enabled") is not True: b.append("physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge") is not True: b.append("apply_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_not_true")
    if lic.get("license_status")!="PHYSICAL_QUANTUM_QI_V13_7_TO_V13_8_COMPATIBILITY_BRIDGE_LICENSE_READY": b.append("physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_license_not_ready")
    for n in ["v13_7_guarded_intent_bridge_receipt_ledger_read_allowed","v13_8_compatibility_bridge_ready_state_write_allowed","bridge_ledger_append_allowed","summary_write_allowed","receipt_write_allowed","audit_append_allowed"]:
        if lic.get(n) is not True: b.append(n.replace("allowed","not_allowed"))
    payload=_validate(_latest(ledger,b),b); written=appended=False
    if not b:
        epoch=int(time.time()); compat="v13_7_to_v13_8_compatibility_bridge_"+payload["execution_intent_status"].rsplit("_",1)[-1]
        rs={"version":"physical_quantum_qi_v13_8_guarded_intent_receipt_ledger_compatibility_bridge_ready_state_v13_20","compatibility_bridge_ready_state":True,"compatibility_bridge_status":compat,**payload,"boundary":{"v13_8_compatibility_bridge_ready_state_only":True,"v13_7_guarded_intent_bridge_receipt_required":True,"can_feed_v13_8_guarded_intent_receipt_ledger_compatibility_bridge":True,"can_feed_v12_5_guarded_execution_intent_receipt_ledger_after_v13_8":True,"candidate_weighting_not_truth":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"bridge_not_direct_compatibility_execution":True,"does_not_run_compatibility_bridge":True,"does_not_write_v12_5_packet":True,"fail_closed_on_boundary_loss":True},"epoch":epoch}
        rs["compatibility_bridge_ready_state_digest"]=_sha(rs); _write(ready,rs); written=True
        rec={"version":"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_record_v13_20","record_type":"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge","compatibility_bridge_status":compat,"source_compatibility_bridge_ready_state_digest":rs["compatibility_bridge_ready_state_digest"],"source_guarded_intent_bridge_receipt_digest":payload["source_guarded_intent_bridge_receipt_digest"],"prev_record_digest":_prev(blog),"boundary":{"bridge_receipt_only":True,"v13_8_compatibility_bridge_ready_state_traceable":True,"same_semantic_root":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"replayable_receipt":True},"epoch":epoch,**{k:payload[k] for k in ["execution_intent_status","v12_5_envelope_status","v12_5_precheck_decision","intent_count"]}}
        rec["record_digest"]=_sha(rec); _append(blog,rec); appended=True
        sm={"version":"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_summary_v13_20","compatibility_bridge_status":compat,"compatibility_bridge_ready_state_digest":rs["compatibility_bridge_ready_state_digest"],"boundary":{"summary_only":True,"can_feed_v13_8_guarded_intent_receipt_ledger_compatibility_bridge":True,"candidate_weighting_not_truth":True},"epoch":epoch,**{k:payload[k] for k in ["execution_intent_status","v12_5_envelope_status","v12_5_precheck_decision","intent_count"]}}
        sm["summary_digest"]=_sha(sm); _write(summary,sm)
    else: compat="v13_7_to_v13_8_compatibility_bridge_block"
    status="PHYSICAL_QUANTUM_QI_V13_7_TO_V13_8_COMPATIBILITY_BRIDGE_READY" if not b else "PHYSICAL_QUANTUM_QI_V13_7_TO_V13_8_COMPATIBILITY_BRIDGE_BLOCKED"
    exec_status=str(payload.get("execution_intent_status","guarded_execution_intent_block")); env,pre=STATUS_TO_V12.get(exec_status,STATUS_TO_V12["guarded_execution_intent_block"]); count=_int(payload.get("intent_count"))
    pid="physical-quantum-qi-v13-7-to-v13-8-compatibility-bridge-"+_sha({"payload":payload,"blockers":b})[:16]
    rc={"version":"kuuos_runtime_daemon_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_v13_20","status":status,"packet_id":pid,"compatibility_bridge_status":compat,"execution_intent_status":exec_status,"v12_5_envelope_status":env,"v12_5_precheck_decision":pre,"intent_count":count,"compatibility_ready_state_written":written,"bridge_ledger_appended":appended,"blockers":b,"warnings":w,"epoch":int(time.time())}
    if lic.get("receipt_write_allowed") is True: _write(receipt,rc)
    if lic.get("audit_append_allowed") is True: _append(audit,{**rc,"audit_record_digest":_sha(rc)})
    return PhysicalQuantumQiV13_7ToV13_8CompatibilityBridgeResult("kuuos_runtime_daemon_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_v13_20",status,pid,str(root),compat,exec_status,env,pre,count,written,appended,str(ready),str(blog),str(summary),str(receipt),str(audit),b,w)
