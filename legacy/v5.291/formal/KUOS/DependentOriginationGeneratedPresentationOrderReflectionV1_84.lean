import KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83

namespace KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83

universe u

/-!
# Generated-presentation order reflection v1.84

Version v1.83 equipped the quotient of literal generator presentations with the
partial order

```text
P <= Q  iff  L_P <= L_Q,
```

where `L_P` is the orthogonally generated left class.  The stronger intrinsic
statement is that, on literal representatives, this order does not require
comparing two closures:

```text
[E] <= [F]  iff  E <= F.rlp.llp.
```

Indeed the forward implication uses only the unit

```text
E <= E.rlp.llp,
```

and the reverse implication is the universal property of the orthogonally
saturated closure of `F`.

Thus the v1.81 mutual-generation relation is exactly the symmetric part of a
canonical preorder on literal presentations, and the v1.81 quotient is its
posetal reflection in the strict order-theoretic sense.

For the two distinguished presentations this gives the exact comparison
frontier

```text
canonical <= standard
  iff every literal canonical generator is standard-generated,

standard <= canonical
  iff every literal standard A/B/C generator is canonical-generated.
```

The second direction is exactly equivalent to the v1.79 generatorwise reverse
structure.  The four positive forward residual fields of v1.79 remain a useful
sufficient geometric decomposition, but they are no longer the intrinsic shape
of the order obligation: one may instead prove the canonical composite
generators standard-generated directly.
-/

/-! ## The literal-presentation preorder -/

/-- One literal presentation generates no more than another when every
literal generator of the first already belongs to the generated left class of
the second. -/
abbrev GeneratedPresentationPreorderLE
    (E F : MorphismProperty (ScaledSSet.{u})) : Prop :=
  E <= externalGeneratedScaledAnodyne F

/-- The literal generation relation is reflexive by the unit of orthogonal
closure. -/
theorem generatedPresentationPreorderLE_refl
    (E : MorphismProperty (ScaledSSet.{u})) :
    GeneratedPresentationPreorderLE E E := by
  simpa [GeneratedPresentationPreorderLE, externalGeneratedScaledAnodyne] using
    (MorphismProperty.le_llp_rlp E)

/-- The literal generation relation is transitive.  The only nontrivial step is
extending `F <= L_G` to `L_F <= L_G` by orthogonal saturation of `L_G`. -/
theorem generatedPresentationPreorderLE_trans
    {E F G : MorphismProperty (ScaledSSet.{u})}
    (hEF : GeneratedPresentationPreorderLE E F)
    (hFG : GeneratedPresentationPreorderLE F G) :
    GeneratedPresentationPreorderLE E G := by
  have hclosure :
      externalGeneratedScaledAnodyne F <=
        externalGeneratedScaledAnodyne G :=
    externalGeneratedScaledAnodyne_le_of_le_saturated
      hFG
      (externalGeneratedScaledAnodyne_isOrthogonallySaturated G)
  exact hEF.trans hclosure

/-! ## Exact order reflection -/

/-- The quotient order is exactly one-sided orthogonal generation on literal
representatives.  This is the order-theoretic universal property hidden behind
the mutual-generation quotient of v1.81. -/
theorem presentationClass_le_iff_generators_le_generated
    (E F : MorphismProperty (ScaledSSet.{u})) :
    presentationClass E <= presentationClass F <->
      E <= externalGeneratedScaledAnodyne F := by
  constructor
  · intro h
    change
      externalGeneratedScaledAnodyne E <=
        externalGeneratedScaledAnodyne F at h
    exact (generatedPresentationPreorderLE_refl E).trans h
  · intro h
    change
      externalGeneratedScaledAnodyne E <=
        externalGeneratedScaledAnodyne F
    exact externalGeneratedScaledAnodyne_le_of_le_saturated
      h
      (externalGeneratedScaledAnodyne_isOrthogonallySaturated F)

/-- Equality of quotient presentations is therefore exactly mutual comparison
in the literal-presentation preorder. -/
theorem presentationClass_eq_iff_mutual_preorder
    (E F : MorphismProperty (ScaledSSet.{u})) :
    presentationClass E = presentationClass F <->
      GeneratedPresentationPreorderLE E F /\
        GeneratedPresentationPreorderLE F E := by
  constructor
  · intro h
    subst F
    exact
      <| And.intro
        (generatedPresentationPreorderLE_refl E)
        (generatedPresentationPreorderLE_refl E)
  · rintro ⟨hEF, hFE⟩
    apply le_antisymm
    · exact
        (presentationClass_le_iff_generators_le_generated E F).2 hEF
    · exact
        (presentationClass_le_iff_generators_le_generated F E).2 hFE

/-- The v1.80 generated-presentation equivalence structure is precisely the
symmetric part of the literal-presentation preorder. -/
theorem generatedPresentationEquivalence_iff_mutual_preorder
    (E F : MorphismProperty (ScaledSSet.{u})) :
    GeneratedScaledAnodynePresentationEquivalence E F <->
      GeneratedPresentationPreorderLE E F /\
        GeneratedPresentationPreorderLE F E := by
  constructor
  · intro K
    exact
      ⟨K.left_generators_le_right_generated,
        K.right_generators_le_left_generated⟩
  · rintro ⟨hEF, hFE⟩
    exact
      { left_generators_le_right_generated := hEF
        right_generators_le_left_generated := hFE }

