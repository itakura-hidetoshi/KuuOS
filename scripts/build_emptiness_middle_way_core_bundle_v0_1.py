#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "specs" / "emptiness_middle_way_core_bundle_v0_1.generated.json"

FILES = [
    "docs/EMPTINESS_DEPENDENT_ORIGINATION_TWO_TRUTHS_MIDDLE_WAY_CORE_v0_1.md",
    "docs/EMPTINESS_MIDDLE_WAY_CORE_AUDIT_EVENT_v0_1.md",
    "docs/EMPTINESS_MIDDLE_WAY_CORE_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/EMPTINESS_MIDDLE_WAY_CORE_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/EMPTINESS_MIDDLE_WAY_CORE_BUNDLE_v0_1.md",
    "specs/emptiness_middle_way_core_fixtures_v0_1.json",
    "specs/emptiness_middle_way_core_audit_hash_chain_fixture_v0_1.jsonl",
    "specs/emptiness_middle_way_core_audit_worm_export_receipt_fixture_v0_1.json",
    "scripts/validate_emptiness_middle_way_core_v0_1.py",
    "scripts/validate_emptiness_middle_way_core_audit_event_v0_1.py",
    "scripts/validate_emptiness_middle_way_core_audit_hash_chain_v0_1.py",
    "scripts/validate_emptiness_middle_way_core_audit_worm_export_receipt_v0_1.py",
    "scripts/build_emptiness_middle_way_core_bundle_v0_1.py",
    "scripts/validate_emptiness_middle_way_core_bundle_v0_1.py"
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    entries = []
    for rel in sorted(FILES):
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        entries.append({"path": rel, "sha256": sha256_file(path), "size_bytes": path.stat().st_size})
    root_payload = "".join(item["path"] + item["sha256"] for item in entries)
    manifest = {
        "id": "emptiness_middle_way_core_bundle_v0_1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_note": "integrity_surface_only",
        "files": entries,
        "bundle_root_hash": hashlib.sha256(root_payload.encode("utf-8")).hexdigest()
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
