# Mandala Multi-WORLD Runtime Contract v0.1

## 曼荼羅 Multi-WORLD ランタイム契約

This document defines the runtime contract for operating multiple WORLD models inside KuuOS without collapsing them into a single master WORLD.

The Mandala layer arranges multiple WORLD models around the fourfold core:

```text
空 / emptiness
縁起 / dependent origination
二諦 gap / two truths gap
中道 / middle way
```

No individual WORLD model may replace this center.

## 1. Core Principle

```text
Many WORLDs may coexist.
No WORLD becomes the center.
```

A WORLD model is a governed local interpretation surface, not ultimate authority.

## 2. Runtime Chain

```text
fourfold core
  -> WORLD model registry
  -> membrane boundary
  -> cross-WORLD transport gate
  -> obstruction visibility
  -> harmony function
  -> residual suffering visibility
  -> Bodhisattva Path belief
```

## 3. WORLD Runtime Object

```yaml
world_runtime_object:
  world_id: string
  world_name: string
  scope: string
  status: DRAFT | ACTIVE | HOLD | QUARANTINE | RETIRED
  membrane_ref: string
  qi_flow_ref: string
  yinyang_frame_ref: string
  wuxing_phase_ref: string
  governance_boundary_ref: string
  obstruction_refs: list
  authority_note: local_world_not_fourfold_core
```

## 4. Cross-WORLD Transport Object

```yaml
cross_world_transport_object:
  transport_id: string
  source_world_id: string
  target_world_id: string
  transport_mode: preserve | transform | reinterpret | quarantine | reject
  membrane_check: PASS | HOLD | FAIL
  gate_check: PASS | HOLD | FAIL
  obstruction_visibility: visible | missing
  harmony_effect: improves | neutral | worsens | unknown
  authority_note: transport_is_not_world_collapse
```

## 5. Harmony Function Runtime

The Harmony Function / 和の関数 coordinates multiple WORLD models without forced sameness.

```yaml
harmony_function_runtime:
  input_worlds: list
  conflicts: list
  obstructions: list
  residual_suffering: list
  output_status: PASS | HOLD | REPAIR | QUARANTINE | REJECT | HANDOVER
  noncollapse_preserved: boolean
  residual_suffering_visible: boolean
  authority_note: harmony_is_coordination_not_domination
```

## 6. Required Invariants

```text
no_world_model_replaces_fourfold_core
world_boundary_must_remain_visible
cross_world_transport_must_be_declared
obstruction_must_not_be_erased
harmony_function_must_not_force_sameness
residual_suffering_visibility_must_be_preserved
bodhisattva_path_belief_must_not_be_erased
```

## 7. Runtime Decisions

```text
transport valid and no obstruction hidden
  -> PASS or REVIEW

transport unclear or membrane missing
  -> HOLD

obstruction hidden
  -> REPAIR or QUARANTINE

one WORLD attempts to dominate center
  -> REJECT

residual suffering remains after harmony
  -> Bodhisattva Path belief route
```

## 8. Guardrails

The Mandala Multi-WORLD runtime must not be used as:

- single master WORLD authority,
- forced consensus,
- majority domination,
- erasure of minority WORLDs,
- erasure of obstruction,
- execution authority,
- proof authority,
- clinical authority.

It is a coordination and governance surface.

## 9. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
