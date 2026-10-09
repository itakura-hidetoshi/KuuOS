import KUOS.DependentOriginationReverseConjugationFourCellTriangleV5_99

namespace KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailCounitFourCellV5_95
open KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96
open KUOS.DependentOriginationReverseConjugationFourCellV5_98
open KUOS.DependentOriginationReverseConjugationFourCellTriangleV5_99

set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section

/-!
# Original actual-lift reverse swallowtail from genuine conjugation (v5.100)

The generic right-hand mate equality of v5.99 must descend without
strictifying non-strict G or replacing either of the distinct original
object equivalences e_Y and e_(F G Y).

The strict F's map₂ and mapComp are native and fixed; their identity
comparators may be reduced but may not be substituted. The result
must satisfy exactly the original v5.66 predicate for the old
v5.95 counit four-cell family and v5.94 target triangulator paste.

Draft until Lean proves every equality and printed axioms show no holes.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

local instance reverseHomCategoryV5100 :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip (actualLiftReverseSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip (actualLiftReverseSwallowtailDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (G := Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))

/-- The actual v5.95 original four-cell is the genuinely chosen
two-equivalence generic counit four-cell of v5.98, with the strict
original F.mapComp comparison retained. -/
theorem actualLiftReverseFourCell_hom_eq_generic
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) Y).hom =
      (reverseConjugationFourCell
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor
            (W := W) A).obj Y))).hom := by
  -- The original target four-cell has the strict projection's native
  -- compositor as a fourth factor. Its hom is the identity, so its inv
  -- equals the identity by the old Iso inverse law, not by replacing F.
  let F := actualLiftForwardPseudofunctor
    (W := W) A WorldLabel PresentationLabel
  let G := actualLiftQuasiInversePseudofunctor
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
  let eta := actualLiftSourceRoundtripUnit (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
  let eps := actualLiftTargetRoundtripCounit (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
  let f := eta.app (G.obj Y)
  let g := G.map (eps.app Y)
  -- The original strict projection has a native composition comparison
  -- constructed from its `map_comp` equality.  Its inverse must retain
  -- the same actual-lift 1-cell endpoints as the original four-cell.
  have hCmpInv : (F.mapComp f g).inv = 𝟙 _ := by
    rfl
  -- First exhibit the actual unchanged v5.95 four-cell using the same
  -- local f,g,F,G,eps used in the strict comparator. This is the true
  -- four-cell, not a newly selected modification.
  change
    (α_ (F.map f) (eps.app (F.obj (G.obj Y))) (eps.app Y)).hom ≫
      (F.map f ◁ (eps.naturality (eps.app Y)).inv) ≫
      (α_ (F.map f) (F.map g) (eps.app Y)).inv ≫
      ((F.mapComp f g).inv ▷ eps.app Y) =
      (reverseConjugationFourCell
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftSourceObjectEquivalence (W := W) A (G.obj Y))).hom
  have hCmpWhisker :
      ((F.mapComp f g).inv ▷ eps.app Y) =
        𝟙 ((F.map f ≫ F.map g) ≫ eps.app Y) := by
    rw [hCmpInv]
    exact Bicategory.id_whiskerRight _ _
  rw [hCmpWhisker, Category.comp_id]
  -- The remaining three factors are exactly the old target counit's
  -- Conjugation.naturality cell and the two native associators. Unfold
  -- their stored original data only after cancelling strict mapComp.
  dsimp [F, G, eta, eps, f, g, actualLiftTargetRoundtripCounit,
    actualLiftSourceRoundtripUnit, actualLiftForwardPseudofunctor,
    actualLiftQuasiInversePseudofunctor]
  -- Reduce only the native actual-lift wrappers; this preserves the
  -- original component choices while exposing their fixed 1-cells.
  dsimp only [actualLiftSourceUnitComponent,
    actualLiftQuasiInverseLax, actualLiftQuasiInversePrelax,
    actualLiftQuasiInverseHomFunctor, actualLiftRepackHomFunctor]
  simp only [actualOneCellOfExactUniversalClassificationOneCell_actualLift]
  simpa only [reverseConjugationFourCell_hom]

/-- Exactly v5.96's original F4 expanded pointwise residual,
not a substitute swallowtail equation. -/
theorem actualLiftReverseExpandedResidual :
    ActualLiftReverseSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro Y
  let e := actualLiftQuasiInverseObjectEquivalence (W := W) A Y
  let d := actualLiftSourceObjectEquivalence (W := W) A
    ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)
  -- Keep all intermediate hom types explicit, rather than relying
  -- on calc to infer a fresh hom-universe when composing these equalities.
  have hFour :
      (actualLiftReverseSwallowtailComponentInterchanger
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) Y).hom =
        (reverseConjugationFourCell e d).hom :=
    actualLiftReverseFourCell_hom_eq_generic (W := W) A Y
  have hGeneric := reverseConjugationFourCell_cancelled e d
  let F := actualLiftForwardPseudofunctor
    (W := W) A WorldLabel PresentationLabel
  let G := actualLiftQuasiInversePseudofunctor
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
  have hMapIdInv : (F.mapId (G.obj Y)).inv = 𝟙 _ := by
    rfl
  -- The original F4 residual retains the native strict F.mapId. Give
  -- its typed contraction target explicitly before cancelling the
  -- comparison, rather than asking `calc` to infer a fresh hom type.
  change
    (actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) Y).hom =
      (d.counit.hom ≫
        ((F.mapId (G.obj Y)).inv ≫
          (ConjugationTriangle.quasiInverseIso e d).inv)) ▷ e.hom
  rw [hMapIdInv]
  -- The middle unit lies in the original target hom category.  State
  -- the native Category identity law at its exact 1-cell endpoint,
  -- rather than requesting a new bicategory context from the tactic.
  simpa only [Category.id_comp] using hFour.trans hGeneric

/-- Genuine original v5.95 reverse four-cell equals the unchanged
v5.94 target horizontal paste component at every target object. -/
theorem actualLiftReversePointwise :
    ActualLiftReverseSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  (actualLiftReversePointwise_iff_expanded
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)).mpr
    (actualLiftReverseExpandedResidual
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The original counit four-cells now have native modification naturality,
deduced from the already-constructed global target triangulator paste. -/
theorem actualLiftReverseNaturality :
    ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro Y Z f
  have hNatural :=
    (reverseTriangulatorPaste
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.naturality f
  have h :
      ActualLiftReverseSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
    actualLiftReversePointwise (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  rw [← h Z, ← h Y] at hNatural
  exact hNatural

/-- The original v5.66 F4 reverse swallowtail, using the original
counit-centered four-cell as the canonical global modification. -/
theorem actualLiftReverseSwallowtail :
    actualLiftReverseSwallowtailPredicate (W := W) A
      (actualLiftReverseSwallowtailInterchangerOfNaturality
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        (actualLiftReverseNaturality (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))) := by
  exact (actualLiftReversePredicate_iff_pointwise
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
    (actualLiftReverseNaturality (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))).mpr
    (actualLiftReversePointwise
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

#print axioms actualLiftReverseFourCell_hom_eq_generic
#print axioms actualLiftReverseExpandedResidual
#print axioms actualLiftReversePointwise
#print axioms actualLiftReverseNaturality
#print axioms actualLiftReverseSwallowtail

end

end KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100
