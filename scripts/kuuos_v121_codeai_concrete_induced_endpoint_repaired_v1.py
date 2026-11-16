#!/usr/bin/env python3
"""CodeAI certified v1.120 based v1.121: concrete B²Nat induced endpoint RLP via certified
standard A/B/C geometry. Three source-distinct Lean candidates, pinned direct
Lean first, real Lean MCP only for green candidate, second direct Lean.
No Git writes, no source promotion, no independent certification from producer.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, require_pins, call_tool, tool_map,
)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import (
    require_semantics, FORBIDDEN_NEW, DISABLED_MCP_TOOLS,
)

ROOT=Path(__file__).resolve().parent.parent
REPO="itakura-hidetoshi/KuuOS"
BASE="validation/kuuos-v120-induced-admission-recovery-20261116"
BASE_SHA="7c64a89b81681f997483d0873887df2f700d1244"
BRANCH="validation/kuuos-v121-induced-endpoint-on-certified-v120-20261116"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingInducedEndpointRLPV1_121.lean"
DEPENDENCIES={
    "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFaceValueBridgeV1_121.lean":"aba1d6010ab557d9836c349743b63858e9362419",
    "formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionPinnedV1_121.lean":"6b1142889bbebaad76a8c143a323c9c272e45076",
    "formal/KUOS/DependentOriginationDoubleDeloopingTypeCTerminalRLPPinnedV1_121.lean":"c81f3765791521e6e151b7f56a3b822cb81e8752",
    "formal/KUOS/DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.lean":"6e06ac88c2b1cdadcb0d0f7496281892a3549c64",
    "formal/KUOS/DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77.lean":"e7d422b89b4a4fa5180790b0c5d49c51b7239786",
    "formal/KUOS/DependentOriginationStandardABCLeibnizCellularComparisonV1_59.lean":"2b852bcd457831d25d50e8ed9dd3ac6a44f6f85e",
    "formal/KUOS/DependentOriginationStandardTypeAEndpointPushoutProductV1_50.lean":"1f24c5e7b30d1392ccd16c8b7b3ed7387b7d72a9",
}
OUT=Path("/tmp/kuuos-v121-codeai-repaired")
MCP=Path("/tmp/kuuos-v121-real-mcp-repaired")
INTRO="""import KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
import KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPPinnedV1_121

namespace KUOS.DependentOriginationDoubleDeloopingInducedEndpointRLPV1_121

open CategoryTheory
open CategoryTheory.Category
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106

noncomputable section

/-!
# Concrete induced-scaled type-(A) endpoint RLP for B²ℕ.

Pinned research source already proves:
- genuine A/B/C terminal right orthogonality for the concrete B²ℕ
  (pinned v1.106 bridge using actual type-C pushout cocycle witnesses);
- type-(A) endpoint prism cellularity/stability for the exact standard
  A/B/C presentation (v1.77).
This file glues the *same morphism properties* to a concrete lifting
statement for the induced-scaled endpoint map of v1.50.

The v1.118 counterexample involves the MINIMALLY scaled attachment,
which is a distinct morphism; nothing here denies that obstruction.
-/

/-- A concrete, unconditional terminal right lifting certificate for every
standard type-(A) *induced-scaled* endpoint pushout-product. -/
theorem natDoubleDelooping_typeA_inducedEndpoint_rlp
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    HasLiftingProperty
      (standardTypeAEndpointPushoutProductHom g)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
"""
AFTER="""

/-- Every actual admissible top arrow into the concrete B²ℕ Duskin nerve
has a scaled cylinder extension respecting the induced endpoint attachment. -/
theorem natDoubleDelooping_typeA_inducedEndpoint_actualExtension
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (f : standardTypeAEndpointPushoutProductSource g ⟶
      natDoubleDeloopingScaledDuskin) :
    ∃ l : scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶
        natDoubleDeloopingScaledDuskin,
      standardTypeAEndpointPushoutProductHom g ≫ l = f := by
  exact (ScaledSSet.hasLiftingProperty_toPoint_iff
    (standardTypeAEndpointPushoutProductHom g)).mp
      (natDoubleDelooping_typeA_inducedEndpoint_rlp g) f

