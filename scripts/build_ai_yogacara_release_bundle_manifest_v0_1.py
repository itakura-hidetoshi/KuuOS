#!/usr/bin/env python3
"""
build_ai_yogacara_release_bundle_manifest_v0_1.py

Builds a JSON release bundle manifest for the KuuOS AI Yogacara / Ten'i layer.

Stdlib-only. No external API calls.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "specs" / "ai_yogacara_release_bundle_manifest_v0_1.generated.json"

BUNDLE_FILES = [
    "docs/YOGACARA_AI_RAW_LAYER_BOUNDARY_v0_1.md",
    "docs/META_MANAS_AI_SELF_FIXATION_OBSERVER_v0_1.md",
    "docs/TENI_AI_ALAYA_TRANSFORMATION_v0_1.md",
    "docs/KUNJU_AI_ALAYA_CONDITIONING_LOOP_v0_1.md",
    "docs/TENI_EVIDENCE_LEDGER_v0_1.md",
    "docs/AI_ALAYA_SEED_TAXONOMY_v0_1.md",
    "docs/AI_ALAYA_SEED_LEDGER_v0_1.md",
    "docs/TENI_PROMOTION_GATE_v0_1.md",
    "docs/TENI_RUNTIME_PROTOCOL_v0_1.md",
    "docs/TENI_PROBE_SUITE_v0_1.md",
    "docs/AI_CONTROL_SURFACE_REGISTRY_v0_1.md",
    "docs/TENI_METRICS_OBSERVABILITY_v0_1.md",
    "docs/TENI_OBSERVABILITY_VALIDATION_INDEX_v0_1.md",
    "docs/TENI_OBSERVABILITY_CI_GUIDE_v0_1.md",
    "docs/TENI_AI_YOGACARA_RELEASE_PACKET_v0_1.md",
    "docs/AI_YOGACARA_RUNTIME_ADAPTER_CONTRACT_v0_1.md",
    "docs/AI_YOGACARA_ADAPTER_AUDIT_EVENT_v0_1.md",
    "docs/AI_YOGACARA_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/AI_YOGACARA_AUDIT_WORM_EXPORT_MANIFEST_v0_1.md",
    "docs/AI_YOGACARA_RELEASE_BUNDLE_MANIFEST_v0_1.md",
    "specs/teni_validation_cases_v0_1.yaml",
    "specs/teni_prometheus_alert_rules_v0_1.yaml",
    "specs/ai_yogacara_runtime_adapter_schema_v0_1.yaml",
    "specs/ai_yogacara_adapter_fixtures_v0_1.json",
    "specs/ai_yogacara_audit_hash_chain_fixture_v0_1.jsonl",
    "specs/ai_yogacara_audit_worm_export_receipt_fixture_v0_1.yaml",
    "scripts/validate_teni_observability_v0_1.py",
    "scripts/validate_ai_yogacara_adapter_schema_v0_1.py",
    "scripts/validate_ai_yogacara_adapter_fixtures_v0_1.py",
    "scripts/validate_ai_yogacara_adapter_audit_event_v0_1.py",
    "scripts/validate_ai_yogacara_audit_hash_chain_v0_1.py",
    "scripts/validate_ai_yogacara_worm_export_receipt_v0_1.py",
    "scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py",
    "examples/ai_yogacara_runtime_adapter_minimal.py",
    "tests/test_ai_yogacara_runtime_adapter_minimal_v0_1.py",
    ".github/workflows/teni_observability_validation.yml",
    ".github/pull_request_template.md",
]

FIXED_POINTS = [
    "release_bundle_manifest_is_integrity_surface_not_authority",
    "bundle_root_hash_proves_file_set_integrity_not_truth",
    "bundle_manifest_does_not_prove_teni_occurrence",
    "bundle_manifest_does_not_grant_execution_authority",
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest() -> dict:
    files = []
    for rel in sorted(BUNDLE_FILES):
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        files.append({
            "path": rel,
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })

    root_payload = "".join(f["path"] + f["sha256"] for f in files)
    bundle_root_hash = hashlib.sha256(root_payload.encode("utf-8")).hexdigest()

    return {
        "id": "ai_yogacara_release_bundle_manifest_v0_1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bundle_version": "0.1",
        "files": files,
        "bundle_root_hash": bundle_root_hash,
        "authority_note": "integrity_surface_not_authority",
        "fixed_points": FIXED_POINTS,
    }


def main() -> int:
    manifest = build_manifest()
    OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUTPUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
