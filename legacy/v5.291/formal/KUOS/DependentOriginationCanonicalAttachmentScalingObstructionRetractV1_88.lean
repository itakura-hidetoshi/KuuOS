import KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
import Mathlib.CategoryTheory.MorphismProperty.Retract

namespace KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open CartesianMonoidalCategory
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87

universe u

/-!
# Canonical attachment scaling obstruction retract v1.88

The canonical KuuOS attachment family allows an arbitrary scaling on every
simplex while keeping the horn-cylinder attachment source minimally scaled.
The comparison with the standard A/B/C presentation therefore contains a
potentially genuine scaling issue.

This file proves that the issue cannot be removed merely by avoiding the
factorization of v1.48.  For every simplex scaling `sDelta`, every horn index,
and either endpoint, the identity-underlying enrichment

```text
(Delta[n], minimal) -> (Delta[n], sDelta)
```

is an arrow retract of the corresponding canonical horn-cylinder attachment

```text
(minimal attachment) -> (Delta[n] x Delta[1], cylinder(sDelta)).
```

The retract is geometric.  The section uses the chosen endpoint face, while
the retraction uses first projection from the cylinder.  The endpoint face is
already contained in the attachment, so the same split diagram exists on both
source and target sides of the arrow.

Since every left orthogonal class is retract-stable, this gives an intrinsic
necessary condition for the unresolved canonical-to-standard comparison:
if every canonical attachment is standard-generated, then every arbitrary
simplex scaling enrichment is standard-generated.  Thus arbitrary scaling is
not only a bookkeeping field in one proof strategy; it is detected directly
by the canonical generator family itself.
-/

/-! ## Minimal-to-chosen simplex scaling enrichment -/

/-- A standard simplex equipped with the minimal scaling. -/
def minimallyScaledSimplex (n : Nat) : ScaledSSet.{u} :=
  ScaledSSet.of (Delta[n] : SSet.{u}) (minimalScaling _)

/-- Identity-underlying enrichment from the minimal simplex scaling to an
arbitrary chosen scaling. -/
def minimalToChosenSimplexScaling
    {n : Nat}
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    minimallyScaledSimplex n ⟶ scaledSimplex sDelta where
  map := 𝟙 _
  scaled := minimalScaling_map _ _

@[simp]
theorem minimalToChosenSimplexScaling_map
    {n : Nat}
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    (minimalToChosenSimplexScaling sDelta).map = 𝟙 _ := by
  rfl

/-! ## Endpoint section and first-projection retractions -/

/-- The endpoint simplex enters the attachment as a scaled map because its
source is minimally scaled. -/
noncomputable def minimalSimplexIntoAttachment
    (n : Nat)
    (i : Fin (n + 1))
    (endpoint : Fin 2) :
    minimallyScaledSimplex n ⟶
      minimallyScaledHornCylinderAttachment n i endpoint where
  map := endpointIntoAttachment n i endpoint
  scaled := minimalScaling_map _ _

/-- The chosen endpoint as a map from the arbitrarily scaled simplex into its
scaled cylinder. -/
noncomputable def chosenScaledEndpoint
    {n : Nat}
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u}))
    (endpoint : Fin 2) :
    scaledSimplex sDelta ⟶ scaledSimplexCylinder sDelta := by
  fin_cases endpoint
  · exact scaledEndpointZero sDelta
  · exact scaledEndpointOne sDelta

/-- First projection from the minimally scaled attachment back to the minimally
scaled simplex.  Minimal source scaling makes the projection automatically a
scaled map. -/
noncomputable def minimalAttachmentFirstProjection
    (n : Nat)
    (i : Fin (n + 1))
    (endpoint : Fin 2) :
    minimallyScaledHornCylinderAttachment n i endpoint ⟶
      minimallyScaledSimplex n where
  map :=
    (hornCylinderAttachment n i endpoint).ι ≫
      CartesianMonoidalCategory.fst _ _
  scaled := minimalScaling_map _ _

/-- First projection from the scaled cylinder to the chosen scaled simplex. -/
def scaledCylinderFirstProjection
    {n : Nat}
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    scaledSimplexCylinder sDelta ⟶ scaledSimplex sDelta where
  map := CartesianMonoidalCategory.fst _ _
  scaled := by
    intro t ht
    change sDelta.thin t.1 at ht
    simpa using ht

/-! ## The arrow retract -/

/-- The endpoint sections give a morphism in the arrow category from the
simplex scaling enrichment to the canonical attachment. -/
noncomputable def simplexScalingToAttachmentArrow
    {n : Nat}
    (i : Fin (n + 1))
    (endpoint : Fin 2)
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    Arrow.mk (minimalToChosenSimplexScaling sDelta) ⟶
      Arrow.mk (scaledHornCylinderAttachmentInclusion i endpoint sDelta) :=
  Arrow.homMk
    (minimalSimplexIntoAttachment n i endpoint)
    (chosenScaledEndpoint sDelta endpoint)
    (by
      apply ScaledSSet.ScaledMap.ext
      fin_cases endpoint <;>
        simp [minimalSimplexIntoAttachment, chosenScaledEndpoint,
          minimalToChosenSimplexScaling,
          scaledHornCylinderAttachmentInclusion])

