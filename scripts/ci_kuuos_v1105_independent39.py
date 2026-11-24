#!/usr/bin/env python3
"""Independent v1.105 exact-source kernel audit, 39 declarations.

This runner consumes the separately GREEN direct-Lean+39-axiom+MCP receipts
and the precise candidate bytes. No proof synthesis, PR adoption, merge, or
CodeAI memory promotion occurs here.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle
from scripts import ci_kuuos_v1105_codeai_r2_local as trial

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
BRANCH = "research/v1105-codeai-r2-independent-20261124"
SANDBOX_RUN = 45340609751
SANDBOX_HEAD = "d02bc8ecc45d67b0071ab09e5e4670480a351bed"
SANDBOX_JOB = 138263094926
WINNER_BLOB = "725b4d73037655576d495e32a6e202cd1affaf15"
WINNER_SHA256 = "98c9e8e6567d6bc64efd1bf82ead0fdd578cc1d838d1e0dfe8a689121e3ab4eb"
ORIGINAL_BLOB = "fb4d15a3467df69b8d2ba14276c2f4da6a1670d5"
V104_BLOB = "5c911aaeb9a21baff57f6af8c8655309af47d027"
V103_SHA = "dbec61c9798481709f2deda0028e84b7515f209e"
ENGINE_SHA = "5383253dbe9cda9cab90a410c2fd66ee6b9d6f41"

SOURCE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105.lean"
V104 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
V103 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
RESEARCH = ROOT / "research/codeai/v1105/r2/A-explicit-nat.lean"
SELECTED = Path("/tmp/kuuos-v1105-independent-selected")
LOCAL = Path("/tmp/kuuos-v1105-independent-local")
OUT = Path("/tmp/kuuos-v1105-independent-proof")
STAGING = ROOT / "formal/KUOS/.v1105-independent-kernel"
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105"
AXIOM_LOG = Path("/tmp/kuuos-v1105-independent-axioms.log")
OLEAN = Path("/tmp/kuuos-v1105-independent-selected.olean")
STANDARD = {"propext","Classical.choice","Quot.sound"}

def require(ok, why):
    if not ok:
        raise RuntimeError("V1105_INDEPENDENT_HOLD:" + why)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def check_blob(path, sha):
    require(path.exists() and path.is_file() and not path.is_symlink()
            and cycle.git_blob(path.read_bytes()) == sha,
            "SOURCE_BLOB_MISMATCH:" + str(path))

def one_file(root, name):
    require(root.is_dir(), "ARTIFACT_DIRECTORY_MISSING:" + str(root))
    files = [p for p in root.rglob(name) if p.is_file() and not p.is_symlink()]
    require(len(files) == 1, "EXPECTED_EXACT_ONE:" + name)
    return files[0]

def github_get(endpoint):
    token = os.getenv("GITHUB_TOKEN", "")
    require(bool(token),"GITHUB_TOKEN_NEEDED_READ_ONLY")
    req = Request("https://api.github.com/repos/" + REPO + endpoint,
        headers={"Authorization":"Bearer " + token,
                 "Accept":"application/vnd.github+json",
                 "X-GitHub-Api-Version":"2022-11-28",
                 "User-Agent":"KuuOS-v1105-Independent39"})
    with urlopen(req,timeout=40) as response:
        return json.load(response)

def upstream():
    x=github_get("/actions/runs/" + str(SANDBOX_RUN))
    require(x.get("status") == "completed" and x.get("conclusion") == "success"
            and x.get("head_sha") == SANDBOX_HEAD
            and x.get("head_branch") == "research/v1105-codeai-r2-20261124"
            and x.get("run_attempt") == 1,
            "UPSTREAM_SANDBOX_SUCCESS_NOT_VERIFIED")
    js=github_get("/actions/runs/" + str(SANDBOX_RUN) + "/jobs?per_page=100").get("jobs",[])
    require(len(js)==1 and js[0].get("id")==SANDBOX_JOB
            and js[0].get("status")=="completed"
            and js[0].get("conclusion")=="success"
            and js[0].get("name")=="v1105-source-bound-local-only",
            "UPSTREAM_SANDBOX_JOB_NOT_EXACT")
    required={
        "Preflight exact source and CodeAI candidate Git blobs",
        "Build v1.104 exact predecessor only",
        "CodeAI direct Lean serial trials, 39 axiom audit and real MCP only after GREEN",
        "Export exact candidate only when local direct plus axioms and real MCP GREEN"}
    greens={s.get("name") for s in js[0].get("steps",[])
            if s.get("conclusion")=="success" and s.get("status")=="completed"}
    require(required<=greens,"REQUIRED_GREEN_STEPS_MISSING")
    artifacts=github_get("/actions/runs/" + str(SANDBOX_RUN) + "/artifacts?per_page=100").get("artifacts",[])
    for name,aid in {
      "kuuos-v1105-r2-local-green-selected-source":14896925164,
      "kuuos-v1105-r2-two-local-direct-receipts":14896291678,
    }.items():
        matching=[a for a in artifacts if a.get("name")==name and not a.get("expired")]
        require(len(matching)==1 and matching[0].get("id")==aid,
                "UPSTREAM_ARTIFACT_MISMATCH:"+name)
    return {"run":SANDBOX_RUN,"head":SANDBOX_HEAD,"job":SANDBOX_JOB}

def local_receipts(candidate):
    selected=json.loads(one_file(SELECTED,"selected.json").read_text())
    require(selected.get("name")=="A-explicit-nat" and
            selected.get("blob")==WINNER_BLOB and
            selected.get("source_head")==SANDBOX_HEAD and
            selected.get("original_blob")==ORIGINAL_BLOB and
            selected.get("v104_blob")==V104_BLOB and
            selected.get("public_names")==39 and
            selected.get("real_mcp")=="MCP_TYPED_LOCAL_GREEN" and
            selected.get("independent_ci_started") is False and
            selected.get("formal_pr_modified") is False,
            "SELECTED_LOCAL_GREEN_METADATA_MISMATCH")
    a=selected["axioms"]
    require(a["checked"]==39 and a["sorryAx"] is False and
            a["nonstandard"]==[] and not set(a["allowed"])-STANDARD,
            "SELECTED_39_AXIOMS_UNTRUSTED")
    rec=json.loads(one_file(LOCAL,"receipt.json").read_text())
    direct=rec.get("direct",{})
    audit=rec.get("audit",{})
    local=rec.get("axioms",{})
    require(rec.get("candidate")=="A-explicit-nat" and
            rec.get("candidate_blob")==WINNER_BLOB and
            rec.get("source_head")==SANDBOX_HEAD and
            rec.get("state")=="LOCAL_DIRECT_AND_39_AXIOMS_GREEN" and
            rec.get("original_blob")==ORIGINAL_BLOB and
            rec.get("predecessor_blob")==V104_BLOB and
            rec.get("formal_PR_3555_mutated") is False and
            rec.get("independent_ci_started") is False,
            "UPSTREAM_DIRECT_RECEIPT_MISMATCH")
    require(direct.get("direct_success") is True and
            direct.get("exit_code")==0 and direct.get("error_count")==0 and
            audit.get("direct_success") is True and
            audit.get("exit_code")==0 and audit.get("error_count")==0 and
            local.get("checked")==39 and local.get("sorryAx") is False and
            local.get("nonstandard")==[] and
            not set(local.get("allowed",[]))-STANDARD,
            "UPSTREAM_KERNEL_39_AXIOMS_NOT_GREEN")
    mcp=json.loads(one_file(LOCAL,"real-mcp-receipt.json").read_text())
    require(mcp.get("candidate_blob")==WINNER_BLOB and
            mcp.get("selected_candidate")=="A-explicit-nat" and
            mcp.get("status")=="MCP_TYPED_LOCAL_GREEN" and
            mcp.get("version")=="lean-lsp-mcp==0.30.0" and
            mcp.get("success") is True and mcp.get("errors")==0 and
            mcp.get("partial") is False and
            mcp.get("failed_dependencies")==[] and
            mcp.get("independent_ci_success") is False,
            "UPSTREAM_REAL_MCP_NOT_GREEN")
    summary=json.loads(one_file(LOCAL,"summary.json").read_text())
    require(summary.get("status")=="LOCAL_LEAN_39_AXIOMS_AND_REAL_MCP_GREEN" and
            summary.get("original_blob")==ORIGINAL_BLOB and
            summary.get("v104_blob")==V104_BLOB and
            summary.get("independent_ci_started") is False and
            summary.get("formal_pr_modified") is False and
            len(summary.get("trials",[]))==1 and
            summary["trials"][0].get("candidate_blob")==WINNER_BLOB,
            "SOURCE_BOUND_SUMMARY_NOT_EXACT")
    return {"local_axioms":local,
            "mcp_receipt_sha256":sha256(one_file(LOCAL,"real-mcp-receipt.json").read_bytes()),
            "summary_sha256":sha256(one_file(LOCAL,"summary.json").read_bytes())}

def prepare():
    require(os.environ.get("GITHUB_ACTIONS")=="true" and
            os.environ.get("GITHUB_REF_NAME")==BRANCH,
            "WRONG_INDEPENDENT_BRANCH")
    up=upstream()
    check_blob(SOURCE,ORIGINAL_BLOB)
    check_blob(V104,V104_BLOB)
    check_blob(V103,V103_SHA)
    check_blob(RESEARCH,WINNER_BLOB)
    check_blob(ROOT / "scripts/kuuos_sandbox_lean_cycle_v1.py",ENGINE_SHA)
    require(cycle.require_pins(ROOT,verify_binaries=False)=={
        "lean_toolchain":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_sha":"5450b53e5ddc75d46418fabb605edbf36bd0beb6"},
        "LEAN_MATHLIB_PIN_MISMATCH")
    b=one_file(SELECTED,"selected.lean").read_bytes()
    require(cycle.git_blob(b)==WINNER_BLOB and
            sha256(b)==WINNER_SHA256 and
            b==RESEARCH.read_bytes(),
            "UPSTREAM_GREEN_BYTES_CHANGED")
    contract=trial.contract(SOURCE.read_text(),b.decode("utf-8"))
    require(contract["inline_where_structure_fields_exact"] is True and
            len(contract["public_declarations"])==39 and
            contract["import_additions"]=={},
            "PUBLIC_NAMES_AND_STRUCT_FIELDS_NOT_EXACT")
    local=local_receipts(b)
    require(not STAGING.exists() and not OUT.exists() and not OLEAN.exists(),
            "REUSED_INDEPENDENT_OUTPUT_PATH")
    STAGING.mkdir(parents=True)
    (STAGING / "Selected.lean").write_bytes(b)
    (STAGING / "AxiomAudit.lean").write_text(
        b.decode("utf-8")+"\n" +
        "\n".join("#print axioms "+NAMESPACE+"."+n for n in contract["public_declarations"]) + "\n")
    OUT.mkdir()
    x={
        "schema":"kuuos-v1105-independent39-source-exact-v1",
        "independent_head":os.environ["GITHUB_SHA"],
        "source":up,"source_git_blob":WINNER_BLOB,"source_sha256":WINNER_SHA256,
        "original":ORIGINAL_BLOB,"v104":V104_BLOB,"v103":V103_SHA,
        "public_declarations":contract["public_declarations"],
        "source_contract":contract,"local":local,
        "independent_ci_success":False,"formal_pr_modified":False,"merged":False
    }
    (OUT/"prepared.json").write_text(json.dumps(x,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1105_INDEPENDENT_EXACT_BYTES_PREPARED",
          json.dumps({"blob":WINNER_BLOB,"sha256":WINNER_SHA256,
                      "names":39,"independent_CI_certified":False}),flush=True)

def complete():
    x=json.loads((OUT/"prepared.json").read_text())
    b=(STAGING/"Selected.lean").read_bytes()
    require(cycle.git_blob(b)==WINNER_BLOB and
            sha256(b)==WINNER_SHA256,"SOURCE_MUTATED_BETWEEN_KERNEL_PASSES")
    require(OLEAN.exists() and OLEAN.stat().st_size>0,
            "KERNEL_ARTIFACT_NOT_CREATED")
    require(AXIOM_LOG.is_file(),"AXIOM_LOG_MISSING")
    ax=cycle.audit_axioms(AXIOM_LOG.read_text(),
                           x["public_declarations"],NAMESPACE)
    require(ax["checked"]==39 and ax["sorryAx"] is False and
            ax["nonstandard"]==[] and not set(ax["allowed"])-STANDARD,
            "INDEPENDENT_39_AXIOMS_NOT_STANDARD")
    for path,blob in [(SOURCE,ORIGINAL_BLOB),(V104,V104_BLOB),
                      (V103,V103_SHA),(RESEARCH,WINNER_BLOB)]:
        check_blob(path,blob)
    receipt={
        "schema":"kuuos-v1105-independent39-source-exact-v1",
        "independent_runner_head":x["independent_head"],
        "independent_source_sha256":WINNER_SHA256,
        "candidate_blob":WINNER_BLOB,
        "source_run":SANDBOX_RUN,"source_head":SANDBOX_HEAD,
        "public_declarations":39,"independent_axioms":ax,
        "sorryAx":False,"warnings":0,"errors":0,
        "independent_ci_success":True,
        "formal_pr_3555_mutated":False,"merged":False,
        "authority":"SOURCE-EXACT INDEPENDENT KERNEL ONLY",
        "limit":"This is type-C cocycle completion for B²ℕ only, not pushout descent or global type-C RLP"
    }
    (OUT/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1105_INDEPENDENT_39_AXIOMS_GREEN",
          json.dumps({"blob":WINNER_BLOB,"checked":39,"axioms":ax,
                      "independent_ci_success":True},sort_keys=True),flush=True)

if __name__=="__main__":
    try:
        require(len(sys.argv)==2 and sys.argv[1] in {"prepare","complete"},
                "PREPARE_OR_COMPLETE_REQUIRED")
        (prepare if sys.argv[1]=="prepare" else complete)()
    except Exception as e:
        OUT.mkdir(exist_ok=True,parents=True)
        (OUT/"obstruction.txt").write_text(type(e).__name__+": "+str(e)+"\n")
        print("KUUOS_V1105_INDEPENDENT_HOLD",type(e).__name__,str(e),file=sys.stderr)
        raise SystemExit(2)
