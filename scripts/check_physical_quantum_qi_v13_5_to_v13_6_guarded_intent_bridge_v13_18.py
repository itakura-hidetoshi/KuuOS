#!/usr/bin/env python3
from __future__ import annotations

import json, pathlib, sys, tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6 import build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5 import build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_v13_18 import build_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge

PT={"process_tensor_digest":"pt-digest-v13-18","memory_kernel_digest":"memory-kernel-digest-v13-18","history_window_digest":"history-window-digest-v13-18","instrument_trace_digest":"instrument-trace-digest-v13-18","non_markov_context_digest":"non-markov-context-digest-v13-18"}
B={"receipt_ledger_only":True,"cycle_gate_reentry_integration_receipt_only":True,"integrated_cycle_gate_state_traceable":True,"integrated_admissible_candidate_set_traceable":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"integration_not_direct_execution":True,"replayable_receipt":True,"fail_closed_on_boundary_loss":True}
PB={"cycle_gate_reentry_integration_only":True,"candidate_weighting_cycle_handoff_receipt_required":True,"integrates_cycle_gate":True,"integrates_admissible_candidate_set":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"integration_not_direct_execution":True,"license_gated_integration":True,"fail_closed_on_boundary_loss":True}
GB={"integrated_cycle_gate_state_only":True,"from_candidate_weighting_cycle_handoff_receipt":True,"uses_process_tensor_feedback":True,"candidate_weighting_not_truth":True,"not_direct_execution_authority":True}
SB={"integrated_admissible_candidate_set_only":True,"from_candidate_weighting_cycle_handoff_receipt":True,"uses_process_tensor_feedback":True,"candidate_weighting_not_truth":True,"not_direct_execution_authority":True}


