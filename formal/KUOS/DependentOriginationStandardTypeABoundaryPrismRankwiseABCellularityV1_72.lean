import KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71

universe u

noncomputable section

/-!
# Rankwise A/B cellularity of the standard type-(A) boundary prism v1.72

Version v1.71 lifted the ordinary Mathlib rank filtration to genuine
ambient-pullback-scaled stages and factored every exact rank cell as

```text
exact horn -- A cobase change --> A-target -- completion --> exact cell.
```

Version v1.70 had already proved that the completion is exhaustively one of

```text
identity, q12, q23.
```

This file converts that geometric classification into the *same cellular
language* used by the v1.59 endpoint certificate.  The important point is that
we do not replace the Mathlib rank filtration and we do not identify the
canonical KuuOS arbitrary-scaling generator family with the standard A/B/C
family.

We isolate the unretracted cellular core

```text
transfiniteCompositions (pushouts (coproducts E_std))
```

and prove:

* every cellwise A phase is one raw standard cellular step;
* q12 and q23 are one raw standard cellular step because they are literal
  pushouts of the standard type-(B) generator;
* transport from a dependent three-cell carrier to the fixed `Delta[3]`
  preserves the completion arrow up to an explicit arrow isomorphism;
* therefore every exact rank cell is a finite transfinite composite of raw
  standard A/B steps;
* consequently the entire rank-indexed exact cell family lands in the v1.59
  `standardABCCellularClosure`.

After this theorem no local q12/q23 calculation is allowed to reappear in the
global rank assembly: the remaining frontier is purely the simultaneous
rank-successor pushout and its natural-number transfinite composition.
-/

/-! ## The raw and strong standard cellular classes -/

/-- One raw standard cellular step: a pushout of a coproduct of standard
A/B/C generators. -/
@[reducible] def standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}) :=
  (MorphismProperty.coproducts.{u}
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u}))).pushouts

/-- The strong, unretracted standard cellular closure. -/
@[reducible] def standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.transfiniteCompositions.{u}
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))

/-- The strong cellular closure is contained in the v1.59 cellular closure by
the final retract operation. -/
theorem standardABCStrongCellularClosure_le_standardABCCellularClosure :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})) ≤
      standardABCCellularClosure := by
  intro X Y f hf
  exact MorphismProperty.le_retracts
    (MorphismProperty.transfiniteCompositions.{u}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))) f hf

/-! ## Every cellwise A phase is one raw standard cellular step -/

/-- The A phase of every exact boundary-prism cell is a pushout of one standard
type-(A) generator, hence already belongs to the raw standard cellular class. -/
theorem standardTypeABoundaryPrismCellAPushoutHom_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellAPushoutHom g j c) := by
  have hgen :
      (MorphismProperty.coproducts.{u}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})))
        (standardTypeAScaledHornGeneratorHom
          (standardTypeABoundaryPrismCellHornIndex g j c)) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAGenerator_mem_ABC
        (standardTypeABoundaryPrismCellHornIndex g j c))
  have hgen' :
      (MorphismProperty.coproducts.{u}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})))
        (scalingEnrichmentPushoutLowerMap c.horn.ι
          (standardTypeAHornInclusion_scaled c.index)) := by
    simpa only [standardTypeABoundaryPrismCellA_lowerMap_eq_generator g j c] using hgen
  exact MorphismProperty.pushouts_mk
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))
    (standardTypeABoundaryPrismCellA_genericPushout g j c
      (standardTypeABoundaryPrismCellACompatible_all g j c)).flip
    hgen'

/-! ## The two fixed B completions are also raw standard cellular steps -/

/-- The fixed q12 completion is literally a pushout of the standard type-(B)
generator. -/
theorem standardTypeBCollapse12CompletionHom_mem_rawCellular :
    standardABCRawCellularStep standardTypeBCollapse12CompletionHom.{u} := by
  have hB :
      (MorphismProperty.coproducts.{u}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))) standardTypeBGeneratorHom.{u} :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      standardTypeBGenerator_mem_ABC.{u}
  exact MorphismProperty.pushouts_mk
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))
    standardTypeBCollapse12Completion_isPushout.{u} hB

