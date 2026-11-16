#!/usr/bin/env python3
"""KuuOS terminal RLP CodeAI round3; source-preserving, pinned, proof-only.
All three round2 direct Lean failures are recorded, never replayed. The new
changes replace a broken concrete-category simplification with simplex
component congruence and unfold horn/point aliases before rewriting.
Direct Lean tests every source, one green can proceed to real Lean MCP
and second direct Lean. Independent certification occurs separately.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts import kuuos_v121_terminal_rlp_codeai_round2_v1 as prev
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

ROOT=base.ROOT
TARGET=prev.TARGET
SOURCE_BLOB=prev.SOURCE_BLOB
HISTORY=ROOT/"memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v121_terminal_round2_v1.json"
OUT=Path("/tmp/kuuos-v121-terminal-codeai-round3")
MCP=Path("/tmp/kuuos-v121-terminal-mcp-round3")
HELPER="KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion"
PRODUCER=43856111778
PRIOR_HEAD="fc01f8f7cbf209fb0fa3b678d19a3c4fb7506218"
PRIOR_TREE="857f09a9083517a9112b188b9e5711a7878349e3"

def check(ok, reason):
    if not ok:
        raise RuntimeError("KUUOS_TERMINAL_ROUND3_FAIL_CLOSED: "+reason)

def one(src,old,new):
    check(src.count(old)==1,"source anchor drift: "+old[:75])
    return src.replace(old,new,1)

def make_variants(original):
    check(base.blob(original.encode())==SOURCE_BLOB,"original terminal blob drift")
    previous=prev.make_variants(original)
    old_hfac=(
      "      simpa [standardTypeCTargetDistinguishedTriangle.{0}] using\n"
      "        ConcreteCategory.congr_hom\n"
      "          (congr_app ("+HELPER+".target_inl_desc K) (op ⦋2⦌))\n"
      "          (standardTypeCTriangle01n m)")
    hfac1=(
      "      have h := congrArg\n"
      "        (fun q : (Δ[m + 3] : SSet.{0}) ⟶ duskinNerve NatDoubleDelooping =>\n"
      "          q.app (op ⦋2⦌) (standardTypeCTriangle01n.{0} m))\n"
      "        ("+HELPER+".target_inl_desc K)\n"
      "      simpa [standardTypeCTargetDistinguishedTriangle.{0}] using h")
    hfac2=(
      "      have happ := congrArg\n"
      "        (fun q : (Δ[m + 3] : SSet.{0}) ⟶ duskinNerve NatDoubleDelooping =>\n"
      "          q.app (op ⦋2⦌))\n"
      "        ("+HELPER+".target_inl_desc K)\n"
      "      have ht := congrArg\n"
      "        (fun q => q (standardTypeCTriangle01n.{0} m)) happ\n"
      "      simpa [standardTypeCTargetDistinguishedTriangle.{0}] using ht")
    items={
      "round3-native-component":(previous["round2-native-pushout-desc"],hfac1),
      "round3-isPushout-component":(previous["round2-isPushout-fully-universe0"],hfac1),
      "round3-isPushout-two-stage":(previous["round2-isPushout-fully-universe0"],hfac2),
    }
    result={}
    for name,(src,fix) in items.items():
        src=one(src,old_hfac,fix)
        src=one(src,"            rw [standardTypeCCarrierMap_inl_horn.{0}]",
            "            dsimp only [natTypeCSourceHornInl]\n"
            "            rw [standardTypeCCarrierMap_inl_horn.{0}]")
        src=one(src,"            rw [standardTypeCCarrierMap_inr_point.{0}]",
            "            dsimp only [natTypeCSourcePointInr]\n"
            "            rw [standardTypeCCarrierMap_inr_point.{0}]")
        check(prev.old.declarations(src)==prev.old.declarations(original),
              "declaration inventory changed: "+name)
        check(src.splitlines()[0]==original.splitlines()[0],
              "import boundary changed: "+name)
        check(base.FORBIDDEN_NEW.search(src) is None,
              "forbidden constructs: "+name)
        check("ConcreteCategory.congr_hom" not in src,
              "old invalid proof retained")
        result[name]=src
    check(len({base.blob(s.encode()) for s in result.values()})==3,
          "duplicate candidate sources")
    return result

def main():
    head,tree=base.event_source()
    require_pins(ROOT)
    original=(ROOT/TARGET).read_bytes()
    check(base.blob(original)==SOURCE_BLOB,"terminal source changed")
    observations=read_observation_seed(HISTORY)
    check(len(observations)==3 and all(x["outcome"]=="DIRECT_LEAN_FAILURE"
          and x["producer_run"]==PRODUCER and x["source_head"]==PRIOR_HEAD
          for x in observations),"round2 failure provenance mismatch")
    check(all(x["source_tree"]==PRIOR_TREE for x in json.loads(HISTORY.read_text())["observations"]),
          "round2 provenance tree mismatch")
    versions=make_variants(original.decode())
    failed={x["candidate_blob"] for x in observations}
    check(all(base.blob(s.encode()) not in failed for s in versions.values()),
          "failed candidate replay")
    base.TARGET=TARGET
    base.OUT=OUT
    base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    try:
        for name,src in versions.items():
            (OUT/(name+".lean")).write_text(src)
            try:
                rows.append(base.direct(name,src))
            finally:
                (ROOT/TARGET).write_bytes(original)
        mcp=base.mcp_verify(head,rows,versions)
    finally:
        (ROOT/TARGET).write_bytes(original)
    check(base.blob((ROOT/TARGET).read_bytes())==SOURCE_BLOB,"original source not restored")
    MCP.mkdir(parents=True,exist_ok=True)
    mcp["source_restored"]=True
    (MCP/"receipt.json").write_text(json.dumps(mcp,sort_keys=True,indent=2)+"\n")
    (OUT/"portfolio.json").write_text(json.dumps({
        "source_head":head,"source_tree":tree,
        "previous_run":PRODUCER,"previous_source_head":PRIOR_HEAD,
        "original_blob":SOURCE_BLOB,"candidate_count":len(rows),
        "candidates":rows,"source_restored":True,
        "git_write_performed":False,"independent_ci_certified":False
    },sort_keys=True,indent=2)+"\n")
    print("KUUOS_TERMINAL_ROUND3 "+json.dumps({
        "head":head,"tested":len(rows),"direct_green":
        [x["variant"] for x in rows if x["status"]=="SUCCESS"],
        "errors":{x["variant"]:x.get("error_count") for x in rows},
        "mcp_status":mcp["status"],"selected":mcp.get("selected"),
        "source_restored":True},sort_keys=True))
    return 0 if mcp["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
