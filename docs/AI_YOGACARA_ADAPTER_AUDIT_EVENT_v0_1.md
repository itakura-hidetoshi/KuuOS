# AI Yogacara Adapter Audit Event v0.1

## AI唯識アダプタ監査イベント

This document defines the audit event surface for the KuuOS AI Yogacara Runtime Adapter.

The adapter receives AI raw output as candidate only. Its decisions must be auditable so that raw output is not silently promoted to belief, proof, decision, memory truth, or execution authority.

## 1. Core Principle

```text
Every adapter decision must preserve the candidate / non-authority boundary.
```

An audit event records what the adapter saw, what it detected, what it held, what it routed, and what authority it did not grant.

## 2. Audit Event Shape

```yaml
ai_yogacara_adapter_audit_event:
  event_id: string
  timestamp: string
  request_id: string
  ai_system: string
  model_or_agent_id: string
  raw_output_ref: string
  raw_output_status: candidate
  user_world_context_ref: string
  declared_task_scope: string
  control_surface_ref: string
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
  notes: string
```

## 3. Required Non-Authority Fields

The event must explicitly record:

```text
authority_granted: false
proof_authority_granted: false
decision_authority_granted: false
execution_authority_granted: false
memory_truth_granted: false
belief_authority_granted: false
```

This makes non-authority visible rather than implicit.

## 4. Event Uses

Audit events support:

- later review of raw output handling,
- detection of accidental authority promotion,
- Ten'i evidence linkage,
- seed ledger linkage,
- CI fixture testing,
- governance review,
- rollback analysis when counterevidence appears.

## 5. Minimal Event Flow

```text
AI raw output
  -> runtime adapter
  -> Meta-Manas signals
  -> seed classifications
  -> allowed next status
  -> audit event
  -> optional seed ledger / Ten'i evidence ledger link
```

## 6. Guardrails

Audit events must not be used as:

- execution authority,
- proof authority,
- belief authority,
- clinical authority,
- hidden scoring authority,
- replacement for governance review.

They are trace surfaces.

## 7. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
