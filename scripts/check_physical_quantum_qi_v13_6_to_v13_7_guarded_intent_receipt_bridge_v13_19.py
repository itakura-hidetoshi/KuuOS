#!/usr/bin/env python3
from __future__ import annotations

import json, pathlib, sys, tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_bridge_receipt_ledger_v13_7 import build_physical_quantum_qi_guarded_intent_bridge_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6 import build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_v13_19 import build_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge

PT={"process_tensor_digest":"pt-digest-v13-19","memory_kernel_digest":"memory-kernel-digest-v13-19","history_window_digest":"history-window-digest-v13-19","instrument_trace_digest":"instrument-trace-digest-v13-19","non_markov_context_digest":"non-markov-context-digest-v13-19"}
BB={"integrated_candidate_to_guarded_intent_bridge_only":True,"cycle_gate_reentry_integration_receipt_required":True,"emits_guarded_execution_intent_packet":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"does_not_run_runner":True,"does_not_mutate_external_state":True,"does_not_start_next_cycle":True,"license_gated_bridge":True,"fail_closed_on_boundary_loss":True}
IPB={"guarded_execution_intent_packet_only":True,"from_integrated_candidate_bridge":True,"requires_guarded_execution_license":True,"candidate_weighting_not_truth":True,"not_direct_execution_authority":True,"does_not_run_runner":True,"does_not_mutate_external_state":True}
IB={"guarded_execution_intent_only":True,"execution_layer_entrypoint":True,"no_dry_run_required":True,"requires_guarded_execution_license":True,"intent_not_world_mutation":True,"does_not_start_next_cycle":True,"does_not_mutate_external_state":True,"does_not_consume_memory":True,"does_not_promote_truth":True}
SB={"guarded_execution_intent_bridge_state_only":True,"from_integrated_candidate_bridge":True,"can_feed_guarded_execution_intent_receipt_layer":True,"candidate_weighting_not_truth":True,"not_direct_execution_authority":True}
RB={"receipt_ledger_only":True,"cycle_gate_reentry_integration_receipt_only":True,"integrated_cycle_gate_state_traceable":True,"integrated_admissible_candidate_set_traceable":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"integration_not_direct_execution":True,"replayable_receipt":True,"fail_closed_on_boundary_loss":True}

