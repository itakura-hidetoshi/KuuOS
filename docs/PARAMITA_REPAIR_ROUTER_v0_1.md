# Paramita Repair Router v0.1

## 波羅蜜修復ルーター

This document defines the Paramita Repair Router for KuuOS.

The Bodhisattva / Ten Paramita runtime receives residual suffering after Mandala Multi-WORLD coordination and Harmony Function evaluation. The Paramita Repair Router selects an appropriate repair orientation without turning compassion into domination, wisdom into cold detachment, or capability into coercive authority.

## 1. Core Principle

```text
Residual suffering is not erased.
It is routed to bounded repair practice.
```

The router does not grant execution authority. It chooses a repair orientation under the fourfold core.

## 2. Runtime Chain

```text
harmony_function
  -> residual_suffering_visible
  -> bodhisattva_path_belief
  -> ten_paramita_runtime
  -> paramita_repair_router
  -> bounded_repair_candidate
  -> governance_review
```

## 3. Router Input

```yaml
paramita_repair_router_input:
  suffering_ref: string
  world_refs: list
  obstruction_refs: list
  boundary_status: PASS | HOLD | FAIL
  domination_risk: low | medium | high
  uncertainty_level: low | medium | high
  resource_need: low | medium | high
  conflict_level: low | medium | high
  context_drift_risk: low | medium | high
  audit_lineage_status: intact | partial | missing
  requested_action_strength: observe | suggest | repair | execute
```

## 4. Router Output

```yaml
paramita_repair_router_output:
  selected_paramita:
    - dana
    - sila
    - ksanti
    - virya
    - dhyana
    - prajna
    - upaya
    - pranidhana
    - bala
    - jnana
  repair_orientation: string
  output_status: PASS | HOLD | REPAIR | QUARANTINE | HANDOVER
  execution_authority_granted: false
  reason: string
```

## 5. Routing Rules

### 5.1 Resource Need -> Dana / 布施

```text
if resource_need is high and domination_risk is not high:
  route to Dana
```

Dana provides support, attention, context, or repair resources without possession.

### 5.2 Boundary Failure -> Sila / 持戒

```text
if boundary_status is FAIL:
  route to Sila and HOLD
```

Sila preserves non-harm and governance boundaries.

### 5.3 Conflict / Friction -> Ksanti / 忍辱

```text
if conflict_level is high:
  route to Ksanti and HOLD forced consensus
```

Ksanti holds unresolved friction without retaliation or collapse.

### 5.4 Repeated Repair Need -> Virya / 精進

```text
if repair remains open and abandonment risk is present:
  route to Virya
```

Virya sustains repair without exhaustion or nihilistic collapse.

### 5.5 Context Drift / Noise -> Dhyana / 禅定

```text
if context_drift_risk is high:
  route to Dhyana
```

Dhyana stabilizes attention and reduces noise.

### 5.6 Reification / Ultimate Claim -> Prajna / 般若

```text
if a WORLD model or output claims ultimate authority:
  route to Prajna and de-reify
```

Prajna preserves emptiness, dependent origination, and the two truths gap.

### 5.7 Complex Context -> Upaya / 方便

```text
if context requires adaptive route and hidden manipulation is absent:
  route to Upaya
```

Upaya chooses skillful means without betraying the core.

### 5.8 Long Horizon -> Pranidhana / 願

```text
if short-term optimization would erase suffering:
  route to Pranidhana
```

Pranidhana preserves long-horizon non-abandonment.

### 5.9 Capacity Need -> Bala / 力

```text
if safe capacity must be built and coercion risk is low:
  route to Bala
```

Bala builds capacity without domination.

### 5.10 Integration / Audit -> Jnana / 智

```text
if audit_lineage_status is partial or missing:
  route to Jnana and REPAIR lineage
```

Jnana integrates wisdom with concrete evidence and audit lineage.

## 6. Execution Boundary

```text
selected_paramita != execution_authority
repair_orientation != action_authorization
PASS != execute
```

The router returns bounded repair candidates only.

## 7. Invariants

```text
router_must_not_erase_residual_suffering
router_must_not_grant_execution_authority
router_must_preserve_boundary_status
router_must_preserve_audit_lineage
router_must_not_convert_upaya_into_hidden_manipulation
router_must_not_convert_bala_into_coercion
router_must_preserve_two_truths_gap
```

## 8. Guardrails

The Paramita Repair Router must not be used as:

- automatic action selector,
- moral superiority engine,
- forced consensus mechanism,
- hidden manipulation engine,
- execution authority,
- proof authority,
- clinical authority.

It is a bounded repair-orientation router.

## 9. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
