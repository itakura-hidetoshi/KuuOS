#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys, tempfile
from typing import Any
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_26_reentry_weighting_activation import build_physical_quantum_qi_v13_26_reentry_weighting_activation

PT={"process_tensor_digest":"pt-v13-26","memory_kernel_digest":"memory-v13-26","history_window_digest":"history-v13-26","instrument_trace_digest":"instrument-v13-26","non_markov_context_digest":"non-markov-v13-26"}
PACKET_BOUNDARY={"process_tensor_execution_feedback_only":True,"uses_execution_effects_as_non_markov_feedback":True,"feeds_path_integral_weighting":True,"history_window_feedback_required":True,"memory_kernel_feedback_required":True,"external_backaction_visible":True,"feedback_not_direct_truth":True,"feedback_not_unbounded_execution":True,"runtime_local_feedback_only":True,"fail_closed_on_boundary_loss":True}
STATE_BOUNDARY={"path_integral_feedback_state_only":True,"non_markov_feedback_preserved":True,"feedback_not_direct_authority":True}
KERNEL_FLAGS={"non_markov_feedback_required":True,"history_window_feedback_required":True,"instrument_trace_feedback_required":True,"process_tensor_feedback_not_truth":True}

def write(path:pathlib.Path,payload:dict[str,Any]):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def parts(kind:str):
    if kind=="reinforce":
        return "process_tensor_feedback_reinforce_next_cycle","guarded_transition_executed","reentry_weighting_reinforce","reinforce_path_weight",2,1,1,1
    if kind=="hold":
        return "process_tensor_feedback_hold_context","guarded_transition_hold","reentry_weighting_hold","open_probe_potential",0,0,0,0
    return "process_tensor_feedback_block_context","guarded_transition_block","reentry_weighting_block","add_barrier_potential",-1,0,0,0

def prepare(root:pathlib.Path,kind:str,*,bad_ready_digest=False,bad_packet=False):
    feedback,execution,reentry,action,path_delta,memory,external,amp=parts(kind)
    packet_digest=f"feedback-packet-{kind}"
    packet={"version":"physical_quantum_qi_process_tensor_execution_feedback_packet_v12_7","feedback_status":feedback,"execution_status":execution,"process_tensor_feedback_kernel":{**KERNEL_FLAGS,"feedback_status":feedback,"path_weight_delta":0 if bad_packet and kind=="reinforce" else path_delta,"memory_feedback_weight":memory,"external_backaction_weight":external,"next_cycle_amplitude_delta":amp},"observed_effects":{"next_cycle_observed":kind=="reinforce","memory_feedback_observed":kind=="reinforce","external_backaction_observed":kind=="reinforce"},"process_tensor_context":dict(PT),"source_digests":{"execution_record":"exec-v13-26","next_cycle_state":"next-v13-26" if kind=="reinforce" else "","memory_consumption":"memory-v13-26" if kind=="reinforce" else "","external_state_mutation":"external-v13-26" if kind=="reinforce" else ""},"boundary":dict(PACKET_BOUNDARY),"process_tensor_execution_feedback_digest":packet_digest,"epoch":1}
    state={"version":"physical_quantum_qi_path_integral_feedback_state_v12_7","path_integral_feedback_ready":True,"feedback_status":feedback,"path_weight_delta":packet["process_tensor_feedback_kernel"]["path_weight_delta"],"memory_feedback_weight":memory,"external_backaction_weight":external,"next_cycle_amplitude_delta":amp,"source_process_tensor_execution_feedback_digest":packet_digest,"process_tensor_context":dict(PT),"boundary":{**STATE_BOUNDARY,"can_feed_next_path_integral_cycle":kind=="reinforce"},"path_integral_feedback_state_digest":f"path-state-{kind}","epoch":1}
    ready_digest=f"receipt-ready-{kind}"
    ready={"version":"physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state_v13_11","process_tensor_feedback_receipt_ready_state":True,"bridge_status":"v12_7_to_v12_8_feedback_receipt_bridge_"+feedback.rsplit("_",1)[-1],"feedback_status":feedback,"execution_status":execution,"expected_v12_9_reentry_weighting_status":reentry,"expected_v12_9_reentry_weighting_action":action,"path_weight_delta":path_delta,"memory_feedback_weight":memory,"external_backaction_weight":external,"next_cycle_amplitude_delta":amp,"source_process_tensor_execution_feedback_digest":packet_digest,"process_tensor_context":dict(PT),"boundary":{"v12_8_feedback_receipt_ready_state_only":True,"v12_7_process_tensor_feedback_packet_required":True,"can_feed_v12_8_process_tensor_feedback_receipt_ledger":True,"can_feed_v12_9_feedback_to_reentry_weighting_bridge_after_receipt":True,"candidate_weighting_not_truth":True},"process_tensor_feedback_receipt_ready_state_digest":ready_digest,"epoch":1}
    activation={"version":"physical_quantum_qi_v13_25_feedback_receipt_activation_record","activation_status":"feedback_receipt_activation_completed","execution_status":execution,"expected_feedback_status":feedback,"observed_feedback_status":feedback,"source_v13_24_feedback_activation_record_digest":"v13-24-digest","source_v13_10_feedback_ready_state_digest":"v13-10-digest","source_v12_7_feedback_packet_digest":packet_digest,"source_v13_11_feedback_receipt_ready_state_digest":"wrong" if bad_ready_digest else ready_digest,"boundary":{"two_stage_feedback_receipt_activation":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"candidate_weighting_not_truth":True,"license_gated_feedback_activation":True,"fail_closed_on_boundary_loss":True},"feedback_receipt_activation_record_digest":f"v13-25-record-{kind}","epoch":1}
    write(root/"physical_quantum_qi_process_tensor_execution_feedback_packet.json",packet)
    write(root/"physical_quantum_qi_path_integral_feedback_state.json",state)
    write(root/"physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state.json",ready)
    write(root/"physical_quantum_qi_v13_25_feedback_receipt_activation_record.json",activation)

