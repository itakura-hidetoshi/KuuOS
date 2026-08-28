import KUOS.DependentOriginationCanonicalSourceScalingErasureOneThinHornFrontierV1_108

namespace KUOS.DependentOriginationCanonicalMinimalHornReverseCoreV1_109

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
open KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107
open KUOS.DependentOriginationCanonicalSourceScalingErasureOneThinHornFrontierV1_108

universe u

/-!
# Canonical minimal-horn reverse core v1.109

Version v1.108 removed every source-scaling issue from the remaining reverse
comparison and reduced standard type-(A)/(C) to minimally scaled horn sources
with one distinguished target-thin triangle.  The target enrichment is not part
of the irreducible geometry either.

For every horn inclusion we introduce the completely minimally scaled map

```text
(Λ[n,i], minimal) --> (Δ[n], minimal).
```

The type-(A) one-thin target is obtained from this map by postcomposing the
identity-underlying enrichment from the minimal simplex to the standard
consecutive-triangle scaling.  The type-(C) uncollapsed `01n` target is obtained
in exactly the same way.  Version v1.108 proves that every such scaling
enrichment on an arbitrary carrier is already canonical-generated.  Since the
canonical generated left class is composition-stable, canonical generation of
the minimal horn therefore implies canonical generation of the corresponding
one-thin horn.

Thus the complete reverse problem has a common sufficient core with no scaling
bookkeeping at all:

```text
minimal inner horns required by type A
minimal outer 0-horns required by type C
```

Type B is already unconditional.  We package precisely those two minimal-horn
families, derive the full generatorwise reverse certificate, and combine it
with the unconditional v1.106-v1.107 separation to obtain strict-order
certificates on generated left classes and quotient presentations.

No minimal horn is asserted canonical-generated here.  The point is to expose
the exact ordinary simplicial geometry which a subsequent prism/cellular
argument must establish, without carrying source or target scaling noise.
-/

/-! ## Completely minimally scaled horn inclusions -/

/-- A standard horn equipped with the minimal scaling. -/
def minimallyScaledHorn
    (n : Nat)
    (i : Fin (n + 1)) : ScaledSSet.{u} :=
  ScaledSSet.of (Λ[n, i] : SSet.{u})
    (minimalScaling (Λ[n, i] : SSet.{u}))

/-- The ordinary horn inclusion with minimal scaling on both source and target. -/
def minimalHornInclusionHom
    {n : Nat}
    (i : Fin (n + 1)) :
    minimallyScaledHorn n i ⟶ minimallyScaledSimplex n where
  map := Λ[n, i].ι
  scaled := minimalScaling_map _ _

/-! ## Type-(A): the one-thin target is only a post-enrichment -/

/-- Minimal simplex scaling is contained in the standard type-(A) scaling. -/
def standardTypeAMinimalTargetLE
    (g : StandardTypeAHornGeneratorIndex) :
    ScalingLE
      (minimalScaling (Δ[g.n] : SSet.{u}))
      (standardTypeASimplexScaling g.i) := by
  intro t ht
  exact minimalScaling_le_standardTypeASimplexScaling g.i t ht

/-- Enrich the minimally scaled simplex to the standard type-(A) target. -/
def minimalToStandardTypeATarget
    (g : StandardTypeAHornGeneratorIndex) :
    minimallyScaledSimplex g.n ⟶ standardTypeAScaledSimplex g :=
  scalingEnrichmentHom (standardTypeAMinimalTargetLE g)

/-- The minimal-source standard type-(A) horn is exactly the completely minimal
horn followed by target scaling enrichment. -/
theorem minimalHorn_comp_typeATargetEnrichment
    (g : StandardTypeAHornGeneratorIndex) :
    minimalHornInclusionHom g.i ≫ minimalToStandardTypeATarget g =
      standardTypeAMinimalSourceHornHom g := by
  apply ScaledSSet.ScaledMap.ext
  simp [minimalHornInclusionHom, minimalToStandardTypeATarget,
    scalingEnrichmentHom, standardTypeAMinimalSourceHornHom]

/-- Canonical generation of the completely minimal inner horn implies the
standard type-(A) one-thin minimal-source horn. -/
theorem standardTypeAMinimalSource_mem_of_minimalHorn
    (g : StandardTypeAHornGeneratorIndex)
    (hmin :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom g.i)) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAMinimalSourceHornHom g) := by
  rw [← minimalHorn_comp_typeATargetEnrichment g]
  exact MorphismProperty.comp_mem
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
    _ _ hmin
    (arbitraryCarrierScalingEnrichment_mem_canonicalGenerated
      (standardTypeAMinimalTargetLE g))

