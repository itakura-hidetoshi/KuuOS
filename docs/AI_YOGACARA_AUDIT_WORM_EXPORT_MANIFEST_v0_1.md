# AI Yogacara Audit WORM Export Manifest v0.1

## AI唯識監査 WORM エクスポート manifest

This document defines the export manifest for moving AI Yogacara audit hash-chain ledgers into WORM-style archival surfaces.

The ledger is an append-only trace surface. Exporting it to WORM storage strengthens preservation, but does not turn the ledger into truth authority.

## 1. Core Principle

```text
WORM export preserves trace continuity.
It does not create proof, belief, decision, clinical, or execution authority.
```

## 2. Export Unit

An export unit contains:

```yaml
ai_yogacara_worm_export_unit:
  export_id: string
  created_at: string
  ledger_ref: string
  ledger_entry_count: integer
  first_event_hash: string
  last_event_hash: string
  chain_root_hash: string
  validator_ref: string
  validation_status: PASS | FAIL | HOLD
  storage_target: local | s3_object_lock | zenodo | institutional_worm | other
  retention_policy: string
  authority_note: trace_surface_not_authority
```

## 3. Chain Root Hash

The chain root hash is calculated from the ordered list of event hashes.

```text
chain_root_hash = SHA256(event_hash_1 || event_hash_2 || ... || event_hash_n)
```

The order is part of the root.

## 4. Export Receipt

The export receipt records:

```yaml
ai_yogacara_worm_export_receipt:
  export_id: string
  ledger_ref: string
  chain_root_hash: string
  last_event_hash: string
  validation_status: PASS | FAIL | HOLD
  exported_at: string
  storage_target: string
  retention_policy: string
  non_authority_statement: true
```

## 5. Required Non-Authority Statement

Each export must preserve:

```text
valid_hash_chain_proves_structural_continuity_not_truth
worm_export_preserves_trace_not_authority
```

## 6. WORM Targets

Potential export targets include:

```text
local immutable archive
S3 Object Lock / Compliance mode
institutional WORM archive
Zenodo-style release archive
external notarization surface
```

The public repository only defines the manifest. Actual storage configuration is environment-specific.

## 7. Guardrails

WORM export must not be used as:

- proof of truth,
- proof of Ten'i occurrence,
- execution authority,
- clinical authority,
- base-model transformation proof,
- replacement for governance review.

It preserves audit trace continuity only.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
