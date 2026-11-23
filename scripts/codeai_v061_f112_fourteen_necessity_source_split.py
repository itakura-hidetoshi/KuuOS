#!/usr/bin/env python3
"""Source-sealed scratch decomposition of genuine 14D five-stage Necessity.

Never edits the original Lean source, theorem bodies, axioms or proof root.
The three modules preserve all six exact declarations and six audit commands,
but this is NOT certification of the unchanged monolithic original file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from scripts.codeai_v061_f112_fourteen_full_source_split import (
    ROOT, SOURCE_BLOB as ORIGINAL_FOURTEEN_BLOB, assert_source as assert_fourteen,
    blob, sha,
)

SOURCE = ROOT / "formal/Kuu/F112/PolygonNativeF55P94DK5PentagonatorFourteenCellNecessity.lean"
SOURCE_BLOB = "a575f68e63b8d64988795fe5ec8389094be7b593"
OUT = ROOT / "artifacts/codeai-v061-f112-fourteen-full-decomposition/necessity"
CORE = "CodeAIV061F112FourteenNecessityCoreProbe"
MIDDLE = "CodeAIV061F112FourteenNecessityMiddleProbe"
TAIL = "CodeAIV061F112FourteenNecessityTailProbe"
START = "/-- The genuine, independent 14D Type-valued comparison generator\n"
MARKER_MIDDLE = "/-- Equality is ONLY in the genuine 14D quotient, not on\n"
MARKER_TAIL = "/-- The selected free-group history cannot descend across the\n"
NAMESPACE = "namespace Kuu.F112.Physical\n"
EXPECTED = (
    "nativeK5PentagonatorFourteenExchange",
    "nativeK5PentagonatorFourteen_relativeNecessity",
    "nativeK5PentagonatorFourteen_quotient_eq",
    "nativeK5PentagonatorFourteen_integerDescent",
    "nativeK5PentagonatorFourteen_historyNoDescent",
    "nativeK5PentagonatorFourteen_noCoreRetraction",
)

def assert_original() -> str:
    assert_fourteen()
    raw = SOURCE.read_bytes()
    assert blob(raw) == SOURCE_BLOB, "Necessity original changed"
    src = raw.decode("utf-8")
    assert src.endswith("\n") and len(src.splitlines()) == 116
    for marker in (START, MARKER_MIDDLE, MARKER_TAIL, NAMESPACE):
        assert src.count(marker) == 1, "source anchor mismatch: " + marker
    assert len(re.findall(r"(?m)^#print axioms ", src)) == 6
    assert src.endswith("end GenuineFiveStage\nend\nend Kuu.F112.Physical\n")
    return src

def render() -> dict:
    src = assert_original()
    a = src.index(MARKER_MIDDLE)
    b = src.index(MARKER_TAIL)
    assert 0 < src.index(START) < a < b
    original_header = NAMESPACE + src.split(NAMESPACE, 1)[1].split(START, 1)[0]
    core = src[:a] + "\nend GenuineFiveStage\nend\nend Kuu.F112.Physical\n"
    middle = "import Kuu.F112." + CORE + "\n" + original_header + src[a:b] + "\nend GenuineFiveStage\nend\nend Kuu.F112.Physical\n"
    tail = "import Kuu.F112." + MIDDLE + "\n" + original_header + src[b:]
    for body in (core, middle, tail):
        assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", body)
        assert body.endswith("\n")
    # Audit the exact original six declarations, their distribution, and all prints.
    original_decl = re.findall(r"(?m)^(?:def|theorem) (nativeK5PentagonatorFourteen\w+)", src)
    assert tuple(original_decl) == EXPECTED, original_decl
    for body, names in zip((core, middle, tail),
                           (EXPECTED[:2], EXPECTED[2:4], EXPECTED[4:])):
        actual = re.findall(r"(?m)^(?:def|theorem) (nativeK5PentagonatorFourteen\w+)", body)
        assert tuple(actual) == names
    assert tail.count("#print axioms ") == 6
    assert re.findall(r"(?m)^#print axioms (\w+)\s*$", tail) == list(EXPECTED)
    # Exact original fragments: only namespace/header/imports and module endings change.
    assert core.startswith(src[:a])
    assert middle.split(original_header, 1)[1].startswith(src[a:b])
    assert tail.split(original_header, 1)[1] == src[b:]
    folder = ROOT / "formal/Kuu/F112"
    paths = [folder / (name + ".lean") for name in (CORE, MIDDLE, TAIL)]
    assert all(not p.exists() for p in paths), "no overwrite of scratch Lean modules"
    for file, body in zip(paths, (core, middle, tail)):
        file.write_text(body)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "kuuos.codeai.v061.f112.14d.necessity_source_split.v1",
        "canonical_source_blob": SOURCE_BLOB,
        "canonical_source_sha256": sha(src),
        "original_fourteen_blob": ORIGINAL_FOURTEEN_BLOB,
        "original_full_source_unchanged": True,
        "six_original_declarations_unchanged": True,
        "all_six_original_axiom_audits_retained": True,
        "original_monolith_certified": False,
        "independent_ci_certified": False,
        "public_root_certified": False,
        "memory_verified_useful": False,
        "merge_authority": False,
        "stage_modules": [p.relative_to(ROOT).as_posix() for p in paths],
        "stage_sha256": [sha(t) for t in (core, middle, tail)],
        "original_fragments_sha256": [sha(t) for t in (src[:a],src[a:b],src[b:])],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest

def shim() -> dict:
    src = assert_original()
    m = json.loads((OUT / "manifest.json").read_text())
    assert m["canonical_source_sha256"] == sha(src)
    for path, expected in zip(m["stage_modules"], m["stage_sha256"]):
        assert sha((ROOT / path).read_text()) == expected
    text = (
        "import Kuu.F112." + TAIL + "\n"
        "#check Kuu.F112.Physical.nativeK5PentagonatorFourteenExchange\n"
        "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_relativeNecessity\n"
        "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_quotient_eq\n"
        "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_integerDescent\n"
        "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_historyNoDescent\n"
        "#check Kuu.F112.Physical.nativeK5PentagonatorFourteen_noCoreRetraction\n"
        "#print axioms Kuu.F112.Physical.nativeK5PentagonatorFourteen_noCoreRetraction\n"
    )
    p = OUT / "CanonicalNecessityShimScratch.lean"
    assert not p.exists(), "no scratch overwrite"
    p.write_text(text)
    return {"scratch_shim": p.relative_to(ROOT).as_posix(),
            "shim_sha256": sha(text), "original_source_unchanged": True,
            "original_monolith_certified": False}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("generate", "shim"), default="generate")
    args = parser.parse_args()
    result = render() if args.phase == "generate" else shim()
    print("CODEAI_F112_14D_NECESSITY_SPLIT", json.dumps(result, sort_keys=True), flush=True)
