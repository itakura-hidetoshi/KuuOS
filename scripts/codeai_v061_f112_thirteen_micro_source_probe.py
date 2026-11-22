#!/usr/bin/env python3
"""Exact source-sealed 13D micro-stage elaboration diagnostic (no adoption).

Split the original GenuineFiveStage into one declaration per scratch module.
Keep all original declaration texts in original order; retain the original
axiom audit on the last module. Never write to the canonical source.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"formal/Kuu/F112/PolygonNativeF55P94DK5ThirteenCellNonabelianPasting.lean"
ORIGINAL_BLOB="657461025d27785fe3e17a2593f0fa9d164da3fc"
ROOT_BLOB="87ee2a7f541e48482e0d76f2abf819932c42f188"
MODEL_A_BLOB="c70aa395d14d873c686008bd80c835c059f936d5"
MATHLIB="5450b53e5ddc75d46418fabb605edbf36bd0beb6"
CORE="CodeAIV061F112ThirteenMicroCoreProbe"
STAGES=[f"CodeAIV061F112ThirteenMicroStage{i:02d}Probe" for i in range(6)]
DECLS=[
    "nativeK5PentagonatorFourteenExchangeThirteen",
    "nativeK5PentagonatorFourteenLeftFirst",
    "nativeK5PentagonatorFourteenRightFirst",
    "nativeK5PentagonatorFourteen_integerBlind",
    "nativeK5PentagonatorFourteen_history_ne",
    "nativeK5PentagonatorFourteen_raw_ne",
]
OUT=ROOT/"artifacts/codeai-v061-f112-thirteen-micro-source"

def blob(b:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def sha(t:str)->str:
    return hashlib.sha256(t.encode()).hexdigest()
def verify()->str:
    b=SOURCE.read_bytes()
    assert blob(b)==ORIGINAL_BLOB
    assert blob((ROOT/"formal/KuuOSFormal.lean").read_bytes())==ROOT_BLOB
    assert blob((ROOT/"formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean").read_bytes())==MODEL_A_BLOB
    assert (ROOT/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
    packages=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [p["rev"] for p in packages if p["name"]=="mathlib"]==[MATHLIB]
    t=b.decode("utf-8")
    assert t.endswith("\n") and len(t.splitlines())==493
    return t

def generate()->dict:
    source=verify()
    marker="section GenuineFiveStage\n"
    assert source.count(marker)==1
    before,rest=source.split(marker,1)
    close="\nend GenuineFiveStage\n"
    assert rest.count(close)==1
    stage,audits=rest.split(close,1)
    assert "#print axioms nativeK5PentagonatorFourteen_raw_ne" in audits
    assert audits.endswith("end\nend Kuu.F112.Physical\n")
    header="namespace Kuu.F112.Physical\n"+source.split(
        "namespace Kuu.F112.Physical\n",1)[1].split(
        "abbrev NativeK5ThirteenHistoryWord",1)[0]
    pattern=r"(?m)^(?:def|theorem) (nativeK5PentagonatorFourteen(?:ExchangeThirteen|LeftFirst|RightFirst|_integerBlind|_history_ne|_raw_ne))(?=\s|:)"
    matches=list(re.finditer(pattern,stage))
    assert [m.group(1) for m in matches]==DECLS, [m.group(1) for m in matches]
    vars_part=stage[:matches[0].start()]
    chunks=[stage[matches[i].start():(matches[i+1].start() if i+1<len(matches) else len(stage))] for i in range(6)]
    assert vars_part+"".join(chunks)==stage
    assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",before+stage+audits)
    outdir=ROOT/"formal/Kuu/F112"
    initial=before+"\nend\nend Kuu.F112.Physical\n"
    files=[(CORE,initial)]
    for i,name in enumerate(STAGES):
        dep=CORE if i==0 else STAGES[i-1]
        endpart=close+(audits if i==5 else "\nend\nend Kuu.F112.Physical\n")
        body="import Kuu.F112."+dep+"\n"+header+marker+vars_part+chunks[i]+endpart
        assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",body)
        files.append((name,body))
    for name,body in files:
        path=outdir/(name+".lean")
        assert not path.exists(),"no scratch overwrite:"+str(path)
        path.write_text(body)
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={
        "schema":"codeai.v061.f112.micro_thirteen_original.v1",
        "original_blob":ORIGINAL_BLOB,
        "original_source_sha256":sha(source),
        "original_source_lines":493,
        "original_declaration_names":DECLS,
        "exact_stage_body_sha256":sha(stage),
        "exact_stage_declaration_concat_sha256":sha("".join(chunks)),
        "original_axiom_audit_sha256":sha(audits),
        "original_theorems_unchanged":True,
        "original_source_unchanged":True,
        "root_unchanged":True,
        "module_names":[name for name,_ in files],
        "module_sha256":{name:sha(body) for name,body in files},
        "mathlib":MATHLIB,"lean":"v4.30.0-rc2",
        "independent_strict_lean":"TEST_REQUIRED","original_root":"HOLD",
        "verified_useful_memory":"HOLD","four_family":"HOLD","merge_authority":False,
    }
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest

if __name__=="__main__":
    print("CODEAI_F112_MICRO_STAGES_SOURCE_SEALED",json.dumps(generate(),sort_keys=True))
