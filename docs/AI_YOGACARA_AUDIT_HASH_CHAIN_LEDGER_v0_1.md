# AI Yogacara Audit Hash Chain Ledger v0.1

## AI唯識監査ハッシュ鎖台帳

This document defines an append-only hash-chain ledger for AI Yogacara Runtime Adapter audit events.

The adapter already records raw AI output as candidate and explicitly marks all authority fields as false. The hash-chain ledger makes that trace harder to silently rewrite.

## 1. Core Principle

```text
Audit events are append-only trace surfaces.
They are not authority.
```

The ledger preserves the sequence of adapter decisions:

```text
raw output
  -> candidate status
  -> Meta-Manas signals
  -> seed classifications
  -> non-authority fields
  -> audit event
  -> hash-chain ledger
```

## 2. Ledger Entry

Each ledger entry includes:

```yaml
ai_yogacara_audit_hash_chain_entry:
  previous_hash: string
  event_id: string
  timestamp: string
  request_id: string
  ai_system: string
  model_or_agent_id: string
  raw_output_ref: string
  raw_output_status: candidate
  meta_manas_signals: list
  seed_classifications: list
  allowed_next_status: list
  governance_route: list
  authority_granted: false
  proof_authority_granted: false
  decision_authority_granted: false
  execution_authority_granted: false
  memory_truth_granted: false
  belief_authority_granted: false
  event_hash: string
```

## 3. Hash Rule

```text
event_hash = SHA256(canonical_json(entry_without_event_hash))
```

The canonical JSON representation uses sorted keys and compact separators.

## 4. Chain Rule

```text
entry[n].previous_hash == entry[n-1].event_hash
```

The first entry may use:

```text
previous_hash = GENESIS
```

## 5. Non-Authority Rule

Every ledger entry must explicitly preserve:

```text
authority_granted: false
proof_authority_granted: false
decision_authority_granted: false
execution_authority_granted: false
memory_truth_granted: false
belief_authority_granted: false
```

## 6. Uses

The hash-chain ledger supports:

- later audit review,
- detection of event rewrite,
- rollback analysis,
- Ten'i evidence linkage,
- CI fixture validation,
- WORM-style external archival when available.

## 7. Guardrails

The ledger must not be used as:

- execution authority,
- proof authority,
- belief authority,
- clinical authority,
- hidden scoring authority,
- final truth certification.

A valid hash chain proves structural continuity of the ledger, not truth of the content.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
