#!/usr/bin/env python3
"""Project actual two-runner CodeAI portfolio evidence into the existing
version-bound memory and v0.2 ensemble. Formal success is NOT a four-family
utility certificate. No external provider, theorem change, or memory promotion.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import ci_verified_lean_project_cache_v1 as cache
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from runtime import kuuos_codeai_subtask_level_version_bound_memory_v0_1 as mem
from runtime import kuuos_codeai_independent_verifier_ensemble_v0_2 as ens
from scripts.build_codeai_independent_verifier_ensemble_fixture_v0_2 import build_request, build_policy

REPO = "itakura-hidetoshi/KuuOS"
MAIN = "e1d754e8e0fc9382001a2e698751aa11d4272b84"
TREE = "bdf2e81fc2cf702481b80e7079e59b1b47836013"
HEAD = "f58b08eca16c13669d2b951fcbe755a610d23695"
RUN = 45719609942
SCOPE = "2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b"
PORTFOLIO = "97a628794bed5c5ae7c582383cf907fcf16716772c26bce3a52f8c99cbf45a72"
DIRECT = "6b3c5c6f359253d4e32154a0c8d1c8f92afbc99175361c46613cb6488fb23be2"
MCP = "673ab171a99417a76c9a888958e59036594131c4fe971a2ed91f8a91d7bba860"
ARTIFACTS = (
    (15071023603, 14343, "247a3237c2bc475eb69054f2890ff1e315a4b186d804ddbc44b236d085fa674e", "local"),
    (15071458472, 13622, "f51c1f784e3aaa217d82b09454b41602b56e143fc381c33cdcc664967febfc75", "independent"),
)
JOBS = (139574324619, 139576762337)
A = "a-missing-hypothesis"
B = "b-exact-reuse"
SOURCE = "formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean"
TARGET = "Kuu.LivingEngi.sourceGlobal_implies_overlapFaithful"

def need(ok, why):
    if not ok:
        raise ValueError(why)

def digest(value):
    return mem.canonical_digest(value)

def sha(value):
    return hashlib.sha256(value).hexdigest()

def save(out, name, value):
    (out/name).write_text(json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def epoch(value):
    return int(datetime.fromisoformat(value.replace("Z","+00:00")).timestamp())

def provenance(out):
    run=cache.api(f"actions/runs/{RUN}")
    need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
         and run["conclusion"]=="success"
         and run["path"]==".github/workflows/codeai-certified-cache-candidate-portfolio-v1.yml",
         "historical workflow identity or status mismatch")
    rows=cache.api(f"actions/runs/{RUN}/jobs?per_page=100")
    need(rows["total_count"]==2 and {j["id"] for j in rows["jobs"]}==set(JOBS),"job inventory mismatch")
    jobs=[]
    for jid in JOBS:
        j=next(x for x in rows["jobs"] if x["id"]==jid)
        need(j["status"]=="completed" and j["conclusion"]=="success","job not green")
        required=["Restore verified canonical project cache","Require actual cache hit, build selected module"]
        required+=["Generate two actual structured candidate patches and compare direct Lean",
                   "Actual Lean MCP diagnostics and verification"] if jid==JOBS[0] else [
                       "Independently regenerate admitted patches and compare Lean evidence"]
        for name in required:
            s=[s for s in j["steps"] if s["name"]==name]
            need(len(s)==1 and s[0]["status"]=="completed" and s[0]["conclusion"]=="success",
                 "required historical step missing: "+name)
        jobs.append({"id":jid,"started_at":j["started_at"],"completed_at":j["completed_at"],
                     "required_steps":required})
    artifacts=[]
    for aid,size,checksum,role in ARTIFACTS:
        a=cache.api(f"actions/artifacts/{aid}")
        need(a["id"]==aid and a["name"]==f"codeai-portfolio-{role}-{RUN}-1"
             and a["size_in_bytes"]==size and a["digest"]=="sha256:"+checksum
             and a["expired"] is False and a["workflow_run"]["id"]==RUN
             and a["workflow_run"]["head_sha"]==HEAD
             and a["workflow_run"]["repository_id"]==cache.REPO_ID
             and a["workflow_run"]["head_repository_id"]==cache.REPO_ID,"artifact origin mismatch")
        path=out/(role+".zip")
        cache.download_zip({"artifact_id":aid,"artifact_size":size,"artifact_digest":checksum},path)
        artifacts.append({"id":aid,"role":role,"size":size,"sha256":checksum})
    return {"run":RUN,"head":HEAD,"jobs":jobs,"artifacts":artifacts}

def read_archive(path):
    with zipfile.ZipFile(path) as z:
        names=[i.filename for i in z.infolist()]
        need(len(names)==len(set(names)) and len(names)<80,"unsafe evidence archive inventory")
        def get(n):
            i=z.getinfo(n)
            need(not i.is_dir() and 0<i.file_size<2_000_000,"unsafe archive member "+n)
            return z.read(i)
        def obj(n): return json.loads(get(n))
        result={k:obj(k+".json") for k in ("gate","portfolio","direct","synthesis","source-observation")}
        result["cases"]={}
        for key in (A,B):
            result["cases"][key]={
                "source":get(key+"/Probe.lean"),
                "patch":get(key+"/candidate.diff"),
                "log":get(key+"/direct.log"),
                "candidate":obj(key+"/candidate.json"),
                "receipt":obj(key+"/candidate-receipt.json"),
            }
        result["winner"]=get("Probe.lean")
        if "mcp.json" in names:
            result["mcp"]=obj("mcp.json")
        if "independent.json" in names:
            result["independent"]=obj("independent.json")
        return result

def verify(out, origin):
    first=read_archive(out/"local.zip")
    fresh=read_archive(out/"independent.zip")
    p=first["portfolio"]; d=first["direct"]; m=first["mcp"]; i=fresh["independent"]
    g=first["gate"]
    need(p==fresh["portfolio"] and digest(p)==PORTFOLIO and p["head"]==MAIN
         and p["tree"]==TREE and p["scope"]==SCOPE and p["selected"]==B
         and p["external_model"] is False and p["new_mathematical_result"] is False
         and p["formal_source_changed"] is False,"portfolio identity mismatch")
    need(g==fresh["gate"] and g==d["gate"] and digest(g)==p["gate_digest"]
         and g["scope"]=="canonical_main" and g["target"]==TARGET
         and g["new_status"]=="HOLD_DUPLICATE_REUSE_REQUIRED" and g["reuse_status"]=="REUSE_EXISTING"
         and g["provider_calls"]==0 and g["unobserved_hits"]==[],"gate mismatch")
    need(d==fresh["direct"] and digest(d)==DIRECT and d["direct_exit"]==0 and d["axioms"]==[]
         and m["status"]=="REAL_LEAN_MCP_REUSE_GREEN" and m["direct_digest"]==DIRECT
         and m["axioms"]==[] and m["mcp_version"]=="0.30.0" and digest(m)==MCP
         and i["status"]=="INDEPENDENT_PORTFOLIO_GREEN" and i["portfolio_digest"]==PORTFOLIO
         and i["first_mcp_digest"]==MCP,"direct/MCP/independent binding mismatch")
    cases={}
    for key in (A,B):
        x,y=first["cases"][key],fresh["cases"][key]
        need(all(x[k]==y[k] for k in ("source","patch","log")),"runner bytes differ: "+key)
        row=next(v for v in p["candidates"] if v["id"]==key)
        need(sha(x["source"])==row["source_sha256"] and sha(x["patch"])==row["patch_sha256"],
             "candidate bytes mismatch")
        for archive in (first,fresh):
            v=archive["cases"][key]
            candidate,receipt=v["candidate"],v["receipt"]
            source=archive["source-observation"]["receipt"]
            need(source[patch.SOURCE_RECEIPT_DIGEST_FIELD]==patch.digest_without(source,patch.SOURCE_RECEIPT_DIGEST_FIELD)
                 and source["source_commit_sha"]==MAIN and source["tree_digest"]==TREE
                 and source["repository_observation_read_only"] is True,
                 "source observation receipt mismatch")
            need(candidate[patch.CANDIDATE_DIGEST_FIELD]==patch.digest_without(candidate,patch.CANDIDATE_DIGEST_FIELD)
                 and receipt[patch.RECEIPT_DIGEST_FIELD]==patch.digest_without(receipt,patch.RECEIPT_DIGEST_FIELD)
                 and receipt["candidate_patch_digest"]==candidate[patch.CANDIDATE_DIGEST_FIELD]
                 and candidate["source_observation_receipt_digest"]==source[patch.SOURCE_RECEIPT_DIGEST_FIELD]
                 and candidate["candidate_id"]==key and candidate["source_commit_sha"]==MAIN
                 and candidate["patch_artifact_digest"]==patch.patch_artifact_digest(v["patch"].decode())
                 and receipt["candidate_patch_ready"] is True and receipt["candidate_selected"] is False,
                 "original CodeAI receipt mismatch")
        cases[key]={**row,"log_sha256":sha(x["log"])}
    a,b=first["cases"][A],first["cases"][B]
    error=a["log"].decode("utf-8")
    need(cases[A]["exit"]==1 and cases[A]["direct_green"] is False
         and "error: Type mismatch" in error
         and "HasGlobal U s → OverlapFiberFaithful U q s" in error and "sorryAx" in error,
         "negative diagnostic absent")
    need(cases[B]["exit"]==0 and cases[B]["direct_green"] is True
         and "does not depend on any axioms" in b["log"].decode()
         and "sorryAx" not in b["log"].decode()
         and first["winner"]==fresh["winner"]==b["source"] and d["probe_sha256"]==sha(b["source"]),
         "positive evidence mismatch")
    need(a["source"].replace(b"sourceGlobal_implies_overlapFaithful U q s\n",
                             b"sourceGlobal_implies_overlapFaithful U q s h\n")==b["source"],
         "candidate difference is not the observed missing hypothesis")
    diagnostic={"target":TARGET,"source_blob":first["source-observation"]["source_blobs"][SOURCE],
                "type_expr_sha256":g["type_expr_sha256"],"failed":cases[A],"successful_alternative":cases[B],
                "actual_lean_log":error,"observed_difference":"explicit final hypothesis h",
                "native_static_error_taxonomy_certificate":"NO_DATA",
                "general_repair_usefulness":"NO_DATA","candidate_A_admitted":False,
                "scope":SCOPE,"source_head":MAIN,"proof_authority":False}
    save(out,"diagnostic.json",diagnostic)
    evidence={"origin":origin,"canonical_head":MAIN,"canonical_tree":TREE,"scope_digest":SCOPE,
              "portfolio_digest":PORTFOLIO,"direct_digest":DIRECT,"mcp_digest":MCP,
              "independent":i,"gate":g,"cases":cases,"diagnostic_digest":digest(diagnostic),
              "source_blob":diagnostic["source_blob"],"external_model":False,
              "new_mathematical_result":False}
    save(out,"evidence.json",evidence)
    return evidence

def ensemble_hold(out,e):
    # Actual single formal-family observation, not independent issuer attestation.
    now=epoch(e["origin"]["jobs"][1]["completed_at"])
    ctx=digest({"canonical_head":MAIN,"tree":TREE,"scope":SCOPE,"target":TARGET,
                "source_blob":e["source_blob"]})
    req=ens.seal(dict(build_request(),request_id="actual-portfolio-formal-only",
        repository_full_name=REPO,source_commit_sha=MAIN,candidate_digest=e["cases"][B]["source_sha256"],
        context_pack_digest=ctx,request_created_epoch=now),ens.REQUEST_DIGEST_FIELD)
    policy=ens.seal(dict(build_policy(),expected_repository_full_name=REPO,
        expected_source_commit_sha=MAIN,expected_candidate_digest=req["candidate_digest"],
        expected_context_pack_digest=ctx,evaluation_epoch=now,maximum_evidence_age=3600,
        maximum_verification_duration=3600,allowed_verifier_ids=["github-lean-formal"],
        allowed_reviewer_ids=["unattested-reviewer"],allowed_runner_ids=["github-independent-runner"]),
        ens.POLICY_DIGEST_FIELD)
    checks=["axiom-free-direct-lean","independent-source-and-log-agreement"]
    packet=ens.seal({
        "evidence_id":"observed-45719609942-formal-only","verifier_id":"github-lean-formal",
        "reviewer_id":"unattested-reviewer","runner_id":"github-independent-runner",
        "organization_id":"single-origin-unattested","verification_session_id":str(JOBS[1]),
        "nonce":"historical-observation-"+str(JOBS[1]),"repository_full_name":REPO,
        "source_commit_sha":MAIN,"candidate_digest":req["candidate_digest"],"context_pack_digest":ctx,
        "check_family":"type_and_formal","verification_method_digest":digest({"method":"pinned Lean"}),
        "environment_digest":digest({"runner":"ubuntu-24.04","scope":SCOPE}),
        "toolchain_digest":digest({"lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6"}),
        "protocol_digest":digest({"source":HEAD,"run":RUN,"attestation":"NO_DATA"}),
        "check_ids":checks,"passed_check_ids":checks,"failed_check_ids":[],"skipped_check_ids":[],
        "finding_labels":[],"highest_severity":"none","declared_outcome":"passed",
        "falsification_executed":False,"falsification_passed":False,"acceptance_criteria_satisfied":True,
        "independent_from_candidate_producer":False,"independent_from_other_verifiers":False,
        "prompt_lineage_independent":False,"repair_memory_independent":False,
        "test_generation_independent":False,"isolated_execution_reported":True,
        "evidence_artifact_digest":ARTIFACTS[1][2],
        "verification_started_epoch":epoch(e["origin"]["jobs"][1]["started_at"]),
        "verification_completed_epoch":now,"kernel_executed_verification":False,
        "repository_mutation_performed":False,"candidate_selection_performed":True,
        "execution_authority_granted":False,"git_authority_granted":False,
        "correctness_proof_claimed":False,
    },ens.EVIDENCE_DIGEST_FIELD)
    result=ens.evaluate_independent_verifier_ensemble(req,policy,[packet])
    need(result.status==ens.STATUS_BLOCKED and result.ensemble is None and result.receipt is None
         and {"ensemble_required_family_missing","ensemble_insufficient_organization_count",
              "ensemble_insufficient_verifier_count"}.issubset(result.issues),"ensemble must hold")
    record={"request":req,"policy":policy,"declared_formal_observation":packet,
            "status":result.status,"issues":list(result.issues),"admitted_ensemble":None,
            "external_issuer_attestation":"NO_DATA","verified_useful":False}
    save(out,"ensemble-hold.json",record)
    return record,ctx,now

def memory_replay(out,e,hold,ctx,now):
    base={"repository_full_name":REPO,"source_commit_sha":MAIN,
          "source_tree_digest":digest({"git_tree_sha1":TREE}),
          "temporal_corpus_digest":digest({"run":RUN,"development_only":True}),
          "context_pack_digest":ctx,"verifier_ensemble_digest":digest(hold),
          "dependency_slice_digest":digest({"source_blob":e["source_blob"],"scope":SCOPE}),
          "toolchain_digest":hold["declared_formal_observation"]["toolchain_digest"],
          "environment_digest":hold["declared_formal_observation"]["environment_digest"],
          "memory_policy_digest":digest({"exact_binding":True,"four_family_required":True,
                                         "holdout_excluded":True,"authority":False})}
    cases=e["cases"]
    stage={
        "localize":(digest({"target":TARGET,"main":MAIN}),digest(e["gate"])),
        "diagnose":(cases[A]["source_sha256"],e["diagnostic_digest"]),
        "edit":(e["diagnostic_digest"],cases[B]["patch_sha256"]),
        "verify":(cases[B]["patch_sha256"],DIRECT),
    }
    def binding(kind):
        return {**base,"subtask_kind":kind,
                "subtask_contract_digest":digest({"kind":kind,"target":TARGET,"scope":SCOPE}),
                "predecessor_output_digest":stage[kind][0]}
    common={"schema_version":mem.SCHEMA_VERSION,"profile_version":mem.PROFILE_VERSION}
    entries=[]
    for kind in mem.SUBTASK_KINDS:
        entries.append(mem.seal({**common,**binding(kind),"entry_id":"portfolio-"+kind+"-observed",
            "entry_revision":"r1","outcome":mem.OUTCOME_INCONCLUSIVE,"evidence_created_epoch":now,
            "subtask_summary":"Observed exact "+kind+" stage; full utility ensemble NOT admitted",
            "input_artifact_digest":stage[kind][0],"output_artifact_digest":stage[kind][1],
            "verification_evidence_digest":digest(e),"derived_from_holdout":False,"superseded":False,
            "repository_mutation_performed":False,"candidate_selected":False,"repair_executed":False,
            "execution_authority_granted":False,"git_authority_granted":False,
            "correctness_claimed":False,"future_success_claimed":False},mem.ENTRY_DIGEST_FIELD))
    corpus=mem.seal({**common,"corpus_id":"portfolio-45719609942-development",
        "corpus_revision":"r1",**{k:base[k] for k in ("repository_full_name","temporal_corpus_digest",
            "context_pack_digest","verifier_ensemble_digest")},"entries":entries},mem.CORPUS_DIGEST_FIELD)
    def query(kind, corpus=corpus, overrides=None):
        bind=dict(binding(kind),**(overrides or {}))
        req=mem.seal({**common,**bind,"request_id":"portfolio-"+kind+"-recall",
            "request_revision":"r1","request_created_epoch":now,"unresolved_questions":[],
            "claims_selection_authority":False,"claims_repair_authority":False,
            "claims_execution_authority":False,"claims_git_authority":False},mem.REQUEST_DIGEST_FIELD)
        policy=mem.seal({**common,**{"expected_"+k:req[k] for k in mem.VERSION_BINDING_FIELDS},
            "evaluation_epoch":now,"maximum_request_age":3600,"maximum_entry_age":86400,
            "maximum_corpus_entries":16,"maximum_matched_entries":4,
            "allowed_outcomes":[mem.OUTCOME_VERIFIED_USEFUL],"required_subtask_kinds":list(mem.SUBTASK_KINDS),
            "require_exact_version_binding":True,"require_subtask_alignment":True,
            "require_dependency_alignment":True,"require_verifier_grounding":True,
            "require_holdout_protection":True,"require_not_superseded":True,"allow_memory_hint":True,
            "allow_repository_mutation":False,"allow_candidate_selection":False,"allow_repair_execution":False,
            "allow_execution_authority":False,"allow_git_authority":False},mem.POLICY_DIGEST_FIELD)
        result=mem.build_codeai_subtask_level_version_bound_memory(request=req,policy=policy,corpus=corpus)
        need(result.status==mem.STATUS_READY and result.memory_pack is not None and result.receipt is not None,
             repr(result.issues))
        need(result.memory_pack["matched_entry_count"]==0 and result.memory_pack["recommendation"]==mem.RECOMMENDATION_NONE,
             "unadmitted memory leaked")
        return {"request":req,"policy":policy,"pack":result.memory_pack,"receipt":result.receipt}
    queries={k:query(k) for k in mem.SUBTASK_KINDS}
    queries["stale"]=query("verify",overrides={"source_commit_sha":"0"*40})
    negative=deepcopy(corpus)
    negative["entries"][-1]=mem.seal(dict(negative["entries"][-1],derived_from_holdout=True,
        outcome=mem.OUTCOME_VERIFIED_USEFUL),mem.ENTRY_DIGEST_FIELD)
    negative=mem.seal(negative,mem.CORPUS_DIGEST_FIELD)
    queries["holdout_fixture"]=query("verify",corpus=negative)
    need(any("holdout_derived" in x["reasons"] for x in queries["holdout_fixture"]["pack"]["excluded_entries"]),
         "holdout exclusion not exercised")
    save(out,"corpus.json",corpus)
    save(out,"recall.json",queries)
    result={"schema":"kuuos.codeai.certified-cache-portfolio-memory.v1","source_head":MAIN,"source_tree":TREE,
            "historical_run":RUN,"historical_evaluation_epoch":now,"evidence_digest":digest(e),
            "diagnostic_digest":e["diagnostic_digest"],"ensemble_hold_digest":digest(hold),
            "ensemble_status":hold["status"],"corpus_digest":corpus[mem.CORPUS_DIGEST_FIELD],
            "observed_subtasks":list(mem.SUBTASK_KINDS),"entries":len(entries),
            "admitted_verified_useful":0,"recall_counts":{k:v["pack"]["matched_entry_count"] for k,v in queries.items()},
            "verified_formal_result_preserved":True,"failed_candidate_preserved":True,
            "learning_mode":"historical-observation-only","new_mathematical_result":False,
            "proof_authority":False,"future_success_claimed":False,"host_authority":False}
    save(out,"receipt.json",result)
    print("KUUOS_PORTFOLIO_MEMORY_REPLAY",json.dumps(result,sort_keys=True),flush=True)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args(); out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated artifacts required")
    out.mkdir(parents=True,exist_ok=True)
    obs=github_observation(MAIN,"canonical_main")
    need(obs["source_tree"]==TREE and digest(cache.remote_scope(cache.api,MAIN))==SCOPE,
         "current canonical binding changed")
    e=verify(out,provenance(out))
    hold,ctx,now=ensemble_hold(out,e)
    result=memory_replay(out,e,hold,ctx,now)
    if a.first:
        need(result==json.loads(a.first.read_text()),"independent memory replay differs")
        print("KUUOS_PORTFOLIO_MEMORY_INDEPENDENT_GREEN",digest(result),flush=True)

if __name__=="__main__":
    main()