/-- A chosen literal scaled cylinder extension from the preceding
fully proven existence theorem, with no forward endpoint RLP assumption. -/
noncomputable def natDoubleDelooping_typeA_inducedEndpoint_chosenLift
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (f : standardTypeAEndpointPushoutProductSource g ⟶
      natDoubleDeloopingScaledDuskin) :
    scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶
      natDoubleDeloopingScaledDuskin :=
  Classical.choose
    (natDoubleDelooping_typeA_inducedEndpoint_actualExtension g f)

/-- The chosen extension commutes with the *induced-scaled* attachment
inclusion, for the original arbitrary admissible top arrow. -/
theorem natDoubleDelooping_typeA_inducedEndpoint_chosenLift_fac
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (f : standardTypeAEndpointPushoutProductSource g ⟶
      natDoubleDeloopingScaledDuskin) :
    standardTypeAEndpointPushoutProductHom g ≫
      natDoubleDelooping_typeA_inducedEndpoint_chosenLift g f = f := by
  exact Classical.choose_spec
    (natDoubleDelooping_typeA_inducedEndpoint_actualExtension g f)

#print axioms natDoubleDelooping_typeA_inducedEndpoint_rlp
#print axioms natDoubleDelooping_typeA_inducedEndpoint_actualExtension
#print axioms natDoubleDelooping_typeA_inducedEndpoint_chosenLift
#print axioms natDoubleDelooping_typeA_inducedEndpoint_chosenLift_fac

end

