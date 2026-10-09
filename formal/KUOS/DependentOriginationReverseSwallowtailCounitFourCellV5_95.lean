import KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93

namespace KUOS.DependentOriginationReverseSwallowtailCounitFourCellV5_95

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Original counit-centered reverse swallowtail four-cell (v5.95)

The reverse v5.66 boundary is a comparison between two *specified*
counit-followed-by-triangle composites. For the actual v5.58 triangles,
the first path at Y is

  (F.map (eta.app (G.obj Y)) ; eps.app (F.obj (G.obj Y))) ; eps.app Y,

and the second path is

  F.map (eta.app (G.obj Y) ; G.map (eps.app Y)) ; eps.app Y.

There is a canonical four-cell comparison in the original target
bicategory. Use the original counit's own pseudonaturality at eps.app Y,
surrounded by the associators and F.mapComp; no strictification,
replacement counit, triangle adjustment, or additional axiom is used.

This is an *objectwise invertible 2-cell*, not yet a modification.
Its whole-morphism naturality and its equality to the original target
triangulator paste remain genuine F4 obligations.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Canonical reverse four-cell at a target object, built entirely from
the unchanged F/G/eta/eps. In particular the *inverse* of eps's own
naturality is used, and the inverse F.mapComp restores the original
right-hand triangle rather than a strict surrogate. -/
def actualLiftReverseSwallowtailComponentInterchanger
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (reverseSwallowtailLeft
      (actualLiftReverseSwallowtailDatum
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).app Y ≅
    (reverseSwallowtailRight
      (actualLiftReverseSwallowtailDatum
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).app Y := by
  let F :=
    actualLiftForwardPseudofunctor
      (W := W) A WorldLabel PresentationLabel
  let G :=
    actualLiftQuasiInversePseudofunctor
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  let eta :=
    actualLiftSourceRoundtripUnit
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  let eps :=
    actualLiftTargetRoundtripCounit
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  exact
    (α_
      (F.map (eta.app (G.obj Y)))
      (eps.app (F.obj (G.obj Y)))
      (eps.app Y)) ≪≫
    Bicategory.whiskerLeftIso
      (F.map (eta.app (G.obj Y)))
      (eps.naturality (eps.app Y)).symm ≪≫
    (α_
      (F.map (eta.app (G.obj Y)))
      (F.map (G.map (eps.app Y)))
      (eps.app Y)).symm ≪≫
    Bicategory.whiskerRightIso
      (F.mapComp (eta.app (G.obj Y)) (G.map (eps.app Y))).symm
      (eps.app Y)

/-- The genuine original reverse interchanger is invertible at every
target object, before imposing any global F4 modification equation. -/
theorem actualLiftReverseSwallowtailComponentInterchanger_inverse
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A Y).hom ≫
    (actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A Y).inv =
      𝟙 ((reverseSwallowtailLeft
        (actualLiftReverseSwallowtailDatum
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).app Y) :=
  (actualLiftReverseSwallowtailComponentInterchanger
    (W := W) A Y).hom_inv_id

#print axioms actualLiftReverseSwallowtailComponentInterchanger
#print axioms actualLiftReverseSwallowtailComponentInterchanger_inverse

end

end KUOS.DependentOriginationReverseSwallowtailCounitFourCellV5_95
