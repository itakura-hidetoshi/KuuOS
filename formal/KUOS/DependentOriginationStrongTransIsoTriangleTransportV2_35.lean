import KUOS.DependentOriginationRouteCompletenessInternalGapV2_34

namespace KUOS.DependentOriginationStrongTransIsoTriangleTransportV2_35

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# StrongTrans-isomorphism triangle transport v2.35

The v2.34 layer isolated one explicit remaining 2-cell hypothesis:
`HigherFactorModificationTriangleIsoTransport`.  This file discharges that
hypothesis from the actual bicategory structure supplied by Mathlib.

For an isomorphism `e : alpha ≅ beta` of StrongTrans 1-cells, restriction along
the higher presentation unit is again an isomorphism of StrongTrans.  Right
whiskering that restricted isomorphism by the fixed comparison StrongTrans gives

```text
restrict(alpha) ≫ K.comparison ≅ restrict(beta) ≫ K.comparison.
```

Composing with an already-existing modification triangle for `beta` produces the
required triangle for `alpha`.

No strictification, carrier identification, ordinary-localization substitute,
or new axiom is used.  The construction is entirely internal to the hom-category
of StrongTrans and Mathlib bicategorical whiskering.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Restriction along the higher presentation unit preserves an isomorphism of
StrongTrans 1-cells.

The object components are obtained by evaluating the original invertible
modification at the image of the presentation unit.  Naturality is inherited
from the original modification. -/
def restrictHigherLocalizedStrongTransIso
    {F G : HigherLocalizedDescentSystem (W := W)}
    {alpha beta : F ⟶ G}
    (e : alpha ≅ beta) :
    restrictHigherLocalizedStrongTrans (W := W) alpha ≅
      restrictHigherLocalizedStrongTrans (W := W) beta :=
  CategoryTheory.Pseudofunctor.StrongTrans.isoMk
    (fun X =>
      { hom := e.hom.as.app ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)
        inv := e.inv.as.app ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)
        hom_inv_id := by
          have h := congrArg
            (fun m => m.as.app ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))
            e.hom_inv_id
          exact h
        inv_hom_id := by
          have h := congrArg
            (fun m => m.as.app ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))
            e.inv_hom_id
          exact h })
    (by
      intro X Y f
      simpa [restrictHigherLocalizedStrongTrans] using
        e.hom.as.naturality
          ((higherPresentationUnitFunctor W).toPseudofunctor.map f))

/-- An isomorphism between factor StrongTrans 1-cells transports an existing
modification triangle from the second factor to the first. -/
theorem hasFactorModificationTriangle_of_iso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha beta : HigherLocalizationFactorMorphism (W := W) H K)
    (e : alpha.hom ≅ beta.hom)
    (hBeta : HasFactorModificationTriangle (W := W) beta) :
    HasFactorModificationTriangle (W := W) alpha := by
  rcases hBeta with ⟨triangle⟩
  refine ⟨?_⟩
  exact
    Bicategory.whiskerRightIso
        (restrictHigherLocalizedStrongTransIso (W := W) e)
        K.comparison ≪≫
      triangle

/-- The v2.34 StrongTrans-isomorphism triangle-transport property is therefore
unconditional for every coherent universal datum. -/
theorem higherFactorModificationTriangleIsoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorModificationTriangleIsoTransport (W := W) U := by
  intro H alpha beta hIso hBeta
  rcases hIso with ⟨e⟩
  exact hasFactorModificationTriangle_of_iso (W := W) alpha beta e hBeta

/-- Global form: the explicit v2.34 iso-transport principle follows from the
Mathlib bicategory of pseudofunctors and StrongTrans. -/
theorem higherFactorModificationTriangleIsoTransportPrinciple :
    HigherFactorModificationTriangleIsoTransportPrinciple
      (W := W) (uH := uH) (vH := vH) := by
  intro R U
  exact higherFactorModificationTriangleIsoTransport (W := W) U

/-- Consequently, for every coherent universal datum, route completeness is
exactly fixed-chosen essential-uniqueness reflection, with no separate
iso-coherence transport hypothesis remaining. -/
theorem routeCompleteness_iff_fixedChosenReflection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenEssentialUniquenessReflection (W := W) U :=
  routeCompleteness_iff_fixedChosenReflection_of_isoTransport
    (W := W) U (higherFactorModificationTriangleIsoTransport (W := W) U)

/-- The corresponding exact failure normal form has only the fixed-chosen
reflection obstruction. -/
theorem not_routeCompleteness_iff_reflectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenEssentialUniquenessReflectionFailure (W := W) U :=
  not_routeCompleteness_iff_reflectionFailure_of_isoTransport
    (W := W) U (higherFactorModificationTriangleIsoTransport (W := W) U)

/-!
After v2.35 the second v2.34 obstruction is closed:

```text
alpha.hom ≅ beta.hom
        |
        | restrict the invertible modification
        v
restrict(alpha.hom) ≅ restrict(beta.hom)
        |
        | Bicategory.whiskerRightIso _ K.comparison
        v
restrict(alpha.hom) ≫ K.comparison
      ≅
restrict(beta.hom) ≫ K.comparison
        |
        | compose with beta's triangle
        v
H.comparison.
```

Thus the remaining route-completeness gap is not modification transport.  It is
precisely the fixed-chosen essential-uniqueness reflection problem identified in
v2.34.
-/

end KUOS.DependentOriginationStrongTransIsoTriangleTransportV2_35
