#!/usr/bin/env python3
from __future__ import annotations

import json, pathlib, sys, tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_receipt_ledger_v12_5 import build_physical_quantum_qi_guarded_execution_intent_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_v13_21 import build_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge

PT={"process_tensor_digest":"pt-digest-v13-21","memory_kernel_digest":"memory-kernel-digest-v13-21","history_window_digest":"history-window-digest-v13-21","instrument_trace_digest":"instrument-trace-digest-v13-21","non_markov_context_digest":"non-markov-context-digest-v13-21"}
B={"guarded_execution_intent_only":True,"execution_layer_entrypoint":True,"no_dry_run_required":True,"transition_candidate_envelope_required":True,"history_bearing_process_tensor":True,"non_markov_context_required":True,"multi_time_window_required":True,"finite_horizon_only":True,"memory_kernel_visible":True,"requires_guarded_execution_license":True,"intent_not_world_mutation":True,"does_not_start_next_cycle":True,"does_not_mutate_external_state":True,"does_not_commit_plan":True,"does_not_consume_memory":True,"does_not_promote_truth":True,"candidate_weighting_not_truth":True,"fail_closed_on_boundary_loss":True}
IB={"guarded_execution_intent_only":True,"execution_layer_entrypoint":True,"no_dry_run_required":True,"requires_guarded_execution_license":True,"intent_not_world_mutation":True,"does_not_start_next_cycle":True,"does_not_mutate_external_state":True,"does_not_consume_memory":True,"does_not_promote_truth":True}

