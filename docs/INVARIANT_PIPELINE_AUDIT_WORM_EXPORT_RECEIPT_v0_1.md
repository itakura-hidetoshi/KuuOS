# Invariant Pipeline Audit WORM Export Receipt v0.1

## 空OS Invariant Pipeline Audit WORM Export Receipt

This document defines the WORM export receipt for the KuuOS Invariant Pipeline Audit Hash-Chain Ledger.

The receipt records the exported ledger root and confirms that the audit lineage is treated as an immutable archival surface.

## 1. Core Principle

```text
WORM export preserves lineage. It does not create authority.
```

The receipt is an archival integrity surface. It does not prove truth, grant execution authority, prove Ten'i, or replace evidence.

## 2. Receipt Fields

```yaml
receipt:
  id: string
  version: string
  exported_at: string
  source_ledger: string
  source_ledger_root_hash: string
  exported_entry_count: integer
  export_mode: WORM
  retention_policy: string
  object_lock_mode: compliance | governance | local_fixture
  non_authority_note: string
  execution_authority_granted: false
  proof_authority_granted: false
  clinical_authority_granted: false
  truth_authority_granted: false
  teni_authority_granted: false
```

## 3. Public Fixture

The public receipt fixture is stored at:

```text
specs/invariant_pipeline_audit_worm_export_receipt_fixture_v0_1.json
```

## 4. Validation

Validated by:

```bash
python3 scripts/validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py
```

The validator checks:

```text
source ledger exists
source ledger hash-chain validates
receipt source_ledger_root_hash matches computed ledger root
exported_entry_count matches JSONL entry count
export_mode is WORM
non-authority fields remain false
```

## 5. Guardrails

The WORM export receipt must not be used as:

- execution authority,
- proof authority,
- clinical authority,
- truth proof,
- Ten'i proof,
- replacement for evidence,
- permission to hide harm,
- permission to bypass governance.

## 6. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
