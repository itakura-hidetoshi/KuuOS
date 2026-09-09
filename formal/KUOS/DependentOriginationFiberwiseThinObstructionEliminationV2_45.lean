import Mathlib.CategoryTheory.Thin
import KUOS.DependentOriginationIsDiscreteBaseObstructionEliminationV2_44

namespace KUOS.DependentOriginationFiberwiseThinObstructionEliminationV2_45

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42

universe u v uH vH

/-!
# Fiberwise-thin obstruction elimination v2.45

The v2.43/v2.44 route kills the modification-coherence obstruction by making
the **base** category discrete.  This file proves an independent structural
route: keep the base category arbitrary, but assume that every category in the
raw Cat-valued contextual system is thin.

For a base arrow `f : X ⟶ Y`, the modification-naturality equation for a stored
v2.18 triangle is an equality between two Cat 2-cells whose common target is the
raw fiber `R.obj (.mk Y)`.  If that fiber is thin, the corresponding functor
category is thin by Mathlib's `CategoryTheory.functor_thin`; hence the underlying
natural transformations are unique.  `Cat.Hom₂.ext` then identifies the two
Cat 2-cells without any assumption on the base arrow.

Thus we obtain a second genuine obstruction-killing mechanism:

```text
fiberwise thin raw system
  -> every stored v2.18 triangle is modification-natural
  -> factor modification-triangle lifting
  -> factor-coherence lifting
  -> weak universality on the coherent chosen carrier
  -> coherent route completeness
  -> no local v2.42 E/R obstruction.
```

This does not assert that arbitrary Cat-valued systems are fiberwise thin, does
not collapse the base category to a discrete one, and does not prove coherent
universal-data existence.  It isolates a target-side 2-cell uniqueness criterion
that is logically independent of the base-side discreteness criterion of v2.44.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Every raw contextual fiber has at most one morphism between any two objects.
This is a property of the Cat-valued target fibers, not of the base context
category. -/
def HigherRawFiberwiseThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ X : Context, Quiver.IsThin (R.obj (.mk X))

/-- Cat 2-cells between fixed functors into a thin target category are unique.
Mathlib supplies thinness of the ordinary functor category; `Cat.Hom₂.ext`
transfers that uniqueness through the Cat 2-cell wrapper. -/
theorem subsingleton_catHom₂_of_targetThin
    {C D : Cat.{vH, uH}} [Quiver.IsThin D]
    (F G : C ⟶ D) : Subsingleton (F ⟶ G) := by
  constructor
  intro η θ
  apply Cat.Hom₂.ext
  exact Subsingleton.elim _ _

/-- Fiberwise thinness makes every stored v2.18 triangle automatically
modification-natural, with no discreteness assumption on `Context`. -/
theorem storedV2_18TriangleIsModificationNatural_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredV2_18TriangleIsModificationNatural (W := W) alpha := by
  intro X Y f
  letI : Quiver.IsThin (R.obj (.mk Y)) := hThin Y
  apply Cat.Hom₂.ext
  exact Subsingleton.elim _ _

/-- Uniform stored-triangle modification naturality follows from fiberwise
thinness of the raw system. -/
theorem higherStoredV2_18TriangleModificationNaturality_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18TriangleModificationNaturality (W := W) U := by
  intro H alpha
  exact storedV2_18TriangleIsModificationNatural_of_fiberwiseThin
    (W := W) hThin alpha

/-- Fiberwise thinness therefore makes factor-coherence lifting automatic for a
fixed coherent universal datum. -/
theorem higherFactorCoherenceLifting_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorCoherenceLifting (W := W) U :=
  higherFactorCoherenceLifting_of_storedTriangleNaturality
    W U
      (higherStoredV2_18TriangleModificationNaturality_of_fiberwiseThin
        (W := W) hThin U)

/-- On a fiberwise-thin raw system, coherent universal data already give a full
v2.18 weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_fiberwiseThin_coherent
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  exact ⟨weakHigherLocalizationUniversalPropertyOfCoherent
    W U (higherFactorCoherenceLifting_of_fiberwiseThin (W := W) hThin U)⟩

/-- The route obstruction also disappears: the required correction/modification
lifting is forced by 2-cell uniqueness in the raw target fibers. -/
theorem higherCoherentRouteCompleteness_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U := by
  intro _hUniversal
  apply
    (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
      (W := W) U).mpr
  exact
    higherFactorModificationTriangleLifting_of_storedTriangleNaturality
      W U
        (higherStoredV2_18TriangleModificationNaturality_of_fiberwiseThin
          (W := W) hThin U)

/-- Fiberwise thinness gives the positive aligned state of the v2.42 local
classification. -/
theorem higherWeakCoherentAlignment_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_fiberwiseThin_coherent
      (W := W) hThin U,
    higherCoherentRouteCompleteness_of_fiberwiseThin (W := W) hThin U⟩

/-- Exact local E/R obstruction elimination under the target-side fiberwise
thinness criterion. -/
theorem no_twoAxisObstruction_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin (W := W) R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_fiberwiseThin (W := W) hThin U)

end KUOS.DependentOriginationFiberwiseThinObstructionEliminationV2_45
