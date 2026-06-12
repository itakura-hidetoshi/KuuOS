#!/usr/bin/env python3
from __future__ import annotations

import json, pathlib, sys, tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_v13_20 import build_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge

PT={"process_tensor_digest":"pt-digest-v13-20","memory_kernel_digest":"memory-kernel-digest-v13-20","history_window_digest":"history-window-digest-v13-20","instrument_trace_digest":"instrument-trace-digest-v13-20","non_markov_context_digest":"non-markov-context-digest-v13-20"}
B={"receipt_ledger_only":True,"guarded_intent_bridge_receipt_only":True,"guarded_execution_intent_packet_traceable":True,"guarded_execution_intent_bridge_state_traceable":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"replayable_receipt":True,"fail_closed_on_boundary_loss":True}

def append(p:pathlib.Path,x:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as h: h.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n")

def load(p:pathlib.Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def loadl(p:pathlib.Path)->list[dict[str,Any]]: return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.is_file() else []

def ctx(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_enabled":True,"apply_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge":True,"runtime_root":str(root)}
def lic(**o:Any)->dict[str,Any]:
    x={"license_status":"PHYSICAL_QUANTUM_QI_V13_7_TO_V13_8_COMPATIBILITY_BRIDGE_LICENSE_READY","v13_7_guarded_intent_bridge_receipt_ledger_read_allowed":True,"v13_8_compatibility_bridge_ready_state_write_allowed":True,"bridge_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}; x.update(o); return x

def parts(k:str):
    if k=="ready": return "guarded_execution_intent_ready","integrated_candidate_to_guarded_intent_ready","transition_candidate_envelope_ready","transition_precheck_admit_candidate",1,{"path_weight_delta":2,"probe_potential_required":False,"barrier_potential_required":False,"barrier_blocks_ready_weight":False,"memory_feedback_weight":1,"external_backaction_weight":1,"next_cycle_amplitude_delta":1}
    if k=="hold": return "guarded_execution_intent_hold","integrated_candidate_to_guarded_intent_hold","transition_candidate_envelope_hold","transition_precheck_hold_candidate",0,{"path_weight_delta":0,"probe_potential_required":True,"barrier_potential_required":False,"barrier_blocks_ready_weight":False,"memory_feedback_weight":0,"external_backaction_weight":0,"next_cycle_amplitude_delta":0}
    return "guarded_execution_intent_block","integrated_candidate_to_guarded_intent_block","transition_candidate_envelope_block","transition_precheck_block_candidate",0,{"path_weight_delta":0,"probe_potential_required":False,"barrier_potential_required":True,"barrier_blocks_ready_weight":True,"memory_feedback_weight":0,"external_backaction_weight":0,"next_cycle_amplitude_delta":0}

def receipt(k:str,*,bad_boundary=False,bad_count=False,missing_context=False)->dict[str,Any]:
    status,bridge,_,_,count,w=parts(k); bd=dict(B); c=dict(PT)
    if bad_boundary: bd["guarded_execution_intent_packet_traceable"]=False
    if missing_context: c["instrument_trace_digest"]=""
    intents=[{"candidate_id":"candidate-v13-20","candidate_weighting":w,"process_tensor_context":c,"guarded_execution_intent_digest":"intent-digest-v13-20"}] if count else []
    if bad_count: intents=[] if count else [{"candidate_id":"unexpected"}]
    return {"record_type":"physical_quantum_qi_guarded_intent_bridge_receipt","bridge_status":bridge,"guarded_execution_intent_status":status,"guarded_execution_intent_count":len(intents) if bad_count else count,"guarded_execution_intents":intents,"candidate_weighting":w,"process_tensor_context":c,"source_guarded_execution_intent_packet_digest":"intent-packet-digest-v13-20","source_integrated_candidate_to_guarded_intent_bridge_digest":"guarded-intent-bridge-digest-v13-20","prev_record_digest":"GENESIS","record_digest":f"guarded-intent-receipt-digest-{k}","boundary":bd,"epoch":1}

def run(root:pathlib.Path,name:str,rec:dict[str,Any]|None,license_packet:dict[str,Any]):
    rt=root/name
    if rec is not None: append(rt/"physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl",rec)
    out=build_physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge(runtime_context=ctx(rt),v13_7_to_v13_8_compatibility_bridge_license=license_packet).to_dict()
    return out,load(rt/"physical_quantum_qi_v13_8_guarded_intent_receipt_ledger_compatibility_bridge_ready_state.json"),loadl(rt/"physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_ledger.jsonl")

def ok(label,out,ready,ledger):
    assert out["status"]=="PHYSICAL_QUANTUM_QI_V13_7_TO_V13_8_COMPATIBILITY_BRIDGE_READY",(label,out)
    assert out["compatibility_ready_state_written"] and out["bridge_ledger_appended"] and not out["blockers"]
    assert ready["boundary"]["can_feed_v13_8_guarded_intent_receipt_ledger_compatibility_bridge"] is True
    assert ready["boundary"]["does_not_write_v12_5_packet"] is True
    assert ledger[-1]["boundary"]["v13_8_compatibility_bridge_ready_state_traceable"] is True

def main()->int:
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td)
        for k in ["ready","hold","block"]:
            out,ready,ledger=run(root,k,receipt(k),lic()); ok(k,out,ready,ledger)
            _,_,env,pre,count,_=parts(k); assert out["v12_5_envelope_status"]==env and out["v12_5_precheck_decision"]==pre and out["intent_count"]==count
        out,ready,ledger=run(root,"chain",receipt("ready"),lic()); ok("chain1",out,ready,ledger)
        out,ready,ledger=run(root,"chain",receipt("hold"),lic()); ok("chain2",out,ready,ledger); assert len(ledger)==2 and ledger[1]["prev_record_digest"]==ledger[0]["record_digest"]
        out,ready,ledger=run(root,"bad_boundary",receipt("ready",bad_boundary=True),lic()); assert out["status"].endswith("BLOCKED") and "guarded_intent_bridge_receipt_boundary_guarded_execution_intent_packet_traceable_missing" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"bad_count",receipt("ready",bad_count=True),lic()); assert out["status"].endswith("BLOCKED") and "v13_8_compat_ready_requires_intent" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"missing_context",receipt("ready",missing_context=True),lic()); assert out["status"].endswith("BLOCKED") and "process_tensor_context_instrument_trace_digest_missing" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"missing",None,lic()); assert out["status"].endswith("BLOCKED") and "guarded_intent_bridge_receipt_ledger_missing" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"license",receipt("ready"),lic(v13_8_compatibility_bridge_ready_state_write_allowed=False)); assert out["status"].endswith("BLOCKED") and "v13_8_compatibility_bridge_ready_state_write_not_allowed" in out["blockers"] and ready=={}
    print("physical_quantum_qi_v13_7_to_v13_8_compatibility_bridge_v13_20 checks passed")
    return 0

if __name__=="__main__": raise SystemExit(main())
