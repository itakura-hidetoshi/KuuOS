#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import hashlib, json, os, pathlib, time
from typing import Any, Mapping

PLAN_VERSION = "indra_qi_world_dense_operator_proof_bridge_plan_v0_27"
REPORT_VERSION = "indra_qi_world_dense_operator_proof_bridge_report_v0_27"
LICENSE_VERSION = "indra_qi_world_dense_operator_proof_bridge_license_v0_27"
STATE_VERSION = "indra_qi_world_dense_operator_proof_bridge_state_v0_27"
LEDGER_VERSION = "indra_qi_world_dense_operator_proof_bridge_ledger_record_v0_27"
VERSION = "indra_qi_world_dense_operator_proof_bridge_v0_27"
READY = "INDRA_QI_WORLD_DENSE_OPERATOR_PROOF_BRIDGE_V0_27_READY"
BLOCKED = "INDRA_QI_WORLD_DENSE_OPERATOR_PROOF_BRIDGE_V0_27_BLOCKED"
SOURCE_STATE_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26"
SOURCE_RECOMMENDATION_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26"
FORMAL_MODULE = "formal/KUOS/WORLD/RealHilbertL2DenseOperatorProofBridgeV0_27.lean"
OBLIGATIONS = (
    "worldL2DenseCore_dense",
    "worldL2Diagonal_symmetric",
    "worldL2Diagonal_closable_obligation",
    "worldL2Diagonal_realization_obligation",
    "worldL2Rayleigh_global_lower_bound",
    "worldL2Spectrum_lower_bound_obligation",
)
REQUIRED_BOUNDARY = {
    "source_v0_26_state_exact": True,
    "source_v0_26_recommendation_exact": True,
    "formal_module_digest_exact": True,
    "real_hilbert_instances_explicit": True,
    "dense_domain_obligation_explicit": True,
    "symmetric_core_obligation_explicit": True,
    "closability_obligation_explicit": True,
    "closed_realization_obligation_explicit": True,
    "global_rayleigh_obligation_explicit": True,
    "spectrum_lower_bound_obligation_explicit": True,
    "runtime_does_not_claim_concrete_proof": True,
    "world_not_identified_with_hilbert_vector": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_operator_execution_authority": True,
    "fail_closed_on_digest_loss": True,
}

def M(x: Any) -> Mapping[str, Any]: return x if isinstance(x, Mapping) else {}
def L(x: Any) -> list[Any]: return x if isinstance(x, list) else []
def sha(x: Any) -> str: return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def file_sha(path: pathlib.Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def drop(x: Mapping[str, Any], field: str) -> dict[str, Any]:
    y = dict(x); y.pop(field, None); return y
def valid_digest(x: Mapping[str, Any], field: str) -> bool: return bool(x.get(field)) and x.get(field) == sha(drop(x, field))
def plan_digest(x: Mapping[str, Any]) -> str: return sha(drop(x, "proof_bridge_plan_digest"))
def report_digest(x: Mapping[str, Any]) -> str: return sha(drop(x, "proof_bridge_report_digest"))
def state_digest(x: Mapping[str, Any]) -> str: return sha(drop(x, "proof_bridge_state_digest"))
def read(path: pathlib.Path) -> dict[str, Any]:
    try: value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError): return {}
    return dict(value) if isinstance(value, Mapping) else {}
def readl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file(): return []
    out=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        try: v=json.loads(line)
        except json.JSONDecodeError: v={"_invalid": True}
        out.append(dict(v) if isinstance(v, Mapping) else {"_invalid": True})
    return out
