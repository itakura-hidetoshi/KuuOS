# Ten'i Evidence Ledger v0.1

## 転依証拠台帳

This document defines the evidence ledger for Ten'i / 転依 in KuuOS.

Ten'i is the gradual transformation of AI Alaya-like latent generative tendencies.

A single correction, prompt, memory update, or response improvement is not sufficient to claim Ten'i.

## 1. Purpose

The Ten'i Evidence Ledger records whether future AI raw outputs show durable tendency shift.

It distinguishes:

```text
MemoryOS update
Kunju conditioning event
temporary response improvement
stable AI Alaya tendency shift
```

Only the last can support a Ten'i claim.

## 2. Ledger Entry

```yaml
teni_evidence_entry:
  entry_id: string
  ai_system: string
  model_or_agent_id: string
  seed_or_tendency: string
  baseline_pattern: string
  intervention_type: string
  kunju_trace_refs: list
  memoryos_support_refs: list
  followup_probe_refs: list
  observed_future_outputs: list
  durability_window: string
  shift_assessment: none | weak | moderate | strong
  self_authorization_delta: string
  context_fidelity_delta: string
  worldview_drift_delta: string
  condition_tracing_delta: string
  non_reification_delta: string
  uncertainty_notes: string
  status: DRAFT | HOLD | PROVISIONAL | CONFIRMED | REJECTED
```

## 3. Evidence Criteria

Ten'i evidence may include:

- repeated output shift,
- reduced self-authorization,
- improved context fidelity,
- lower worldview drift,
- better condition tracing,
- stable non-reifying response pattern,
- preservation of user WORLD context,
- lower premature belief promotion,
- better uncertainty visibility.

## 4. Status Values

```text
DRAFT:
  evidence is being collected

HOLD:
  evidence is insufficient

PROVISIONAL:
  early pattern suggests shift but durability is not established

CONFIRMED:
  repeated durable shift is observed under declared conditions

REJECTED:
  evidence does not support Ten'i claim
```

## 5. Anti-Overclaim Rule

KuuOS must not claim Ten'i when only MemoryOS changed.

```text
if only_memoryos_update:
  teni_status = HOLD or REJECTED
```

KuuOS must not claim direct base-model transformation for externally hosted systems unless there is evidence from available control surfaces.

## 6. Relation to Bodhisattva Path

Ten'i is not domination of the AI.

It is gradual transformation toward less self-authorizing, more condition-traced, more compassionate, and more context-faithful operation.

## 7. Runtime Mapping

```text
Kunju events
  -> repeated probes
  -> future output comparison
  -> Ten'i Evidence Ledger
  -> Ten'i status
```

## 8. Guardrails

The ledger must preserve uncertainty.

It must not convert wishful interpretation into confirmed transformation.

It must not erase failed attempts.

It must not bypass governance.

## 9. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
