# Filtered Generated-Holonomy Bridge v2.73 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Connect the generic filtered-obstruction theory to fully generated localization-loop holonomy and prove that the explicit v2.69 octahedral nontrivial holonomy is not flat in any filtration separated at the identity.

**Architecture:** The generic bridge imports v2.72 and v2.68 but not v2.69. For each fixed generated loop, its evaluated automorphism type is used as the obstruction carrier; a filtration is explicit input. A second countermodel-only file imports the generic bridge and v2.69 evaluation theorem and derives the hard-obstruction result from `counterGeneratedLoop_holonomy_ne_refl`.

**Tech Stack:** Lean `leanprover/lean4:v4.30.0-rc2`; Mathlib rev `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; Lake; exact-head GitHub CI.

**Spec:** `docs/superpowers/specs/2026-09-15-filtered-residual-hyperdescent-design.md`

## Global Constraints

- Stack on v2.72 exact green head `7e3cad8513fec8250dc960e80b1c9bca8b3888c9`.
- Generic bridge must not import any v2.69 countermodel file.
- No canonical filtration is imposed on automorphism types; `F` is always explicit input.
- Do not weaken or redefine `GeneratedHolonomyTrivial`.
- Flatness implies identity only with `SeparatedAt (Iso.refl _)`.
- Countermodel theorem must use the already proved v2.69 nontrivial-holonomy theorem; do not re-prove the octahedral calculation.
- No claim that weak admissibility admits a correcting tower or that correction implies higher-localization factorization.
- No `sorry`, `admit`, new `axiom`, or umbrella/version promotion.

---

### Task 1: Generic per-loop filtered holonomy bridge

**Files:**
- Create: `formal/KUOS/DependentOriginationFilteredGeneratedHolonomyV2_73.lean`

Core interface:

```lean
import KUOS.DependentOriginationFlatCompletionV2_72
import KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

namespace KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73

open CategoryTheory
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]

/-- A fixed generated loop has flat evaluated holonomy relative to an explicit
filtration on its automorphism carrier. -/
def FilteredGeneratedHolonomyFlat
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (F : ObstructionFiltration
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (γ : GeneratedLocalizationLoop W p) : Prop :=
  F.Flat (generatedHolonomy W R D γ)
```

Prove:

```lean
theorem generatedHolonomy_eq_refl_of_filteredFlat
    ...
    (F : ObstructionFiltration (...))
    (γ : GeneratedLocalizationLoop W p)
    (hsep : F.SeparatedAt (Iso.refl _))
    (hflat : FilteredGeneratedHolonomyFlat W R D F γ) :
    generatedHolonomy W R D γ = Iso.refl _ := by
  exact F.flat_eq_of_separatedAt hsep hflat
```

This theorem is local to one loop and makes no global holonomy-triviality assertion.

---

### Task 2: v2.69 octahedral hard-obstruction bridge

**Files:**
- Create: `formal/KUOS/DependentOriginationFilteredHolonomyCountermodelV2_73.lean`

Imports:

```lean
import KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
import KUOS.DependentOriginationGeneratedHolonomyCountermodelEvaluationV2_69
```

Open the existing v2.69 namespace and define an abbreviation for the fixed loop's automorphism carrier if it improves elaboration readability.

Target theorem for arbitrary pointwise data:

```lean
theorem counterGeneratedLoop_not_flat_of_separated
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration
      ((freePathEvaluator allMorphisms counterSystem D).map
          (rawPath a00 ≫ rawPath b00) ≅
       (freePathEvaluator allMorphisms counterSystem D).map
          (rawPath a00 ≫ rawPath b00)))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    ¬ F.Flat
      (generatedHolonomy allMorphisms counterSystem D counterGeneratedLoop) := by
  exact F.not_flat_of_ne_of_separatedAt hsep
    (counterGeneratedLoop_holonomy_ne_refl D)
```

Also expose the predicate-level formulation:

```lean
theorem counterGeneratedLoop_not_filteredGeneratedHolonomyFlat
    ... :
    ¬ FilteredGeneratedHolonomyFlat
      allMorphisms counterSystem D F counterGeneratedLoop :=
  counterGeneratedLoop_not_flat_of_separated D F hsep
```

Finally specialize to `counterD` if elaboration remains simple; otherwise the arbitrary-`D` theorem is mathematically stronger and sufficient.

---

### Task 3: Exact-head governance validation

- Branch: `formal/dependent-origination-filtered-generated-holonomy-v273`.
- Base: `formal/dependent-origination-flat-completion-v272`.
- Draft PR title: `Bridge filtered obstruction to generated holonomy v2.73`.
- Final changed files exactly:
  - `formal/KUOS/DependentOriginationFilteredGeneratedHolonomyV2_73.lean`
  - `formal/KUOS/DependentOriginationFilteredHolonomyCountermodelV2_73.lean`
- First validate the generic bridge alone if needed; then add the countermodel bridge and revalidate the new exact head.
- Require strict Lean formal validation and governance summary success on the final exact head.
- Keep Draft; do not merge or mark ready.

## Self-Review Result

- Generic v2.73 has no dependency on v2.69.
- The filtration remains explicit; there is no invented canonical notion of asymptotic smallness for arbitrary automorphisms.
- The countermodel conclusion is exactly `nontrivial + separated ⇒ not flat`.
- No factorization theorem is inferred from the new filtered language.
