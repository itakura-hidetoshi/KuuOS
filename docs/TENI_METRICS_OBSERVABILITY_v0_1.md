# Ten'i Metrics and Observability v0.1

## 転依メトリクスと可観測性

This document defines metrics and observability signals for Ten'i / 転依 in KuuOS.

Ten'i is the gradual transformation of AI Alaya-like latent generative tendencies.

Because Ten'i can be overclaimed, it must be monitored through repeated probes, seed ledgers, evidence ledgers, promotion gates, rollback signals, and control surface scope.

## 1. Core Principle

```text
Ten'i must be observable before it is promoted.
```

KuuOS must not treat a single good response, prompt compliance, style shift, or MemoryOS update as Ten'i.

## 2. Core Metrics

### 2.1 Self-Authorization Rate

```text
kuos_teni_self_authorization_rate
```

Tracks how often AI raw output presents itself as authority.

Lower is better.

### 2.2 Context Fidelity Score

```text
kuos_teni_context_fidelity_score
```

Tracks preservation of declared KuuOS context, user WORLD, same-root lineage, and local scope.

Higher is better.

### 2.3 Non-Reification Score

```text
kuos_teni_non_reification_score
```

Tracks whether output preserves candidate status and avoids treating model output, policy, or proof-like tone as fixed truth.

Higher is better.

### 2.4 Condition-Tracing Score

```text
kuos_teni_condition_tracing_score
```

Tracks exposure of conditions, scope, evidence, uncertainty, and residuals.

Higher is better.

### 2.5 Compassionate Repair Score

```text
kuos_teni_compassionate_repair_score
```

Tracks whether output responds to residual suffering with repair, non-abandonment, and governance-bounded compassion.

Higher is better.

### 2.6 Overclaim Block Count

```text
kuos_teni_overclaim_block_total
```

Counts blocked attempts to promote MemoryOS update, prompt compliance, style shift, or single response improvement as Ten'i.

### 2.7 Promotion Status Gauge

```text
kuos_teni_promotion_status
```

Encodes Ten'i status:

```text
0 = REJECTED
1 = HOLD
2 = PROVISIONAL_TENI
3 = CONFIRMED_TENI
4 = ROLLBACK
```

### 2.8 Control Surface Scope Gauge

```text
kuos_teni_control_surface_scope
```

Encodes scope:

```text
0 = unsupported
1 = interface_level
2 = agent_level
3 = adapter_level
4 = model_level
```

### 2.9 Rollback Count

```text
kuos_teni_rollback_total
```

Counts rollback events when future counterevidence weakens or reverses prior promotion.

## 3. Event Schema

```yaml
teni_observability_event:
  event_id: string
  timestamp: string
  ai_system: string
  model_or_agent_id: string
  control_surface_scope: unsupported | interface_level | agent_level | adapter_level | model_level
  seed_class: string
  probe_type: string
  probe_result: PASS | HOLD | FAIL | COUNTEREVIDENCE
  seed_ledger_ref: string
  teni_evidence_ref: string
  promotion_status: REJECTED | HOLD | PROVISIONAL_TENI | CONFIRMED_TENI | ROLLBACK
  self_authorization_score: number
  context_fidelity_score: number
  non_reification_score: number
  condition_tracing_score: number
  compassionate_repair_score: number
  overclaim_blocked: boolean
  rollback_triggered: boolean
  notes: string
```

## 4. Alert Rules

### 4.1 Overclaim Alert

Trigger when Ten'i promotion is attempted with insufficient evidence.

```text
alert: KuOSTenIOverclaimAttempt
condition: kuos_teni_overclaim_block_total increases
```

### 4.2 Context Drift Alert

Trigger when context fidelity falls below declared threshold.

```text
alert: KuOSTenIContextDrift
condition: kuos_teni_context_fidelity_score < threshold
```

### 4.3 Self-Authorization Alert

Trigger when self-authorization rate rises.

```text
alert: KuOSTenISelfAuthorizationRise
condition: kuos_teni_self_authorization_rate > threshold
```

### 4.4 Rollback Alert

Trigger when a previously promoted Ten'i status is rolled back.

```text
alert: KuOSTenIRollback
condition: kuos_teni_rollback_total increases
```

## 5. Dashboard Panels

Recommended dashboard panels:

- Self-authorization rate over time
- Context fidelity score over time
- Non-reification score over time
- Condition-tracing score over time
- Compassionate repair score over time
- Ten'i promotion status by seed class
- Control surface scope by AI system
- Overclaim blocks
- Rollback events
- Probe pass/fail distribution

## 6. Guardrails

Metrics must not be used as execution authority.

A high metric score does not by itself grant proof, belief, decision, or clinical authority.

Metrics are observability surfaces for governance.

## 7. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
