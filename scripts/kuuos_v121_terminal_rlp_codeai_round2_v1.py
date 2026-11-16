#!/usr/bin/env python3
"""KuuOS v1.121 terminal RLP CodeAI round2. Compare exact pinned mathlib
pushout.desc/inl_desc/inr_desc and explicitly universe-zero IsPushout.
The old 17-error round1 source remains unchanged, including all 19 declarations.
No proof adoption, Git write, or independent CI in this candidate producer.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from scripts import kuuos_v121_terminal_rlp_codeai_round1_v1 as old
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

ROOT=base.ROOT
TARGET=old.TARGET
SOURCE_BLOB=old.SOURCE_BLOB
OUT=Path("/tmp/kuuos-v121-terminal-codeai-round2")
MCP=Path("/tmp/kuuos-v121-terminal-mcp-round2")
HISTORY=ROOT/"memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v121_terminal_round1_v1.json"

def check(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V121_TERMINAL_ROUND2_FAIL_CLOSED: "+why)

def one(src: str, old: str, new: str) -> str:
    check(src.count(old)==1, "unexpected source anchor: "+old[:85])
    return src.replace(old,new,1)

def make_variants(original: str) -> dict[str,str]:
    check(base.blob(original.encode())==SOURCE_BLOB,"terminal original blob drift")
    # All source proof statements retained from the exact round1 candidate.
    # Previous failure showed that implicit category/universe synthesis
    # attempted Category Type instead of SSet.{0}; use the fixed native model.
    common=old.candidates(original)["explicit-assoc-qualified"]
    names=old.declarations(original)
    for symbol in [
        "standardTypeCEdgeToSimplex",
        "standardTypeCEdgeCollapseToPoint",
        "standardTypeCEdgeToHorn",
        "standardTypeCEdgeToHorn_comp_hornInclusion",
        "standardTypeCSourceCarrier",
        "standardTypeCTargetCarrier",
        "standardTypeCSourceCarrier_isPushout",
        "standardTypeCTargetCarrier_isPushout",
        "standardTypeCSource_edge_collapsed",
        "standardTypeCCarrierMap",
        "standardTypeCCarrierMap_inl_horn",
        "standardTypeCCarrierMap_inr_point",
        "standardTypeCTargetScaling",
        "standardTypeCTargetDistinguishedTriangle",
        "standardTypeCGeneratorHom",
    ]:
        common=re.sub(r"\b"+symbol+r"\b(?!\.)",symbol+".{0}",common)
    common=common.replace("MorphismProperty ScaledSSet",
                          "MorphismProperty (ScaledSSet.{0})")
    common=common.replace(
        "KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.StandardArbitraryScalingObstructionClosed",
        "KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.StandardArbitraryScalingObstructionClosed.{0}")
    common=common.replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.canonicalKuuOSPresentation",
        "KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation.{0}")
    common=common.replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.standardABCPresentation",
        "KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation.{0}")
    for symbol in ["standardGeneratedScaledFibrationABC","canonicalGeneratedScaledAnodyne"]:
        common=re.sub(r"\b"+symbol+r"\b(?!\.)",symbol+".{0}",common)
    # This does not postulate RLP: the same terminal witness and finite
    # cocycle completion are still required in the original theorem bodies.
    direct=common
    direct=one(direct,
        "(standardTypeCTargetCarrier_isPushout.{0} m).desc",
        "pushout.desc")
    direct=one(direct,
        "(standardTypeCTargetCarrier_isPushout.{0} m).inl_desc",
        "pushout.inl_desc")
    direct=one(direct,
        "(standardTypeCTargetCarrier_isPushout.{0} m).inr_desc",
        "pushout.inr_desc")
    mixed=common
    mixed=one(mixed,
        "(standardTypeCTargetCarrier_isPushout.{0} m).inl_desc",
        "pushout.inl_desc")
    mixed=one(mixed,
        "(standardTypeCTargetCarrier_isPushout.{0} m).inr_desc",
        "pushout.inr_desc")
    pinned=common
    variants={
        "round2-native-pushout-desc":direct,
        "round2-isPushout-desc-pushout-lemmas":mixed,
        "round2-isPushout-fully-universe0":pinned,
    }
    check(len({base.blob(v.encode()) for v in variants.values()})==3,
          "candidate variants duplicated")
    for name,src in variants.items():
        check(old.declarations(src)==names,"declaration inventory changed: "+name)
        check(src.splitlines()[0]==original.splitlines()[0],"imports changed")
        check(base.FORBIDDEN_NEW.search(src) is None,"forbidden proof construct")
        check("KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.canonicalKuuOSPresentation" not in src,
              "old undefined presentation namespace")
    return variants

def main() -> int:
    head,tree=base.event_source()
    require_pins(ROOT)
    original=(ROOT/TARGET).read_bytes()
    check(base.blob(original)==SOURCE_BLOB,"terminal source changed")
    observations=read_observation_seed(HISTORY)
    check(len(observations)==2 and all(x["outcome"]=="DIRECT_LEAN_FAILURE" and
            x["producer_run"]==43852391288 for x in observations),
          "previous failed variant provenance drift")
    choices=make_variants(original.decode("utf-8"))
    fail_hashes={x["candidate_blob"] for x in observations}
    check(all(base.blob(x.encode()) not in fail_hashes for x in choices.values()),
          "replay of known failure blob")
    base.TARGET=TARGET; base.OUT=OUT; base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    try:
        for name,src in choices.items():
            (OUT/(name+".lean")).write_text(src)
            try:
                rows.append(base.direct(name,src))
            finally:
                (ROOT/TARGET).write_bytes(original)
        receipt=base.mcp_verify(head,rows,choices)
    finally:
        (ROOT/TARGET).write_bytes(original)
    check(base.blob((ROOT/TARGET).read_bytes())==SOURCE_BLOB,
          "original terminal proof not restored")
    MCP.mkdir(parents=True,exist_ok=True)
    receipt["source_restored"]=True
    (MCP/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    (OUT/"portfolio.json").write_text(json.dumps({
        "source_head":head,"source_tree":tree,
        "original_terminal_blob":SOURCE_BLOB,"previous_run":43852391288,
        "candidate_count":len(rows),"candidates":rows,
        "source_restored":True,"git_write_performed":False,
        "independent_ci_certified":False
    },sort_keys=True,indent=2)+"\n")
    print("KUUOS_TERMINAL_ROUND2 "+json.dumps({
        "head":head,"tested":len(rows),
        "direct_green":[r["variant"] for r in rows if r["status"]=="SUCCESS"],
        "error_counts":{r["variant"]:r.get("error_count") for r in rows},
        "mcp_status":receipt["status"],"selected":receipt.get("selected"),
        "source_restored":True
    },sort_keys=True))
    return 0 if receipt["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
