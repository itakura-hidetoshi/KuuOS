import KUOS.DependentOriginationExternalScaledDuskinFibrancyV1_47

namespace KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46

universe u

/-!
# Canonical scaled-attachment factorization v1.48

The external comparison interface of v1.46 asks for

`T ≤ E.rlp.llp`

for an external scaled-anodyne generator family `E`, where `T` is the KuuOS
family of minimally-scaled horn-cylinder attachments.

A direct comparison with the standard scaled-anodyne generators must account
for a genuine scaling difference.  The canonical KuuOS generator has minimal
scaling on its attachment source, while the cylinder carries the scaling
pulled back from its simplex coordinate.

This layer isolates that difference canonically.  For every generator we put
on the same underlying attachment the scaling induced by the cylinder
inclusion.  The original generator then factors as

```text
minimal attachment
  -- scaling enrichment -->
induced-scaled attachment
  -- induced inclusion -->
scaled cylinder.
```

Thus proving `T ≤ E.rlp.llp` splits into two independent geometric tasks:

1. the source scaling-enrichment maps lie in `E.rlp.llp`;
2. the induced attachment inclusions lie in `E.rlp.llp`.

The second piece is the one that can be compared to the standard type-(A)
inner-horn pushout-product geometry.  The first piece records exactly the extra
strength introduced by the KuuOS minimal source scaling.  No claim is made
here that either piece is already standard scaled-anodyne.
-/

/-! ## Pulling a scaling back along a simplicial map -/

/-- Pull a scaling on `Y` back along a simplicial map `f : X ⟶ Y`. -/
def pullbackScaling
    {X Y : SSet.{u}}
    (sY : ScaledSimplicialSet Y)
    (f : X ⟶ Y) : ScaledSimplicialSet X where
  thin := fun t => sY.thin (f.app _ t)
  thin_sigma_zero := by
    intro x
    rw [SSet.σ_naturality_apply f 0 x]
    exact sY.thin_sigma_zero _
  thin_sigma_one := by
    intro x
    rw [SSet.σ_naturality_apply f 1 x]
    exact sY.thin_sigma_one _

/-- The defining map of a pullback scaling is scaled by construction. -/
theorem pullbackScaling_map
    {X Y : SSet.{u}}
    (sY : ScaledSimplicialSet Y)
    (f : X ⟶ Y) :
    IsScaledMap (pullbackScaling sY f) sY f := by
  intro t ht
  exact ht

/-! ## The induced-scaled horn-cylinder attachment -/

/-- The scaling on the horn-cylinder attachment induced from the scaled
cylinder along the underlying inclusion. -/
def inducedHornCylinderAttachmentScaling
    {n : Nat}
    (i : Fin (n + 1))
    (ε : Fin 2)
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    ScaledSimplicialSet (hornCylinderAttachment n i ε : SSet.{u}) :=
  pullbackScaling (simplexCylinderScaling sΔ)
    (hornCylinderAttachment n i ε).ι

/-- The same underlying attachment as v1.41, now carrying the scaling induced
from the cylinder rather than the minimal scaling. -/
def inducedScaledHornCylinderAttachment
    {n : Nat}
    (i : Fin (n + 1))
    (ε : Fin 2)
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})) : ScaledSSet.{u} :=
  ScaledSSet.of (hornCylinderAttachment n i ε : SSet.{u})
    (inducedHornCylinderAttachmentScaling i ε sΔ)

/-- Enrich the minimal attachment scaling to the scaling induced from the
cylinder.  The underlying simplicial map is the identity. -/
def minimalToInducedHornCylinderAttachment
    {n : Nat}
    (i : Fin (n + 1))
    (ε : Fin 2)
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    minimallyScaledHornCylinderAttachment n i ε ⟶
      inducedScaledHornCylinderAttachment i ε sΔ where
  map := 𝟙 _
  scaled := minimalScaling_map _ _

/-- The induced-scaled attachment inclusion into the scaled cylinder. -/
def inducedScaledHornCylinderAttachmentInclusion
    {n : Nat}
    (i : Fin (n + 1))
    (ε : Fin 2)
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    inducedScaledHornCylinderAttachment i ε sΔ ⟶
      scaledSimplexCylinder sΔ where
  map := (hornCylinderAttachment n i ε).ι
  scaled := pullbackScaling_map _ _

/-- The canonical minimally-scaled attachment inclusion factors literally as
scaling enrichment followed by the induced-scaled inclusion. -/
theorem scaledHornCylinderAttachmentInclusion_factorization
    {n : Nat}
    (i : Fin (n + 1))
    (ε : Fin 2)
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    minimalToInducedHornCylinderAttachment i ε sΔ ≫
        inducedScaledHornCylinderAttachmentInclusion i ε sΔ =
      scaledHornCylinderAttachmentInclusion i ε sΔ := by
  apply ScaledSSet.ScaledMap.ext
  change
    𝟙 (hornCylinderAttachment n i ε : SSet.{u}) ≫
        (hornCylinderAttachment n i ε).ι =
      (hornCylinderAttachment n i ε).ι
  exact Category.id_comp _

/-! ## Factor the canonical generator family -/

/-- The source-scaling enrichment associated to a canonical generator index. -/
def scaledHornAttachmentScalingEnrichment
    (g : ScaledHornAttachmentGeneratorIndex.{u}) :
    minimallyScaledHornCylinderAttachment g.n g.i g.endpoint ⟶
      inducedScaledHornCylinderAttachment g.i g.endpoint g.simplexScaling :=
  minimalToInducedHornCylinderAttachment g.i g.endpoint g.simplexScaling