/-- First projections give the reverse arrow-category morphism. -/
noncomputable def attachmentToSimplexScalingArrow
    {n : Nat}
    (i : Fin (n + 1))
    (endpoint : Fin 2)
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    Arrow.mk (scaledHornCylinderAttachmentInclusion i endpoint sDelta) ⟶
      Arrow.mk (minimalToChosenSimplexScaling sDelta) :=
  Arrow.homMk
    (minimalAttachmentFirstProjection n i endpoint)
    (scaledCylinderFirstProjection sDelta)
    (by
      apply ScaledSSet.ScaledMap.ext
      simp [minimalAttachmentFirstProjection, scaledCylinderFirstProjection,
        minimalToChosenSimplexScaling,
        scaledHornCylinderAttachmentInclusion, Category.assoc])

/-- The minimal-to-chosen simplex scaling enrichment is an arrow retract of
any canonical attachment carrying that simplex scaling. -/
noncomputable def minimalToChosenSimplexScaling_retractArrow
    {n : Nat}
    (i : Fin (n + 1))
    (endpoint : Fin 2)
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    RetractArrow
      (minimalToChosenSimplexScaling sDelta)
      (scaledHornCylinderAttachmentInclusion i endpoint sDelta) where
  i := simplexScalingToAttachmentArrow i endpoint sDelta
  r := attachmentToSimplexScalingArrow i endpoint sDelta
  retract := by
    apply Arrow.hom_ext
    · apply ScaledSSet.ScaledMap.ext
      fin_cases endpoint <;>
        simp [simplexScalingToAttachmentArrow,
          attachmentToSimplexScalingArrow,
          minimalSimplexIntoAttachment,
          minimalAttachmentFirstProjection,
          chosenScaledEndpoint,
          scaledCylinderFirstProjection,
          Category.assoc]
    · apply ScaledSSet.ScaledMap.ext
      fin_cases endpoint <;>
        simp [simplexScalingToAttachmentArrow,
          attachmentToSimplexScalingArrow,
          chosenScaledEndpoint,
          scaledCylinderFirstProjection]

/-! ## Retract-stable left classes see the scaling enrichment -/

/-- Any retract-stable morphism class containing one canonical attachment also
contains its endpoint-detected simplex scaling enrichment. -/
theorem minimalToChosenSimplexScaling_mem_of_attachment_mem
    (P : MorphismProperty (ScaledSSet.{u}))
    [P.IsStableUnderRetracts]
    {n : Nat}
    (i : Fin (n + 1))
    (endpoint : Fin 2)
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u}))
    (hmem : P (scaledHornCylinderAttachmentInclusion i endpoint sDelta)) :
    P (minimalToChosenSimplexScaling sDelta) := by
  exact MorphismProperty.of_retract
    (P := P)
    (minimalToChosenSimplexScaling_retractArrow i endpoint sDelta)
    hmem

/-- In particular every arbitrary simplex scaling enrichment belongs to the
canonical generated left class. -/
theorem minimalToChosenSimplexScaling_mem_canonicalGenerated
    {n : Nat}
    (sDelta : ScaledSimplicialSet (Delta[n] : SSet.{u})) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (minimalToChosenSimplexScaling sDelta) := by
  let g : ScaledHornAttachmentGeneratorIndex.{u} :=
    { n := n
      i := 0
      endpoint := 0
      simplexScaling := sDelta }
  apply minimalToChosenSimplexScaling_mem_of_attachment_mem
    (P := canonicalGeneratedScaledAnodyne)
    g.i g.endpoint sDelta
  exact scaledHornAttachmentGenerators_le_generated _
    (scaledHornAttachmentGenerator_mem g)

/-! ## Package all arbitrary simplex scaling enrichments -/

/-- Index for one arbitrary simplex scaling enrichment. -/
structure SimplexScalingEnrichmentIndex where
  n : Nat
  simplexScaling : ScaledSimplicialSet (Delta[n] : SSet.{u})

/-- The enrichment map represented by one index. -/
def simplexScalingEnrichmentHom
    (q : SimplexScalingEnrichmentIndex.{u}) :
    minimallyScaledSimplex q.n ⟶ scaledSimplex q.simplexScaling :=
  minimalToChosenSimplexScaling q.simplexScaling

/-- Morphism property consisting of all minimal-to-chosen simplex scaling
enrichments in every dimension. -/
def simplexScalingEnrichments : MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun q : SimplexScalingEnrichmentIndex.{u} =>
      simplexScalingEnrichmentHom q)

