#!/usr/bin/env python3
"""Exact-source terminal-RLP CodeAI adapter, PR3562, bounded round one.
Templates are hypotheses; only direct Lean, real MCP and independent CI
establish their respective outcomes. No proof adoption or Git writes here.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
from pathlib import Path
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates, make_case
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

SOURCE_HEAD = "f6c421d8877542de1fb524068ba8b3393e0a835c"
SOURCE_TREE = "f985cc1bacdd0f596de058281434d527d9f6f0f1"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeCTerminalRLPPinnedV1_121.lean"
SOURCE_BLOB = "c81f3765791521e6e151b7f56a3b822cb81e8752"
ADAPTER = "scripts/kuuos_v121_terminal_rlp_codeai_round1_v1.py"
WORKFLOW = ".github/workflows/kuuos-v121-terminal-rlp-codeai-round1-v1.yml"
OLD_WORKFLOW = ".github/workflows/kuuos-v121-codeai-concrete-induced-endpoint-repaired-v1.yml"
OUT = Path("/tmp/kuuos-v121-terminal-codeai-round1")
MCP = Path("/tmp/kuuos-v121-terminal-mcp-round1")
OWNER = "KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106"
HELPER = OWNER + ".NatTypeCSourceCocycleCompletion"
HARNESS = {
 "scripts/kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1.py":"e64bdbda9cb65faee08e8690f111418f178ad5cf",
 "scripts/check_kuuos_lean_lsp_mcp_compatibility_v7_17.py":"1d3d48269db2bc055c1d75677786c12b69ef8967",
 "scripts/check_kuuos_lean_mcp_parent_pr3522_v155_v1.py":"acd3fada7b977f0b405feeb9deac9665499fe562",
 "scripts/kuuos_lean_mcp_repair_loop_v1.py":"c46209655b820354e63fd8264e392cda1198ccfc",
 "runtime/kuuos_codeai_lean_failure_memoryos_v0_1.py":"9f86641e60d0e76fafd8d850e7053d5e1cae6df8",
 "runtime/kuuos_codeai_lean_observation_intake_v0_1.py":"470a87a30eae70949ee2f077c67582d3b2056404",
 "runtime/kuuos_codeai_lean_observation_intake_v0_2.py":"570ba08950403d05fbe28fcb1b2866c2b1cd21ab",
}
REASONS = {
 "explicit-assoc-qualified":"Read all 347 source lines and the exact imported cocycle. Explicitly resolve local helpers instead of structure-owned dot notation, unfold the triangle wrapper, eliminate ofHoms directly, and close the unnamed section. Causes remain hypotheses pending Lean.",
 "rewrite-assoc-qualified":"Same preserved declarations and assumptions; use an explicit associativity rewrite instead of simp normalization for the collapsed-edge compatibility equation. Not a replay of a failed candidate."
}

def replace_once(text: str, old: str, new: str) -> str:
    base.require(text.count(old)==1, "ambiguous exact repair span")
    return text.replace(old,new,1)

def declarations(text: str) -> list[str]:
    return re.findall(r"(?m)^(?:theorem|def) ([A-Za-z0-9_]+)",text)

def candidates(original: str) -> dict[str,str]:
    base.require(base.blob(original.encode())==SOURCE_BLOB,"terminal source drift")
    common=original
    for name in sorted(["edge_compat","toTargetMap","target_inl_desc","target_inr_desc",
                         "cocycle_distinguished_thin","toTargetMap_scaled","toLift","toLift_fac"],
                       key=len,reverse=True):
        common=re.sub(r"\bK\."+name+r"\b", "("+HELPER+"."+name+" K)", common)
    common=common.replace("    IsScaledMap\n",
      "    KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22.IsScaledMap\n")
    common=replace_once(common,
      "  rw [NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]",
      "  dsimp only [standardTypeCTriangle01n]\n  rw [NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]")
    common=replace_once(common,
      "  rw [MorphismProperty.rlp_ofHoms_iff_hasLiftingProperty Nat]\n  exact natDoubleDelooping_hasLiftingProperty_standardTypeC",
      "  intro X Y i hi\n  cases hi with\n  | mk m => exact natDoubleDelooping_hasLiftingProperty_standardTypeC m")
    for prefix in ["KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.",
                   "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83."]:
        common=re.sub(re.escape(prefix)+r"\n +",prefix,common)
    common=replace_once(common,
      "    hle _ natDoubleDelooping_standardABC_generators_rlp",
      "    hle (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) natDoubleDelooping_standardABC_generators_rlp")
    common=replace_once(common,"end "+OWNER+"\n","end\n\nend "+OWNER+"\n")
    old="            rw [← standardTypeCEdgeToHorn_comp_hornInclusion]\n            simp"
    proofs={
      "explicit-assoc-qualified":"""            simpa only [Category.assoc] using
              congrArg (fun q => q ≫ K.cocycle.toSimplexMap)
                (standardTypeCEdgeToHorn_comp_hornInclusion m).symm""",
      "rewrite-assoc-qualified":"""            rw [← Category.assoc]
            exact congrArg (fun q => q ≫ K.cocycle.toSimplexMap)
              (standardTypeCEdgeToHorn_comp_hornInclusion m).symm"""
    }
    result={}
    for name,proof in proofs.items():
        code=replace_once(common,old,proof)
        base.require(declarations(code)==declarations(original),"declaration inventory changed")
        base.require(code.splitlines()[0]==original.splitlines()[0],"imports changed")
        base.require(not forbidden_code_constructs(code),"forbidden proof construct")
        # Explicit syntactic resolution, not changed mathematical hypotheses.
        normalized=code
        for name2 in ["edge_compat","toTargetMap","target_inl_desc","target_inr_desc",
                      "cocycle_distinguished_thin","toTargetMap_scaled","toLift","toLift_fac"]:
            normalized=normalized.replace("("+HELPER+"."+name2+" K)","K."+name2)
        normalized=normalized.replace(
          "KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22.IsScaledMap","IsScaledMap")
        headers=lambda s:[re.sub(r"\s+","",x.split(":=")[0].split(" where")[0])
          for x in re.split(r"(?m)^(?:theorem|def) ",s)[1:]]
        # Compare each pre-proof statement; normalize only broken dotted line breaks.
        base.require(headers(normalized)==headers(original),"theorem statements/assumptions changed")
        result[name]=code
    base.require(len({base.blob(s.encode()) for s in result.values()})==2,"duplicate variants")
    return result

def source_context() -> tuple[str,str]:
    base.require(os.environ.get("GITHUB_RUN_ATTEMPT")=="1","no candidate replay on workflow rerun")
    producer,tree=base.event_source()
    token=os.environ["GITHUB_TOKEN"]
    commit=base.github("commits/"+producer,token)
    base.require([p["sha"] for p in commit["parents"]]==[SOURCE_HEAD],
                 "producer is not the first child of the exact repair source")
    base.require({f["filename"] for f in commit["files"]}=={ADAPTER,WORKFLOW,OLD_WORKFLOW},
                 "producer modifies more than the three validation files")
    source=base.github("git/commits/"+SOURCE_HEAD,token)
    base.require(source["tree"]["sha"]==SOURCE_TREE,"source tree drift")
    for p,expected in {**base.DEPENDENCIES,**HARNESS}.items():
        base.require(base.blob((base.ROOT/p).read_bytes())==expected,"pinned dependency changed: "+p)
    return producer,tree

def main() -> int:
    producer,producer_tree=source_context()
    base.require_pins(base.ROOT)
    original=(base.ROOT/TARGET).read_bytes()
    base.require(base.blob(original)==SOURCE_BLOB,"exact target changed")
    versions=candidates(original.decode())
    memory=read_observation_directory(base.ROOT/"memoryos/external/github/2026/11")
    versions,history=route_candidates(versions,memory,source_head=SOURCE_HEAD,
                                    source_tree=SOURCE_TREE,imported_blob=SOURCE_BLOB)
    failed={c["candidate_blob"] for c in memory if c["outcome"]=="DIRECT_LEAN_FAILURE"}
    versions={k:v for k,v in versions.items() if base.blob(v.encode()) not in failed}
    base.require(1<=len(versions)<=4,"no novel candidates within budget")
    base.TARGET=TARGET; base.OUT=OUT; base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    (OUT/"memory-context.json").write_text(json.dumps(history,indent=2)+"\n")
    rows=[];receipt={}; cases=[]
    try:
        for name,code in versions.items():
            (OUT/(name+".lean")).write_text(code)
            try:
                row=base.direct(name,code)
            finally:
                (base.ROOT/TARGET).write_bytes(original)
            row["repair_hypothesis"]=REASONS[name]
            row["next_applicability"]="Exact terminal source/import/pins only; failed candidate hash must not be replayed."
            rows.append(row)
            cases.append(make_case(source_head=SOURCE_HEAD,source_tree=SOURCE_TREE,
                imported_blob=SOURCE_BLOB,variant=name,candidate_blob=row["candidate_blob"],
                producer_run=int(os.environ["GITHUB_RUN_ID"]),
                outcome="DIRECT_LEAN_SUCCESS" if row["status"]=="SUCCESS" else
                    ("DIRECT_LEAN_FAILURE" if row["errors"] else "NO_DATA"),errors=row["errors"]))
        # Reread the live PR before MCP; an external HEAD update aborts this attempt.
        source_context()
        try:
            receipt=base.mcp_verify(SOURCE_HEAD,rows,versions)
        finally:
            (base.ROOT/TARGET).write_bytes(original)
        receipt.update(producer_head=producer,producer_tree=producer_tree,
                       source_tree=SOURCE_TREE,source_restored=True)
    finally:
        (base.ROOT/TARGET).write_bytes(original)
        base.require(base.blob(original)==base.blob((base.ROOT/TARGET).read_bytes()),"restore failed")
        portfolio={"source_head":SOURCE_HEAD,"source_tree":SOURCE_TREE,
          "producer_head":producer,"producer_tree":producer_tree,
          "target":TARGET,"original_blob":SOURCE_BLOB,"round":1,
          "candidate_count":len(rows),"candidates":rows,"source_restored":True,
          "git_write_performed":False,"independent_ci_certified":False,
          "causal_status":"UNVERIFIED_HYPOTHESIS"}
        (OUT/"portfolio.json").write_text(json.dumps(portfolio,indent=2)+"\n")
        (OUT/"mcp-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
        (OUT/"memory-cases.json").write_text(json.dumps(cases,indent=2)+"\n")
        packet={"profile":"memoryos_codeai_lean_observations_v0_1",
          "repository":base.REPO,"authority":"external_pointer_only",
          "observations":[{k:c[k] for k in ["source_head","source_tree","imported_blob",
             "variant","candidate_blob","producer_run","outcome"]}|{"errors":r["errors"]}
             for c,r in zip(cases,rows)]}
        if packet["observations"]:
            p=OUT/"kuuos_codeai_lean_observations_v121_terminal_round1_v1.json"
            p.write_text(json.dumps(packet,indent=2)+"\n")
            read_observation_seed(p)
        print("KUUOS_TERMINAL_ROUND1 "+json.dumps(portfolio,sort_keys=True))
        print("KUUOS_TERMINAL_REAL_MCP "+json.dumps(receipt,sort_keys=True))
    return 0 if receipt.get("status")=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
