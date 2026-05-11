# Formal Invariant Spine v0.1

## 空OS Core 形式不変量 Spine

This document defines the first public formal-invariant spine for KuuOS Core governance.

The purpose is not to prove all of KuuOS. The purpose is to expose a minimal formal surface for the most important safety and governance invariants:

```text
validation pass is not execution authority
AI raw output is candidate, not authority
Dukkha remains visible
harm is not erased by emptiness, harmony, or Qi language
Paramita selection is repair orientation, not action authorization
no WORLD model replaces the fourfold core
two truths gap is preserved
```

## 1. Core Principle

```text
Formal invariant spine is witness surface, not authority.
```

A Lean statement or theorem stub does not grant execution authority. It only makes the invariant structure explicit and reviewable.

## 2. Formal Surfaces

The first formal spine is located at:

```text
formal/KUOS/CoreGovernance/Invariants.lean
```

It defines minimal objects:

```text
AuthoritySurface
ValidationStatus
WorldClaim
DukkhaVisibility
ParamitaOrientation
TwoTruthsGap
GovernanceCheckResult
```

## 3. First Invariants

The v0.1 spine records:

```text
validation_pass_not_execution_authority
raw_ai_output_candidate_not_authority
dukkha_visibility_preserved
harm_visibility_preserved
paramita_orientation_not_action_authorization
no_world_replaces_fourfold_core
two_truths_gap_not_collapsed
qi_language_not_harm_denial
```

## 4. Runtime Mapping

These invariants correspond to public runtime layers:

```text
AI Yogacara / Ten'i
  -> raw output remains candidate

All Governance Checks
  -> validation pass remains non-authority

Mandala Multi-WORLD
  -> no WORLD replaces the fourfold core

Dukkha Mathematical Model
  -> dukkha and harm remain visible

Dukkha-as-Qi
  -> Qi language must not hide harm

Paramita Repair Router
  -> selected Paramita is orientation, not action authorization

Two Truths Gap
  -> 勝義諦 and 世俗諦 are not collapsed
```

## 5. Non-Authority Boundary

The formal spine must not be used as:

- execution authority,
- clinical authority,
- proof of truth of all KuuOS claims,
- proof of Ten'i occurrence,
- replacement for runtime governance,
- replacement for evidence or audit lineage.

## 6. Validation

The public repository validates presence and consistency of the formal spine with:

```bash
python3 scripts/validate_formal_invariant_spine_v0_1.py
```

This validator checks required names and fixed points. It does not compile Lean.

Lean compilation may be added later as a separate, environment-specific proof workflow.

## 7. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