/-- Every indexed enrichment lies in the packaged family. -/
theorem simplexScalingEnrichment_mem
    (q : SimplexScalingEnrichmentIndex.{u}) :
    (simplexScalingEnrichments : MorphismProperty (ScaledSSet.{u}))
      (simplexScalingEnrichmentHom q) := by
  exact MorphismProperty.ofHoms.mk q

/-- The complete arbitrary-scaling enrichment family is already contained in
the canonical generated left class. -/
theorem simplexScalingEnrichments_le_canonicalGenerated :
    (simplexScalingEnrichments : MorphismProperty (ScaledSSet.{u})) ≤
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) := by
  intro X Y f hf
  dsimp [simplexScalingEnrichments] at hf
  cases hf with
  | mk q =>
      exact minimalToChosenSimplexScaling_mem_canonicalGenerated
        q.simplexScaling

/-! ## Necessary condition for canonical-to-standard comparison -/

/-- Direct inclusion of the canonical generators into the standard-generated
class forces every arbitrary simplex scaling enrichment to be
standard-generated. -/
theorem simplexScalingEnrichments_le_standardGenerated_of_canonicalGenerators_le
    (hcanonical :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC) :
    (simplexScalingEnrichments : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  intro X Y f hf
  dsimp [simplexScalingEnrichments] at hf
  cases hf with
  | mk q =>
      let g : ScaledHornAttachmentGeneratorIndex.{u} :=
        { n := q.n
          i := 0
          endpoint := 0
          simplexScaling := q.simplexScaling }
      apply minimalToChosenSimplexScaling_mem_of_attachment_mem
        (P := standardGeneratedScaledAnodyneABC)
        g.i g.endpoint q.simplexScaling
      exact hcanonical _ (scaledHornAttachmentGenerator_mem g)

/-- The quotient-order form of the same necessary condition. -/
theorem simplexScalingEnrichments_le_standardGenerated_of_canonicalKuuOS_le_standardABC
    (h : canonicalKuuOSPresentation ≤ standardABCPresentation) :
    (simplexScalingEnrichments : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  exact
    simplexScalingEnrichments_le_standardGenerated_of_canonicalGenerators_le
      (canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated.1 h)

/-- Hence the existing positive forward residual package necessarily implies
standard generation of every arbitrary simplex scaling enrichment. -/
theorem simplexScalingEnrichments_le_standardGenerated_of_positiveResidual
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    (simplexScalingEnrichments : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  exact
    simplexScalingEnrichments_le_standardGenerated_of_canonicalKuuOS_le_standardABC
      (canonicalKuuOS_le_standardABC_of_positiveResidual K)

/-! ## Obstruction form -/

/-- A single arbitrary simplex scaling enrichment outside the standard-generated
class prevents the canonical presentation from lying below the standard one. -/
theorem not_canonicalKuuOS_le_standardABC_of_scalingEnrichment_not_mem
    (q : SimplexScalingEnrichmentIndex.{u})
    (hnot :
      ¬ standardGeneratedScaledAnodyneABC
        (simplexScalingEnrichmentHom q)) :
    ¬ canonicalKuuOSPresentation ≤ standardABCPresentation := by
  intro h
  have hall :=
    simplexScalingEnrichments_le_standardGenerated_of_canonicalKuuOS_le_standardABC h
  exact hnot (hall _ (simplexScalingEnrichment_mem q))

/-- The same witness prevents collapse of the standard/canonical presentation
gap. -/
theorem not_standardCanonicalPresentationGapClosed_of_scalingEnrichment_not_mem
    (q : SimplexScalingEnrichmentIndex.{u})
    (hnot :
      ¬ standardGeneratedScaledAnodyneABC
        (simplexScalingEnrichmentHom q)) :
    ¬ StandardCanonicalPresentationGapClosed.{u} := by
  intro hgap
  have hcanonical :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC :=
    (standardCanonicalPresentationGapClosed_iff_direct_generator_inclusions.1 hgap).2
  have hall :=
    simplexScalingEnrichments_le_standardGenerated_of_canonicalGenerators_le
      hcanonical
  exact hnot (hall _ (simplexScalingEnrichment_mem q))

/-!
The forward comparison frontier now has an intrinsic lower bound on what any
proof must accomplish:

```text
canonical <= standard
  -> every canonical attachment is standard-generated
  -> every minimal-to-arbitrary simplex scaling enrichment is standard-generated.
```

The middle implication is the v1.84 order reflection.  The last implication is
the arrow retract proved here and therefore does not depend on the v1.48
factorization strategy.  A future comparison may still prove canonical
attachments directly, but it cannot thereby avoid the scaling content: the
endpoint/first-projection retract recovers that content from the composite
attachment itself.
-/

end KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
