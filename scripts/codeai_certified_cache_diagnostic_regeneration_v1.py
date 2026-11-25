#!/usr/bin/env python3
"""Exact historical diagnostic context -> original CodeAI regeneration.

The previous two candidates are reconstituted as a seed inventory, not
retried in Lean. A deliberate duplicate provider response tests the native
patch-artifact exclusion. Only an actually different, typed test consumer
is compiled. This is a deterministic local provider experiment, not new
mathematics, a generalized repair-memory hint or an external model call.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import zipfile

import codeai_canonical_cache_reuse_probe_v1 as probe
import codeai_certified_cache_candidate_portfolio_v1 as old
from scripts import ci_verified_lean_project_cache_v1 as cache
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from runtime import kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 as synth
from runtime import kuuos_codeai_autonomous_candidate_regeneration_v0_1 as regen
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import render_unified_diff
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, git_blob

ROOT=probe.ROOT
MAIN="e1d754e8e0fc9382001a2e698751aa11d4272b84"
TREE="bdf2e81fc2cf702481b80e7079e59b1b47836013"
SCOPE=old.EXPECTED_SCOPE
MEM_RUN=45722237558
MEM_HEAD="014b1531846c3b4979901e9c5af3d10ac58c40aa"
MEM_RECEIPT="4a43405db609338b03c0c84307d76e34a664286b2e27217cccc7f087aae53226"
DIAG="6c97fadde43e119b7fb892c1ccc07e04a3b51c9f055f32724b1f1dc5d9ba966d"
EVIDENCE="c648a54c78d9e9d936b60563bf672b05146efdde61b742667e26d11f12d98c63"
ARTIFACTS=(
    (15073345157,11366,"a7dfd65c758ec14b759232c1bbc07091cefbf5b2515b158c719cd4ca15902e02","local"),
    (15072327855,11366,"d71c8fccb310d91ef6429847186056ed1705ae7982b9d5ecfd0e65a12e849938","independent"),
)
A="a-missing-hypothesis"
B="b-exact-reuse"
C="c-diagnostic-explicit-exact"
PATH=old.PATH

def need(ok, reason):
    if not ok:
        raise ValueError(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(out,name,value):
    probe.save(out/name,value)

def history(out):
    run=cache.api(f"actions/runs/{MEM_RUN}")
    need(run["head_sha"]==MEM_HEAD and run["run_attempt"]==1
         and run["status"]=="completed" and run["conclusion"]=="success"
         and run["path"]==".github/workflows/codeai-certified-cache-portfolio-memory-v1.yml",
         "memory workflow identity/status mismatch")
    jobs=cache.api(f"actions/runs/{MEM_RUN}/jobs?per_page=100")
    names={139583144014:"Reobserve actual completed jobs, digest-verify archived evidence, enforce ensemble HOLD",
           139583262360:"Fetch historical evidence afresh and compare independent memory receipt"}
    need(jobs["total_count"]==2 and {x["id"] for x in jobs["jobs"]}==set(names),"memory jobs mismatch")
    for j in jobs["jobs"]:
        need(j["status"]=="completed" and j["conclusion"]=="success"
             and any(s["name"]==names[j["id"]] and s["status"]=="completed"
                     and s["conclusion"]=="success" for s in j["steps"]),
             "memory replay step not green")
    first=None
    for aid,size,checksum,role in ARTIFACTS:
        a=cache.api(f"actions/artifacts/{aid}")
        need(a["id"]==aid and a["name"]==f"codeai-portfolio-memory-{role}-{MEM_RUN}-1"
             and a["size_in_bytes"]==size and a["digest"]=="sha256:"+checksum
             and a["expired"] is False and a["workflow_run"]["id"]==MEM_RUN
             and a["workflow_run"]["head_sha"]==MEM_HEAD
             and a["workflow_run"]["repository_id"]==cache.REPO_ID
             and a["workflow_run"]["head_repository_id"]==cache.REPO_ID,
             "memory artifact metadata mismatch")
        p=out/(role+".zip")
        cache.download_zip({"artifact_id":aid,"artifact_size":size,"artifact_digest":checksum},p)
        with zipfile.ZipFile(p) as z:
            names=z.namelist()
            need(len(names)==len(set(names)),"duplicate archive members")
            def obj(name):
                i=z.getinfo(name+".json")
                need(0<i.file_size<2_000_000 and not i.is_dir(),"invalid evidence member")
                return json.loads(z.read(i))
            rows={k:obj(k) for k in ("receipt","diagnostic","evidence","ensemble-hold")}
        if first is None:
            first=rows
        else:
            need(first==rows,"independent memory bytes differ semantically")
    rec,d,e,h=(first[k] for k in ("receipt","diagnostic","evidence","ensemble-hold"))
    need(digest(rec)==MEM_RECEIPT and digest(d)==DIAG and digest(e)==EVIDENCE
         and rec["diagnostic_digest"]==DIAG and rec["evidence_digest"]==EVIDENCE
         and rec["ensemble_hold_digest"]==digest(h) and h["status"]=="blocked"
         and rec["admitted_verified_useful"]==0 and rec["verified_formal_result_preserved"] is True
         and d["general_repair_usefulness"]=="NO_DATA" and d["candidate_A_admitted"] is False,
         "historical evidence or authority boundary mismatch")
    need(e["gate"]["target"]==probe.NAME and e["canonical_head"]==MAIN
         and e["canonical_tree"]==TREE and e["scope_digest"]==SCOPE,
         "historical scope mismatch")
    return first

def binding(gate,scope):
    return {"head":gate["canonical_head"],"tree":gate["canonical_tree"],"scope":digest(scope),
            "target":gate["target"],"type_expr_sha256":gate["type_expr_sha256"],
            "source_blob":git_blob((ROOT/probe.SOURCE).read_bytes()),
            "failed_source_sha256":sha(old.TEXTS[A].encode())}

def lookup(history,query):
    d,e=history["diagnostic"],history["evidence"]
    if digest(d)!=DIAG or digest(e)!=EVIDENCE or digest(history["receipt"])!=MEM_RECEIPT:
        return {"status":"HOLD_TAMPERED_HISTORY","context":None}
    expected={"head":d["source_head"],"tree":e["canonical_tree"],"scope":d["scope"],
              "target":d["target"],"type_expr_sha256":d["type_expr_sha256"],
              "source_blob":d["source_blob"],"failed_source_sha256":d["failed"]["source_sha256"]}
    if query!=expected:
        return {"status":"HOLD_REOBSERVE_SCOPE","context":None}
    text=d["actual_lean_log"]
    need("error: Type mismatch" in text and
         "HasGlobal U s → OverlapFiberFaithful U q s" in text and "sorryAx" in text,
         "diagnostic missing")
    context={"schema":"kuuos.codeai.exact-diagnostic-advisory.v1","binding":expected,
             "historical_memory_receipt_digest":MEM_RECEIPT,"diagnostic_digest":DIAG,
             "historical_evidence_digest":EVIDENCE,"failed_log":text,
             "failed_patch_sha256":d["failed"]["patch_sha256"],
             "successful_alternative_sha256":d["successful_alternative"]["source_sha256"],
             "observed_difference":d["observed_difference"],
             "scope":"EXACT_HISTORICAL_OBSERVATION_ONLY","verified_useful":False,
             "general_repair_usefulness":"NO_DATA","verifier_ensemble":"HOLD",
             "proof_authority":False,"future_success_claimed":False}
    return {"status":"EXACT_DIAGNOSTIC_OBSERVED_TEST_REQUIRED","context":context}

def generate(head,out,gate,scope,history,started):
    q=binding(gate,scope)
    selected=lookup(history,q)
    need(selected["status"]=="EXACT_DIAGNOSTIC_OBSERVED_TEST_REQUIRED","diagnostic not admitted as observation")
    ctx=selected["context"]
    for k in q:
        drift=dict(q); drift[k]="changed"
        need(lookup(history,drift)["context"] is None,"stale diagnostic leaked: "+k)
    tamper=dict(history,diagnostic=dict(history["diagnostic"],observed_difference="invented"))
    need(lookup(tamper,q)["status"]=="HOLD_TAMPERED_HISTORY","tampered diagnostic leaked")
    save(out,"diagnostic-context.json",selected)
    files={probe.SOURCE:(ROOT/probe.SOURCE).read_text(encoding="utf-8")}
    source,observed=old.observation_receipt(head,gate,files,started,scope)
    now=int(time.time())
    session=observed["observation"]["session_id"]
    # Exact historical candidate bodies are present in the prior experiment;
    # the new seed inventory uses fresh envelope epochs, not a backdated
    # generation receipt. Verify byte hashes against independent history.
    texts=dict(old.TEXTS)
    for key in (A,B):
        need(sha(texts[key].encode())==history["evidence"]["cases"][key]["source_sha256"],
             "seed source digest mismatch")
    req=patch.seal({"request_id":"diagnostic-seed-rehydration","request_revision":"r1",
        "intent_text":"Reconstitute historical isolated test seeds only; do not execute them.",
        "candidate_count":2,"request_created_epoch":now,"requirement_trace_ids":["intent:exact-reuse"],
        "test_plan_ids":["direct-lean","real-mcp","independent-lean"],"risk_labels":["isolated-test"],
        "unresolved_candidate_questions":[],"prior_candidate_digests":[],"prior_producer_session_ids":[]},
        synth.REQUEST_DIGEST_FIELD)
    synpol=patch.seal({"allowed_provider_ids":["local_model"],"maximum_provider_calls":2,
        "maximum_raw_output_bytes":10000,"maximum_intent_bytes":100000,
        "maximum_repository_snapshot_bytes":1000000,"maximum_proposals":2,"evaluation_epoch":now,
        "maximum_response_age":60,"maximum_request_age":60,
        "allowed_repository_path_prefixes":["formal","artifacts/codeai-portfolio"],
        "forbidden_repository_path_prefixes":["formal/private"]},synth.POLICY_DIGEST_FIELD)
    cpol=patch.seal({"expected_source_observation_receipt_digest":source[patch.SOURCE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name":cache.REPO,"expected_source_commit_sha":head,
        "allowed_patch_formats":["unified_diff"],"maximum_patch_bytes":10000,"maximum_changed_paths":1,
        "allowed_path_prefixes":["artifacts/codeai-portfolio"],"forbidden_path_prefixes":["formal","lean"],
        "allow_deletions":False,"allow_renames":False,"allow_binary_patches":False,
        "allow_submodule_patches":False,"allow_mode_changes":False,"require_requirement_trace":True,
        "require_test_plan":True,"allow_evidence_degradation":False,"known_risk_labels":["isolated-test"],
        "handover_risk_labels":[],"evaluation_epoch":now,"maximum_candidate_age":60},patch.POLICY_DIGEST_FIELD)
    def response(key,text):
        return {"provider_response_id":"response:"+key,"producer_session_id":"session:"+key+":"+session,
            "response_created_epoch":now,"raw_output":json.dumps({"proposal_id":key,"candidate_revision":"r1",
                "edits":[{"path":PATH,"operation":"add","new_content":text}],"risk_labels":["isolated-test"],
                "unresolved_candidate_questions":[]}),"claims_authority":False,"hides_uncertainty":False,
            "bypasses_governance":False,"evidence_missing":False}
    seed_result=synth.build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=source,repository_files=files,synthesis_request=req,
        synthesis_policy=synpol,candidate_policy=cpol,
        provider_adapters=[synth.ProviderAdapter(k,"local_model","historical-seed-rehydration",
                           lambda prompt,k=k:response(k,texts[k])) for k in sorted(texts)])
    need(seed_result.status==synth.STATUS_READY and len(seed_result.candidates)==2,
         "seed reconstitution failed: "+repr(seed_result.issues))
    seeds=seed_result.candidates
    for s in seeds:
        need(sha(s.patch_artifact.encode())==history["evidence"]["cases"][s.proposal_id]["patch_sha256"],
             "seed patch differs from archived independent evidence")
    # A new request uses actual archived diagnostics, not a fake typed-error
    # classification or an admitted four-family verifier certificate.
    context_json=json.dumps(ctx,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    intent="Construct an isolated typed consumer of the exact existing theorem; preserve all premises.\n"+context_json
    request=patch.seal({"request_id":"actual-diagnostic-regeneration","request_revision":"r1",
        "intent_text":intent,"target_unique_candidate_count":3,"maximum_rounds_requested":1,
        "request_created_epoch":now,"feedback_reasons":["actual Lean diagnostic: missing HasGlobal U s argument",
        "exact diagnostic receipt "+DIAG,"verified_useful unavailable; direct revalidation required"],
        "diversity_axes":["explicit-premise-application"],"requirement_trace_ids":["intent:exact-reuse"],
        "test_plan_ids":["direct-lean","real-mcp","independent-lean"],"risk_labels":["isolated-test"],
        "unresolved_candidate_questions":[],"prior_candidate_digests":[],"prior_producer_session_ids":[]},
        regen.REQUEST_DIGEST_FIELD)
    policy=patch.seal({"allowed_provider_ids":["local_model"],"allowed_diversity_axes":["explicit-premise-application"],
        "maximum_rounds":1,"maximum_provider_calls_per_round":2,"maximum_total_provider_calls":2,
        "maximum_raw_output_bytes":10000,"maximum_intent_bytes":100000,"maximum_repository_snapshot_bytes":1000000,
        "maximum_feedback_items":8,"maximum_existing_candidates":2,"maximum_unique_candidates":3,
        "evaluation_epoch":now,"maximum_response_age":60,"maximum_request_age":60,
        "allowed_repository_path_prefixes":["formal","artifacts/codeai-portfolio"],
        "forbidden_repository_path_prefixes":["formal/private"]},regen.POLICY_DIGEST_FIELD)
    # Deliberate repeated response is a negative test. It must never be
    # forwarded to Lean. The second callback constructs a different proof
    # body from the failed source and observed missing premise.
    prior_artifacts={x.patch_candidate["patch_artifact_digest"] for x in seeds}
    calls=[]
    old_line="  sourceGlobal_implies_overlapFaithful U q s\n"
    need(texts[A].count(old_line)==1,"failed source shape changed")
    fixed=texts[A].replace("OverlapFiberFaithful U q s :=\n"+old_line,
                           "OverlapFiberFaithful U q s := by\n  exact sourceGlobal_implies_overlapFaithful U q s h\n")
    need(fixed!=texts[A] and fixed!=texts[B],"new candidate must be a distinct patch")
    def callback(prompt,key,text):
        need(context_json in prompt["intent_text"] and prompt["repository_files"]==files
             and set(prompt["forbidden_patch_artifact_digests"])==prior_artifacts
             and any(DIAG in v for v in prompt["feedback_reasons"]),
             "exact diagnostic or prior-patch context missing")
        calls.append(key)
        return response(key,text)
    result=regen.build_codeai_autonomous_candidate_regeneration(
        source_generation_receipt=seed_result.receipt,source_observation_receipt=source,
        repository_files=files,seed_candidates=seeds,regeneration_request=request,
        regeneration_policy=policy,candidate_policy=cpol,
        provider_adapters=[
            regen.ProviderAdapter("a-repeat-negative","local_model","deliberate-negative-fixture",
                lambda prompt:callback(prompt,"repeat-A-new-id",texts[A])),
            regen.ProviderAdapter("b-exact-diagnostic","local_model","bounded-deterministic-diagnostic-repair",
                lambda prompt:callback(prompt,C,fixed))])
    save(out,"regeneration.json",{"status":result.status,"issues":result.issues,
        "attempts":[asdict(x) for x in result.attempts],"receipt":result.receipt})
    need(result.status==regen.STATUS_READY and len(result.regenerated_candidates)==1
         and len(result.attempts)==2 and calls==["repeat-A-new-id",C],
         "native regeneration failed: "+repr(result.issues))
    need(result.attempts[0].novelty_rejection_reason=="semantic_duplicate_patch_artifact"
         and not result.attempts[0].accepted_novel_candidate
         and result.attempts[1].accepted_novel_candidate,"native exact duplicate filter failed")
    candidate=result.regenerated_candidates[0]
    expected,shape,issues=render_unified_diff(files,[{"path":PATH,"operation":"add","new_content":fixed}])
    need(not issues and candidate.proposal_id==C and expected==candidate.patch_artifact
         and candidate.patch_candidate["added_paths"]==[PATH],"candidate patch mismatch")
    save(out,"candidate.json",candidate.patch_candidate)
    save(out,"candidate-receipt.json",candidate.candidate_receipt)
    (out/"candidate.diff").write_text(candidate.patch_artifact,encoding="utf-8")
    probe_path=out/"Probe.lean"
    probe_path.write_text(fixed,encoding="utf-8")
    need(sha(probe_path.read_bytes()) not in {sha(v.encode()) for v in texts.values()},
         "historical candidate re-presented to Lean")
    p=subprocess.run(["lake","env","lean",*probe.canonical_direct_options((ROOT/"lakefile.toml").read_bytes()),
                      str(probe_path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True,timeout=300)
    log=p.stdout+"\n"+p.stderr
    (out/"direct.log").write_text(log,encoding="utf-8")
    print(log,flush=True)
    need(p.returncode==0 and "does not depend on any axioms" in log and "sorryAx" not in log
         and not re.search(r"\b(?:warning|error):",log),"fresh candidate direct Lean failed")
    direct={"gate":gate,"probe_sha256":sha(probe_path.read_bytes()),"direct_exit":0,
            "axioms":[],"proof_authority":False,"novelty_certified":False}
    save(out,"direct.json",direct)
    stable={"canonical_head":head,"canonical_tree":gate["canonical_tree"],"scope":digest(scope),
        "diagnostic_context_digest":digest(ctx),"historical_memory_receipt":MEM_RECEIPT,
        "stale_binding_rejections":len(q),"tamper_rejected":True,"native_duplicate_rejected":True,
        "historical_seed_lean_executions":0,"new_candidate_lean_executions":1,
        "candidate":C,"candidate_source_sha256":direct["probe_sha256"],
        "candidate_patch_sha256":sha(candidate.patch_artifact.encode()),
        "direct_digest":digest(direct),"verified_useful":False,"external_model":False,
        "proof_authority":False,"new_mathematical_result":False}
    save(out,"feedback.json",stable)
    need(probe.actual_observation(head)["source_tree"]==TREE,"canonical main changed")
    print("KUUOS_DIAGNOSTIC_REGENERATION_DIRECT_GREEN",json.dumps(stable,sort_keys=True),flush=True)
    return stable

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True)
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args(); out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="mcp":
        probe.mcp(a.head,out)
        return
    started=int(time.time())
    scope=cache.local_scope(ROOT,a.head)
    need(a.head==MAIN and digest(scope)==SCOPE,"unsupported source scope")
    h=history(out)
    gate=probe.actual_gate(a.head,out)
    current=generate(a.head,out,gate,scope,h,started)
    if a.phase=="independent":
        need(a.first is not None,"first receipt required")
        first=json.loads((a.first/"feedback.json").read_text())
        d=json.loads((a.first/"direct.json").read_text())
        m=json.loads((a.first/"mcp.json").read_text())
        need(first==current and m["status"]=="REAL_LEAN_MCP_REUSE_GREEN"
             and m["direct_digest"]==digest(d) and d==json.loads((out/"direct.json").read_text()),
             "independent regeneration evidence differs")
        receipt={"status":"INDEPENDENT_DIAGNOSTIC_REGENERATION_GREEN","feedback_digest":digest(current),
                 "first_mcp_digest":digest(m),"verified_useful":False,"proof_authority":False}
        save(out,"independent.json",receipt)
        print("KUUOS_DIAGNOSTIC_REGENERATION_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