def dump(p:pathlib.Path,x:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def load(p:pathlib.Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def loadl(p:pathlib.Path)->list[dict[str,Any]]: return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.is_file() else []

def ctx(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_enabled":True,"apply_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge":True,"runtime_root":str(root)}
def lic(**o:Any)->dict[str,Any]:
    x={"license_status":"PHYSICAL_QUANTUM_QI_V13_8_TO_V12_5_GUARDED_EXECUTION_RECEIPT_BRIDGE_LICENSE_READY","v13_8_compat_guarded_execution_intent_packet_read_allowed":True,"v12_5_receipt_ready_state_write_allowed":True,"bridge_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}; x.update(o); return x

def c125(root:pathlib.Path)->dict[str,Any]: return {"physical_quantum_qi_guarded_execution_intent_receipt_ledger_enabled":True,"apply_physical_quantum_qi_guarded_execution_intent_receipt_ledger":True,"runtime_root":str(root)}
def l125()->dict[str,Any]: return {"license_status":"PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_LICENSE_READY","guarded_execution_intent_packet_read_allowed":True,"receipt_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}

def parts(k:str):
    if k=="ready": return "guarded_execution_intent_ready","transition_candidate_envelope_ready","transition_precheck_admit_candidate",1,{"path_weight_delta":2,"probe_potential_required":False,"barrier_potential_required":False,"barrier_blocks_ready_weight":False}
    if k=="hold": return "guarded_execution_intent_hold","transition_candidate_envelope_hold","transition_precheck_hold_candidate",0,{"path_weight_delta":0,"probe_potential_required":True,"barrier_potential_required":False,"barrier_blocks_ready_weight":False}
    return "guarded_execution_intent_block","transition_candidate_envelope_block","transition_precheck_block_candidate",0,{"path_weight_delta":0,"probe_potential_required":False,"barrier_potential_required":True,"barrier_blocks_ready_weight":True}

def packet(k:str,*,bad_boundary=False,bad_count=False,missing_context=False)->dict[str,Any]:
    status,env,pre,count,w=parts(k); bd=dict(B); c=dict(PT)
    if bad_boundary: bd["transition_candidate_envelope_required"]=False
    if missing_context: c["process_tensor_digest"]=""
    intents=[]
    if count:
        intents=[{"intent_type":"physical_quantum_qi_guarded_execution_intent","intent_index":0,"candidate_id":"candidate-v13-21","transition_precheck_decision":"transition_precheck_admit_candidate","corridor_stability_gate_decision":"corridor_stability_admit","candidate_weighting":w,"process_tensor_context":c,"source_transition_candidate_envelope_digest":"env-digest-v13-21","guarded_execution_intent_digest":"intent-digest-v13-21","boundary":dict(IB)}]
    if bad_count: intents=[] if count else [{"intent_type":"physical_quantum_qi_guarded_execution_intent","intent_index":0,"boundary":dict(IB)}]
    return {"physical_quantum_qi_guarded_execution_intent_considered":True,"execution_intent_status":status,"envelope_status":env,"transition_precheck_decision":pre,"intent_count":len(intents) if bad_count else count,"envelope_count":count,"guarded_execution_intents":intents,"process_tensor_context":c,"source_digests":{},"boundary":bd,"guarded_execution_intent_packet_digest":f"v12-5-compatible-packet-{k}","epoch":1}

def run(root:pathlib.Path,name:str,pkt:dict[str,Any]|None,license_packet:dict[str,Any]):
    rt=root/name
    if pkt is not None: dump(rt/"physical_quantum_qi_guarded_execution_intent_packet.json",pkt)
    out=build_physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge(runtime_context=ctx(rt),v13_8_to_v12_5_guarded_execution_receipt_bridge_license=license_packet).to_dict()
    return out,load(rt/"physical_quantum_qi_v12_5_guarded_execution_intent_receipt_ready_state.json"),loadl(rt/"physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_ledger.jsonl")

def ok(label,out,ready,ledger):
    assert out["status"]=="PHYSICAL_QUANTUM_QI_V13_8_TO_V12_5_GUARDED_EXECUTION_RECEIPT_BRIDGE_READY",(label,out)
    assert out["receipt_ready_state_written"] and out["bridge_ledger_appended"] and not out["blockers"]
    assert ready["boundary"]["can_feed_v12_5_guarded_execution_intent_receipt_ledger"] is True
    assert ready["boundary"]["does_not_run_v12_5_receipt_ledger"] is True
    assert ledger[-1]["boundary"]["v12_5_receipt_ready_state_traceable"] is True

def accept125(rt:pathlib.Path,label:str,status:str,count:int):
    out=build_physical_quantum_qi_guarded_execution_intent_receipt_ledger(runtime_context=c125(rt),guarded_execution_intent_receipt_ledger_license=l125()).to_dict()
    assert out["status"]=="PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_READY",(label,out)
    assert out["execution_intent_status"]==status and out["intent_count"]==count and out["ledger_appended"] is True

def main()->int:
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td)
        for k in ["ready","hold","block"]:
            pkt=packet(k); out,ready,ledger=run(root,k,pkt,lic()); ok(k,out,ready,ledger); status,_,_,count,_=parts(k); accept125(root/k,k,status,count)
        out,ready,ledger=run(root,"chain",packet("ready"),lic()); ok("chain1",out,ready,ledger)
        out,ready,ledger=run(root,"chain",packet("hold"),lic()); ok("chain2",out,ready,ledger); assert len(ledger)==2 and ledger[1]["prev_record_digest"]==ledger[0]["record_digest"]
        out,ready,ledger=run(root,"bad_boundary",packet("ready",bad_boundary=True),lic()); assert out["status"].endswith("BLOCKED") and "guarded_execution_intent_boundary_transition_candidate_envelope_required_missing" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"bad_count",packet("ready",bad_count=True),lic()); assert out["status"].endswith("BLOCKED") and "guarded_execution_intent_ready_without_intents" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"missing_context",packet("ready",missing_context=True),lic()); assert out["status"].endswith("BLOCKED") and "process_tensor_context_process_tensor_digest_missing" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"missing",None,lic()); assert out["status"].endswith("BLOCKED") and "guarded_execution_intent_packet_missing_or_invalid" in out["blockers"] and ready=={}
        out,ready,ledger=run(root,"license",packet("ready"),lic(v12_5_receipt_ready_state_write_allowed=False)); assert out["status"].endswith("BLOCKED") and "v12_5_receipt_ready_state_write_not_allowed" in out["blockers"] and ready=={}
    print("physical_quantum_qi_v13_8_to_v12_5_guarded_execution_receipt_bridge_v13_21 checks passed")
    return 0

if __name__=="__main__": raise SystemExit(main())
