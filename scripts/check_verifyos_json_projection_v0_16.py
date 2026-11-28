#!/usr/bin/env python3
"""Actual raw JSON to Lean projection, with exact replay of synthetic evidence."""
from __future__ import annotations
import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/"tests")]
from scripts import check_verifyos_typed_projection_v0_15 as t
from scripts import check_verifyos_method_sound_coverage_v0_14 as m

b,c,p = t.b,t.c,t.c.p
need,blob,sha,canonical,save,load,normalize = t.need,t.blob,t.sha,t.canonical,t.save,t.load,t.normalize
NS = "KUOS.VerifyOS.JsonProjectionV0_16."
SOURCE = "scripts/lean_probes/verifyos_json_projection_v0_16.lean"
CLI = "scripts/lean_probes/verifyos_json_projection_cli_v0_16.lean"
PINS = {
    SOURCE:"c1b34a9ffd87c501f65de50f84ff75e298a212c8",
    CLI:"34ad19e18f73866754fe9678b808ad4c0e4e2891",
    "scripts/check_verifyos_typed_projection_v0_15.py":"60e9803245d206f62187999edaf8711d38bca967",
}
MODULES = ("MethodSoundCoverage","TypedProjection","JsonProjection","ProjectionCLI")
NAMESPACES = (m.NS,t.NS,NS,"")
BOUNDARY = dict(proof_authority=False,action_authority=False,complete_python_refinement_proved=False)


def sources():
    for path,digest in PINS.items():
        need(re.fullmatch(r"[0-9a-f]{40}",digest) is not None,"INVALID_PIN_FORMAT:"+path)
        raw=(ROOT/path).read_bytes()
        actual=blob(raw)
        print("VERIFYOS_V016_SOURCE_PIN",path,"bytes",len(raw),"actual",actual,"expected",digest,flush=True)
        need(actual==digest,"SOURCE_PIN:"+path+":"+actual+":"+digest)
    prior,typed=t.sources()
    return prior,typed,(ROOT/SOURCE).read_bytes(),(ROOT/CLI).read_bytes()


def inventory(raw):
    text=raw.decode("utf-8")
    names=re.findall(r"(?m)^ *(?:inductive|structure|def|theorem) (\w+)",text)
    theorems=re.findall(r"(?m)^ *theorem (\w+)",text)
    need(names==re.findall(r"(?m)^#print axioms (\w+)$",text),"AUDIT_INVENTORY")
    need(len(set(names))==len(names),"DUPLICATE_DECLARATION")
    need(not re.search(r"\b(?:sorry|admit|axiom|unsafe|native_decide)\b",
        "\n".join(x for x in text.splitlines() if not x.startswith("#print axioms"))),"FORBIDDEN_PROOF_TOKEN")
    return names,theorems


def compile_module(project,name,raw,ns,out):
    names,theorems=inventory(raw)
    env={**os.environ,"LEAN_PATH":str(project.resolve())}
    version=subprocess.run(["lean","--version"],check=True,capture_output=True,text=True).stdout.strip()
    need("version 4.30.0-rc2" in version,"LEAN_PIN")
    path=project/(name+".lean")
    path.write_bytes(raw)
    start=time.monotonic()
    res=subprocess.run(["lean","-DwarningAsError=true","-Dweak.sorryAsError=true","-o",
        name+".olean",name+".lean"],cwd=project,env=env,capture_output=True,text=True,timeout=180)
    log=res.stdout+"\n"+res.stderr
    (out/(name+".log")).write_text(log)
    print(log,flush=True)
    print("VERIFYOS_V016_LEAN_EXIT",name,res.returncode,"seconds",time.monotonic()-start,flush=True)
    need(res.returncode==0 and (project/(name+".olean")).is_file(),"DIRECT_LEAN_FAILED:"+name)
    need(not re.search(r"\b(?:warning:|error:|sorryAx)\b",log),"LEAN_DIAGNOSTIC:"+name)
    found=re.findall(r"'("+re.escape(ns)+r"\w+)' (?:does not depend on any axioms|depends on axioms: \[([^\]]*)\])",log)
    need(len(found)==len(names) and {x[0] for x in found}=={ns+x for x in names},"AXIOM_INVENTORY:"+name)
    need(path.read_bytes()==raw,"MODULE_DRIFT")
    return dict(source_sha256=sha(raw),source_blob=blob(raw),version=version,declarations=len(names),
        theorems=len(theorems),axioms={n:normalize([x.strip() for x in a.split(",") if x.strip()]) for n,a in found})


