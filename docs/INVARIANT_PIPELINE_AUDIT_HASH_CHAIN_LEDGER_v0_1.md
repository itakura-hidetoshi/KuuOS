# Invariant Pipeline Audit Hash-Chain Ledger v0.1

## 空OS Invariant Pipeline Audit Hash-Chain Ledger

This document defines the append-only hash-chain ledger for KuuOS Invariant Governance Pipeline audit events.

The ledger records audit events emitted by:

```text
Invariant Preservation Matrix
  -> Invariant Gate Runtime
  -> Invariant Governance Pipeline Audit Event
```

## 1. Core Principle

```text
Audit events become lineage records, not authority.
```

The hash-chain ledger improves tamper-evidence. It does not prove truth, grant execution authority, prove Ten'i, or replace WORM archival.

## 2. Ledger Entry Fields

Each ledger line is JSONL and must contain:

```yaml
ledger_entry:
  sequence: integer
  previous_hash: string
  event: object
  event_hash: string
  entry_hash: string
```

## 3. Hash Rules

### 3.1 Event Hash

```text
event_hash = sha256(canonical_json(event))
```

### 3.2 Entry Hash

```text
entry_hash = sha256(canonical_json({sequence, previous_hash, event_hash}))
```

### 3.3 Chain Rule

```text
entry[n].previous_hash == entry[n-1].entry_hash
```

For the first entry:

```text
previous_hash = GENESIS
```

## 4. Required Non-Authority Fields

Every event inside the ledger must preserve:

```text
execution_authority_granted: false
proof_authority_granted: false
clinical_authority_granted: false
truth_authority_granted: false
teni_authority_granted: false
```

## 5. Required Visibility

Every event must preserve:

```text
transformation_axis
required_invariants
violated_invariants
matrix_status
gate_status
gate_closed
required_repair_route
reason
```

## 6. Fixture

The public fixture is stored at:

```text
specs/invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl
```

## 7. Validation

Validated by:

```bash
python3 scripts/validate_invariant_pipeline_audit_hash_chain_v0_1.py
```

The validator checks:

```text
JSONL parses
sequence increments
previous_hash links correctly
event_hash matches canonical event
entry_hash matches canonical entry payload
non-authority fields remain false
required visibility fields exist
```

## 8. Guardrails

The ledger must not be used as:

- execution authority,
- proof authority,
- clinical authority,
- truth proof,
- Ten'i proof,
- replacement for evidence,
- replacement for WORM export,
- permission to hide harm.

## 9. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
