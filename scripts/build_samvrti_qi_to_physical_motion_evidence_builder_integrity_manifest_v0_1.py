#!/usr/bin/env python3
"""Build Samvrti Qi to Physical Motion evidence builder integrity manifest v0.1.

The chain index is the single source of truth for this integrity surface. The
builder derives entries from chain_indexes/samvrti_qi_to_physical_motion_evidence_builder_chain_index_v0_1.json
and computes a reproducible bundle root without granting new authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
BASE = "samvrti_qi_to_physical_motion_evidence_builder"
CHAIN_INDEX_PATH = ROOT / "chain_indexes" / f"{BASE}_chain_index_v0_1.json"
OUTPUT_PATH = ROOT / "specs" / f"{BASE}_integrity_manifest_v0_1.generated.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_chain_index() -> Dict[str, Any]:
    with CHAIN_INDEX_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def chain_files_from_index(chain_index: Dict[str, Any]) -> List[str]:
    entries = chain_index.get("chain_order", [])
    paths: List[str] = []
    for entry in entries:
        rel_path = entry.get("path")
        if not isinstance(rel_path, str) or not rel_path:
            raise ValueError("chain_order entry missing path")
        paths.append(rel_path)
    if len(paths) != len(set(paths)):
        raise ValueError("chain_order contains duplicate paths")
    return paths


def file_entry(rel_path: str) -> Dict[str, Any]:
    path = ROOT / rel_path
    data = path.read_bytes()
    return {
        "path": rel_path,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def build_manifest() -> Dict[str, Any]:
    chain_index = load_chain_index()
    chain_files = chain_files_from_index(chain_index)
    entries = [file_entry(path) for path in chain_files]
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "manifest_id": f"{BASE}_integrity_manifest_v0_1",
        "status": "generated_integrity_manifest",
        "module": "SamvrtiQiToPhysicalMotionEvidenceBuilder",
        "version": "v0_1",
        "source_of_truth": str(CHAIN_INDEX_PATH.relative_to(ROOT)),
        "chain_index_id": chain_index.get("chain_index_id"),
        "chain_stage_count": len(chain_files),
        "bundle_root_sha256": sha256_bytes(canonical),
        "entry_count": len(entries),
        "entries": entries,
        "authority_boundary": {
            "integrity_manifest_grants_execution_authority": False,
            "integrity_manifest_grants_truth_authority": False,
            "integrity_manifest_grants_theorem_authority": False,
            "integrity_manifest_grants_medical_act_authorization": False,
        },
        "lineage_policy": {
            "same_root_required": True,
            "append_only": True,
            "overwrite_forbidden": True,
            "destructive_replacement_forbidden": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write generated manifest to specs/")
    args = parser.parse_args()
    manifest = build_manifest()
    text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT_PATH.write_text(text, encoding="utf-8")
        print(f"WROTE: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"bundle_root_sha256: {manifest['bundle_root_sha256']}")
    print(f"entry_count: {manifest['entry_count']}")
    print(f"source_of_truth: {manifest['source_of_truth']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
