import KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78

namespace KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78

universe u

/-!
# Positive canonical residual split v1.79

Version v1.78 separated the full presentation comparison into the two exact
closure inclusions

```text
canonicalGenerated <= standardGenerated
standardGenerated <= canonicalGenerated.
```

The first direction still inherited one deliberately negative field from
v1.59:

```text
induced canonical f
+ not standard-type-A f
=> standard-generated f.
```

That statement was correct, but it is not the right geometry for the next
proof.  A canonical index contains the actual dimension, horn index, endpoint,
and arbitrary simplex scaling, so the complement of the completed standard-A
case has a canonical positive partition:

1. the horn is inner and the simplex scaling is not the standard type-A
   scaling;
2. the horn fails the left inner inequality;
3. the left inequality holds but the right inner inequality fails.

The remaining v1.48 source-scaling enrichment is kept as its own fourth
obligation.  This file packages exactly those four index-level obligations and
proves that they imply the old v1.59 residual structure.

For the reverse comparison we likewise replace the opaque union-level field

```text
standard A/B/C <= canonicalGenerated
```

by the three literal generator obligations: every concrete type-A horn, the
single type-B scaling enrichment, and every concrete type-C collapsed-edge
map.

Thus after v1.79 every still-open comparison hypothesis is attached to a
positive geometric generator/index rather than to a complement of a morphism
property.  No new comparison obligation is asserted true here.
-/

/-! ## Recovering the completed standard-A branch from a canonical index -/

/-- An inner canonical index carrying exactly the standard type-A simplex
scaling is literally the canonical image of the corresponding standard type-A
attachment index. -/
theorem canonicalIndex_eq_standardTypeA_toCanonical
    (g : ScaledHornAttachmentGeneratorIndex.{u})
    (h0 : 0 < g.i)
    (hn : g.i < Fin.last g.n)
    (hs : g.simplexScaling = standardTypeASimplexScaling g.i) :
    g =
      ({ n := g.n
         i := g.i
         inner_left := h0
         inner_right := hn
         endpoint := g.endpoint } :
        StandardTypeAHornAttachmentGeneratorIndex).toCanonical := by
  cases g with
  | mk n i endpoint simplexScaling =>
      dsimp at h0 hn hs ⊢
      subst simplexScaling
      rfl

/-- Consequently an inner canonical induced attachment with the exact standard
A scaling belongs to the already-completed standard type-A induced subfamily.
This is the branch discharged by v1.77. -/
theorem inducedCanonical_mem_standardTypeA_of_inner_standardScaling
    (g : ScaledHornAttachmentGeneratorIndex.{u})
    (h0 : 0 < g.i)
    (hn : g.i < Fin.last g.n)
    (hs : g.simplexScaling = standardTypeASimplexScaling g.i) :
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u}))
      (inducedScaledHornAttachmentGeneratorHom g) := by
  let a : StandardTypeAHornAttachmentGeneratorIndex :=
    { n := g.n
      i := g.i
      inner_left := h0
      inner_right := hn
      endpoint := g.endpoint }
  have hg : g = a.toCanonical := by
    simpa [a] using
      canonicalIndex_eq_standardTypeA_toCanonical g h0 hn hs
  rw [hg]
  simpa [standardTypeAInducedScaledHornAttachmentGeneratorHom,
    StandardTypeAHornAttachmentGeneratorIndex.toCanonical] using
    standardTypeAInducedScaledHornAttachmentGenerator_mem a

/-! ## Positive forward residual data -/

/-- Positive, index-level replacement for the v1.59 forward residual.

