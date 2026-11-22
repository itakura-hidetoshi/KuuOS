#!/usr/bin/env python3
"""CodeAI v0.61: source-sealed, diagnostic-only .olean split of F112 P94.

Never edits/replaces the authoritative 14-cell source. The first module is
the exact prefix (through GenuineFourteenPasting) and the second is the
verbatim GenuineFiveStage section with the original local header. This
measures whether module-boundary elaboration avoids a localized slowdown.
A success of split modules is NOT an original-module/root certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/"formal/Kuu/F112/PolygonNativeF55P94DK5FourteenCellNonabelianPasting.lean"
EXPECTED_BLOB = "928b6f5bdb59c6ba74fbb8122666fc6e274f4d7c"
ROOT_BLOB = "87ee2a7f541e48482e0d76f2abf819932c42f188"
CANDIDATE_BLOB = "c70aa395d14d873c686008bd80c835c059f936d5"
MATHLIB = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
CORE_NAME = "CodeAIV061F112CoreProbe"
TAIL_NAME = "CodeAIV061F112FiveStageTailProbe"

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def make_split(part: str) -> dict:
    raw = SOURCE.read_bytes()
    assert blob(raw) == EXPECTED_BLOB, "source changed"
    assert blob((ROOT/"formal/KuuOSFormal.lean").read_bytes()) == ROOT_BLOB
    assert blob((ROOT/"formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean").read_bytes()) == CANDIDATE_BLOB
    assert (ROOT/"lean-toolchain").read_text().strip() == "leanprover/lean4:v4.30.0-rc2"
    mathlib = [x for x in json.loads((ROOT/"lake-manifest.json").read_text())["packages"] if x["name"] == "mathlib"]
    assert len(mathlib) == 1 and mathlib[0]["rev"] == MATHLIB
    src = raw.decode("utf-8")
    assert src.endswith("\n")
    assert len(src.splitlines()) == 352
    start = "section GenuineFiveStage\n"
    stop = "\nend GenuineFiveStage"
    assert src.count(start) == 1 and src.count(stop) == 1
    assert src.count("\nend GenuineFourteenPasting\n") == 1
    assert src.count("namespace Kuu.F112.Physical\n") == 1

    prefix, suffix = src.split(start, 1)
    stage, remaining = suffix.split(stop, 1)
    assert "nativeK5PentagonatorFifteen_raw_ne" in stage
    assert "#print axioms" in remaining
    core = prefix + "\nend\nend Kuu.F112.Physical\n"

    # Entire header (namespace, Category variables, noncomputable section).
    header = src.split("namespace Kuu.F112.Physical\n",1)[1].split(
        "abbrev NativeK5FourteenHistoryWord",1)[0]
    header = "namespace Kuu.F112.Physical\n" + header
    variants = {
        "exchange-only": "\ndef nativeK5PentagonatorFifteenLeftFirst :=",
        "after-left": "\ndef nativeK5PentagonatorFifteenRightFirst :=",
        "full-tail": None,
    }
    cut = variants[part]
    if cut:
        assert stage.count(cut) == 1, "ambiguous cut"
        stage = stage.split(cut, 1)[0]

    tail = (
        f"import Kuu.F112.{CORE_NAME}\n"
        + header + start + stage
        + "\nend GenuineFiveStage\n\nend\nend Kuu.F112.Physical\n"
    )
    assert "sorry" not in tail and "admit" not in tail
    assert "sorry" not in core and "admit" not in core

    dest = ROOT/"artifacts/codeai-v061-f112-olean-split"/part
    dest.mkdir(parents=True,exist_ok=True)
    moddir=ROOT/"formal/Kuu/F112"
    core_path=moddir/(CORE_NAME+".lean")
    tail_path=moddir/(TAIL_NAME+".lean")
    assert not core_path.exists() and not tail_path.exists(), "forbid overwrite"
    core_path.write_text(core)
    tail_path.write_text(tail)

    record = {
        "schema":"codeai.v061.f112.olean_split_diagnostic.v1",
        "part":part,
        "original_blob":EXPECTED_BLOB,
        "original_lines":len(src.splitlines()),
        "original_unchanged":True,
        "diagnostic_only":True,
        "core_sha256":hashlib.sha256(core.encode()).hexdigest(),
        "tail_sha256":hashlib.sha256(tail.encode()).hexdigest(),
        "core_rel":str(core_path.relative_to(ROOT)),
        "tail_rel":str(tail_path.relative_to(ROOT)),
        "lean":"v4.30.0-rc2","mathlib":MATHLIB,
        "root_status":"HOLD","module_status":"HOLD",
        "memory":"HOLD","merge_authority":False,
    }
    (dest/"manifest.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    return record

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--part",choices=("exchange-only","after-left","full-tail"),required=True)
    args=p.parse_args()
    print("CODEAI_F112_SPLIT_PREPARE",json.dumps(make_split(args.part),sort_keys=True))