def license_packet(**overrides):
    value={"license_status":"PHYSICAL_QUANTUM_QI_V13_26_REENTRY_WEIGHTING_ACTIVATION_LICENSE_READY","v13_25_activation_record_read_allowed":True,"v12_8_feedback_receipt_ready_state_read_allowed":True,"v12_8_receipt_ledger_invoke_allowed":True,"v12_9_reentry_bridge_invoke_allowed":True,"activation_record_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True,"v12_8_receipt_ledger_license":{"license_status":"PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_LICENSE_READY","process_tensor_execution_feedback_packet_read_allowed":True,"path_integral_feedback_state_read_allowed":True,"receipt_ledger_append_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True},"v12_9_reentry_bridge_license":{"license_status":"PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_LICENSE_READY","process_tensor_feedback_receipt_ledger_read_allowed":True,"reentry_weighting_bridge_packet_write_allowed":True,"reentry_weighting_state_write_allowed":True,"summary_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}}
    value.update(overrides)
    return value

def context(root):
    return {"physical_quantum_qi_v13_26_reentry_weighting_activation_enabled":True,"apply_physical_quantum_qi_v13_26_reentry_weighting_activation":True,"runtime_root":str(root)}

def run(root,lic):
    return build_physical_quantum_qi_v13_26_reentry_weighting_activation(runtime_context=context(root),v13_26_reentry_weighting_activation_license=lic).to_dict()

def main():
    with tempfile.TemporaryDirectory() as td:
        base=pathlib.Path(td)
        for kind in ("reinforce","hold","block"):
            root=base/kind; prepare(root,kind); out=run(root,license_packet())
            feedback,_,reentry,action,*_=parts(kind)
            assert out["status"]=="PHYSICAL_QUANTUM_QI_V13_26_REENTRY_WEIGHTING_ACTIVATION_READY",(kind,out)
            assert out["feedback_status"]==feedback
            assert out["observed_reentry_weighting_status"]==reentry
            assert out["observed_reentry_weighting_action"]==action
            assert out["v12_8_receipt_ledger_invoked"] is True
            assert out["v12_9_reentry_bridge_invoked"] is True
            assert out["receipt_ledger_appended"] is True
            assert out["reentry_weighting_packet_written"] is True
            assert out["reentry_weighting_state_updated"] is True
            state=json.loads((root/"physical_quantum_qi_reentry_weighting_state.json").read_text(encoding="utf-8"))
            assert state["reentry_weighting_status"]==reentry and state["reentry_weighting_action"]==action
        root=base/"digest"; prepare(root,"reinforce",bad_ready_digest=True); out=run(root,license_packet())
        assert out["status"].endswith("BLOCKED") and out["v12_8_receipt_ledger_invoked"] is False
        assert "v13_25_feedback_receipt_ready_state_digest_mismatch" in out["blockers"]
        root=base/"packet"; prepare(root,"reinforce",bad_packet=True); out=run(root,license_packet())
        assert out["status"].endswith("BLOCKED") and out["v12_8_receipt_ledger_invoked"] is True and out["v12_9_reentry_bridge_invoked"] is False
        assert "v12_8_feedback_receipt_ledger_not_ready" in out["blockers"]
        root=base/"license"; prepare(root,"reinforce"); out=run(root,license_packet(v12_9_reentry_bridge_invoke_allowed=False))
        assert out["status"].endswith("BLOCKED") and out["v12_8_receipt_ledger_invoked"] is False
        assert "v12_9_reentry_bridge_invoke_not_allowed" in out["blockers"]
    print("physical_quantum_qi_v13_26_bridge checks passed")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
