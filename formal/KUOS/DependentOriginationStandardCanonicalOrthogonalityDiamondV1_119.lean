import KUOS.DependentOriginationCanonicalTypeAThreeRelativeHornRigidityV1_118
import KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115
import KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87

namespace KUOS.DependentOriginationStandardCanonicalOrthogonalityDiamondV1_119

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
open KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107
open KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115
open KUOS.DependentOriginationCanonicalTypeAThreeRelativeHornRigidityV1_118

universe u

noncomputable section

/-!
# The standard/canonical orthogonality diamond v1.119

Version v1.118 settles the presentation-level comparison in the opposite way
from the earlier inclusion frontier: the standard A/B/C generated left class
and the canonical KuuOS generated left class are incomparable.  The two
separating mechanisms are genuinely different:

* canonical not <= standard: the atomic scaling enrichment together with the
  concrete standard-right terminal map of `B^2 N` (v1.106-v1.107);
* standard not <= canonical: the degree-three type-(A) horn `Lambda[3,1] ->
  Delta[3]`, which is itself canonical-right but cannot lift against itself
  (v1.118).

This file records the resulting global geometry once, at the generated-class,
right-class, quotient-presentation, and complete-lattice levels.  In the
presentation lattice, writing

```text
S = standardABCPresentation
C = canonicalKuuOSPresentation,
```

incomparability turns the old unoriented interval of v1.87 into a genuine
strict diamond:

```text
        S sup C
        /     \
       S       C
        \     /
        S inf C
```

All four displayed edges are strict.

This does not contradict v1.115.  Terminal maps form a special semantic slice
of the right classes, and there the order is one-sided:

```text
Fib_canonical  is strictly contained in  Fib_standardABC.
```

Thus the final comparison picture is not equality and not a global strict
order.  The full orthogonal theories are incomparable, while their fibrant
object semantics are strictly ordered.
-/

/-! ## Retire the two old comparison packages -/

/-- The generatorwise standard-to-canonical reverse package is impossible:
its degree-three type-(A) field contradicts v1.118. -/
theorem standardABCCanonicalGeneratorwiseReverseComparison_not_exists :
    ¬ StandardABCCanonicalGeneratorwiseReverseComparison.{u} := by
  intro K
  exact typeAThreeOne_not_mem_canonicalGenerated
    (K.typeA_mem typeAThreeOneIndex)

/-- The positive canonical-to-standard residual package is likewise
impossible, because it would imply the forward generated-left inclusion ruled
out in v1.107. -/
theorem standardABCCanonicalPositiveResidualComparison_not_exists :
    ¬ StandardABCCanonicalPositiveResidualComparison.{u} := by
  intro K
  exact canonicalGenerated_not_le_standardGenerated
    K.canonicalGenerated_le_standardGenerated

/-! ## Quotient presentation incomparability -/

/-- The standard quotient presentation is not below the canonical point. -/
theorem standardABCPresentation_not_le_canonicalKuuOS :
    ¬ (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
      canonicalKuuOSPresentation := by
  intro h
  exact standardABCCanonicalGeneratorwiseReverseComparison_not_exists
    ((standardABC_le_canonicalKuuOS_iff_generatorwiseReverse).1 h)

/-- The canonical quotient presentation is not below the standard point. -/
theorem canonicalKuuOSPresentation_not_le_standardABC :
    ¬ (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
      standardABCPresentation := by
  intro h
  have hgen :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC :=
    (canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated).1 h
  have hsat :
      IsOrthogonallySaturated
        (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})) := by
    change
      IsOrthogonallySaturated
        (externalGeneratedScaledAnodyne
          (standardScaledAnodyneGeneratorsABC :
            MorphismProperty (ScaledSSet.{u})))
    exact externalGeneratedScaledAnodyne_isOrthogonallySaturated _
  have hleft :
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC :=
    canonicalGeneratedScaledAnodyne_le_of_saturated hgen hsat
  exact canonicalGenerated_not_le_standardGenerated hleft

