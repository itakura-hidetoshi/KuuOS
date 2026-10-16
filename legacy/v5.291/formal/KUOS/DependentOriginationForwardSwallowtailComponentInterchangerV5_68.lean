import KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67

namespace KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49

set_option autoImplicit false

noncomputable section

/-!
# Forward swallowtail component interchanger v5.68

v5.67 isolates the eta/eta pseudonaturality core.  This file transports that
core to the full object-component boundary of the v5.65 forward swallowtail
for the unchanged actual-lift datum.

At X the left path is definitionally

  eta_X ; G.map (F.map eta_X ; eps_(F X)),

while the right path is definitionally

  eta_X ; (eta_(R X) ; G.map eps_(F X)),

with R = F ; G.

The canonical comparison is the four-step paste

1. G.mapComp on F.map eta_X and eps_(F X);
2. inverse associator;
3. the inverse eta/eta naturality core, right-whiskered by G.map eps_(F X);
4. associator.

No strictification of G and no replacement of eta, eps, F or G is used.
This is still pointwise data; modification naturality is the next obligation.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

abbrev actualLiftForwardSwallowtailDatumV68 :=
  actualLiftForwardSwallowtailDatum
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev actualLiftForwardSwallowtailSourceV68 :=
  ActualLiftSource
    (W := W) A WorldLabel PresentationLabel

/-- Canonical object-level forward swallowtail interchanger.

The source and target are exactly the two StrongTrans components appearing in
the v5.65 forward swallowtail predicate. -/
def actualLiftForwardSwallowtailComponentInterchanger
    (X :
      actualLiftForwardSwallowtailSourceV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) :
    (forwardSwallowtailLeft
      (actualLiftForwardSwallowtailDatumV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).app X ≅
    (forwardSwallowtailRight
      (actualLiftForwardSwallowtailDatumV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).app X := by
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
    Bicategory.whiskerLeftIso
        (eta.app X)
        (G.mapComp
          (F.map (eta.app X))
          (eps.app (F.obj X))) ≪≫
      (α_
        (eta.app X)
        (G.map (F.map (eta.app X)))
        (G.map (eps.app (F.obj X)))).symm ≪≫
      Bicategory.whiskerRightIso
        (actualLiftUnitSelfNaturalityIso
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)
          X).symm
        (G.map (eps.app (F.obj X))) ≪≫
      (α_
        (eta.app X)
        (eta.app
          ((Pseudofunctor.comp F G).obj X))
        (G.map (eps.app (F.obj X))))

/-- The middle eta/eta comparison used by v5.68 is literally the v5.67 core,
with no new 2-cell choice. -/
@[simp] theorem actualLiftForwardSwallowtailComponentInterchanger_core
    (X :
      actualLiftForwardSwallowtailSourceV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) :
    (actualLiftUnitSelfNaturalityIso
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      X).inv =
    ((actualLiftSourceRoundtripUnit
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality
        ((actualLiftSourceRoundtripUnit
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).app X)).inv :=
  rfl

/-!
## Boundary after v5.68

The canonical forward-swallowtail comparison now exists at every object of the
actual-lift source bicategory and has exactly the v5.65 boundary.

The remaining obstruction is global: prove that these objectwise 2-cells obey
the modification naturality square between
`forwardSwallowtailLeft` and `forwardSwallowtailRight`.  Only after that
global modification is constructed can its equality with the v5.65
`forwardTriangulatorPaste` be stated and proved.
-/

#print axioms actualLiftForwardSwallowtailComponentInterchanger
#print axioms actualLiftForwardSwallowtailComponentInterchanger_core

end

end KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
