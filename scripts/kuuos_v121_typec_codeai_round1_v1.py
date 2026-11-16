#!/usr/bin/env python3
"""CodeAI v1.121 Type-C isolated source-bound repair experiment.

The exact previous pinned v1.105 copy failed with >100 elaboration errors
before the v1.106 geometry or new endpoint-RLP theorem could run.
Test distinct structural hypotheses without modifying any original Lean source
permanently. This is NOT a proof or an independent CI certificate.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins

ROOT=base.ROOT
BRANCH="validation/kuuos-v121-induced-endpoint-on-certified-v120-20261116"
BASE="validation/kuuos-v120-induced-admission-recovery-20261116"
BASE_SHA="7c64a89b81681f997483d0873887df2f700d1244"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionPinnedV1_121.lean"
ORIGINAL_BLOB="6b1142889bbebaad76a8c143a323c9c272e45076"
BRIDGE="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFaceValueBridgeV1_121.lean"
BRIDGE_BLOB="51c84705c4eaffe6f607fb87f0891662613cdb94"
OUT=Path("/tmp/kuuos-v121-typec-codeai-round1")
MCP=Path("/tmp/kuuos-v121-typec-real-mcp-round1")
EXPECTED_THEOREM_NAMES=[
    "typeCThree_face1_val","typeCThree_face2_val","typeCThree_face3_val",
    "natTypeCThreeLabel013_eq_zero","natTypeCHornMap_mapComp_eq_label",
    "natTypeCHornLabel_tetrahedron_of_hornSimplex",
    "natTypeCFour_face1_eq0234","natTypeCFour_face2_eq0134",
    "natTypeCFour_face3_eq0124","natTypeCFour_face4_eq0123",
    "natTypeCFourLabels_all_equations",
    "natTypeCFourCocycle_restrict",
    "natTypeCFour_cocycle_completion",
    "natTypeCHighCocycle_restrict",
]
FIN_EQ=re.compile(
  r"have h([abcd])' : ([abcd]) = \((\d) : Fin 5\) := by apply Fin\.ext; omega"
)

def req(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V121_TYPEC_NO_DATA: "+why)

def replace_one(src: str, old: str, new: str, n: int=1) -> str:
    req(src.count(old)==n,"source anchor count drift: "+old[:60])
    return src.replace(old,new)

def mk_variants(original: str) -> dict[str,str]:
    req(original.startswith(
        "import KUOS.DependentOriginationDoubleDeloopingTypeAFaceValueBridgeV1_121\n"
    ),"unexpected original import")
    req(original.count(": SSet)")==22,"unexpected universe-location count")
    req(original.count("standardTypeCSourceCarrier m")==4,"source-carrier count drift")
    req(original.count("(by omega) (by omega)")==4,"Fin-last proof locations drift")
    req(original.count("by apply Fin.ext; omega")==20,"Fin ext proof count drift")
    # Hypothesis A: all actual B²Nat source/target simplicial sets live in
    # concrete universe 0. This is the fixed universe of the existing
    # concrete target (not a general fibrancy claim).
    a=original.replace(": SSet)",": SSet.{0})")
    a=a.replace("standardTypeCSourceCarrier m",
                "standardTypeCSourceCarrier.{0} m")
    a=a.replace("standardTypeCEdgeToHorn m",
                "standardTypeCEdgeToHorn.{0} m")
    a=a.replace("standardTypeCEdgeCollapseToPoint m",
                "standardTypeCEdgeCollapseToPoint.{0} m")
    # Hypothesis B: mirror the previously independent pinned v1.103
    # simplicial naturality proof rather than an unqualified declaration.
    b=replace_one(a,"natSimplex_triangle_face_comparison",
       "KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100.NatNormalizedDuskinCocycle.natSimplex_triangle_face_comparison")
    b=replace_one(b,
       "          apply congrArg duskinComparison\n          rw [← hsource]\n          exact hnat.symm",
       "          rw [← hsource]\n          exact congrArg duskinComparison hnat.symm")
    b=b.replace("ext Δ x","ext k x")
    b=b.replace("rcases Δ with ⟨⟨q⟩⟩","rcases k with ⟨⟨q⟩⟩")
    req(b.count("ext k x")==2 and b.count("rcases k with ⟨⟨q⟩⟩")==2,
        "restriction-ext signatures altered")
    # Hypothesis C: explicit Fin-order constructors and Fin.ext
    # by transport of existing integer-label equalities. In Lean 4,
    # omega cannot normalize all elaborated OfNat (Fin n) numerals.
    c=b.replace("(by omega) (by omega)",
                "(Fin.zero_le _) (Fin.le_last _)")
    c,count=FIN_EQ.subn(lambda m:
       f"have h{m.group(1)}' : {m.group(2)} = ({m.group(3)} : Fin 5) := by apply Fin.ext; simpa using h{m.group(1)}",
       c)
    req(count==20,"20 explicit finite cases not retained")
    # No theorem signatures, imports, constructors or named proof
    # obligations are removed. Variants vary only local elaboration hints.
    v={"typec-round1-universe0":a,
       "typec-round1-universe0-naturality":b,
       "typec-round1-universe0-naturality-fin":c}
    old=[m.group(1) for m in re.finditer(r"(?m)^theorem (\w+)",original)]
    req(all(x in old for x in EXPECTED_THEOREM_NAMES),
        "required v1.105 declarations missing")
    for name,source in v.items():
        check=[m.group(1) for m in re.finditer(r"(?m)^theorem (\w+)",source)]
        req(check==old, "proof declaration inventory changed: "+name)
        req(source.split("\n",1)[0]==original.split("\n",1)[0],
            "import boundary changed: "+name)
        req(base.FORBIDDEN_NEW.search(source) is None,
            "forbidden Lean construct: "+name)
    req(len({base.blob(s.encode()) for s in v.values()})==3,
        "duplicate CodeAI source candidate")
    return v

def main() -> int:
    head,tree=base.event_source()
    require_pins(ROOT)
    req(base.blob((ROOT/BRIDGE).read_bytes())==BRIDGE_BLOB,
        "exact v1.112/bridge imported Lean source drift")
    req(base.blob((ROOT/TARGET).read_bytes())==ORIGINAL_BLOB,
        "original v1.105 source changed")
    original=(ROOT/TARGET).read_bytes()
    choices=mk_variants(original.decode("utf-8"))
    base.TARGET=TARGET
    base.OUT=OUT
    base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    mcp=None
    try:
        for name,source in choices.items():
            try:
                rows.append(base.direct(name,source))
            finally:
                (ROOT/TARGET).write_bytes(original)
        mcp=base.mcp_verify(head,rows,choices)
    finally:
        (ROOT/TARGET).write_bytes(original)
        req(base.blob((ROOT/TARGET).read_bytes())==ORIGINAL_BLOB,
            "original file not restored")
    mcp["source_restored"]=True
    MCP.mkdir(parents=True,exist_ok=True)
    (MCP/"receipt.json").write_text(json.dumps(mcp,sort_keys=True,indent=2)+"\n")
    receipt={
      "source_head":head,"source_tree":tree,
      "source_original_blob":ORIGINAL_BLOB,
      "bridge_imported_blob":BRIDGE_BLOB,
      "candidate_count":len(rows),"candidates":rows,
      "source_restored":True,"git_write_performed":False,
      "independent_ci_certified":False,
    }
    (OUT/"portfolio.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V121_TYPEC_CODEAI "+json.dumps({
        "head":head,"candidate_count":len(rows),
        "direct_green":[r["variant"] for r in rows if r["status"]=="SUCCESS"],
        "errors":{r["variant"]:r.get("error_count") for r in rows},
        "mcp_status":mcp["status"],"source_restored":True
    },sort_keys=True))
    return 0 if mcp["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
