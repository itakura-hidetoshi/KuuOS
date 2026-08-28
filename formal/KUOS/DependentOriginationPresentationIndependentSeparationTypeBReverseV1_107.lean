import KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82
import KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
import KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106

namespace KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82
open KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79

universe u

/-!
# Presentation-independent separation and type-(B) reverse comparison v1.107

Version v1.106 produced a concrete standard-right map

```text
p_N : B²ℕ ⟶ *
```

which does not reflect thin two-simplices, while v1.91-v1.92 identified the
atomic two-simplex scaling enrichment

```text
i₂ : (Δ[2], minimal) ⟶ (Δ[2], minimal + {id₂})
```

as a canonical-generated left map and characterized its RLP exactly by
thinness reflection.

The first half of this file packages those two facts into one literal
orthogonality separator and then descends the right-class property
"every generated fibration reflects thin two-simplices" to the quotient type
`GeneratedScaledAnodynePresentation`.  The canonical quotient point satisfies
that invariant; the standard A/B/C quotient point does not.  Hence the two
quotient presentations are unequal for a reason stated entirely in terms of
their generated right classes.

The second half begins the reverse comparison.  For arbitrary scalings
`s₁ ≤ s₂` on one standard simplex, the identity-underlying enrichment

```text
(Δ[n], s₁) ⟶ (Δ[n], s₂)
```

is a right factor of the minimal-to-`s₂` enrichment through the
minimal-to-`s₁` enrichment.  The left factor is epi because its underlying
simplicial map is the identity.  Version v1.82's epi-precomposition descent and
v1.88's canonical membership of every minimal-to-chosen simplex enrichment
therefore imply canonical membership of *every* simplex scaling enrichment
`s₁ ≤ s₂`.

The literal standard type-(B) generator is exactly such an enrichment, so its
reverse comparison field is now unconditional.  Type-(A) and type-(C) remain
the genuine scaled-filtration frontier.
-/

/-! ## The explicit atomic / B²ℕ orthogonality separator -/

/-- The atomic canonical enrichment does not have the lifting property against
the concrete standard-right terminal map of `B²ℕ`. -/
theorem atomicTwoSimplexEnrichment_not_hasLiftingProperty_natDoubleDeloopingTerminal :
    ¬ HasLiftingProperty
      atomicTwoSimplexEnrichment
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  rw [atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices]
  exact natDoubleDelooping_terminal_not_reflectsThinTwoSimplices

/-- Package the presentation separator as one explicit orthogonality witness:
`i₂` lies in the canonical generated left class, `p_N` lies in the standard
generated right class, and the pair is not orthogonal. -/
structure AtomicNatOrthogonalitySeparator : Prop where
  canonicalLeft :
    (canonicalGeneratedScaledAnodyne : MorphismProperty ScaledSSet)
      atomicTwoSimplexEnrichment
  standardRight :
    (standardGeneratedScaledAnodyneABC : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)
  notOrthogonal :
    ¬ HasLiftingProperty
      atomicTwoSimplexEnrichment
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)

/-- The concrete separator exists unconditionally after v1.106. -/
def atomicNatOrthogonalitySeparator : AtomicNatOrthogonalitySeparator where
  canonicalLeft := atomicTwoSimplexEnrichment_mem_canonicalGenerated
  standardRight := natDoubleDelooping_standardGeneratedABC_rlp
  notOrthogonal :=
    atomicTwoSimplexEnrichment_not_hasLiftingProperty_natDoubleDeloopingTerminal

/-- The same one pair directly proves that the canonical generated left class
is not contained in the standard generated left class. -/
theorem canonicalGenerated_not_le_standardGenerated :
    ¬ (canonicalGeneratedScaledAnodyne : MorphismProperty ScaledSSet) ≤
      standardGeneratedScaledAnodyneABC := by
  intro hle
  have hstdLeft :
      standardGeneratedScaledAnodyneABC atomicTwoSimplexEnrichment :=
    hle _ atomicNatOrthogonalitySeparator.canonicalLeft
  exact atomicNatOrthogonalitySeparator.notOrthogonal
    (hstdLeft _ atomicNatOrthogonalitySeparator.standardRight)

/-! ## Quotient-level thin-reflection invariant -/

/-- Presentation-independent predicate saying that every map in the generated
right orthogonal class reflects thin two-simplices.  It is defined directly on
the quotient presentation, so no chosen generator representative remains. -/
def EveryGeneratedRightReflectsThinTwoSimplices
    (P : GeneratedScaledAnodynePresentation.{u}) : Prop :=
  generatedFibrationClass P ≤
    (thinReflectingTwoSimplexMaps : MorphismProperty (ScaledSSet.{u}))

/-- The canonical quotient point satisfies the thin-reflection invariant. -/
theorem canonicalKuuOSPresentation_everyGeneratedRightReflectsThinTwoSimplices :
    EveryGeneratedRightReflectsThinTwoSimplices
      (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) := by
  change
    (externalGeneratedScaledFibration
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u}))) ≤
      (thinReflectingTwoSimplexMaps : MorphismProperty (ScaledSSet.{u}))
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp ≤
      (thinReflectingTwoSimplexMaps : MorphismProperty (ScaledSSet.{u}))
  intro X Y p hp
  exact canonicalAttachmentRight_reflectsThinTwoSimplices hp