def dump(p:pathlib.Path,x:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def append(p:pathlib.Path,x:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as h: h.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n")

def load(p:pathlib.Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def loadl(p:pathlib.Path)->list[dict[str,Any]]: return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.is_file() else []

def ctx(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_enabled":True,"apply_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge":True,"runtime_root":str(root)}
def lic(**o:Any)->dict[str,Any]:
    x={"license_status":"PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_LICENSE_READY","v13_5_integration_receipt_ledger_read_allowed":True,"v13_6_guarded_intent_ready_state_write_allowed":True,"bridge_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}; x.update(o); return x

def c5(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled":True,"apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger":True,"runtime_root":str(root)}
def l5()->dict[str,Any]: return {"license_status":"PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_LICENSE_READY","integration_packet_read_allowed":True,"integrated_cycle_gate_state_read_allowed":True,"integrated_admissible_candidate_set_read_allowed":True,"receipt_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}
def c6(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_enabled":True,"apply_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge":True,"runtime_root":str(root)}
def l6()->dict[str,Any]: return {"license_status":"PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_LICENSE_READY","cycle_gate_reentry_integration_receipt_ledger_read_allowed":True,"bridge_packet_write_allowed":True,"guarded_execution_intent_packet_write_allowed":True,"bridge_state_write_allowed":True,"bridge_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}

def parts(k:str):
    if k=="admit": return "cycle_gate_reentry_integration_admit","integrated_cycle_gate_admit","integrated_admissible_candidate_set_admit",1,"guarded_execution_intent_ready",{"path_weight_delta":2,"probe_potential_required":False,"barrier_potential_required":False,"barrier_blocks_ready_weight":False,"memory_feedback_weight":1,"external_backaction_weight":1,"next_cycle_amplitude_delta":1}
    if k=="hold": return "cycle_gate_reentry_integration_hold","integrated_cycle_gate_hold","integrated_admissible_candidate_set_probe",1,"guarded_execution_intent_hold",{"path_weight_delta":0,"probe_potential_required":True,"barrier_potential_required":False,"barrier_blocks_ready_weight":False,"memory_feedback_weight":0,"external_backaction_weight":0,"next_cycle_amplitude_delta":0}
    return "cycle_gate_reentry_integration_block","integrated_cycle_gate_block","integrated_admissible_candidate_set_block",0,"guarded_execution_intent_block",{"path_weight_delta":0,"probe_potential_required":False,"barrier_potential_required":True,"barrier_blocks_ready_weight":True,"memory_feedback_weight":0,"external_backaction_weight":0,"next_cycle_amplitude_delta":0}

def receipt(k:str, *, bad_boundary=False,bad_gate=False,bad_set=False,bad_count=False,bad_weight=False,missing_context=False)->dict[str,Any]:
    integ,gate,setv,count,_,w=parts(k); w=dict(w)
    if bad_weight: w["path_weight_delta"]=0 if k=="admit" else w["path_weight_delta"]; w["barrier_blocks_ready_weight"]=False if k=="block" else w["barrier_blocks_ready_weight"]
    candidates=[{"candidate_id":"candidate-v13-18","candidate_digest":"candidate-digest-v13-18"}] if count else []
    if bad_count: candidates=[] if count else [{"candidate_id":"unexpected"}]
    boundary=dict(B); context=dict(PT)
    if bad_boundary: boundary["integrated_cycle_gate_state_traceable"]=False
    if missing_context: context["memory_kernel_digest"]=""
    return {"version":"physical_quantum_qi_cycle_gate_reentry_integration_receipt_record_v13_5","record_type":"physical_quantum_qi_cycle_gate_reentry_integration_receipt","integration_status":integ,"integrated_cycle_gate_status":"wrong_gate" if bad_gate else gate,"integrated_admissible_candidate_set_status":"wrong_set" if bad_set else setv,"admissible_candidate_count":len(candidates) if not bad_count else (0 if count else 1),"integrated_candidates":candidates,"candidate_weighting":w,"process_tensor_context":context,"source_cycle_gate_reentry_integration_digest":"integration-digest-v13-18","prev_record_digest":"GENESIS","record_digest":f"integration-receipt-digest-{k}","boundary":boundary,"epoch":1}

def write_v13_4_outputs(rt:pathlib.Path,k:str)->None:
    integ,gate,setv,count,_,w=parts(k); c=[{"candidate_id":"candidate-v13-18","candidate_digest":"candidate-digest-v13-18"}] if count else []
    dump(rt/"physical_quantum_qi_cycle_gate_reentry_integration_packet.json", {"cycle_gate_reentry_integration_considered":True,"integration_status":integ,"integrated_cycle_gate_status":gate,"integrated_admissible_candidate_set_status":setv,"admissible_candidate_count":count,"integrated_candidates":c,"candidate_weighting":w,"process_tensor_context":PT,"source_digests":{},"boundary":PB,"cycle_gate_reentry_integration_digest":"integration-digest-v13-18","epoch":1})
    dump(rt/"physical_quantum_qi_integrated_cycle_gate_state.json", {"integrated_cycle_gate_ready":True,"integrated_cycle_gate_status":gate,"candidate_weighting":w,"source_cycle_gate_reentry_integration_digest":"integration-digest-v13-18","process_tensor_context":PT,"boundary":GB,"epoch":1})
    dump(rt/"physical_quantum_qi_integrated_admissible_candidate_set.json", {"integrated_admissible_candidate_set_ready":True,"integrated_admissible_candidate_set_status":setv,"admissible_candidate_count":count,"integrated_candidates":c,"candidate_weighting":w,"source_cycle_gate_reentry_integration_digest":"integration-digest-v13-18","process_tensor_context":PT,"boundary":SB,"epoch":1})

def run(root:pathlib.Path,name:str,rec:dict[str,Any]|None,license_packet:dict[str,Any]):
    rt=root/name
    if rec is not None: append(rt/"physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl", rec)
    out=build_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge(runtime_context=ctx(rt),v13_5_to_v13_6_guarded_intent_bridge_license=license_packet).to_dict()
    return out,load(rt/"physical_quantum_qi_v13_6_integrated_candidate_to_guarded_intent_ready_state.json"),loadl(rt/"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_ledger.jsonl")

def ok(label,out,ready,ledger):
    assert out["status"]=="PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_READY",(label,out)
    assert out["guarded_intent_ready_state_written"] and out["bridge_ledger_appended"] and not out["blockers"]
    assert ready["boundary"]["can_feed_v13_6_integrated_candidate_to_guarded_intent_bridge"] is True
    assert ready["boundary"]["does_not_run_guarded_intent_bridge"] is True
    assert ledger[-1]["boundary"]["v13_6_guarded_intent_bridge_ready_state_traceable"] is True

def accept6(rt:pathlib.Path,label:str,guarded:str,count:int):
    out=build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge(runtime_context=c6(rt),integrated_candidate_to_guarded_intent_bridge_license=l6()).to_dict()
    assert out["status"]=="PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_READY",(label,out)
    assert out["guarded_execution_intent_status"]==guarded
    assert out["guarded_execution_intent_count"]==count
    assert out["guarded_execution_intent_packet_written"] is True

def full(root:pathlib.Path,k:str):
    rt=root/f"full_{k}"; write_v13_4_outputs(rt,k)
    out5=build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger(runtime_context=c5(rt),cycle_gate_reentry_integration_receipt_ledger_license=l5()).to_dict()
    assert out5["status"]=="PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_READY",out5
    out,ready,ledger=run(root,f"full_{k}",None,lic()); ok(f"full_{k}",out,ready,ledger)
    _,_,_,count,guarded,_=parts(k); accept6(rt,f"full_{k}",guarded,count if guarded=="guarded_execution_intent_ready" else 0)

def main()->int:
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td)
        for k in ["admit","hold","block"]:
            out,ready,ledger=run(root,k,receipt(k),lic()); ok(k,out,ready,ledger)
            _,_,_,count,guarded,_=parts(k); assert out["guarded_execution_intent_status"]==guarded; accept6(root/k,k,guarded,count if guarded=="guarded_execution_intent_ready" else 0)
        for k in ["admit","hold","block"]: full(root,k)
        out,ready,ledger=run(root,"chain",receipt("admit"),lic()); ok("chain1",out,ready,ledger)
        out,ready,ledger=run(root,"chain",receipt("hold"),lic()); ok("chain2",out,ready,ledger); assert len(ledger)==2 and ledger[1]["prev_record_digest"]==ledger[0]["record_digest"]
        cases=[("bad_boundary",receipt("admit",bad_boundary=True),"cycle_gate_reentry_integration_receipt_boundary_integrated_cycle_gate_state_traceable_missing"),("bad_gate",receipt("hold",bad_gate=True),"cycle_gate_reentry_integration_receipt_gate_status_mismatch"),("bad_set",receipt("block",bad_set=True),"cycle_gate_reentry_integration_receipt_candidate_set_status_mismatch"),("bad_count",receipt("admit",bad_count=True),"v13_6_bridge_requires_integrated_candidate_for_admit_or_hold"),("bad_weight",receipt("block",bad_weight=True),"v13_6_bridge_block_weighting_invalid"),("missing_context",receipt("admit",missing_context=True),"process_tensor_context_memory_kernel_digest_missing")]
        for name,rec,err in cases:
            out,ready,ledger=run(root,name,rec,lic()); assert out["status"].endswith("BLOCKED") and err in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"missing",None,lic()); assert "cycle_gate_reentry_integration_receipt_ledger_missing" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"license",receipt("admit"),lic(v13_6_guarded_intent_ready_state_write_allowed=False)); assert "v13_6_guarded_intent_ready_state_write_not_allowed" in out["blockers"] and ready=={}
    print("physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_v13_18 checks passed")
    return 0

if __name__=="__main__": raise SystemExit(main())
