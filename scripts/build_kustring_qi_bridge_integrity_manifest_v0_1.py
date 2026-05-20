#!/usr/bin/env python3
"""Build KuString Qi Bridge integrity manifest v0.1.

The manifest is generated from the full baseline chain index. It gives the
bridge a reproducible bundle root without granting any new authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "specs" / "kustring_qi_bridge_integrity_manifest_v0_1.generated.json"

CHAIN_FILES = [
    "examples/kustring_qi_bridge_minimal.py",
    "docs/KUSTRING_QI_BRIDGE_v0_1.md",
    "specs/kustring_qi_bridge_contract_v0_1.json",
    "validation_cases/kustring_qi_bridge_cases_v0_1.json",
    "scripts/validate_kustring_qi_bridge_v0_1.py",
    "specs/kustring_qi_bridge_release_bundle_manifest_v0_1.json",
    "specs/kustring_qi_bridge_release_packet_v0_1.json",
    "scripts/validate_kustring_qi_bridge_release_bundle_v0_1.py",
    "specs/kustring_qi_bridge_finality_packet_v0_1.json",
    "scripts/check_kustring_qi_bridge_finality_packet_v0_1.py",
    "specs/kustring_qi_bridge_chain_index_v0_1.json",
    "specs/kustring_qi_bridge_baseline_packet_v0_1.json",
    "specs/kustring_qi_bridge_baseline_established_final_packet_v0_1.json",
    "scripts/check_kustring_qi_bridge_chain_index_v0_1.py",
    "scripts/build_kustring_qi_bridge_integrity_manifest_v0_1.py",
    "scripts/validate_kustring_qi_bridge_integrity_manifest_v0_1.py",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_entry(rel_path: str) -> Dict[str, Any]:
    path = ROOT / rel_path
    data = path.read_bytes()
    return {
        "path": rel_path,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def build_manifest() -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = [file_entry(path) for path in CHAIN_FILES]
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "manifest_id": "kustring_qi_bridge_integrity_manifest_v0_1",
        "status": "generated_integrity_manifest",
        "module": "KuStringQiBridge",
        "version": "v0_1",
        "bundle_root_sha256": sha256_bytes(canonical),
        "entry_count": len(entries),
        "entries": entries,
        "authority_boundary": {
            "integrity_manifest_grants_execution_authority": False,
            "integrity_manifest_grants_truth_authority": False,
            "integrity_manifest_grants_theorem_authority": False,
            "integrity_manifest_grants_medical_act_authorization": False
        },
        "lineage_policy": {
            "same_root_required": True,
            "append_only": True,
            "overwrite_forbidden": True,
            "destructive_replacement_forbidden": True
        }
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())