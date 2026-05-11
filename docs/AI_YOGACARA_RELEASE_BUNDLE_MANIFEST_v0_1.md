# AI Yogacara Release Bundle Manifest v0.1

## AI唯識・転依リリースバンドル manifest

This document defines the release bundle manifest for the KuuOS AI Yogacara / Ten'i layer.

The bundle manifest lists the public release-surface files and their SHA256 digests so that the layer can be archived, cited, mirrored, or WORM-exported as a coherent unit.

## 1. Core Principle

```text
A release bundle manifest proves file integrity of a release surface.
It does not prove truth, Ten'i occurrence, execution authority, clinical authority, or base-model transformation.
```

## 2. Bundle Scope

The AI Yogacara / Ten'i release bundle includes:

```text
Yogacara raw-layer boundary
Meta-Manas observer
Ten'i transformation docs
Kunju conditioning loop
Seed taxonomy and seed ledger
Ten'i evidence ledger
Ten'i promotion gate
Ten'i runtime protocol
Probe suite
AI control surface registry
Metrics and observability
Validation cases
Prometheus alert rules
Runtime adapter contract
Minimal adapter implementation
Adapter schema
Adapter fixtures
Adapter audit event
Audit hash-chain ledger
WORM export manifest and receipt fixture
CI workflow
Release packet and PR checklist
```

## 3. Manifest Shape

```json
{
  "id": "ai_yogacara_release_bundle_manifest_v0_1",
  "generated_at": "ISO-8601 timestamp",
  "bundle_version": "0.1",
  "files": [
    {
      "path": "docs/...",
      "sha256": "...",
      "size_bytes": 1234
    }
  ],
  "bundle_root_hash": "SHA256 of ordered file digest lines",
  "authority_note": "integrity_surface_not_authority"
}
```

## 4. Bundle Root Hash

The bundle root hash is order-sensitive.

```text
bundle_root_hash = SHA256(path_1 || sha256_1 || path_2 || sha256_2 || ...)
```

Files are ordered lexicographically by path.

## 5. Required Non-Authority Statement

Every bundle manifest must preserve:

```text
release_bundle_manifest_is_integrity_surface_not_authority
bundle_root_hash_proves_file_set_integrity_not_truth
bundle_manifest_does_not_prove_teni_occurrence
bundle_manifest_does_not_grant_execution_authority
```

## 6. Local Commands

Build manifest:

```bash
python3 scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py
```

Validate manifest generation:

```bash
python3 scripts/validate_ai_yogacara_release_bundle_manifest_v0_1.py
```

## 7. Guardrails

The release bundle manifest must not be used as:

- proof of truth,
- proof of Ten'i occurrence,
- proof authority,
- belief authority,
- clinical authority,
- execution authority,
- base-model transformation evidence by itself.

It is a file-integrity and release-surface continuity artifact.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