end KUOS.DependentOriginationDoubleDeloopingInducedEndpointRLPV1_121
"""

def blob(b: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def require(ok: bool, what: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V121_CODEAI_FAIL_CLOSED: "+what)

def github(path: str, token: str) -> dict:
    req=urllib.request.Request(
      "https://api.github.com/repos/"+REPO+"/"+path,
      headers={"Accept":"application/vnd.github+json",
        "Authorization":"Bearer "+token,"User-Agent":"KuuOS-v121-CodeAI-main"})
    with urllib.request.urlopen(req,timeout=45) as res:
        return json.load(res)

def event_source() -> tuple[str,str]:
    event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pr=event.get("pull_request") or {}
    h,b=pr.get("head") or {},pr.get("base") or {}
    require(event.get("repository",{}).get("full_name")==REPO
        and pr.get("draft") is True and pr.get("state")=="open"
        and h.get("ref")==BRANCH and b.get("ref")==BASE
        and b.get("sha")==BASE_SHA,"wrong exact v1.120 source lease")
    sha=h.get("sha")
    require(isinstance(sha,str) and re.fullmatch(r"[0-9a-f]{40}",sha) is not None,
            "missing HEAD")
    token=os.environ.get("GITHUB_TOKEN","")
    require(bool(token),"read-only GitHub source token required")
    actual=github("pulls/"+str(event["number"]),token)
    require((actual.get("head") or {}).get("sha")==sha
        and (actual.get("base") or {}).get("sha")==BASE_SHA
        and actual.get("draft") is True,"PR mutated while evaluating")
    commit=github("git/commits/"+sha,token)
    tree=(commit.get("tree") or {}).get("sha","")
    require(re.fullmatch(r"[0-9a-f]{40}",tree) is not None,"missing source Git tree")
    return sha,tree

PROOFS={
 "membership-explicit":"""  have hmem : standardGeneratedScaledAnodyneABC
      (standardTypeAEndpointPushoutProductHom g) :=
    (standardTypeAEndpointPushoutProducts_le_standardGenerated
      standardABCTypeAEndpointLeibnizStability_proved)
      _ (standardTypeAEndpointPushoutProductGenerator_mem g)
  exact hmem _ natDoubleDelooping_standardABC_generators_rlp""",
 "membership-apply":"""  have h : standardGeneratedScaledAnodyneABC
      (standardTypeAEndpointPushoutProductHom g) := by
    apply (standardTypeAEndpointPushoutProducts_le_standardGenerated
      standardABCTypeAEndpointLeibnizStability_proved)
    exact standardTypeAEndpointPushoutProductGenerator_mem g
  exact h _ natDoubleDelooping_standardABC_generators_rlp""",
 "membership-cellular":"""  have hcell := standardTypeAEndpointPushoutProducts_le_standardGenerated
      standardABCTypeAEndpointLeibnizCellularCertificateConstructed.toLeibnizStability
  exact (hcell _ (standardTypeAEndpointPushoutProductGenerator_mem g))
      _ natDoubleDelooping_standardABC_generators_rlp""",
}

def sources() -> dict[str,str]:
    versions={k:INTRO+v+AFTER for k,v in PROOFS.items()}
    require(len({blob(x.encode("utf-8")) for x in versions.values()})==3,
            "nonunique CodeAI candidates")
    for name,s in versions.items():
        require(s.count("\ntheorem ")==3 and s.count("\nnoncomputable def ")==1
            and s.count("#print axioms ")==4
            and FORBIDDEN_NEW.search(s) is None,
            "changed declaration inventory or forbidden Lean construct: "+name)
    return versions

def direct(name: str, code: str) -> dict:
    row={"variant":name,"candidate_blob":blob(code.encode()),
         "candidate_sha256":hashlib.sha256(code.encode()).hexdigest(),
         "status":"NO_DATA","error_count":None}
    try:
        (ROOT/TARGET).write_text(code,encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="v121-codeai-direct-") as d:
            olean=Path(d)/"candidate.olean"
            try:
                p=subprocess.run(["lake","env","lean",
                    "-DwarningAsError=true","-Dweak.sorryAsError=true",
                    "-o",str(olean),TARGET],
                    cwd=ROOT,capture_output=True,text=True,timeout=600)
                log=p.stdout+"\n"+p.stderr
                row["exit_code"]=p.returncode
                row["olean_exists"]=olean.is_file()
                row["status"]="SUCCESS" if p.returncode==0 and olean.is_file() and "sorryAx" not in log else "FAILURE"
            except subprocess.TimeoutExpired as ex:
                log=str(ex.stdout or "")+"\n"+str(ex.stderr or "")
                row["status"]="TIMEOUT"
                row["exit_code"]=None
                row["olean_exists"]=False
            row["errors"]=[l[:850] for l in log.splitlines() if "error:" in l or "error(" in l][:30]
            row["error_count"]=len(row["errors"])
            row["log_sha256"]=hashlib.sha256(log.encode()).hexdigest()
            (OUT/(name+".log")).write_text(log,encoding="utf-8")
            if row["status"]=="SUCCESS" and row["errors"]:
                row["status"]="FAILURE"
    finally:
        (ROOT/TARGET).unlink(missing_ok=True)
    print("KUUOS_V121_CODEAI_DIRECT "+json.dumps(row,sort_keys=True))
    return row

def mcp_verify(head: str, rows: list[dict], choices: dict[str,str]) -> dict:
    green=[x for x in rows if x.get("status")=="SUCCESS" and x.get("exit_code")==0
         and x.get("olean_exists") is True and x.get("error_count")==0]
    receipt={"source_head":head,"direct_green":[r["variant"] for r in green],
         "selected":None,"selected_blob":None,"mcp_success":False,
         "mcp_errors":None,"second_direct_success":False,
         "git_write_performed":False,"independent_ci_certified":False,
         "status":"DIRECT_LEAN_NO_GREEN"}
    MCP.mkdir(parents=True,exist_ok=False)
    client=None
    try:
        if not green:
            return receipt
        selected=green[0]
        code=choices[selected["variant"]]
        raw=code.encode("utf-8")
        require(blob(raw)==selected["candidate_blob"],"CodeAI candidate identity drift")
        (ROOT/TARGET).write_bytes(raw)
        receipt["selected"]=selected["variant"]
        client=MCPClient(
            ["uvx","--from","lean-lsp-mcp==0.30.0",
             "lean-lsp-mcp","--transport","stdio"],
            cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
                "LEAN_MCP_DISABLED_TOOLS":DISABLED_MCP_TOOLS,
                "LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
        client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,
            "capabilities":{},"clientInfo":{"name":"KuuOS CodeAI v1.121","version":"1"}})
        client.notify("notifications/initialized")
        listed=tool_map(client.request("tools/list"))
        require({"lean_diagnostic_messages","lean_goal","lean_multi_attempt"}.issubset(listed)
            and "lean_build" not in listed and "lean_run_code" not in listed,
            "Lean MCP tool surface drift")
        diag=call_tool(client,"lean_diagnostic_messages",{"file_path":TARGET,"timeout_s":120})
        obs=require_semantics(structured(diag),raw)
        receipt["mcp_success"]=obs.success and not obs.partial and not obs.errors
        receipt["mcp_errors"]=len(obs.errors)
        receipt["mcp_diagnostic_sha256"]=hashlib.sha256(json.dumps(
            obs.diagnostics,sort_keys=True).encode()).hexdigest()
        require(receipt["mcp_success"],"actual real Lean MCP diagnostics not green")
        client.close();client=None
        with tempfile.TemporaryDirectory(prefix="v121-second-") as d:
            olean=Path(d)/"candidate.olean"
            p=subprocess.run(["lake","env","lean",
                "-DwarningAsError=true","-Dweak.sorryAsError=true",
                "-o",str(olean),TARGET],
                cwd=ROOT,capture_output=True,text=True,timeout=600)
            log=p.stdout+"\n"+p.stderr
            (MCP/"second_direct.log").write_text(log,encoding="utf-8")
            receipt["second_direct_success"]=p.returncode==0 and olean.is_file()
            receipt["second_direct_exit"]=p.returncode
            receipt["second_direct_log_sha256"]=hashlib.sha256(log.encode()).hexdigest()
            require(receipt["second_direct_success"] and "sorryAx" not in log,
                    "MCP candidate failed second direct Lean")
        (MCP/"candidate.lean").write_bytes(raw)
        receipt["selected_blob"]=blob(raw)
        receipt["status"]="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI"
    except Exception as ex:
        receipt["status"]="MCP_OR_DIRECT_OBSTRUCTION"
        receipt["obstruction"]=type(ex).__name__+": "+str(ex)[:700]
    finally:
        if client is not None:
            try: client.close()
            except Exception as ex: receipt["close_obstruction"]=str(ex)[:150]
        (ROOT/TARGET).unlink(missing_ok=True)
    return receipt

def main() -> int:
    head,tree=event_source()
    require_pins(ROOT)
    require(not (ROOT/TARGET).exists(),"refuse to overwrite proof module")
    for p,expected in DEPENDENCIES.items():
        require(blob((ROOT/p).read_bytes())==expected,
                "fixed imported theorem source differs from pinned research source: "+p)
    versions=sources()
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    try:
        for name,code in versions.items():
            rows.append(direct(name,code))
        mcp=mcp_verify(head,rows,versions)
    finally:
        (ROOT/TARGET).unlink(missing_ok=True)
    require(not (ROOT/TARGET).exists(),"original package not restored")
    mcp["source_restored"]=True
    (MCP/"receipt.json").write_text(json.dumps(mcp,sort_keys=True,indent=2)+"\n")
    result={"source_head":head,"source_tree":tree,
        "base_certified_v120_head":BASE_SHA,
        "candidate_count":len(rows),"candidates":rows,
        "git_write_performed":False,"source_restored":True,
        "independent_ci_certified":False}
    (OUT/"portfolio.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V121_CODEAI_MCP "+json.dumps(mcp,sort_keys=True))
    print("KUUOS_V121_CODEAI_SUMMARY "+json.dumps({
        "tested":len(rows),"direct_green":sum(x["status"]=="SUCCESS" for x in rows),
        "selected":mcp.get("selected"),"status":mcp["status"]},sort_keys=True))
    return 0 if mcp["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
