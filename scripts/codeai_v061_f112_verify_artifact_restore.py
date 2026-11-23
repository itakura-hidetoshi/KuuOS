#!/usr/bin/env python3
"""CodeAI v0.61 F112: verify a historical pinned Lean dependency artifact.

Read-only provenance checks precede extraction. This canonical-main-root verifier MUST REJECT the old research-root 193-olean artifact. The artifact is permitted
only as an accelerator of a NEW direct independent Lean kernel run; it is not
a verification receipt, a theorem, or an authorization to promote Memory.
No repository source, Lean declaration, or Git ref is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BLOBS = {
    "formal/Kuu/F112/PolygonNativeF55P94DK5FourteenCellNonabelianPasting.lean":
        "928b6f5bdb59c6ba74fbb8122666fc6e274f4d7c",
    "formal/KuuOSFormal.lean":
        "f8c348ec9c8e76c4c02dd2c1623a633def52f948",
    "formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean":
        "c70aa395d14d873c686008bd80c835c059f936d5",
}
LEAN = "leanprover/lean4:v4.30.0-rc2"
MATHLIB = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as file:
        for part in iter(lambda:file.read(2**20), b""):
            h.update(part)
    return h.hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()


def verify_source() -> None:
    for path, expected in SOURCE_BLOBS.items():
        data=(ROOT/path).read_bytes()
        assert git_blob(data)==expected, "original_source_changed:"+path
    assert (ROOT/"lean-toolchain").read_text().strip()==LEAN, "lean_toolchain_changed"
    pkgs=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [p["rev"] for p in pkgs if p["name"]=="mathlib"]==[MATHLIB], "mathlib_changed"


def safe_tar_entries(path: Path) -> None:
    r=subprocess.run(["tar","--zstd","-tf",str(path)],capture_output=True,text=True,check=True)
    entries=r.stdout.splitlines()
    assert entries, "NO_DATA: empty archived build"
    for item in entries:
        rel=PurePosixPath(item)
        assert not rel.is_absolute(), "absolute_archive_path"
        assert ".." not in rel.parts, "traversal_archive_path"
        assert rel.parts[0]=="build", "archive_outside_build"
    r=subprocess.run(["tar","--zstd","-tvf",str(path)],capture_output=True,text=True,check=True)
    for item in r.stdout.splitlines():
        assert item and item[0] in ("-","d"), "archive_contains_link_or_special_file"


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-dir",type=Path,required=True)
    ap.add_argument("--expected-producer-head",required=True)
    ap.add_argument("--receipt-path",type=Path,required=True)
    args=ap.parse_args()
    verify_source()
    folder=args.artifact_dir.resolve()
    manifest=json.loads((folder/"manifest.json").read_text())
    index_path=folder/"olean-index.json"
    archive=folder/"lake-build-prefix.tar.zst"
    check=folder/"lake-build-prefix.tar.zst.sha256"
    assert len(args.expected_producer_head)==40 and all(c in "0123456789abcdef" for c in args.expected_producer_head), "invalid_expected_head"
    assert manifest["head"]==args.expected_producer_head, "producer_head_mismatch"
    assert manifest["schema"]=="codeai.v061.f112.durable_olean_progress.v3", "wrong_manifest_schema"
    assert manifest["lean"]=="v4.30.0-rc2" and manifest["mathlib"]==MATHLIB, "artifact_toolchain_mismatch"
    assert manifest["changes_to_formal"] is False and manifest["changes_to_public_root"] is False
    for path,expected in SOURCE_BLOBS.items():
        assert manifest["source"][path]["blob"]==expected, "artifact_source_mismatch:"+path
        assert manifest["source"][path]["sha256"]==sha256(ROOT/path), "artifact_source_bytes_differ:"+path
    metadata=manifest["archive"]
    assert metadata["format"]=="tar.zst" and metadata["formal_certification"]=="HOLD"
    assert metadata["sha256"]==sha256(archive), "archive_sha256_mismatch"
    assert metadata["index_sha256"]==sha256(index_path), "olean_index_sha256_mismatch"
    assert check.read_text().split()[0]==metadata["sha256"], "sha256sum_manifest_mismatch"
    index=json.loads(index_path.read_text())
    assert len(index)==metadata["olean_count"] and len(index)>0, "olean_count_mismatch"
    paths=set()
    for entry in index:
        rel=PurePosixPath(entry["path"])
        assert rel.parts[:4]==(".lake","build","lib","lean"), "invalid_olean_file_path"
        assert rel.suffix==".olean" and ".." not in rel.parts, "invalid_olean_filename"
        assert entry["path"] not in paths, "duplicate_olean_path"
        assert len(entry["sha256"])==64 and entry["size_bytes"]>0
        paths.add(entry["path"])
    safe_tar_entries(archive)
    target=ROOT/".lake/build/lib/lean"
    assert not target.exists() or not any(target.rglob("*.olean")), "forbidden_existing_compiled_prefix_overwrite"
    subprocess.run(["tar","--zstd","--no-same-owner","-xf",str(archive),"-C",str(ROOT/".lake")],check=True)
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/".lake/build/lib/lean").rglob("*.olean")}
    assert actual==paths, "restored_olean_file_set_mismatch"
    for e in index:
        p=ROOT/e["path"]
        assert p.stat().st_size==e["size_bytes"] and sha256(p)==e["sha256"], "restored_olean_digest_mismatch:"+e["path"]
    receipt={
        "schema":"codeai.v061.f112.durable_olean_import.v1",
        "expected_producer_head":args.expected_producer_head,
        "archive_sha256":metadata["sha256"],
        "source_git_blobs":SOURCE_BLOBS,
        "olean_count":len(actual),
        "lean":LEAN,"mathlib":MATHLIB,
        "artifact_integrity_verified":True,
        "local_lean_certified":False,
        "root_strict_lean_certified":False,
        "verified_useful_memory":"HOLD",
        "merge_authority":False,
    }
    args.receipt_path.parent.mkdir(parents=True,exist_ok=True)
    args.receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("CODEAI_F112_ARCHIVE_INTEGRITY",json.dumps(receipt,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