/-- Hence the literal standard type-(A) generator is canonical-generated as
soon as its completely minimal horn is. -/
theorem standardTypeA_mem_canonicalGenerated_of_minimalHorn
    (g : StandardTypeAHornGeneratorIndex)
    (hmin :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom g.i)) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAScaledHornGeneratorHom g) := by
  apply (standardTypeA_mem_canonicalGenerated_iff_minimalSource g).2
  exact standardTypeAMinimalSource_mem_of_minimalHorn g hmin

/-! ## Type-(C): the `01n` target is likewise only a post-enrichment -/

/-- Minimal scaling is contained in the uncollapsed type-(C) one-thin scaling. -/
def standardTypeCMinimalTargetLE
    (m : Nat) :
    ScalingLE
      (minimalScaling (Δ[m + 3] : SSet.{u}))
      (standardTypeCUncollapsedTargetScaling m) := by
  intro t ht
  exact Or.inl ht

/-- Enrich the minimally scaled simplex by declaring only `01n` additionally
thin. -/
def minimalToStandardTypeCUncollapsedTarget
    (m : Nat) :
    minimallyScaledSimplex (m + 3) ⟶
      ScaledSSet.of (Δ[m + 3] : SSet.{u})
        (standardTypeCUncollapsedTargetScaling m) :=
  scalingEnrichmentHom (standardTypeCMinimalTargetLE m)

/-- The uncollapsed type-(C) one-thin outer horn is the completely minimal
outer horn followed by its target enrichment. -/
theorem minimalOuterHorn_comp_typeCTargetEnrichment
    (m : Nat) :
    minimalHornInclusionHom (0 : Fin (m + 4)) ≫
        minimalToStandardTypeCUncollapsedTarget m =
      standardTypeCOuterOneThinHornHom m := by
  apply ScaledSSet.ScaledMap.ext
  simp [minimalHornInclusionHom, minimalToStandardTypeCUncollapsedTarget,
    scalingEnrichmentHom, standardTypeCOuterOneThinHornHom]

/-- Canonical generation of the completely minimal outer horn implies
canonical generation of the uncollapsed type-(C) one-thin horn. -/
theorem standardTypeCOuterOneThin_mem_of_minimalHorn
    (m : Nat)
    (hmin :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom (0 : Fin (m + 4)))) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeCOuterOneThinHornHom m) := by
  rw [← minimalOuterHorn_comp_typeCTargetEnrichment m]
  exact MorphismProperty.comp_mem
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
    _ _ hmin
    (arbitraryCarrierScalingEnrichment_mem_canonicalGenerated
      (standardTypeCMinimalTargetLE m))

/-- Therefore the actual collapsed-edge type-(C) generator is canonical-
generated whenever the corresponding completely minimal outer horn is. -/
theorem standardTypeC_mem_canonicalGenerated_of_minimalHorn
    (m : Nat)
    (hmin :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom (0 : Fin (m + 4)))) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeCGeneratorHom m) := by
  exact standardTypeC_mem_canonicalGenerated_of_outerOneThin m
    (standardTypeCOuterOneThin_mem_of_minimalHorn m hmin)

/-! ## The exact minimal-horn sufficient core -/

/-- The remaining minimal-horn data sufficient for the full standard A/B/C
reverse comparison.  Only the inner horns occurring in type A and the outer
zero-horns occurring in type C are requested. -/
structure StandardABCCanonicalMinimalHornReverseCore : Prop where
  typeA :
    ∀ g : StandardTypeAHornGeneratorIndex,
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom g.i)
  typeC :
    ∀ m : Nat,
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom (0 : Fin (m + 4)))

namespace StandardABCCanonicalMinimalHornReverseCore

/-- Minimal-horn core data produces the v1.108 common one-thin-horn data and
therefore the complete generatorwise reverse certificate. -/
def toGeneratorwiseReverse
    (K : StandardABCCanonicalMinimalHornReverseCore.{u}) :
    StandardABCCanonicalGeneratorwiseReverseComparison.{u} :=
  standardABCCanonicalGeneratorwiseReverseComparison_of_oneThinHorns
    (fun g => standardTypeAMinimalSource_mem_of_minimalHorn g (K.typeA g))
    (fun m => standardTypeCOuterOneThin_mem_of_minimalHorn m (K.typeC m))

/-- Hence every standard-generated left map is canonical-generated. -/
theorem standardGenerated_le_canonicalGenerated
    (K : StandardABCCanonicalMinimalHornReverseCore.{u}) :
    standardGeneratedScaledAnodyneABC ≤
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) :=
  K.toGeneratorwiseReverse.standardGenerated_le_canonicalGenerated

