#!/usr/bin/env python3
"""KuuOS v1.121 induced-scaled Type-A endpoint RLP; source-bound CodeAI.

Actual v1.121 Type-C terminal right lifting property is certified separately
at exact source blob 24cc915ad7...; do not use the historical failing v1.106
import closure. Generate three source-distinct proof candidates using the
actual v1.77 Leibniz stability and v1.59 inclusion. Build every candidate in
pinned Lean before actual Lean MCP; MCP success must be followed by another
direct Lean run. No producer proof authority, no Git write, no adoption here.
"""
from __future__ import annotations
import json,re
from pathlib import Path
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

ROOT=base.ROOT
TARGET=base.TARGET
OUT=Path("/tmp/kuuos-v121-endpoint-codeai-on-certified-terminal-v1")
MCP=Path("/tmp/kuuos-v121-endpoint-real-mcp-on-certified-terminal-v1")
TERMINAL_BLOB="24cc915ad7693a7083ccd19c2614cb5339778381"
COCYCLE_BLOB="90672c999cb7f76c448d8932875900ee871bf80f"
MEMORY=ROOT/"memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v121_terminal_round4_success_v1.json"
CERT_RUN=43862315102
CERT_HEAD="a60846ccdf65becf08cd1492515cf6536521bf52"
EXPECTED={
  **base.DEPENDENCIES,
  "formal/KUOS/DependentOriginationDoubleDeloopingTypeCTerminalRLPPinnedV1_121.lean":TERMINAL_BLOB
}

def check(cond: bool, msg: str) -> None:
    if not cond: raise RuntimeError("KUUOS_V121_ENDPOINT_FAIL_CLOSED: "+msg)

def main() -> int:
    head,tree=base.event_source()
    require_pins(ROOT)
    check(not (ROOT/TARGET).exists(),"refuse overwrite of actual Lean proof")
    check(not OUT.exists() and not MCP.exists(),"stale candidate workspace")
    for p,sha in EXPECTED.items():
        check(base.blob((ROOT/p).read_bytes())==sha,
              "fixed imported source blob changed: "+p)
    recorded=read_observation_seed(MEMORY)
    check(len(recorded)==3,"round4 success provenance missing")
    check(any(r["variant"]=="round4-native-direct" and
         r["candidate_blob"]==TERMINAL_BLOB and
         r["producer_run"]==43860696324 and
         r["outcome"]=="DIRECT_LEAN_SUCCESS" for r in recorded),
         "validated terminal candidate provenance changed")
    token=__import__("os").environ["GITHUB_TOKEN"]
    certified=base.github("actions/runs/"+str(CERT_RUN),token)
    check(certified["head_sha"]==CERT_HEAD
          and certified["status"]=="completed"
          and certified["conclusion"]=="success",
          "independent terminal proof CI not certified at pinned source")
    source_ref=base.github("git/commits/"+head,token)
    merge_ref=base.github("git/ref/pull/3562/merge",token)
    merge_commit=base.github("git/commits/"+merge_ref["object"]["sha"],token)
    check(source_ref["tree"]["sha"]==tree==merge_commit["tree"]["sha"],
          "source/test-merge Git trees not equal")
    versions=base.sources()
    check(len(versions)==3 and
          all("natDoubleDelooping_typeA_inducedEndpoint_actualExtension" in s
              and "natDoubleDelooping_typeA_inducedEndpoint_chosenLift_fac" in s
              and "natDoubleDelooping_standardABC_generators_rlp" in s
              for s in versions.values()),"actual lift and cocycle dependency lost")
    base.OUT=OUT; base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    try:
        for name,src in versions.items():
            (OUT/(name+".lean")).write_text(src,encoding="utf-8")
            rows.append(base.direct(name,src))
        receipt=base.mcp_verify(head,rows,versions)
    finally:
        (ROOT/TARGET).unlink(missing_ok=True)
    check(not (ROOT/TARGET).exists(),"source mutated after direct Lean")
    MCP.mkdir(parents=True,exist_ok=True)
    receipt["source_restored"]=True
    (MCP/"receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    (OUT/"portfolio.json").write_text(json.dumps({
      "source_head":head,"source_tree":tree,
      "certified_terminal_blob":TERMINAL_BLOB,
      "certified_terminal_run":CERT_RUN,
      "candidate_count":len(rows),"candidates":rows,
      "source_restored":True,"git_write_performed":False,
      "independent_ci_certified":False
    },sort_keys=True,indent=2)+"\n")
    print("KUUOS_V121_ENDPOINT_CODEAI "+json.dumps({
      "head":head,"source_tree":tree,
      "tested":len(rows),
      "direct_green":[r["variant"] for r in rows if r["status"]=="SUCCESS"],
      "errors":{r["variant"]:r.get("error_count") for r in rows},
      "selected":receipt.get("selected"),
      "real_mcp_status":receipt["status"],
      "source_restored":True
    },sort_keys=True))
    return 0 if receipt["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
