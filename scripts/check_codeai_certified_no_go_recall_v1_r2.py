#!/usr/bin/env python3
"""R2: reuse the existing typed MCP response decoder for archived evidence.

Actual prior CI artifacts are downloaded and SHA256 verified, never recompiled.
Unknown, stale, missing or changed targets HOLD. No new proof or provider call.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path.cwd().resolve()
INSTALL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(INSTALL))
from runtime import kuuos_codeai_certified_no_go_recall_v1 as m
from runtime import kuuos_codeai_no_go_memory_v1 as n
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from scripts import ci_verified_lean_project_cache_v1 as cache
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured

def need(ok,why):
    if not ok:
        raise ValueError(why)

def save(path,value):
    path.write_text(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def archive(path,names):
    with zipfile.ZipFile(path) as z:
        inventory=z.namelist()
        need(len(inventory)==len(set(inventory)) and len(inventory)<100,"unsafe evidence archive inventory")
        result={}
        for name in names:
            i=z.getinfo(name)
            need(0<i.file_size<10_000_000 and not i.is_dir(),"invalid archive member")
            result[name]=json.loads(z.read(i))
        return result

def historical_bundle(p,out):
    rid=p["run_id"]
    run=cache.api(f"actions/runs/{rid}")
    need(run["head_sha"]==p["head"] and run["run_attempt"]==p["run_attempt"]
         and run["status"]=="completed" and run["conclusion"]=="success"
         and run["path"]==".github/workflows/codeai-no-go-memory-v1-r2.yml","historical run mismatch")
    jobs=cache.api(f"actions/runs/{rid}/jobs?per_page=100")
    checks={p["sandbox_job"]:["Verify and reuse exact archived direct evidence",
              "Actual Lean MCP name-only axiom audit with raw response preservation"],
            p["independent_job"]:["Independently repeat typed applications and compare exact no-go routes"]}
    need(jobs["total_count"]==2 and {j["id"] for j in jobs["jobs"]}==set(checks),"job inventory mismatch")
    for j in jobs["jobs"]:
        need(j["status"]=="completed" and j["conclusion"]=="success","historical job not green")
        for name in checks[j["id"]]:
            need(any(s["name"]==name and s["status"]=="completed" and s["conclusion"]=="success"
                     for s in j["steps"]),"historical verification step missing")
    data={}
    for art in p["artifacts"]:
        a=cache.api(f"actions/artifacts/{art['id']}")
        role=art["role"]
        need(a["id"]==art["id"] and a["name"]==f"codeai-no-go-r2-{role}-{rid}-1"
             and a["size_in_bytes"]==art["size"] and a["digest"]=="sha256:"+art["sha256"]
             and a["expired"] is False and a["workflow_run"]["id"]==rid
             and a["workflow_run"]["head_sha"]==p["head"]
             and a["workflow_run"]["repository_id"]==cache.REPO_ID
             and a["workflow_run"]["head_repository_id"]==cache.REPO_ID,"artifact origin mismatch")
        z=out/(role+".zip")
        cache.download_zip({"artifact_id":art["id"],"artifact_size":art["size"],"artifact_digest":art["sha256"]},z)
        common=["direct.json","recall.json"]
        if role=="local":
            names=common+["mcp.json","mcp-diagnostics.json"]+[
                f"mcp-verify-{i}.json" for i in range(p["observed_declarations"])]
        else:
            names=common+["routes.json","independent.json"]
        data[role]=archive(z,names)
    a,b=data["local"],data["independent"]
    need(a["direct.json"]==b["direct.json"] and a["recall.json"]==b["recall.json"],
         "independent direct/recall mismatch")
    d,mp,rec=a["direct.json"],a["mcp.json"],b["independent.json"]
    need(rec["status"]=="INDEPENDENT_NO_GO_GREEN" and rec["direct_digest"]==p["direct_digest"]
         and rec["mcp_digest"]==p["mcp_digest"] and rec["route_digest"]==p["route_digest"]
         and rec["routes"]==p["routes"] and rec["independent_direct_recomputed"] is True
         and rec["provider_calls"]==0,"independent route receipt mismatch")
    need(mp["raw_responses_preserved"] is True and mp["status"]=="REAL_LEAN_MCP_NO_GO_GREEN",
         "actual MCP receipt absent")
    raw_diag=a["mcp-diagnostics.json"]
    diag=structured(raw_diag)
    need(raw_diag["result"].get("isError") is False,"MCP diagnostic transport error")
    need(isinstance(diag.get("items"),list),"MCP diagnostic items missing")
    print("KUUOS_ARCHIVED_NOGO_DIAGNOSTIC",json.dumps({k:diag.get(k) for k in ("success","partial","timed_out","failed_dependencies")},sort_keys=True),flush=True)
    need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
         and diag["failed_dependencies"]==[] and not any(x.get("severity") in ("error","warning") for x in diag["items"]),
         "historical diagnostics incomplete")
    by_name={x["name"]:x for x in mp["observations"]}
    need(len(by_name)==len(mp["observations"])==len(d["observations"])==p["observed_declarations"],
         "MCP audit inventory mismatch")
    for i,row in enumerate(d["observations"]):
        response=a[f"mcp-verify-{i}.json"]
        raw=response["result"]
        value=structured(response)
        observed=by_name[row["name"]]
        need(raw["isError"] is False and value["warnings"]==[]
             and set(value["axioms"])<=n.STANDARD
             and sorted(value["axioms"])==row["axioms"]==observed["axioms"]
             and value["axioms"]==observed["raw_axioms"],"MCP raw axiom audit mismatch")
    bundle={"direct":d,"recall":a["recall.json"],"mcp":mp,
            "independent_direct":b["direct.json"],"routes":b["routes.json"]}
    m.validate_historical_bundle(bundle)
    return bundle

def run(head,out):
    p=m.load_lineage()
    bundle=historical_bundle(p,out)
    obs=github_observation(head,"canonical_main")
    scope=cache.remote_scope(cache.api,head)
    need(cache.local_scope(ROOT,head)==scope,"canonical scope mismatch")
    args=dict(root=ROOT,observation=obs,proof_scope=scope,bundle=bundle,subject=p["subject"])
    found=m.recall_certified_no_go(**args)
    need(found["status"]=="SELECTED_NO_GO_CONTEXT_MATCHED",repr(found.get("issues")))
    ctx=found["context"]
    files={path:(ROOT/path).read_text(encoding="utf-8") for path in n.BLOBS}
    calls=[]
    def forbidden_provider(*args,**kwargs):
        calls.append("unexpected provider call")
        raise ValueError("provider not permitted for this exact route")
    results={}
    for key in sorted(p["routes"]):
        request=m.make_target_request(ctx,key)
        result=m.build_selected_no_go_research_synthesis(**args,target_request=request,
            repository_files=files,provider_adapters=[forbidden_provider])
        need(result["status"]==p["routes"][key] and result["synthesis"] is None
             and result["candidate_generation_allowed"] is False
             and result["proof_authority"] is False,"pre-provider verdict mismatch")
        results[key]=result
    raw=m.make_target_request(ctx,"original_raw")
    def check_hold(name,changes,request=raw,files_arg=files):
        result=m.build_selected_no_go_research_synthesis(**dict(args,**changes),
            target_request=request,repository_files=files_arg,provider_adapters=[forbidden_provider])
        need(result["status"]=="HOLD_NO_GO_REVIEW" and result["synthesis"] is None
             and not result["candidate_generation_allowed"],"unsafe admission: "+name)
        return name
    rejects=[
        check_hold("different_target_proposition",{},dict(raw,proposition=n.CASES["alternative_raw"][0])),
        check_hold("changed_target_expr",{},dict(raw,target_expr_digest="0"*64)),
        check_hold("changed_request_digest",{},dict(raw,request_digest="0"*64)),
        check_hold("conditional_without_premise",{},dict(raw,target_id="conditional_without_hbad")),
        check_hold("unreviewed_subject",{"subject":"unknown"}),
        check_hold("noncanonical_scope",{"observation":dict(obs,scope="research_head")}),
        check_hold("changed_scope",{"proof_scope":dict(scope,runner="changed")}),
        check_hold("missing_original_source_context",{},raw,{n.SOURCE:files[n.SOURCE]}),
        check_hold("tampered_negative_route",{"bundle":dict(bundle,routes=dict(bundle["routes"],status="invented"))}),
        check_hold("tampered_mcp",{"bundle":dict(bundle,mcp=dict(bundle["mcp"],status="invented"))}),
        check_hold("missing_independent_direct",{"bundle":dict(bundle,independent_direct={})}),
    ]
    need(not calls,"provider executed")
    receipt={"schema":"kuuos.codeai.selected-certified-no-go-recall-replay.v1",
             "historical_run":p["run_id"],"historical_head":p["historical_source_head"],
             "current_head":head,"current_tree":obs["source_tree"],"lineage_blob":m.LINEAGE_BLOB,
             "route_digest":p["route_digest"],"context_digest":found["context_digest"],
             "routes":{k:v["status"] for k,v in results.items()},
             "negative_positive_reused":len(results),"hold_regressions":rejects,
             "prior_actual_mcp_audits":p["observed_declarations"],
             "prior_actual_artifact_projection":True,"new_lean_executions":0,
             "provider_calls":len(calls),"semantic_search_complete":False,
             "proof_authority":False,"candidate_generation_allowed":False}
    save(out/"recall-context.json",ctx)
    save(out/"routes.json",results)
    save(out/"receipt.json",receipt)
    print("KUUOS_CERTIFIED_NOGO_PREPROVIDER_GREEN",json.dumps(receipt,ensure_ascii=False,sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser();p.add_argument("--head",required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    receipt=run(a.head,out)
    if a.first:
        need(json.loads(a.first.read_text())==receipt,"independent route recall receipt differs")
        print("KUUOS_CERTIFIED_NOGO_PREPROVIDER_INDEPENDENT",digest(receipt),flush=True)

if __name__=="__main__":
    main()
