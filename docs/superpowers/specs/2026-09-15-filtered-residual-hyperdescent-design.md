# KuuOS Filtered Residual Hyperdescent v2.70–v2.73 — Design

**Date:** 2026-09-15 JST

**Status:** design-only, non-authoritative, stacked on the open v2.69 proof head

**Stack base:** `940c3b8f164ac35e49e6fcf2532aef9bba3c2eff`

**Upstream PR:** #1651 — `Truth-test weak admissibility with octahedral generated holonomy v2.69`

## 1. Authority boundary

This design does not promote any new theorem into KuuOS authority. The upstream v2.69 PR remains Draft and unmerged. This branch records the next mathematical architecture only.

Authority remains:

1. canonical GitHub theorem SHA,
2. formal Lean artifacts,
3. README / ROADMAP,
4. CI/runtime receipts,
5. memory or model interpretation.

The OpenAI Navier–Stokes work is used as mathematical inspiration, not as an imported axiom or theorem dependency.

## 2. Mathematical motivation

The current KuuOS higher dependent-origination line has sharpened the general-W obstruction through:

```text
pointwise choices
→ five coherence defects
→ gauge obstruction
→ retained relation 2-cells
→ fully generated localization 2-cells
→ generated-loop holonomy.
```

v2.69 supplies an explicit six-object octahedral countermodel whose generated loop has nontrivial `C2` holonomy. Thus weak admissibility alone does not force generated-holonomy triviality.

The next question is not merely whether an obstruction is zero, but whether it can be improved through a sequence of exact-invariant-preserving corrections. The abstraction suggested by the constructive Navier–Stokes proof is:

```text
retain exact constraints
+ measure residual order by a decreasing filtration
+ improve that order by correction steps
+ pass to a limit that preserves eventual level membership
+ distinguish flat-but-nontrivial phenomena from genuinely trivial defects.
```

This design calls that layer **Filtered Residual Hyperdescent**.

## 3. Design principles

The new layer must be a conservative extension of v2.68–v2.69.

It must not:

- weaken `GeneratedHolonomyTrivial`,
- reinterpret nontrivial v2.69 holonomy as trivial,
- assume a metric, topology, norm, or completeness in v2.70,
- introduce PDE-specific objects into the KuuOS core,
- silently identify asymptotic smallness with equality,
- add axioms, `sorry`, or `admit`.

It must:

- separate exact constraints from residual defects,
- expose filtration order explicitly,
- allow nondeterministic/existential correction steps,
- state exactly which limit principle turns eventual level control into flatness,
- require separatedness before flatness can imply exact triviality,
- connect back to generated holonomy only through an explicit bridge.

## 4. v2.70 — Filtered Obstruction Core

### 4.1 Core structure

Introduce a generic decreasing filtration without assuming algebraic structure:

```lean
structure ObstructionFiltration (D : Type u) where
  level : ℕ → Set D
  antitone_level : Antitone level
```

This is deliberately weaker than a filtered group. Later layers may add compatibility with multiplication/composition without changing the core API.

### 4.2 Predicates

```lean
def ObstructionFiltration.OrderAtLeast
    (F : ObstructionFiltration D) (n : ℕ) (d : D) : Prop :=
  d ∈ F.level n

def ObstructionFiltration.Flat
    (F : ObstructionFiltration D) (d : D) : Prop :=
  ∀ n, d ∈ F.level n

def ObstructionFiltration.SeparatedAt
    (F : ObstructionFiltration D) (e : D) : Prop :=
  ∀ d, F.Flat d → d = e
```

The intended interpretation is:

```text
OrderAtLeast F n d = defect d vanishes through level n
Flat F d           = defect lies in every filtration level
SeparatedAt F e    = the only flat defect is the distinguished exact defect e
```

### 4.3 Required theorems

At minimum:

```lean
orderAtLeast_mono
flat_orderAtLeast
flat_eq_of_separatedAt
not_flat_of_ne_of_separatedAt
```