/-- The induced-scaled attachment inclusion associated to a canonical generator
index. -/
def inducedScaledHornAttachmentGeneratorHom
    (g : ScaledHornAttachmentGeneratorIndex.{u}) :
    inducedScaledHornCylinderAttachment g.i g.endpoint g.simplexScaling ⟶
      scaledSimplexCylinder g.simplexScaling :=
  inducedScaledHornCylinderAttachmentInclusion
    g.i g.endpoint g.simplexScaling

/-- All source-scaling enrichment maps. -/
def scaledHornAttachmentScalingEnrichments :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun g : ScaledHornAttachmentGeneratorIndex.{u} =>
      scaledHornAttachmentScalingEnrichment g)

/-- All induced-scaled attachment inclusions. -/
def inducedScaledHornAttachmentGenerators :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun g : ScaledHornAttachmentGeneratorIndex.{u} =>
      inducedScaledHornAttachmentGeneratorHom g)

/-- Every source-scaling enrichment lies in its generator property. -/
theorem scaledHornAttachmentScalingEnrichment_mem
    (g : ScaledHornAttachmentGeneratorIndex.{u}) :
    (scaledHornAttachmentScalingEnrichments : MorphismProperty (ScaledSSet.{u}))
      (scaledHornAttachmentScalingEnrichment g) :=
  MorphismProperty.ofHoms.mk g

/-- Every induced attachment inclusion lies in its generator property. -/
theorem inducedScaledHornAttachmentGenerator_mem
    (g : ScaledHornAttachmentGeneratorIndex.{u}) :
    (inducedScaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u}))
      (inducedScaledHornAttachmentGeneratorHom g) :=
  MorphismProperty.ofHoms.mk g

/-- Each original canonical generator is the composite of its scaling
enrichment and induced-scaled attachment inclusion. -/
theorem scaledHornAttachmentGeneratorHom_factorization
    (g : ScaledHornAttachmentGeneratorIndex.{u}) :
    scaledHornAttachmentScalingEnrichment g ≫
        inducedScaledHornAttachmentGeneratorHom g =
      scaledHornAttachmentGeneratorHom g := by
  exact scaledHornCylinderAttachmentInclusion_factorization
    g.i g.endpoint g.simplexScaling

/-! ## Refining the external comparison burden -/

/-- Factor-level data sufficient to prove the first inclusion in the v1.46
external comparison criterion. -/
structure CanonicalAttachmentFactorComparison
    (E : MorphismProperty (ScaledSSet.{u})) : Prop where
  scalingEnrichments_le_externalGenerated :
    (scaledHornAttachmentScalingEnrichments : MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne E
  inducedAttachments_le_externalGenerated :
    (inducedScaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne E

namespace CanonicalAttachmentFactorComparison

variable {E : MorphismProperty (ScaledSSet.{u})}

/-- If both factors are externally generated-anodyne, then every original
canonical attachment generator is externally generated-anodyne. -/
theorem canonicalGenerators_le_externalGenerated
    (K : CanonicalAttachmentFactorComparison E) :
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne E := by
  intro A B f hf
  dsimp [scaledHornAttachmentGenerators] at hf
  cases hf with
  | mk g =>
      rw [← scaledHornAttachmentGeneratorHom_factorization g]
      exact MorphismProperty.comp_mem
        (externalGeneratedScaledAnodyne E)
        (scaledHornAttachmentScalingEnrichment g)
        (inducedScaledHornAttachmentGeneratorHom g)
        (CanonicalAttachmentFactorComparison.scalingEnrichments_le_externalGenerated K _
          (scaledHornAttachmentScalingEnrichment_mem g))
        (CanonicalAttachmentFactorComparison.inducedAttachments_le_externalGenerated K _
          (inducedScaledHornAttachmentGenerator_mem g))

end CanonicalAttachmentFactorComparison

/-- A full external comparison can therefore be assembled from the two factor
inclusions plus the reverse generator inclusion already required in v1.46. -/
structure FactorizedScaledAnodyneGeneratorComparison
    (E : MorphismProperty (ScaledSSet.{u})) : Prop where
  factors : CanonicalAttachmentFactorComparison E
  externalGenerators_le_canonicalGenerated :
    E ≤ (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))

namespace FactorizedScaledAnodyneGeneratorComparison

variable
    {E : MorphismProperty (ScaledSSet.{u})}
    (K : FactorizedScaledAnodyneGeneratorComparison E)

/-- Factor-level comparison data canonically produces the exact v1.46
mutual-closure comparison certificate. -/
def toScaledAnodyneGeneratorComparison :
    ScaledAnodyneGeneratorComparison E where
  canonicalGenerators_le_externalGenerated :=
    K.factors.canonicalGenerators_le_externalGenerated
  externalGenerators_le_canonicalGenerated :=
    K.externalGenerators_le_canonicalGenerated

/-- Hence the external and canonical generated left classes agree. -/
theorem externalGeneratedScaledAnodyne_eq_canonical :
    externalGeneratedScaledAnodyne E =
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) :=
  K.toScaledAnodyneGeneratorComparison.externalGeneratedScaledAnodyne_eq_canonical

/-- And their right lifting classes agree. -/
theorem externalGeneratedScaledFibration_eq_canonical :
    externalGeneratedScaledFibration E =
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) :=
  K.toScaledAnodyneGeneratorComparison.externalGeneratedScaledFibration_eq_canonical

end FactorizedScaledAnodyneGeneratorComparison

/-!
The external comparison frontier has now been sharpened from one opaque
inclusion

```text
T ≤ E.rlp.llp
```

to two geometrically distinct inclusions

```text
scaling enrichments ≤ E.rlp.llp
induced attachments  ≤ E.rlp.llp.
```

For the standard scaled-anodyne generators, the induced-attachment side is the
natural location of the type-(A) inner-horn pushout-product argument.  The
scaling-enrichment side is a separate question and must not be silently folded
into that argument.
-/

end KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
