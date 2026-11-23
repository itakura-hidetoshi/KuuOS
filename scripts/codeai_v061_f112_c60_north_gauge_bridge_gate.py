#!/usr/bin/env python3
"""Original C60 north face + genuine K5 typed gauge: source-sealed Lean receipt.

This only certifies the two NEW local bridge declarations when independently
compiled. It NEVER certifies the 14D monolith, root Strict Lean, global descent
or the existence of the chosen five native F45 stages.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/codeai-v061-f112-c60-north-gauge"
SOURCE = ROOT / "formal/Kuu/F112/PolygonNativeC60NorthK5GaugeBoundaryBridge.lean"
SOURCE_BLOB = "1914712a6c47fa342fe6f2f72ff36137058e976c"
CANONICAL = {
    "formal/Kuu/F112/PolygonNativeC60PhysicalGaugeAtlas.lean":
        "14cd46eea79c1f06663c24ab4bae5877206aa669",
    "formal/Kuu/F112/PolygonNativeC60K5TypedGaugeCoherence.lean":
        "8539df6040d815345160b6a262fbad0327579201",
    "formal/Kuu/F112/PolygonNativeF55P94DK5FourteenCellNonabelianPasting.lean":
        "928b6f5bdb59c6ba74fbb8122666fc6e274f4d7c",
    "formal/KuuOSFormal.lean":
        "87ee2a7f541e48482e0d76f2abf819932c42f188",
}
EXPECTED = (
    "nativeC60NorthK5_gauge_invariance_and_typed_obstruction",
    "nativeC60NorthK5_nonflat_and_no_old_filler",
)
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REGEX_BAD = re.compile(r"(?im)(?:PANIC at |Lean panicked|^\s*(?:error|warning):|sorryAx)")
REGEX_AX = re.compile(r"depends on axioms:\s*\[([^\]]*)\]", re.S)

def blob(data:bytes)->str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def pinned_sources()->dict:
    import json
    raw=SOURCE.read_bytes()
    assert blob(raw)==SOURCE_BLOB, "original research bridge source changed"
    for p, expected in CANONICAL.items():
        assert blob((ROOT/p).read_bytes())==expected, "source pin mismatch: "+p
    assert (ROOT/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
    pkgs=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [p["rev"] for p in pkgs if p["name"]=="mathlib"]==[
      "5450b53e5ddc75d46418fabb605edbf36bd0beb6"]
    src=raw.decode()
    assert len(re.findall(r"(?m)^\s*\(t[1-5] : KuuNativeF45Tree \(\.pentagon \.north\)",src))==5
    assert re.findall(r"(?m)^#print axioms (nativeC60NorthK5_\w+)", src)==list(EXPECTED)
    assert re.findall(r"(?m)^theorem (nativeC60NorthK5_\w+)", src)==list(EXPECTED)
    assert not re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b",src)
    return {"source_blob":SOURCE_BLOB, "source_sha256":sha(raw),
            "canonical_blobs":CANONICAL,"pinned_lean":"v4.30.0-rc2",
            "pinned_mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
            "theorems":list(EXPECTED)}

def preflight()->int:
    x=pinned_sources()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"source-manifest.json").write_text(json.dumps(x,sort_keys=True,indent=2)+"\n")
    print("CODEAI_C60_NORTH_PREFLIGHT",json.dumps(x,sort_keys=True))
    return 0

def direct(*,independent:bool)->int:
    m=pinned_sources()
    prior=json.loads((OUT/"source-manifest.json").read_text())
    assert m==prior, "original source changed since preflight"
    proof=(OUT/"direct-lean.log").read_bytes()
    dep=(OUT/"dependency-build.log").read_bytes()
    full=(proof+dep).decode("utf-8","replace")
    rcs=[(OUT/f).read_text().strip() for f in ("dependency-exit.txt","direct-exit.txt")]
    bad=REGEX_BAD.findall(full)
    names=[f"'{name}'" for name in [f"Kuu.F112.Physical.{x}" for x in EXPECTED]]
    for name in names:
        assert name in full, "NO_DATA: missing Lean axiom audit: "+name
    ax=set()
    for item in REGEX_AX.findall(full):
        ax.update(a.strip() for a in item.split(",") if a.strip())
    if not ax.issubset(STANDARD_AXIOMS):
        bad.append("nonstandard axioms "+str(sorted(ax-STANDARD_AXIOMS)))
    olean=ROOT/".lake/build/lib/lean/Kuu/F112/PolygonNativeC60NorthK5GaugeBoundaryBridge.olean"
    if not olean.is_file() or olean.stat().st_size==0:
        bad.append("missing compiled .olean")
    if rcs!=["0","0"]:
        bad.append("nonzero exit codes "+repr(rcs))
    result={**m, "schema":"kuuos.codeai.v061.c60.north.local.v1",
        "scope":"C60_NORTH_PHY_GAUGE_AND_NINE_TYPED_K5_FACE_CO_OBSERVATION_ONLY",
        "status":"LOCAL_LEAN_CLEAN" if not bad else "HOLD_LEAN_OBSTRUCTION",
        "independent_runner":independent,"direct_lean_rc":rcs[1],
        "dependency_build_rc":rcs[0],
        "diagnostic_count":len(bad),"diagnostics":bad[:12],
        "axioms":sorted(ax),"direct_log_sha256":sha(proof),
        "dependency_log_sha256":sha(dep),
        "original_14d_monolith_certified":False,"public_root_certified":False,
        "formal_adoption":False,"memory_verified_useful":False,"merge_authority":False}
    if independent:
        first=json.loads((ROOT/"first-sandbox/c60-north-local-receipt.json").read_text())
        assert first["status"]=="LOCAL_LEAN_CLEAN" and not first["independent_runner"]
        for key in ("source_blob","source_sha256","canonical_blobs","theorems","axioms","pinned_lean","pinned_mathlib"):
            assert result[key]==first[key], "fresh vs sandbox source/proof mismatch: "+key
    (OUT/("c60-north-independent-receipt.json" if independent else "c60-north-local-receipt.json")).write_text(
        json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("CODEAI_C60_NORTH_LEAN",json.dumps(result,sort_keys=True))
    return 0 if not bad else 1

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase",choices=("preflight","direct"),required=True)
    ap.add_argument("--independent",action="store_true")
    args=ap.parse_args()
    raise SystemExit(preflight() if args.phase=="preflight" else direct(independent=args.independent))
