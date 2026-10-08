import KUOS.DependentOriginationForwardSwallowtailExplicitResidualV5_90

namespace KUOS.DependentOriginationForwardReverseContractionCancellationV5_91

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationForwardCanonicalNaturalityV5_87
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88
open KUOS.DependentOriginationForwardSwallowtailExplicitResidualV5_90

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Cancel the unchanged reverse triangle contraction (v5.91)

v5.90 identified the exact four-cell/triangulator residual.
The reverse contraction is *invertible*, hence it can be cancelled
on the right in the original source hom category.  This removes the
inverse reverse-contraction from the remaining F3 equation, without
altering either triangulator or assuming the swallowtail condition.

The residual becomes a concrete equality between (1) the original
v5.68 four-cell pasted with the unchanged reverse contraction and
(2) the mapped original forward contraction followed by G.mapId.
-/

namespace Generic

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]

/-- In any bicategory, right cancellation of an invertible 2-cell
commutes with left whiskering.  This is the precise native mathlib
Iso.eq_comp_inv, not an ad hoc cancellation axiom. -/
theorem whiskerLeft_eq_comp_inv_iff
    {X Y Z : B} (f : X ⟶ Y)
    {g h k : Y ⟶ Z} (a : g ⟶ k) (e : h ≅ k)
    (sigma : f ≫ g ⟶ f ≫ h) :
    sigma = f ◁ (a ≫ e.inv) ↔
      sigma ≫ (f ◁ e.hom) = f ◁ a := by
  simpa only [Bicategory.whiskerLeft_comp,
      Bicategory.whiskerLeftIso_hom, Bicategory.whiskerLeftIso_inv] using
    (Iso.eq_comp_inv (Bicategory.whiskerLeftIso f e)
      (f := f ◁ a) (g := sigma))

end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The exact *remaining* F3 condition after cancelling the original
reverse triangle contraction, at each source object.  In contrast
to the previously unexpanded horizontal paste, this keeps only one
mapped forward contraction and its non-strict G.mapId comparison. -/
def ActualLiftForwardSwallowtailCancelledCore : Prop :=
  ∀ X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel,
    ((actualLiftForwardSwallowtailComponentInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) X).hom) ≫
      (((actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app X) ◁
        (actualLiftQuasiInverseTriangleIso (W := W) A
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).hom) =
    ((actualLiftSourceRoundtripUnit (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app X) ◁
      ((actualLiftQuasiInversePseudofunctor (W := W) A).map₂
          ((actualLiftForwardTriangleIso (W := W) A X).hom) ≫
        ((actualLiftQuasiInversePseudofunctor (W := W) A).mapId
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).hom)

/-- Cancelling the reverse contraction is exactly reversible.
No new coherence law is used: the equivalence is the whiskered
iso cancellation theorem, specialized to the original four cells. -/
theorem actualLiftForwardExpanded_iff_cancelled :
    ActualLiftForwardSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) ↔
    ActualLiftForwardSwallowtailCancelledCore.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  constructor
  · intro h X
    let F := actualLiftForwardPseudofunctor
      (W := W) A WorldLabel PresentationLabel
    let G := actualLiftQuasiInversePseudofunctor
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
    let eta := actualLiftSourceRoundtripUnit
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
    let cF := actualLiftForwardTriangleIso (W := W) A X
    let cG := actualLiftQuasiInverseTriangleIso (W := W) A (F.obj X)
    let a := G.map₂ cF.hom ≫ (G.mapId (F.obj X)).hom
    let sigma :=
      (actualLiftForwardSwallowtailComponentInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).hom
    exact (Generic.whiskerLeft_eq_comp_inv_iff (eta.app X) a cG sigma).mp (h X)
  · intro h X
    let F := actualLiftForwardPseudofunctor
      (W := W) A WorldLabel PresentationLabel
    let G := actualLiftQuasiInversePseudofunctor
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
    let eta := actualLiftSourceRoundtripUnit
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
    let cF := actualLiftForwardTriangleIso (W := W) A X
    let cG := actualLiftQuasiInverseTriangleIso (W := W) A (F.obj X)
    let a := G.map₂ cF.hom ≫ (G.mapId (F.obj X)).hom
    let sigma :=
      (actualLiftForwardSwallowtailComponentInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).hom
    exact (Generic.whiskerLeft_eq_comp_inv_iff (eta.app X) a cG sigma).mpr (h X)

/-- Final original global forward-swallowtail predicate is equivalent
to the smaller cancelled-core diagram, by v5.90 and cancellation. -/
theorem actualLiftForwardPredicate_iff_cancelled :
    KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.actualLiftForwardSwallowtailPredicate.{u, v, uH, uW, uP, vH}
      (W := W) A
      (actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) ↔
    ActualLiftForwardSwallowtailCancelledCore.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  exact (actualLiftForwardPredicate_iff_expanded
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)).trans
    (actualLiftForwardExpanded_iff_cancelled
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

#print axioms Generic.whiskerLeft_eq_comp_inv_iff
#print axioms ActualLiftForwardSwallowtailCancelledCore
#print axioms actualLiftForwardExpanded_iff_cancelled
#print axioms actualLiftForwardPredicate_iff_cancelled

end

end KUOS.DependentOriginationForwardReverseContractionCancellationV5_91
