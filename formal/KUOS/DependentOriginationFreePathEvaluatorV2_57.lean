import Mathlib.CategoryTheory.Localization.Construction
import KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56

namespace KUOS.DependentOriginationFreePathEvaluatorV2_57

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56

universe u v uH vH

/-!
# General-W free-path evaluator v2.57

The v2.56 layer proves that weak higher `W`-admissibility already contains,
without any additional mathematical assumption, pointwise half-adjoint
equivalence data for every `w ∈ W`.

Mathlib's canonical localization is constructed from the quiver
`Localization.Construction.LocQuiver W`.  Its edges are exactly

* ordinary arrows `f : X ⟶ Y` of `Context`, and
* formal inverse edges attached to `w ∈ W`.

This file performs the next existence step before quotient descent.  Given the
pointwise v2.56 data, we send ordinary edges to `R.map f` and formal inverse
edges to the chosen quasi-inverse.  The universal property of the free path
category, implemented by Mathlib's `Quiv.lift`, then produces an honest functor

```text
Paths (LocQuiver W) ⥤ Cat.
```

Thus arbitrary finite words in ordinary presentation arrows and formal
`W`-inverses already have a strict path-level evaluation in `Cat`.  No quotient
relation is imposed in this file.  In particular, this is not yet a functor on
`W.Localization` and is not yet the desired localized pseudofunctor.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The quiver-level evaluation of the generators of the canonical localization.

Ordinary arrows are evaluated by the original pseudofunctor `R`.  A formal
inverse edge for `w ∈ W` is evaluated by the chosen inverse functor contained in
the v2.56 half-adjoint equivalence package. -/
noncomputable def localizedGeneratorPrefunctor
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    Localization.Construction.LocQuiver W ⥤q Cat.{vH, uH} where
  obj X := R.obj (.mk X.obj)
  map := by
    intro X Y e
    rcases e with f | w
    · exact R.map f.toLoc
    · exact D.inverse w.1 w.2

/-- Evaluate every finite localization word in `Cat` by the free-category
universal property.

At this stage the source is the free path category, not the quotient
`W.Localization`. -/
noncomputable def freePathEvaluator
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    Paths (Localization.Construction.LocQuiver W) ⥤ Cat.{vH, uH} :=
  Quiv.lift (localizedGeneratorPrefunctor W R D)

/-- The path evaluator has exactly the original fiber category on objects. -/
@[simp] theorem freePathEvaluator_obj
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (X : Localization.Construction.LocQuiver W) :
    (freePathEvaluator W R D).obj (.mk X) = R.obj (.mk X.obj) := by
  rfl

/-- On an ordinary generator, free-path evaluation is exactly the original
`R.map`; no comparison isomorphism is inserted at generator level. -/
@[simp] theorem freePathEvaluator_map_ordinary
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) :
    (freePathEvaluator W R D).map
        (Localization.Construction.ψ₁ W f) = R.map f.toLoc := by
  change 𝟙 _ ≫ R.map f.toLoc = R.map f.toLoc
  simp

/-- On a formal inverse generator, free-path evaluation is exactly the chosen
v2.56 quasi-inverse. -/
@[simp] theorem freePathEvaluator_map_formalInverse
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    (freePathEvaluator W R D).map
        (Localization.Construction.ψ₂ W w hw) = D.inverse w hw := by
  change 𝟙 _ ≫ D.inverse w hw = D.inverse w hw
  simp

/-- Weak `W`-admissibility therefore canonically produces a free-path evaluator
by first choosing the Mathlib half-adjoint equivalences from v2.56. -/
noncomputable def freePathEvaluatorOfAdmissible
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R) :
    Paths (Localization.Construction.LocQuiver W) ⥤ Cat.{vH, uH} :=
  freePathEvaluator W R
    (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)

/-- The admissibility-produced evaluator still agrees exactly with `R.map` on
every ordinary presentation arrow. -/
@[simp] theorem freePathEvaluatorOfAdmissible_map_ordinary
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    {X Y : Context} (f : X ⟶ Y) :
    (freePathEvaluatorOfAdmissible W hR).map
        (Localization.Construction.ψ₁ W f) = R.map f.toLoc := by
  simp [freePathEvaluatorOfAdmissible]

/-!
## Boundary fixed by v2.57

We now have, for general `W`, the exact implication

```text
IsHigherWAdmissible W R
        ↓
pointwise chosen half-adjoint equivalences on R.map(w)
        ↓
LocQuiver W ⥤q Cat
        ↓ Quiv.lift
Paths (LocQuiver W) ⥤ Cat.
```

The missing step is no longer evaluation of formal inverse words.  It is descent
through the quotient defining `W.Localization`.

For the four generating relations

```text
id, comp, Winv₁, Winv₂
```

the expected comparison 2-isomorphisms are supplied respectively by
`R.mapId`, `R.mapComp`, and the unit/counit isomorphisms in the chosen v2.56
adjoint-equivalence data.  The next layer should package these generating
relation isomorphisms explicitly and then isolate the coherence required to make
the resulting transport independent of a chosen derivation in the quotient
relation closure.

No quotient pseudofunctor, higher-localization factorization, stackification, or
general universal property is claimed here.
-/

end KUOS.DependentOriginationFreePathEvaluatorV2_57
