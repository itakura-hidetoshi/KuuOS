#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json, os, pathlib, time
from typing import Any, Mapping

BRIDGE = {
    "cycle_gate_reentry_integration_admit": ("integrated_candidate_to_guarded_intent_ready", "guarded_execution_intent_ready", "emit_guarded_ready_intent", 1),
    "cycle_gate_reentry_integration_hold": ("integrated_candidate_to_guarded_intent_hold", "guarded_execution_intent_hold", "emit_guarded_hold_intent", 0),
    "cycle_gate_reentry_integration_block": ("integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0),
}
GATE = {"cycle_gate_reentry_integration_admit":"integrated_cycle_gate_admit","cycle_gate_reentry_integration_hold":"integrated_cycle_gate_hold","cycle_gate_reentry_integration_block":"integrated_cycle_gate_block"}
SET = {"cycle_gate_reentry_integration_admit":"integrated_admissible_candidate_set_admit","cycle_gate_reentry_integration_hold":"integrated_admissible_candidate_set_probe","cycle_gate_reentry_integration_block":"integrated_admissible_candidate_set_block"}
REQ_BOUNDARY = ("receipt_ledger_only","cycle_gate_reentry_integration_receipt_only","integrated_cycle_gate_state_traceable","integrated_admissible_candidate_set_traceable","uses_process_tensor_feedback","non_markov_feedback_preserved","history_window_feedback_preserved","memory_kernel_feedback_preserved","external_backaction_visible","candidate_weighting_not_truth","integration_not_direct_execution","replayable_receipt","fail_closed_on_boundary_loss")
REQ_CTX = ("process_tensor_digest","memory_kernel_digest","history_window_digest","instrument_trace_digest","non_markov_context_digest")

@dataclass(frozen=True)
class PhysicalQuantumQiV13_5ToV13_6GuardedIntentBridgeResult:
    version: str; status: str; packet_id: str; runtime_root: str; bridge_status: str
    integration_status: str; guarded_execution_intent_status: str; guarded_intent_emit_action: str
    expected_guarded_execution_intent_count: int; guarded_intent_ready_state_written: bool; bridge_ledger_appended: bool
    guarded_intent_ready_state_path: str; bridge_ledger_path: str; summary_path: str; receipt_path: str; audit_path: str
    blockers: list[str]; warnings: list[str]
    def to_dict(self) -> dict[str, Any]: return asdict(self)

def _m(v: Any) -> Mapping[str, Any]: return v if isinstance(v, Mapping) else {}
def _sha(v: Any) -> str: return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def _int(v: Any) -> int:
    try: return int(v or 0)
    except (TypeError, ValueError): return 0

def _root(v: Any, b: list[str]) -> pathlib.Path:
    if not v: b.append("runtime_root_missing"); return pathlib.Path(".").resolve()
    p = pathlib.Path(str(v)).expanduser().resolve()
    if p == pathlib.Path("/").resolve(): b.append("runtime_root_forbidden")
    return p

def _write(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8"); os.replace(tmp, path)

def _append(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as h: h.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)+"\n")

def _latest(path: pathlib.Path, b: list[str]) -> dict[str, Any]:
    if not path.is_file(): b.append("cycle_gate_reentry_integration_receipt_ledger_missing"); return {}
    last = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip(): last = line
    if not last: b.append("cycle_gate_reentry_integration_receipt_ledger_empty"); return {}
    try: v = json.loads(last)
    except json.JSONDecodeError: b.append("cycle_gate_reentry_integration_receipt_ledger_latest_line_invalid"); return {}
    return v if isinstance(v, dict) else {}

def _prev(path: pathlib.Path) -> str:
    if not path.is_file(): return "GENESIS"
    last = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip(): last = line
    if not last: return "GENESIS"
    try: v = json.loads(last)
    except json.JSONDecodeError: return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(v.get("record_digest", _sha(v)))

def _weight(w: Mapping[str, Any]) -> dict[str, Any]:
    return {"path_weight_delta":_int(w.get("path_weight_delta")),"probe_potential_required":w.get("probe_potential_required") is True,"barrier_potential_required":w.get("barrier_potential_required") is True,"barrier_blocks_ready_weight":w.get("barrier_blocks_ready_weight") is True,"memory_feedback_weight":_int(w.get("memory_feedback_weight")),"external_backaction_weight":_int(w.get("external_backaction_weight")),"next_cycle_amplitude_delta":_int(w.get("next_cycle_amplitude_delta"))}

def _ctx(c: Mapping[str, Any], b: list[str]) -> dict[str, str]:
    out = {k: str(c.get(k, "")) for k in REQ_CTX}
    for k, v in out.items():
        if not v: b.append(f"process_tensor_context_{k}_missing")
    return out

def _check_weight(status: str, w: dict[str, Any], b: list[str]) -> None:
    if status == "cycle_gate_reentry_integration_admit" and (w["path_weight_delta"] <= 0 or w["probe_potential_required"] or w["barrier_potential_required"] or w["barrier_blocks_ready_weight"] or w["memory_feedback_weight"] <= 0 or w["external_backaction_weight"] <= 0 or w["next_cycle_amplitude_delta"] <= 0): b.append("v13_6_bridge_admit_weighting_invalid")
    if status == "cycle_gate_reentry_integration_hold" and (w["path_weight_delta"] != 0 or not w["probe_potential_required"] or w["barrier_potential_required"] or w["barrier_blocks_ready_weight"] or w["memory_feedback_weight"] != 0 or w["external_backaction_weight"] != 0 or w["next_cycle_amplitude_delta"] != 0): b.append("v13_6_bridge_hold_weighting_invalid")
    if status == "cycle_gate_reentry_integration_block" and (w["path_weight_delta"] != 0 or w["probe_potential_required"] or not w["barrier_potential_required"] or not w["barrier_blocks_ready_weight"] or w["memory_feedback_weight"] != 0 or w["external_backaction_weight"] != 0 or w["next_cycle_amplitude_delta"] != 0): b.append("v13_6_bridge_block_weighting_invalid")

def _validate(record: Mapping[str, Any], b: list[str]) -> dict[str, Any]:
    if not record: return {}
    if record.get("record_type") != "physical_quantum_qi_cycle_gate_reentry_integration_receipt": b.append("cycle_gate_reentry_integration_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for flag in REQ_BOUNDARY:
        if boundary.get(flag) is not True: b.append(f"cycle_gate_reentry_integration_receipt_boundary_{flag}_missing")
    status = str(record.get("integration_status", "cycle_gate_reentry_integration_block"))
    if status not in BRIDGE: b.append("cycle_gate_reentry_integration_status_invalid"); status = "cycle_gate_reentry_integration_block"
    bridge, guarded, emit, _ = BRIDGE[status]
    if str(record.get("integrated_cycle_gate_status", "")) != GATE[status]: b.append("cycle_gate_reentry_integration_receipt_gate_status_mismatch")
    if str(record.get("integrated_admissible_candidate_set_status", "")) != SET[status]: b.append("cycle_gate_reentry_integration_receipt_candidate_set_status_mismatch")
    count = _int(record.get("admissible_candidate_count")); candidates = record.get("integrated_candidates", [])
    if not isinstance(candidates, list): b.append("integrated_candidates_not_list"); candidates = []
    if status in {"cycle_gate_reentry_integration_admit", "cycle_gate_reentry_integration_hold"} and (count <= 0 or len(candidates) != count): b.append("v13_6_bridge_requires_integrated_candidate_for_admit_or_hold")
    if status == "cycle_gate_reentry_integration_block" and (count != 0 or candidates): b.append("v13_6_bridge_block_with_integrated_candidates")
    w = _weight(_m(record.get("candidate_weighting"))); _check_weight(status, w, b)
    return {"integration_status":status,"bridge_status":bridge,"guarded_execution_intent_status":guarded,"guarded_intent_emit_action":emit,"expected_guarded_execution_intent_count": count if guarded == "guarded_execution_intent_ready" else 0,"admissible_candidate_count":count,"integrated_candidates":candidates,"candidate_weighting":w,"process_tensor_context":_ctx(_m(record.get("process_tensor_context")), b),"source_cycle_gate_reentry_integration_receipt_digest":str(record.get("record_digest", _sha(dict(record)))),"source_cycle_gate_reentry_integration_digest":str(record.get("source_cycle_gate_reentry_integration_digest", ""))}

def build_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge(*, runtime_context: Mapping[str, Any], v13_5_to_v13_6_guarded_intent_bridge_license: Mapping[str, Any]) -> PhysicalQuantumQiV13_5ToV13_6GuardedIntentBridgeResult:
    ctx, lic = _m(runtime_context), _m(v13_5_to_v13_6_guarded_intent_bridge_license); blockers: list[str] = []; warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger = root/"physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl"; ready = root/"physical_quantum_qi_v13_6_integrated_candidate_to_guarded_intent_ready_state.json"; blog = root/"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_ledger.jsonl"; summary = root/"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_summary.json"; receipt = root/"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_receipt.json"; audit = root/"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_audit.jsonl"
    if ctx.get("physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_enabled") is not True: blockers.append("physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge") is not True: blockers.append("apply_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_LICENSE_READY": blockers.append("physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_license_not_ready")
    for n in ["v13_5_integration_receipt_ledger_read_allowed","v13_6_guarded_intent_ready_state_write_allowed","bridge_ledger_append_allowed","summary_write_allowed","receipt_write_allowed","audit_append_allowed"]:
        if lic.get(n) is not True: blockers.append(n.replace("allowed", "not_allowed"))
    payload = _validate(_latest(ledger, blockers), blockers)
    written = appended = False
    if not blockers:
        epoch = int(time.time())
        rs = {"version":"physical_quantum_qi_v13_6_integrated_candidate_to_guarded_intent_ready_state_v13_18","integrated_candidate_to_guarded_intent_ready_state":True,**payload,"boundary":{"v13_6_guarded_intent_bridge_ready_state_only":True,"v13_5_integration_receipt_required":True,"can_feed_v13_6_integrated_candidate_to_guarded_intent_bridge":True,"emits_guarded_execution_intent_packet_after_v13_6":True,"uses_process_tensor_feedback":True,"non_markov_feedback_preserved":True,"history_window_feedback_preserved":True,"memory_kernel_feedback_preserved":True,"external_backaction_visible":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"does_not_run_guarded_intent_bridge":True,"does_not_run_runner":True,"does_not_mutate_external_state":True,"does_not_start_next_cycle":True,"fail_closed_on_boundary_loss":True},"epoch":epoch}
        rs["guarded_intent_bridge_ready_state_digest"] = _sha(rs); _write(ready, rs); written = True
        rec = {"version":"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_record_v13_18","record_type":"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge","source_guarded_intent_bridge_ready_state_digest":rs["guarded_intent_bridge_ready_state_digest"],"prev_record_digest":_prev(blog),"boundary":{"bridge_receipt_only":True,"v13_6_guarded_intent_bridge_ready_state_traceable":True,"same_semantic_root":True,"uses_process_tensor_feedback":True,"candidate_weighting_not_truth":True,"bridge_not_direct_execution":True,"replayable_receipt":True},"epoch":epoch,**{k:payload[k] for k in ["bridge_status","integration_status","guarded_execution_intent_status","guarded_intent_emit_action","expected_guarded_execution_intent_count","source_cycle_gate_reentry_integration_receipt_digest"]}}
        rec["record_digest"] = _sha(rec); _append(blog, rec); appended = True
        sm = {"version":"physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_summary_v13_18","boundary":{"summary_only":True,"can_feed_v13_6_integrated_candidate_to_guarded_intent_bridge":True,"candidate_weighting_not_truth":True},"epoch":epoch,**{k:payload[k] for k in ["bridge_status","integration_status","guarded_execution_intent_status","guarded_intent_emit_action","expected_guarded_execution_intent_count"]}}
        sm["summary_digest"] = _sha(sm); _write(summary, sm)
    status = "PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_BLOCKED"
    pkt = "physical-quantum-qi-v13-5-to-v13-6-guarded-intent-bridge-" + _sha({"payload":payload,"blockers":blockers})[:16]
    bridge_status = str(payload.get("bridge_status", "integrated_candidate_to_guarded_intent_block")); integration = str(payload.get("integration_status", "cycle_gate_reentry_integration_block")); guarded = str(payload.get("guarded_execution_intent_status", "guarded_execution_intent_block")); emit = str(payload.get("guarded_intent_emit_action", "emit_guarded_block_intent")); expected = _int(payload.get("expected_guarded_execution_intent_count"))
    rc = {"version":"kuuos_runtime_daemon_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_v13_18","status":status,"packet_id":pkt,"bridge_status":bridge_status,"integration_status":integration,"guarded_execution_intent_status":guarded,"guarded_intent_emit_action":emit,"expected_guarded_execution_intent_count":expected,"guarded_intent_ready_state_written":written,"bridge_ledger_appended":appended,"blockers":blockers,"warnings":warnings,"epoch":int(time.time())}
    if lic.get("receipt_write_allowed") is True: _write(receipt, rc)
    if lic.get("audit_append_allowed") is True: _append(audit, {**rc, "audit_record_digest": _sha(rc)})
    return PhysicalQuantumQiV13_5ToV13_6GuardedIntentBridgeResult("kuuos_runtime_daemon_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_v13_18",status,pkt,str(root),bridge_status,integration,guarded,emit,expected,written,appended,str(ready),str(blog),str(summary),str(receipt),str(audit),blockers,warnings)
