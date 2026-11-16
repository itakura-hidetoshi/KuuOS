#!/usr/bin/env python3
"""CodeAI Type-C round2 after exact five-error direct Lean observation #43829329953.
Test source-distinct structural proof repairs without editing original sources.
Direct pinned Lean before actual real Lean MCP; independent CI is separate.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from scripts import kuuos_v121_typec_codeai_round1_v1 as old
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins

ROOT=old.ROOT
TARGET=old.TARGET
ORIGINAL_BLOB=old.ORIGINAL_BLOB
BRIDGE=old.BRIDGE
BRIDGE_BLOB=old.BRIDGE_BLOB
OUT=Path("/tmp/kuuos-v121-typec-codeai-round2")
MCP=Path("/tmp/kuuos-v121-typec-real-mcp-round2")

def check(ok: bool, why: str) -> None:
    if not ok: raise RuntimeError("KUUOS_V121_TYPEC_ROUND2_FAIL_CLOSED: "+why)

def replace_one(s: str, left: str, right: str) -> str:
    check(s.count(left)==1,"source drift for "+left[:80])
    return s.replace(left,right,1)

def make_variants(original: str) -> dict[str,str]:
    source=old.mk_variants(original)["typec-round1-universe0-naturality-fin"]
    source=replace_one(source,
        "(SSet.horn.face (0 : Fin 4) (2 : Fin 4) (by decide))) = 0 := by",
        "(SSet.horn.face (0 : Fin 4) (2 : Fin 4) (by decide))) = (0 : Nat) := by")
    source=replace_one(source,
        "            congr <;> exact Subsingleton.elim _ _",
        "            congr")
    source=replace_one(source,
        "        simp\n      · by_cases hcdEq",
        "        all_goals simp\n      · by_cases hcdEq")
    source=replace_one(source,
        "end KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105\n",
        "end\n\nend KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105\n")
    oldrw="  rw [hx0, hx1, hx2, hx3] at hcoc\n  simpa [NatTetrahedronEquation, sigma, e01, e12, e23] using hcoc"
    check(source.count(oldrw)==1,"dependent rewrite source differs")
    variants={
      "round2-eq-subst":source.replace(oldrw,
          "  subst a\n  subst b\n  subst c\n  subst d\n  simpa [NatTetrahedronEquation, sigma, e01, e12, e23] using hcoc"),
      "round2-simpa-hx":source.replace(oldrw,
          "  simpa [NatTetrahedronEquation, sigma, e01, e12, e23, hx] using hcoc"),
      "round2-simp-hx0":source.replace(oldrw,
          "  simp only [hx0, hx1, hx2, hx3] at hcoc\n  simpa [NatTetrahedronEquation, sigma, e01, e12, e23] using hcoc"),
      "round2-simpa-using":source.replace(oldrw,
          "  simpa only [hx0, hx1, hx2, hx3, NatTetrahedronEquation] using hcoc"),
    }
    check(len({base.blob(v.encode()) for v in variants.values()})==4,"duplicate candidates")
    old_names=[m.group(1) for m in re.finditer(r"(?m)^theorem\s+(\w+)",original)]
    for name,c in variants.items():
        new_names=[m.group(1) for m in re.finditer(r"(?m)^theorem\s+(\w+)",c)]
        check(new_names==old_names,"theorem inventory changed: "+name)
        check(c.startswith(original.split("\n",1)[0]+"\n"),"import changed: "+name)
        check(base.FORBIDDEN_NEW.search(c) is None,"forbidden construct: "+name)
        check("rw [hx0, hx1, hx2, hx3] at hcoc" not in c,"dependent rw retained")
    return variants

def main() -> int:
    head,tree=base.event_source()
    require_pins(ROOT)
    original=(ROOT/TARGET).read_bytes()
    check(base.blob(original)==ORIGINAL_BLOB,"original source changed")
    check(base.blob((ROOT/BRIDGE).read_bytes())==BRIDGE_BLOB,"bridge blob changed")
    versions=make_variants(original.decode("utf-8"))
    base.TARGET=TARGET
    base.OUT=OUT
    base.MCP=MCP
    OUT.mkdir(parents=True,exist_ok=False)
    rows=[]
    try:
        for name,src in versions.items():
            try:
                rows.append(base.direct(name,src))
            finally:
                (ROOT/TARGET).write_bytes(original)
        mcp=base.mcp_verify(head,rows,versions)
    finally:
        (ROOT/TARGET).write_bytes(original)
    check(base.blob((ROOT/TARGET).read_bytes())==ORIGINAL_BLOB,
          "original Lean file not restored")
    MCP.mkdir(parents=True,exist_ok=True)
    mcp["source_restored"]=True
    (MCP/"receipt.json").write_text(json.dumps(mcp,sort_keys=True,indent=2)+"\n")
    (OUT/"portfolio.json").write_text(json.dumps({
        "source_head":head,"source_tree":tree,"original_v105_blob":ORIGINAL_BLOB,
        "bridge_blob":BRIDGE_BLOB,"candidate_count":len(rows),
        "candidates":rows,"source_restored":True,"git_write_performed":False,
        "independent_ci_certified":False
    },sort_keys=True,indent=2)+"\n")
    print("KUUOS_V121_TYPEC_ROUND2 "+json.dumps({
      "head":head,"tested":len(rows),
      "direct_green":[x["variant"] for x in rows if x["status"]=="SUCCESS"],
      "error_counts":{x["variant"]:x.get("error_count") for x in rows},
      "selected":mcp.get("selected"),"mcp_status":mcp["status"],
      "source_restored":True},sort_keys=True))
    return 0 if mcp["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
