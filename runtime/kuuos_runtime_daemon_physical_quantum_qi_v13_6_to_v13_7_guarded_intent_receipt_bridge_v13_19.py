#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json, os, pathlib, time
from typing import Any, Mapping

BRIDGE = {"integrated_candidate_to_guarded_intent_ready":("guarded_execution_intent_ready","emit_guarded_ready_intent"),"integrated_candidate_to_guarded_intent_hold":("guarded_execution_intent_hold","emit_guarded_hold_intent"),"integrated_candidate_to_guarded_intent_block":("guarded_execution_intent_block","emit_guarded_block_intent")}
REQ_BRIDGE=("integrated_candidate_to_guarded_intent_bridge_only","cycle_gate_reentry_integration_receipt_required","emits_guarded_execution_intent_packet","uses_process_tensor_feedback","non_markov_feedback_preserved","history_window_feedback_preserved","memory_kernel_feedback_preserved","external_backaction_visible","candidate_weighting_not_truth","bridge_not_direct_execution","does_not_run_runner","does_not_mutate_external_state","does_not_start_next_cycle","license_gated_bridge","fail_closed_on_boundary_loss")
REQ_INTENT_PACKET=("guarded_execution_intent_packet_only","from_integrated_candidate_bridge","requires_guarded_execution_license","candidate_weighting_not_truth","not_direct_execution_authority","does_not_run_runner","does_not_mutate_external_state")
REQ_STATE=("guarded_execution_intent_bridge_state_only","from_integrated_candidate_bridge","can_feed_guarded_execution_intent_receipt_layer","candidate_weighting_not_truth","not_direct_execution_authority")
REQ_CTX=("process_tensor_digest","memory_kernel_digest","history_window_digest","instrument_trace_digest","non_markov_context_digest")

