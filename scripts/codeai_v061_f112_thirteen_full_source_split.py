#!/usr/bin/env python3
"""Source-sealed full 13D module decomposition, diagnostic-only.

The original canonical .lean remains byte-identical. The emitted scratch core
and tail copy its declaration text verbatim, including EVERY five-stage
declaration and the complete original axiom audit. The optional shim imports
the full scratch tail under the canonical module name in an isolated runner
using only a separate scratch file; never overwrite canonical source.

This is an elaboration-cost experiment, not proof admission or root authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"formal/Kuu/F112/PolygonNativeF55P94DK5ThirteenCellNonabelianPasting.lean"
SOURCE_BLOB="657461025d27785fe3e17a2593f0fa9d164da3fc"
PUBLIC_ROOT="87ee2a7f541e48482e0d76f2abf819932c42f188"
MODEL_A="c70aa395d14d873c686008bd80c835c059f936d5"
MATHLIB="5450b53e5ddc75d46418fabb605edbf36bd0beb6"
CORE="CodeAIV061F112ThirteenFullCoreProbe"
TAIL="CodeAIV061F112ThirteenFullTailProbe"
OUT=ROOT/"artifacts/codeai-v061-f112-thirteen-full-decomposition"

def blob(x:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(x)).encode()+b"\0"+x).hexdigest()

def sha(s:str)->str:
    return hashlib.sha256(s.encode()).hexdigest()

def assert_source()->str:
    b=SOURCE.read_bytes()
    assert blob(b)==SOURCE_BLOB,"stale original source"
    for path,expected in {
      "formal/KuuOSFormal.lean":PUBLIC_ROOT,
      "formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean":MODEL_A
    }.items():
        assert blob((ROOT/path).read_bytes())==expected,path
    assert (ROOT/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
    pkgs=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [p["rev"] for p in pkgs if p["name"]=="mathlib"]==[MATHLIB]
    text=b.decode()
    assert text.endswith("\n") and len(text.splitlines())==493
    assert text.count("section GenuineFiveStage\n")==1
    assert text.count("namespace Kuu.F112.Physical\n")==1
    assert text.count("abbrev NativeK5ThirteenHistoryWord")==1
    assert text.count("end GenuineFiveStage\n")==1
    assert text.count("#print axioms nativeK5PentagonatorFourteen_raw_ne")==1
    return text

def render()->dict:
    source=assert_source()
    marker="section GenuineFiveStage\n"
    prefix,stage=source.split(marker,1)
    header="namespace Kuu.F112.Physical\n"+source.split(
        "namespace Kuu.F112.Physical\n",1)[1].split(
        "abbrev NativeK5ThirteenHistoryWord",1)[0]
    core=prefix+"\nend\nend Kuu.F112.Physical\n"
    tail="import Kuu.F112."+CORE+"\n"+header+marker+stage
    assert stage.endswith("end\nend Kuu.F112.Physical\n"),"tail must carry the original final closes"
    assert stage.count("def nativeK5PentagonatorFourteenLeftFirst :=")==1
    assert stage.count("def nativeK5PentagonatorFourteenRightFirst :=")==1
    assert stage.count("theorem nativeK5PentagonatorFourteen_integerBlind :")==1
    assert stage.count("theorem nativeK5PentagonatorFourteen_history_ne :")==1
    assert stage.count("theorem nativeK5PentagonatorFourteen_raw_ne :")==1
    for text in (core,tail):
      assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",text)
      assert text.endswith("\n")
    lib=ROOT/"formal/Kuu/F112"
    p_core,p_tail=(lib/(CORE+".lean"),lib/(TAIL+".lean"))
    assert not p_core.exists() and not p_tail.exists(),"no overwrite"
    p_core.write_text(core)
    p_tail.write_text(tail)
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={
        "schema":"codeai.v061.f112.13d.full_source_split.v1",
        "parent_original_git_blob":SOURCE_BLOB,
        "parent_original_sha256":sha(source),
        "parent_original_lines":len(source.splitlines()),
        "raw_original_stage_sha256":sha(marker+stage),
        "exact_original_prefix_sha256":sha(prefix),
        "scratch_core_sha256":sha(core),
        "scratch_full_tail_sha256":sha(tail),
        "core_path":str(p_core.relative_to(ROOT)),
        "tail_path":str(p_tail.relative_to(ROOT)),
        "full_five_stage_statements_unchanged":True,
        "all_original_axiom_audit_commands_retained":True,
        "original_lean_file_unchanged":True,
        "public_root_unchanged":True,
        "toolchain":"v4.30.0-rc2",
        "mathlib":MATHLIB,
        "formal_adoption":False,
        "independent_original_module_certified":False,
        "full_root":"HOLD","four_verifier_families":"HOLD",
        "verified_useful_memory":"HOLD","merge_authority":False
    }
    (OUT/"manifest.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    return manifest

def shim()->dict:
    source=assert_source()
    d=json.loads((OUT/"manifest.json").read_text())
    assert d["parent_original_sha256"]==sha(source)
    for path,key in [(CORE,"scratch_core_sha256"),(TAIL,"scratch_full_tail_sha256")]:
        assert sha((ROOT/"formal/Kuu/F112"/(path+".lean")).read_text())==d[key]
    shimtext=(
      "import Kuu.F112."+TAIL+"\n\n"
      "#check Kuu.F112.Physical.nativeK5PentagonatorFourteenLeftFirst\n"
      "#check Kuu.F112.Physical.nativeK5PentagonatorFourteenRightFirst\n"
      "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_integerBlind\n"
      "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_history_ne\n"
      "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_raw_ne\n"
      "#print axioms Kuu.F112.Physical.nativeK5PentagonatorFourteen_raw_ne\n"
    )
    p=OUT/"CanonicalShimScratch.lean"
    assert not p.exists(),"shim overwrite forbidden"
    p.write_text(shimtext)
    return {"shim_path":str(p.relative_to(ROOT)),"shim_sha256":sha(shimtext),
            "never_overwrote_canonical_original":True,
            "canonical_original_git_blob":SOURCE_BLOB,
            "formal_adoption":False,"full_root":"HOLD"}

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--phase",choices=["generate","shim"],default="generate")
    opts=a.parse_args()
    ans=render() if opts.phase=="generate" else shim()
    print("CODEAI_F112_13D_FULL_SPLIT",json.dumps(ans,sort_keys=True),flush=True)
