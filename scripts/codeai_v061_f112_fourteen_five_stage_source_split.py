#!/usr/bin/env python3
"""Exact-source staged 14D five-stage specialization, scratch only.

Four modules isolate Exchange, LeftFirst, RightFirst and all original theorems
plus the original 21 #print axioms directives. No declaration, theorem body,
source boundary, or assumption is modified. This does not certify the
unchanged original 14D monolithic file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

from scripts.codeai_v061_f112_fourteen_full_source_split import (
    ROOT, SOURCE, SOURCE_BLOB, OUT, CORE, assert_source, blob, sha,
)

NAMES = (
    "CodeAIV061F112FourteenFiveExchangeProbe",
    "CodeAIV061F112FourteenFiveLeftFirstProbe",
    "CodeAIV061F112FourteenFiveRightFirstProbe",
    "CodeAIV061F112FourteenFiveTheoremsProbe",
)
MARKER = "section GenuineFiveStage\n"
START = "/-- ORIGINAL source-dependent five-stage C60 K5 fourteen-cell. -/\n"
ANCHORS = (
    "def nativeK5PentagonatorFifteenLeftFirst :=",
    "def nativeK5PentagonatorFifteenRightFirst :=",
    "theorem nativeK5PentagonatorFifteen_integerBlind :",
)
EXPECTED = (
    "nativeK5PentagonatorFifteenExchangeFourteen",
    "nativeK5PentagonatorFifteenLeftFirst",
    "nativeK5PentagonatorFifteenRightFirst",
    "nativeK5PentagonatorFifteen_integerBlind",
    "nativeK5PentagonatorFifteen_history_ne",
    "nativeK5PentagonatorFifteen_raw_ne",
)
DIR = OUT / "five-stage"

def pieces() -> tuple[str, str, list[str]]:
    src = assert_source()
    assert blob(SOURCE.read_bytes()) == SOURCE_BLOB
    assert src.count(MARKER) == 1
    prefix, stage = src.split(MARKER, 1)
    assert stage.count(START) == 1
    header_vars, tail = stage.split(START, 1)
    header_vars = MARKER + header_vars
    assert all(tail.count(x) == 1 for x in ANCHORS)
    splits = [tail.index(x) for x in ANCHORS]
    assert splits == sorted(splits) and 0 < splits[0]
    parts = [
        START + tail[:splits[0]],
        tail[splits[0]:splits[1]],
        tail[splits[1]:splits[2]],
        tail[splits[2]:],
    ]
    assert header_vars + "".join(parts) == MARKER + stage
    assert parts[-1].endswith("end\nend Kuu.F112.Physical\n")
    assert tuple(re.findall(
        r"(?m)^(?:def|theorem) (nativeK5PentagonatorFifteen\w+)", "".join(parts)
    )) == EXPECTED
    assert len(re.findall(r"(?m)^#print axioms ", parts[-1])) == 21
    assert all(not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", p) for p in parts)
    prelude = "namespace Kuu.F112.Physical\n" + src.split(
        "namespace Kuu.F112.Physical\n", 1)[1].split(
            "abbrev NativeK5FourteenHistoryWord", 1)[0]
    return prelude, header_vars, parts

def render() -> dict:
    prelude, section_header, raw_parts = pieces()
    compiled = []
    for i, part in enumerate(raw_parts):
        prev = CORE if i == 0 else NAMES[i-1]
        prefix = "import Kuu.F112." + prev + "\n" + prelude + section_header
        text = prefix + part
        if i < len(NAMES) - 1:
            text += "\nend GenuineFiveStage\nend\nend Kuu.F112.Physical\n"
        assert text.endswith("\n")
        compiled.append(text)
    original = assert_source()
    DIR.mkdir(parents=True,exist_ok=True)
    candidates = [ROOT / "formal/Kuu/F112" / (name + ".lean") for name in NAMES]
    assert all(not p.exists() for p in candidates), "scratch source overwrite forbidden"
    for file, body in zip(candidates,compiled):
        file.write_text(body,encoding="utf-8")
    man = {
        "schema":"kuuos.codeai.v061.14d.five_stage_exact_pieces.v1",
        "original_fourteen_source_blob": SOURCE_BLOB,
        "original_fourteen_sha256": sha(original),
        "original_stage_sha256": sha(MARKER + original.split(MARKER,1)[1]),
        "original_five_stage_source_unchanged":True,
        "original_theorem_declarations_and_bodies_unchanged":True,
        "original_axiom_audits":21,
        "module_names":list(NAMES),
        "source_sha256":[sha(p) for p in compiled],
        "original_fragments_sha256":[sha(p) for p in raw_parts],
        "original_monolith_certified":False,
        "independent_ci_certified":False,
        "public_root_certified":False,
        "memory_verified_useful":False,
        "merge_authority":False,
    }
    assert not (DIR/"manifest.json").exists(),"scratch manifest overwrite forbidden"
    (DIR/"manifest.json").write_text(json.dumps(man,indent=2,sort_keys=True)+"\n")
    return man

def shim() -> dict:
    src=assert_source()
    man=json.loads((DIR/"manifest.json").read_text())
    assert man["original_fourteen_source_blob"]==SOURCE_BLOB
    assert man["original_fourteen_sha256"]==sha(src)
    for name,digest in zip(man["module_names"],man["source_sha256"]):
        assert sha((ROOT/"formal/Kuu/F112"/(name+".lean")).read_text())==digest
    target=OUT/"CanonicalShimScratch.lean"
    assert not target.exists(), "cannot overwrite canonical shim scratch"
    body = "import Kuu.F112." + NAMES[-1] + "\n"
    for name in EXPECTED:
        body += "#check Kuu.F112.Physical." + name + "\n"
    body += "#print axioms Kuu.F112.Physical.nativeK5PentagonatorFifteen_raw_ne\n"
    target.write_text(body)
    return {"shim_path":target.relative_to(ROOT).as_posix(),
            "shim_sha256":sha(body),"canonical_original_unchanged":True,
            "original_monolith_certified":False}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--phase",choices=("generate","shim"),default="generate")
    v=p.parse_args()
    print("CODEAI_F112_14D_FIVE_STAGE_SPLIT",
          json.dumps(render() if v.phase=="generate" else shim(),sort_keys=True),flush=True)