/-- The fixed q23 completion is literally a pushout of the standard type-(B)
generator. -/
theorem standardTypeBCollapse23CompletionHom_mem_rawCellular :
    standardABCRawCellularStep standardTypeBCollapse23CompletionHom.{u} := by
  have hB :
      (MorphismProperty.coproducts.{u}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))) standardTypeBGeneratorHom.{u} :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      standardTypeBGenerator_mem_ABC.{u}
  exact MorphismProperty.pushouts_mk
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))
    standardTypeBCollapse23Completion_isPushout.{u} hB

/-! ## Explicit carrier/scaling isomorphisms for the exceptional three-cells -/

/-- Equality of two scalings on a fixed carrier gives an isomorphism whose
underlying simplicial maps are literally identities.  Keeping this constructor
explicit avoids allowing equality transports to pollute the later arrow
comparison. -/
def scalingEqualityIso
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t) :
    ScaledSSet.of X s ≅ ScaledSSet.of X t := by
  cases h
  exact Iso.refl _

@[simp]
theorem scalingEqualityIso_hom_map
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t) :
    (scalingEqualityIso s t h).hom.map = 𝟙 X := by
  cases h
  rfl

@[simp]
theorem scalingEqualityIso_inv_map
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t) :
    (scalingEqualityIso s t h).inv.map = 𝟙 X := by
  cases h
  rfl

/-- One-shot isomorphism from a dependent actual three-cell carrier to the
fixed `Delta[3]` carrier carrying the v1.70 transported scaling. -/
private noncomputable def scalingIsoOfDimensionEq
    {n : ℕ} (h : n = 3)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    ScaledSSet.of (Δ[n] : SSet.{u}) s ≅
      ScaledSSet.of (Δ[3] : SSet.{u})
        (Eq.mp
          (congrArg (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) h) s) := by
  cases h
  exact Iso.refl _

noncomputable def standardTypeABoundaryPrismCellScalingIsoToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3)
    (s : ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u})) :
    ScaledSSet.of (Δ[c.dim + 1] : SSet.{u}) s ≅
      ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3 s) := by
  exact scalingIsoOfDimensionEq h3 s

/-! ## Explicit dimension-equality transport for completion morphisms -/

private noncomputable def scaledCompletionTransportOfDimensionEq
    {n : ℕ} (hn : n = 3)
    (s t : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (f : ScaledSSet.of (Δ[n] : SSet.{u}) s ⟶
      ScaledSSet.of (Δ[n] : SSet.{u}) t) :
    ScaledSSet.of (Δ[3] : SSet.{u})
        (Eq.mp (congrArg
          (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) hn) s) ⟶
      ScaledSSet.of (Δ[3] : SSet.{u})
        (Eq.mp (congrArg
          (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) hn) t) := by
  cases hn
  exact f

private noncomputable def scaledCompletionTransportArrowIsoOfDimensionEq
    {n : ℕ} (hn : n = 3)
    (s t : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (f : ScaledSSet.of (Δ[n] : SSet.{u}) s ⟶
      ScaledSSet.of (Δ[n] : SSet.{u}) t) :
    Arrow.mk f ≅
      Arrow.mk (scaledCompletionTransportOfDimensionEq hn s t f) := by
  cases hn
  exact Iso.refl _

/-- Transport the identity-underlying completion arrow itself to the fixed
three-simplex carrier. -/
noncomputable def standardTypeABoundaryPrismCellCompletionTransportToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3) :
    ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellAPushoutScaling g j c)) ⟶
      ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellScaling g j c)) := by
  exact scaledCompletionTransportOfDimensionEq h3
    (standardTypeABoundaryPrismCellAPushoutScaling g j c)
    (standardTypeABoundaryPrismCellScaling g j c)
    (standardTypeABoundaryPrismCellCompletionHom g j c)

