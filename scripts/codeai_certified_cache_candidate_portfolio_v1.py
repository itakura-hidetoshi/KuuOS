#!/usr/bin/env python3
"""Exercise the original CodeAI candidate envelope on an actual canonical
REUSE_EXISTING decision, using two bounded local test proposals.

This is software integration, not new mathematics or external AI generation.
The only proposed edit is an isolated test consumer, never a public proof.
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

import codeai_canonical_cache_reuse_probe_v1 as probe
from runtime import kuuos_codeai_intent_repository_observation_envelope_v0_1 as obs_kernel
from runtime import kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 as synth
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import render_unified_diff
from scripts import ci_verified_lean_project_cache_v1 as cache
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest

ROOT = probe.ROOT
PATH = "artifacts/codeai-portfolio/Probe.lean"
EXPECTED_SCOPE = "2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b"
TEXTS = {
    "a-missing-hypothesis": probe.PROBE.replace(
        "sourceGlobal_implies_overlapFaithful U q s h",
        "sourceGlobal_implies_overlapFaithful U q s"),
    "b-exact-reuse": probe.PROBE,
}

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(out, name, value):
    probe.save(out / name, value)

def observation_receipt(head, gate, files, started, scope):
    # The source observations are collected outside the CodeAI kernel.
    # Use actual GitHub canonical observations, successful prior receipts,
    # and local source bytes; no example or synthetic receipt is promoted.
    observation = probe.actual_observation(head)
    need(observation["source_tree"] == gate["canonical_tree"], "tree changed")
    baseline = []
    for rid in (45711044643, 45711044342, 45714018632):
        run = cache.api(f"actions/runs/{rid}")
        need(run["status"] == "completed" and run["conclusion"] == "success",
             "baseline not completed/success")
        expected_head = head if rid != 45714018632 else "ce551f27e5b4b0c68944b94c018104c21cfb6286"
        need(run["head_sha"] == expected_head, "baseline source mismatch")
        baseline.append(digest({"id":rid, "head":run["head_sha"], "status":run["status"],
                                "conclusion":run["conclusion"]}))
    need(cache.local_scope(ROOT, head) == scope == cache.remote_scope(cache.api, head),
         "canonical proof scope mismatch")
    source_paths = sorted(set(files) | {"lakefile.toml", "lake-manifest.json", "lean-toolchain"})
    source_blobs = {}
    for path in source_paths:
        local = ROOT / path
        need(local.is_file() and not local.is_symlink(), "source missing")
        actual = subprocess.check_output(["git", "rev-parse", f"{head}:{path}"], cwd=ROOT, text=True).strip()
        need(probe.ROOT == ROOT and actual == hashlib.sha1(
            b"blob " + str(local.stat().st_size).encode() + b"\0" + local.read_bytes()).hexdigest(),
            "source blob mismatch")
        source_blobs[path] = actual
    now = int(time.time())
    session = f"{os.environ['GITHUB_RUN_ID']}:{os.environ['GITHUB_RUN_ATTEMPT']}:{os.environ['GITHUB_JOB']}"
    intent = obs_kernel.seal({
        "intent_id":"canonical-cache-portfolio-integration-v1",
        "source_actor_id":"research-assistant",
        "source_channel":"user-directed-codeai-research-continuation",
        "intent_revision":"r1",
        "requirements":["Compare two isolated test consumers of an existing theorem"],
        "assumptions":["REUSE_EXISTING is observed for the exact canonical theorem",
                       "Candidate material is locally supplied test input, not external model output"],
        "unresolved_questions":[],
        "preserved_invariants":["exact canonical proof scope", "no new proof or merge authority"],
        "forbidden_changes":["no canonical source mutation", "no new public theorem", "no external provider"],
        "success_criteria":["one typed consumer fails and one succeeds in real Lean"],
        "authority_owner_id":"repository-owner",
        "intent_created_epoch":started, "prior_intent_digests":[],
        "intent_provenance_confirmed":True,
    }, obs_kernel.INTENT_DIGEST_FIELD)
    repo = obs_kernel.seal({
        "repository_full_name":"itakura-hidetoshi/KuuOS",
        "source_commit_sha":head, "source_branch":"main", "tree_digest":observation["source_tree"],
        "dependency_lock_digest":sha((ROOT/"lake-manifest.json").read_bytes()),
        "toolchain_digest":"lean-4.30.0-rc2-python-3.12", "toolchain_supported":True,
        "observed_paths":source_paths, "unavailable_paths":[], "declared_path_count":len(source_paths),
        "baseline_check_digests":baseline+[digest(gate), digest(scope), digest(source_blobs)],
        "baseline_checks_complete":True,
        "code_owner_scope_digest":digest({"scope":"isolated test only", "path":PATH}),
        "crosses_unowned_boundary":False,
        "observation_started_epoch":started, "observation_completed_epoch":now,
        "session_id":session, "nonce_digest":digest({"session":session,"head":head}),
        "prior_session_ids":[], "prior_nonce_digests":[], "prior_observation_digests":[],
        "observation_collected_by_kernel":False,
        "repository_files_changed_by_kernel":False,"git_ref_changed_by_kernel":False,
        "branch_created_by_kernel":False,"commit_created_by_kernel":False,
        "push_performed_by_kernel":False,"pull_request_created_by_kernel":False,
        "external_side_effect_performed_by_kernel":False,
        "selection_authority_claimed":False,"execution_authority_claimed":False,
        "merge_authority_claimed":False,"deployment_authority_claimed":False,
        "secret_access_authority_claimed":False,
    }, obs_kernel.REPOSITORY_OBSERVATION_DIGEST_FIELD)
    policy = obs_kernel.seal({
        "expected_repository_full_name":"itakura-hidetoshi/KuuOS",
        "expected_source_commit_sha":head,"allowed_source_branches":["main"],
        "supported_toolchain_digests":["lean-4.30.0-rc2-python-3.12"],
        "maximum_observed_paths":8,"maximum_observation_duration":600,
        "require_complete_baseline":True,"require_code_owner_scope":True,
        "allow_partial_observation":False,
    }, obs_kernel.POLICY_DIGEST_FIELD)
    result = obs_kernel.build_codeai_intent_repository_observation_envelope(
        intent_packet=intent,repository_observation=repo,observation_policy=policy)
    need(result.status == obs_kernel.STATUS_READY and result.receipt is not None
         and result.receipt["repository_observation_read_only"] is True, repr(result))
    return result.receipt, {"intent":intent,"observation":repo,"policy":policy,
                            "source_blobs":source_blobs}

def portfolio(head, out, gate, scope, started):
    need(gate["reuse_status"] == "REUSE_EXISTING" and gate["provider_calls"] == 0,
         "original research gate did not allow exact reuse")
    files = {probe.SOURCE:(ROOT/probe.SOURCE).read_bytes().decode("utf-8")}
    source, observed = observation_receipt(head, gate, files, started, scope)
    save(out, "source-observation.json", {"receipt":source, **observed})
    epoch = int(time.time())
    intent = "Isolated software test consumer, not a new mathematical theorem. Reuse " + probe.NAME
    request = patch.seal({
        "request_id":"canonical-cache-portfolio-v1", "request_revision":"r1",
        "intent_text":intent+"\n"+json.dumps(gate,sort_keys=True), "candidate_count":2,
        "request_created_epoch":epoch, "requirement_trace_ids":["intent:exact-reuse"],
        "test_plan_ids":["direct-lean","real-mcp","independent-lean"],
        "risk_labels":["isolated-test"],"unresolved_candidate_questions":[],
        "prior_candidate_digests":[],"prior_producer_session_ids":[],
    }, synth.REQUEST_DIGEST_FIELD)
    policy = patch.seal({
        "allowed_provider_ids":["local_model"], "maximum_provider_calls":2,
        "maximum_raw_output_bytes":10000,"maximum_intent_bytes":100000,
        "maximum_repository_snapshot_bytes":1000000,"maximum_proposals":2,
        "evaluation_epoch":epoch,"maximum_response_age":60,"maximum_request_age":60,
        "allowed_repository_path_prefixes":["formal","artifacts/codeai-portfolio"],
        "forbidden_repository_path_prefixes":["formal/private"],
    }, synth.POLICY_DIGEST_FIELD)
    candidate_policy = patch.seal({
        "expected_source_observation_receipt_digest":source[patch.SOURCE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name":"itakura-hidetoshi/KuuOS",
        "expected_source_commit_sha":head,"allowed_patch_formats":["unified_diff"],
        "maximum_patch_bytes":10000,"maximum_changed_paths":1,
        "allowed_path_prefixes":["artifacts/codeai-portfolio"],
        "forbidden_path_prefixes":["formal","lean"],"allow_deletions":False,
        "allow_renames":False,"allow_binary_patches":False,"allow_submodule_patches":False,
        "allow_mode_changes":False,"require_requirement_trace":True,"require_test_plan":True,
        "allow_evidence_degradation":False,"known_risk_labels":["isolated-test"],
        "handover_risk_labels":[],"evaluation_epoch":epoch,"maximum_candidate_age":60,
    }, patch.POLICY_DIGEST_FIELD)
    calls=[]
    def callback(key):
        def generate(prompt):
            need(prompt["repository_files"] == files and prompt["intent_text"] == request["intent_text"],
                 "provider context changed")
            calls.append(key)
            return {
                "provider_response_id":"response:"+key,
                "producer_session_id":"session:"+key+":"+observed["observation"]["session_id"],
                "response_created_epoch":epoch,
                "raw_output":json.dumps({"proposal_id":key,"candidate_revision":"r1",
                    "edits":[{"path":PATH,"operation":"add","new_content":TEXTS[key]}],
                    "risk_labels":["isolated-test"],"unresolved_candidate_questions":[]}),
                "claims_authority":False,"hides_uncertainty":False,
                "bypasses_governance":False,"evidence_missing":False,
            }
        return generate
    # The research gate already returned REUSE_EXISTING, not a new research
    # candidate. The generic software kernel only constructs a test consumer.
    result = synth.build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=source,repository_files=files,
        synthesis_request=request,synthesis_policy=policy,candidate_policy=candidate_policy,
        provider_adapters=[synth.ProviderAdapter(k,"local_model","local-supplied-test-material",callback(k))
                           for k in sorted(TEXTS)])
    save(out,"synthesis.json", {"status":result.status,"issues":result.issues,
        "attempts":[asdict(x) for x in result.attempts],"receipt":result.receipt})
    need(result.status == synth.STATUS_READY and len(result.candidates)==2 and calls==sorted(TEXTS),
         "original candidate kernel did not produce two admitted patches: "+repr(result.issues))
    rows=[]
    for candidate in result.candidates:
        key = candidate.proposal_id
        text = TEXTS[key]
        expected, shape, issues = render_unified_diff(files,[{"path":PATH,"operation":"add","new_content":text}])
        need(not issues and expected==candidate.patch_artifact
             and candidate.patch_candidate["added_paths"]==[PATH],
             "generated patch correspondence failed")
        folder=out/key
        folder.mkdir()
        (folder/"candidate.diff").write_text(candidate.patch_artifact)
        save(folder,"candidate.json",candidate.patch_candidate)
        save(folder,"candidate-receipt.json",candidate.candidate_receipt)
        f=folder/"Probe.lean"
        f.write_text(text,encoding="utf-8")
        cmd=["lake","env","lean",*probe.canonical_direct_options((ROOT/"lakefile.toml").read_bytes()),
             str(f.relative_to(ROOT))]
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=300)
        log=p.stdout+"\n"+p.stderr
        (folder/"direct.log").write_text(log)
        good=(p.returncode==0 and "does not depend on any axioms" in log
              and "sorryAx" not in log and not re.search(r"\b(?:warning|error):",log))
        # Do not manufacture success from candidate rank or intended outcome.
        row={"id":key,"source_sha256":sha(f.read_bytes()),
             "patch_sha256":sha(candidate.patch_artifact.encode()),"exit":p.returncode,
             "direct_green":good,"log_sha256":sha(log.encode())}
        rows.append(row)
        print("KUUOS_PORTFOLIO_ATTEMPT",json.dumps(row,sort_keys=True),flush=True)
        print(log,flush=True)
    winners=[x for x in rows if x["direct_green"]]
    need(len(winners)==1 and winners[0]["id"]=="b-exact-reuse",
         "expected one genuine Lean success")
    bad=next(x for x in rows if x["id"]=="a-missing-hypothesis")
    need(bad["exit"]!=0 and "error:" in (out/bad["id"]/"direct.log").read_text(),
         "negative candidate did not produce actual Lean error")
    chosen=winners[0]
    # The chosen bytes are copied from the admitted patch's directly checked
    # isolated file; no source write to the canonical formal library.
    (out/"Probe.lean").write_bytes((out/chosen["id"]/"Probe.lean").read_bytes())
    direct={"gate":gate,"probe_sha256":chosen["source_sha256"],"direct_exit":0,
            "axioms":[],"proof_authority":False,"novelty_certified":False}
    save(out,"direct.json",direct)
    stable={"head":head,"tree":gate["canonical_tree"],"scope":digest(scope),
            "gate_digest":digest(gate),"selected":chosen["id"],
            "candidates":[{k:v for k,v in row.items() if k!="log_sha256"} for row in sorted(rows,key=lambda x:x["id"])],
            "external_model":False,"new_mathematical_result":False,
            "formal_source_changed":False}
    save(out,"portfolio.json",stable)
    print("KUUOS_PORTFOLIO_DIRECT_GREEN",json.dumps(stable,sort_keys=True),flush=True)
    need(probe.actual_observation(head)["source_tree"]==gate["canonical_tree"],"canonical main changed")
    return stable

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True)
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args()
    out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated output only")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="mcp":
        probe.mcp(a.head,out)
        return
    started=int(time.time())
    scope=cache.local_scope(ROOT,a.head)
    need(digest(scope)==EXPECTED_SCOPE,"unexpected proof scope")
    gate=probe.actual_gate(a.head,out)
    current=portfolio(a.head,out,gate,scope,started)
    if a.phase=="independent":
        need(a.first is not None,"first receipt required")
        first=json.loads((a.first/"portfolio.json").read_text())
        d=json.loads((a.first/"direct.json").read_text())
        m=json.loads((a.first/"mcp.json").read_text())
        need(first==current and m["status"]=="REAL_LEAN_MCP_REUSE_GREEN"
             and m["direct_digest"]==digest(d)
             and d==json.loads((out/"direct.json").read_text()),
             "independent candidate evidence differs")
        receipt={"status":"INDEPENDENT_PORTFOLIO_GREEN",
                 "portfolio_digest":digest(current),"first_mcp_digest":digest(m),
                 "proof_authority":False,"novelty_certified":False}
        save(out,"independent.json",receipt)
        print("KUUOS_PORTFOLIO_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