The final theorem is essential for v2.73:

```lean
F.SeparatedAt e → d ≠ e → ¬ F.Flat d.
```

### 4.4 No premature algebra

v2.70 must not require `Group D`, `Monoid D`, `TopologicalSpace D`, or `MetricSpace D`. Those structures are instances or later refinements, not the definition of filtered obstruction itself.

## 5. v2.71 — Exact-Invariant Correction Gain

### 5.1 Residual problem

Introduce a problem whose states have an exact invariant and a residual:

```lean
structure ResidualProblem (State : Type u) (D : Type v) where
  invariant : State → Prop
  residual : State → D
```

A correction relation is intentionally relational rather than functional:

```lean
Step : State → State → Prop
```

This avoids hiding noncanonical correction choices inside `Classical.choice`.

### 5.2 Gain predicate

For positive gain `δ`:

```lean
def HasCorrectionGain
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
```

### 5.3 Required theorem boundary

v2.71 proves finite iteration only. It must not claim convergence.

Define a finite correction chain and prove that `k` correction steps raise the residual order by at least `k * δ`, while preserving the exact invariant.

Schematic target:

```text
initial residual ∈ F^n
+ k admissible correction steps of gain δ
------------------------------------------
final residual ∈ F^(n + kδ)
and invariant remains exact.
```

This is the formal analogue of repeated residual-order improvement while preserving a hard constraint by construction.

## 6. v2.72 — Flat Completion / Limit Descent

v2.72 adds only the abstract limit principle needed to turn arbitrarily high finite order into flatness.

### 6.1 Correction tower

A tower stores the actual sequence and proof of each step:

```lean
structure CorrectionTower
    (Step : State → State → Prop) where
  state : ℕ → State
  step : ∀ n, Step (state n) (state (n + 1))
```

### 6.2 Limit transfer datum

Do not assume a topology. Instead isolate exactly what a chosen limit construction must prove:

```lean
structure ResidualLimitData
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (T : CorrectionTower Step) where
  limitState : State
  invariant_limit :
    (∀ n, P.invariant (T.state n)) → P.invariant limitState
  level_limit :
    ∀ k,
      (∃ N, ∀ n ≥ N, F.OrderAtLeast k (P.residual (T.state n))) →
      F.OrderAtLeast k (P.residual limitState)
```

This datum is the authority boundary between a formal/asymptotic tower and an actual completed state.

### 6.3 Main theorem

Under positive correction gain, an initial finite-order bound, and a compatible correction tower, residual order eventually exceeds every fixed level. `ResidualLimitData.level_limit` then gives:

```lean
F.Flat (P.residual L.limitState)
```

while `invariant_limit` preserves the exact invariant.

No theorem may conclude `P.residual L.limitState = e` without an explicit `F.SeparatedAt e` hypothesis.

## 7. v2.73 — Filtered Generated-Holonomy Bridge

### 7.1 Per-loop obstruction object

For a fixed generated localization loop `γ` at path `p`, use

```lean
D := ((freePathEvaluator W R D₀).map p ≅
      (freePathEvaluator W R D₀).map p)
```

as the obstruction type and

```lean
e := Iso.refl _
```

as the exact defect.

The bridge does not impose a canonical filtration on every automorphism type. A filtration is explicit input.

### 7.2 Flat generated holonomy

Define a local predicate:

```lean
FilteredGeneratedHolonomyFlat F γ :=
  F.Flat (generatedHolonomy W R D₀ γ)
```

Then prove:

```lean
F.SeparatedAt (Iso.refl _) →
FilteredGeneratedHolonomyFlat F γ →
generatedHolonomy W R D₀ γ = Iso.refl _.
```

This is one-way unless further hypotheses are supplied.

### 7.3 v2.69 hard-obstruction theorem

Import the v2.69 countermodel only in the countermodel bridge file, not in the generic bridge.

Use the proved theorem

