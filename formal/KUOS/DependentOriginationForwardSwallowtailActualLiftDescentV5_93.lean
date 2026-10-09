import KUOS.DependentOriginationForwardConjugationFourCellCoherenceV5_92

namespace KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationForwardCanonicalNaturalityV5_87
open KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83
open KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88
open KUOS.DependentOriginationForwardSwallowtailExplicitResidualV5_90
open KUOS.DependentOriginationForwardReverseContractionCancellationV5_91
open KUOS.DependentOriginationForwardConjugationFourCellCoherenceV5_92

set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section

/-!
# Specialize the original forward four-cell coherence to actual lifts (v5.93)

v5.92 established the genuine bicategorical four-cell/contraction law for
two *distinct* stored adjoint equivalences e : a ≌ x and d : b ≌ a.

The actual-lift hom categories of v5.41 have exactly the target 2-cells as
their hom types, and v5.42 maps those 2-cells definitionally identically.
Thus we may specialize v5.92 to e_(F X) and e_(F G F X) without imposing any
strictness on the original G, equating objectwise choices, or changing
F/G/eta/eps. All mapComp, mapId and associator comparisons remain native.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The exact v5.91 cancelled residual holds at every *original*
source object by specializing the genuine v5.92 conjugation theorem.
The two chosen equivalences remain independent. -/
theorem actualLiftForwardCancelledCore :
    ActualLiftForwardSwallowtailCancelledCore.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro X
  let e := actualLiftSourceObjectEquivalence (W := W) A X
  let d := actualLiftSourceObjectEquivalence (W := W) A
    ((actualLiftSourceRoundtrip (W := W) A).obj X)
  exact conjugationForwardFourCell_cancelled e d

/-- Discharge v5.88's original pointwise F3 proposition, using exactly the
already-proved equivalences v5.90/v5.91 and the native four-cell theorem. -/
theorem actualLiftForwardSwallowtailPointwise :
    ActualLiftForwardSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  exact
    (actualLiftForwardPointwise_iff_expanded
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mpr
      ((actualLiftForwardExpanded_iff_cancelled
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).mpr
        (actualLiftForwardCancelledCore
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))

/-- The *original* v5.65 forward swallowtail law, with the unchanged
v5.87 canonical Iso of the original v5.68 four cells. -/
theorem actualLiftForwardSwallowtail :
    actualLiftForwardSwallowtailPredicate.{u, v, uH, uW, uP, vH}
      (W := W) A
      (actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) := by
  exact
    (actualLiftForwardPredicate_iff_cancelled
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mpr
      (actualLiftForwardCancelledCore
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))

/-- The same genuine forward law for the original v5.83 global Iso,
which v5.87 identified with the canonical original-family Iso. -/
theorem actualLiftForwardGlobalSwallowtail :
    actualLiftForwardSwallowtailPredicate.{u, v, uH, uW, uP, vH}
      (W := W) A
      (actualLiftForwardSwallowtailGlobalIso.{u, v, uH, uW, uP, vH}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) := by
  exact
    (actualLiftForwardGlobalPredicate_iff_pointwise
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mpr
      (actualLiftForwardSwallowtailPointwise
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))

#print axioms actualLiftForwardCancelledCore
#print axioms actualLiftForwardSwallowtailPointwise
#print axioms actualLiftForwardSwallowtail
#print axioms actualLiftForwardGlobalSwallowtail

end

end KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93