def dump(p:pathlib.Path,x:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def append(p:pathlib.Path,x:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as h: h.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n")

def load(p:pathlib.Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def loadl(p:pathlib.Path)->list[dict[str,Any]]: return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.is_file() else []

def ctx(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_enabled":True,"apply_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge":True,"runtime_root":str(root)}
def lic(**o:Any)->dict[str,Any]:
    x={"license_status":"PHYSICAL_QUANTUM_QI_V13_6_TO_V13_7_GUARDED_INTENT_RECEIPT_BRIDGE_LICENSE_READY","v13_6_bridge_packet_read_allowed":True,"v13_6_guarded_execution_intent_packet_read_allowed":True,"v13_6_bridge_state_read_allowed":True,"v13_7_receipt_ready_state_write_allowed":True,"bridge_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}; x.update(o); return x

def c6(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_enabled":True,"apply_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge":True,"runtime_root":str(root)}
def l6()->dict[str,Any]: return {"license_status":"PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_LICENSE_READY","cycle_gate_reentry_integration_receipt_ledger_read_allowed":True,"bridge_packet_write_allowed":True,"guarded_execution_intent_packet_write_allowed":True,"bridge_state_write_allowed":True,"bridge_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}
def c7(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_guarded_intent_bridge_receipt_ledger_enabled":True,"apply_physical_quantum_qi_guarded_intent_bridge_receipt_ledger":True,"runtime_root":str(root)}
def l7()->dict[str,Any]: return {"license_status":"PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_LICENSE_READY","bridge_packet_read_allowed":True,"guarded_execution_intent_packet_read_allowed":True,"bridge_state_read_allowed":True,"receipt_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}

def parts(k:str):
    if k=="ready": return "integrated_candidate_to_guarded_intent_ready","guarded_execution_intent_ready","emit_guarded_ready_intent",1,{"path_weight_delta":2,"probe_potential_required":False,"barrier_potential_required":False,"barrier_blocks_ready_weight":False,"memory_feedback_weight":1,"external_backaction_weight":1,"next_cycle_amplitude_delta":1}
    if k=="hold": return "integrated_candidate_to_guarded_intent_hold","guarded_execution_intent_hold","emit_guarded_hold_intent",0,{"path_weight_delta":0,"probe_potential_required":True,"barrier_potential_required":False,"barrier_blocks_ready_weight":False,"memory_feedback_weight":0,"external_backaction_weight":0,"next_cycle_amplitude_delta":0}
    return "integrated_candidate_to_guarded_intent_block","guarded_execution_intent_block","emit_guarded_block_intent",0,{"path_weight_delta":0,"probe_potential_required":False,"barrier_potential_required":True,"barrier_blocks_ready_weight":True,"memory_feedback_weight":0,"external_backaction_weight":0,"next_cycle_amplitude_delta":0}

def write_v13_6_outputs(rt:pathlib.Path,k:str,*,bad_boundary=False,bad_intent_packet=False,bad_state=False,bad_count=False,bad_weight=False,missing_context=False)->None:
    bridge,guarded,emit,count,w=parts(k); w=dict(w)
    if bad_weight: w["path_weight_delta"]=0 if k=="ready" else w["path_weight_delta"]; w["barrier_blocks_ready_weight"]=False if k=="block" else w["barrier_blocks_ready_weight"]
    context=dict(PT); bd=dict(BB)
    if missing_context: context["history_window_digest"]=""
    if bad_boundary: bd["emits_guarded_execution_intent_packet"]=False
    intent=[{"intent_id":"intent-v13-19","transition_precheck_decision":"transition_precheck_admit_candidate","corridor_stability_gate_decision":"corridor_stability_admit","candidate_weighting":w,"boundary":IB}] if count else []
    if bad_count: intent=[] if count else [{"intent_id":"unexpected","boundary":IB}]
    digest=f"guarded-intent-bridge-digest-{k}"; ip_digest=f"guarded-intent-packet-digest-{k}"
    dump(rt/"physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json",{"integrated_candidate_to_guarded_intent_bridge_considered":True,"bridge_status":bridge,"guarded_execution_intent_status":guarded,"guarded_intent_emit_action":emit,"guarded_execution_intent_count":len(intent) if bad_count else count,"guarded_execution_intents":intent,"candidate_weighting":w,"process_tensor_context":context,"source_digests":{"cycle_gate_reentry_integration_receipt":"integration-receipt-digest-v13-19","cycle_gate_reentry_integration":"integration-digest-v13-19"},"boundary":bd,"integrated_candidate_to_guarded_intent_bridge_digest":digest,"epoch":1})
    ipb=dict(IPB)
    if bad_intent_packet: ipb["from_integrated_candidate_bridge"]=False
    dump(rt/"physical_quantum_qi_guarded_execution_intent_packet.json",{"guarded_execution_intent_packet_ready":True,"guarded_execution_intent_status":guarded,"guarded_execution_intent_count":len(intent) if bad_count else count,"guarded_execution_intents":intent,"candidate_weighting":w,"source_integrated_candidate_to_guarded_intent_bridge_digest":digest,"boundary":ipb,"guarded_execution_intent_packet_digest":ip_digest,"epoch":1})
    state={"guarded_execution_intent_bridge_state_ready":True,"bridge_status":bridge,"guarded_execution_intent_status":guarded,"source_integrated_candidate_to_guarded_intent_bridge_digest":digest,"guarded_execution_intent_packet_digest":ip_digest,"candidate_weighting":w,"process_tensor_context":context,"boundary":dict(SB),"epoch":1}
    if bad_state: state["bridge_status"]="wrong_bridge"
    dump(rt/"physical_quantum_qi_guarded_execution_intent_bridge_state.json",state)

def integration_receipt(k:str)->dict[str,Any]:
    bridge,guarded,emit,count,w=parts(k)
    integ={"ready":"cycle_gate_reentry_integration_admit","hold":"cycle_gate_reentry_integration_hold","block":"cycle_gate_reentry_integration_block"}[k]
    gate={"ready":"integrated_cycle_gate_admit","hold":"integrated_cycle_gate_hold","block":"integrated_cycle_gate_block"}[k]
    aset={"ready":"integrated_admissible_candidate_set_admit","hold":"integrated_admissible_candidate_set_probe","block":"integrated_admissible_candidate_set_block"}[k]
    c=[{"candidate_id":"candidate-v13-19","candidate_digest":"candidate-digest-v13-19"}] if count else []
    return {"record_type":"physical_quantum_qi_cycle_gate_reentry_integration_receipt","integration_status":integ,"integrated_cycle_gate_status":gate,"integrated_admissible_candidate_set_status":aset,"admissible_candidate_count":count,"integrated_candidates":c,"candidate_weighting":w,"process_tensor_context":PT,"source_cycle_gate_reentry_integration_digest":"integration-digest-v13-19","prev_record_digest":"GENESIS","record_digest":"integration-receipt-digest-v13-19","boundary":RB,"epoch":1}

def run(root:pathlib.Path,name:str,kind:str|None,license_packet:dict[str,Any],**kw:Any):
    rt=root/name
    if kind is not None: write_v13_6_outputs(rt,kind,**kw)
    out=build_physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge(runtime_context=ctx(rt),v13_6_to_v13_7_guarded_intent_receipt_bridge_license=license_packet).to_dict()
    return out,load(rt/"physical_quantum_qi_v13_7_guarded_intent_bridge_receipt_ready_state.json"),loadl(rt/"physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_ledger.jsonl")

def ok(label,out,ready,ledger):
    assert out["status"]=="PHYSICAL_QUANTUM_QI_V13_6_TO_V13_7_GUARDED_INTENT_RECEIPT_BRIDGE_READY",(label,out)
    assert out["receipt_ready_state_written"] and out["bridge_ledger_appended"] and not out["blockers"]
    assert ready["boundary"]["can_feed_v13_7_guarded_intent_bridge_receipt_ledger"] is True
    assert ready["boundary"]["does_not_run_receipt_ledger"] is True
    assert ledger[-1]["boundary"]["v13_7_receipt_ready_state_traceable"] is True

def accept7(rt:pathlib.Path,label:str,guarded:str,count:int):
    out=build_physical_quantum_qi_guarded_intent_bridge_receipt_ledger(runtime_context=c7(rt),guarded_intent_bridge_receipt_ledger_license=l7()).to_dict()
    assert out["status"]=="PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_READY",(label,out)
    assert out["guarded_execution_intent_status"]==guarded and out["guarded_execution_intent_count"]==count and out["ledger_appended"] is True

def full(root:pathlib.Path,k:str):
    rt=root/f"full_{k}"; append(rt/"physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl",integration_receipt(k))
    out6=build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge(runtime_context=c6(rt),integrated_candidate_to_guarded_intent_bridge_license=l6()).to_dict()
    assert out6["status"]=="PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_READY",out6
    out,ready,ledger=run(root,f"full_{k}",None,lic()); ok(f"full_{k}",out,ready,ledger)
    _,guarded,_,count,_=parts(k); accept7(rt,f"full_{k}",guarded,count)

def main()->int:
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td)
        for k in ["ready","hold","block"]:
            out,ready,ledger=run(root,k,k,lic()); ok(k,out,ready,ledger); _,guarded,_,count,_=parts(k); accept7(root/k,k,guarded,count)
        for k in ["ready","hold","block"]: full(root,k)
        out,ready,ledger=run(root,"chain","ready",lic()); ok("chain1",out,ready,ledger)
        out,ready,ledger=run(root,"chain","hold",lic()); ok("chain2",out,ready,ledger); assert len(ledger)==2 and ledger[1]["prev_record_digest"]==ledger[0]["record_digest"]
        cases=[("bad_boundary",{"bad_boundary":True},"integrated_candidate_to_guarded_intent_bridge_boundary_emits_guarded_execution_intent_packet_missing"),("bad_intent_packet",{"bad_intent_packet":True},"guarded_execution_intent_packet_boundary_from_integrated_candidate_bridge_missing"),("bad_state",{"bad_state":True},"guarded_execution_intent_bridge_state_bridge_status_mismatch"),("bad_count",{"bad_count":True},"guarded_execution_intent_count_mismatch"),("bad_weight",{"bad_weight":True},"v13_7_bridge_block_weighting_invalid"),("missing_context",{"missing_context":True},"process_tensor_context_history_window_digest_missing")]
        for name,kw,err in cases:
            kind="block" if name=="bad_weight" else "ready"
            out,ready,ledger=run(root,name,kind,lic(),**kw); assert out["status"].endswith("BLOCKED") and err in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"missing",None,lic()); assert "integrated_candidate_to_guarded_intent_bridge_packet_missing_or_invalid" in out["blockers"] and "guarded_execution_intent_packet_missing_or_invalid" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"license","ready",lic(v13_7_receipt_ready_state_write_allowed=False)); assert "v13_7_receipt_ready_state_write_not_allowed" in out["blockers"] and ready=={}
    print("physical_quantum_qi_v13_6_to_v13_7_guarded_intent_receipt_bridge_v13_19 checks passed")
    return 0

if __name__=="__main__": raise SystemExit(main())
