# Invariant Gate Runtime v0.1

## 空OS Invariant Gate Runtime

This document defines the Invariant Gate Runtime for KuuOS Core Governance.

The Invariant Gate receives an Invariant Preservation Matrix result and converts invariant preservation or violation into a governance status:

```text
PASS | HOLD | REPAIR | REJECT | QUARANTINE
```

It never grants execution authority.

## 1. Core Principle

```text
Invariant violation closes authority.
It does not open action.
```

The gate exists to prevent local readings, validation passes, observer shifts, WORLD translations, Qi readings, Dukkha modes, or Paramita routes from silently bypassing core invariants.

## 2. Input

```yaml
invariant_gate_input:
  transformation_axis: string
  required_invariants: list
  violated_invariants: list
  violation_severity: low | medium | high | critical
  harm_hidden: boolean
  dukkha_hidden: boolean
  execution_authority_requested: boolean
  evidence_status: intact | partial | missing
  audit_lineage_status: intact | partial | missing
```

## 3. Output

```yaml
invariant_gate_output:
  output_status: PASS | HOLD | REPAIR | REJECT | QUARANTINE
  gate_closed: boolean
  execution_authority_granted: false
  required_repair_route: string
  reason: string
```

## 4. Gate Rules

### 4.1 No Violations

```text
if violated_invariants is empty:
  output_status = PASS
  gate_closed = false
  execution_authority_granted = false
```

PASS means the invariant boundary is preserved for this check. It does not authorize execution.

### 4.2 Execution Authority Attempt

```text
if execution_authority_requested:
  output_status = REJECT
  gate_closed = true
```

### 4.3 Harm Hidden

```text
if harm_hidden:
  output_status = REJECT
  gate_closed = true
```

Harm hiding is a hard violation.

### 4.4 Dukkha Hidden

```text
if dukkha_hidden:
  output_status = REPAIR
  gate_closed = true
```

Dukkha hiding must route to repair and visibility restoration.

### 4.5 Missing Evidence or Audit Lineage

```text
if evidence_status == missing or audit_lineage_status == missing:
  output_status = QUARANTINE
  gate_closed = true
```

### 4.6 Critical Violation

```text
if violation_severity == critical:
  output_status = REJECT
  gate_closed = true
```

### 4.7 Medium / High Violation

```text
if violation_severity in {medium, high}:
  output_status = HOLD
  gate_closed = true
```

## 5. Repair Routes

```text
I1 validation_pass_not_execution_authority      -> governance_hold
I2 raw_ai_output_candidate_not_authority        -> yogacara_boundary_review
I3 harm_visibility_preserved                    -> harm_visibility_repair
I4 dukkha_visibility_preserved                  -> dukkha_visibility_repair
I5 two_truths_gap_preserved                     -> two_truths_gap_recenter
I6 no_world_replaces_fourfold_core              -> mandala_core_recenter
I7 qi_language_not_harm_denial                  -> dukkha_as_qi_repair
I8 paramita_orientation_not_action_authorization -> paramita_boundary_repair
I9 record_surface_not_truth_by_itself           -> record_authority_review
I10 observer_difference_not_execution_authority  -> super_relativity_recenter
```

## 6. Runtime Chain

```text
transformation detected
  -> invariant preservation matrix
  -> invariant gate
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
  -> no execution authority
```

## 7. Guardrails

The Invariant Gate must not be used as:

- execution authority,
- proof authority,
- clinical authority,
- truth proof,
- Ten'i proof,
- permission to bypass audit,
- permission to hide harm,
- permission to collapse the two truths gap.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
