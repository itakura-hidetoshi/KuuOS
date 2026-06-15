#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,pathlib,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from runtime.kuuos_indra_qi_world_dense_operator_proof_bridge_core_v0_27 import *

def write(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,sort_keys=True),encoding="utf-8")
def source(root):
    state={"version":SOURCE_STATE_VERSION,"spine_id":"s","analysis_run_id":"a","world_model_id":"w","source_world_state_digest":"wd","world_l2_embedding_report_digest":"er","carrier":{"scalar_field":"real","space_kind":"ell2_countable_real","complete_real_hilbert_space_declared":True},"representation_boundary":{"world_not_identified_with_hilbert_vector":True,"multi_world_noncollapse_preserved":True,"two_truths_gap_preserved":True},"operator_template":{"dense_core_declared":True,"symmetric_core_declared":True,"self_" + "adjointness_status":"not_asserted_by_runtime","unbounded_operator_execution_enabled":False},"decision":"world_l2_analytic_spine_ready"};state["world_l2_spine_state_digest"]=sha(state)
    rec={"version":SOURCE_RECOMMENDATION_VERSION,"spine_id":"s","analysis_run_id":"a","world_model_id":"w","source_world_state_digest":"wd","world_l2_embedding_report_digest":"er","decision":"world_l2_analytic_spine_ready","analytic_spine_ready":True,"recommendation_only":True,"runtime_validation_not_mathematical_theorem":True,"world_state_unchanged":True};rec["world_l2_spine_recommendation_digest"]=sha(rec)
    write(root/"indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json",state);write(root/"indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26.json",rec);return state,rec
def packet(root,state,rec):
    module=root/FORMAL_MODULE;ms=hashlib.sha256(module.read_bytes()).hexdigest()
    p={"version":PLAN_VERSION,"bridge_id":"b","bridge_run_id":"r","world_model_id":"w","expected_source_state_digest":state["world_l2_spine_state_digest"],"expected_source_recommendation_digest":rec["world_l2_spine_recommendation_digest"],"formal_module_path":FORMAL_MODULE,"expected_formal_module_sha256":ms,"boundary":dict(REQUIRED_BOUNDARY)};p["proof_bridge_plan_digest"]=plan_digest(p)
    report={"version":REPORT_VERSION,"bridge_run_id":"r","formal_module_sha256":ms,"instance_order":{"physical_hilbert_instances":["NormedAddCommGroup","InnerProductSpace ℝ","CompleteSpace"]},"realization_status":"formal_realization_obligation_bound_not_runtime_proved","proof_obligations":[{"theorem_id":x,"status":"bridge_theorem_declared","concrete_proof_claimed_by_runtime":False} for x in OBLIGATIONS]};report["proof_bridge_report_digest"]=report_digest(report)
    lic={"version":LICENSE_VERSION,"bound_plan_digest":p["proof_bridge_plan_digest"],"bound_report_digest":report["proof_bridge_report_digest"],"bound_source_state_digest":state["world_l2_spine_state_digest"],"bound_source_recommendation_digest":rec["world_l2_spine_recommendation_digest"],"bound_formal_module_sha256":ms,"state_write_allowed":True,"ledger_append_allowed":True,"recommendation_write_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True,"runtime_theorem_claim_authority_granted":False,"operator_execution_authority_granted":False,"world_update_authority_granted":False,"truth_authority_granted":False};return p,report,lic
def context(root): return {"runtime_root":str(root),"indra_qi_world_dense_operator_proof_bridge_v0_27_enabled":True,"apply_indra_qi_world_dense_operator_proof_bridge_v0_27":True}
def main():
    lean=(ROOT/FORMAL_MODULE).read_text(encoding="utf-8")
    for token in OBLIGATIONS: assert token in lean
    assert "worldNotIdentifiedWithCarrier" in lean and "spectralRealizationCertificate" in lean
    with tempfile.TemporaryDirectory() as d:
        root=pathlib.Path(d);(root/FORMAL_MODULE).parent.mkdir(parents=True);(root/FORMAL_MODULE).write_text(lean,encoding="utf-8");state,rec=source(root);before={p.name:p.read_bytes() for p in [root/"indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json",root/"indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26.json"]};p,r,l=packet(root,state,rec);result=build_world_dense_operator_proof_bridge(runtime_context=context(root),proof_bridge_plan=p,proof_bridge_license=l,proof_bridge_report=r);assert result.status==READY and result.decision=="world_dense_operator_proof_bridge_ready" and result.obligation_count==6;after={p.name:p.read_bytes() for p in [root/"indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json",root/"indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26.json"]};assert before==after
        replay=build_world_dense_operator_proof_bridge(runtime_context=context(root),proof_bridge_plan=p,proof_bridge_license=l,proof_bridge_report=r);assert replay.status==BLOCKED and "proof_bridge_replay_detected" in replay.blockers
    manifest=json.loads((ROOT/"manifests/qi_world_dense_operator_proof_bridge_v0_27.json").read_text())
    for group in ("runtime","scripts","docs","formal","example"):
        for rel in manifest[group]: assert (ROOT/rel).is_file(),rel
    print("qi_world_dense_operator_proof_bridge_v0_27 checks passed");return 0
if __name__=="__main__": raise SystemExit(main())
