#!/usr/bin/env python3
"""R74 R2: compile the unchanged directly audited source once; verify imported
theorems through real lean_verify. Preserve complete fresh full-source diagnostics.
The import module is an audit transport, not a new proof or release authority."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_batch_readiness_v1_r74 as r1
v=r1.v
sha=r1.r63.r62.r23.sha
load=r1.load
digest=r1.old.digest
ROOT=r1.ROOT
RUN=46130035958
JOB=140932946382
HEAD="880d06b1b3836c13c548fdc063c0d020e2df6206"
ART=15258336529
ART_DIGEST="sha256:6ea5493286b7bb75f8add452e9c1ca70eb23965de7a4f2af0d3f8c24bf93cc6c"
DIRECT="52c2f717f36e56d6d2350a3597fc0d5feeb29833d3e28ad233fbb01642be0783"
DIRECT_SOURCE="16c48f91e2c9de221dc2c01577caac9b7737d3108e2fe2e3a11d9c6452f41490"
MCP_SOURCE="a25d39e0c62c6f28bca42d0d179fca3d91a97f2a371622626064ee5322c3a289"
COVERAGE="f33f56722763c4baf6768078f6fcf197e267ba5f294ec0b02c700ae2343af93c"
VERIFY_API_BLOB="86fc7a528cbd7d980c97b6558b805ca2dfc28743"
SCRATCH_API_BLOB="d8bcf34decb2459d2cdcefb8c84f70f3f2986b6a"
MODULE="RecoveryDualityR62"
VIEW="McpCapsuleApplication.lean"
VIEW_TEXT="import "+MODULE+"\n"
CAP="audit-capsule"
CAP_MANIFEST="r74-r2-audit-capsule.json"
REPLAY="r74-r2-imported-replay.json"
REPAIR="r74-r2-repair.json"
STANDARD={"Classical.choice","Quot.sound","propext"}
FIELDS=("type_expr_repr","type_expr_sha256","universe_parameters","type_constants",
        "proof_constants","axioms","proof_body_observed","direct_expression_constants_only","expected_direct_refs")
HIST_RAW=tuple("parent-r"+str(i)+"-raw-replay.json" for i in range(62,74))

def original_failure(a):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN));job=api("actions/jobs/"+str(JOB));art=api("actions/artifacts/"+str(ART))
    v.need(run["id"]==RUN and run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="failure" and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R74 registry batch readiness" and s["status"]=="completed" and s["conclusion"]=="success" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R74 new declarations and exact prior receipt reuse" and s["status"]=="completed" and s["conclusion"]=="failure" for s in job["steps"]),
           "R74 R1 successful direct and failed MCP lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r74-local-46130035958-1" and art["digest"]==ART_DIGEST and not art["expired"] and
           art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R74 R1 artifact identity")
    p=a.r1_failure;d=load(p/"direct.json")
    v.need(sha((p/"direct.json").read_bytes())=="7a52163a9a13538e99822857d5229d350aa01e15c3aa38e496bab540862c9304" and
           digest(d)==DIRECT and d["status"]=="R74_DIRECT_REGISTRY_BATCH_READINESS" and
           d["readiness_path_key"]=="2b300673b9dfb37e177b6a5233459ac57f3bf9cd23bebea4205abab13da852e5" and
           sha((p/(MODULE+".lean")).read_bytes())==DIRECT_SOURCE and
           sha((p/"McpApplication.lean").read_bytes())==MCP_SOURCE and
           (p/"McpApplication.lean").read_bytes()==d["fresh_application"]["mcp_source"].encode() and
           len(d["fresh_application"]["observations"])==327 and len(d["new_theorem_names"])==14,
           "R74 R1 exact direct receipt and source")
    rows=d["fresh_application"]["observations"]
    v.need(not (p/"mcp.json").exists() and {q.name for q in p.glob("mcp-verify-*.json")}==
           {"mcp-verify-"+str(j)+".json" for j in range(313)} and
           rows[313]["name"]=="KuuOSR74.actual_order_independent_0" and
           set(x["name"] for x in rows[313:])==set(d["new_theorem_names"]),
           "R74 R1 no new declaration MCP receipt")
    # Prior R1 full diagnostic receipt is preserved as history, not as R2 fresh evidence.
    coverage=load(p/"mcp-diagnostic-coverage.json")
    v.need(digest(coverage)==COVERAGE and coverage["source_sha256"]==MCP_SOURCE and
           coverage["mcp_version"]==v.EXPECTED_SERVER_VERSION and coverage["full_source"] is True and
           coverage["no_line_or_declaration_filter"] is True and len(coverage["receipts"])==2,
           "R74 R1 complete diagnostic scope")
    for entry,(severity,name) in zip(coverage["receipts"],r1.DIAG_FILES):
        v.need(entry["severity"]==severity and entry["file"]==name and
               entry["request"]=={"file_path":"artifacts/olean-r74/McpApplication.lean","severity":severity,"timeout_s":600} and
               entry["raw_sha256"]==sha((p/name).read_bytes()) and r1.complete_diagnostic(load(p/name)),
               "R74 R1 complete diagnostic "+severity)
    parent=p/"parent-r73-receipts";pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(digest(pd)==r1.DIRECT and digest(pm)==r1.MCP,"R74 R1 prior receipts")
    for j,row in enumerate(rows[:313]):
        v.need(row==pd["fresh_application"]["observations"][j] and
               (p/f"mcp-verify-{j}.json").read_bytes()==(parent/f"mcp-verify-{j}.json").read_bytes(),
               "R74 R1 exact historical MCP receipt "+str(j))
    return d,coverage

def capsule_files(folder):
    base=folder/(MODULE+".olean")
    files=[base,Path(str(base)+".server"),Path(str(base)+".private")]
    present=[p.is_file() and not p.is_symlink() for p in files]
    v.need(present[0] and present[1]==present[2],"R74 audit capsule parts incomplete")
    v.need({p.name for p in folder.iterdir()}=={p.name for p,ok in zip(files,present) if ok},
           "R74 audit capsule unexpected file")
    return [{"name":p.name,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for p,ok in zip(files,present) if ok]

def install(folder,files):
    v.need(capsule_files(folder)==files,"R74 audit capsule manifest")
    dest=ROOT/".lake/build/lib/lean"
    v.need(dest.is_dir(),"R74 canonical cache absent")
    for suffix in (".olean",".olean.server",".olean.private"):
        v.need(not (dest/(MODULE+suffix)).exists(),"R74 audit module destination collision")
    for f in files:
        with (dest/f["name"]).open("xb") as dst:
            dst.write((folder/f["name"]).read_bytes())
        v.need(sha((dest/f["name"]).read_bytes())==f["sha256"],"R74 installed audit capsule drift")

def installed_matches(files):
    dest=ROOT/".lake/build/lib/lean"
    for f in files:
        p=dest/f["name"]
        v.need(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==f["sha256"],
               "R74 imported module changed "+f["name"])

def direct_compile(a,out):
    prior,coverage=original_failure(a)
    cap=out/CAP;cap.mkdir()
    old_run=r1.r63.r62.r23.run_lean
    compiled=0
    def compile_once(args,path,src):
        nonlocal compiled
        if path!=ROOT/"artifacts"/"olean-r62"/(MODULE+".lean"):
            return old_run(args,path,src)
        v.need(compiled==0 and args==[] and isinstance(src,str) and sha(src.encode())==DIRECT_SOURCE,
               "R74 only compile exact original direct source")
        path.write_text(src,encoding="utf-8")
        opts=v.canonical_direct_options((ROOT/"lakefile.toml").read_bytes())
        # Same original source; module root/output only. No hypothesis, option or proof changes.
        command=["lake","env","lean",*opts,"--root="+str(path.parent),"-o",str(cap/(MODULE+".olean")),str(path)]
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=600)
        log=result.stdout+"\n"+result.stderr
        path.with_suffix(".log").write_text(log,encoding="utf-8")
        v.need(result.returncode==0 and not re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)",log),
               "R74 compile original directly audited source failed")
        compiled+=1
        return log
    r1.r63.r62.r23.run_lean=compile_once
    try:
        d=r1.direct(a,out)
    finally:
        r1.r63.r62.r23.run_lean=old_run
    v.need(compiled==1 and d==prior and digest(d)==DIRECT,
           "R74 exact original direct proof receipt after compile")
    for name in r1.FILES+(r1.NEW,"direct.json",MODULE+".lean","formal-source.lean",
                 "readiness-application.lean","readiness-computation.lean","readiness-computation.json",
                 "historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",*HIST_RAW):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R74 R1 unchanged exact bytes "+name)
    files=capsule_files(cap);install(cap,files)
    # Observe the compiled module in a new Lean file, rather than assuming
    # byte identity implies that import resolves the intended declarations.
    raw_expected={}
    for filename in (*HIST_RAW,r1.NEW):
        obs=load(out/filename)
        if filename==r1.NEW:obs=obs["raw_theorems"]
        v.need(not set(raw_expected).intersection(obs),"R74 duplicate raw inventory")
        raw_expected.update(obs)
    rows=d["fresh_application"]["observations"]
    names=sorted(x["name"] for x in rows)
    expected={x["name"]:x for x in rows}
    v.need(len(raw_expected)==228 and set(raw_expected)<=set(names),"R74 imported full proof inventory")
    src=VIEW_TEXT+"\n"+r1.raw_observer(sorted(raw_expected))+v.suffix(names)
    log=old_run([],out/"CapsuleObservation.lean",src)
    observed=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]["expected_direct_refs"]} for n in names])
    v.need(len(observed)==len(rows)==327 and {x["name"] for x in observed}==set(names),"R74 imported audit inventory")
    for row in observed:
        old=expected[row["name"]]
        v.need(all(row[k]==old[k] for k in FIELDS) and "sorryAx" not in row["type_expr_repr"],
               "R74 imported type, proof references, universe or axioms differ "+row["name"])
    raw=r1.raw_audit(log,{x["name"]:x for x in observed},sorted(raw_expected))
    for name,row in raw.items():
        prior_raw=raw_expected[name]
        v.need(all(row[k]==prior_raw[k] for k in ("name","type_expr","proof_expr","universe_parameters")) and
               sorted(set(row["axioms"]))==sorted(set(prior_raw["axioms"])) and "sorryAx" not in row["type_expr"],
               "R74 imported complete proof or type drift "+name)
    replay={"observations":[{"name":row["name"],**{k:row[k] for k in FIELDS}} for row in observed],
            "raw_proof_digests":{n:digest({**x,"axioms":sorted(set(x["axioms"]))}) for n,x in raw.items()}}
    v.save(out/REPLAY,replay)
    (out/VIEW).write_text(VIEW_TEXT,encoding="utf-8")
    manifest={"schema":"kuuos.codeai.r74.compiled-audit-transport.v1","module":MODULE,"files":files,
              "source_sha256":DIRECT_SOURCE,"direct_digest":DIRECT,"mcp_source_sha256":MCP_SOURCE,
              "view":VIEW,"view_sha256":sha(VIEW_TEXT.encode()),"imported_replay_digest":digest(replay),
              "imported_audits":327,"imported_complete_proofs":228,"compiled_once_per_direct_runner":True,
              "same_source_propositions":True,"proof_authority":False,"action_authority":False}
    v.save(out/CAP_MANIFEST,manifest)
    # Preserve R1 failure evidence separately from the new execution.
    hist=out/"r74-r1-mcp-history";hist.mkdir()
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        shutil.copyfile(a.r1_failure/name,hist/name)
    repair={"status":"R74_R2_COMPILED_AUDIT_TRANSPORT","r1_run":RUN,"r1_job":JOB,"r1_head":HEAD,
            "r1_artifact":ART,"r1_artifact_digest":ART_DIGEST,"r1_direct_digest":DIRECT,
            "r1_diagnostic_coverage_digest":COVERAGE,"r1_direct_receipt_equal":True,
            "r1_original_sources_and_proofs_equal":True,"r1_new_mcp_receipts":0,
            "r1_first_unfinished_theorem":"KuuOSR74.actual_order_independent_0",
            "r1_observed_timeout_s":300,"r1_failure_not_admitted":True,
            "pinned_verify_api_blob":VERIFY_API_BLOB,"pinned_scratch_api_blob":SCRATCH_API_BLOB,
            "direct_compilation_count":1,"imported_audits":327,"imported_complete_proofs":228,
            "all_imported_types_refs_axioms_equal":True,"all_imported_available_full_proofs_equal":True,
            "imported_replay_digest":digest(replay),"full_source_diagnostics_required_fresh":True,
            "new_mcp_audits_required":14,"prior_mcp_audits_reused":313,"proof_authority":False,"action_authority":False}
    v.save(out/REPAIR,repair)
    print("KUUOS_R74_R2_CAPSULE",json.dumps({"manifest":manifest,"repair":repair},sort_keys=True),flush=True)
    return d

def check_capsule(out,d):
    manifest=load(out/CAP_MANIFEST);replay=load(out/REPLAY)
    v.need(manifest["schema"]=="kuuos.codeai.r74.compiled-audit-transport.v1" and manifest["module"]==MODULE and
           manifest["files"]==capsule_files(out/CAP) and manifest["source_sha256"]==sha((out/(MODULE+".lean")).read_bytes())==DIRECT_SOURCE and
           manifest["direct_digest"]==digest(d)==DIRECT and manifest["mcp_source_sha256"]==MCP_SOURCE and
           manifest["view"]==VIEW and (out/VIEW).read_bytes()==VIEW_TEXT.encode() and
           manifest["view_sha256"]==sha((out/VIEW).read_bytes()) and manifest["imported_replay_digest"]==digest(replay) and
           manifest["imported_audits"]==len(replay["observations"])==327 and
           manifest["imported_complete_proofs"]==len(replay["raw_proof_digests"])==228 and
           manifest["proof_authority"] is False and manifest["action_authority"] is False,
           "R74 exact compiled transport manifest")
    rows=d["fresh_application"]["observations"]
    v.need(replay["observations"]==[{"name":r["name"],**{k:r[k] for k in FIELDS}} for r in rows],
           "R74 imported replay metadata")
    raw_expected={}
    for name in (*HIST_RAW,r1.NEW):
        x=load(out/name)
        if name==r1.NEW:x=x["raw_theorems"]
        raw_expected.update(x)
    v.need(replay["raw_proof_digests"]=={n:digest({**x,"axioms":sorted(set(x["axioms"]))}) for n,x in raw_expected.items()},
           "R74 imported exact proof digests")
    return manifest,replay

def new_client(label):
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=r1.DIAG_CLIENT_TIMEOUT)
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":label,"version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools")
        return client
    except BaseException:
        client.close();raise

def mcp(out):
    d=load(out/"direct.json");manifest,replay=check_capsule(out,d)
    installed_matches(manifest["files"])
    parent=out/"parent-r73-receipts";pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(digest(pd)==r1.DIRECT and digest(pm)==r1.MCP and pm["direct_digest"]==r1.DIRECT and
           pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R74 parent MCP lineage")
    parent_rows={r["name"]:(j,r) for j,r in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==313 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R74 distinct MCP inventory")
    p=out/"McpApplication.lean";p.write_text(d["fresh_application"]["mcp_source"],encoding="utf-8")
    v.need(sha(p.read_bytes())==MCP_SOURCE,"R74 original full-source diagnostics target")
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp"]
    version=v.server_version(cmd,ROOT)
    # Fresh full-source diagnostic evidence on unchanged source. The subsequent
    # individual axiom checks use a separate MCP session importing the capsule.
    client=new_client("KuuOS R74 full-source diagnostics")
    try:
        coverage=r1.run_complete_diagnostics(client,str(p.relative_to(ROOT)),out,p)
    finally:
        client.close()
    client=new_client("KuuOS R74 compiled audit transport")
    rows=[];origins=[]
    rel=str((out/VIEW).relative_to(ROOT))
    try:
        for j,row in enumerate(d["fresh_application"]["observations"]):
            name=row["name"];dest=out/f"mcp-verify-{j}.json"
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(row==prior and d["parent_raw_replay_bytewise_equal"],"R74 unchanged prior direct observation")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,dest);raw=load(dest)
                origin={"name":name,"mode":"exact_reused","origin_run":r1.RUN,"origin_job":140922302875,
                        "parent_audit_index":k,"prior_origin":pm["audit_origins"][k],"receipt_sha256":sha(dest.read_bytes())}
            else:
                v.need(name in d["new_theorem_names"],"R74 new audit identity")
                installed_matches(manifest["files"])
                args={"file_path":rel,"theorem_name":name,"scan_source":False}
                print("KUUOS_R74_R2_VERIFY_START",json.dumps(args,sort_keys=True),flush=True)
                raw=client.request("tools/call",{"name":"lean_verify","arguments":args})
                v.save(dest,raw)
                v.need(raw["result"]["isError"] is False,"R74 imported lean_verify failed "+name)
                origin={"name":name,"mode":"fresh_actual_mcp","receipt_sha256":sha(dest.read_bytes()),
                        "request":args,"audit_capsule_digest":digest(manifest),"audit_view_sha256":manifest["view_sha256"]}
            val=v.structured(raw);ax=r1.normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R74 actual MCP axiom audit "+name)
            rows.append({"name":name,"axioms":ax});origins.append(origin)
    finally:
        client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==313 and fresh==14 and len(rows)==327,"R74 new and reused MCP counts")
    installed_matches(manifest["files"])
    result={"status":"R74_REAL_MCP_GREEN","direct_digest":digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":r1.MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
            "diagnostic_coverage_digest":digest(coverage),"mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version,
            "audit_transport":"compiled_import_exact_replay","audit_capsule_digest":digest(manifest),
            "audit_view_sha256":manifest["view_sha256"],"imported_replay_digest":digest(replay)}
    v.save(out/"mcp.json",result)
    print("KUUOS_R74_MCP",json.dumps({"mcp_digest":digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True,
          "audit_transport":result["audit_transport"],"audit_capsule_digest":digest(manifest)},sort_keys=True),flush=True)

def independent(d,first,out):
    current,replay=check_capsule(out,d);prior,first_replay=check_capsule(first,d)
    mp=load(first/"mcp.json")
    v.need(replay==first_replay and (first/REPAIR).read_bytes()==(out/REPAIR).read_bytes() and
           mp["audit_transport"]=="compiled_import_exact_replay" and mp["audit_capsule_digest"]==digest(prior) and
           mp["audit_view_sha256"]==prior["view_sha256"] and mp["imported_replay_digest"]==digest(first_replay),
           "R74 independent exact capsule semantic replay")
    fresh=[x for x in mp["audit_origins"] if x["mode"]=="fresh_actual_mcp"]
    v.need(len(fresh)==14 and {x["name"] for x in fresh}==set(d["new_theorem_names"]),"R74 actual fresh MCP inventory")
    for x in fresh:
        v.need(x["request"]=={"file_path":"artifacts/olean-r74/"+VIEW,"theorem_name":x["name"],"scan_source":False} and
               x["audit_capsule_digest"]==digest(prior) and x["audit_view_sha256"]==prior["view_sha256"],
               "R74 actual import-only MCP request identity")
    # Original independent verifier still validates all 327 individual receipts,
    # both complete full-source diagnostic receipts, and every prior ledger.
    r1.independent(d,first,out)
    result={"status":"R74_R2_INDEPENDENT_AUDIT_TRANSPORT_GREEN","direct_digest":digest(d),
            "mcp_digest":digest(mp),"sandbox_audit_capsule_digest":digest(prior),
            "independent_audit_capsule_digest":digest(current),"compiled_file_bytes_equal":current["files"]==prior["files"],
            "imported_replay_digest":digest(replay),"imported_replay_equal":True,"imported_audits":327,
            "imported_complete_proofs":228,"new_actual_mcp_audits":14,"prior_mcp_audits_reused":313,
            "fresh_full_source_diagnostics":True,"r1_direct_receipt_equal":True,
            "historical_research_only":True,"proof_authority":False,"action_authority":False}
    v.save(out/"r74-r2-independent-transport.json",result)
    print("KUUOS_R74_R2_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r73-local","r73-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"R74 isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct_compile(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
