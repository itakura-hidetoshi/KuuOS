#!/usr/bin/env python3
"""Source-hash-sealed CodeAI v0.61 F112 13D local elaboration bisection.

The 13D ORIGINAL Lean module remains byte-identical. This diagnostic
generates two distinct scratch modules, one exact general/observer prefix,
one five-stage fragment. A matrix variant changes only a diagnostic
presentation of the left-first term; none is admitted into formal roots.
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
ROOT_BLOB="87ee2a7f541e48482e0d76f2abf819932c42f188"
MODEL_A_BLOB="c70aa395d14d873c686008bd80c835c059f936d5"
MATHLIB="5450b53e5ddc75d46418fabb605edbf36bd0beb6"
CORE="CodeAIV061F112ThirteenCoreProbe"
TAIL="CodeAIV061F112ThirteenVariantProbe"
ORIGINAL="""def nativeK5PentagonatorFourteenLeftFirst :=
  nativeK5ThirteenPastingLeftThenRight
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)"""
VARIANTS={
    "exchange-only":None,
    "original-left":ORIGINAL,
    "witness-let":"""def nativeK5PentagonatorFourteenLeftFirst :=
  let W := nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5
  nativeK5ThirteenPastingLeftThenRight
    (NativeK5StructuralThirteenCell.squareExchange W)""",
    "typed-result":"""def nativeK5PentagonatorFourteenLeftFirst :
    NativeK5StructuralThirteenCell p
      (.trans (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)
        (.symm (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)))
      (.trans (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5)
        (.symm (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5))) :=
  nativeK5ThirteenPastingLeftThenRight
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)""",
    "direct-square":"""def nativeK5PentagonatorFourteenLeftFirst :=
  nativeK5ThirteenPastingLeftThenRight
    (NativeK5StructuralThirteenCell.squareExchange
      (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5))"""
}

def blob(data:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def sha(source:str)->str:
    return hashlib.sha256(source.encode()).hexdigest()

def produce(variant:str)->dict:
    assert variant in VARIANTS
    b=SOURCE.read_bytes()
    assert blob(b)==SOURCE_BLOB,"wrong_thirteen_source"
    assert blob((ROOT/"formal/KuuOSFormal.lean").read_bytes())==ROOT_BLOB,"wrong_public_root"
    assert blob((ROOT/"formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean").read_bytes())==MODEL_A_BLOB,"wrong_codeai_candidate"
    assert (ROOT/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
    p=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [x["rev"] for x in p if x["name"]=="mathlib"]==[MATHLIB]
    source=b.decode("utf-8")
    assert source.endswith("\n") and len(source.splitlines())==493
    assert source.count(ORIGINAL)==1
    mark="section GenuineFiveStage\n"
    assert source.count(mark)==1
    prefix,rest=source.split(mark,1)
    assert rest.count("def nativeK5PentagonatorFourteenLeftFirst :=")==1
    assert rest.count("def nativeK5PentagonatorFourteenRightFirst :=")==1
    header="namespace Kuu.F112.Physical\n"+source.split("namespace Kuu.F112.Physical\n",1)[1].split("abbrev NativeK5ThirteenHistoryWord",1)[0]
    assert header.count("noncomputable section")==1
    core=prefix+"\nend\nend Kuu.F112.Physical\n"
    if variant=="exchange-only":
        partial=rest.split("def nativeK5PentagonatorFourteenLeftFirst :=",1)[0]
    else:
        partial=rest.split("def nativeK5PentagonatorFourteenRightFirst :=",1)[0]
        assert partial.count(ORIGINAL)==1
        partial=partial.replace(ORIGINAL,VARIANTS[variant],1)
    tail="import Kuu.F112."+CORE+"\n"+header+mark+partial+"\nend GenuineFiveStage\n\nend\nend Kuu.F112.Physical\n"
    # Reject new trust bypasses; references to 'axiom' in comments or print
    # instructions are not proof admissions.
    assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",core)
    assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",tail)
    folder=ROOT/"formal/Kuu/F112"
    core_path,tail_path=folder/(CORE+".lean"),folder/(TAIL+".lean")
    assert not core_path.exists() and not tail_path.exists(),"scratch_must_not_overwrite"
    core_path.write_text(core)
    tail_path.write_text(tail)
    out=ROOT/"artifacts/codeai-v061-f112-13d-source-sealed-bisect"/variant
    out.mkdir(parents=True,exist_ok=True)
    m={
      "schema":"codeai.v061.f112.13d_bisect.v1",
      "source_blob":SOURCE_BLOB,"source_sha256":hashlib.sha256(b).hexdigest(),
      "source_lines":len(source.splitlines()),
      "variant":variant,
      "original_leftfirst_sha256":sha(ORIGINAL),
      "core_sha256":sha(core),"tail_sha256":sha(tail),
      "core_path":str(core_path.relative_to(ROOT)),
      "tail_path":str(tail_path.relative_to(ROOT)),
      "toolchain":"v4.30.0-rc2","mathlib":MATHLIB,
      "real_source_unchanged":True,"formal_admission":False,
      "full_14d_root":"HOLD","four_verifier_families":"HOLD",
      "version_bound_memory":"HOLD","merge_authority":False
    }
    (out/"manifest.json").write_text(json.dumps(m,sort_keys=True,indent=2)+"\n")
    return m

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--variant",required=True,choices=sorted(VARIANTS))
    a=ap.parse_args()
    print("CODEAI_F112_13D_BISECT_CANDIDATE",json.dumps(produce(a.variant),sort_keys=True))
