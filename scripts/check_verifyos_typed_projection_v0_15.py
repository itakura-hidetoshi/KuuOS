#!/usr/bin/env python3
"""Exact-source core Lean + differential projection fixtures + actual MCP."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
from scripts import check_verifyos_method_sound_coverage_v0_14 as prior
from runtime import kuuos_verifyos_claim_evidence_binding_v0_3 as c
from runtime import kuuos_verifyos_question_claim_contract_v0_4 as q
from runtime import kuuos_verifyos_diverse_ledger_audit_v0_13 as d
import test_kuuos_verifyos_diverse_ledger_audit_v0_13 as fixture

b = c.b
NS = "KUOS.VerifyOS.TypedProjectionV0_15."
FIXNS = "KUOS.VerifyOS.TypedProjectionFixturesV0_15."
SOURCE = "scripts/lean_probes/verifyos_typed_projection_v0_15.lean"
SOURCE_BLOB = "93d96c900ad40edebed74da41a6dcc916ae04c7d"
PINNED = {
    SOURCE: SOURCE_BLOB,
    "scripts/lean_probes/verifyos_method_sound_coverage_v0_14.lean": "b11ce505cb5f0d13fc812474299e5b0b96a50b87",
    "scripts/check_verifyos_method_sound_coverage_v0_14.py": "ccc6291731924fcd194a6e7cb41e5f23d503af78",
    "runtime/kuuos_verifyos_claim_evidence_binding_v0_3.py": "001d89ed1d9395c9d7a72595fe7e1a60716c4ecd",
    "runtime/kuuos_verifyos_question_claim_contract_v0_4.py": "b7376966a5ef4a27f156c5732de5498df267ee96",
    "runtime/kuuos_verifyos_diverse_ledger_audit_v0_13.py": "a0e357f3eda8edd58ea7a1a9facf45849cbaaa7b",
    "tests/test_kuuos_verifyos_diverse_ledger_audit_v0_13.py": "917354921f7bc76448e6d07be0d31321b15721d6",
}
FIELDS = {
    "integrity_status": (0, "stdout", ("status",), "status"),
    "scope_status": (1, "stdout", ("status",), "status"),
    "integrity_exit_code": (0, "process", ("exit_code",), "zero"),
    "scope_exit_code": (1, "process", ("exit_code",), "zero"),
    "snapshot_seq": (0, "stdout", ("seq",), "nat"),
    "snapshot_tip": (0, "stdout", ("tip_sha256",), "digest"),
    "rule_count": (0, "stdout", ("rule_count",), "nat"),
    "withdrawn_count": (0, "stdout", ("withdrawn_count",), "nat"),
    "obstruction_count": (0, "stdout", ("obstruction_count",), "nat"),
    "research_certificate_count": (0, "stdout", ("research_certificate_count",), "nat"),
    "scope_candidate_count": (1, "stdout", ("reviews", "candidate"), "nat"),
    "scope_held_count": (1, "stdout", ("reviews", "held"), "nat"),
    "scope_no_use_count": (1, "stdout", ("reviews", "no_use"), "nat"),
}
UNSUPPORTED = ("action_permission", "current_tip", "external_truth", "lean_proof", "new_context_validity")
ORDER = tuple(FIELDS) + UNSUPPORTED
need, blob, sha, canonical, save, load, normalize = prior.need, prior.blob, prior.sha, prior.canonical, prior.save, prior.load, prior.normalize


def sources():
    for path, expected in PINNED.items():
        need(blob((ROOT / path).read_bytes()) == expected, "PINNED_BLOB:" + path)
    need(c.FIELDS == FIELDS and set(c.UNSUPPORTED) == set(UNSUPPORTED) and tuple(q.ORDER) == ORDER, "CLAIM_REGISTRY_DRIFT")
    return prior.exact_source(), (ROOT / SOURCE).read_bytes()


def inventory(raw):
    text = raw.decode("utf-8")
    declarations = re.findall(r"(?m)^(?:inductive|structure|def|theorem) (\w+)", text)
    theorems = re.findall(r"(?m)^theorem (\w+)", text)
    need(declarations == re.findall(r"(?m)^#print axioms (\w+)$", text), "AXIOM_INVENTORY")
    need(len(set(declarations)) == len(declarations), "DUPLICATE_DECLARATION")
    need(not re.search(r"\b(?:sorry|admit|axiom|unsafe|native_decide)\b",
        "\n".join(line for line in text.splitlines() if not line.startswith("#print axioms"))), "FORBIDDEN_PROOF_TOKEN")
    return declarations, theorems


def value(raw):
    if type(raw) is int and raw >= 0:
        return "some (.nat " + str(raw) + ")"
    if type(raw) is str:
        need(all(32 <= ord(x) <= 126 for x in raw), "FIXTURE_ASCII_ONLY")
        return "some (.text " + json.dumps(raw) + ")"
    # Missing, Boolean, negative, floating, object and array values have no
    # representation in the admitted Nat/String view; they project to HOLD.
    return "none"


def raw_field(receipt, claim):
    if claim not in FIELDS:
        return None
    i, source, path, _ = FIELDS[claim]
    try:
        record = receipt["processes"][i]
        node = b.parse(record["stdout"]) if source == "stdout" else record
        for key in path:
            node = node[key]
        return node
    except c.ERRORS:
        return None


def fixture_source():
    test = fixture.PairTests("test_real_pair_and_diverse_match")
    try:
        root, args = test.pair("correct")
        result = d.verify_diverse(root, **args)
        need(result["status"] == "DIVERSE_FROZEN_PROFILE_AGREEMENT_ONLY", "SYNTHETIC_SIGNED_PAIR_NOT_ADMITTED")
        receipt = c.p.strict(args["primary_raw"])["receipt"]
        request = args["request"]
        binding = sha(canonical(args["context"]))
        pub = result["pair"]["primary"]
        real_rows = pub["claims"]
        need([x["claim_id"] for x in real_rows] == list(ORDER), "SIGNED_FIXTURE_COVERAGE")
        need(sum(x["status"] == "OBSERVED_IN_ADMITTED_RECEIPT" for x in real_rows) == 13, "SIGNED_FIXTURE_COUNT")
        # Only value projections, not synthetic raw evidence or random keys, enter Lean.
        projected = [c.project(x, receipt, request, pub) for x in ORDER]
        need(projected == real_rows, "SIGNED_FIXTURE_PROJECTION_MISMATCH")
        cases = [("signed_pair", receipt, request, True, True)]
        def mutate(name, i, updates=None, remove=(), exit_code=None, tip=None):
            new = copy.deepcopy(receipt)
            req = dict(request)
            rec = new["processes"][i]
            payload = b.parse(rec["stdout"])
            for key in remove:
                payload.pop(key, None)
            payload.update(updates or {})
            rec["stdout"] = canonical(payload).decode()
            if exit_code is not None:
                rec["exit_code"] = exit_code
            if tip is not None:
                req["tip"] = tip
            cases.append((name,new,req,True,True))
        mutate("wrong_integrity_status", 0, {"status":"PASS_SCOPE_RECORDS_ONLY"})
        mutate("wrong_scope_status", 1, {"status":"PASS_INTEGRITY_ONLY"})
        mutate("nonzero_exit", 0, exit_code=7)
        mutate("nonzero_scope_exit", 1, exit_code=3)
        mutate("bool_not_nat", 0, {"rule_count":True,"withdrawn_count":False})
        mutate("negative_nat", 0, {"obstruction_count":-1})
        mutate("float_not_nat", 0, {"research_certificate_count":2.5})
        mutate("text_not_nat", 0, {"seq":"1","rule_count":"10"})
        mutate("missing_fields", 0, remove=("rule_count","withdrawn_count","seq"))
        mutate("invalid_reviews", 1, {"reviews":{"candidate":-1,"held":True,"no_use":"0"}})
        mutate("missing_reviews", 1, remove=("reviews",))
        mutate("different_tip", 0, {"tip_sha256":"f"*64})
        mutate("uppercase_tip", 0, {"tip_sha256":"A"*64}, tip="A"*64)
        mutate("short_tip", 0, {"tip_sha256":"a"*63}, tip="a"*63)
        mutate("bad_hex_tip", 0, {"tip_sha256":"g"*64}, tip="g"*64)
        cases.extend([("wrong_context",receipt,request,True,False),("unadmitted",receipt,request,False,True)])
        lines = ["import TypedProjection", "", "namespace "+FIXNS[:-1],
                 "open "+NS[:-1], "set_option maxRecDepth 4096", "set_option maxHeartbeats 2000000", "",
                 "def allClaims : List Claim := ["+", ".join("."+x for x in ORDER)+"]",
                 "def observableClaims : List Claim := ["+", ".join("."+x for x in FIELDS)+"]", ""]
        summary = []
        decls = ["allClaims","observableClaims"]
        for i,(name,rec,req,admitted,same_context) in enumerate(cases):
            tag = "case_"+str(i)
            ctx = tag+"_ctx"; view = tag+"_receipt"
            expected = [c.project(x,rec,req,pub) for x in ORDER] if admitted and same_context else [c.held(x,"UNADMITTED_OR_WRONG_CONTEXT") for x in ORDER]
            # c.project is deliberately invoked on mutated typed views only;
            # those cases are not claimed to be genuine admitted bundles.
            lines.append("def "+ctx+" : SnapshotContext := "+ "⟨"+json.dumps(binding)+", "+json.dumps(req["tip"])+"⟩")
            lines.extend(["def "+view+" : ReceiptView where",
                "  admitted := "+str(admitted).lower(),
                "  context := "+(ctx if same_context else "⟨\"different context\", "+json.dumps(req["tip"])+"⟩"),
                "  raw := fun"])
            for x in FIELDS:
                lines.append("    | ."+x+" => "+value(raw_field(rec,x)))
            # Even forged supplied values in unsupported positions remain HOLD.
            lines.append("    | _ => some (.nat 1)")
            rows = ["(."+x+", "+("("+value(y["value"])+")" if y["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" else "none")+")" for x,y in zip(ORDER,expected)]
            lines.extend(["theorem "+tag+"_rows : rows "+view+" "+ctx+" allClaims =",
                "    ["+",\n     ".join(rows)+"] := by decide",
                "theorem "+tag+"_all : complete "+view+" "+ctx+" allClaims = false := by decide"])
            complete = all(y["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" for y in expected[:len(FIELDS)])
            lines.append("theorem "+tag+"_observable : complete "+view+" "+ctx+" observableClaims = "+str(complete).lower()+" := by decide")
            decls.extend([ctx,view,tag+"_rows",tag+"_all",tag+"_observable"])
            summary.append({"case":name,"observed":sum(y["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" for y in expected),
                            "held":sum(y["status"]=="HOLD" for y in expected),"observable_complete":complete,
                            "runtime_projection_comparison":admitted and same_context})
        lines.extend(["",*("#print axioms "+x for x in decls),"","end "+FIXNS[:-1],""])
        return "\n".join(lines).encode(), summary
    finally:
        test.doCleanups()


def run_lean(project, name, raw, namespace, out):
    decls, theorems = inventory(raw)
    version = subprocess.run(["lean","--version"],check=True,capture_output=True,text=True).stdout.strip()
    need("version 4.30.0-rc2" in version,"LEAN_VERSION")
    start = time.monotonic()
    result = subprocess.run(["lean","-DwarningAsError=true","-Dweak.sorryAsError=true",
        "-o", name+".olean",name+".lean"],cwd=project,
        env={**os.environ,"LEAN_PATH":str(project.resolve())},capture_output=True,text=True,timeout=180)
    log = result.stdout + "\n" + result.stderr
    (out/(name+".log")).write_text(log)
    print(log,flush=True)
    print("VERIFYOS_V015_LEAN_EXIT",name,result.returncode,"seconds",time.monotonic()-start,flush=True)
    need(result.returncode==0 and (project/(name+".olean")).is_file(),"DIRECT_LEAN_FAILED:"+name)
    need(not re.search(r"\b(?:warning:|error:|sorryAx)\b",log),"LEAN_DIAGNOSTIC:"+name)
    pattern = r"'("+re.escape(namespace)+r"\w+)' (?:does not depend on any axioms|depends on axioms: \[([^\]]*)\])"
    found = re.findall(pattern,log)
    need(len(found)==len(decls) and {x[0] for x in found}=={namespace+x for x in decls},"AXIOM_INVENTORY:"+name)
    return {"source_sha256":sha(raw),"source_blob":blob(raw),"version":version,
            "declarations":len(decls),"theorems":len(theorems),
            "axioms":{n:normalize([x.strip() for x in a.split(",") if x.strip()]) for n,a in found}}


def direct(out):
    original, raw = sources()
    fixture_raw, summary = fixture_source()
    out.mkdir(parents=True,exist_ok=False)
    project = out/"project"; project.mkdir()
    (project/"lean-toolchain").write_text(prior.PIN+"\n")
    names = ("MethodSoundCoverage","TypedProjection","ProjectionFixtures")
    (project/"lakefile.toml").write_text('name = "VerifyOSProjectionProbe"\nversion = "0.1.0"\ndefaultTargets = ["TypedProjection"]\n'+''.join('\n[[lean_lib]]\nname = "'+x+'"\n' for x in names))
    audits = {}
    for name,source,ns in zip(names,(original,raw,fixture_raw),(prior.NS,NS,FIXNS)):
        (project/(name+".lean")).write_bytes(source)
        audits[name] = run_lean(project,name,source,ns,out)
        need((project/(name+".lean")).read_bytes()==source,"SOURCE_DRIFT")
    need(sources()==(original,raw),"INPUT_SOURCE_DRIFT")
    receipt = {"schema":"kuuos.verifyos.typed-projection.v0.15.direct",
        "checkout_sha":os.environ.get("GITHUB_SHA"),"pinned_blobs":PINNED,
        "modules":audits,"cases":summary,
        "runtime_projection_cases":sum(x["runtime_projection_comparison"] for x in summary),
        "claim_value_comparisons":len(ORDER)*sum(x["runtime_projection_comparison"] for x in summary),
        "conditional_projection_only":True,"complete_python_refinement_proved":False,
        "proof_authority":False,"action_authority":False}
    save(out/"direct.json",receipt)
    print("VERIFYOS_V015_DIRECT",json.dumps(receipt,sort_keys=True),flush=True)
    return receipt


def mcp_audit(out):
    original,raw=sources(); project=out/"project"
    receipt=load(out/"direct.json")
    need((project/"MethodSoundCoverage.lean").read_bytes()==original and
         (project/"TypedProjection.lean").read_bytes()==raw and
         receipt["modules"]["TypedProjection"]["source_sha256"]==sha(raw),"MCP_SOURCE_MISMATCH")
    _,theorems=inventory(raw)
    cmd=["uvx","--from","lean-lsp-mcp=="+prior.mcp.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=prior.mcp.server_version(cmd[:-2],project)
    client=prior.mcp.MCPClient(cmd,cwd=project,env={"LEAN_PROJECT_PATH":str(project),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":prior.mcp.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows={}
    try:
        client.request("initialize",{"protocolVersion":prior.mcp.PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"VerifyOS typed projection","version":"0.15"}})
        client.notify("notifications/initialized")
        need({"lean_diagnostic_messages","lean_verify"}<=set(prior.mcp.tool_map(client.request("tools/list"))),"MCP_TOOLS")
        response=prior.mcp.call_tool(client,"lean_diagnostic_messages",{"file_path":"TypedProjection.lean","timeout_s":180})
        save(out/"mcp-diagnostics.json",response)
        diag=prior.structured(response)
        need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
             and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
             and not any(x.get("severity") in ("warning","error") for x in diag["items"]),"MCP_DIAGNOSTIC_FAILURE")
        for i,name in enumerate(theorems):
            full=NS+name
            response=prior.mcp.call_tool(client,"lean_verify",{"file_path":"TypedProjection.lean","theorem_name":full,"scan_source":False})
            save(out/f"mcp-verify-{i}.json",response)
            result=prior.structured(response)
            axioms=normalize(result.get("axioms"))
            need(result.get("warnings")==[] and axioms==receipt["modules"]["TypedProjection"]["axioms"][full],"MCP_AXIOM_MISMATCH:"+full)
            rows[full]=axioms
            print("VERIFYOS_V015_MCP_AUDIT",full,json.dumps(axioms),flush=True)
    finally:
        client.close()
    need((project/"TypedProjection.lean").read_bytes()==raw and sources()==(original,raw),"MCP_SOURCE_DRIFT")
    mp={"status":"REAL_LEAN_MCP_CHECKED","direct_sha256":sha(canonical(receipt)),
        "source_blob":SOURCE_BLOB,"source_sha256":sha(raw),"theorems":rows,"mcp_version":version}
    save(out/"mcp.json",mp)
    print("VERIFYOS_V015_MCP",json.dumps(mp,sort_keys=True),flush=True)


def independent(out,first):
    actual=direct(out); before=load(first/"direct.json")
    need(actual==before,"INDEPENDENT_RECEIPT_MISMATCH")
    for name in actual["modules"]:
        need((out/"project"/(name+".lean")).read_bytes()==(first/"project"/(name+".lean")).read_bytes(),"INDEPENDENT_SOURCE_MISMATCH")
    mp=load(first/"mcp.json")
    _,theorems=inventory((ROOT/SOURCE).read_bytes())
    expected={NS+x:actual["modules"]["TypedProjection"]["axioms"][NS+x] for x in theorems}
    need(mp["status"]=="REAL_LEAN_MCP_CHECKED" and mp["direct_sha256"]==sha(canonical(before))
         and mp["source_blob"]==SOURCE_BLOB and mp["source_sha256"]==actual["modules"]["TypedProjection"]["source_sha256"]
         and mp["theorems"]==expected,"INDEPENDENT_MCP_RECEIPT_MISMATCH")
    diag=prior.structured(load(first/"mcp-diagnostics.json"))
    need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and isinstance(diag["items"],list)
        and not any(x.get("severity") in ("warning","error") for x in diag["items"]),"INDEPENDENT_MCP_DIAGNOSTICS")
    for i,name in enumerate(theorems):
        row=prior.structured(load(first/f"mcp-verify-{i}.json"))
        need(row["warnings"]==[] and normalize(row["axioms"])==expected[NS+name],"INDEPENDENT_MCP_ROW")
    result={"status":"INDEPENDENT_TYPED_PROJECTION_MATCHED_ONLY","direct_sha256":sha(canonical(actual)),
        "mcp_sha256":sha(canonical(mp)),"source_blob":SOURCE_BLOB,"theorems":len(theorems),
        "claim_value_comparisons":actual["claim_value_comparisons"],"cases":len(actual["cases"]),
        "complete_python_refinement_proved":False,"proof_authority":False,"action_authority":False}
    save(out/"independent.json",result)
    print("VERIFYOS_V015_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase",choices=("fixtures","direct","mcp","independent"),required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--first",type=Path)
    args=ap.parse_args()
    if args.phase=="fixtures":
        sources()
        raw,summary=fixture_source()
        args.out.mkdir(parents=True,exist_ok=False)
        (args.out/"ProjectionFixtures.lean").write_bytes(raw)
        save(args.out/"fixture-summary.json",summary)
        print("VERIFYOS_V015_FIXTURE_CANDIDATES",json.dumps(summary,sort_keys=True))
    elif args.phase=="direct": direct(args.out)
    elif args.phase=="mcp": mcp_audit(args.out)
    else:
        need(args.first is not None,"SANDBOX_RECEIPT_REQUIRED")
        independent(args.out,args.first)


if __name__=="__main__":
    main()