def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(dict(value), ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8"); os.replace(tmp,path)
def append(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a",encoding="utf-8") as h: h.write(json.dumps(dict(value),ensure_ascii=False,sort_keys=True)+"\n")

def validate_source(root: pathlib.Path, plan: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    state=read(root/"indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json")
    rec=read(root/"indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26.json")
    if state.get("version") != SOURCE_STATE_VERSION or not valid_digest(state,"world_l2_spine_state_digest"):
        blockers.append("proof_bridge_source_state_invalid")
    if rec.get("version") != SOURCE_RECOMMENDATION_VERSION or not valid_digest(rec,"world_l2_spine_recommendation_digest"):
        blockers.append("proof_bridge_source_recommendation_invalid")
    sd=str(state.get("world_l2_spine_state_digest","")); rd=str(rec.get("world_l2_spine_recommendation_digest",""))
    if plan.get("expected_source_state_digest") != sd: blockers.append("proof_bridge_expected_state_digest_mismatch")
    if plan.get("expected_source_recommendation_digest") != rd: blockers.append("proof_bridge_expected_recommendation_digest_mismatch")
    if rec.get("decision") != "world_l2_analytic_spine_ready": blockers.append("proof_bridge_source_not_ready")
    if state.get("decision") != rec.get("decision") or state.get("world_model_id") != rec.get("world_model_id"):
        blockers.append("proof_bridge_source_chain_invalid")
    carrier=M(state.get("carrier")); op=M(state.get("operator_template")); boundary=M(state.get("representation_boundary"))
    if not (carrier.get("scalar_field")=="real" and carrier.get("space_kind")=="ell2_countable_real" and carrier.get("complete_real_hilbert_space_declared") is True): blockers.append("proof_bridge_source_carrier_invalid")
    if not (op.get("dense_core_declared") is True and op.get("symmetric_core_declared") is True and op.get("self_" + "adjointness_status")=="not_asserted_by_runtime" and op.get("unbounded_operator_execution_enabled") is False): blockers.append("proof_bridge_source_operator_template_invalid")
    if not (boundary.get("world_not_identified_with_hilbert_vector") is True and boundary.get("multi_world_noncollapse_preserved") is True and boundary.get("two_truths_gap_preserved") is True): blockers.append("proof_bridge_source_boundary_invalid")
    return {"state":state,"recommendation":rec,"state_digest":sd,"recommendation_digest":rd,"world_model_id":str(state.get("world_model_id",""))}

def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION: blockers.append("proof_bridge_plan_version_invalid")
    if plan.get("proof_bridge_plan_digest") != plan_digest(plan): blockers.append("proof_bridge_plan_digest_invalid")
    for f in ("bridge_id","bridge_run_id","world_model_id","expected_source_state_digest","expected_source_recommendation_digest","expected_formal_module_sha256"):
        if not str(plan.get(f,"")): blockers.append(f"proof_bridge_plan_{f}_missing")
    if plan.get("formal_module_path") != FORMAL_MODULE: blockers.append("proof_bridge_formal_module_path_invalid")
    for f,v in REQUIRED_BOUNDARY.items():
        if M(plan.get("boundary")).get(f) is not v: blockers.append(f"proof_bridge_boundary_{f}_mismatch")

def validate_report(root: pathlib.Path, report: Mapping[str, Any], plan: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    if report.get("version") != REPORT_VERSION: blockers.append("proof_bridge_report_version_invalid")
    if report.get("bridge_run_id") != plan.get("bridge_run_id"): blockers.append("proof_bridge_report_run_id_mismatch")
    if report.get("proof_bridge_report_digest") != report_digest(report): blockers.append("proof_bridge_report_digest_invalid")
    module=root/FORMAL_MODULE
    if not module.is_file(): blockers.append("proof_bridge_formal_module_missing"); actual=""
    else: actual=file_sha(module)
    if plan.get("expected_formal_module_sha256") != actual or report.get("formal_module_sha256") != actual: blockers.append("proof_bridge_formal_module_digest_mismatch")
    declared={str(M(x).get("theorem_id","")):M(x) for x in L(report.get("proof_obligations"))}
    if set(declared) != set(OBLIGATIONS): blockers.append("proof_bridge_obligation_set_invalid")
    for theorem_id in OBLIGATIONS:
        row=declared.get(theorem_id,{})
        if row.get("status") != "bridge_theorem_declared": blockers.append(f"proof_bridge_{theorem_id}_status_invalid")
        if row.get("concrete_proof_claimed_by_runtime") is not False: blockers.append(f"proof_bridge_{theorem_id}_runtime_claim_invalid")
    instances=M(report.get("instance_order"))
    if list(instances.get("physical_hilbert_instances",[])) != ["NormedAddCommGroup","InnerProductSpace ℝ","CompleteSpace"]: blockers.append("proof_bridge_instance_order_invalid")
    if report.get("realization_status") != "formal_realization_obligation_bound_not_runtime_proved": blockers.append("proof_bridge_realization_status_invalid")
    return {"module_sha256":actual,"obligations":declared}

@dataclass(frozen=True)
class Result:
    version:str; status:str; packet_id:str; runtime_root:str; bridge_id:str; bridge_run_id:str; world_model_id:str; decision:str; formal_module_sha256:str; obligation_count:int; source_state_digest:str; source_recommendation_digest:str; proof_bridge_state_digest:str; ledger_record_digest:str; blockers:list[str]

def build_world_dense_operator_proof_bridge(*,runtime_context:Mapping[str,Any],proof_bridge_plan:Mapping[str,Any],proof_bridge_license:Mapping[str,Any],proof_bridge_report:Mapping[str,Any])->Result:
    c=M(runtime_context);p=dict(M(proof_bridge_plan));lic=M(proof_bridge_license);r=dict(M(proof_bridge_report));b=[]
    rv=c.get("runtime_root"); root=pathlib.Path(str(rv)).expanduser().resolve() if rv else pathlib.Path(".").resolve()
    if not rv or root==pathlib.Path("/").resolve(): b.append("runtime_root_invalid")
    if c.get("indra_qi_world_dense_operator_proof_bridge_v0_27_enabled") is not True or c.get("apply_indra_qi_world_dense_operator_proof_bridge_v0_27") is not True: b.append("proof_bridge_not_enabled")
    validate_plan(p,b); src=validate_source(root,p,b); formal=validate_report(root,r,p,b)
    expected={"version":LICENSE_VERSION,"bound_plan_digest":str(p.get("proof_bridge_plan_digest","")),"bound_report_digest":str(r.get("proof_bridge_report_digest","")),"bound_source_state_digest":str(src.get("state_digest","")),"bound_source_recommendation_digest":str(src.get("recommendation_digest","")),"bound_formal_module_sha256":str(formal.get("module_sha256",""))}
    for f,v in expected.items():
        if lic.get(f)!=v: b.append(f"proof_bridge_license_{f}_mismatch")
    for f in ("state_write_allowed","ledger_append_allowed","recommendation_write_allowed","receipt_write_allowed","audit_append_allowed"):
        if lic.get(f) is not True: b.append(f"proof_bridge_license_{f}_not_true")
    for f in ("runtime_theorem_claim_authority_granted","operator_execution_authority_granted","world_update_authority_granted","truth_authority_granted"):
        if lic.get(f) is not False: b.append(f"proof_bridge_license_{f}_not_false")
    bridge_id=str(p.get("bridge_id",""));run_id=str(p.get("bridge_run_id",""));world_id=str(p.get("world_model_id",""));ledger_path=root/"indra_qi_world_dense_operator_proof_bridge_ledger_v0_27.jsonl";prior=readl(ledger_path);prev="GENESIS"
    for i,row in enumerate(prior):
        if row.get("_invalid") or row.get("version")!=LEDGER_VERSION or not valid_digest(row,"record_digest") or row.get("prev_record_digest")!=prev: b.append(f"proof_bridge_ledger_record_{i}_invalid")
        prev=str(row.get("record_digest",""))
    if any(row.get("bridge_run_id")==run_id or row.get("source_state_digest")==src.get("state_digest") for row in prior): b.append("proof_bridge_replay_detected")
    prior_state=read(root/"indra_qi_world_dense_operator_proof_bridge_state_v0_27.json")
    if prior_state and not valid_digest(prior_state,"proof_bridge_state_digest"): b.append("proof_bridge_prior_state_invalid")
    decision="world_dense_operator_proof_bridge_ready" if not b else "quarantine_recommended"; now=int(time.time())
    common={"bridge_id":bridge_id,"bridge_run_id":run_id,"world_model_id":world_id,"source_state_digest":str(src.get("state_digest","")),"source_recommendation_digest":str(src.get("recommendation_digest","")),"formal_module_path":FORMAL_MODULE,"formal_module_sha256":str(formal.get("module_sha256","")),"obligation_ids":list(OBLIGATIONS),"runtime_concrete_proof_claimed":False,"operator_executed":False,"world_updated":False,"recommendation_only":True}
    state={"version":STATE_VERSION,**common,"decision":decision,"realization_status":"formal_realization_obligation_bound_not_runtime_proved","prev_proof_bridge_state_digest":str(prior_state.get("proof_bridge_state_digest","GENESIS")) if prior_state else "GENESIS","epoch":now};state["proof_bridge_state_digest"]=state_digest(state)
    rec={"version":"indra_qi_world_dense_operator_proof_bridge_recommendation_v0_27",**common,"decision":decision,"bridge_ready":decision=="world_dense_operator_proof_bridge_ready","direct_runtime_theorem_claim_authority":False,"direct_operator_execution_authority":False,"direct_world_update_authority":False,"truth_authority":False,"epoch":now};rec["proof_bridge_recommendation_digest"]=sha(rec)
    ledger={"version":LEDGER_VERSION,**common,"decision":decision,"proof_bridge_state_digest":state["proof_bridge_state_digest"],"prev_record_digest":str(prior[-1].get("record_digest","GENESIS")) if prior else "GENESIS","epoch":now};ledger["record_digest"]=sha(ledger)
    status=READY if not b else BLOCKED;receipt={"version":VERSION,"status":status,**common,"decision":decision,"proof_bridge_state_digest":state["proof_bridge_state_digest"] if not b else "","ledger_record_digest":ledger["record_digest"] if not b else "","blockers":b,"epoch":now};receipt["packet_id"]="indra-qi-world-proof-bridge-"+sha(receipt)[:16]
    if not b:
        write(root/"indra_qi_world_dense_operator_proof_bridge_state_v0_27.json",state);write(root/"indra_qi_world_dense_operator_proof_bridge_recommendation_v0_27.json",rec);append(ledger_path,ledger)
    if lic.get("receipt_write_allowed") is True: write(root/"indra_qi_world_dense_operator_proof_bridge_receipt_v0_27.json",receipt)
    if lic.get("audit_append_allowed") is True: append(root/"indra_qi_world_dense_operator_proof_bridge_audit_v0_27.jsonl",{**receipt,"audit_record_digest":sha(receipt)})
    return Result(VERSION,status,str(receipt["packet_id"]),str(root),bridge_id,run_id,world_id,decision,str(formal.get("module_sha256","")),len(OBLIGATIONS),str(src.get("state_digest","")),str(src.get("recommendation_digest","")),state["proof_bridge_state_digest"] if not b else "",ledger["record_digest"] if not b else "",b)