/-- The actual dependent completion arrow and its fixed-three-simplex transport
are isomorphic as arrows. -/
noncomputable def standardTypeABoundaryPrismCellCompletionArrowIsoToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk
        (standardTypeABoundaryPrismCellCompletionTransportToThree g j c h3) := by
  exact scaledCompletionTransportArrowIsoOfDimensionEq h3
    (standardTypeABoundaryPrismCellAPushoutScaling g j c)
    (standardTypeABoundaryPrismCellScaling g j c)
    (standardTypeABoundaryPrismCellCompletionHom g j c)

/-! ## Typed invariance under dimension and scaling equalities -/

private noncomputable def scaledIdentityArrowIsoOfDimensionEq
    {n : ℕ} (hn : n = 3)
    (s t : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (s3 t3 : ScaledSimplicialSet (Δ[3] : SSet.{u}))
    (hs : Eq.mp
      (congrArg (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) hn) s = s3)
    (ht : Eq.mp
      (congrArg (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) hn) t = t3)
    (f : ScaledSSet.of (Δ[n] : SSet.{u}) s ⟶ ScaledSSet.of (Δ[n] : SSet.{u}) t)
    (f3 : ScaledSSet.of (Δ[3] : SSet.{u}) s3 ⟶ ScaledSSet.of (Δ[3] : SSet.{u}) t3)
    (hf : f.map = 𝟙 (Δ[n] : SSet.{u}))
    (hf3 : f3.map = 𝟙 (Δ[3] : SSet.{u})) :
    Arrow.mk f ≅ Arrow.mk f3 := by
  cases hn
  change s = s3 at hs
  change t = t3 at ht
  cases hs
  cases ht
  have hmap : f.map = f3.map := hf.trans hf3.symm
  have heq : f = f3 := by
    apply ScaledSSet.ScaledMap.ext
    exact hmap
  exact eqToIso (congrArg Arrow.mk heq)

private noncomputable def scaledArrowIsoOfTargetScalingEq
    {A : ScaledSSet.{u}} {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t)
    (f : A ⟶ ScaledSSet.of X s)
    (g : A ⟶ ScaledSSet.of X t)
    (hmap : f.map = g.map) :
    Arrow.mk f ≅ Arrow.mk g := by
  cases h
  have heq : f = g := by
    apply ScaledSSet.ScaledMap.ext
    exact hmap
  exact eqToIso (congrArg Arrow.mk heq)

/-! ## Exceptional completion arrows are fixed q12/q23 up to arrow isomorphism -/

/-- Source-object identification for a q12 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ12SourceIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse12BaseScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) ≪≫
    scalingEqualityIso _ _ h.A_base

/-- Target-object identification for a q12 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ12TargetIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardTypeABoundaryPrismScaledCellTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse12CompletedScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellScaling g j c) ≪≫
    scalingEqualityIso _ _ h.completed_target

/-- The actual q12 exceptional completion is arrow-isomorphic to the fixed
v1.57 q12 completion pushout. -/
noncomputable def standardTypeABoundaryPrismCellQ12CompletionArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk standardTypeBCollapse12CompletionHom.{u} := by
  exact scaledIdentityArrowIsoOfDimensionEq
    h.target_three
    (standardTypeABoundaryPrismCellAPushoutScaling g j c)
    (standardTypeABoundaryPrismCellScaling g j c)
    standardTypeBCollapse12BaseScaling
    standardTypeBCollapse12CompletedScaling
    h.A_base h.completed_target
    (standardTypeABoundaryPrismCellCompletionHom g j c)
    standardTypeBCollapse12CompletionHom.{u}
    (by rfl) (by rfl)

/-- Source-object identification for a q23 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ23SourceIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse23BaseScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) ≪≫
    scalingEqualityIso _ _ h.A_base

