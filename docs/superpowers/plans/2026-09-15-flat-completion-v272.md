# Flat Completion / Limit Descent v2.72 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn an explicitly supplied infinite correction history with linearly improving filtration order into a flat residual at an explicitly supplied limit state, and derive exact triviality only under separatedness.

**Architecture:** v2.72 imports green v2.71 but does not derive an infinite tower from finite correction existence. `FilteredCorrectionTower` stores the entire history, invariant, step relation, and order certificate. `ResidualLimitData` stores the actual limit state, its invariant, and the exact level-transfer principle. Arithmetic plus `0 < δ` gives eventual membership in every fixed filtration level; the limit-transfer datum gives flatness; separatedness alone upgrades flatness to equality.

**Tech Stack:** Lean `leanprover/lean4:v4.30.0-rc2`; Mathlib rev `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; Lake; exact-head GitHub CI.

**Spec:** `docs/superpowers/specs/2026-09-15-filtered-residual-hyperdescent-design.md`

## Global Constraints

- Stack on v2.71 exact green head `55928d964c9c0f32dc0b8ceb62b97858b3d17db8`.
- Never infer an infinite tower from `HasCorrectionGain` or `exists_finiteCorrectionChain_of_gain`.
- No topology, metric, completeness, Cauchy, summability, Borel realization, or PDE assumptions.
- `ResidualLimitData.invariant_limit` is direct evidence; do not pretend arbitrary invariants pass to unspecified limits.
- `level_limit` is the only generic authority boundary from eventual finite-level control to the actual limit state.
- No equality conclusion without `SeparatedAt`.
- No v2.73 generated-holonomy imports.
- No `sorry`, `admit`, new `axiom`, or umbrella/version promotion.

---

### Task 1: Explicit filtered correction tower and eventual-order theorem

**Files:**
- Create: `formal/KUOS/DependentOriginationFlatCompletionV2_72.lean`

Implement:

```lean
import KUOS.DependentOriginationCorrectionGainV2_71

namespace KUOS.DependentOriginationFlatCompletionV2_72

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionGainV2_71

universe u v

structure FilteredCorrectionTower
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (δ n₀ : ℕ) where
  state : ℕ → State
  invariant : ∀ n, P.invariant (state n)
  step : ∀ n, Step (state n) (state (n + 1))
  order : ∀ n,
    F.OrderAtLeast (n₀ + n * δ) (P.residual (state n))
```

Then prove in `namespace FilteredCorrectionTower`:

```lean
theorem eventually_orderAtLeast
    ...
    (T : FilteredCorrectionTower F P Step δ n₀)
    (hδ : 0 < δ) (k : ℕ) :
    ∃ N, ∀ n ≥ N,
      F.OrderAtLeast k (P.residual (T.state n)) := by
  refine ⟨k, ?_⟩
  intro n hn
  have hmul : n ≤ n * δ := by
    simpa using Nat.mul_le_mul_left n hδ
  have hk : k ≤ n₀ + n * δ := by
    omega
  exact F.orderAtLeast_mono hk (T.order n)
```

If the local Mathlib signature requires a `1 ≤ δ` hypothesis rather than `0 < δ`, derive it explicitly with `have hδ1 : 1 ≤ δ := hδ` and use that in `Nat.mul_le_mul_left`.

Validation target:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationFlatCompletionV2_72
```

---

### Task 2: Limit-transfer datum and flatness theorem

Add:

```lean
structure ResidualLimitData
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop} {δ n₀ : ℕ}
    (T : FilteredCorrectionTower F P Step δ n₀) where
  limitState : State
  invariant_limit : P.invariant limitState
  level_limit :
    ∀ k,
      (∃ N, ∀ n ≥ N,
        F.OrderAtLeast k (P.residual (T.state n))) →
      F.OrderAtLeast k (P.residual limitState)
```

Prove:

```lean
theorem limit_invariant_and_flat
    ...
    (T : FilteredCorrectionTower F P Step δ n₀)
    (L : ResidualLimitData F P T)
    (hδ : 0 < δ) :
    P.invariant L.limitState ∧
      F.Flat (P.residual L.limitState) := by
  refine ⟨L.invariant_limit, ?_⟩
  intro k
  exact L.level_limit k (T.eventually_orderAtLeast hδ k)
```

Do not add any claim that such an `L` exists generically.

---

### Task 3: Separated completion corollary

Prove:

```lean
theorem limit_residual_eq_of_separatedAt
    ...
    (T : FilteredCorrectionTower F P Step δ n₀)
    (L : ResidualLimitData F P T)
    (hδ : 0 < δ)
    {e : D}
    (hsep : F.SeparatedAt e) :
    P.residual L.limitState = e := by
  exact F.flat_eq_of_separatedAt hsep
    (limit_invariant_and_flat F P T L hδ).2
```

This theorem is the sole generic v2.72 route from asymptotic order improvement to exact residual equality.

---

### Task 4: Exact-head governance validation

- Branch: `formal/dependent-origination-flat-completion-v272`.
- Base: `formal/dependent-origination-correction-gain-v271`.
- Draft PR title: `Formalize flat completion and limit descent v2.72`.
- Changed files exactly: `formal/KUOS/DependentOriginationFlatCompletionV2_72.lean`.
- Require strict Lean formal validation and governance summary success on exact head.
- Keep Draft; do not merge or mark ready.

## Self-Review Result

- Finite existence does not imply infinite history.
- Infinite history does not imply an actual limit state.
- Actual limit state does not inherit residual levels except through explicit `level_limit`.
- Flatness does not imply equality except through explicit separatedness.
- The exact invariant is direct evidence on the limit state, not an unstated closedness theorem.