def projected_rows(receipt,req,pub):
    return [{"claim_id":x,"value":(r["value"] if r["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" else None)}
        for x in t.ORDER for r in [c.project(x,receipt,req,pub)]]


def hold_rows():
    return [{"claim_id":x,"value":None} for x in t.ORDER]


def construct_cases(folder):
    """Only synthetic v0.13 fixtures; mutated inputs are NOT admitted receipts."""
    folder.mkdir()
    test=t.fixture.PairTests("test_real_pair_and_diverse_match")
    try:
        root,args=test.pair("correct")
        verified=t.d.verify_diverse(root,**args)
        need(verified["status"]=="DIVERSE_FROZEN_PROFILE_AGREEMENT_ONLY","PAIR_NOT_ADMITTED")
        pub=verified["pair"]["primary"]; raw=args["primary_raw"]; req=args["request"]
        bundle=p.strict(raw)
        context=sha(canonical(args["context"]))
        request_digest=sha(canonical(req))
        need(pub["context_sha256"]==context and pub["bundle_sha256"]==sha(raw)
            and pub["request_sha256"]==request_digest,"ADMITTED_BYTE_BINDING")
        signed=[{"claim_id":x["claim_id"],"value":x["value"]} for x in pub["claims"]]
        need(projected_rows(bundle["receipt"],req,pub)==signed and sum(x["value"] is not None for x in signed)==13,
            "SIGNED_ROW_MISMATCH")
        cases=[]
        def add(name,raw_bytes,rows=None,status="TYPED_JSON_PROJECTION_ONLY",mode="synthetic_mutation",
                source=context,target=context,tip=req["tip"],request=request_digest,admitted=True):
            path=name+".json"
            # The original admitted bundle is passed unchanged; the test cases
            # separately exercise rejection of intentionally forged bytes.
            (folder/path).write_bytes(raw_bytes)
            cases.append(dict(name=name,file=path,raw_sha256=sha(raw_bytes),request=request,
                source=source,target=target,tip=tip,admitted=admitted,mode=mode,
                expected_status=status,expected_rows=hold_rows() if rows is None else rows))
        add("signed_pair",raw,signed,mode="actual_admitted_synthetic_pair")
        def mutate(name,transform,compare=True,**kw):
            changed=copy.deepcopy(bundle)
            transform(changed["receipt"])
            rows=projected_rows(changed["receipt"],req,pub) if compare else None
            add(name,canonical(changed),rows,**kw)
        def stdout_mut(name,i,transform,compare=True,**kw):
            def edit(rec):
                node=rec["processes"][i]
                payload=b.parse(node["stdout"])
                transform(payload)
                node["stdout"]=canonical(payload).decode()
            mutate(name,edit,compare,**kw)
        def stdout_text(name,transform,i=0):
            def edit(rec):
                node=rec["processes"][i]
                node["stdout"]=transform(node["stdout"])
            mutate(name,edit,False,status="HOLD")
        add("pretty_unsorted",json.dumps(bundle,ensure_ascii=False,indent=2).encode(),signed)
        stdout_mut("boolean_not_nat",0,lambda x:x.update(rule_count=True,withdrawn_count=False))
        stdout_mut("negative_count",0,lambda x:x.update(obstruction_count=-1))
        stdout_mut("text_not_nat",0,lambda x:x.update(rule_count="10",seq="1"))
        stdout_mut("missing_fields",0,lambda x:[x.pop(k) for k in ("rule_count","seq")])
        stdout_mut("nested_array",1,lambda x:x.update(reviews=[1,2,3]))
        stdout_mut("wrong_status",0,lambda x:x.update(status="PASS_SCOPE_RECORDS_ONLY"))
        stdout_mut("literal_unicode",0,lambda x:x.update(status="未知"))
        stdout_mut("wrong_tip",0,lambda x:x.update(tip_sha256="f"*64))
        stdout_mut("unsupported_injection",0,lambda x:x.update(action_permission=True,current_tip=req["tip"],external_truth=True,lean_proof=True,new_context_validity=True))
        mutate("nonzero_exit",lambda r:r["processes"][0].update(exit_code=7))
        mutate("boolean_exit",lambda r:r["processes"][1].update(exit_code=False))
        mutate("wrong_gate",lambda r:r["processes"][0].update(gate="wrong.py"),False,status="HOLD")
        mutate("swapped_gates",lambda r:r["processes"].reverse(),False,status="HOLD")
        mutate("missing_process",lambda r:r["processes"].pop(),False,status="HOLD")
        mutate("wrong_request",lambda r:r.update(request_sha256="f"*64),False,status="HOLD")
        add("wrong_context",raw,status="HOLD",source="f"*64)
        add("unadmitted",raw,status="HOLD",admitted=False)
        add("bad_context_encoding",raw,status="HOLD",target="not a digest")
        add("duplicate_outer_key",raw.replace(b'"receipt":',b'"receipt":null,"receipt":',1),status="HOLD")
        add("trailing_bytes",raw+b"false",status="HOLD")
        add("malformed_outer",raw[:-10],status="HOLD")
        def prefix_member(s,key,value):
            need(s.startswith("{"),"FIXTURE_OBJECT")
            return "{"+json.dumps(key)+":"+value+","+s[1:]
        stdout_text("duplicate_stdout_key",lambda s:prefix_member(s,"rule_count","11"))
        stdout_text("exponent_number",lambda s:s.replace('"rule_count": 10','"rule_count": 1e1'))
        stdout_text("integral_decimal",lambda s:s.replace('"rule_count": 10','"rule_count": 10.0'))
        stdout_text("leading_zero",lambda s:s.replace('"rule_count": 10','"rule_count": 010'))
        stdout_text("integer_limit",lambda s:s.replace('"rule_count": 10','"rule_count": '+'9'*65))
        stdout_text("unicode_escape",lambda s:s.replace('"rule_count"','"\\u0072ule_count"'))
        stdout_text("nested_duplicate_key",lambda s:prefix_member(s,"reviews",'{"x":1,"x":2}'),i=1)
        stdout_text("malformed_stdout",lambda s:"{")
        stdout_text("depth_limit",lambda s:prefix_member(s,"deep","["*513+"0"+"]"*513))
        # Guard mutation construction itself; no negative test may silently
        # exercise the original normal stdout because a replacement missed.
        for item in cases:
            if item["name"] in {"exponent_number","integral_decimal","leading_zero","integer_limit","unicode_escape"}:
                need(item["raw_sha256"]!=sha(raw),"MUTATION_NOT_APPLIED:"+item["name"])
        save(folder/"manifest.json",cases)
        return cases
    finally:
        test.doCleanups()


def run_cases(project,folder,cases,out_log):
    args=[]
    for item in cases:
        name=item["file"]
        need(name==item["name"]+".json" and re.fullmatch(r"[a-z_]+\.json",name),"CASE_NAME")
        raw=(folder/name).read_bytes()
        need(sha(raw)==item["raw_sha256"],"CASE_BYTE_BINDING:"+name)
        raw.decode("utf-8",errors="strict")
        args.extend([str((folder/name).resolve()),item["request"],item["source"],item["target"],
                     item["tip"],str(item["admitted"]).lower()])
    start=time.monotonic()
    result=subprocess.run(["lean","-DwarningAsError=true","-Dweak.sorryAsError=true","--run","ProjectionCLI.lean",*args],
        cwd=project,env={**os.environ,"LEAN_PATH":str(project.resolve())},capture_output=True,text=True,timeout=180)
    out_log.write_text(result.stdout+"\n"+result.stderr)
    print("VERIFYOS_V016_JSON_EXIT",result.returncode,"seconds",time.monotonic()-start,flush=True)
    need(result.returncode==0 and not result.stderr.strip(),"JSON_BRIDGE_PROCESS_FAILED")
    lines=result.stdout.splitlines()
    non_json=[x for x in lines if not x.startswith("{")]
    need(len(non_json)==2 and all(re.fullmatch(r"'(?:runCases|main)' (?:does not depend on any axioms|depends on axioms: \[[^\]]*\])",x) for x in non_json),
        "JSON_BRIDGE_UNEXPECTED_OUTPUT")
    outputs=[b.parse(x) for x in lines if x.startswith("{")]
    need(len(outputs)==len(cases),"JSON_BRIDGE_OUTPUT_COUNT")
    for case,out in zip(cases,outputs):
        need(set(out)=={"status","reason","claims",*BOUNDARY},"JSON_OUTPUT_SCHEMA")
        need(out["status"]==case["expected_status"] and all(out[k] is v for k,v in BOUNDARY.items()),
            "JSON_STATUS_OR_AUTHORITY:"+case["name"]+":"+str(out.get("reason")))
        need(type(out["reason"]) is str and bool(out["reason"])==(out["status"]=="HOLD"),"JSON_REASON")
        need(canonical(out["claims"])==canonical(case["expected_rows"]),"JSON_VALUE_MISMATCH:"+case["name"])
        need(sha((folder/case["file"]).read_bytes())==case["raw_sha256"],"CASE_DRIFT")
        print("VERIFYOS_V016_CASE",case["name"],out["status"],
              sum(x["value"] is not None for x in out["claims"]),flush=True)
    return outputs


def summary(cases,outputs):
    return [dict(name=x["name"],mode=x["mode"],status=y["status"],claims=y["claims"]) for x,y in zip(cases,outputs)]


def direct(out):
    src=sources()
    out.mkdir(parents=True,exist_ok=False)
    project=out/"project"; project.mkdir()
    (project/"lean-toolchain").write_text(m.PIN+"\n")
    (project/"lakefile.toml").write_text('name = "VerifyOSJsonProbe"\nversion = "0.1.0"\ndefaultTargets = ["JsonProjection"]\n'+
        ''.join('\n[[lean_lib]]\nname = "'+x+'"\n' for x in MODULES[:-1]))
    audits={name:compile_module(project,name,raw,ns,out) for name,raw,ns in zip(MODULES,src,NAMESPACES)}
    cases=construct_cases(out/"cases")
    outputs=run_cases(project,out/"cases",cases,out/"json-execution.log")
    save(out/"outputs.json",outputs)
    stable=summary(cases,outputs)
    need(sources()==src and all((project/(name+".lean")).read_bytes()==raw for name,raw in zip(MODULES,src)),"SOURCE_DRIFT")
    receipt=dict(schema="kuuos.verifyos.json-projection.v0.16.direct",checkout_sha=os.environ.get("GITHUB_SHA"),
        pinned_blobs=PINS,modules=audits,cases=len(cases),manifest_sha256=sha(canonical(cases)),
        outputs_sha256=sha(canonical(outputs)),summary_sha256=sha(canonical(stable)),
        claim_value_comparisons=len(cases)*len(t.ORDER),**BOUNDARY)
    save(out/"direct.json",receipt)
    print("VERIFYOS_V016_DIRECT",json.dumps(receipt,sort_keys=True),flush=True)
    return receipt


def mcp_audit(out):
    src=sources(); project=out/"project"; receipt=load(out/"direct.json")
    need(all((project/(name+".lean")).read_bytes()==raw for name,raw in zip(MODULES,src)),"MCP_SOURCE_MISMATCH")
    _,theorems=inventory(src[2])
    cmd=["uvx","--from","lean-lsp-mcp=="+m.mcp.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=m.mcp.server_version(cmd[:-2],project)
    client=m.mcp.MCPClient(cmd,cwd=project,env={"LEAN_PROJECT_PATH":str(project),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":m.mcp.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows={}
    try:
        client.request("initialize",{"protocolVersion":m.mcp.PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"VerifyOS JSON projection","version":"0.16"}})
        client.notify("notifications/initialized")
        need({"lean_diagnostic_messages","lean_verify"}<=set(m.mcp.tool_map(client.request("tools/list"))),"MCP_TOOLS")
        response=m.mcp.call_tool(client,"lean_diagnostic_messages",{"file_path":"JsonProjection.lean","timeout_s":180})
        save(out/"mcp-diagnostics.json",response)
        check_diag(response)
        for i,name in enumerate(theorems):
            full=NS+name
            response=m.mcp.call_tool(client,"lean_verify",{"file_path":"JsonProjection.lean","theorem_name":full,"scan_source":False})
            save(out/f"mcp-verify-{i}.json",response)
            result=m.structured(response)
            axioms=normalize(result.get("axioms"))
            need(result.get("warnings")==[] and axioms==receipt["modules"]["JsonProjection"]["axioms"][full],"MCP_AXIOM_MISMATCH:"+full)
            rows[full]=axioms
            print("VERIFYOS_V016_MCP_AUDIT",full,json.dumps(axioms),flush=True)
    finally:
        client.close()
    need(sources()==src and all((project/(name+".lean")).read_bytes()==raw for name,raw in zip(MODULES,src)),"MCP_SOURCE_DRIFT")
    mp=dict(status="REAL_LEAN_MCP_CHECKED",direct_sha256=sha(canonical(receipt)),source_blob=PINS[SOURCE],
        theorems=rows,mcp_version=version)
    save(out/"mcp.json",mp)
    print("VERIFYOS_V016_MCP",json.dumps(mp,sort_keys=True),flush=True)


def check_diag(response):
    diag=m.structured(response)
    need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
        and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
        and not any(x.get("severity") in ("warning","error") for x in diag["items"]),"MCP_DIAGNOSTICS")


def independent(out,first):
    actual=direct(out); prior=load(first/"direct.json")
    need(all(actual[k]==prior[k] for k in ("schema","checkout_sha","pinned_blobs","modules","cases",
        "summary_sha256","claim_value_comparisons",*BOUNDARY)),"INDEPENDENT_SUMMARY_MISMATCH")
    src=sources()
    for name,raw in zip(MODULES,src):
        need((first/"project"/(name+".lean")).read_bytes()==raw,"INDEPENDENT_SOURCE_MISMATCH")
    old_cases=load(first/"cases/manifest.json"); old_outputs=load(first/"outputs.json")
    need(sha(canonical(old_cases))==prior["manifest_sha256"] and sha(canonical(old_outputs))==prior["outputs_sha256"]
        and sha(canonical(summary(old_cases,old_outputs)))==prior["summary_sha256"],"FIRST_RECEIPT_BINDING")
    replay=run_cases(out/"project",first/"cases",old_cases,out/"exact-first-replay.log")
    need(canonical(replay)==canonical(old_outputs),"EXACT_JSON_REPLAY_MISMATCH")
    mp=load(first/"mcp.json")
    _,theorems=inventory(src[2])
    expected={NS+x:actual["modules"]["JsonProjection"]["axioms"][NS+x] for x in theorems}
    need(mp["status"]=="REAL_LEAN_MCP_CHECKED" and mp["direct_sha256"]==sha(canonical(prior))
         and mp["source_blob"]==PINS[SOURCE] and mp["theorems"]==expected,"MCP_RECEIPT_BINDING")
    check_diag(load(first/"mcp-diagnostics.json"))
    for i,name in enumerate(theorems):
        row=m.structured(load(first/f"mcp-verify-{i}.json"))
        need(row["warnings"]==[] and normalize(row["axioms"])==expected[NS+name],"MCP_ROW")
    result=dict(status="INDEPENDENT_JSON_BRIDGE_MATCHED_ONLY",direct_sha256=sha(canonical(actual)),
        first_direct_sha256=sha(canonical(prior)),mcp_sha256=sha(canonical(mp)),source_blob=PINS[SOURCE],
        cases=actual["cases"],claim_value_comparisons=actual["claim_value_comparisons"],
        exact_first_input_replay=True,fresh_synthetic_pair_replayed=True,theorems=len(theorems),**BOUNDARY)
    save(out/"independent.json",result)
    print("VERIFYOS_V016_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--first",type=Path)
    args=ap.parse_args()
    if args.phase=="direct": direct(args.out)
    elif args.phase=="mcp": mcp_audit(args.out)
    else:
        need(args.first is not None,"FIRST_RECEIPT_REQUIRED")
        independent(args.out,args.first)


if __name__=="__main__":
    main()