/-- Target-object identification for a q23 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ23TargetIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardTypeABoundaryPrismScaledCellTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse23CompletedScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellScaling g j c) ≪≫
    scalingEqualityIso _ _ h.completed_target

/-- The actual q23 exceptional completion is arrow-isomorphic to the fixed
v1.57 q23 completion pushout. -/
noncomputable def standardTypeABoundaryPrismCellQ23CompletionArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk standardTypeBCollapse23CompletionHom.{u} := by
  exact scaledIdentityArrowIsoOfDimensionEq
    h.target_three
    (standardTypeABoundaryPrismCellAPushoutScaling g j c)
    (standardTypeABoundaryPrismCellScaling g j c)
    standardTypeBCollapse23BaseScaling
    standardTypeBCollapse23CompletedScaling
    h.A_base h.completed_target
    (standardTypeABoundaryPrismCellCompletionHom g j c)
    standardTypeBCollapse23CompletionHom.{u}
    (by rfl) (by rfl)

/-- Every q12 exceptional completion is itself one raw standard cellular step. -/
theorem standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q12
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellCompletionHom g j c) := by
  exact
    ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
      (standardTypeABoundaryPrismCellQ12CompletionArrowIso g j c h)).2
      standardTypeBCollapse12CompletionHom_mem_rawCellular

/-- Every q23 exceptional completion is itself one raw standard cellular step. -/
theorem standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q23
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellCompletionHom g j c) := by
  exact
    ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
      (standardTypeABoundaryPrismCellQ23CompletionArrowIso g j c h)).2
      standardTypeBCollapse23CompletionHom_mem_rawCellular

/-! ## Pure A cells and complete exact-cell cellularity -/

/-- If no B completion is needed, the A-pushout arrow and the exact cell arrow
are isomorphic by the identity on the source and the scaling-equality
isomorphism on the target. -/
noncomputable def standardTypeABoundaryPrismCellPureAArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellAPushoutHom g j c) ≅
      Arrow.mk (standardTypeABoundaryPrismScaledCellHom g j c) := by
  exact scaledArrowIsoOfTargetScalingEq
    (standardTypeABoundaryPrismCellAPushoutScaling g j c)
    (standardTypeABoundaryPrismCellScaling g j c) h
    (standardTypeABoundaryPrismCellAPushoutHom g j c)
    (standardTypeABoundaryPrismScaledCellHom g j c) (by
      change c.horn.ι =
        (standardTypeABoundaryPrismRankFunction.{u} g).basicCell j c
      exact (standardTypeABoundaryPrism_basicCell_eq_typeA_underlying g j c).symm)

