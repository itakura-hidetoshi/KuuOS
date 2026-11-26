#!/usr/bin/env python3
"""Actual archival evidence projection and native duplicate exclusion.

This is a development integration replay, not a new Lean certification.
Prior pilot sources are fetched at their immutable research HEAD. Canonical
proof bytes are observed separately from the candidate runtime under test.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import zipfile

ROOT = Path.cwd().resolve()
INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(INSTALL))
from runtime import kuuos_codeai_exact_diagnostic_memory_v1 as m
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from runtime import kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 as synth
from runtime import kuuos_codeai_autonomous_candidate_regeneration_v0_1 as regen
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import render_unified_diff
from scripts import ci_verified_lean_project_cache_v1 as cache
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation

def need(ok, reason):
    if not ok:
        raise ValueError(reason)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")

def read_archive(path,names):
    with zipfile.ZipFile(path) as z:
        inventory=z.namelist()
        need(len(inventory)==len(set(inventory)) and len(inventory)<80,"invalid archive inventory")
        values={}
        for name in names:
            i=z.getinfo(name)
            need(not i.is_dir() and 0<i.file_size<2_000_000,"invalid archive member")
            values[name]=z.read(i)
        return values

def observed_regeneration(packet,out):
    provenance=packet["provenance"]["regeneration"]
    rid=provenance["run_id"]
    run=cache.api(f"actions/runs/{rid}")
    need(run["head_sha"]==provenance["head"] and run["run_attempt"]==1
         and run["status"]=="completed" and run["conclusion"]=="success"
         and run["path"]==".github/workflows/codeai-certified-cache-diagnostic-regeneration-v1.yml",
         "regeneration run mismatch")
    jobs=cache.api(f"actions/runs/{rid}/jobs?per_page=100")
    need(jobs["total_count"]==2 and {j["id"] for j in jobs["jobs"]}==set(provenance["jobs"]),
         "regeneration job inventory mismatch")
    expected={provenance["jobs"][0]:["Recover exact diagnostic evidence and regenerate one distinct candidate",
            "Actual Lean MCP diagnostics and verification"],
            provenance["jobs"][1]:["Independently regenerate exact diagnostic consumer and compare Lean evidence"]}
    for j in jobs["jobs"]:
        need(j["status"]=="completed" and j["conclusion"]=="success","job not green")
        for name in expected[j["id"]]:
            need(any(s["name"]==name and s["status"]=="completed" and s["conclusion"]=="success"
                     for s in j["steps"]),"required step missing")
    data={}
    common=["feedback.json","direct.json","Probe.lean","candidate.diff","direct.log","regeneration.json"]
    for art in provenance["artifacts"]:
        aid,role=art["id"],art["role"]
        a=cache.api(f"actions/artifacts/{aid}")
        need(a["id"]==aid and a["name"]==f"codeai-diagnostic-regeneration-{role}-{rid}-1"
             and a["size_in_bytes"]==art["size"] and a["digest"]=="sha256:"+art["sha256"]
             and a["expired"] is False and a["workflow_run"]["id"]==rid
             and a["workflow_run"]["head_sha"]==provenance["head"]
             and a["workflow_run"]["repository_id"]==cache.REPO_ID
             and a["workflow_run"]["head_repository_id"]==cache.REPO_ID,"archive metadata mismatch")
        path=out/(role+".zip")
        cache.download_zip({"artifact_id":aid,"artifact_size":art["size"],"artifact_digest":art["sha256"]},path)
        data[role]=read_archive(path,common+(["mcp.json"] if role=="local" else ["independent.json"]))
    a,b=data["local"],data["independent"]
    for key in ("feedback.json","direct.json","Probe.lean","candidate.diff"):
        need(a[key]==b[key],"independent artifact content mismatch "+key)
    f,d,mp,i=map(json.loads,(a["feedback.json"],a["direct.json"],a["mcp.json"],b["independent.json"]))
    c=packet["regenerated"]
    need(m.digest(f)==c["feedback_digest"] and m.digest(d)==c["direct_digest"]
         and m.digest(mp)==c["mcp_digest"] and i["feedback_digest"]==c["feedback_digest"]
         and i["first_mcp_digest"]==c["mcp_digest"]
         and i["status"]=="INDEPENDENT_DIAGNOSTIC_REGENERATION_GREEN"
         and mp["status"]=="REAL_LEAN_MCP_REUSE_GREEN" and d["axioms"]==mp["axioms"]==[]
         and d["direct_exit"]==0 and sha(a["Probe.lean"])==c["source_sha256"]
         and sha(a["candidate.diff"])==c["patch_sha256"],"regeneration receipt binding mismatch")
    for key in ("stale_binding_rejections","tamper_rejected","native_duplicate_rejected",
                "historical_seed_lean_executions","new_candidate_lean_executions"):
        need(f[key]==c[key],"regeneration observation mismatch "+key)
    for role,rows in data.items():
        q=json.loads(rows["regeneration.json"])
        need(q["attempts"][0]["novelty_rejection_reason"]=="semantic_duplicate_patch_artifact"
             and q["attempts"][0]["accepted_novel_candidate"] is False
             and q["attempts"][1]["accepted_novel_candidate"] is True,"original duplicate rejection missing")
        log=rows["direct.log"].decode()
        need("does not depend on any axioms" in log and "sorryAx" not in log
             and "error:" not in log and "warning:" not in log,"historical fresh Lean audit mismatch")
    return a["Probe.lean"].decode("utf-8"),a["candidate.diff"]

def project(packet,prior):
    d,e,rec=prior["diagnostic"],prior["evidence"],prior["receipt"]
    mp=packet["provenance"]["memory"]
    need(m.digest(d)==mp["diagnostic_digest"] and m.digest(e)==mp["evidence_digest"]
         and m.digest(rec)==mp["receipt_digest"] and rec["admitted_verified_useful"]==0,
         "historical memory receipt mismatch")
    for k,v in (("target",packet["target"]),("source_blob",packet["source_blob"]),
                ("type_expr_sha256",packet["type_expr_sha256"]),("scope",packet["proof_scope_digest"]),
                ("source_head",packet["historical_source_head"]),("observed_difference",packet["observed_difference"])):
        need(d[k]==v,"projected diagnostic field mismatch "+k)
    need(e["canonical_tree"]==packet["historical_source_tree"] and e["portfolio_digest"]==packet["provenance"]["portfolio"]["portfolio_digest"],
         "historical scope/portfolio mismatch")
    for key in ("failed","successful_alternative"):
        for k in ("id","source_sha256","patch_sha256","log_sha256"):
            need(d[key][k]==packet[key][k],"candidate observation mismatch "+key+":"+k)
    log=d["actual_lean_log"]
    need(sha(log.encode())==packet["failed"]["log_sha256"]
         and all(packet["failed"][k] in log for k in ("diagnostic","term","actual_type","expected_type"))
         and "sorryAx" in log and d["failed"]["exit"]==packet["failed"]["exit"]
         and d["failed"]["direct_green"] is False and d["successful_alternative"]["direct_green"] is True,
         "actual compiler diagnostic mismatch")
    return d

def native_replay(packet,old,probe,head,out,observation,scope,gate,texts,patches,started):
    files={probe.SOURCE:(ROOT/probe.SOURCE).read_text(encoding="utf-8")}
    # The pinned previous pilot constructs a real read-only source receipt
    # for its historical canonical baseline; not a synthetic source receipt.
    source,observed=old.observation_receipt(head,gate,files,started,scope)
    now=int(time.time())
    session=observed["observation"]["session_id"]
    path=old.PATH
    req=patch.seal({"request_id":"immutable-diagnostic-seed-inventory","request_revision":"r1",
        "intent_text":"Rehydrate exact historical isolated patch inventory only; no Lean execution.",
        "candidate_count":3,"request_created_epoch":now,"requirement_trace_ids":["intent:exact-reuse"],
        "test_plan_ids":["historical-patch-duplicate-rejection"],"risk_labels":["isolated-test"],
        "unresolved_candidate_questions":[],"prior_candidate_digests":[],"prior_producer_session_ids":[]},synth.REQUEST_DIGEST_FIELD)
    sp=patch.seal({"allowed_provider_ids":["local_model"],"maximum_provider_calls":3,
        "maximum_raw_output_bytes":10000,"maximum_intent_bytes":100000,
        "maximum_repository_snapshot_bytes":1000000,"maximum_proposals":3,"evaluation_epoch":now,
        "maximum_response_age":60,"maximum_request_age":60,
        "allowed_repository_path_prefixes":["formal","artifacts/codeai-portfolio"],
        "forbidden_repository_path_prefixes":["formal/private"]},synth.POLICY_DIGEST_FIELD)
    cp=patch.seal({"expected_source_observation_receipt_digest":source[patch.SOURCE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name":cache.REPO,"expected_source_commit_sha":head,
        "allowed_patch_formats":["unified_diff"],"maximum_patch_bytes":10000,"maximum_changed_paths":1,
        "allowed_path_prefixes":["artifacts/codeai-portfolio"],"forbidden_path_prefixes":["formal","lean"],
        "allow_deletions":False,"allow_renames":False,"allow_binary_patches":False,
        "allow_submodule_patches":False,"allow_mode_changes":False,"require_requirement_trace":True,
        "require_test_plan":True,"allow_evidence_degradation":False,"known_risk_labels":["isolated-test"],
        "handover_risk_labels":[],"evaluation_epoch":now,"maximum_candidate_age":60},patch.POLICY_DIGEST_FIELD)
    def response(k,text):
        return {"provider_response_id":"response:"+k,"producer_session_id":"session:"+k+":"+session,
            "response_created_epoch":now,"raw_output":json.dumps({"proposal_id":k,"candidate_revision":"r1",
                "edits":[{"path":path,"operation":"add","new_content":text}],"risk_labels":["isolated-test"],
                "unresolved_candidate_questions":[]}),"claims_authority":False,"hides_uncertainty":False,
            "bypasses_governance":False,"evidence_missing":False}
    seeds=synth.build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=source,repository_files=files,synthesis_request=req,
        synthesis_policy=sp,candidate_policy=cp,
        provider_adapters=[synth.ProviderAdapter(k,"local_model","historical-seed",
                           lambda prompt,k=k:response(k,texts[k])) for k in sorted(texts)])
    need(seeds.status==synth.STATUS_READY and len(seeds.candidates)==3,repr(seeds.issues))
    need(all(s.patch_artifact.encode()==patches[s.proposal_id] for s in seeds.candidates),
         "seed rehydration changed historical patch bytes")
    rr=patch.seal({"request_id":"immutable-diagnostic-duplicate-test","request_revision":"r1",
        "intent_text":"Isolated software integration: reject historical duplicate patches.",
        "target_unique_candidate_count":4,"maximum_rounds_requested":1,"request_created_epoch":now,
        "feedback_reasons":["exact diagnostic observation replay"],"diversity_axes":["duplicate-negative"],
        "requirement_trace_ids":["intent:exact-reuse"],"test_plan_ids":["historical-patch-duplicate-rejection"],
        "risk_labels":["isolated-test"],"unresolved_candidate_questions":[],
        "prior_candidate_digests":[],"prior_producer_session_ids":[]},regen.REQUEST_DIGEST_FIELD)
    rp=patch.seal({"allowed_provider_ids":["local_model"],"allowed_diversity_axes":["duplicate-negative"],
        "maximum_rounds":1,"maximum_provider_calls_per_round":3,"maximum_total_provider_calls":3,
        "maximum_raw_output_bytes":10000,"maximum_intent_bytes":100000,"maximum_repository_snapshot_bytes":1000000,
        "maximum_feedback_items":12,"maximum_existing_candidates":3,"maximum_unique_candidates":4,
        "evaluation_epoch":now,"maximum_response_age":60,"maximum_request_age":60,
        "allowed_repository_path_prefixes":["formal","artifacts/codeai-portfolio"],
        "forbidden_repository_path_prefixes":["formal/private"]},regen.POLICY_DIGEST_FIELD)
    aid=packet["failed"]["id"]
    args=dict(root=ROOT,observation=observation,proof_scope=scope,target=packet["target"],
              failed_source=texts[aid].encode(),failed_patch=patches[aid],
              source_observation_receipt=source,repository_files=files,regeneration_request=rr)
    rejected=m.prepare_exact_diagnostic_regeneration(**args,seed_candidates=seeds.candidates[:-1])
    need(rejected["request"] is None and "historical_seed_inventory_incomplete" in rejected["issues"],
         "incomplete native seed inventory did not hold")
    prepared=m.prepare_exact_diagnostic_regeneration(**args,seed_candidates=seeds.candidates)
    need(prepared["request"] is not None and prepared["native_regeneration_required"]
         and prepared["verified_useful"] is False,"advisory preparation failed: "+repr(prepared["issues"]))
    calls=[]
    ctx_json=json.dumps(prepared["context"],sort_keys=True,ensure_ascii=False,separators=(",",":"))
    def callback(prompt,k):
        need(ctx_json in prompt["intent_text"]
             and any(packet["provenance"]["memory"]["diagnostic_digest"] in x for x in prompt["feedback_reasons"])
             and set(prompt["forbidden_patch_artifact_digests"])=={s.patch_candidate["patch_artifact_digest"] for s in seeds.candidates},
             "actual native provider context mismatch")
        calls.append(k)
        return response("repeat-"+k,texts[k])
    result=regen.build_codeai_autonomous_candidate_regeneration(
        source_generation_receipt=seeds.receipt,source_observation_receipt=source,
        repository_files=files,seed_candidates=seeds.candidates,regeneration_request=prepared["request"],
        regeneration_policy=rp,candidate_policy=cp,
        provider_adapters=[regen.ProviderAdapter(k,"local_model","duplicate-negative-fixture",
                           lambda prompt,k=k:callback(prompt,k)) for k in sorted(texts)])
    need(result.status==regen.STATUS_BLOCKED and len(result.regenerated_candidates)==0
         and len(result.attempts)==3 and calls==sorted(texts)
         and all(a.novelty_rejection_reason=="semantic_duplicate_patch_artifact" and not a.accepted_novel_candidate
                 for a in result.attempts),"historical candidate escaped native duplicate filter")
    save(out/"native-regeneration.json",{"prepared":prepared,"attempts":[asdict(a) for a in result.attempts],
                                         "receipt":result.receipt})
    return prepared["context_digest"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pilot",type=Path,required=True)
    p.add_argument("--head",required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args()
    sys.path.insert(0,str(a.pilot.resolve()))
    import codeai_certified_cache_diagnostic_regeneration_v1 as pilot
    import codeai_certified_cache_candidate_portfolio_v1 as old
    import codeai_canonical_cache_reuse_probe_v1 as probe
    out=a.out.resolve();need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    started=int(time.time())
    packet=m.load_packet()
    prior_dir=out/"history";prior_dir.mkdir()
    prior=pilot.history(prior_dir)
    project(packet,prior)
    c_text,c_patch=observed_regeneration(packet,out)
    texts={**old.TEXTS,packet["regenerated"]["id"]:c_text}
    files={probe.SOURCE:(ROOT/probe.SOURCE).read_text(encoding="utf-8")}
    patches={}
    for key in ("failed","successful_alternative","regenerated"):
        row=packet[key];k=row["id"]
        diff,_,issues=render_unified_diff(files,[{"path":old.PATH,"operation":"add","new_content":texts[k]}])
        need(not issues and sha(texts[k].encode())==row["source_sha256"]
             and sha(diff.encode())==row["patch_sha256"],"historical bytes differ")
        patches[k]=diff.encode()
    need(patches[packet["regenerated"]["id"]]==c_patch,"regenerated patch differs")
    observation=github_observation(a.head,"canonical_main")
    scope=cache.remote_scope(cache.api,a.head)
    need(cache.local_scope(ROOT,a.head)==scope,"local canonical proof scope mismatch")
    aid=packet["failed"]["id"]
    args=dict(root=ROOT,observation=observation,proof_scope=scope,target=packet["target"],
              failed_source=texts[aid].encode(),failed_patch=patches[aid])
    found=m.recall_exact_diagnostic(**args)
    need(found["context"] is not None and found["verified_useful"] is False,"actual recall failed: "+repr(found))
    for bad in (dict(args,target="unknown"),dict(args,failed_source=b"changed"),
                dict(args,failed_patch=b"changed"),dict(args,observation=dict(observation,scope="research_head")),
                dict(args,proof_scope=dict(scope,runner="changed"))):
        need(m.recall_exact_diagnostic(**bad)["context"] is None,"mismatch leaked diagnostic")
    # The historical baseline receipt used in this integration test is
    # fixed to the observed historical main. If main changes, recall remains
    # independently checked, but native replay needs a new receipt.
    need(a.head==packet["historical_source_head"],"native replay baseline requires re-observation")
    gate=probe.actual_gate(a.head,out)
    ctx=native_replay(packet,old,probe,a.head,out,observation,scope,gate,texts,patches,started)
    need(ctx==found["context_digest"],"prepared context differs from recalled context")
    stable={"packet_blob":m.PACKET_BLOB,"historical_source_head":packet["historical_source_head"],
            "current_source_head":a.head,"current_source_tree":observation["source_tree"],
            "proof_scope_digest":packet["proof_scope_digest"],"context_digest":ctx,
            "historical_patch_digests":sorted(m.observed_patch_sha256s(packet)),
            "actual_archive_projection":True,"mismatch_rejections":5,"incomplete_seed_rejected":True,
            "native_duplicate_rejections":3,"new_lean_executions":0,"verified_useful":False,
            "global_verifier_ensemble":"HOLD","external_model":False,"proof_authority":False}
    save(out/"integration-receipt.json",stable)
    if a.first:
        need(json.loads(a.first.read_text())==stable,"independent integration receipt differs")
        print("KUUOS_EXACT_DIAGNOSTIC_MEMORY_INDEPENDENT",m.digest(stable),flush=True)
    print("KUUOS_EXACT_DIAGNOSTIC_MEMORY_GREEN",json.dumps(stable,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
