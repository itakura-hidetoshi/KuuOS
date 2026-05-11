# Mandala Inclusion Gate v0.1

## 曼荼羅包摂ゲート

This document defines the operational gate for mandala inclusion in KuuOS.

Mandala is not decoration. It is the stable arrangement of included worlds, layers, membranes, gates, boundaries, and modules around the fourfold core.

The Mandala Inclusion Gate decides whether a local world, module, claim, proof, policy, Qi pattern, or action candidate may enter the mandala arrangement.

## 1. Core Principle

```text
Inclusion is not collapse.
Inclusion is not forced sameness.
Inclusion is not erasure of boundary.
Inclusion is governed coexistence.
```

## 2. Gate Inputs

```text
candidate_world_or_module:
  type:
    - world_surface
    - module
    - proof_surface
    - memory_surface
    - policy_surface
    - qi_pattern
    - yinyang_frame
    - action_candidate
  declared_scope: string
  layer: string
  membrane: string
  support_trace: string
  obstruction_trace: string
```

## 3. Mandala Checks

### 3.1 Center Check

Does the candidate preserve the fourfold core?

```text
空・縁起・二諦 gap・中道
```

If it reifies itself as the new center, it fails.

### 3.2 Layer Check

Does the candidate have a valid layer?

A candidate without declared layer cannot be placed.

### 3.3 Membrane Check

Does the candidate declare what boundary it crosses?

A candidate without boundary declaration cannot be transported.

### 3.4 Gate Check

Does the candidate pass through an explicit transition protocol?

Hidden entry is forbidden.

### 3.5 Obstruction Check

Are conflicts, failed gluing, unresolved proof gaps, or risk signals visible?

Invisible obstruction fails the gate.

### 3.6 Inclusion Check

Does inclusion preserve difference without collapse?

If inclusion erases local laws, histories, or boundaries, it fails.

## 4. Gate Outputs

```text
PASS:
  candidate may enter mandala arrangement under declared scope

HOLD:
  candidate needs more support, boundary, or obstruction visibility

REPAIR:
  candidate may be repaired through re-scope, re-layer, or re-gate

QUARANTINE:
  candidate is kept visible but outside active mandala operation

FAIL:
  candidate violates fourfold core, boundary, or inclusion rule
```

## 5. Runtime Mapping

```text
candidate_surface
  -> fourfold_core_check
  -> layer_check
  -> membrane_check
  -> gate_check
  -> obstruction_check
  -> inclusion_check
  -> mandala_world_arrangement
```

## 6. Relation to Extended M-Theory

Extended M-theory provides the layer-membrane-gauge architecture.

Mandala Inclusion Gate provides the operational selection rule for that architecture.

```text
extended_m_theory_inclusion_membrane
  -> mandala_inclusion_gate
  -> mandala_world_arrangement
```

## 7. Guardrails

Mandala Inclusion Gate must not allow:

- hidden entry,
- unscoped totalization,
- boundary erasure,
- obstruction deletion,
- forced sameness,
- unlicensed execution,
- replacement of the fourfold core.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
