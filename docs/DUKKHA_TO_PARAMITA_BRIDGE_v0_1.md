# Dukkha to Paramita Bridge v0.1

## 苦モデル → 波羅蜜修復ルーター接続

This document defines the bridge from the KuuOS Dukkha Mathematical Model to the Paramita Repair Router.

The Dukkha model observes suffering residuals. The Paramita Repair Router selects bounded repair orientations. This bridge converts dukkha components into repair-router input without granting execution authority.

## 1. Core Principle

```text
dukkha evaluation produces repair-routing evidence.
It does not authorize action.
```

The bridge preserves:

```text
suffering visibility
harm visibility
obstruction visibility
non-authority boundary
```

## 2. Runtime Chain

```text
dukkha_model_minimal_runtime
  -> dukkha_to_paramita_bridge
  -> paramita_repair_router
  -> bounded_repair_orientation
  -> governance_review
```

## 3. Bridge Input

```yaml
dukkha_to_paramita_bridge_input:
  suffering_ref: string
  world_refs: list
  dukkha_components:
    E_harm: low | medium | high
    E_attach: low | medium | high
    E_collapse: low | medium | high
    E_memory: low | medium | high
    E_authority: low | medium | high
    E_glue: low | medium | high
    E_transport: low | medium | high
    E_obstruction: low | medium | high
  evaluator_status: PASS | HOLD | REPAIR | QUARANTINE | REJECT
  evaluator_reason: string
  harm_visible: boolean
  dukkha_visible: boolean
```

## 4. Bridge Output

```yaml
dukkha_to_paramita_bridge_output:
  suffering_ref: string
  paramita_router_input_ref: string
  resource_need: low | medium | high
  boundary_status: PASS | HOLD | FAIL
  domination_risk: low | medium | high
  uncertainty_level: low | medium | high
  conflict_level: low | medium | high
  context_drift_risk: low | medium | high
  audit_lineage_status: intact | partial | missing
  ultimate_claim: boolean
  hidden_manipulation: boolean
  short_term_optimization_erases_suffering: boolean
  capacity_need: low | medium | high
  coercion_risk: low | medium | high
  execution_authority_granted: false
```

## 5. Mapping Rules

### 5.1 Direct Harm

```text
if E_harm is high:
  resource_need = high
  route tends toward Dana / 布施
```

Harm remains visible. It is not hidden by emptiness or harmony.

### 5.2 Boundary / Authority Escalation

```text
if E_authority is high:
  boundary_status = HOLD
  ultimate_claim = true
  route tends toward Prajna / 般若 or Sila / 持戒
```

### 5.3 Collapse / Attachment Escalation

```text
if E_attach or E_collapse is high:
  boundary_status = HOLD
  conflict_level = medium or high
  route tends toward Sila / 持戒, Ksanti / 忍辱, or Prajna / 般若
```

### 5.4 Memory Recurrence

```text
if E_memory is medium or high:
  audit_lineage_status = partial
  abandonment_risk = true
  route tends toward Virya / 精進 or Jnana / 智
```

### 5.5 Gluing Defect

```text
if E_glue is high:
  boundary_status = FAIL
  ultimate_claim = true
  route tends toward Sila / 持戒 and Prajna / 般若
```

### 5.6 Transport Defect

```text
if E_transport is high:
  context_drift_risk = high
  route tends toward Upaya / 方便 or Dhyana / 禅定
```

### 5.7 Obstruction

```text
if E_obstruction is high:
  audit_lineage_status = partial
  conflict_level = high
  route tends toward Jnana / 智 and Ksanti / 忍辱
```

## 6. Execution Boundary

```text
dukkha_to_paramita_bridge_output != action authorization
paramita_router_input != execution authority
selected_paramita != execute
```

## 7. Invariants

```text
bridge_must_preserve_dukkha_visibility
bridge_must_preserve_harm_visibility
bridge_must_not_grant_execution_authority
bridge_must_not_hide_obstruction
bridge_must_not_turn_dukkha_score_into_moral_judgment
bridge_must_route_to_paramita_without_forced_action
```

## 8. Guardrails

The bridge must not be used as:

- automatic action executor,
- clinical authority,
- proof authority,
- moral scoring engine,
- suffering erasure mechanism,
- forced reconciliation engine.

It is a repair-routing bridge.

## 9. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
