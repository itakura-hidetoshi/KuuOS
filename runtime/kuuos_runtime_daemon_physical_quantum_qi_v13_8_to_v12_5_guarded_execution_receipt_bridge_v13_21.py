#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json, os, pathlib, time
from typing import Any, Mapping

STATUSES={"guarded_execution_intent_ready":("transition_candidate_envelope_ready","transition_precheck_admit_candidate"),"guarded_execution_intent_hold":("transition_candidate_envelope_hold","transition_precheck_hold_candidate"),"guarded_execution_intent_block":("transition_candidate_envelope_block","transition_precheck_block_candidate")}
REQ_PACKET=("guarded_execution_intent_only","execution_layer_entrypoint","no_dry_run_required","transition_candidate_envelope_required","history_bearing_process_tensor","non_markov_context_required","multi_time_window_required","finite_horizon_only","memory_kernel_visible","requires_guarded_execution_license","intent_not_world_mutation","does_not_start_next_cycle","does_not_mutate_external_state","does_not_commit_plan","does_not_consume_memory","does_not_promote_truth","candidate_weighting_not_truth","fail_closed_on_boundary_loss")
REQ_INTENT=("guarded_execution_intent_only","execution_layer_entrypoint","no_dry_run_required","requires_guarded_execution_license","intent_not_world_mutation","does_not_start_next_cycle","does_not_mutate_external_state","does_not_consume_memory","does_not_promote_truth")
CTX=("process_tensor_digest","memory_kernel_digest","history_window_digest","instrument_trace_digest","non_markov_context_digest")

@dataclass(frozen=True)
class PhysicalQuantumQiV13_8ToV12_5GuardedExecutionReceiptBridgeResult:
    version:str; status:str; packet_id:str; runtime_root:str; bridge_status:str; execution_intent_status:str; envelope_status:str; transition_precheck_decision:str; intent_count:int; receipt_ready_state_written:bool; bridge_ledger_appended:bool; receipt_ready_state_path:str; bridge_ledger_path:str; summary_path:str; receipt_path:str; audit_path:str; blockers:list[str]; warnings:list[str]
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

def _read(p:pathlib.Path)->dict[str,Any]:
    if not p.is_file(): return {}
    try: x=json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError: return {}
    return x if isinstance(x,dict) else {}

