#!/usr/bin/env python3
"""KuuOS CodeAI v0.61 F112 five-stage *proposal-only* localization.

Read the exact, immutable original 353-line Lean module, change one
five-stage declaration only in a throwaway fragment, and retain the
original source and all independent proof definitions unchanged.

This does not certify the source module, public root, or learned memory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("formal/Kuu/F112/PolygonNativeF55P94DK5FourteenCellNonabelianPasting.lean")
ORIGINAL_BLOB = "928b6f5bdb59c6ba74fbb8122666fc6e274f4d7c"
ROOT_BLOB = "87ee2a7f541e48482e0d76f2abf819932c42f188"
MODEL_A_BLOB = "c70aa395d14d873c686008bd80c835c059f936d5"
MATHLIB = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"

ORIGINAL = """def nativeK5PentagonatorFifteenLeftFirst :=
  nativeK5FourteenPastingLeftThenRight
    (nativeK5PentagonatorFifteenExchangeFourteen t1 t2 t3 t4 t5)"""

REPLACEMENTS = {
    "direct-square": """def nativeK5PentagonatorFifteenLeftFirst :=
  nativeK5FourteenPastingLeftThenRight
    (NativeK5StructuralFourteenCell.squareExchange
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5))""",
    "local-let": """def nativeK5PentagonatorFifteenLeftFirst :=
  let W := nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5
  nativeK5FourteenPastingLeftThenRight
    (NativeK5StructuralFourteenCell.squareExchange W)""",
    "typed-result": """def nativeK5PentagonatorFifteenLeftFirst :
    (let W := nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5
     NativeK5StructuralFourteenCell p
       (.trans (nativeK5ThirteenPastingLeftThenRight W)
         (.symm (nativeK5ThirteenPastingLeftThenRight W)))
       (.trans (nativeK5ThirteenPastingRightThenLeft W)
         (.symm (nativeK5ThirteenPastingRightThenLeft W)))) :=
  nativeK5FourteenPastingLeftThenRight
    (nativeK5PentagonatorFifteenExchangeFourteen t1 t2 t3 t4 t5)""",
}


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def check_exact_source() -> str:
    data = (ROOT / SOURCE).read_bytes()
    assert git_blob(data) == ORIGINAL_BLOB, "immutable_original_blob_mismatch"
    assert git_blob((ROOT / "formal/KuuOSFormal.lean").read_bytes()) == ROOT_BLOB
    assert git_blob((ROOT / "formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean").read_bytes()) == MODEL_A_BLOB
    assert (ROOT / "lean-toolchain").read_text().strip() == "leanprover/lean4:v4.30.0-rc2"
    packages = json.loads((ROOT / "lake-manifest.json").read_text())["packages"]
    mathlib = [p for p in packages if p["name"] == "mathlib"]
    assert len(mathlib) == 1 and mathlib[0]["rev"] == MATHLIB
    source = data.decode("utf-8")
    # The pinned source has 352 nonempty-or-blank physical lines plus final LF.
    assert source.endswith("\n"), "unexpected_source_line_ending"
    assert len(source.splitlines()) == 352
    assert source.count(ORIGINAL) == 1
    return source


def produce(candidate: str, out: Path) -> dict:
    source = check_exact_source()
    marker = "def nativeK5PentagonatorFifteenRightFirst :="
    assert source.count(marker) == 1
    source_prefix = source.split(marker, 1)[0]
    assert source_prefix.count(ORIGINAL) == 1
    assert "end GenuineFourteenPasting\n" in source_prefix
    assert "section GenuineFiveStage\n" in source_prefix
    replacement = REPLACEMENTS[candidate]
    fragment = source_prefix.replace(ORIGINAL, replacement) + (
        "\nend GenuineFiveStage\n\nend\nend Kuu.F112.Physical\n"
    )
    out.mkdir(parents=True, exist_ok=True)
    (out / "Candidate.lean").write_text(fragment)
    manifest = {
        "schema": "codeai.v061.f112.fivestage.leftfirst.candidate.v2",
        "candidate": candidate,
        "original_git_blob": ORIGINAL_BLOB,
        "original_source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "candidate_sha256": hashlib.sha256(fragment.encode()).hexdigest(),
        "original_source_lines": len(source.splitlines()),
        "source_prefix_lines": len(source_prefix.splitlines()),
        "replacement": replacement,
        "fourteen_cell_core_unchanged": True,
        "original_repository_lean_unchanged": True,
        "kind": "candidate_proposal_only",
        "local_compile": "TEST_REQUIRED",
        "formal_four_family_evidence": "HOLD",
        "verified_useful_memory": "HOLD",
        "full_original_module": "HOLD",
        "full_public_root": "HOLD",
        "merge_authority": False,
        "mathlib": MATHLIB,
        "lean": "v4.30.0-rc2",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", choices=sorted(REPLACEMENTS), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print("CODEAI_F112_CANDIDATE", json.dumps(produce(args.candidate, args.output), sort_keys=True))
