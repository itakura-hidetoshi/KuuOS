#!/usr/bin/env python3
"""KuuOS CodeAI type-C terminal RLP round4: directly transport established
component equalities, avoiding invalid simp and absent rw matches. No changes
to theorem statements, imports, source proof bytes, mathlib, or base.
"""
from __future__ import annotations
import json,re
from pathlib import Path
from scripts import kuuos_v121_terminal_rlp_codeai_round3_v1 as prev
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

ROOT=base.ROOT
TARGET=prev.TARGET
SOURCE_BLOB=prev.SOURCE_BLOB
MEM=ROOT/"memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v121_terminal_round3_v1.json"
OUT=Path("/tmp/kuuos-v121-terminal-codeai-round4")
MCP=Path("/tmp/kuuos-v121-terminal-mcp-round4")
HELPER=prev.HELPER
PRODUCER=43859692693
PREV_HEAD="0aed99eb66f9530c8a85ccc4d9c0cdcba0b44d64"
PREV_TREE="ef97e9481b320f583ea1f7c4e02f9fad490e56dc"

def check(ok, why):
    if not ok: raise RuntimeError("KUUOS_V121_TERMINAL_ROUND4_FAIL_CLOSED: "+why)

def once(s,old,new):
    check(s.count(old)==1,"anchor drift: "+old[:90])
    return s.replace(old,new,1)

def make_variants(original):
    check(base.blob(original.encode())==SOURCE_BLOB,"original source drift")
    previous=prev.make_variants(original)
    old_names=re.findall(r"(?m)^(?:theorem|def)\s+([A-Za-z0-9_]+)",original)
    result={}
    for name,source,mode in [
      ("round4-native-direct",previous["round3-native-component"],"exact"),
      ("round4-isPushout-plain-simp",previous["round3-isPushout-component"],"plain"),
      ("round4-isPushout-two-stage",previous["round3-isPushout-two-stage"],"twostage")]:
        if mode=="twostage":
            source=once(source,
              "      simpa [standardTypeCTargetDistinguishedTriangle.{0}] using ht",
              "      exact ht")
        else:
            replacement=(
              "      exact h" if mode=="exact" else
              "      simpa only [standardTypeCTargetDistinguishedTriangle] using h")
            source=once(source,
              "      simpa [standardTypeCTargetDistinguishedTriangle.{0}] using h",
              replacement)
        source=once(source,
          "            rw [standardTypeCCarrierMap_inl_horn.{0}]",
          "            exact congrArg\n"
          "              (fun q => q ≫ ("+HELPER+".toTargetMap K))\n"
          "              (standardTypeCCarrierMap_inl_horn.{0} m)")
        source=once(source,
          "            rw [standardTypeCCarrierMap_inr_point.{0}]",
          "            exact congrArg\n"
          "              (fun q => q ≫ ("+HELPER+".toTargetMap K))\n"
          "              (standardTypeCCarrierMap_inr_point.{0} m)")
        check(re.findall(r"(?m)^(?:theorem|def)\s+([A-Za-z0-9_]+)",source)==old_names,
              "theorem inventory changed")
        check(source.splitlines()[0]==original.splitlines()[0],"import changed")
        check(base.FORBIDDEN_NEW.search(source) is None,"forbidden proof construct")
        result[name]=source
    check(len({base.blob(v.encode()) for v in result.values()})==3,
          "candidate collision")
    return result

def main():
    head,tree=base.event_source()
    require_pins(ROOT)
    original=(ROOT/TARGET).read_bytes()
    check(base.blob(original)==SOURCE_BLOB,"target source changed")
    obs=read_observation_seed(MEM)
    check(len(obs)==3 and all(x["source_head"]==PREV_HEAD and
       x["producer_run"]==PRODUCER and x["outcome"]=="DIRECT_LEAN_FAILURE"
       for x in obs),"round3 failure provenance invalid")
    check(all(x["source_tree"]==PREV_TREE for x in json.loads(MEM.read_text())["observations"]),
          "round3 source tree provenance drift")
    variants=make_variants(original.decode("utf-8"))
    hashes={x["candidate_blob"] for x in obs}
    check(all(base.blob(x.encode()) not in hashes for x in variants.values()),"failed blob replay")
    base.TARGET=TARGET; base.OUT=OUT; base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    try:
        for name,s in variants.items():
            (OUT/(name+".lean")).write_text(s)
            try: rows.append(base.direct(name,s))
            finally: (ROOT/TARGET).write_bytes(original)
        mcp=base.mcp_verify(head,rows,variants)
    finally:
        (ROOT/TARGET).write_bytes(original)
    check(base.blob((ROOT/TARGET).read_bytes())==SOURCE_BLOB,"source not restored")
    MCP.mkdir(parents=True,exist_ok=True)
    mcp["source_restored"]=True
    (MCP/"receipt.json").write_text(json.dumps(mcp,sort_keys=True,indent=2)+"\n")
    (OUT/"portfolio.json").write_text(json.dumps({
        "source_head":head,"source_tree":tree,"previous_run":PRODUCER,
        "candidate_count":len(rows),"candidates":rows,
        "source_restored":True,"git_write_performed":False,
        "independent_ci_certified":False},sort_keys=True,indent=2)+"\n")
    print("KUUOS_TERMINAL_ROUND4 "+json.dumps({
        "head":head,"tested":len(rows),
        "direct_green":[x["variant"] for x in rows if x["status"]=="SUCCESS"],
        "errors":{x["variant"]:x.get("error_count") for x in rows},
        "mcp_status":mcp["status"],"selected":mcp.get("selected"),
        "source_restored":True},sort_keys=True))
    return 0 if mcp["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