/-- Quotient-level reverse inclusion follows from exactly the same core. -/
theorem standardPresentation_le_canonicalPresentation
    (K : StandardABCCanonicalMinimalHornReverseCore.{u}) :
    standardABCPresentation ≤ canonicalKuuOSPresentation :=
  (standardABC_le_canonicalKuuOS_iff_generatorwiseReverse).2
    K.toGeneratorwiseReverse

/-- Combined with the unconditional B²ℕ separator, the minimal-horn core would
make the generated-left inclusion genuinely strict.  This form avoids any
ambiguity about `<`: it states both the inclusion and failure of its converse. -/
theorem generatedLeft_strictOrderCertificate
    (K : StandardABCCanonicalMinimalHornReverseCore.{u}) :
    standardGeneratedScaledAnodyneABC ≤
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ∧
      ¬ (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC :=
  ⟨K.standardGenerated_le_canonicalGenerated,
    canonicalGenerated_not_le_standardGenerated⟩

/-- The same conclusion at the presentation quotient level: if the minimal
horn core is closed, standard lies strictly below canonical because the reverse
order direction is already unconditionally impossible. -/
theorem presentation_strictOrderCertificate
    (K : StandardABCCanonicalMinimalHornReverseCore.{u}) :
    standardABCPresentation ≤ canonicalKuuOSPresentation ∧
      ¬ canonicalKuuOSPresentation ≤ standardABCPresentation :=
  ⟨K.standardPresentation_le_canonicalPresentation,
    natDoubleDelooping_not_canonicalKuuOS_le_standardABC⟩

end StandardABCCanonicalMinimalHornReverseCore

/-! ## A stronger uniform formulation -/

/-- Uniform hypothesis that every minimally scaled horn inclusion belongs to
the canonical generated left class.  This is stronger than needed for A/C,
but is a convenient target for a common prism/cellular theorem. -/
def AllMinimalHornInclusionsCanonical : Prop :=
  ∀ (n : Nat) (i : Fin (n + 1)),
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (minimalHornInclusionHom i)

/-- The uniform minimal-horn theorem immediately supplies the exact A/C core. -/
def minimalHornReverseCore_of_all
    (H : AllMinimalHornInclusionsCanonical.{u}) :
    StandardABCCanonicalMinimalHornReverseCore.{u} where
  typeA := fun g => H g.n g.i
  typeC := fun m => H (m + 3) (0 : Fin (m + 4))

/-- Consequently a uniform minimal-horn theorem would finish the whole reverse
standard-to-canonical generated-left inclusion. -/
theorem standardGenerated_le_canonicalGenerated_of_allMinimalHorns
    (H : AllMinimalHornInclusionsCanonical.{u}) :
    standardGeneratedScaledAnodyneABC ≤
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) :=
  (minimalHornReverseCore_of_all H).standardGenerated_le_canonicalGenerated

/-- And, because the opposite inclusion is already refuted, the same theorem
would establish the desired strict presentation order. -/
theorem presentation_strictOrderCertificate_of_allMinimalHorns
    (H : AllMinimalHornInclusionsCanonical.{u}) :
    standardABCPresentation ≤ canonicalKuuOSPresentation ∧
      ¬ canonicalKuuOSPresentation ≤ standardABCPresentation :=
  (minimalHornReverseCore_of_all H).presentation_strictOrderCertificate

/-!
The reverse frontier is now free of scaled decoration:

```text
minimal horn Λ[n,i] -> Δ[n]
       |
       | postcompose canonical target-scaling enrichment
       v
one-thin A/C horn of v1.108
       |
       | type-C edge-collapse descent when needed
       v
literal standard A/C generator
       |
       + type-B already closed in v1.107
       v
standardGenerated <= canonicalGenerated.
```

Together with v1.106-v1.107:

```text
canonicalGenerated ≰ standardGenerated
canonicalPresentation ≰ standardPresentation.
```

Therefore closing the indicated minimal inner/outer horn core is sufficient for

```text
standardGenerated < canonicalGenerated
[standard] < [canonical]
```

in the precise order-theoretic sense of inclusion plus failure of the converse.
The next mathematical unit can work entirely on ordinary/minimally scaled horn
geometry, using the existing Mathlib prism pairing and relative-cell machinery;
no further source-scaling or distinguished-triangle algebra is needed.
-/

end KUOS.DependentOriginationCanonicalMinimalHornReverseCoreV1_109