```lean
counterGeneratedLoop_holonomy_ne_refl
```

to derive:

```lean
F.SeparatedAt (Iso.refl _) →
¬ F.Flat
    (generatedHolonomy allMorphisms counterSystem D counterGeneratedLoop).
```

In particular, for `counterD`, the explicit octahedral holonomy is not merely nontrivial; it is incompatible with flatness in every filtration separated at the identity.

This formally distinguishes a **hard obstruction** from a defect that can be pushed to arbitrarily high filtration order.

## 8. The mathematical distinction introduced by v2.70–v2.73

After these layers, KuuOS can distinguish:

```text
exactly trivial obstruction
    d = e

flat obstruction
    d ∈ ⋂ₙ Fⁿ

separated flat obstruction
    d ∈ ⋂ₙ Fⁿ and separatedness forces d = e

correctable obstruction
    finite correction steps raise filtration order

hard obstruction
    d ≠ e in a separated filtration, hence d is not flat
```

Thus `flat` is never silently equated with `trivial`.

## 9. Relation to dependent origination

The new layer refines the existing descent question:

```text
Can local data glue globally?
```

into:

```text
What is the obstruction presentation?
At what filtration order does it survive?
Which corrections preserve the exact invariant?
Does each correction raise obstruction order?
Does the correction history admit a completion?
Does the completed residual become flat?
Is the filtration separated, so flatness descends to exact triviality?
```

This preserves the KuuOS anti-reification boundary: neither a local approximation, an asymptotic tower, nor a model assertion promotes itself to exact global truth.

## 10. File decomposition

Planned theorem files:

```text
formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
formal/KUOS/DependentOriginationCorrectionGainV2_71.lean
formal/KUOS/DependentOriginationFlatCompletionV2_72.lean
formal/KUOS/DependentOriginationFilteredGeneratedHolonomyV2_73.lean
formal/KUOS/DependentOriginationFilteredHolonomyCountermodelV2_73.lean
```

The generic v2.73 file imports v2.68 but not v2.69. The countermodel v2.73 file imports the v2.69 evaluation theorem and the generic v2.73 bridge.

`formal/KuuOSFormalV0_69.lean` is not renamed merely because these layers are added; umbrella/version changes remain a separate repository-governance decision.

## 11. Validation requirements

Every theorem unit must satisfy the existing KuuOS proof discipline:

- pinned repository Lean/mathlib toolchain,
- no `sorry`, `admit`, or new axioms,
- additive/tighten-only changes,
- theorem names and imports explicit,
- exact-head CI validation before any promotion,
- v2.69 remains unchanged by v2.70–v2.73,
- negative v2.69 theorem remains a negative theorem; no reinterpretation as factorization failure.

Expected axiom footprint for the new elementary generic layers should be no stronger than ordinary Mathlib logical dependencies already accepted by the repository. Any unexpected axiom dependency is a blocker.

## 12. Deferred extensions

The following are intentionally outside v2.70–v2.73:

- filtered groups / pronilpotent groups,
- multiplicative compatibility `F^m * F^n ⊆ F^(m+n)`,
- metric or topological completeness,
- Borel realization,
- PDE residuals,
- concentration/compactness theorems,
- a theorem that general weak admissibility always admits a correcting tower,
- a theorem that filtered correction implies higher-localization factorization.

These become meaningful only after the generic hard/soft obstruction distinction is theorem-backed.

## 13. Success criterion

The mathematical unit is successful when Lean proves, without altering v2.69, the chain

```text
positive correction gain
→ arbitrarily high finite residual order
→ flat residual at an explicitly justified limit
→ exact triviality only under separatedness
```

and independently proves for the explicit v2.69 octahedral loop

```text
nontrivial generated holonomy
+ separated filtration at identity
→ not flat.
```

That is the first theorem-level KuuOS distinction between an asymptotically removable obstruction and a genuinely persistent generated-holonomy obstruction.
