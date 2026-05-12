#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "specs" / "provider_boundary_bundle_v0_1.generated.json"

FILES = [
    "docs/AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_EVENT_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/PROVIDER_BOUNDARY_BUNDLE_v0_1.md",
    "specs/ai_provider_boundary_fixtures_v0_1.json",
    "specs/ai_provider_boundary_audit_hash_chain_fixture_v0_1.jsonl",
    "specs/ai_provider_boundary_audit_worm_export_receipt_fixture_v0_1.json",
    "scripts/validate_ai_provider_boundary_runtime_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_event_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_hash_chain_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_worm_export_receipt_v0_1.py",
    "scripts/build_provider_boundary_bundle_v0_1.py",
    "scripts/validate_provider_boundary_bundle_v0_1.py",
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
    root_payload = "".join(x["path"] + x["sha256"] for x in entries)
    manifest = {
        "id": "provider_boundary_bundle_v0_1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_note": "integrity_surface_only",
        "files": entries,
        "bundle_root_hash": hashlib.sha256(root_payload.encode("utf-8")).hexdigest(),
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
