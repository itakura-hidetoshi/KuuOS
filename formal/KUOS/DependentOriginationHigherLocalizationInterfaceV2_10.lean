import Mathlib.CategoryTheory.Bicategory.Functor.LocallyDiscrete
import KUOS.DependentOriginationHigherStackCarrierV2_9

namespace KUOS.DependentOriginationHigherLocalizationInterfaceV2_10

open CategoryTheory
open Opposite
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Higher presentation-localization interface v2.10

The v2.9 layer constructs the native Cat-valued stack carrier

```text
DO₂(C,W,A)
```

as the full sub-bicategory of pseudofunctors on the localized site satisfying
Mathlib stack descent.

The remaining obstruction is now isolated precisely.  Ordinary localization gives

```text
C --Q--> C[W⁻¹]
```

with a universal property for ordinary functors sending `W` to isomorphisms.  A raw
higher contextual system, however, is a pseudofunctor to `Cat`; the correct weak
presentation-invariance condition is that every morphism in `W` is sent to an
equivalence of categories.  The existing 1-categorical localization theorem does
not automatically provide the corresponding pseudofunctorial factorization.

This file therefore does three things without overclaiming:

1. defines the raw Cat-valued contextual systems and the exact `W`-admissibility
   predicate;
2. defines the canonical restriction of any localized higher system back along the
   presentation unit, including the double-opposite variance correction;
3. packages the missing bicategorical localization statement as explicit
   factorization data, with pointwise-equivalence comparison, and proves that any
   such factorization whose lift is a stack canonically determines an object of
   `DO₂`.

No existence or uniqueness of this higher factorization is postulated as an axiom
or asserted as a theorem here.  Those are the next genuine universal-property
obligations.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A raw Cat-valued higher contextual system before presentation localization. -/
abbrev RawHigherContextualSystem :=
  Pseudofunctor (LocallyDiscrete Context) Cat.{vH, uH}

/-- The ordinary presentation-localization functor, followed by the canonical
variance correction into the double-opposite category used by the localized
stack semantics. -/
noncomputable def higherPresentationUnitFunctor :
    Context ⥤ (HigherLocalizedSite W)ᵒᵖ :=
  W.Q ⋙ opOp (LocalizedContext W)

/-- Restrict a localized Cat-valued contextual system back to the raw context
category along the canonical presentation unit. -/
noncomputable def restrictHigherLocalizedSystem
    (F : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    RawHigherContextualSystem.{u, v, uH, vH} (Context := Context) :=
  Pseudofunctor.comp (higherPresentationUnitFunctor W).toPseudofunctor F

/-- Weak higher presentation invariance: every declared presentation morphism is
sent to an equivalence of categories, not necessarily to a strict isomorphism. -/
def IsHigherWAdmissible
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) : Prop :=
  ∀ ⦃X Y : Context⦄ (f : X ⟶ Y), W f → (R.map f.toLoc).toFunctor.IsEquivalence

/-- Raw higher contextual systems bundled with the exact weak `W`-admissibility
condition required by a bicategorical presentation-localization theorem. -/
def RawHigherWObject :=
  { R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context) //
      IsHigherWAdmissible W R }

/-- Explicit factorization data for the still-missing higher localization theorem.

The comparison is a strong transformation from the restriction of the proposed
localized lift to the raw system.  Requiring every component to be an equivalence
of categories records the correct weak notion of agreement at the Cat-valued
level, without pretending that the two pseudofunctors are definitionally equal. -/
structure HigherLocalizationFactorization
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) where
  /-- Proposed localized pseudofunctor. -/
  lift : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)
  /-- Pseudonatural comparison back to the raw system. -/
  comparison : restrictHigherLocalizedSystem W lift ⟶ R
  /-- The comparison is pointwise an equivalence of categories. -/
  comparison_isEquivalence :
    ∀ X : Context, (comparison.app (.mk X)).toFunctor.IsEquivalence

/-- A higher localization factorization whose localized lift also satisfies the
full generated-topology stack condition. -/
structure HigherStackLocalizationFactorization
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
    extends HigherLocalizationFactorization (W := W) R where
  /-- The localized lift is a genuine Cat-valued stack. -/
  isStack : IsHigherGrothendieckDescentComplete W A lift

/-- Any successful higher localization factorization with stack descent determines
canonically an object of the already-constructed higher carrier `DO₂`. -/
def completion2OfHigherStackLocalizationFactorization
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (h : HigherStackLocalizationFactorization (W := W) A R) :
    DependentOriginationCompletion2 (W := W) A :=
  ⟨h.lift, h.isStack⟩

/-- The object of `DO₂` produced by a successful higher factorization has exactly
the localized pseudofunctor supplied by that factorization. -/
@[simp] theorem completion2OfHigherStackLocalizationFactorization_val
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (h : HigherStackLocalizationFactorization (W := W) A R) :
    (completion2OfHigherStackLocalizationFactorization (W := W) A h :
      HigherStackObject (W := W) A).1 = h.lift := by
  rfl

/-- Existence of a higher localization factorization is kept as an explicit
proposition rather than silently assumed. -/
def HasHigherLocalizationFactorization
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) : Prop :=
  Nonempty (HigherLocalizationFactorization (W := W) R)

/-- Likewise, existence of a factorization landing in the stack carrier is an
explicit proposition. -/
def HasHigherStackLocalizationFactorization
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) : Prop :=
  Nonempty (HigherStackLocalizationFactorization (W := W) A R)

/-- A stack-localization factorization in particular provides ordinary higher
localization factorization data. -/
theorem hasHigherLocalizationFactorization_of_stack
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
    (h : HasHigherStackLocalizationFactorization (W := W) A R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases h with ⟨h⟩
  exact ⟨h.toHigherLocalizationFactorization⟩

/-!
The obstruction is therefore represented formally rather than rhetorically:

```text
raw W-admissible Cat-valued pseudofunctor
          |
          |  higher localization factorization
          |  (existence + coherent uniqueness still to prove)
          v
localized Cat-valued pseudofunctor
          |
          |  stack descent
          v
        DO₂(C,W,A).
```

The next theorem unit should attack the missing universal property itself: prove
existence and coherent essential uniqueness of `HigherLocalizationFactorization`
for `IsHigherWAdmissible` raw systems, or identify an additional hypothesis under
which that theorem is valid.  Only after that bridge is established is a raw
`W + J + H` classification theorem justified.
-/

end KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
