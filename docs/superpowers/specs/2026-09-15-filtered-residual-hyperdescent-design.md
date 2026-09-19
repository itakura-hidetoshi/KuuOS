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
+ make an infinite correction history explicit rather than inferred
+ pass to a limit only through a stated level-transfer principle
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
- infer an infinite correction tower from one-step existential correction without an explicit choice/construction boundary,
- add axioms, `sorry`, or `admit`.

It must:

- separate exact constraints from residual defects,
- expose filtration order explicitly,
- allow nondeterministic/existential finite correction steps,
- represent infinite correction histories as explicit data,
- state exactly which limit principle turns eventual level control into flatness,
- require the distinguished exact defect itself to be flat,
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
  F.Flat e ∧ ∀ d, F.Flat d → d = e
```

The intended interpretation is:

```text
OrderAtLeast F n d = defect d vanishes through level n
Flat F d           = defect lies in every filtration level
SeparatedAt F e    = e is flat and every flat defect equals e
```

This definition prevents vacuous “separatedness” in a filtration with no flat elements.

### 4.3 Required theorems

At minimum:

```lean
orderAtLeast_mono
flat_orderAtLeast
separatedAt_exact_flat
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

### 5.2 One-step gain predicate

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

The witness `y` may depend on the certified current order `n`. This dependence is retained rather than erased.

### 5.3 Finite correction chain

Define a finite chain carrying the certified order at each stage. The chain must store enough data that no theorem needs to guess which existential witness was selected.

Schematic data:

```lean
structure FiniteCorrectionChain
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (δ n₀ k : ℕ) where
  state : Fin (k + 1) → State
  invariant : ∀ i, P.invariant (state i)
  step : ∀ i : Fin k, Step (state i.castSucc) (state i.succ)
  order : ∀ i, F.OrderAtLeast (n₀ + i.1 * δ) (P.residual (state i))
```

Exact indexing may be adjusted to Mathlib ergonomics, but the stored mathematical content must remain explicit.

### 5.4 Required theorem boundary

v2.71 proves finite iteration only. From `HasCorrectionGain`, an invariant initial state, and an initial order certificate, prove existence of a `k`-step finite correction chain ending at order at least `n₀ + k * δ`.

It must not claim:

- convergence,
- existence of an infinite tower,
- flatness,
- exact residual triviality.

This keeps finite dependent choice separate from the later infinite-history boundary.

## 6. v2.72 — Flat Completion / Limit Descent

v2.72 adds the abstract data needed to turn an **explicit** arbitrarily improving correction history into flatness. It does not derive that infinite history from v2.71.

### 6.1 Filtered correction tower

```lean
structure FilteredCorrectionTower
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

A positive-gain hypothesis `0 < δ` is supplied to theorems using the tower rather than hidden in the structure.

This explicit `order` field is intentional: an arbitrary `Step` tower need not consist of the improving witnesses promised existentially by v2.71.

### 6.2 Limit transfer datum

Do not assume a topology. Instead isolate exactly what a chosen limit construction must prove:

```lean
structure ResidualLimitData
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (T : FilteredCorrectionTower F P Step δ n₀) where
  limitState : State
  invariant_limit : P.invariant limitState
  level_limit :
    ∀ k,
      (∃ N, ∀ n ≥ N,
        F.OrderAtLeast k (P.residual (T.state n))) →
      F.OrderAtLeast k (P.residual limitState)
```

`invariant_limit` is stored directly. A concrete analytic/topological realization may later prove it from a convergence theorem, but the generic core does not pretend that arbitrary invariants are closed under unspecified limits.

`level_limit` is the precise authority boundary between an asymptotic correction history and an actual completed state.

### 6.3 Main theorem

Given `0 < δ`, arithmetic implies that for every fixed filtration level `k`, sufficiently late stages of the tower lie in level `k`. `ResidualLimitData.level_limit` then gives

```lean
F.Flat (P.residual L.limitState)
```

and `L.invariant_limit` supplies the exact invariant.

No theorem may conclude

```lean
P.residual L.limitState = e
```

without an explicit `F.SeparatedAt e` hypothesis.

### 6.4 Separated completion corollary

With separatedness, prove the conservative corollary:

```lean
0 < δ →
F.SeparatedAt e →
P.residual L.limitState = e.
```

This is the only generic route in v2.72 from arbitrarily high correction order to exact residual triviality.

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

This formally distinguishes a **hard obstruction** from a defect that can be pushed to arbitrarily high filtration order in some correction system.

## 8. The mathematical distinction introduced by v2.70–v2.73

After these layers, KuuOS can distinguish:

```text
exactly trivial obstruction
    d = e

flat obstruction
    d ∈ ⋂ₙ Fⁿ

separated flat obstruction
    d ∈ ⋂ₙ Fⁿ and separatedness forces d = e

finite-order correctable obstruction
    certified correction steps raise filtration order

completed correctable obstruction
    an explicit improving tower plus level-compatible limit gives flatness

hard obstruction
    d ≠ e in a filtration separated at e, hence d is not flat
```

Thus `flat` is never silently equated with `trivial`, and one-step correctability is never silently promoted to existence of an infinite correction history.

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
Does each certified correction raise obstruction order?
Does an explicit correction history exist?
Does that history admit a level-compatible completion?
Does the completed residual become flat?
Is the filtration separated, so flatness descends to exact triviality?
```

This preserves the KuuOS anti-reification boundary: neither a local approximation, a finite correction theorem, an asymptotic tower, nor a model assertion promotes itself to exact global truth.

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
- a theorem deriving an infinite correction tower from `HasCorrectionGain` without an explicit additional choice/construction principle,
- Borel realization,
- PDE residuals,
- concentration/compactness theorems,
- a theorem that general weak admissibility always admits a correcting tower,
- a theorem that filtered correction implies higher-localization factorization.

These become meaningful only after the generic hard/soft obstruction distinction is theorem-backed.

## 13. Success criterion

The mathematical unit is successful when Lean proves, without altering v2.69, the chain

```text
positive one-step correction gain
→ arbitrarily high finite residual order along finite certified chains
→ flat residual from an explicit improving tower plus justified limit transfer
→ exact triviality only under separatedness
```

and independently proves for the explicit v2.69 octahedral loop

```text
nontrivial generated holonomy
+ filtration separated at identity
→ not flat.
```

That is the first theorem-level KuuOS distinction between a defect that admits controlled asymptotic removal data and a genuinely persistent generated-holonomy obstruction.