@dataclass(frozen=True)
class PhysicalQuantumQiV13_6ToV13_7GuardedIntentReceiptBridgeResult:
    version:str; status:str; packet_id:str; runtime_root:str; bridge_status:str; guarded_execution_intent_status:str; guarded_intent_emit_action:str; guarded_execution_intent_count:int; receipt_ready_state_written:bool; bridge_ledger_appended:bool; receipt_ready_state_path:str; bridge_ledger_path:str; summary_path:str; receipt_path:str; audit_path:str; blockers:list[str]; warnings:list[str]
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
    p.parent.mkdir(parents=True,exist_ok=True); tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(dict(x),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(tmp,p)

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

def _weight(w:Mapping[str,Any])->dict[str,Any]:
    return {"path_weight_delta":_int(w.get("path_weight_delta")),"probe_potential_required":w.get("probe_potential_required") is True,"barrier_potential_required":w.get("barrier_potential_required") is True,"barrier_blocks_ready_weight":w.get("barrier_blocks_ready_weight") is True,"memory_feedback_weight":_int(w.get("memory_feedback_weight")),"external_backaction_weight":_int(w.get("external_backaction_weight")),"next_cycle_amplitude_delta":_int(w.get("next_cycle_amplitude_delta"))}

def _ctx(c:Mapping[str,Any],b:list[str])->dict[str,str]:
    out={k:str(c.get(k,"")) for k in REQ_CTX}
    for k,v in out.items():
        if not v: b.append(f"process_tensor_context_{k}_missing")
    return out

def _validate_weight(bridge:str,w:dict[str,Any],b:list[str])->None:
    if bridge=="integrated_candidate_to_guarded_intent_ready" and (w["path_weight_delta"]<=0 or w["probe_potential_required"] or w["barrier_potential_required"] or w["barrier_blocks_ready_weight"] or w["memory_feedback_weight"]<=0 or w["external_backaction_weight"]<=0 or w["next_cycle_amplitude_delta"]<=0): b.append("v13_7_bridge_ready_weighting_invalid")
    if bridge=="integrated_candidate_to_guarded_intent_hold" and (w["path_weight_delta"]!=0 or not w["probe_potential_required"] or w["barrier_potential_required"] or w["barrier_blocks_ready_weight"] or w["memory_feedback_weight"]!=0 or w["external_backaction_weight"]!=0 or w["next_cycle_amplitude_delta"]!=0): b.append("v13_7_bridge_hold_weighting_invalid")
    if bridge=="integrated_candidate_to_guarded_intent_block" and (w["path_weight_delta"]!=0 or w["probe_potential_required"] or not w["barrier_potential_required"] or not w["barrier_blocks_ready_weight"] or w["memory_feedback_weight"]!=0 or w["external_backaction_weight"]!=0 or w["next_cycle_amplitude_delta"]!=0): b.append("v13_7_bridge_block_weighting_invalid")

def _validate_packet(pkt:Mapping[str,Any],b:list[str],warn:list[str])->dict[str,Any]:
    if not pkt: b.append("integrated_candidate_to_guarded_intent_bridge_packet_missing_or_invalid"); return {}
    if pkt.get("integrated_candidate_to_guarded_intent_bridge_considered") is not True: b.append("integrated_candidate_to_guarded_intent_bridge_considered_not_true")
    bd=_m(pkt.get("boundary"))
    for f in REQ_BRIDGE:
        if bd.get(f) is not True: b.append(f"integrated_candidate_to_guarded_intent_bridge_boundary_{f}_missing")
    bridge=str(pkt.get("bridge_status","integrated_candidate_to_guarded_intent_block"))
    if bridge not in BRIDGE: b.append("integrated_candidate_to_guarded_intent_bridge_status_invalid"); bridge="integrated_candidate_to_guarded_intent_block"
    guarded,emit=BRIDGE[bridge]
    if str(pkt.get("guarded_execution_intent_status",""))!=guarded: b.append("guarded_execution_intent_status_mismatch")
    if str(pkt.get("guarded_intent_emit_action",""))!=emit: b.append("guarded_intent_emit_action_mismatch")
    count=_int(pkt.get("guarded_execution_intent_count")); intents=pkt.get("guarded_execution_intents",[])
    if not isinstance(intents,list): b.append("guarded_execution_intents_not_list"); intents=[]
    if count!=len(intents): b.append("guarded_execution_intent_count_mismatch")
    if bridge=="integrated_candidate_to_guarded_intent_ready" and count<=0: b.append("v13_7_bridge_ready_requires_intent")
    if bridge!="integrated_candidate_to_guarded_intent_ready" and count!=0: b.append("v13_7_bridge_hold_or_block_with_intent")
    w=_weight(_m(pkt.get("candidate_weighting"))); _validate_weight(bridge,w,b)
    if not pkt.get("integrated_candidate_to_guarded_intent_bridge_digest"): warn.append("integrated_candidate_to_guarded_intent_bridge_digest_missing")
    return {"bridge_status":bridge,"guarded_execution_intent_status":guarded,"guarded_intent_emit_action":emit,"guarded_execution_intent_count":count,"guarded_execution_intents":intents,"candidate_weighting":w,"process_tensor_context":_ctx(_m(pkt.get("process_tensor_context")),b),"source_integrated_candidate_to_guarded_intent_bridge_digest":str(pkt.get("integrated_candidate_to_guarded_intent_bridge_digest",_sha(dict(pkt)))),"source_cycle_gate_reentry_integration_receipt_digest":str(_m(pkt.get("source_digests")).get("cycle_gate_reentry_integration_receipt","")),"source_cycle_gate_reentry_integration_digest":str(_m(pkt.get("source_digests")).get("cycle_gate_reentry_integration",""))}

def _validate_intent_packet(ip:Mapping[str,Any],p:Mapping[str,Any],b:list[str])->None:
    if not ip: b.append("guarded_execution_intent_packet_missing_or_invalid"); return
    if ip.get("guarded_execution_intent_packet_ready") is not True: b.append("guarded_execution_intent_packet_not_ready")
    if str(ip.get("guarded_execution_intent_status",""))!=p.get("guarded_execution_intent_status"): b.append("guarded_execution_intent_packet_status_mismatch")
    if _int(ip.get("guarded_execution_intent_count"))!=_int(p.get("guarded_execution_intent_count")): b.append("guarded_execution_intent_packet_count_mismatch")
    if str(ip.get("source_integrated_candidate_to_guarded_intent_bridge_digest",""))!=p.get("source_integrated_candidate_to_guarded_intent_bridge_digest"): b.append("guarded_execution_intent_packet_source_digest_mismatch")
    bd=_m(ip.get("boundary"))
    for f in REQ_INTENT_PACKET:
        if bd.get(f) is not True: b.append(f"guarded_execution_intent_packet_boundary_{f}_missing")

def _validate_state(st:Mapping[str,Any],p:Mapping[str,Any],ip:Mapping[str,Any],b:list[str])->None:
    if not st: b.append("guarded_execution_intent_bridge_state_missing_or_invalid"); return
    if st.get("guarded_execution_intent_bridge_state_ready") is not True: b.append("guarded_execution_intent_bridge_state_not_ready")
    if str(st.get("bridge_status",""))!=p.get("bridge_status"): b.append("guarded_execution_intent_bridge_state_bridge_status_mismatch")
    if str(st.get("guarded_execution_intent_status",""))!=p.get("guarded_execution_intent_status"): b.append("guarded_execution_intent_bridge_state_intent_status_mismatch")
    if str(st.get("source_integrated_candidate_to_guarded_intent_bridge_digest",""))!=p.get("source_integrated_candidate_to_guarded_intent_bridge_digest"): b.append("guarded_execution_intent_bridge_state_source_digest_mismatch")
    if str(st.get("guarded_execution_intent_packet_digest",""))!=str(ip.get("guarded_execution_intent_packet_digest","")): b.append("guarded_execution_intent_bridge_state_intent_packet_digest_mismatch")
    bd=_m(st.get("boundary"))
    for f in REQ_STATE:
        if bd.get(f) is not True: b.append(f"guarded_execution_intent_bridge_state_boundary_{f}_missing")

def build_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge(*,runtime_context:Mapping[str,Any],v13_6_to_v13_7_guarded_intent_receipt_bridge_license:Mapping[str,Any])->PhysicalQuantumQiV13_6ToV13_7GuardedIntentReceiptBridgeResult:
    ctx,lic=_m(runtime_context),_m(v13_6_to_v13_7_guarded_intent_receipt_bridge_license); b:list[str]=[]; w:list[str]=[]; root=_root(ctx.get("runtime_root"),b)
    bp=root/"physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json"; ip=root/"physical_quantum_qi_guarded_execution_intent_packet.json"; sp=root/"physical_quantum_qi_guarded_execution_intent_bridge_state.json"
    ready=root/"physical_quantum_qi_v13_7_guarded_intent_bridge_receipt_ready_state.json"; blog=root/"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_ledger.jsonl"; summary=root/"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_summary.json"; receipt=root/"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_receipt.json"; audit=root/"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_audit.jsonl"
    if ctx.get("physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_enabled") is not True: b.append("physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge") is not True: b.append("apply_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_not_true")
    if lic.get("license_status")!="PHYSICAL_QUANTUM_QI_V13_6_TO_V13_7_GUARDED_INTENT_RECEIPT_BRIDGE_LICENSE_READY": b.append("physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_license_not_ready")
    for n in ["v13_6_bridge_packet_read_allowed","v13_6_guarded_execution_intent_packet_read_allowed","v13_6_bridge_state_read_allowed","v13_7_receipt_ready_state_write_allowed","bridge_ledger_append_allowed","summary_write_allowed","receipt_write_allowed","audit_append_allowed"]:
        if lic.get(n) is not True: b.append(n.replace("allowed","not_allowed"))
    pkt=_read(bp); ipkt=_read(ip); payload=_validate_packet(pkt,b,w); _validate_intent_packet(ipkt,payload,b); _validate_state(_read(sp),payload,ipkt,b)
    written=appended=False
    if not b:
        epoch=int(time.time())
        rs={"version":"physical_quantum_qi_v13_7_guarded_intent_bridge_receipt_ready_state_v13_19","guarded_intent_bridge_receipt_ready_state":True,**payload,"boundary":{"v13_7_guarded_intent_bridge_receipt_ready_state_only":True,"v13_6_bridge_packet_required":True,"v13_6_guarded_execution_intent_packet_required":True,"v13_6_bridge_state_required":True,"can_feed_v13_7_guarded_intent_bridge_receipt_ledger":True,"guarded_execution_intent_packet_traceable":True,"guarded_execution_intent_bridge_state_traceable":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"bridge_not_direct_receipt_append":True,"does_not_run_receipt_ledger":True,"fail_closed_on_boundary_loss":True},"epoch":epoch}
        rs["guarded_intent_bridge_receipt_ready_state_digest"]=_sha(rs); _write(ready,rs); written=True
        rec={"version":"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_record_v13_19","record_type":"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge","source_guarded_intent_bridge_receipt_ready_state_digest":rs["guarded_intent_bridge_receipt_ready_state_digest"],"source_integrated_candidate_to_guarded_intent_bridge_digest":payload["source_integrated_candidate_to_guarded_intent_bridge_digest"],"source_guarded_execution_intent_packet_digest":str(ipkt.get("guarded_execution_intent_packet_digest","")),"prev_record_digest":_prev(blog),"boundary":{"bridge_receipt_only":True,"v13_7_receipt_ready_state_traceable":True,"guarded_execution_intent_packet_traceable":True,"guarded_execution_intent_bridge_state_traceable":True,"same_semantic_root":True,"uses_process_tensor_feedback":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"replayable_receipt":True},"epoch":epoch,**{k:payload[k] for k in ["bridge_status","guarded_execution_intent_status","guarded_intent_emit_action","guarded_execution_intent_count"]}}
        rec["record_digest"]=_sha(rec); _append(blog,rec); appended=True
        sm={"version":"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_summary_v13_19","guarded_intent_bridge_receipt_ready_state_digest":rs["guarded_intent_bridge_receipt_ready_state_digest"],"boundary":{"summary_only":True,"can_feed_v13_7_guarded_intent_bridge_receipt_ledger":True,"candidate_weighting_not_truth":True},"epoch":epoch,**{k:payload[k] for k in ["bridge_status","guarded_execution_intent_status","guarded_intent_emit_action","guarded_execution_intent_count"]}}
        sm["summary_digest"]=_sha(sm); _write(summary,sm)
    status="PHYSICAL_QUANTUM_QI_V13_6_TO_V13_7_GUARDED_INTENT_RECEIPT_BRIDGE_READY" if not b else "PHYSICAL_QUANTUM_QI_V13_6_TO_V13_7_GUARDED_INTENT_RECEIPT_BRIDGE_BLOCKED"
    bridge=str(payload.get("bridge_status","integrated_candidate_to_guarded_intent_block")); guarded=str(payload.get("guarded_execution_intent_status","guarded_execution_intent_block")); emit=str(payload.get("guarded_intent_emit_action","emit_guarded_block_intent")); count=_int(payload.get("guarded_execution_intent_count"))
    pid="physical-quantum-qi-v13-6-to-v13-7-guarded-intent-receipt-bridge-"+_sha({"payload":payload,"blockers":b})[:16]
    rc={"version":"kuuos_runtime_daemon_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_v13_19","status":status,"packet_id":pid,"bridge_status":bridge,"guarded_execution_intent_status":guarded,"guarded_intent_emit_action":emit,"guarded_execution_intent_count":count,"receipt_ready_state_written":written,"bridge_ledger_appended":appended,"blockers":b,"warnings":w,"epoch":int(time.time())}
    if lic.get("receipt_write_allowed") is True: _write(receipt,rc)
    if lic.get("audit_append_allowed") is True: _append(audit,{**rc,"audit_record_digest":_sha(rc)})
    return PhysicalQuantumQiV13_6ToV13_7GuardedIntentReceiptBridgeResult("kuuos_runtime_daemon_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_v13_19",status,pid,str(root),bridge,guarded,emit,count,written,appended,str(ready),str(blog),str(summary),str(receipt),str(audit),b,w)
