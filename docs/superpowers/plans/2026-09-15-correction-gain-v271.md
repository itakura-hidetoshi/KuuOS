# Exact-Invariant Correction Gain v2.71 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Formalize one-step residual-order gain and prove existence of explicit finite correction histories of arbitrary prescribed finite length while preserving an exact invariant.

**Architecture:** v2.71 imports only the green v2.70 filtration core. A residual problem separates an exact invariant from a defect value; correction is represented by a relation rather than a function. A finite correction history is an inductive chain retaining every selected intermediate state, and a theorem recursively constructs a length-`k` chain whose terminal defect order is at least `n₀ + k * δ`.

**Tech Stack:** Lean `leanprover/lean4:v4.30.0-rc2`; Mathlib rev `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; Lake; exact-head GitHub CI.

**Spec:** `docs/superpowers/specs/2026-09-15-filtered-residual-hyperdescent-design.md`

## Global Constraints

- Stack implementation on v2.70 exact green head `c2dd83efa6e3e4bdb6878796177fea4c526bc0f8`.
- Keep v2.70 and all v2.68/v2.69 files unchanged.
- No infinite correction tower, convergence, limit, flatness conclusion, or generated-holonomy bridge in v2.71.
- `Step` remains relational; do not replace it by a canonical correction function.
- The finite chain must retain the actual sequence of selected correction states in its inductive proof data.
- `HasCorrectionGain` requires `0 < δ` and the existential next-state gain property.
- No `sorry`, `admit`, new `axiom`, or umbrella/version promotion.

---

### Task 1: Define residual problem, correction gain, and finite chain

**Files:**
- Create: `formal/KUOS/DependentOriginationCorrectionGainV2_71.lean`

**Interfaces:**
- Consumes: `ObstructionFiltration`, `OrderAtLeast` from v2.70.
- Produces:
  - `ResidualProblem`
  - `HasCorrectionGain`
  - `correctionGain_pos`
  - `FiniteCorrectionChain`

Implement:

```lean
import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationCorrectionGainV2_71

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration

universe u v

structure ResidualProblem (State : Type u) (D : Type v) where
  invariant : State → Prop
  residual : State → D

def HasCorrectionGain
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (δ : ℕ) : Prop :=
  0 < δ ∧
    ∀ x n,
      P.invariant x →
      F.OrderAtLeast n (P.residual x) →
      ∃ y,
        Step x y ∧
        P.invariant y ∧
        F.OrderAtLeast (n + δ) (P.residual y)

theorem correctionGain_pos
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop) {δ : ℕ}
    (h : HasCorrectionGain F P Step δ) : 0 < δ :=
  h.1

inductive FiniteCorrectionChain
    {State : Type u} (Step : State → State → Prop) :
    ℕ → State → State → Prop
  | nil (x : State) : FiniteCorrectionChain Step 0 x x
  | snoc {k : ℕ} {x y z : State}
      (hxy : FiniteCorrectionChain Step k x y)
      (hyz : Step y z) :
      FiniteCorrectionChain Step (k + 1) x z
```

Verification:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCorrectionGainV2_71
```

Expected: PASS.

---

### Task 2: Prove arbitrary finite correction gain

**Files:**
- Modify: `formal/KUOS/DependentOriginationCorrectionGainV2_71.lean`

**Interfaces:**
- Consumes: `HasCorrectionGain`, `FiniteCorrectionChain`.
- Produces: `exists_finiteCorrectionChain_of_gain`.

Add:

```lean
/-- A one-step existential gain can be iterated for every prescribed finite
length without selecting or postulating an infinite correction history. -/
theorem exists_finiteCorrectionChain_of_gain
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    {δ n₀ : ℕ}
    (hgain : HasCorrectionGain F P Step δ)
    {x : State}
    (hxinv : P.invariant x)
    (hxord : F.OrderAtLeast n₀ (P.residual x))
    (k : ℕ) :
    ∃ y,
      FiniteCorrectionChain Step k x y ∧
      P.invariant y ∧
      F.OrderAtLeast (n₀ + k * δ) (P.residual y) := by
  induction k generalizing x n₀ with
  | zero =>
      refine ⟨x, FiniteCorrectionChain.nil x, hxinv, ?_⟩
      simpa using hxord
  | succ k ih =>
      obtain ⟨y, hchain, hyinv, hyord⟩ := ih hxinv hxord
      obtain ⟨z, hyz, hzinv, hzord⟩ :=
        hgain.2 y (n₀ + k * δ) hyinv hyord
      refine ⟨z, FiniteCorrectionChain.snoc hchain hyz, hzinv, ?_⟩
      simpa [Nat.succ_mul, Nat.add_assoc] using hzord
```

If Lean cannot infer generalized `x`/`n₀` in the `ih` call, use the explicit form:

```lean
obtain ⟨y, hchain, hyinv, hyord⟩ :=
  ih (x := x) (n₀ := n₀) hxinv hxord
```

This is an elaboration adjustment only; do not change the theorem statement.

Verification:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCorrectionGainV2_71
```

Expected: PASS.

---

### Task 3: Exact-head governance validation

- Open Draft stacked PR from `formal/dependent-origination-correction-gain-v271` to `formal/dependent-origination-filtered-obstruction-core-v270`.
- PR diff must contain exactly `formal/KUOS/DependentOriginationCorrectionGainV2_71.lean`.
- PR title: `Formalize exact-invariant correction gain v2.71`.
- Keep Draft.
- Require `KuuOS PR Governance Gate` on the exact head SHA.
- Require `Strict Lean formal validation = success` and final governance summary `= success`.
- Do not mark ready or merge.

## Self-Review Result

- Finite/infinite boundary is explicit: only finite `k` is constructed.
- The correction choice is relational/existential; no canonical selector is introduced.
- Intermediate correction states are retained by the inductive chain proof object.
- Exact invariant and terminal residual order are both certified.
- No v2.72 completion assumptions leak into v2.71.