def _write(p:pathlib.Path,x:Mapping[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(dict(x),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(t,p)

def _append(p:pathlib.Path,x:Mapping[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as h: h.write(json.dumps(dict(x),ensure_ascii=False,sort_keys=True)+"\n")

def _prev(p:pathlib.Path)->str:
    if not p.is_file(): return "GENESIS"
    last=""
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip(): last=line
    if not last: return "GENESIS"
    try: x=json.loads(last)
    except json.JSONDecodeError: return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(x.get("record_digest",_sha(x)))

def _ctx(c:Mapping[str,Any],b:list[str])->dict[str,str]:
    out={k:str(c.get(k,"")) for k in CTX}
    for k,v in out.items():
        if not v: b.append(f"process_tensor_context_{k}_missing")
    return out

def _weight_ok(w:Mapping[str,Any],idx:int,b:list[str])->dict[str,Any]:
    weight=dict(_m(w)); delta=_int(weight.get("path_weight_delta")); probe=weight.get("probe_potential_required") is True; barrier=weight.get("barrier_potential_required") is True; blocks=weight.get("barrier_blocks_ready_weight") is True
    if delta<=0: b.append(f"guarded_execution_intent_{idx}_without_positive_delta")
    if probe or barrier or blocks: b.append(f"guarded_execution_intent_{idx}_with_probe_or_barrier")
    return weight

def _intent_ok(intent:Mapping[str,Any],idx:int,context:Mapping[str,str],b:list[str])->dict[str,Any]:
    bd=_m(intent.get("boundary"))
    for f in REQ_INTENT:
        if bd.get(f) is not True: b.append(f"guarded_execution_intent_{idx}_boundary_{f}_missing")
    if intent.get("intent_type")!="physical_quantum_qi_guarded_execution_intent": b.append(f"guarded_execution_intent_{idx}_type_invalid")
    if _int(intent.get("intent_index"))!=idx: b.append(f"guarded_execution_intent_{idx}_index_mismatch")
    if intent.get("transition_precheck_decision")!="transition_precheck_admit_candidate": b.append(f"guarded_execution_intent_{idx}_precheck_decision_invalid")
    if intent.get("corridor_stability_gate_decision")!="corridor_stability_admit": b.append(f"guarded_execution_intent_{idx}_stability_decision_invalid")
    ictx=dict(_m(intent.get("process_tensor_context")))
    for k,v in context.items():
        if not ictx.get(k): b.append(f"guarded_execution_intent_{idx}_{k}_missing")
        elif str(ictx.get(k))!=v: b.append(f"guarded_execution_intent_{idx}_{k}_mismatch")
    return {"intent_type":str(intent.get("intent_type","")),"intent_index":idx,"candidate_id":str(intent.get("candidate_id","")),"transition_precheck_decision":str(intent.get("transition_precheck_decision","")),"corridor_stability_gate_decision":str(intent.get("corridor_stability_gate_decision","")),"candidate_weighting":_weight_ok(_m(intent.get("candidate_weighting")),idx,b),"process_tensor_context":ictx,"source_transition_candidate_envelope_digest":str(intent.get("source_transition_candidate_envelope_digest","")),"guarded_execution_intent_digest":str(intent.get("guarded_execution_intent_digest",_sha(dict(intent))))}

def _packet_ok(p:Mapping[str,Any],b:list[str],w:list[str])->dict[str,Any]:
    if not p: b.append("guarded_execution_intent_packet_missing_or_invalid"); return {}
    if p.get("physical_quantum_qi_guarded_execution_intent_considered") is not True: b.append("guarded_execution_intent_considered_not_true")
    bd=_m(p.get("boundary"))
    for f in REQ_PACKET:
        if bd.get(f) is not True: b.append(f"guarded_execution_intent_boundary_{f}_missing")
    status=str(p.get("execution_intent_status","guarded_execution_intent_block"))
    if status not in STATUSES: b.append("guarded_execution_intent_status_invalid"); status="guarded_execution_intent_block"
    env,pre=STATUSES[status]
    if str(p.get("envelope_status",""))!=env: b.append("guarded_execution_intent_envelope_status_mismatch")
    if str(p.get("transition_precheck_decision",""))!=pre: b.append("guarded_execution_intent_precheck_decision_mismatch")
    context=_ctx(_m(p.get("process_tensor_context")),b)
    intents=[dict(_m(i)) for i in p.get("guarded_execution_intents",[]) ] if isinstance(p.get("guarded_execution_intents"),list) else []
    intent_count=_int(p.get("intent_count")); envelope_count=_int(p.get("envelope_count"))
    if intent_count!=len(intents): b.append("guarded_execution_intent_count_mismatch")
    if status=="guarded_execution_intent_ready" and (intent_count<=0 or envelope_count<=0): b.append("guarded_execution_intent_ready_without_intents")
    if status!="guarded_execution_intent_ready" and intent_count!=0: b.append("guarded_execution_intent_hold_or_block_with_intents")
    clean=[_intent_ok(i,idx,context,b) for idx,i in enumerate(intents)]
    if not p.get("guarded_execution_intent_packet_digest"): w.append("guarded_execution_intent_packet_digest_missing")
    return {"execution_intent_status":status,"envelope_status":env,"transition_precheck_decision":pre,"intent_count":len(clean),"envelope_count":envelope_count,"guarded_execution_intents":clean,"process_tensor_context":context,"source_guarded_execution_intent_packet_digest":str(p.get("guarded_execution_intent_packet_digest",_sha(dict(p))))}

def build_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge(*,runtime_context:Mapping[str,Any],v13_8_to_v12_5_guarded_execution_receipt_bridge_license:Mapping[str,Any])->PhysicalQuantumQiV13_8ToV12_5GuardedExecutionReceiptBridgeResult:
    ctx,lic=_m(runtime_context),_m(v13_8_to_v12_5_guarded_execution_receipt_bridge_license); b:list[str]=[]; w:list[str]=[]; root=_root(ctx.get("runtime_root"),b)
    packet=root/"physical_quantum_qi_guarded_execution_intent_packet.json"; ready=root/"physical_quantum_qi_v12_5_guarded_execution_intent_receipt_ready_state.json"; blog=root/"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_ledger.jsonl"; summary=root/"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_summary.json"; receipt=root/"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_receipt.json"; audit=root/"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_audit.jsonl"
    if ctx.get("physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_enabled") is not True: b.append("physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge") is not True: b.append("apply_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_not_true")
    if lic.get("license_status")!="PHYSICAL_QUANTUM_QI_V13_8_TO_V12_5_GUARDED_EXECUTION_RECEIPT_BRIDGE_LICENSE_READY": b.append("physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_license_not_ready")
    for n in ["v13_8_compat_guarded_execution_intent_packet_read_allowed","v12_5_receipt_ready_state_write_allowed","bridge_ledger_append_allowed","summary_write_allowed","receipt_write_allowed","audit_append_allowed"]:
        if lic.get(n) is not True: b.append(n.replace("allowed","not_allowed"))
    payload=_packet_ok(_read(packet),b,w); written=appended=False
    if not b:
        epoch=int(time.time()); bs="v13_8_to_v12_5_guarded_execution_receipt_bridge_"+payload["execution_intent_status"].rsplit("_",1)[-1]
        rs={"version":"physical_quantum_qi_v12_5_guarded_execution_intent_receipt_ready_state_v13_21","v12_5_guarded_execution_intent_receipt_ready_state":True,"bridge_status":bs,**payload,"boundary":{"v12_5_receipt_ready_state_only":True,"v13_8_compat_guarded_execution_intent_packet_required":True,"can_feed_v12_5_guarded_execution_intent_receipt_ledger":True,"execution_layer_entrypoint":True,"no_dry_run_required":True,"candidate_weighting_not_truth":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"bridge_not_direct_receipt_append":True,"does_not_run_v12_5_receipt_ledger":True,"does_not_mutate_external_state":True,"does_not_start_next_cycle":True,"fail_closed_on_boundary_loss":True},"epoch":epoch}
        rs["v12_5_receipt_ready_state_digest"]=_sha(rs); _write(ready,rs); written=True
        rec={"version":"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_record_v13_21","record_type":"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge","bridge_status":bs,"source_v12_5_receipt_ready_state_digest":rs["v12_5_receipt_ready_state_digest"],"source_guarded_execution_intent_packet_digest":payload["source_guarded_execution_intent_packet_digest"],"prev_record_digest":_prev(blog),"boundary":{"bridge_receipt_only":True,"v12_5_receipt_ready_state_traceable":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"replayable_receipt":True},"epoch":epoch,**{k:payload[k] for k in ["execution_intent_status","envelope_status","transition_precheck_decision","intent_count"]}}
        rec["record_digest"]=_sha(rec); _append(blog,rec); appended=True
        sm={"version":"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_summary_v13_21","bridge_status":bs,"v12_5_receipt_ready_state_digest":rs["v12_5_receipt_ready_state_digest"],"boundary":{"summary_only":True,"can_feed_v12_5_guarded_execution_intent_receipt_ledger":True,"candidate_weighting_not_truth":True},"epoch":epoch,**{k:payload[k] for k in ["execution_intent_status","envelope_status","transition_precheck_decision","intent_count"]}}
        sm["summary_digest"]=_sha(sm); _write(summary,sm)
    else: bs="v13_8_to_v12_5_guarded_execution_receipt_bridge_block"
    status="PHYSICAL_QUANTUM_QI_V13_8_TO_V12_5_GUARDED_EXECUTION_RECEIPT_BRIDGE_READY" if not b else "PHYSICAL_QUANTUM_QI_V13_8_TO_V12_5_GUARDED_EXECUTION_RECEIPT_BRIDGE_BLOCKED"
    exec_status=str(payload.get("execution_intent_status","guarded_execution_intent_block")); env,pre=STATUSES.get(exec_status,STATUSES["guarded_execution_intent_block"]); count=_int(payload.get("intent_count")); pid="physical-quantum-qi-v13-8-to-v12-5-guarded-execution-receipt-bridge-"+_sha({"payload":payload,"blockers":b})[:16]
    rc={"version":"kuuos_runtime_daemon_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_v13_21","status":status,"packet_id":pid,"bridge_status":bs,"execution_intent_status":exec_status,"envelope_status":env,"transition_precheck_decision":pre,"intent_count":count,"receipt_ready_state_written":written,"bridge_ledger_appended":appended,"blockers":b,"warnings":w,"epoch":int(time.time())}
    if lic.get("receipt_write_allowed") is True: _write(receipt,rc)
    if lic.get("audit_append_allowed") is True: _append(audit,{**rc,"audit_record_digest":_sha(rc)})
    return PhysicalQuantumQiV13_8ToV12_5GuardedExecutionReceiptBridgeResult("kuuos_runtime_daemon_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_v13_21",status,pid,str(root),bs,exec_status,env,pre,count,written,appended,str(ready),str(blog),str(summary),str(receipt),str(audit),b,w)