/-- The two presentation-independent quotient points are incomparable. -/
theorem standardCanonicalPresentations_incomparable :
    (¬ (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
        canonicalKuuOSPresentation) ∧
      (¬ (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
        standardABCPresentation) := by
  exact ⟨standardABCPresentation_not_le_canonicalKuuOS,
    canonicalKuuOSPresentation_not_le_standardABC⟩

/-! ## Right-class incomparability -/

/-- The v1.118 degree-three horn is a concrete canonical-right map which is not
standard-right. -/
theorem typeAThreeOne_canonicalRight_not_standardRight :
    (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u}))
        (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) ∧
      ¬ standardGeneratedScaledFibrationABC
        (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) := by
  constructor
  · exact typeAThreeOne_canonicalRight
  · intro hstd
    exact typeAThreeOne_not_hasLiftingProperty_self
      (hstd _ (standardTypeAGenerator_mem_ABC typeAThreeOneIndex))

/-- Incomparability of the generated left classes dualizes to incomparability
of the generated right classes. -/
theorem standardCanonicalGeneratedRight_incomparable :
    (¬ (canonicalGeneratedScaledFibration :
          MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledFibrationABC) ∧
      (¬ standardGeneratedScaledFibrationABC ≤
        (canonicalGeneratedScaledFibration :
          MorphismProperty (ScaledSSet.{u}))) := by
  constructor
  · intro h
    have hllp := MorphismProperty.antitone_llp h
    change
      standardGeneratedScaledAnodyneABC ≤
        (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u})) at hllp
    exact standardGenerated_not_le_canonicalGenerated hllp
  · intro h
    have hllp := MorphismProperty.antitone_llp h
    change
      (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC at hllp
    exact canonicalGenerated_not_le_standardGenerated hllp

/-! ## The old interval is a genuine strict diamond -/

/-- The lower envelope is not the standard point. -/
theorem standardCanonicalLowerEnvelope_ne_standardABC :
    standardCanonicalLowerEnvelope.{u} ≠ standardABCPresentation := by
  intro h
  apply standardABCPresentation_not_le_canonicalKuuOS
  rw [← h]
  exact lowerEnvelope_le_canonicalKuuOS

/-- The lower envelope is not the canonical point. -/
theorem standardCanonicalLowerEnvelope_ne_canonicalKuuOS :
    standardCanonicalLowerEnvelope.{u} ≠ canonicalKuuOSPresentation := by
  intro h
  apply canonicalKuuOSPresentation_not_le_standardABC
  rw [← h]
  exact lowerEnvelope_le_standardABC

/-- The standard point is not the upper envelope. -/
theorem standardABCPresentation_ne_upperEnvelope :
    (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) ≠
      standardCanonicalUpperEnvelope := by
  intro h
  apply canonicalKuuOSPresentation_not_le_standardABC
  rw [h]
  exact canonicalKuuOS_le_upperEnvelope

/-- The canonical point is not the upper envelope. -/
theorem canonicalKuuOSPresentation_ne_upperEnvelope :
    (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≠
      standardCanonicalUpperEnvelope := by
  intro h
  apply standardABCPresentation_not_le_canonicalKuuOS
  rw [h]
  exact standardABC_le_upperEnvelope

/-- Strict lower-left edge of the presentation diamond. -/
theorem lowerEnvelope_lt_standardABC :
    standardCanonicalLowerEnvelope.{u} < standardABCPresentation := by
  exact lt_of_le_of_ne lowerEnvelope_le_standardABC
    standardCanonicalLowerEnvelope_ne_standardABC

/-- Strict lower-right edge of the presentation diamond. -/
theorem lowerEnvelope_lt_canonicalKuuOS :
    standardCanonicalLowerEnvelope.{u} < canonicalKuuOSPresentation := by
  exact lt_of_le_of_ne lowerEnvelope_le_canonicalKuuOS
    standardCanonicalLowerEnvelope_ne_canonicalKuuOS

/-- Strict upper-left edge of the presentation diamond. -/
theorem standardABC_lt_upperEnvelope :
    (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) <
      standardCanonicalUpperEnvelope := by
  exact lt_of_le_of_ne standardABC_le_upperEnvelope
    standardABCPresentation_ne_upperEnvelope

/-- Strict upper-right edge of the presentation diamond. -/
theorem canonicalKuuOS_lt_upperEnvelope :
    (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) <
      standardCanonicalUpperEnvelope := by
  exact lt_of_le_of_ne canonicalKuuOS_le_upperEnvelope
    canonicalKuuOSPresentation_ne_upperEnvelope

/-- The v1.87 presentation gap cannot close. -/
theorem standardCanonicalPresentationGap_not_closed :
    ¬ StandardCanonicalPresentationGapClosed.{u} := by
  intro hgap
  have heq := standardCanonicalPresentationGapClosed_iff.1 hgap
  exact standardABCPresentation_not_le_canonicalKuuOS (le_of_eq heq)

/-- Package all four strict lattice edges. -/
theorem standardCanonicalPresentation_strictDiamond :
    standardCanonicalLowerEnvelope.{u} < standardABCPresentation ∧
      standardCanonicalLowerEnvelope.{u} < canonicalKuuOSPresentation ∧
      (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) <
        standardCanonicalUpperEnvelope ∧
      (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) <
        standardCanonicalUpperEnvelope := by
  exact ⟨lowerEnvelope_lt_standardABC,
    lowerEnvelope_lt_canonicalKuuOS,
    standardABC_lt_upperEnvelope,
    canonicalKuuOS_lt_upperEnvelope⟩

/-! ## One presentation-independent orthogonality certificate -/

/-- Complete order-theoretic geometry of the standard/canonical pair, before
specializing to terminal maps. -/
structure StandardCanonicalOrthogonalityDiamond : Prop where
  leftClassesIncomparable :
    (¬ (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})) ≤
        (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u}))) ∧
      (¬ (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC)
  rightClassesIncomparable :
    (¬ (canonicalGeneratedScaledFibration :
          MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledFibrationABC) ∧
      (¬ standardGeneratedScaledFibrationABC ≤
        (canonicalGeneratedScaledFibration :
          MorphismProperty (ScaledSSet.{u})))
  presentationsIncomparable :
    (¬ (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
        canonicalKuuOSPresentation) ∧
      (¬ (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
        standardABCPresentation)
  strictDiamond :
    standardCanonicalLowerEnvelope.{u} < standardABCPresentation ∧
      standardCanonicalLowerEnvelope.{u} < canonicalKuuOSPresentation ∧
      (standardABCPresentation : GeneratedScaledAnodynePresentation.{u}) <
        standardCanonicalUpperEnvelope ∧
      (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) <
        standardCanonicalUpperEnvelope

/-- The complete orthogonality diamond is inhabited unconditionally. -/
def standardCanonicalOrthogonalityDiamond :
    StandardCanonicalOrthogonalityDiamond.{u} where
  leftClassesIncomparable := standardCanonicalGenerated_incomparable
  rightClassesIncomparable := standardCanonicalGeneratedRight_incomparable
  presentationsIncomparable := standardCanonicalPresentations_incomparable
  strictDiamond := standardCanonicalPresentation_strictDiamond

/-! ## Terminal semantics has a different, strict one-sided order -/

/-- The final semantic profile: full generated theories are incomparable, but
canonical fibrant-object semantics is strictly contained in standard A/B/C
fibrant-object semantics. -/
theorem standardCanonical_finalSemanticProfile :
    StandardCanonicalOrthogonalityDiamond ∧
      ((∀ X : ScaledSSet,
          IsAttachmentFibrant X → IsStandardABCFibrant X) ∧
        (∃ X : ScaledSSet,
          IsStandardABCFibrant X ∧ ¬ IsAttachmentFibrant X)) := by
  exact ⟨standardCanonicalOrthogonalityDiamond,
    canonicalFibrantObjects_strictlyContainedIn_standardABCFibrantObjects⟩

/-!
The comparison geometry is therefore settled:

```text
full generated left classes:
  L_standard || L_canonical

full generated right classes:
  R_standard || R_canonical

presentation lattice:

        standard sup canonical
              /   \
      standard     canonical
              \   /
        standard inf canonical

with all four edges strict.

terminal/fibrant-object slice:
  Fib_canonical  is strictly contained in  Fib_standardABC.
```

The old v1.79 reverse and positive-forward comparison structures are now
provably uninhabited.  Type-(C) geometry may still be studied on its own, but
it can no longer restore a global standard/canonical inclusion or equality.
-/

end

end KUOS.DependentOriginationStandardCanonicalOrthogonalityDiamondV1_119