The four fields are disjoint by construction except for the harmless choice of
placing a doubly-outer horn in the left-failure branch first. -/
structure StandardABCCanonicalPositiveResidualComparison : Prop where
  scalingEnrichment_mem :
    ∀ g : ScaledHornAttachmentGeneratorIndex.{u},
      standardGeneratedScaledAnodyneABC
        (scaledHornAttachmentScalingEnrichment g)
  innerNonstandardInduced_mem :
    ∀ (g : ScaledHornAttachmentGeneratorIndex.{u}),
      0 < g.i →
      g.i < Fin.last g.n →
      g.simplexScaling ≠ standardTypeASimplexScaling g.i →
      standardGeneratedScaledAnodyneABC
        (inducedScaledHornAttachmentGeneratorHom g)
  leftOuterInduced_mem :
    ∀ (g : ScaledHornAttachmentGeneratorIndex.{u}),
      ¬ 0 < g.i →
      standardGeneratedScaledAnodyneABC
        (inducedScaledHornAttachmentGeneratorHom g)
  rightOuterInduced_mem :
    ∀ (g : ScaledHornAttachmentGeneratorIndex.{u}),
      0 < g.i →
      ¬ g.i < Fin.last g.n →
      standardGeneratedScaledAnodyneABC
        (inducedScaledHornAttachmentGeneratorHom g)

namespace StandardABCCanonicalPositiveResidualComparison

/-- The positive index partition implies exactly the older morphism-property
residual structure.  The only classical split is equality of the arbitrary
simplex scaling with the standard type-A scaling. -/
def toResidual
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    StandardABCCanonicalResidualComparison.{u} where
  scalingEnrichments_le_standardGenerated := by
    intro A B f hf
    dsimp [scaledHornAttachmentScalingEnrichments] at hf
    cases hf with
    | mk g =>
        exact K.scalingEnrichment_mem g
  nonTypeAInduced_mem := by
    intro A B f hf hnotA
    dsimp [inducedScaledHornAttachmentGenerators] at hf
    cases hf with
    | mk g =>
        classical
        by_cases h0 : 0 < g.i
        · by_cases hn : g.i < Fin.last g.n
          · by_cases hs :
              g.simplexScaling = standardTypeASimplexScaling g.i
            · exfalso
              exact hnotA
                (inducedCanonical_mem_standardTypeA_of_inner_standardScaling
                  g h0 hn hs)
            · exact K.innerNonstandardInduced_mem g h0 hn hs
          · exact K.rightOuterInduced_mem g h0 hn
        · exact K.leftOuterInduced_mem g h0

/-- Therefore the four positive forward obligations already imply the full
canonical-to-standard generated-left inclusion isolated in v1.78. -/
theorem canonicalGenerated_le_standardGenerated
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC :=
  canonicalGenerated_le_standardGenerated_of_residual K.toResidual

/-- Dually, every standard A/B/C fibration is canonical whenever the four
positive forward obligations hold. -/
theorem standardFibration_le_canonicalFibration
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    standardGeneratedScaledFibrationABC ≤
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u})) :=
  standardGeneratedFibration_le_canonicalGeneratedFibration_of_residual
    K.toResidual

end StandardABCCanonicalPositiveResidualComparison

/-! ## Positive reverse data: the three literal standard generator families -/

/-- Generator-by-generator form of the reverse comparison.  This keeps type-A,
type-B, and type-C geometry separate all the way to the final union. -/
structure StandardABCCanonicalGeneratorwiseReverseComparison : Prop where
  typeA_mem :
    ∀ g : StandardTypeAHornGeneratorIndex,
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeAScaledHornGeneratorHom g)
  typeB_mem :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      standardTypeBGeneratorHom
  typeC_mem :
    ∀ m : Nat,
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeCGeneratorHom m)

namespace StandardABCCanonicalGeneratorwiseReverseComparison