/-- The quotient equality theorem of v1.81 and the order reflection theorem are
therefore literally the same identification criterion. -/
theorem presentationClass_eq_iff_generatedPresentationEquivalence
    (E F : MorphismProperty (ScaledSSet.{u})) :
    presentationClass E = presentationClass F <->
      GeneratedScaledAnodynePresentationEquivalence E F := by
  exact presentationClass_eq_iff E F

/-! ## Exact standard/canonical directional obligations -/

/-- The canonical quotient point lies below the standard A/B/C point exactly
when every *literal canonical composite generator* is standard-generated.
No factorization into scaling enrichment and induced attachment is logically
required by the order itself. -/
theorem canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated :
    canonicalKuuOSPresentation <= standardABCPresentation <->
      (scaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})) <=
        standardGeneratedScaledAnodyneABC := by
  simpa [canonicalKuuOSPresentation, standardABCPresentation,
    externalGeneratedScaledAnodyne, standardGeneratedScaledAnodyneABC] using
    (presentationClass_le_iff_generators_le_generated
      (scaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u}))
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))

/-- Conversely the standard A/B/C point lies below the canonical point exactly
when the literal standard A/B/C union is canonical-generated. -/
theorem standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated :
    standardABCPresentation <= canonicalKuuOSPresentation <->
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) <=
        (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u})) := by
  simpa [standardABCPresentation, canonicalKuuOSPresentation,
    externalGeneratedScaledAnodyne, canonicalGeneratedScaledAnodyne] using
    (presentationClass_le_iff_generators_le_generated
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
      (scaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})))

/-- The v1.79 four-field positive forward residual package is a sufficient
geometric route to the exact canonical-to-standard order direction. -/
theorem canonicalKuuOS_le_standardABC_of_positiveResidual
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    canonicalKuuOSPresentation <= standardABCPresentation := by
  apply
    canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated.2
  exact canonicalGenerators_le_standardGenerated_of_residual K.toResidual

/-- The reverse order direction is not merely implied by the generatorwise
v1.79 package: it is equivalent to it, because the standard presentation is
literally the A/B/C union. -/
theorem standardABC_le_canonicalKuuOS_iff_generatorwiseReverse :
    standardABCPresentation <= canonicalKuuOSPresentation <->
      StandardABCCanonicalGeneratorwiseReverseComparison.{u} := by
  rw [standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated]
  constructor
  · intro h
    exact
      { typeA_mem := fun g =>
          h _ (standardTypeAGenerator_mem_ABC g)
        typeB_mem :=
          h _ standardTypeBGenerator_mem_ABC
        typeC_mem := fun m =>
          h _ (standardTypeCGenerator_mem_ABC m) }
  · intro K
    exact K.toReverse.standardGenerators_le_canonicalGenerated

/-- Full presentation identification is exactly the two literal one-sided
generation statements.  This is the direct generator-level form of the
posetal-reflection equality criterion. -/
theorem standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions :
    standardABCPresentation = canonicalKuuOSPresentation <->
      ((standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})) <=
        (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u}))) /\
      ((scaledHornAttachmentGenerators :
          MorphismProperty (ScaledSSet.{u})) <=
        standardGeneratedScaledAnodyneABC) := by
  rw [standardABC_eq_canonical_iff_mutual_le,
    standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated,
    canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated]

/-- The positive v1.79 master package factors through the exact two order
directions, rather than being part of the definition of presentation equality. -/
theorem standardABC_eq_canonicalKuuOS_of_positiveComparison_via_order
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    standardABCPresentation = canonicalKuuOSPresentation := by
  apply standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions.2
  constructor
  · exact K.reverse.toReverse.standardGenerators_le_canonicalGenerated
  · exact canonicalGenerators_le_standardGenerated_of_residual
      K.forward.toResidual

/-!
The v1.84 comparison frontier is therefore smaller than the v1.79 proof
strategy:

```text
literal presentations E,F
  E ⪯ F  :<=>  E <= F.rlp.llp

quotient projection:
  [E] <= [F]  <=>  E ⪯ F

standard/canonical:
  canonical <= standard
    <=> canonical literal generators <= standardGenerated

  standard <= canonical
    <=> standard literal A/B/C generators <= canonicalGenerated
    <=> v1.79 generatorwise reverse package

  standard = canonical
    <=> both one-sided literal generation statements.
```

Consequently future geometric work is free to prove a canonical composite
generator standard-generated directly.  The scaling-enrichment / induced-map
split of v1.79 remains available when it is useful, but is no longer imposed by
the presentation-independent formulation.  The unconditional canonical WFS
and unconditional canonical endpoint theorem remain independent of either
comparison direction.
-/

end KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