/-- Every exact boundary-prism rank cell lies in the strong unretracted
standard A/B cellular closure.  The proof uses exactly the exhaustive local
trichotomy and no additional geometric case. -/
theorem standardTypeABoundaryPrismScaledCellHom_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    standardABCStrongCellularClosure
      (standardTypeABoundaryPrismScaledCellHom g j c) := by
  have hAraw := standardTypeABoundaryPrismCellAPushoutHom_mem_rawCellular g j c
  have hA :
      standardABCStrongCellularClosure
        (standardTypeABoundaryPrismCellAPushoutHom g j c) :=
    MorphismProperty.le_transfiniteCompositions
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ hAraw
  rcases standardTypeABoundaryPrismCellCompletion_complete_classification
      g j c with hpure | h12 | h23
  · have hExactRaw :
        standardABCRawCellularStep
          (standardTypeABoundaryPrismScaledCellHom g j c) :=
      ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
        (standardTypeABoundaryPrismCellPureAArrowIso g j c hpure)).1 hAraw
    exact MorphismProperty.le_transfiniteCompositions _ _ hExactRaw
  · have hBraw :=
      standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q12
        g j c h12
    have hcomp :
        standardABCStrongCellularClosure
          (standardTypeABoundaryPrismCellAPushoutHom g j c ≫
            standardTypeABoundaryPrismCellCompletionHom g j c) := by
      change
        MorphismProperty.transfiniteCompositions.{u}
          (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
          (standardTypeABoundaryPrismCellAPushoutHom g j c ≫
            standardTypeABoundaryPrismCellCompletionHom g j c)
      exact
        (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions _ _)
          _
          (MorphismProperty.TransfiniteCompositionOfShape.ofOrderIso
            (.ofComp _ _ hAraw hBraw)
            (orderIsoShrink.{u} (Fin 3)).symm).mem
    simpa only [standardTypeABoundaryPrismScaledCellHom_factor_A_completion]
      using hcomp
  · have hBraw :=
      standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q23
        g j c h23
    have hcomp :
        standardABCStrongCellularClosure
          (standardTypeABoundaryPrismCellAPushoutHom g j c ≫
            standardTypeABoundaryPrismCellCompletionHom g j c) := by
      change
        MorphismProperty.transfiniteCompositions.{u}
          (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
          (standardTypeABoundaryPrismCellAPushoutHom g j c ≫
            standardTypeABoundaryPrismCellCompletionHom g j c)
      exact
        (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions _ _)
          _
          (MorphismProperty.TransfiniteCompositionOfShape.ofOrderIso
            (.ofComp _ _ hAraw hBraw)
            (orderIsoShrink.{u} (Fin 3)).symm).mem
    simpa only [standardTypeABoundaryPrismScaledCellHom_factor_A_completion]
      using hcomp

/-- Hence every exact boundary-prism rank cell lies in the precise v1.59
standard A/B/C cellular closure. -/
theorem standardTypeABoundaryPrismScaledCellHom_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    standardABCCellularClosure
      (standardTypeABoundaryPrismScaledCellHom g j c) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeABoundaryPrismScaledCellHom_mem_strongCellular g j c)

/-! ## Package every rank cell as one global indexed family -/

/-- Global index of all exact cells of the natural-number rank filtration. -/
def StandardTypeABoundaryPrismRankCellIndex
    (g : StandardTypeAHornAttachmentGeneratorIndex) : Type u :=
  Σ j : ℕ, (standardTypeABoundaryPrismRankFunction.{u} g).Cell j

/-- The complete family of exact pullback-scaled cells occurring anywhere in
the boundary-prism rank filtration. -/
def standardTypeABoundaryPrismExactScaledCellGenerators
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun γ : StandardTypeABoundaryPrismRankCellIndex g =>
      standardTypeABoundaryPrismScaledCellHom g γ.1 γ.2)

/-- Every exact cell in the entire Mathlib rank filtration is standard
A/B/C-cellular.  This is the global local-to-cellular exit theorem: subsequent
rank assembly can consume one uniform theorem and never reopen the q12/q23
classification. -/
theorem standardTypeABoundaryPrismExactScaledCellGenerators_le_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismExactScaledCellGenerators g :
      MorphismProperty (ScaledSSet.{u})) ≤ standardABCCellularClosure := by
  intro X Y f hf
  cases hf with
  | mk γ =>
      exact standardTypeABoundaryPrismScaledCellHom_mem_cellular
        g γ.1 γ.2

/-!
The local scaled geometry is now fully consumed by the cellular calculus:

```text
all rank cells
  = pure A  or  A;q12  or  A;q23
  -> each A phase is pushout(coproduct(E_std))
  -> each q12/q23 phase is pushout(coproduct(E_std))
  -> each exact cell is a finite transfinite composite of raw A/B steps
  -> every exact cell belongs to standardABCCellularClosure.
```

The next and only remaining endpoint-prism task is genuinely rankwise:
construct the simultaneous scaled successor square at every natural-number
rank, using the already fixed ordinary Mathlib rank pushout and the exact
ambient pullback scalings of v1.71, then take the natural-number transfinite
composition and feed it into
`StandardABCTypeAEndpointLeibnizCellularCertificate`.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