/-- The standard A/B/C quotient point fails the same invariant, witnessed by
the terminal map of `B²ℕ`. -/
theorem standardABCPresentation_not_everyGeneratedRightReflectsThinTwoSimplices :
    ¬ EveryGeneratedRightReflectsThinTwoSimplices
      (standardABCPresentation : GeneratedScaledAnodynePresentation) := by
  intro hall
  have hreflect :
      ReflectsThinTwoSimplices
        (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
    apply hall
    change
      (standardScaledAnodyneGeneratorsABC : MorphismProperty ScaledSSet).rlp
        (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)
    exact natDoubleDelooping_standardABC_generators_rlp
  exact natDoubleDelooping_terminal_not_reflectsThinTwoSimplices hreflect

/-- Therefore the standard and canonical generated presentations are distinct
as points of the quotient by mutual orthogonal generation. -/
theorem standardABCPresentation_ne_canonicalKuuOSPresentation :
    (standardABCPresentation : GeneratedScaledAnodynePresentation) ≠
      canonicalKuuOSPresentation := by
  intro hEq
  apply standardABCPresentation_not_everyGeneratedRightReflectsThinTwoSimplices
  rw [hEq]
  exact canonicalKuuOSPresentation_everyGeneratedRightReflectsThinTwoSimplices

/-! ## Generic canonical membership of simplex scaling enrichments -/

/-- The minimal-to-chosen simplex enrichment is epi because its underlying
simplicial map is the identity. -/
instance minimalToChosenSimplexScaling_epi
    {n : Nat}
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    Epi (minimalToChosenSimplexScaling sDelta) where
  left_cancellation := by
    intro Z f g h
    apply ScaledSSet.ScaledMap.ext
    have hmap := congrArg ScaledSSet.ScaledMap.map h
    simpa [minimalToChosenSimplexScaling] using hmap

/-- Minimal-to-`s₁` followed by the identity enrichment `s₁ ≤ s₂` is exactly
minimal-to-`s₂`. -/
theorem minimalToChosen_comp_scalingEnrichmentHom
    {n : Nat}
    {s₁ s₂ : ScaledSimplicialSet (Delta[n] : SSet.{u})}
    (h₁₂ : ScalingLE s₁ s₂) :
    minimalToChosenSimplexScaling s₁ ≫ scalingEnrichmentHom h₁₂ =
      minimalToChosenSimplexScaling s₂ := by
  apply ScaledSSet.ScaledMap.ext
  simp [minimalToChosenSimplexScaling, scalingEnrichmentHom]

/-- Every identity-underlying enlargement between two scalings on the same
standard simplex belongs to the canonical generated left class. -/
theorem simplexScalingEnrichment_mem_canonicalGenerated
    {n : Nat}
    {s₁ s₂ : ScaledSimplicialSet (Delta[n] : SSet.{u})}
    (h₁₂ : ScalingLE s₁ s₂) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (scalingEnrichmentHom h₁₂) := by
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp.llp
      (scalingEnrichmentHom h₁₂)
  apply llp_mem_of_epi_precomp
    ((scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp)
    (minimalToChosenSimplexScaling s₁)
    (scalingEnrichmentHom h₁₂)
  rw [minimalToChosen_comp_scalingEnrichmentHom]
  exact minimalToChosenSimplexScaling_mem_canonicalGenerated s₂

/-! ## Close the standard type-(B) reverse field -/

/-- The literal standard type-(B) scaling-only generator is canonical-generated
unconditionally. -/
theorem standardTypeBGenerator_mem_canonicalGenerated :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      standardTypeBGeneratorHom := by
  simpa [standardTypeBGeneratorHom] using
    (simplexScalingEnrichment_mem_canonicalGenerated
      (u := u) standardTypeBSourceScaling_le_target)

/-- Hence the complete singleton type-(B) generator family lies in the
canonical generated left class. -/
theorem standardTypeBScaledAnodyneGenerators_le_canonicalGenerated :
    (standardTypeBScaledAnodyneGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) := by
  intro X Y f hf
  dsimp [standardTypeBScaledAnodyneGenerators] at hf
  cases hf with
  | mk unitIndex =>
      cases unitIndex
      exact standardTypeBGenerator_mem_canonicalGenerated

/-- After type-(B) is discharged, constructing the full generatorwise reverse
certificate requires only the genuinely geometric type-(A) and type-(C)
fields. -/
def standardABCCanonicalGeneratorwiseReverseComparison_of_typeAC
    (hA :
      ∀ g : StandardTypeAHornGeneratorIndex,
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
          (standardTypeAScaledHornGeneratorHom g))
    (hC :
      ∀ m : Nat,
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
          (standardTypeCGeneratorHom m)) :
    StandardABCCanonicalGeneratorwiseReverseComparison.{u} where
  typeA_mem := hA
  typeB_mem := standardTypeBGenerator_mem_canonicalGenerated
  typeC_mem := hC

/-!
The comparison frontier is now sharper:

```text
presentation-independent separator:
  i₂ ∈ L_canonical
  p_N ∈ R_standard
  ¬ HasLiftingProperty i₂ p_N

therefore
  L_canonical ≰ L_standard
  [standard] ≠ [canonical]
  by a quotient-level generated-right invariant.

reverse comparison:
  every simplex scaling enrichment s₁ -> s₂ is canonical-generated
  => standard type-B is canonical-generated unconditionally.

remaining reverse geometry:
  type-A scaled horns
  type-C collapsed outer horns.
```

No forward equality target is restored: v1.106-v1.107 prove that the quotient
presentations are genuinely separated.  The remaining question is whether the
standard generated left class embeds strictly into the stronger canonical
class.
-/

end KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107