/-- The three concrete standard generator obligations assemble into the v1.59
reverse union-level comparison. -/
def toReverse
    (K : StandardABCCanonicalGeneratorwiseReverseComparison.{u}) :
    StandardABCCanonicalReverseComparison.{u} where
  standardGenerators_le_canonicalGenerated := by
    intro X Y f hf
    change
      ((standardTypeAScaledHornGenerators :
          MorphismProperty (ScaledSSet.{u})) ⊔
        standardTypeBScaledAnodyneGenerators ⊔
        standardTypeCScaledAnodyneGenerators) f at hf
    rcases hf with hfAB | hfC
    · rcases hfAB with hfA | hfB
      · dsimp [standardTypeAScaledHornGenerators] at hfA
        cases hfA with
        | mk g =>
            exact K.typeA_mem g
      · dsimp [standardTypeBScaledAnodyneGenerators] at hfB
        cases hfB with
        | mk unitIndex =>
            cases unitIndex
            exact K.typeB_mem
    · dsimp [standardTypeCScaledAnodyneGenerators] at hfC
      cases hfC with
      | mk m =>
          exact K.typeC_mem m

/-- Hence the generatorwise reverse obligations imply the entire
standard-generated to canonical-generated inclusion. -/
theorem standardGenerated_le_canonicalGenerated
    (K : StandardABCCanonicalGeneratorwiseReverseComparison.{u}) :
    standardGeneratedScaledAnodyneABC ≤
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) :=
  standardGenerated_le_canonicalGenerated_of_reverse K.toReverse

/-- And the corresponding canonical-right to standard-right inclusion. -/
theorem canonicalFibration_le_standardFibration
    (K : StandardABCCanonicalGeneratorwiseReverseComparison.{u}) :
    (canonicalGeneratedScaledFibration :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledFibrationABC :=
  canonicalGeneratedFibration_le_standardGeneratedFibration_of_reverse
    K.toReverse

end StandardABCCanonicalGeneratorwiseReverseComparison

/-! ## Full equality from positive geometric data only -/

/-- Post-v1.77 master comparison stated entirely using positive geometric
obligations. -/
structure StandardABCCanonicalPositiveComparisonCertificate : Prop where
  forward : StandardABCCanonicalPositiveResidualComparison.{u}
  reverse : StandardABCCanonicalGeneratorwiseReverseComparison.{u}

namespace StandardABCCanonicalPositiveComparisonCertificate

/-- Recover the older v1.59 master certificate when a consumer needs that API. -/
def toComparisonCertificate
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    StandardABCCanonicalComparisonCertificate.{u} :=
  standardABCCanonicalComparisonCertificateConstructed
    K.forward.toResidual K.reverse.toReverse

/-- Positive forward and reverse geometry gives equality of the generated left
classes. -/
theorem generatedAnodyne_eq
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    standardGeneratedScaledAnodyneABC =
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) :=
  standardGeneratedScaledAnodyneABC_eq_canonical_of_residual_reverse
    K.forward.toResidual K.reverse.toReverse

/-- The same positive data gives equality of the generated right classes. -/
theorem generatedFibration_eq
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    standardGeneratedScaledFibrationABC =
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u})) :=
  standardGeneratedScaledFibrationABC_eq_canonical_of_residual_reverse
    K.forward.toResidual K.reverse.toReverse

end StandardABCCanonicalPositiveComparisonCertificate

/-!
The comparison frontier is now positive and non-overlapping:

```text
FORWARD
  every canonical minimal->induced scaling enrichment is standard-generated
  every inner / nonstandard-scaling induced attachment is standard-generated
  every left-outer induced attachment is standard-generated
  every right-outer induced attachment is standard-generated
      => canonicalGenerated <= standardGenerated

REVERSE
  every literal standard A generator is canonical-generated
  the literal standard B generator is canonical-generated
  every literal standard C generator is canonical-generated
      => standardGenerated <= canonicalGenerated

both
      => equality of left classes
      => equality of right classes.
```

The standard-A inner / standard-scaling branch is absent from the open forward
list because v1.77 already proves it.  In particular, no argument in this file
collapses arbitrary canonical simplex scalings to the standard type-A scaling.
-/

end KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
