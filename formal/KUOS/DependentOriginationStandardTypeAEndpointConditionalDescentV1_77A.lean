import KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76

namespace KUOS.DependentOriginationStandardTypeAEndpointConditionalDescentV1_77A

open CategoryTheory
open CategoryTheory.Category
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
open KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76

universe u

set_option maxHeartbeats 1500000

/-!
# v1.77A: conditional gluing from the missing raw endpoint A-cell

This file does NOT supply the missing endpoint A-cell. Its quantified premise
keeps that geometric obstruction explicit. The actual v1.76 A/B transfinite
composition is used as an independently proved second leg.

The generated A/B/C *left class* is multiplicative (v1.59).
We do not assume that the bare transfiniteCompositions class itself has an
unavailable multiplicativity instance, or silently promote raw/strong to a
full certificate.
-/

/-- Once the opposite endpoint-to-boundary inclusion is genuinely a raw
standard A/B/C cellular step for every standard type-A index, the already
certified v1.76 boundary-to-cylinder transfinite A/B proof gives the full
standard generated right lifting theorem by compositional orthogonality.
The premise remains a distinct, unproved geometric obligation. -/
theorem standardABCTypeAEndpointLeibnizLifting_of_missingRawA
    (hA : ∀ (g : KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49.StandardTypeAHornAttachmentGeneratorIndex),
      standardABCRawCellularStep.{u}
        (standardTypeAEndpointToBoundaryPrism.{u} g)) :
    StandardABCTypeAEndpointLeibnizLifting.{u} := by
  intro g X Y p hp
  have hAstrong :
      standardABCStrongCellularClosure.{u}
        (standardTypeAEndpointToBoundaryPrism.{u} g) :=
    MorphismProperty.le_transfiniteCompositions.{u}
      (standardABCRawCellularStep.{u} :
        MorphismProperty (ScaledSSet.{u})) _ (hA g)
  have hAgen :
      standardGeneratedScaledAnodyneABC.{u}
        (standardTypeAEndpointToBoundaryPrism.{u} g) :=
    standardABCCellularClosure_le_generated.{u} _
      (standardABCStrongCellularClosure_le_standardABCCellularClosure.{u} _
        hAstrong)
  have hBgen :
      standardGeneratedScaledAnodyneABC.{u}
        (standardTypeABoundaryPrismToCylinder.{u} g) :=
    standardABCCellularClosure_le_generated.{u} _
      (standardTypeABoundaryPrismToCylinder_mem_cellular.{u} g)
  have hcomp :
      standardGeneratedScaledAnodyneABC.{u}
        (standardTypeAEndpointToBoundaryPrism.{u} g ≫
          standardTypeABoundaryPrismToCylinder.{u} g) :=
    (standardGeneratedScaledAnodyneABC.{u} :
      MorphismProperty (ScaledSSet.{u})).comp_mem _ _ hAgen hBgen
  have hfull :
      standardGeneratedScaledAnodyneABC.{u}
        (standardTypeAEndpointScaledLeibnizPushoutProductHom.{u} g) := by
    simpa only [standardTypeAEndpointLeibniz_factor_boundaryPrism] using hcomp
  exact hfull p hp

/-- The exact same conditional geometric input also implies standard
type-A endpoint Leibniz stability; the converse or arbitrary-canonical-family
comparison is not asserted. -/
theorem standardABCTypeAEndpointLeibnizStability_of_missingRawA
    (hA : ∀ (g : KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49.StandardTypeAHornAttachmentGeneratorIndex),
      standardABCRawCellularStep.{u}
        (standardTypeAEndpointToBoundaryPrism.{u} g)) :
    StandardABCTypeAEndpointLeibnizStability.{u} :=
  standardABCTypeAEndpointLeibnizStability_iff_lifting.mpr
    (standardABCTypeAEndpointLeibnizLifting_of_missingRawA hA)

end KUOS.DependentOriginationStandardTypeAEndpointConditionalDescentV1_77A
