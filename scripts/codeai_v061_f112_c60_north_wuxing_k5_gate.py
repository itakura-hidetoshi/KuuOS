#!/usr/bin/env python3
"""Exact-source five-phase C60/K5 bridge gate: direct Lean then independent.

Proof scope is ONE conditional theorem with five original typed F45 inputs,
NOT an asserted identification of physical/phase/higher gauges.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/codeai-v061-f112-c60-north-wuxing-k5"
SOURCE = "formal/Kuu/F112/PolygonNativeC60NorthWuxingK5TripleGaugeBridge.lean"
TARGET_BLOB = "e9bc8cf34d81351c55a95ebdba4c9752ba645fb4"
CANONICAL = {
    "formal/KUOS/Architecture/QiWuxingNativeC60GaugeV3_4.lean":
        "836a0cccc0263e33d652da6b9391e4d5c07cb368",
    "formal/Kuu/F112/PolygonNativeC60NorthK5GaugeBoundaryBridge.lean":
        "1914712a6c47fa342fe6f2f72ff36137058e976c",
    "formal/Kuu/F112/PolygonNativeC60PhysicalGaugeAtlas.lean":
        "14cd46eea79c1f06663c24ab4bae5877206aa669",
    "formal/Kuu/F112/PolygonNativeC60K5TypedGaugeCoherence.lean":
        "8539df6040d815345160b6a262fbad0327579201",
    "formal/Kuu/F112/PolygonNativeF55P94DK5FourteenCellNonabelianPasting.lean":
        "928b6f5bdb59c6ba74fbb8122666fc6e274f4d7c",
    "formal/KuuOSFormal.lean":
        "87ee2a7f541e48482e0d76f2abf819932c42f188",
}
NAME = "nativeC60NorthWuxingK5_threeGauge_obstructions"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}
BAD = re.compile(r"(?im)(?:PANIC at |Lean panicked|^\s*(?:error|warning):|sorryAx)")
AXIOMS = re.compile(r"depends on axioms:\s*\[([^\]]*)\]", re.S)

def git_blob(b: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def sha(b: bytes)->str:
    return hashlib.sha256(b).hexdigest()

def guard()->dict:
    raw=(ROOT/SOURCE).read_bytes()
    assert git_blob(raw)==TARGET_BLOB, "candidate source blob mismatch"
    for path,blob in CANONICAL.items():
        assert git_blob((ROOT/path).read_bytes())==blob, "source drift: "+path
    assert (ROOT/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
    pkgs=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [p["rev"] for p in pkgs if p["name"]=="mathlib"]==[
        "5450b53e5ddc75d46418fabb605edbf36bd0beb6"]
    text=raw.decode()
    assert len(re.findall(r"(?m)^\s*\(t[1-5] : KuuNativeF45Tree \(\.pentagon \.north\)",text))==5
    assert re.findall(r"(?m)^theorem (nativeC60NorthWuxingK5_\w+)",text)==[NAME]
    assert re.findall(r"(?m)^#print axioms (nativeC60NorthWuxingK5_\w+)",text)==[NAME]
    assert not re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",text)
    return {
        "schema":"kuuos.codeai.v061.c60.north.wuxing_k5.pin.v1",
        "source_blob":TARGET_BLOB,
        "source_sha256":sha(raw),
        "original_blobs":CANONICAL,
        "theorem":NAME,
        "lean":"v4.30.0-rc2",
        "mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "scope":"genuine C60 north-fivefold local phases, incidence-gauge and typed K5 witness",
        "identifies_gauges":False,
        "original_14d_certified":False,
        "full_root_certified":False,
        "merge_authority":False
    }

def preflight()->int:
    o=guard()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"manifest.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")
    print("CODEAI_F112_C60_WUXING_PREFLIGHT",json.dumps(o,sort_keys=True),flush=True)
    return 0

def verify(independent:bool)->int:
    expected=guard()
    manifest=json.loads((OUT/"manifest.json").read_text())
    assert manifest==expected,"pin mismatch after source preflight"
    dep_log=(OUT/"dependency-build.log").read_bytes()
    direct_log=(OUT/"direct-lean.log").read_bytes()
    raw=(dep_log+direct_log).decode("utf-8","replace")
    codes=[(OUT/n).read_text().strip() for n in ("dependency-exit.txt","direct-exit.txt")]
    issues=[]
    if codes!=["0","0"]: issues.append("nonzero rc "+str(codes))
    issues.extend([m.group(0) for m in BAD.finditer(raw)])
    if "'Kuu.F112.Physical."+NAME+"'" not in raw:
        issues.append("NO_DATA: missing theorem axiom print")
    olean=ROOT/".lake/build/lib/lean/Kuu/F112/PolygonNativeC60NorthWuxingK5TripleGaugeBridge.olean"
    if not olean.exists() or olean.stat().st_size==0:
        issues.append("NO_DATA: missing independent olean")
    axioms=set()
    for found in AXIOMS.findall(raw):
        axioms.update(x.strip() for x in found.split(",") if x.strip())
    if not axioms.issubset(STANDARD):
        issues.append("unexpected axioms "+str(sorted(axioms-STANDARD)))
    result={**expected,
        "status":"LOCAL_LEAN_CLEAN" if not issues else "HOLD_SOURCE_OR_LEAN_DIAGNOSTICS",
        "proven_scope":"ONE C60_WUXING_K5_CONDITIONAL_THEOREM_ONLY",
        "independent_runner":independent,
        "axioms":sorted(axioms),
        "diagnostic_count":len(issues),
        "diagnostics":issues[:8],
        "dependency_rc":codes[0],"direct_lean_rc":codes[1],
        "dependency_log_sha256":sha(dep_log),
        "direct_log_sha256":sha(direct_log),
        "original_14d_certified":False,
        "full_root_certified":False,
        "memory_verified_useful":False,
        "formal_adoption":False,
        "merge_authority":False
    }
    if independent:
        first=json.loads((ROOT/"first-sandbox/local-receipt.json").read_text())
        assert first["status"]=="LOCAL_LEAN_CLEAN" and first["independent_runner"] is False
        for key in ("source_blob","source_sha256","original_blobs","theorem","axioms","lean","mathlib"):
            assert result[key]==first[key], "independent source or axiom mismatch: "+key
    file="independent-receipt.json" if independent else "local-receipt.json"
    (OUT/file).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("CODEAI_F112_C60_WUXING_LEAN",json.dumps(result,sort_keys=True),flush=True)
    return 0 if not issues else 1

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase",required=True,choices=("preflight","direct"))
    ap.add_argument("--independent",action="store_true")
    args=ap.parse_args()
    raise SystemExit(preflight() if args.phase=="preflight" else verify(args.independent))
